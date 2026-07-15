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


def test_openapi_documents_common_responses_for_core_routes():
    client = TestClient(create_app())

    response = client.get("/openapi.json")

    assert response.status_code == 200
    paths = response.json()["paths"]
    expected_operations = [
        ("/api/health", "get", []),
        ("/api/cases/analyze", "post", ["400"]),
        ("/api/cases/search", "post", ["400"]),
        ("/api/cases/{case_id}", "get", ["404"]),
        ("/api/cases/{case_id}/sections", "get", ["404"]),
        ("/api/cases/{case_id}/summary", "post", ["404"]),
        ("/api/cases/{case_id}/simplify", "post", ["404"]),
        ("/api/cases/{case_id}/simplified", "get", ["404"]),
        ("/api/cases/{case_id}/paragraphs/{paragraph_id}/simplify", "post", ["404"]),
        ("/api/legal-terms/{term}", "get", ["404"]),
        ("/api/cases/{case_id}/legal-terms", "get", ["404"]),
        ("/api/cases/{case_id}/similar", "get", ["404"]),
    ]

    for path, method, error_statuses in expected_operations:
        operation = paths[path][method]
        assert operation["responses"]["200"]["content"]["application/json"]["schema"]["$ref"] == "#/components/schemas/ApiResponse"
        for status_code in error_statuses:
            assert operation["responses"][status_code]["content"]["application/json"]["schema"]["$ref"] == "#/components/schemas/ApiResponse"
