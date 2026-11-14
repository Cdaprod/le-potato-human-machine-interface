# Roadmap

## v0.1: foundation
- [x] Installable Python package and CLI
- [x] HTTP API and browser dashboard with expressive eyes
- [x] Read-only USB serial device discovery
- [x] MQTT publish/subscribe integration
- [x] Bounded in-memory event bus
- [x] Simulated test events
- [x] Contribution docs, test scaffolding and CI
- [ ] Physical Le Potato validation, boot service verification
- [ ] MQTT integration test in CI against actual Mosquitto

## v0.2: hardware testing
- [ ] Test fixtures and explicit device adapters
- [ ] Port ownership, permissions, serial terminal and bounded commands
- [ ] SQLite event history with retention limits
- [ ] Reproducible scripted test scenarios
- [ ] Diagnostic exports and trace capture

## v0.3: eyes / physical expression
- [ ] Identify GPIO LCD controller and wiring
- [ ] Create optional framebuffer/I2C/SPI driver backend
- [ ] Configurable expression rules, easing, attention and timeouts
- [ ] Authenticated browser sessions and secure LAN dashboard

## v1.0: community
- [ ] Stable event schemas and plugin interfaces
- [ ] Release automation and verified deployment recipes
- [ ] Example adapters for ESP-IDF, CircuitPython, GRBL and OctoPrint
- [ ] Hardware capability manifests and docs for contributor boards
