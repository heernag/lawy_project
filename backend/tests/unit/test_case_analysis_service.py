from app.services.case_analysis_service import CaseAnalysisService


def test_analyze_used_goods_refund_without_adding_facts():
    query = "중고 노트북을 구매했는데 제품이 고장 났고 판매자가 환불을 거부합니다."

    result = CaseAnalysisService().analyze(query)

    assert result.category == "민사"
    assert result.sub_category == "매매계약"
    assert "구매자" in result.parties
    assert "판매자" in result.parties
    assert "중고" in result.search_keywords
    assert all("폭행" not in fact for fact in result.facts)


def test_analyze_warns_about_possible_phone_number():
    query = "010-1234-5678 번호로 연락했는데 환불을 거부합니다."

    result = CaseAnalysisService().analyze(query)

    assert result.privacy_warnings
    assert "전화번호" in result.privacy_warnings[0]
