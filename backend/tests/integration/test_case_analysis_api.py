from fastapi.testclient import TestClient

from app.main import create_app


def test_analyze_api_returns_case_analysis():
    client = TestClient(create_app())

    response = client.post(
        "/api/cases/analyze",
        json={"query": "전세 보증금을 돌려받지 못하고 있습니다."},
    )

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["category"] == "민사"
    assert data["sub_category"] == "임대차"
    assert "보증금 반환" in data["legal_issues"]


def test_analyze_api_rejects_blank_query():
    client = TestClient(create_app())

    response = client.post("/api/cases/analyze", json={"query": ""})

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "INVALID_REQUEST"
