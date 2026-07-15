from app.schemas.search import CaseSearchRequest
from app.services.case_search_service import CaseSearchService


def test_search_finds_case_by_case_number_first():
    request = CaseSearchRequest(query="샘플-사건번호-001", page=1, size=10)

    result = CaseSearchService().search(request)

    assert result.total_count == 1
    assert result.results[0].case_id == "sample-001"
    assert result.results[0].similarity_reason == "사건번호가 정확히 일치합니다."


def test_search_filters_by_category():
    request = CaseSearchRequest(query="임금", category="노동", page=1, size=10)

    result = CaseSearchService().search(request)

    assert result.total_count == 1
    assert result.results[0].case_id == "sample-003"


def test_search_filters_by_decision_date_range():
    request = CaseSearchRequest(query="샘플", start_date="2024-01-01", end_date="2024-12-31", page=1, size=10)

    result = CaseSearchService().search(request)

    assert result.total_count == 1
    assert result.results[0].case_id == "sample-002"


def test_search_uses_stored_search_text_when_available():
    class SearchTextProvider:
        def search_cases(self, query, filters):
            return [
                {
                    "case_id": "sample-search-text",
                    "case_number": "샘플-검색-001",
                    "case_name": "겉보기 제목",
                    "court_name": "샘플 법원",
                    "decision_date": "2025-01-01",
                    "category": "민사",
                    "judgment_result": "인용",
                    "summary": "",
                    "main_issues": [],
                    "original_text": "",
                    "search_text": "특별검색어가 저장된 로컬 검색 인덱스",
                    "source_name": "MVP sample data",
                    "source_url": "",
                }
            ]

    request = CaseSearchRequest(query="특별검색어", page=1, size=10)

    result = CaseSearchService(provider=SearchTextProvider()).search(request)

    assert result.total_count == 1
    assert result.results[0].case_id == "sample-search-text"
