import json
from datetime import date
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.case import CaseDocument, CaseLegalTerm, CaseParagraph, CaseSection, CaseSummary, LegalTerm


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

    def upsert_summary(self, case_id: str, summary: dict[str, Any]) -> CaseSummary | None:
        if self.get_case(case_id) is None:
            return None
        summary_id = f"{case_id}:summary"
        row = self.session.get(CaseSummary, summary_id) or CaseSummary(id=summary_id, case_id=case_id)
        row.one_line_summary = summary.get("one_line_summary", "")
        row.background = summary.get("background", "")
        row.plaintiff_claim = summary.get("plaintiff_claim", "")
        row.defendant_claim = summary.get("defendant_claim", "")
        row.court_reasoning = summary.get("court_reasoning", "")
        row.judgment_result = summary.get("judgment_result", "")
        self.session.add(row)
        self.session.commit()
        self.session.refresh(row)
        return row

    def get_summary(self, case_id: str) -> dict[str, Any] | None:
        row = self.session.get(CaseSummary, f"{case_id}:summary")
        if row is None:
            return None
        return {
            "one_line_summary": row.one_line_summary,
            "background": row.background,
            "plaintiff_claim": row.plaintiff_claim,
            "defendant_claim": row.defendant_claim,
            "court_reasoning": row.court_reasoning,
            "judgment_result": row.judgment_result,
        }

    def upsert_legal_term(self, term: dict[str, Any]) -> LegalTerm:
        term_name = term["term"]
        row = self.get_legal_term_row(term_name) or LegalTerm(id=term_name, term=term_name)
        row.easy_definition = term.get("easy_definition", "")
        row.example = term.get("example", "")
        row.caution = term.get("caution", "")
        row.source = term.get("source", "MVP built-in glossary")
        self.session.add(row)
        self.session.commit()
        self.session.refresh(row)
        return row

    def get_legal_term_row(self, term: str) -> LegalTerm | None:
        return self.session.scalar(select(LegalTerm).where(LegalTerm.term == term))

    def get_legal_term(self, term: str) -> dict[str, Any] | None:
        row = self.get_legal_term_row(term)
        if row is None:
            return None
        return self._legal_term_to_dict(row)

    def list_legal_terms(self) -> list[dict[str, Any]]:
        rows = self.session.scalars(select(LegalTerm).order_by(LegalTerm.term)).all()
        return [self._legal_term_to_dict(row) for row in rows]

    def upsert_case_legal_terms(self, case_id: str, terms: list[dict[str, Any]]) -> None:
        existing = self.session.scalars(select(CaseLegalTerm).where(CaseLegalTerm.case_id == case_id)).all()
        for row in existing:
            self.session.delete(row)
        self.session.flush()
        for item in terms:
            term_row = self.get_legal_term_row(item["term"])
            if term_row is None:
                continue
            paragraph_id = item.get("paragraph_id")
            storage_paragraph_id = self._storage_id(case_id, paragraph_id) if paragraph_id else None
            self.session.add(
                CaseLegalTerm(
                    id=f"{case_id}:term:{term_row.id}:{paragraph_id or 'case'}",
                    case_id=case_id,
                    term_id=term_row.id,
                    context_meaning=item.get("context_meaning", ""),
                    paragraph_id=storage_paragraph_id,
                )
            )
        self.session.commit()

    def get_case_legal_terms(self, case_id: str) -> list[dict[str, Any]]:
        rows = self.session.scalars(select(CaseLegalTerm).where(CaseLegalTerm.case_id == case_id)).all()
        results = []
        for row in rows:
            term_row = self.session.get(LegalTerm, row.term_id)
            if term_row is None:
                continue
            item = self._legal_term_to_dict(term_row)
            item["context_meaning"] = row.context_meaning
            item["paragraph_id"] = self._public_id(row.paragraph_id) if row.paragraph_id else None
            results.append(item)
        return results

    def _legal_term_to_dict(self, row: LegalTerm) -> dict[str, Any]:
        return {
            "term": row.term,
            "easy_definition": row.easy_definition,
            "example": row.example,
            "caution": row.caution,
            "source": row.source,
        }

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
