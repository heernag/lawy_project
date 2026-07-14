from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.core.errors import CASE_NOT_FOUND, INVALID_REQUEST
from app.core.responses import api_error, api_success
from app.schemas.case_analysis import CaseAnalysisRequest
from app.schemas.search import CaseSearchRequest
from app.schemas.summary import SummaryRequest
from app.services.case_analysis_service import CaseAnalysisService
from app.services.case_detail_service import CaseDetailService
from app.services.case_search_service import CaseSearchService
from app.services.legal_term_service import LegalTermService
from app.services.summary_service import SummaryService

router = APIRouter()


@router.post("/cases/analyze")
def analyze_case(request: CaseAnalysisRequest):
    query = request.query.strip()
    if not query or len(query) > 2000:
        return JSONResponse(
            status_code=400,
            content=api_error(INVALID_REQUEST, "사건 설명은 1자 이상 2000자 이하로 입력해야 합니다."),
        )
    return api_success(CaseAnalysisService().analyze(query).model_dump())


@router.post("/cases/search")
def search_cases(request: CaseSearchRequest):
    if not request.query.strip():
        return JSONResponse(
            status_code=400,
            content=api_error(INVALID_REQUEST, "검색어를 입력해야 합니다."),
        )
    return api_success(CaseSearchService().search(request).model_dump())


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


@router.get("/cases/{case_id}/similar")
def get_similar_cases(case_id: str):
    result = CaseSearchService().similar(case_id)
    if result is None:
        return JSONResponse(
            status_code=404,
            content=api_error(CASE_NOT_FOUND, "판결문을 찾을 수 없습니다."),
        )
    return api_success(result.model_dump())


@router.get("/cases/{case_id}/legal-terms")
def get_case_legal_terms(case_id: str):
    if CaseDetailService().get_case_detail(case_id) is None:
        return JSONResponse(
            status_code=404,
            content=api_error(CASE_NOT_FOUND, "판결문을 찾을 수 없습니다."),
        )
    return api_success({"case_id": case_id, "terms": LegalTermService().extract_terms(case_id)})


@router.post("/cases/{case_id}/summary")
def summarize_case(case_id: str, request: SummaryRequest):
    result = SummaryService().summarize(case_id, request.force_regenerate)
    if result is None:
        return JSONResponse(
            status_code=404,
            content=api_error(CASE_NOT_FOUND, "판결문을 찾을 수 없습니다."),
        )
    return api_success(result)
