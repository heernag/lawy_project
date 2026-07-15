import hashlib
import math
import re

from app.providers.base_embedding_provider import EmbeddingProvider


class LocalHashEmbeddingProvider(EmbeddingProvider):
    def __init__(self, dimensions: int = 128):
        if dimensions <= 0:
            raise ValueError("dimensions must be positive")
        self.dimensions = dimensions

    def embed(self, text: str) -> list[float]:
        vector = [0.0] * self.dimensions
        for token in self._tokenize(text):
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            index = int.from_bytes(digest[:4], "big") % self.dimensions
            sign = 1.0 if digest[4] % 2 == 0 else -1.0
            vector[index] += sign

        magnitude = math.sqrt(sum(value * value for value in vector))
        if magnitude == 0:
            return vector
        return [round(value / magnitude, 6) for value in vector]

    def _tokenize(self, text: str) -> list[str]:
        return [token for token in re.split(r"[\s,.;:!?()\[\]{}\"']+", text.lower()) if token]
