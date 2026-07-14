from pydantic import BaseModel


class LegalTermResponse(BaseModel):
    term: str
    easy_definition: str
    context_meaning: str = ""
    example: str
    caution: str
    source: str
