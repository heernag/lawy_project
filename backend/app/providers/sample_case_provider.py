import json
from pathlib import Path
from typing import Any

from app.providers.base_case_provider import CaseProvider


class SampleCaseProvider(CaseProvider):
    def __init__(self, path: Path):
        self.path = path

    def _load(self) -> list[dict[str, Any]]:
        return json.loads(self.path.read_text(encoding="utf-8"))

    def search_cases(self, query: str, filters: dict[str, Any]) -> list[dict[str, Any]]:
        query_terms = [term for term in query.split() if term]
        cases = self._load()
        filtered_cases = self._apply_filters(cases, filters)
        if not query_terms:
            return filtered_cases
        return [
            case
            for case in filtered_cases
            if any(
                term in " ".join(
                    [
                        case.get("case_number", ""),
                        case.get("case_name", ""),
                        case.get("summary", ""),
                        case.get("original_text", ""),
                        " ".join(case.get("main_issues", [])),
                    ]
                )
                for term in query_terms
            )
        ]

    def get_case(self, case_id: str) -> dict[str, Any] | None:
        for case in self._load():
            if case.get("case_id") == case_id:
                return case
        return None

    def _apply_filters(self, cases: list[dict[str, Any]], filters: dict[str, Any]) -> list[dict[str, Any]]:
        result = cases
        for key, value in filters.items():
            if value is None or value == "":
                continue
            result = [case for case in result if case.get(key) == value]
        return result
