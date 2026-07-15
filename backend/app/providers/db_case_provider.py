import json
from typing import Any

from sqlalchemy.orm import Session

from app.models.case import CaseDocument
from app.providers.base_case_provider import CaseProvider
from app.repositories.case_repository import CaseRepository


class DbCaseProvider(CaseProvider):
    def __init__(self, repository: CaseRepository | None = None, session_factory: Any | None = None):
        self.repository = repository
        self.session_factory = session_factory

    def search_cases(self, query: str, filters: dict[str, Any]) -> list[dict[str, Any]]:
        repository, session = self._repository()
        try:
            cases = [self._to_dict(document, repository) for document in repository.list_cases()]
        finally:
            self._close_session(session)
        filtered = self._apply_filters(cases, filters)
        query_terms = [term for term in query.split() if term]
        if not query_terms:
            return filtered
        return [
            case
            for case in filtered
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
        repository, session = self._repository()
        try:
            document = repository.get_case(case_id)
            if document is None:
                return None
            return self._to_dict(document, repository)
        finally:
            self._close_session(session)

    def _to_dict(self, document: CaseDocument, repository: CaseRepository) -> dict[str, Any]:
        return {
            "case_id": document.id,
            "external_id": document.external_id,
            "case_number": document.case_number,
            "case_name": document.case_name,
            "court_name": document.court_name,
            "court_department": document.court_department,
            "decision_date": document.decision_date.isoformat() if document.decision_date else None,
            "category": document.category,
            "judgment_result": document.judgment_result,
            "order_text": document.order_text,
            "original_text": document.original_text,
            "summary": document.summary,
            "main_issues": json.loads(document.main_issues or "[]"),
            "source_name": document.source_name,
            "source_url": document.source_url,
            "sections": repository.get_case_sections(document.id),
        }

    def update_paragraph_simplification(
        self,
        case_id: str,
        paragraph_id: str,
        simplified_text: str,
        validation_status: str,
        warnings: list[str],
    ) -> None:
        repository, session = self._repository()
        try:
            repository.update_paragraph_simplification(case_id, paragraph_id, simplified_text, validation_status, warnings)
        finally:
            self._close_session(session)

    def get_summary(self, case_id: str) -> dict[str, Any] | None:
        repository, session = self._repository()
        try:
            return repository.get_summary(case_id)
        finally:
            self._close_session(session)

    def upsert_summary(self, case_id: str, summary: dict[str, Any]) -> None:
        repository, session = self._repository()
        try:
            repository.upsert_summary(case_id, summary)
        finally:
            self._close_session(session)

    def _apply_filters(self, cases: list[dict[str, Any]], filters: dict[str, Any]) -> list[dict[str, Any]]:
        result = cases
        for key, value in filters.items():
            if value is None or value == "":
                continue
            result = [case for case in result if case.get(key) == value]
        return result

    def _repository(self) -> tuple[CaseRepository, Session | None]:
        if self.repository is not None:
            return self.repository, None
        if self.session_factory is None:
            raise RuntimeError("DbCaseProvider requires a repository or session_factory.")
        session = self.session_factory()
        return CaseRepository(session), session

    def _close_session(self, session: Session | None) -> None:
        if session is not None:
            session.close()
