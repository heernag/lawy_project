from app.services.local_similarity_service import LocalSimilarityService


def test_similarity_scores_overlap_higher_than_unrelated_text():
    service = LocalSimilarityService()

    related = service.score("노트북 하자 환불", "중고 노트북에 하자가 있어 환불을 구한 사건")
    unrelated = service.score("노트북 하자 환불", "임금과 퇴직금 지급에 관한 사건")

    assert related > unrelated
    assert 0 <= related <= 1


def test_similarity_uses_embedding_provider_when_tokens_do_not_overlap():
    class FakeEmbeddingProvider:
        def embed(self, text):
            if text == "query":
                return [1.0, 0.0]
            return [1.0, 0.0]

    service = LocalSimilarityService(embedding_provider=FakeEmbeddingProvider())

    score = service.score("query", "document")

    assert score > 0
