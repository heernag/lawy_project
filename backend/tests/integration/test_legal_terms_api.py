from fastapi.testclient import TestClient

from app.main import create_app


def test_legal_term_api_returns_definition():
    client = TestClient(create_app())

    response = client.get("/api/legal-terms/기각")

    assert response.status_code == 200
    assert response.json()["data"]["term"] == "기각"


def test_case_legal_terms_api_returns_terms():
    client = TestClient(create_app())

    response = client.get("/api/cases/sample-001/legal-terms")

    assert response.status_code == 200
    assert response.json()["data"]["terms"]


def test_summary_api_returns_summary():
    client = TestClient(create_app())

    response = client.post("/api/cases/sample-001/summary", json={"force_regenerate": False})

    assert response.status_code == 200
    assert response.json()["data"]["one_line_summary"]
