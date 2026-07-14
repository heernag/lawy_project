from fastapi.testclient import TestClient

from app.main import create_app


def test_full_flow_analyze_search_detail_simplify():
    client = TestClient(create_app())

    analyze = client.post("/api/cases/analyze", json={"query": "중고 노트북 하자 환불 거부"})
    assert analyze.status_code == 200

    search = client.post("/api/cases/search", json={"query": "중고 노트북 하자 환불", "page": 1, "size": 10})
    assert search.status_code == 200
    case_id = search.json()["data"]["results"][0]["case_id"]

    detail = client.get(f"/api/cases/{case_id}")
    assert detail.status_code == 200
    assert detail.json()["data"]["case_id"] == case_id

    simplified = client.post(
        f"/api/cases/{case_id}/simplify",
        json={"section_types": ["주문"], "force_regenerate": False},
    )
    assert simplified.status_code == 200
    assert simplified.json()["data"]["case_id"] == case_id


def test_full_flow_does_not_return_unstored_case():
    client = TestClient(create_app())

    response = client.get("/api/cases/not-real-case")

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "CASE_NOT_FOUND"
