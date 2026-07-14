from pydantic import BaseModel


class SummaryRequest(BaseModel):
    force_regenerate: bool = False


class CaseSummaryResponse(BaseModel):
    one_line_summary: str
    background: str
    plaintiff_claim: str
    defendant_claim: str
    main_issues: list[str]
    court_reasoning: str
    judgment_result: str
    legal_terms: list[str]
