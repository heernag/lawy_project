from pathlib import Path
from typing import Any

from app.providers.sample_case_provider import SampleCaseProvider
from app.schemas.search import CaseSearchItem, CaseSearchRequest, CaseSearchResponse
from app.services.local_similarity_service import LocalSimilarityService


class CaseSearchService:
    def __init__(
        self,
        provider: SampleCaseProvider | None = None,
        similarity_service: LocalSimilarityService | None = None,
    ):
        self.provider = provider or SampleCaseProvider(Path("data/sample_cases.json"))
        self.similarity_service = similarity_service or LocalSimilarityService()

    def search(self, request: CaseSearchRequest) -> CaseSearchResponse:
        filters = {
            "category": request.category,
            "court_name": request.court,
            "judgment_result": request.judgment_result,
            "start_date": request.start_date,
            "end_date": request.end_date,
        }
        provider_filters = {key: value for key, value in filters.items() if key not in {"start_date", "end_date"}}
        cases = self.provider.search_cases("", provider_filters)
        cases = self._filter_by_date(cases, request.start_date, request.end_date)
        exact_matches = [case for case in cases if self._normalize(case.get("case_number", "")) == self._normalize(request.query)]
        scored_cases = exact_matches if exact_matches else self._score_cases(request.query, cases)

        start = (request.page - 1) * request.size
        end = start + request.size
        paged = scored_cases[start:end]
        return CaseSearchResponse(
            total_count=len(scored_cases),
            page=request.page,
            size=request.size,
            results=[self._to_item(case) for case in paged],
            applied_filters={key: value for key, value in filters.items() if value},
            extracted_keywords=sorted(self.similarity_service.tokenize(request.query)),
        )

    def similar(self, case_id: str) -> CaseSearchResponse | None:
        source = self.provider.get_case(case_id)
        if source is None:
            return None
        request = CaseSearchRequest(query=" ".join(source.get("main_issues", [])) or source.get("summary", ""), page=1, size=10)
        result = self.search(request)
        result.results = [item for item in result.results if item.case_id != case_id]
        result.total_count = len(result.results)
        return result

    def _score_cases(self, query: str, cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
        scored = []
        for case in cases:
            document = " ".join(
                [
                    case.get("case_name", ""),
                    case.get("summary", ""),
                    " ".join(case.get("main_issues", [])),
                    case.get("original_text", ""),
                ]
            )
            score = self.similarity_service.score(query, document)
            if score > 0:
                case = dict(case)
                case["_similarity_score"] = score
                case["_similarity_reason"] = "검색어와 판결문 키워드가 일부 일치합니다."
                scored.append(case)
        return sorted(scored, key=lambda item: item.get("_similarity_score", 0), reverse=True)

    def _to_item(self, case: dict[str, Any]) -> CaseSearchItem:
        exact = case.get("_similarity_reason") is None
        return CaseSearchItem(
            case_id=case["case_id"],
            case_number=case.get("case_number", ""),
            case_name=case.get("case_name", ""),
            court_name=case.get("court_name", ""),
            decision_date=case.get("decision_date"),
            category=case.get("category", ""),
            judgment_result=case.get("judgment_result", ""),
            summary=case.get("summary", ""),
            main_issues=case.get("main_issues", []),
            similarity_score=1.0 if exact else case.get("_similarity_score", 0.0),
            similarity_reason="사건번호가 정확히 일치합니다." if exact else case.get("_similarity_reason", ""),
            source_name=case.get("source_name", ""),
            source_url=case.get("source_url", ""),
        )

    def _normalize(self, value: str) -> str:
        return "".join(value.split()).lower()

    def _filter_by_date(self, cases: list[dict[str, Any]], start_date: str | None, end_date: str | None) -> list[dict[str, Any]]:
        if not start_date and not end_date:
            return cases
        result = []
        for case in cases:
            decision_date = case.get("decision_date")
            if not decision_date:
                continue
            if start_date and decision_date < start_date:
                continue
            if end_date and decision_date > end_date:
                continue
            result.append(case)
        return result
