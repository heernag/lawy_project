import re


class LocalSimilarityService:
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
        return round(overlap / len(query_tokens), 4)
