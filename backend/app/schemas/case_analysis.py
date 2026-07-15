from pydantic import BaseModel


class CaseAnalysisRequest(BaseModel):
    query: str


class PrivacyDetection(BaseModel):
    type: str
    label: str
    masked_value: str


class InputWarning(BaseModel):
    type: str
    message: str


class CaseAnalysisResult(BaseModel):
    category: str
    sub_category: str
    sanitized_query: str
    parties: list[str]
    dispute_target: str
    facts: list[str]
    legal_issues: list[str]
    search_keywords: list[str]
    legal_terms: list[str]
    privacy_detections: list[PrivacyDetection]
    privacy_warnings: list[str]
    input_warnings: list[InputWarning]
