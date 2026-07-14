from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.repositories.case_repository import CaseRepository


def test_case_repository_upserts_and_reads_case():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    session = sessionmaker(bind=engine)()
    repository = CaseRepository(session)

    saved = repository.upsert_case(
        {
            "case_id": "sample-999",
            "case_number": "샘플-사건번호-999",
            "case_name": "샘플 매매계약 사건",
            "court_name": "샘플 법원",
            "court_department": "샘플 재판부",
            "decision_date": "2025-01-01",
            "category": "민사",
            "judgment_result": "일부 인용",
            "order_text": "피고는 원고에게 5,000,000원을 지급하라.",
            "original_text": "주문\n피고는 원고에게 5,000,000원을 지급하라.",
            "summary": "샘플 요약",
            "main_issues": ["매매 목적물의 하자"],
            "source_name": "MVP sample data",
            "source_url": "",
        }
    )

    found = repository.get_case(saved.id)

    assert found is not None
    assert found.external_id == "sample-999"
    assert found.case_number == "샘플-사건번호-999"
    assert found.source_name == "MVP sample data"
