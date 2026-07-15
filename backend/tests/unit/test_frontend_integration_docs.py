from pathlib import Path


FRONTEND_GUIDE = Path("docs/frontend-integration.md")


def test_frontend_integration_guide_documents_core_response_types():
    guide = FRONTEND_GUIDE.read_text(encoding="utf-8")

    expected_contract_fragments = [
        "export interface CaseSearchResponse",
        "total_count: number;",
        "applied_filters: Record<string, unknown>;",
        "extracted_keywords: string[];",
        "export interface CaseDetailResponse",
        "court_department: string;",
        "order_text: string;",
        "original_text: string;",
        "export interface SimplificationRequest",
        "section_types?: string[] | null;",
        "force_regenerate: boolean;",
        "export interface SimplifiedParagraph",
        "validation_status: string;",
        "warnings: string[];",
        "export interface SimplifiedCaseResponse",
        "paragraphs: SimplifiedParagraph[];",
    ]

    for fragment in expected_contract_fragments:
        assert fragment in guide
