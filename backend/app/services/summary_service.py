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

    def _line_after(self, text: str, heading: str) -> str:
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        for index, line in enumerate(lines[:-1]):
            if line == heading:
                return lines[index + 1]
        return ""
