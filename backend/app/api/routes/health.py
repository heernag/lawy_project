from fastapi import APIRouter, Depends

from app.api.dependencies import get_case_provider
from app.core.responses import api_success
from app.providers.base_case_provider import CaseProvider
from app.services.health_service import HealthService

router = APIRouter()


@router.get("/health")
def health(provider: CaseProvider = Depends(get_case_provider)):
    return api_success(HealthService(provider).check())
