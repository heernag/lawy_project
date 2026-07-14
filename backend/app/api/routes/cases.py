from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.core.errors import CASE_NOT_FOUND
from app.core.responses import api_error, api_success
from app.services.case_detail_service import CaseDetailService

router = APIRouter()


@router.get("/cases/{case_id}")
def get_case(case_id: str):
    result = CaseDetailService().get_case_detail(case_id)
    if result is None:
        return JSONResponse(
            status_code=404,
            content=api_error(CASE_NOT_FOUND, "판결문을 찾을 수 없습니다."),
        )
    return api_success(result)


@router.get("/cases/{case_id}/sections")
def get_case_sections(case_id: str):
    result = CaseDetailService().get_case_sections(case_id)
    if result is None:
        return JSONResponse(
            status_code=404,
            content=api_error(CASE_NOT_FOUND, "판결문을 찾을 수 없습니다."),
        )
    return api_success(result)
