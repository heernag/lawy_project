from fastapi.testclient import TestClient

from app.main import create_app


def test_get_case_detail_returns_sample_case():
    client = TestClient(create_app())

    response = client.get("/api/cases/sample-001")

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["case_id"] == "sample-001"
    assert data["case_number"] == "샘플-사건번호-001"
    assert data["source_name"] == "MVP sample data"


def test_get_case_sections_returns_ordered_sections():
    client = TestClient(create_app())

    response = client.get("/api/cases/sample-001/sections")

    assert response.status_code == 200
    sections = response.json()["data"]["sections"]
    assert sections[0]["section_type"] == "주문"
    assert sections[0]["paragraphs"][0]["paragraph_order"] == 1


def test_get_missing_case_returns_common_error():
    client = TestClient(create_app())

    response = client.get("/api/cases/missing")

    assert response.status_code == 404
    assert response.json()["success"] is False
    assert response.json()["error"]["code"] == "CASE_NOT_FOUND"
