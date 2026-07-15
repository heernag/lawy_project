from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.api.dependencies import get_case_provider
from app.core.errors import CASE_NOT_FOUND, INVALID_REQUEST
from app.core.responses import api_error, api_success
from app.providers.base_case_provider import CaseProvider
from app.schemas.case_analysis import CaseAnalysisRequest
from app.schemas.search import CaseSearchRequest
from app.schemas.simplification import SimplificationRequest
from app.schemas.summary import SummaryRequest
from app.services.case_analysis_service import CaseAnalysisService
from app.services.case_detail_service import CaseDetailService
from app.services.case_search_service import CaseSearchService
from app.services.legal_term_service import LegalTermService
from app.services.simplification_service import SimplificationService
from app.services.summary_service import SummaryService

router = APIRouter()


@router.post("/cases/analyze")
def analyze_case(request: CaseAnalysisRequest):
    query = request.query.strip()
    if len(query) < 5 or len(query) > 2000:
        return JSONResponse(
            status_code=400,
            content=api_error(INVALID_REQUEST, "사건 설명은 5자 이상 2000자 이하로 입력해야 합니다."),
        )
    return api_success(CaseAnalysisService().analyze(query).model_dump())


@router.post("/cases/search")
def search_cases(request: CaseSearchRequest, provider: CaseProvider = Depends(get_case_provider)):
    if not request.query.strip():
        return JSONResponse(
            status_code=400,
            content=api_error(INVALID_REQUEST, "검색어를 입력해야 합니다."),
        )
    return api_success(CaseSearchService(provider=provider).search(request).model_dump())


@router.get("/cases/{case_id}")
def get_case(case_id: str, provider: CaseProvider = Depends(get_case_provider)):
    result = CaseDetailService(provider=provider).get_case_detail(case_id)
    if result is None:
        return JSONResponse(
            status_code=404,
            content=api_error(CASE_NOT_FOUND, "판결문을 찾을 수 없습니다."),
        )
    return api_success(result)


@router.get("/cases/{case_id}/sections")
def get_case_sections(case_id: str, provider: CaseProvider = Depends(get_case_provider)):
    result = CaseDetailService(provider=provider).get_case_sections(case_id)
    if result is None:
        return JSONResponse(
            status_code=404,
            content=api_error(CASE_NOT_FOUND, "판결문을 찾을 수 없습니다."),
        )
    return api_success(result)


@router.get("/cases/{case_id}/similar")
def get_similar_cases(case_id: str, provider: CaseProvider = Depends(get_case_provider)):
    result = CaseSearchService(provider=provider).similar(case_id)
    if result is None:
        return JSONResponse(
            status_code=404,
            content=api_error(CASE_NOT_FOUND, "판결문을 찾을 수 없습니다."),
        )
    return api_success(result.model_dump())


@router.get("/cases/{case_id}/legal-terms")
def get_case_legal_terms(case_id: str, provider: CaseProvider = Depends(get_case_provider)):
    if CaseDetailService(provider=provider).get_case_detail(case_id) is None:
        return JSONResponse(
            status_code=404,
            content=api_error(CASE_NOT_FOUND, "판결문을 찾을 수 없습니다."),
        )
    return api_success({"case_id": case_id, "terms": LegalTermService(provider=provider).extract_terms(case_id)})


@router.post("/cases/{case_id}/summary")
def summarize_case(case_id: str, request: SummaryRequest, provider: CaseProvider = Depends(get_case_provider)):
    result = SummaryService(provider=provider).summarize(case_id, request.force_regenerate)
    if result is None:
        return JSONResponse(
            status_code=404,
            content=api_error(CASE_NOT_FOUND, "판결문을 찾을 수 없습니다."),
        )
    return api_success(result)


@router.post("/cases/{case_id}/simplify")
def simplify_case(case_id: str, request: SimplificationRequest, provider: CaseProvider = Depends(get_case_provider)):
    result = SimplificationService(provider=provider).simplify_case(case_id, request.section_types, request.force_regenerate)
    if result is None:
        return JSONResponse(
            status_code=404,
            content=api_error(CASE_NOT_FOUND, "판결문을 찾을 수 없습니다."),
        )
    return api_success(result)


@router.get("/cases/{case_id}/simplified")
def get_simplified_case(case_id: str, provider: CaseProvider = Depends(get_case_provider)):
    result = SimplificationService(provider=provider).get_simplified_case(case_id)
    if result is None:
        return JSONResponse(
            status_code=404,
            content=api_error(CASE_NOT_FOUND, "판결문을 찾을 수 없습니다."),
        )
    return api_success(result)


@router.post("/cases/{case_id}/paragraphs/{paragraph_id}/simplify")
def simplify_single_paragraph(case_id: str, paragraph_id: str, provider: CaseProvider = Depends(get_case_provider)):
    result = SimplificationService(provider=provider).simplify_paragraph(case_id, paragraph_id)
    if result is None:
        return JSONResponse(
            status_code=404,
            content=api_error(CASE_NOT_FOUND, "판결문 또는 문단을 찾을 수 없습니다."),
        )
    return api_success(result)
