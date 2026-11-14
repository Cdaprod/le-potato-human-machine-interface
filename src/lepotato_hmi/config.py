"""Runtime settings. Environment variables can be injected using systemd."""
import os
from dataclasses import dataclass


def truthy(name: str, default: bool) -> bool:
    return os.getenv(name, str(default)).lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    host: str = "127.0.0.1"
    port: int = 8080
    mqtt_host: str = "127.0.0.1"
    mqtt_port: int = 1883
    mqtt_username: str = ""
    mqtt_password: str = ""
    mqtt_topic_prefix: str = "benchlab"
    mqtt_enabled: bool = True
    serial_enabled: bool = True
    api_token: str = ""

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            host=os.getenv("HMI_HOST", "127.0.0.1"),
            port=int(os.getenv("HMI_PORT", "8080")),
            mqtt_host=os.getenv("HMI_MQTT_HOST", "127.0.0.1"),
            mqtt_port=int(os.getenv("HMI_MQTT_PORT", "1883")),
            mqtt_username=os.getenv("HMI_MQTT_USERNAME", ""),
            mqtt_password=os.getenv("HMI_MQTT_PASSWORD", ""),
            mqtt_topic_prefix=os.getenv("HMI_MQTT_TOPIC_PREFIX", "benchlab").strip("/"),
            mqtt_enabled=truthy("HMI_MQTT_ENABLED", True),
            serial_enabled=truthy("HMI_SERIAL_ENABLED", True),
            api_token=os.getenv("HMI_API_TOKEN", ""),
        )
