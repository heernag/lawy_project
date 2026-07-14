from pydantic import BaseModel


class SimplificationRequest(BaseModel):
    section_types: list[str] | None = None
    force_regenerate: bool = False


class SimplifiedParagraph(BaseModel):
    paragraph_id: str
    original_text: str
    simplified_text: str
    validation_status: str
    warnings: list[str]
