from app.services.simplification_service import SimplificationService


def test_simplify_case_returns_paragraphs_with_validation_status():
    result = SimplificationService().simplify_case("sample-001", ["주문"], False)

    assert result is not None
    assert result["case_id"] == "sample-001"
    assert result["paragraphs"][0]["validation_status"] == "passed"
    assert "지급해야 합니다" in result["paragraphs"][0]["simplified_text"]


def test_simplify_missing_case_returns_none():
    result = SimplificationService().simplify_case("missing", None, False)

    assert result is None
