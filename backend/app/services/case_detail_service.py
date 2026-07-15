from pathlib import Path
from typing import Any

from app.providers.sample_case_provider import SampleCaseProvider
from app.services.paragraph_service import ParagraphService


class CaseDetailService:
    def __init__(
        self,
        provider: SampleCaseProvider | None = None,
        paragraph_service: ParagraphService | None = None,
    ):
        self.provider = provider or SampleCaseProvider(Path("data/sample_cases.json"))
        self.paragraph_service = paragraph_service or ParagraphService()

    def get_case_detail(self, case_id: str) -> dict[str, Any] | None:
        case = self.provider.get_case(case_id)
        if case is None:
            return None
        return {
            "case_id": case["case_id"],
            "case_number": case.get("case_number", ""),
            "case_name": case.get("case_name", ""),
            "court_name": case.get("court_name", ""),
            "court_department": case.get("court_department", ""),
            "decision_date": case.get("decision_date"),
            "category": case.get("category", ""),
            "judgment_result": case.get("judgment_result", ""),
            "order_text": case.get("order_text", ""),
            "original_text": case.get("original_text", ""),
            "source_name": case.get("source_name", ""),
            "source_url": case.get("source_url", ""),
            "summary": case.get("summary", ""),
            "main_issues": case.get("main_issues", []),
        }

    def get_case_sections(self, case_id: str) -> dict[str, Any] | None:
        case = self.provider.get_case(case_id)
        if case is None:
            return None
        stored_sections = case.get("sections") or []
        if stored_sections:
            return {
                "case_id": case["case_id"],
                "sections": stored_sections,
            }
        sections = self.paragraph_service.split_sections(case.get("original_text", ""))
        return {
            "case_id": case["case_id"],
            "sections": [section.to_dict() for section in sections],
        }
