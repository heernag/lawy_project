import json
from pathlib import Path

from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.models import CaseDocument
from app.providers.sample_case_provider import SampleCaseProvider
from app.repositories.case_repository import CaseRepository
from app.services.paragraph_service import ParagraphService


def bootstrap_database(engine: Engine, sample_path: Path, legal_terms_path: Path | None = None) -> None:
    Base.metadata.create_all(bind=engine)
    session = sessionmaker(bind=engine)()
    try:
        repository = CaseRepository(session)
        provider = SampleCaseProvider(sample_path)
        paragraph_service = ParagraphService()
        if legal_terms_path is None:
            legal_terms_path = sample_path.parent / "legal_terms.json"
        if legal_terms_path.exists():
            for term in json.loads(legal_terms_path.read_text(encoding="utf-8")):
                repository.upsert_legal_term(term)
        for case in provider.search_cases("", {}):
            repository.upsert_case(case)
            sections = [section.to_dict() for section in paragraph_service.split_sections(case.get("original_text", ""))]
            repository.upsert_sections(case["case_id"], sections)
    finally:
        session.close()
