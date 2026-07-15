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


def test_case_repository_upserts_and_reads_summary():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    session = sessionmaker(bind=engine)()
    repository = CaseRepository(session)
    repository.upsert_case(
        {
            "case_id": "sample-summary",
            "case_number": "샘플-요약-001",
            "case_name": "요약 저장 사건",
            "court_name": "샘플 법원",
            "decision_date": "2025-01-01",
            "category": "민사",
            "judgment_result": "인용",
            "order_text": "피고는 원고에게 지급하라.",
            "original_text": "주문\n피고는 원고에게 지급하라.",
            "summary": "문서 기본 요약",
            "main_issues": ["요약 저장"],
            "source_name": "MVP sample data",
            "source_url": "",
        }
    )

    repository.upsert_summary(
        "sample-summary",
        {
            "one_line_summary": "저장된 한 줄 요약",
            "background": "저장된 배경",
            "plaintiff_claim": "저장된 원고 주장",
            "defendant_claim": "저장된 피고 주장",
            "court_reasoning": "저장된 판단",
            "judgment_result": "저장된 결과",
        },
    )

    summary = repository.get_summary("sample-summary")

    assert summary is not None
    assert summary["one_line_summary"] == "저장된 한 줄 요약"
    assert summary["court_reasoning"] == "저장된 판단"
