from fastapi.testclient import TestClient

from app.api.dependencies import get_case_provider
from app.main import create_app


def test_health_returns_common_success_response():
    client = TestClient(create_app())

    response = client.get("/api/health")

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["error"] is None
    assert body["data"]["status"] == "ok"
    assert body["data"]["checks"]["case_provider"] == "ok"
    assert body["data"]["checks"]["case_count"] >= 1
    assert body["data"]["checks"]["sample_data_loaded"] is True


def test_health_returns_degraded_when_case_provider_fails():
    class FailingProvider:
        def search_cases(self, query, filters):
            raise RuntimeError("database password leaked")

    app = create_app()
    app.dependency_overrides[get_case_provider] = lambda: FailingProvider()
    client = TestClient(app)

    response = client.get("/api/health")

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["status"] == "degraded"
    assert body["data"]["checks"] == {
        "case_provider": "error",
        "case_count": 0,
        "sample_data_loaded": False,
        "message": "case provider check failed",
    }
