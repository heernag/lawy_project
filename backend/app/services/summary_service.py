from pathlib import Path
from typing import Any

from app.providers.sample_case_provider import SampleCaseProvider
from app.services.legal_term_service import LegalTermService


class SummaryService:
    def __init__(self, provider: SampleCaseProvider | None = None):
        self.provider = provider or SampleCaseProvider(Path("data/sample_cases.json"))

    def summarize(self, case_id: str, force_regenerate: bool = False) -> dict[str, Any] | None:
        case = self.provider.get_case(case_id)
        if case is None:
            return None
        stored_summary = self._stored_summary(case_id)
        if stored_summary is not None and not force_regenerate:
            return self._with_dynamic_fields(case, stored_summary)
        generated = self._generate_summary(case_id, case)
        self._persist_summary(case_id, generated)
        return generated

    def _generate_summary(self, case_id: str, case: dict[str, Any]) -> dict[str, Any]:
        original_text = case.get("original_text", "")
        return {
            "one_line_summary": case.get("summary", ""),
            "background": self._line_after(original_text, "이유"),
            "plaintiff_claim": self._line_after(original_text, "원고 주장"),
            "defendant_claim": self._line_after(original_text, "피고 주장"),
            "main_issues": case.get("main_issues", []),
            "court_reasoning": self._line_after(original_text, "법원의 판단"),
            "judgment_result": case.get("judgment_result", ""),
            "legal_terms": [item["term"] for item in LegalTermService(self.provider).extract_terms(case_id)],
        }

    def _stored_summary(self, case_id: str) -> dict[str, Any] | None:
        getter = getattr(self.provider, "get_summary", None)
        if getter is None:
            return None
        return getter(case_id)

    def _persist_summary(self, case_id: str, summary: dict[str, Any]) -> None:
        writer = getattr(self.provider, "upsert_summary", None)
        if writer is not None:
            writer(case_id, summary)

    def _with_dynamic_fields(self, case: dict[str, Any], summary: dict[str, Any]) -> dict[str, Any]:
        result = dict(summary)
        result["main_issues"] = case.get("main_issues", [])
        result["legal_terms"] = [item["term"] for item in LegalTermService(self.provider).extract_terms(case["case_id"])]
        return result

    def _line_after(self, text: str, heading: str) -> str:
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        for index, line in enumerate(lines[:-1]):
            if line == heading:
                return lines[index + 1]
        return ""
