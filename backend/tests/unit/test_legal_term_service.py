from app.services.legal_term_service import LegalTermService


def test_get_known_legal_term_has_easy_definition():
    result = LegalTermService().get_term("기각")

    assert result["term"] == "기각"
    assert "받아들이지" in result["easy_definition"]
    assert result["source"] == "MVP built-in glossary"


class LegalTermMemoryProvider:
    def get_case(self, case_id):
        return {
            "case_id": case_id,
            "original_text": "원고의 손해배상 청구를 기각한다.",
            "summary": "손해배상 청구 기각 사건",
            "main_issues": ["손해배상"],
            "sections": [
                {
                    "section_id": "section-1",
                    "section_type": "주문",
                    "section_order": 1,
                    "original_text": "원고의 손해배상 청구를 기각한다.",
                    "paragraphs": [
                        {
                            "paragraph_id": "paragraph-1-1",
                            "paragraph_order": 1,
                            "original_text": "원고의 손해배상 청구를 기각한다.",
                        }
                    ],
                }
            ],
        }

    def get_legal_term(self, term):
        if term == "기각":
            return {
                "term": "기각",
                "easy_definition": "저장된 기각 정의",
                "example": "원고의 청구를 기각한다.",
                "caution": "기각과 각하는 다릅니다.",
                "source": "DB glossary",
            }
        return None

    def list_legal_terms(self):
        return [
            {
                "term": "기각",
                "easy_definition": "저장된 기각 정의",
                "example": "원고의 청구를 기각한다.",
                "caution": "기각과 각하는 다릅니다.",
                "source": "DB glossary",
            }
        ]

    def get_case_legal_terms(self, case_id):
        return []

    def upsert_case_legal_terms(self, case_id, terms):
        self.saved_case_id = case_id
        self.saved_terms = terms


def test_get_term_prefers_provider_glossary():
    result = LegalTermService(provider=LegalTermMemoryProvider()).get_term("기각")

    assert result["easy_definition"] == "저장된 기각 정의"
    assert result["source"] == "DB glossary"


def test_extract_terms_persists_case_term_links_with_paragraph_id():
    provider = LegalTermMemoryProvider()

    results = LegalTermService(provider=provider).extract_terms("sample-001")

    assert results[0]["term"] == "기각"
    assert results[0]["paragraph_id"] == "paragraph-1-1"
    assert provider.saved_case_id == "sample-001"
    assert provider.saved_terms[0]["paragraph_id"] == "paragraph-1-1"


def test_extract_terms_from_case_text():
    results = LegalTermService().extract_terms("sample-001")

    terms = [item["term"] for item in results]
    assert "손해배상" in terms
