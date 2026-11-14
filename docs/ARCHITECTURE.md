# Architecture

```text
Serial enumeration -----> event bus <----- MQTT bridge <--- Mosquitto
                              |
                       state projection
                              |
                       HTTP / Web API
                              |
                       Browser dashboard
                       Expression engine
                              |
                   future physical LCD driver
```

This is a supervisory device interaction platform, **not** an industrial safety controller.

### Components
- `serial_devices.py`: read-only serial enumeration; no automatic USB mounts in the Docker profile.
- `events.py`: bounded in-memory history and independent subscriber queues.
- `mqtt.py`: async/threadsafe bridge to Mosquitto; subscribed to the configured topic prefix.
- `emotions.py`: deterministic event → visual expression mapping.
- `application.py`: test simulation, event polling, API routes and authentication checks.
- `static/`: lightweight browser dashboard and eyes.
- `compose.yaml`: local Docker orchestrator with private broker and local-only HTTP publication.

### Event schema

`{"kind": "test.passed", "source": "simulator", "payload": {"name": "fixture"}, "timestamp": "..."}`.

Recent events are a bounded in-memory ring (250 entries), **not a database**. MQTT inbound payload display is capped; QoS0 is not durable.

### Security boundaries

The browser uses a Bearer token to access APIs and receives it from a local login form; this is an early local development experience, not an SSO system. Never publish the web port directly to untrusted networks. Use localhost / SSH tunneling for remote access. Broker is private to the Compose bridge but anonymous inside it; do not add unknown containers to the bridge. Hardware device access is disabled in Compose by default, and firmware writing, active tests and real-time machine movement are outside the current scope.

See [Docker deployment](DOCKER.md), [hardware](HARDWARE.md), and [roadmap](ROADMAP.md).
