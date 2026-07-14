from pathlib import Path
from typing import Any

from app.providers.sample_case_provider import SampleCaseProvider
from app.services.paragraph_service import ParagraphService
from app.validators.legal_text_validator import LegalTextValidator


class SimplificationService:
    def __init__(
        self,
        provider: SampleCaseProvider | None = None,
        paragraph_service: ParagraphService | None = None,
        validator: LegalTextValidator | None = None,
    ):
        self.provider = provider or SampleCaseProvider(Path("data/sample_cases.json"))
        self.paragraph_service = paragraph_service or ParagraphService()
        self.validator = validator or LegalTextValidator()

    def simplify_case(
        self,
        case_id: str,
        section_types: list[str] | None,
        force_regenerate: bool,
    ) -> dict[str, Any] | None:
        case = self.provider.get_case(case_id)
        if case is None:
            return None
        paragraphs = []
        for section in self.paragraph_service.split_sections(case.get("original_text", "")):
            if section_types and section.section_type not in section_types:
                continue
            for paragraph in section.paragraphs:
                paragraphs.append(self._simplify_paragraph(paragraph.paragraph_id, paragraph.original_text))
        return {"case_id": case_id, "paragraphs": paragraphs}

    def get_simplified_case(self, case_id: str) -> dict[str, Any] | None:
        return self.simplify_case(case_id, None, False)

    def simplify_paragraph(self, case_id: str, paragraph_id: str) -> dict[str, Any] | None:
        case = self.provider.get_case(case_id)
        if case is None:
            return None
        for section in self.paragraph_service.split_sections(case.get("original_text", "")):
            for paragraph in section.paragraphs:
                if paragraph.paragraph_id == paragraph_id:
                    return self._simplify_paragraph(paragraph.paragraph_id, paragraph.original_text)
        return None

    def _simplify_paragraph(self, paragraph_id: str, original_text: str) -> dict[str, Any]:
        simplified = original_text
        replacements = {
            "지급하라": "지급해야 합니다",
            "반환하라": "반환해야 합니다",
            "이에 대하여": "이 금액에 대해",
            "다 갚는 날까지": "실제로 모두 갚는 날까지",
            "연 12%의 비율로 계산한 돈": "연 12%의 지연이자",
            "청구를 일부 인용한다": "청구 중 일부를 받아들입니다",
        }
        for source, target in replacements.items():
            simplified = simplified.replace(source, target)
        validation = self.validator.validate(original_text, simplified)
        return {
            "paragraph_id": paragraph_id,
            "original_text": original_text,
            "simplified_text": simplified,
            "validation_status": validation.status,
            "warnings": validation.warnings,
        }
