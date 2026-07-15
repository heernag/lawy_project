from fastapi import APIRouter, Depends

from app.api.dependencies import get_case_provider
from app.core.responses import api_success
from app.providers.base_case_provider import CaseProvider

router = APIRouter()


@router.get("/health")
def health(provider: CaseProvider = Depends(get_case_provider)):
    try:
        cases = provider.search_cases("", {})
    except Exception:
        return api_success(
            {
                "status": "degraded",
                "checks": {
                    "case_provider": "error",
                    "case_count": 0,
                    "sample_data_loaded": False,
                    "message": "case provider check failed",
                },
            }
        )

    case_count = len(cases)
    return api_success(
        {
            "status": "ok" if case_count > 0 else "degraded",
            "checks": {
                "case_provider": "ok",
                "case_count": case_count,
                "sample_data_loaded": case_count > 0,
            },
        }
    )
