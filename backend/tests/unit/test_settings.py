from app.core.config import Settings


def test_default_similarity_mode_is_free_local_hash():
    settings = Settings()

    assert settings.similarity_mode == "local_hash"
