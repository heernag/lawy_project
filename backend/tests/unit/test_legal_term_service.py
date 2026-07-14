from app.services.legal_term_service import LegalTermService


def test_get_known_legal_term_has_easy_definition():
    result = LegalTermService().get_term("기각")

    assert result["term"] == "기각"
    assert "받아들이지" in result["easy_definition"]
    assert result["source"] == "MVP built-in glossary"


def test_extract_terms_from_case_text():
    results = LegalTermService().extract_terms("sample-001")

    terms = [item["term"] for item in results]
    assert "손해배상" in terms
