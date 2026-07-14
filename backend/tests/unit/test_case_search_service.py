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
