# Frontend Integration Guide

Run the backend:

```powershell
cd backend
python -m uvicorn app.main:app --reload
```

Swagger: `http://localhost:8000/docs`

OpenAPI JSON: `http://localhost:8000/openapi.json`

Set CORS origins in `.env`:

```env
CORS_ORIGINS=http://localhost:5173
```

## TypeScript Types

```typescript
export interface ApiResponse<T> {
  success: boolean;
  data: T | null;
  error: ApiError | null;
}

export interface ApiError {
  code: string;
  message: string;
  details: unknown | null;
}

export interface PrivacyDetection {
  type:
    | "phone_number"
    | "resident_registration_number"
    | "email"
    | "address"
    | string;
  label: string;
  masked_value: string;
}

export interface InputWarning {
  type: "prompt_injection_suspected" | string;
  message: string;
}

export interface CaseAnalysisResult {
  category: string;
  sub_category: string;
  sanitized_query: string;
  parties: string[];
  dispute_target: string;
  facts: string[];
  legal_issues: string[];
  search_keywords: string[];
  legal_terms: string[];
  privacy_detections: PrivacyDetection[];
  privacy_warnings: string[];
  input_warnings: InputWarning[];
}

export interface CaseSearchRequest {
  query: string;
  category?: string | null;
  court?: string | null;
  start_date?: string | null;
  end_date?: string | null;
  judgment_result?: string | null;
  page: number;
  size: number;
}

export interface CaseSearchItem {
  case_id: string;
  case_number: string;
  case_name: string;
  court_name: string;
  decision_date: string | null;
  category: string;
  judgment_result: string;
  summary: string;
  main_issues: string[];
  similarity_score: number;
  similarity_reason: string;
  source_name: string;
  source_url: string;
}
```

## Fetch Example

```typescript
const response = await fetch("http://localhost:8000/api/cases/search", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    query: "중고 노트북 하자 환불",
    page: 1,
    size: 10,
  }),
});

const data = await response.json();
```

For `/api/cases/analyze`, use `sanitized_query` for any client-side preview
after privacy detection. Keep the original user input only in local form state
unless the user explicitly submits it for the next backend action.
Privacy detection is local and currently covers phone numbers, resident-
registration-number patterns, email addresses, and clear Korean road-address
patterns.
The backend rejects analysis queries shorter than 5 characters or longer than
2000 characters. Display `input_warnings` as caution text, not as a legal
conclusion.
For search, send `page >= 1` and `1 <= size <= 50`. Invalid request bodies are
returned as HTTP 400 with `error.code === "INVALID_REQUEST"`.
Malformed JSON and missing required fields also use this same error shape.
Do not rely on `error.details` being present. It is available in development-
like environments and hidden in production-like environments.
Search `query` is normalized by trimming and collapsing repeated whitespace;
the normalized value must be 2 to 500 characters.
Date filters must be `YYYY-MM-DD`; when both dates are present, `start_date`
must be earlier than or equal to `end_date`.

## User Notice

This service is a reference tool for searching and understanding stored public or sample judgments. It is not legal advice and does not predict win/loss probability.
