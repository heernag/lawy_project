from pathlib import Path

from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.models import CaseDocument
from app.providers.sample_case_provider import SampleCaseProvider
from app.repositories.case_repository import CaseRepository


def bootstrap_database(engine: Engine, sample_path: Path) -> None:
    Base.metadata.create_all(bind=engine)
    session = sessionmaker(bind=engine)()
    try:
        repository = CaseRepository(session)
        provider = SampleCaseProvider(sample_path)
        for case in provider.search_cases("", {}):
            repository.upsert_case(case)
    finally:
        session.close()
