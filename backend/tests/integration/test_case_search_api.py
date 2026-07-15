from fastapi.testclient import TestClient

from app.main import create_app


def test_search_api_returns_paginated_results():
    client = TestClient(create_app())

    response = client.post(
        "/api/cases/search",
        json={"query": "중고 노트북 하자 환불", "page": 1, "size": 10},
    )

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["total_count"] >= 1
    assert data["results"][0]["case_id"] == "sample-001"
    assert data["extracted_keywords"]


def test_search_api_returns_common_error_for_invalid_page():
    client = TestClient(create_app())

    response = client.post(
        "/api/cases/search",
        json={"query": "deposit dispute", "page": 0, "size": 10},
    )

    assert response.status_code == 400
    body = response.json()
    assert body["success"] is False
    assert body["error"]["code"] == "INVALID_REQUEST"


def test_search_api_returns_common_error_for_invalid_size():
    client = TestClient(create_app())

    response = client.post(
        "/api/cases/search",
        json={"query": "deposit dispute", "page": 1, "size": 100},
    )

    assert response.status_code == 400
    body = response.json()
    assert body["success"] is False
    assert body["error"]["code"] == "INVALID_REQUEST"


def test_similar_api_returns_cases_except_source_case():
    client = TestClient(create_app())

    response = client.get("/api/cases/sample-001/similar")

    assert response.status_code == 200
    results = response.json()["data"]["results"]
    assert all(item["case_id"] != "sample-001" for item in results)
