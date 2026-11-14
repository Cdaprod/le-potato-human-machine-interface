"""Event-to-expression state projection. No artificial emotional intelligence implied."""
from dataclasses import dataclass
from .events import Event


@dataclass
class Expression:
    mood: str = "idle"
    detail: str = "Observing"


MAPPINGS = {
    "device.discovered": ("curious", "New device detected"),
    "device.disconnected": ("concerned", "Device disconnected"),
    "test.started": ("focused", "Test in progress"),
    "test.passed": ("happy", "Test passed"),
    "test.failed": ("concerned", "Test failed"),
    "mqtt.connected": ("happy", "MQTT connected"),
    "mqtt.disconnected": ("concerned", "MQTT unavailable"),
    "system.error": ("concerned", "System error"),
}


class EmotionEngine:
    def __init__(self):
        self.expression = Expression()

    def apply(self, event: Event) -> Expression:
        if event.kind in MAPPINGS:
            mood, detail = MAPPINGS[event.kind]
            self.expression = Expression(mood, detail)
        return self.expression
