from fastapi.testclient import TestClient

from app.main import create_app


def test_openapi_exposes_core_paths_for_frontend():
    client = TestClient(create_app())

    response = client.get("/openapi.json")

    assert response.status_code == 200
    paths = response.json()["paths"]
    expected_paths = {
        "/api/health",
        "/api/cases/analyze",
        "/api/cases/search",
        "/api/cases/{case_id}",
        "/api/cases/{case_id}/sections",
        "/api/cases/{case_id}/summary",
        "/api/cases/{case_id}/simplify",
        "/api/cases/{case_id}/simplified",
        "/api/cases/{case_id}/paragraphs/{paragraph_id}/simplify",
        "/api/legal-terms/{term}",
        "/api/cases/{case_id}/legal-terms",
        "/api/cases/{case_id}/similar",
    }

    assert expected_paths.issubset(paths.keys())


def test_openapi_documents_common_api_response_schemas():
    client = TestClient(create_app())

    response = client.get("/openapi.json")

    assert response.status_code == 200
    schemas = response.json()["components"]["schemas"]

    assert schemas["ApiError"]["required"] == ["code", "message", "details"]
    assert set(schemas["ApiError"]["properties"].keys()) == {"code", "message", "details"}
    assert schemas["ApiResponse"]["required"] == ["success", "data", "error"]
    assert set(schemas["ApiResponse"]["properties"].keys()) == {"success", "data", "error"}


def test_openapi_documents_standard_error_responses_for_case_lookup():
    client = TestClient(create_app())

    response = client.get("/openapi.json")

    assert response.status_code == 200
    operation = response.json()["paths"]["/api/cases/{case_id}"]["get"]

    assert operation["responses"]["200"]["content"]["application/json"]["schema"]["$ref"] == "#/components/schemas/ApiResponse"
    assert operation["responses"]["404"]["content"]["application/json"]["schema"]["$ref"] == "#/components/schemas/ApiResponse"
