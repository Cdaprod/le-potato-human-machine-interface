# Contributing

Thanks for helping build an open hardware HMI platform.

1. Open an issue for changes that affect public APIs, protocols or new hardware support.
2. Fork, create a focused feature branch, and open a PR with a problem statement.
3. Create a virtual environment and install with `pip install -e '.[dev]'`.
4. Run `ruff check .` and `pytest -q`.
5. Include hardware-independent tests; CI should not need an actual Le Potato.
6. When adding a hardware adapter, identify board model, kernel, GPIO voltage, display/driver model, pin mapping, and proof of validation.
7. Keep interface, event bus, tests and device-specific drivers separated.

Never commit credentials, network secrets, unique device IDs, private serial logs or access tokens. Do not send arbitrary hardware signals without validating voltage/current limits.

Security reports should be sent privately to maintainers rather than posted as exploitable public issues.
