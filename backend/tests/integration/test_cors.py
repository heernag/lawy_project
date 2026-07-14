from fastapi.testclient import TestClient

from app.main import create_app


def test_cors_preflight_allows_configured_origin():
    client = TestClient(create_app())

    response = client.options(
        "/api/health",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"
