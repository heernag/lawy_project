from app.services.local_similarity_service import LocalSimilarityService


def test_similarity_scores_overlap_higher_than_unrelated_text():
    service = LocalSimilarityService()

    related = service.score("노트북 하자 환불", "중고 노트북에 하자가 있어 환불을 구한 사건")
    unrelated = service.score("노트북 하자 환불", "임금과 퇴직금 지급에 관한 사건")

    assert related > unrelated
    assert 0 <= related <= 1
