from app.services.summary_service import SummaryService


def test_summary_uses_only_existing_sample_case_text():
    result = SummaryService().summarize("sample-001")

    assert result is not None
    assert result["one_line_summary"] == "중고 노트북 하자와 환불 거부에 관한 샘플 사건입니다."
    assert "매매 목적물의 하자" in result["main_issues"]


class SummaryMemoryProvider:
    def __init__(self):
        self.saved_summary = {
            "one_line_summary": "저장된 요약",
            "background": "저장된 배경",
            "plaintiff_claim": "",
            "defendant_claim": "",
            "court_reasoning": "저장된 판단",
            "judgment_result": "저장된 결과",
        }
        self.upsert_count = 0

    def get_case(self, case_id):
        return {
            "case_id": case_id,
            "original_text": "이유\n새 배경\n법원의 판단\n새 판단",
            "summary": "새 요약",
            "judgment_result": "인용",
            "main_issues": ["쟁점"],
        }

    def get_summary(self, case_id):
        return self.saved_summary

    def upsert_summary(self, case_id, summary):
        self.upsert_count += 1
        self.saved_summary = summary


def test_summary_reuses_stored_summary_when_force_regenerate_is_false():
    provider = SummaryMemoryProvider()

    result = SummaryService(provider=provider).summarize("sample-001", force_regenerate=False)

    assert result["one_line_summary"] == "저장된 요약"
    assert provider.upsert_count == 0


def test_summary_regenerates_and_stores_when_force_regenerate_is_true():
    provider = SummaryMemoryProvider()

    result = SummaryService(provider=provider).summarize("sample-001", force_regenerate=True)

    assert result["one_line_summary"] == "새 요약"
    assert provider.upsert_count == 1
