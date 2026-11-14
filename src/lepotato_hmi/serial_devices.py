"""Read-only USB serial enumeration. No port opening, flashing, or hardware writes."""
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Device:
    path: str
    description: str
    hwid: str
    vid: int | None
    pid: int | None

    def serialize(self) -> dict:
        return asdict(self)


def discover() -> list[Device]:
    try:
        from serial.tools import list_ports
    except ImportError:
        return []
    return [
        Device(p.device, p.description, p.hwid, p.vid, p.pid)
        for p in list_ports.comports()
    ]
