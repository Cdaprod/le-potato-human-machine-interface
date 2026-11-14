# Le Potato HMI 🥔

**A Linux-native hardware testing and MQTT messaging dashboard with expressive status eyes.**

[![CI](https://github.com/Cdaprod/le-potato-human-machine-interface/actions/workflows/ci.yml/badge.svg)](https://github.com/Cdaprod/le-potato-human-machine-interface/actions/workflows/ci.yml)

Originally a CNC control-console concept, this repository now provides a reusable, device-agnostic interaction platform for embedded devices. It targets the Libre Computer **Le Potato**, but Linux SBCs and desktops are supported for development. **The little LCD eyes are an optional interface, not the project’s purpose.**

## Capabilities

| Feature | Current state |
|---|---|
| Browser testing and messaging dashboard | Initial implementation |
| Animated eyes with event-to-expression mappings | Browser simulator |
| HTTP API, OpenAPI docs, recent event history | Implemented |
| USB serial enumeration | Read-only discovery |
| MQTT publish/subscribe through Mosquitto | Implemented; needs broker |
| Simulated test events | Implemented |
| Physical GPIO LCD driver | Planned; display controller unknown |
| Firmware flashing and active device tests | Planned; not implemented |

No initial code writes to physical serial ports or drives CNC motion. The expression engine maps events to visual states deterministically; it is not an AI sentiment model.

## Quick start (Python 3.10+)

```bash
git clone https://github.com/Cdaprod/le-potato-human-machine-interface.git
cd le-potato-human-machine-interface
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[dev]'
HMI_MQTT_ENABLED=false lepotato-hmi
```

Open **http://127.0.0.1:8080**. Simulate passing/failing tests and watch the animated eyes react. API documentation lives at **/docs**.

### Optional MQTT broker for local development

```bash
docker compose -f deploy/compose.yaml up -d
lepotato-hmi
```

This example broker binds **only to localhost** and intentionally allows anonymous clients **for development only**. Never expose it to your LAN or the internet without provisioning credentials, network restrictions and TLS. To publish a sample message:

```bash
mosquitto_pub -h 127.0.0.1 -t benchlab/demo/status -m '{"online":true}'
```

The dashboard still works with MQTT disabled/disconnected. The default MQTT topic prefix is `benchlab/`.

## Configuration and security

See [`.env.example`](.env.example). This app reads the process environment; it does **not** automatically load dotenv files. The dashboard binds only to loopback by default. If you explicitly bind externally, configure `HMI_API_TOKEN` and put an authenticated HTTPS reverse proxy in front of it; the browser UI is designed for localhost **without** bearer-token authentication at this stage. The API supports Bearer authorization for scripted clients.

Never attach unknown voltages to SBC GPIO. The MQTT bridge and simulated testing do not implement realtime motion control, hardware interlocks or E-stop behavior. GRBL and printer controllers remain authoritative for those functions. Event history is bounded and in-memory, and MQTT QoS0 is not durable.

## Repository layout

```text
src/lepotato_hmi/
  config.py             Environment settings
  application.py        API, lifecycle and polling
  cli.py                Entrypoint
  events.py             Bounded event bus
  emotions.py           Expression projection
  mqtt.py               MQTT publish/subscribe bridge
  serial_devices.py     Read-only USB serial enumeration
  static/               Browser dashboard + eyes simulator
tests/                  Hardware-independent tests
deploy/                 Loopback-only development MQTT broker
systemd/                Optional dedicated Linux service
docs/                   Architecture, hardware, roadmap and history
.github/                CI, templates, contributor workflow
images/                 Original enclosure photography
```

The original CNC console proposal is preserved at [docs/history/CNC_CONSOLE_PLAN.md](docs/history/CNC_CONSOLE_PLAN.md), linked to the original Git commit and retained images.

## Development

```bash
ruff check .
pytest -q
```

Hardware verification and MQTT integration tests remain outstanding. For reproducible community contributions, see [CONTRIBUTING.md](CONTRIBUTING.md), [architecture](docs/ARCHITECTURE.md), and [roadmap](docs/ROADMAP.md). Licensed under [MIT](LICENSE).

## Systemd deployment

The `systemd/lepotato-hmi.service` example assumes a dedicated system user `lepotato-hmi`, a venv at `/opt/lepotato-hmi/.venv`, and `/etc/lepotato-hmi.env`. It is a service **template**, not an automated installer. Physical LCD drivers are intentionally excluded until the controller and connections are verified.
