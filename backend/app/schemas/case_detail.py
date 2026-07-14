from pydantic import BaseModel


class CaseDetailResponse(BaseModel):
    case_id: str
    case_number: str
    case_name: str
    court_name: str
    court_department: str
    decision_date: str | None
    category: str
    judgment_result: str
    order_text: str
    original_text: str
    source_name: str
    source_url: str
    summary: str
    main_issues: list[str]
