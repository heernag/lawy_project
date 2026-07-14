from pydantic import BaseModel, Field


class CaseSearchRequest(BaseModel):
    query: str
    category: str | None = None
    court: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    judgment_result: str | None = None
    page: int = Field(default=1, ge=1)
    size: int = Field(default=10, ge=1, le=50)


class CaseSearchItem(BaseModel):
    case_id: str
    case_number: str
    case_name: str
    court_name: str
    decision_date: str | None
    category: str
    judgment_result: str
    summary: str
    main_issues: list[str]
    similarity_score: float
    similarity_reason: str
    source_name: str
    source_url: str


class CaseSearchResponse(BaseModel):
    total_count: int
    page: int
    size: int
    results: list[CaseSearchItem]
    applied_filters: dict
    extracted_keywords: list[str]
