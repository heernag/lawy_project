from app.providers.local_hash_embedding_provider import LocalHashEmbeddingProvider


def test_local_hash_embedding_provider_returns_fixed_length_vector():
    provider = LocalHashEmbeddingProvider(dimensions=16)

    vector = provider.embed("노트북 하자 환불")

    assert len(vector) == 16
    assert any(value != 0 for value in vector)
    assert all(-1.0 <= value <= 1.0 for value in vector)


def test_local_hash_embedding_provider_is_deterministic():
    provider = LocalHashEmbeddingProvider(dimensions=16)

    first = provider.embed("노트북 하자 환불")
    second = provider.embed("노트북 하자 환불")

    assert first == second
