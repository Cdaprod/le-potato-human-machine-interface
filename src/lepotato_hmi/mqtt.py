"""MQTT bridge. Paho thread callbacks enter the owner asyncio event loop."""
import asyncio
import json
from typing import Any

import paho.mqtt.client as mqtt

from .config import Settings
from .events import Event, EventBus


class MQTTBridge:
    def __init__(self, settings: Settings, bus: EventBus):
        self.settings = settings
        self.bus = bus
        self.loop: asyncio.AbstractEventLoop | None = None
        self.connected = False
        self.client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2, client_id="lepotato-hmi"
        )
        if settings.mqtt_username:
            self.client.username_pw_set(settings.mqtt_username, settings.mqtt_password)
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message

    def _emit(self, kind: str, payload: dict[str, Any]) -> None:
        if self.loop:
            self.loop.call_soon_threadsafe(
                self.bus.publish, Event.build(kind, "mqtt", payload)
            )

    def _on_connect(self, client, userdata, flags, reason_code, properties):
        self.connected = not reason_code.is_failure
        if self.connected:
            client.subscribe(f"{self.settings.mqtt_topic_prefix}/#")
        self._emit(
            "mqtt.connected" if self.connected else "mqtt.disconnected",
            {"reason": str(reason_code)},
        )

    def _on_disconnect(self, client, userdata, flags, reason_code, properties):
        self.connected = False
        self._emit("mqtt.disconnected", {"reason": str(reason_code)})

    def _on_message(self, client, userdata, message):
        raw = message.payload[:8192]
        decoded = raw.decode("utf-8", errors="replace")
        try:
            payload = json.loads(decoded)
        except json.JSONDecodeError:
            payload = decoded
        self._emit("mqtt.message", {
            "topic": message.topic,
            "payload": payload,
            "truncated": len(message.payload) > len(raw),
        })

    def start(self, loop: asyncio.AbstractEventLoop) -> None:
        self.loop = loop
        self.client.connect_async(
            self.settings.mqtt_host, self.settings.mqtt_port, keepalive=30
        )
        self.client.loop_start()

    def stop(self) -> None:
        self.client.disconnect()
        self.client.loop_stop()

    def publish(self, topic: str, payload: Any) -> None:
        prefix = self.settings.mqtt_topic_prefix + "/"
        if (
            not topic.startswith(prefix)
            or "#" in topic
            or "+" in topic
            or chr(0) in topic
        ):
            raise ValueError(f"Topics must be under {prefix} without wildcards")
        result = self.client.publish(
            topic, json.dumps(payload, separators=(",", ":")), qos=0
        )
        if result.rc != mqtt.MQTT_ERR_SUCCESS:
            raise RuntimeError(
                f"MQTT publish rejected: {mqtt.error_string(result.rc)}"
            )
