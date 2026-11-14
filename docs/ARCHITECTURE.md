# Architecture

```text
Serial discovery -----> event bus <----- MQTT broker
                           |
                    state projection
                           |
                   HTTP / WebSocket
                           |
              Dashboard + browser eyes
                           |
                  future LCD driver
```

This is a hardware **control plane**, not a hard realtime machine controller.

* `events.py`: bounded event history, separate subscriber queues.
* `serial_devices.py`: enumerates Linux USB serial interfaces without opening them.
* `mqtt.py`: brokers messaging; MQTT callbacks marshal into asyncio.
* `emotions.py`: deterministic event-to-expression mapping.
* `application.py`: API and background discovery.
* `static/`: zero-build status dashboard and animated eye simulator.

## Event contract

Events have the structure `{kind, source, payload, timestamp}`. Typical kinds: `device.discovered`, `device.disconnected`, `mqtt.message`, `test.started`, `test.passed`, `test.failed`. They are currently stored in a 250-event in-memory ring buffer. MQTT payloads are capped to 8 KiB when displayed; truncation is identified.

## Extensibility

Add adapters which emit standard events. Do not have protocol adapters import display code. Add optional display drivers when the screen controller, bus and safe electrical configuration are known. Add test fixtures with explicit allowlisted port ownership and safe command boundaries. A full physical test runner requires safety checks, timeout handling, disconnection recovery and reproducible scenarios before enabling writes.

## Security

The sample development broker is localhost-only. Do not expose anonymous MQTT brokers to LAN clients. HTTP defaults to loopback; external HTTP use requires credentials and TLS termination. The local web UI is not an authenticated remote dashboard. Do not bypass machine-side E-stop, limits, or interlocks.
