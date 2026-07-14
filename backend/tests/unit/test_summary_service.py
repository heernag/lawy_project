from app.services.summary_service import SummaryService


def test_summary_uses_only_existing_sample_case_text():
    result = SummaryService().summarize("sample-001")

    assert result is not None
    assert result["one_line_summary"] == "중고 노트북 하자와 환불 거부에 관한 샘플 사건입니다."
    assert "매매 목적물의 하자" in result["main_issues"]
