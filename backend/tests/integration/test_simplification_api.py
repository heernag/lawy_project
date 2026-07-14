from fastapi.testclient import TestClient

from app.main import create_app


def test_simplify_case_api_returns_simplified_paragraphs():
    client = TestClient(create_app())

    response = client.post(
        "/api/cases/sample-001/simplify",
        json={"section_types": ["주문"], "force_regenerate": False},
    )

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["case_id"] == "sample-001"
    assert data["paragraphs"][0]["original_text"]
    assert data["paragraphs"][0]["simplified_text"]


def test_get_simplified_case_api_returns_generated_result():
    client = TestClient(create_app())

    response = client.get("/api/cases/sample-001/simplified")

    assert response.status_code == 200
    assert response.json()["data"]["paragraphs"]


def test_simplify_single_paragraph_api_uses_stable_paragraph_id():
    client = TestClient(create_app())

    response = client.post("/api/cases/sample-001/paragraphs/paragraph-1-1/simplify")

    assert response.status_code == 200
    assert response.json()["data"]["paragraph_id"] == "paragraph-1-1"
