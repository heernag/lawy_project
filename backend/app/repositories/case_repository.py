import json
from datetime import date
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.case import CaseDocument


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

    def _parse_date(self, value: str | None) -> date | None:
        if not value:
            return None
        return date.fromisoformat(value)
