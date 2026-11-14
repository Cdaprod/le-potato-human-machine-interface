"""A bounded in-memory bus with independent subscriber queues."""
import asyncio
from collections import deque
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class Event:
    kind: str
    source: str
    payload: dict[str, Any]
    timestamp: str

    @classmethod
    def build(cls, kind: str, source: str, payload: dict[str, Any]) -> "Event":
        return cls(kind, source, payload, datetime.now(timezone.utc).isoformat())

    def serialize(self) -> dict[str, Any]:
        return asdict(self)


class EventBus:
    def __init__(self, capacity: int = 250):
        self.history: deque[Event] = deque(maxlen=capacity)
        self.subscribers: set[asyncio.Queue[Event]] = set()

    def publish(self, event: Event) -> None:
        self.history.append(event)
        for queue in tuple(self.subscribers):
            if queue.full():
                try:
                    queue.get_nowait()
                except asyncio.QueueEmpty:
                    pass
            queue.put_nowait(event)

    def subscribe(self, capacity: int = 100) -> asyncio.Queue[Event]:
        queue: asyncio.Queue[Event] = asyncio.Queue(maxsize=capacity)
        self.subscribers.add(queue)
        return queue

    def unsubscribe(self, queue: asyncio.Queue[Event]) -> None:
        self.subscribers.discard(queue)
