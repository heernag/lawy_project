import json
from datetime import date
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.case import CaseDocument, CaseParagraph, CaseSection


class CaseRepository:
    def __init__(self, session: Session):
        self.session = session

    def upsert_case(self, raw_case: dict[str, Any]) -> CaseDocument:
        case_id = raw_case["case_id"]
        existing = self.get_case(case_id)
        document = existing or CaseDocument(id=case_id, external_id=case_id)
        document.external_id = raw_case.get("external_id", case_id)
        document.case_number = raw_case.get("case_number", "")
        document.case_name = raw_case.get("case_name", "")
        document.court_name = raw_case.get("court_name", "")
        document.court_department = raw_case.get("court_department", "")
        document.decision_date = self._parse_date(raw_case.get("decision_date"))
        document.category = raw_case.get("category", "")
        document.judgment_result = raw_case.get("judgment_result", "")
        document.order_text = raw_case.get("order_text", "")
        document.original_text = raw_case.get("original_text", "")
        document.summary = raw_case.get("summary", "")
        document.main_issues = json.dumps(raw_case.get("main_issues", []), ensure_ascii=False)
        document.source_name = raw_case.get("source_name", "")
        document.source_url = raw_case.get("source_url", "")
        if existing is None:
            self.session.add(document)
        self.session.commit()
        self.session.refresh(document)
        return document

    def get_case(self, case_id: str) -> CaseDocument | None:
        return self.session.get(CaseDocument, case_id)

    def list_cases(self) -> list[CaseDocument]:
        return list(self.session.scalars(select(CaseDocument)).all())

    def upsert_sections(self, case_id: str, sections: list[dict[str, Any]]) -> None:
        document = self.get_case(case_id)
        if document is None:
            return
        for existing in list(document.sections):
            self.session.delete(existing)
        self.session.flush()
        for section in sections:
            public_section_id = section["section_id"]
            section_row = CaseSection(
                id=self._storage_id(case_id, public_section_id),
                case_id=case_id,
                section_type=section.get("section_type", ""),
                section_order=section.get("section_order", 0),
                original_text=section.get("original_text", ""),
            )
            self.session.add(section_row)
            for paragraph in section.get("paragraphs", []):
                self.session.add(
                    CaseParagraph(
                        id=self._storage_id(case_id, paragraph["paragraph_id"]),
                        section_id=section_row.id,
                        paragraph_order=paragraph.get("paragraph_order", 0),
                        original_text=paragraph.get("original_text", ""),
                        simplified_text=paragraph.get("simplified_text", ""),
                        validation_status=paragraph.get("validation_status", "not_generated"),
                        validation_warnings=json.dumps(paragraph.get("warnings", []), ensure_ascii=False),
                    )
                )
        self.session.commit()

    def get_case_sections(self, case_id: str) -> list[dict[str, Any]]:
        document = self.get_case(case_id)
        if document is None:
            return []
        return [
            {
                "section_id": self._public_id(section.id),
                "section_type": section.section_type,
                "section_order": section.section_order,
                "original_text": section.original_text,
                "paragraphs": [
                    {
                        "paragraph_id": self._public_id(paragraph.id),
                        "paragraph_order": paragraph.paragraph_order,
                        "original_text": paragraph.original_text,
                        "simplified_text": paragraph.simplified_text,
                        "validation_status": paragraph.validation_status,
                        "warnings": json.loads(paragraph.validation_warnings or "[]"),
                    }
                    for paragraph in sorted(section.paragraphs, key=lambda item: item.paragraph_order)
                ],
            }
            for section in sorted(document.sections, key=lambda item: item.section_order)
        ]

    def update_paragraph_simplification(
        self,
        case_id: str,
        paragraph_id: str,
        simplified_text: str,
        validation_status: str,
        warnings: list[str],
    ) -> CaseParagraph | None:
        paragraph = self.session.get(CaseParagraph, self._storage_id(case_id, paragraph_id))
        if paragraph is None:
            return None
        paragraph.simplified_text = simplified_text
        paragraph.validation_status = validation_status
        paragraph.validation_warnings = json.dumps(warnings, ensure_ascii=False)
        self.session.commit()
        self.session.refresh(paragraph)
        return paragraph

    def _storage_id(self, case_id: str, public_id: str) -> str:
        if public_id.startswith(f"{case_id}:"):
            return public_id
        return f"{case_id}:{public_id}"

    def _public_id(self, storage_id: str) -> str:
        return storage_id.split(":", 1)[1] if ":" in storage_id else storage_id

    def _parse_date(self, value: str | None) -> date | None:
        if not value:
            return None
        return date.fromisoformat(value)
