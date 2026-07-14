from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.core.errors import INVALID_REQUEST
from app.core.responses import api_error, api_success
from app.services.legal_term_service import LegalTermService

router = APIRouter()


@router.get("/legal-terms/{term}")
def get_legal_term(term: str):
    result = LegalTermService().get_term(term)
    if result is None:
        return JSONResponse(
            status_code=404,
            content=api_error(INVALID_REQUEST, "법률 용어를 찾을 수 없습니다."),
        )
    return api_success(result)
