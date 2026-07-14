from pydantic import BaseModel


class CaseAnalysisRequest(BaseModel):
    query: str


class CaseAnalysisResult(BaseModel):
    category: str
    sub_category: str
    parties: list[str]
    dispute_target: str
    facts: list[str]
    legal_issues: list[str]
    search_keywords: list[str]
    legal_terms: list[str]
    privacy_warnings: list[str]
