"""FastAPI application, simulator, device polling and MQTT event projection."""
import asyncio
import hmac
import logging
from contextlib import asynccontextmanager
from dataclasses import asdict
from pathlib import Path
from typing import Any
from fastapi import Depends, FastAPI, Header, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from .config import Settings
from .emotions import EmotionEngine
from .events import Event, EventBus
from .mqtt import MQTTBridge
from .serial_devices import discover

logger = logging.getLogger(__name__)
STATIC = Path(__file__).parent / "static"


class Message(BaseModel):
    topic: str = Field(min_length=1, max_length=255)
    payload: Any


class TestEvent(BaseModel):
    kind: str = Field(pattern=r"^test\.(started|passed|failed)$")
    name: str = Field(min_length=1, max_length=100)


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings.from_env()
    bus = EventBus()
    engine = EmotionEngine()
    bridge = MQTTBridge(settings, bus) if settings.mqtt_enabled else None

    def emit(kind: str, source: str, payload: dict[str, Any]):
        event = Event.build(kind, source, payload)
        bus.publish(event)
        engine.apply(event)

    async def watch_emotions():
        queue = bus.subscribe()
        try:
            while True:
                engine.apply(await queue.get())
        finally:
            bus.unsubscribe(queue)

    async def watch_devices():
        known: set[str] = set()
        while True:
            current = {device.path for device in discover()} if settings.serial_enabled else set()
            for path in sorted(current - known):
                emit("device.discovered", "serial", {"path": path})
            for path in sorted(known - current):
                emit("device.disconnected", "serial", {"path": path})
            known = current
            await asyncio.sleep(5)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        tasks = [
            asyncio.create_task(watch_emotions()),
            asyncio.create_task(watch_devices()),
        ]
        if bridge:
            try:
                bridge.start(asyncio.get_running_loop())
            except Exception:
                logger.exception("MQTT initialization failed")
                emit("mqtt.disconnected", "mqtt", {"reason": "startup failed"})
        yield
        if bridge:
            bridge.stop()
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)

    app = FastAPI(title="Le Potato HMI", version="0.1.0", lifespan=lifespan)

    def require_token(authorization: str | None = Header(default=None)):
        if not settings.api_token:
            if settings.host not in ("127.0.0.1", "localhost", "::1"):
                raise HTTPException(503, "Set HMI_API_TOKEN before non-loopback binding")
            return
        if not authorization or not hmac.compare_digest(
            authorization, f"Bearer {settings.api_token}"
        ):
            raise HTTPException(401, "Invalid API token")

    app.mount("/static", StaticFiles(directory=STATIC), name="static")

    @app.get("/")
    def home():
        return FileResponse(STATIC / "index.html")

    @app.get("/api/health", dependencies=[Depends(require_token)])
    def health():
        return {"status": "ok", "mqtt_connected": bool(bridge and bridge.connected)}

    @app.get("/api/status", dependencies=[Depends(require_token)])
    def status():
        return {
            "expression": asdict(engine.expression),
            "mqtt_connected": bool(bridge and bridge.connected),
            "events": len(bus.history),
        }

    @app.get("/api/devices", dependencies=[Depends(require_token)])
    def devices():
        return [device.serialize() for device in discover()] if settings.serial_enabled else []

    @app.get("/api/events", dependencies=[Depends(require_token)])
    def events():
        return [event.serialize() for event in reversed(bus.history)]

    @app.post("/api/test-event", dependencies=[Depends(require_token)])
    def test_event(value: TestEvent):
        emit(value.kind, "simulator", {"name": value.name})
        return {"accepted": True}

    @app.post("/api/mqtt/publish", dependencies=[Depends(require_token)])
    def publish(value: Message):
        if not bridge or not bridge.connected:
            raise HTTPException(503, "MQTT broker unavailable")
        try:
            bridge.publish(value.topic, value.payload)
        except ValueError as exc:
            raise HTTPException(400, str(exc)) from exc
        except RuntimeError as exc:
            raise HTTPException(503, str(exc)) from exc
        return {"accepted": True}

    @app.websocket("/ws/events")
    async def websocket_events(ws: WebSocket):
        auth = ws.headers.get("authorization", "")
        if settings.api_token:
            if not hmac.compare_digest(auth, f"Bearer {settings.api_token}"):
                await ws.close(code=1008)
                return
        elif settings.host not in ("127.0.0.1", "localhost", "::1"):
            await ws.close(code=1008)
            return
        await ws.accept()
        queue = bus.subscribe()
        try:
            while True:
                await ws.send_json((await queue.get()).serialize())
        except WebSocketDisconnect:
            pass
        finally:
            bus.unsubscribe(queue)

    return app
