from datetime import date
import re

from pydantic import BaseModel, Field, field_validator, model_validator


class CaseSearchRequest(BaseModel):
    query: str
    category: str | None = None
    court: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    judgment_result: str | None = None
    page: int = Field(default=1, ge=1)
    size: int = Field(default=10, ge=1, le=50)

    @field_validator("query")
    @classmethod
    def normalize_query(cls, value: str) -> str:
        normalized = re.sub(r"\s+", " ", value).strip()
        if len(normalized) < 2 or len(normalized) > 500:
            raise ValueError("검색어는 2자 이상 500자 이하로 입력해야 합니다.")
        return normalized

    @field_validator("start_date", "end_date")
    @classmethod
    def validate_date_format(cls, value: str | None) -> str | None:
        if value is None:
            return value
        try:
            date.fromisoformat(value)
        except ValueError as exc:
            raise ValueError("날짜는 YYYY-MM-DD 형식이어야 합니다.") from exc
        return value

    @model_validator(mode="after")
    def validate_date_range(self) -> "CaseSearchRequest":
        if self.start_date and self.end_date:
            if date.fromisoformat(self.start_date) > date.fromisoformat(self.end_date):
                raise ValueError("start_date는 end_date보다 늦을 수 없습니다.")
        return self


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
