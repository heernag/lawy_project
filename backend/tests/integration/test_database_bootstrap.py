from pathlib import Path

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

from app.db.bootstrap import bootstrap_database
from app.db.base import Base
from app.providers.db_case_provider import DbCaseProvider
from app.repositories.case_repository import CaseRepository


def test_bootstrap_database_creates_tables_and_loads_sample_cases(tmp_path):
    db_path = tmp_path / "cases.db"
    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})

    bootstrap_database(engine, Path("data/sample_cases.json"))

    inspector = inspect(engine)
    assert "case_documents" in inspector.get_table_names()

    session = sessionmaker(bind=engine)()
    repository = CaseRepository(session)
    assert repository.get_case("sample-001") is not None
    sections = repository.get_case_sections("sample-001")
    assert sections[0]["section_type"] == "주문"
    assert sections[0]["paragraphs"][0]["paragraph_id"] == "paragraph-1-1"
    assert repository.get_legal_term("기각")["source"] == "MVP built-in glossary"
    assert "중고 노트북" in repository.get_case_search_index("sample-001")


def test_db_case_provider_reads_cases_from_repository():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    session = sessionmaker(bind=engine)()
    repository = CaseRepository(session)
    repository.upsert_case(
        {
            "case_id": "sample-db",
            "case_number": "샘플-DB-001",
            "case_name": "DB 저장 판결문",
            "court_name": "샘플 법원",
            "decision_date": "2025-01-01",
            "category": "민사",
            "judgment_result": "인용",
            "order_text": "피고는 원고에게 지급하라.",
            "original_text": "주문\n피고는 원고에게 지급하라.",
            "summary": "DB에서 읽는 샘플 사건입니다.",
            "main_issues": ["DB 저장"],
            "source_name": "MVP sample data",
            "source_url": "",
        }
    )

    provider = DbCaseProvider(repository)

    assert provider.get_case("sample-db")["case_name"] == "DB 저장 판결문"
    assert provider.search_cases("저장", {})[0]["case_id"] == "sample-db"


def test_db_case_provider_returns_persisted_sections_from_repository():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    session = sessionmaker(bind=engine)()
    repository = CaseRepository(session)
    repository.upsert_case(
        {
            "case_id": "sample-section",
            "case_number": "샘플-SECTION-001",
            "case_name": "문단 저장 사건",
            "court_name": "샘플 법원",
            "decision_date": "2025-01-01",
            "category": "민사",
            "judgment_result": "인용",
            "order_text": "피고는 원고에게 지급하라.",
            "original_text": "주문\n피고는 원고에게 지급하라.",
            "summary": "문단 저장 샘플 사건입니다.",
            "main_issues": ["문단 저장"],
            "source_name": "MVP sample data",
            "source_url": "",
        }
    )
    repository.upsert_sections(
        "sample-section",
        [
            {
                "section_id": "section-1",
                "section_type": "주문",
                "section_order": 1,
                "original_text": "피고는 원고에게 지급하라.",
                "paragraphs": [
                    {
                        "paragraph_id": "paragraph-1-1",
                        "paragraph_order": 1,
                        "original_text": "피고는 원고에게 지급하라.",
                    }
                ],
            }
        ],
    )

    case = DbCaseProvider(repository).get_case("sample-section")

    assert case["sections"][0]["paragraphs"][0]["original_text"] == "피고는 원고에게 지급하라."


def test_db_case_provider_reads_legal_terms_from_repository():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    session = sessionmaker(bind=engine)()
    repository = CaseRepository(session)
    repository.upsert_legal_term(
        {
            "term": "기각",
            "easy_definition": "법원이 청구를 받아들이지 않는다는 뜻입니다.",
            "example": "원고의 청구를 기각한다.",
            "caution": "기각과 각하는 의미가 다릅니다.",
            "source": "MVP built-in glossary",
        }
    )

    provider = DbCaseProvider(repository)

    assert provider.get_legal_term("기각")["easy_definition"].startswith("법원이")


def test_app_exposes_database_backed_provider():
    from app.main import create_app

    client = TestClient(create_app())

    assert isinstance(client.app.state.case_provider, DbCaseProvider)
