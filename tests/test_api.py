from fastapi.testclient import TestClient
from lepotato_hmi.application import create_app
from lepotato_hmi.config import Settings


def test_health_and_simulated_events():
    app = create_app(Settings(mqtt_enabled=False, serial_enabled=False))
    with TestClient(app) as client:
        assert client.get("/api/health").json()["status"] == "ok"
        assert client.post(
            "/api/test-event", json={"kind": "test.passed", "name": "smoke"}
        ).status_code == 200
        assert client.get("/api/status").json()["expression"]["mood"] == "happy"
        assert client.get("/api/events").json()[0]["kind"] == "test.passed"
        assert client.get("/api/devices").json() == []
        assert client.post(
            "/api/test-event", json={"kind": "device.discovered", "name": "x"}
        ).status_code == 422


def test_optional_bearer_token():
    app = create_app(Settings(mqtt_enabled=False, serial_enabled=False, api_token="secret"))
    with TestClient(app) as client:
        assert client.get("/api/status").status_code == 401
        assert client.get(
            "/api/status", headers={"Authorization": "Bearer secret"}
        ).status_code == 200


def test_no_broker_publish():
    app = create_app(Settings(mqtt_enabled=False, serial_enabled=False))
    with TestClient(app) as client:
        response = client.post(
            "/api/mqtt/publish",
            json={"topic": "benchlab/demo", "payload": {"message": "hello"}},
        )
        assert response.status_code == 503
