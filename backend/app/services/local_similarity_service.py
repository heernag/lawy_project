import re

from app.providers.base_embedding_provider import EmbeddingProvider
from app.providers.local_hash_embedding_provider import LocalHashEmbeddingProvider


class LocalSimilarityService:
    def __init__(self, embedding_provider: EmbeddingProvider | None = None):
        self.embedding_provider = embedding_provider or LocalHashEmbeddingProvider()

    def tokenize(self, text: str) -> set[str]:
        tokens = re.split(r"[\s,.;:!?()\[\]{}\"']+", text)
        return {token.strip() for token in tokens if token.strip()}

    def score(self, query: str, document: str) -> float:
        query_tokens = self.tokenize(query)
        document_tokens = self.tokenize(document)
        if not query_tokens or not document_tokens:
            return 0.0
        overlap = 0
        for query_token in query_tokens:
            if query_token in document_tokens or any(query_token in document_token for document_token in document_tokens):
                overlap += 1
        keyword_score = overlap / len(query_tokens)
        vector_score = self._cosine_similarity(
            self.embedding_provider.embed(query),
            self.embedding_provider.embed(document),
        )
        return round(max(keyword_score, vector_score), 4)

    def _cosine_similarity(self, left: list[float], right: list[float]) -> float:
        if not left or not right or len(left) != len(right):
            return 0.0
        dot_product = sum(left_value * right_value for left_value, right_value in zip(left, right))
        if dot_product <= 0:
            return 0.0
        return min(dot_product, 1.0)
