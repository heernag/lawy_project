from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.main import create_app


def test_validation_error_includes_details_in_development(monkeypatch):
    monkeypatch.setenv("APP_ENV", "development")
    get_settings.cache_clear()
    client = TestClient(create_app())

    response = client.post(
        "/api/cases/search",
        json={"query": "deposit dispute", "page": 0, "size": 10},
    )

    assert response.status_code == 400
    body = response.json()
    assert body["error"]["code"] == "INVALID_REQUEST"
    assert body["error"]["details"]

    get_settings.cache_clear()


def test_validation_error_hides_details_in_production(monkeypatch):
    monkeypatch.setenv("APP_ENV", "production")
    get_settings.cache_clear()
    client = TestClient(create_app())

    response = client.post(
        "/api/cases/search",
        json={"query": "deposit dispute", "page": 0, "size": 10},
    )

    assert response.status_code == 400
    body = response.json()
    assert body["error"]["code"] == "INVALID_REQUEST"
    assert body["error"]["details"] is None

    get_settings.cache_clear()


def test_malformed_json_returns_common_invalid_request_error(monkeypatch):
    monkeypatch.setenv("APP_ENV", "development")
    get_settings.cache_clear()
    client = TestClient(create_app())

    response = client.post(
        "/api/cases/search",
        content='{"query": "deposit dispute",',
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 400
    body = response.json()
    assert body["success"] is False
    assert body["error"]["code"] == "INVALID_REQUEST"
    assert body["error"]["details"]

    get_settings.cache_clear()


def test_missing_required_body_field_returns_common_invalid_request_error(monkeypatch):
    monkeypatch.setenv("APP_ENV", "development")
    get_settings.cache_clear()
    client = TestClient(create_app())

    response = client.post("/api/cases/search", json={"page": 1, "size": 10})

    assert response.status_code == 400
    body = response.json()
    assert body["success"] is False
    assert body["error"]["code"] == "INVALID_REQUEST"
    assert body["error"]["details"]

    get_settings.cache_clear()
