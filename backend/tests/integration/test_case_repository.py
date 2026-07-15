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


def test_case_repository_upserts_and_reads_case_legal_terms():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    session = sessionmaker(bind=engine)()
    repository = CaseRepository(session)
    repository.upsert_case(
        {
            "case_id": "sample-term-link",
            "case_number": "샘플-용어-001",
            "case_name": "용어 연결 사건",
            "court_name": "샘플 법원",
            "decision_date": "2025-01-01",
            "category": "민사",
            "judgment_result": "기각",
            "order_text": "원고의 청구를 기각한다.",
            "original_text": "주문\n원고의 손해배상 청구를 기각한다.",
            "summary": "손해배상 청구 기각 사건",
            "main_issues": ["손해배상"],
            "source_name": "MVP sample data",
            "source_url": "",
        }
    )
    repository.upsert_legal_term(
        {
            "term": "손해배상",
            "easy_definition": "손해를 금전 등으로 메우는 것입니다.",
            "example": "손해배상을 청구한다.",
            "caution": "손해와 책임이 인정되어야 합니다.",
            "source": "MVP built-in glossary",
        }
    )
    repository.upsert_case_legal_terms(
        "sample-term-link",
        [
            {
                "term": "손해배상",
                "context_meaning": "현재 문단에서 손해배상 청구를 뜻합니다.",
                "paragraph_id": "paragraph-1-1",
            }
        ],
    )

    terms = repository.get_case_legal_terms("sample-term-link")

    assert terms[0]["term"] == "손해배상"
    assert terms[0]["paragraph_id"] == "paragraph-1-1"
    assert terms[0]["easy_definition"] == "손해를 금전 등으로 메우는 것입니다."
