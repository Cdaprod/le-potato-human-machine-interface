# Docker deployment

## Threat model

Compose provides a local development deployment of the HMI and a private development Mosquitto instance. It is **not** a secure multi-tenant broker, a production authentication system or a safe machine-control environment.

- Web port binds to `127.0.0.1:8080` on the host.
- Web/API requests use a Bearer token after local browser login.
- Browser token is kept in tab session storage; avoid untrusted browser extensions or cross-origin injection.
- All browser assets are local static files.
- No host GPIO, USB, Docker socket, privileged mode or host networking is mounted.
- MQTT is an anonymous listener inside Compose's private default network. Any container joined to that network could access it; avoid doing so.
- No database, retention, backup or authentication service is configured.

The health endpoint intentionally returns a minimal unauthenticated `{"status":"ok"}` so container healthchecks can function; other API endpoints require the configured token.

## Start

```bash
cp .env.example .env
# Edit .env: HMI_API_TOKEN must be a strong, nonempty random value.
docker compose config --quiet
docker compose up --build -d
docker compose ps
```

Open http://127.0.0.1:8080 and authenticate with your configured token. Do not forward the port directly over the public internet.

## Remote access over SSH

```bash
ssh -L 8080:127.0.0.1:8080 user@your-le-potato
```

Use http://127.0.0.1:8080 from the SSH client. A hardened TLS reverse proxy plus documented authenticated sessions is future work.

## Hardware / SBC constraints

The Docker image is multi-stage, runs as non-root uid 10001, drops privileges and uses a read-only root filesystem. Building the image on the Le Potato requires a working ARM64 container runtime, adequate storage and sufficient memory. The configuration has **not been tested on the physical Le Potato**.

Host serial discovery is disabled by default. For specific verified USB adapters, create a locally maintained `compose.override.yaml` and grant the minimum required devices and group permissions. Do not use `privileged: true`, blanket `/dev` access or `network_mode: host`.

The tiny GPIO-connected LCD is not configured, since its exact controller, bus and wiring are unknown.

## Commands

```bash
docker compose logs --tail=200 -f hmi
docker compose up --build -d
docker compose down
```

## Production hardening checklist

- [ ] Provision authenticated MQTT users and restrict topics (ACL).
- [ ] Terminate HTTPS and expose only authenticated UI routes through a gateway.
- [ ] Implement proper server-side sessions / CSRF policy before shared-user deployments.
- [ ] Pin and review container image digests and dependencies.
- [ ] Add artifact provenance, SBOM and vulnerability scanning.
- [ ] Configure backups and retention once persistent events are implemented.
- [ ] Add hardware-specific tests, startup checks and power-loss recovery.

See [architecture](ARCHITECTURE.md) and [hardware](HARDWARE.md) for integration contracts.
