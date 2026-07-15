from app.core.config import Settings
from app.services.case_search_service import CaseSearchService

import pytest


def test_default_similarity_mode_is_free_local_hash():
    settings = Settings()

    assert settings.similarity_mode == "local_hash"


def test_search_service_rejects_unsupported_similarity_mode():
    with pytest.raises(ValueError, match="Unsupported similarity mode"):
        CaseSearchService(similarity_mode="paid_remote")
