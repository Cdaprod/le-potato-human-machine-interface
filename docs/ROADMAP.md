# Roadmap

## v0.1 — software foundation
- [x] Installable Python package, CLI, REST API and simulation
- [x] Event bus, read-only serial enumeration and MQTT bridge
- [x] Expressive browser eyes linked to system events
- [x] Community scaffolding and Python CI
- [x] Multi-stage container build, Compose example, Docker smoke-test workflow
- [ ] Validate actual Docker deployment on Le Potato hardware
- [ ] Broker integration testing in CI against real Mosquitto

## v0.2 — embedded diagnostics
- [ ] Device capability registry and USB by-id discovery
- [ ] Explicit device ownership, bounded test commands and fixture definitions
- [ ] Persistent event history with retention controls
- [ ] Authenticated, authorization-aware LAN dashboard and MQTT service
- [ ] Portable diagnostics export

## v0.3 — expressive interface
- [ ] Verify GPIO-connected LCD controller, resolution and pin mapping
- [ ] Implement optional I2C/SPI LCD renderer without coupling to the backend
- [ ] Configurable behavior state machine with easing/blink timing
- [ ] Adaptive events and user-driven attention triggers

## v1.0 — community platform
- [ ] Stable plugin/adapter API with protocol contract tests
- [ ] ARM64 hardware CI and documented production deployment
- [ ] Sample integrations for CircuitPython, ESP-IDF, GRBL and OctoPrint
- [ ] Supply-chain signing, SBOM and security review
