"""Executable Le Potato HMI service entrypoint."""
import argparse
import uvicorn
from .config import Settings


def main():
    parser = argparse.ArgumentParser(description="Le Potato hardware HMI")
    parser.add_argument("--host", help="Bind address (default: localhost)")
    parser.add_argument("--port", type=int, help="HTTP port")
    args = parser.parse_args()
    settings = Settings.from_env()
    host = args.host or settings.host
    if host not in ("127.0.0.1", "localhost", "::1") and not settings.api_token:
        parser.error("Non-loopback binding requires HMI_API_TOKEN")
    uvicorn.run(
        "lepotato_hmi.application:create_app",
        factory=True,
        host=host,
        port=args.port or settings.port,
    )


if __name__ == "__main__":
    main()
