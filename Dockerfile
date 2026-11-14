# syntax=docker/dockerfile:1
FROM python:3.12-slim-bookworm AS builder
WORKDIR /app
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
COPY pyproject.toml README.md LICENSE ./
COPY src ./src
RUN pip wheel --no-cache-dir --wheel-dir /wheels .

FROM python:3.12-slim-bookworm
LABEL org.opencontainers.image.source="https://github.com/Cdaprod/le-potato-human-machine-interface" \
      org.opencontainers.image.description="Cdaprod embedded-device HMI and MQTT testing dashboard" \
      org.opencontainers.image.licenses="MIT"
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HMI_HOST=0.0.0.0 \
    HMI_PORT=8080
RUN groupadd --system --gid 10001 hmi && useradd --system --uid 10001 --gid hmi --home-dir /nonexistent --shell /usr/sbin/nologin hmi
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir --no-index --find-links=/wheels lepotato-hmi && rm -rf /wheels
USER 10001:10001
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD python -c "import urllib.request;urllib.request.urlopen('http://127.0.0.1:8080/api/health',timeout=3)" || exit 1
CMD ["lepotato-hmi"]
