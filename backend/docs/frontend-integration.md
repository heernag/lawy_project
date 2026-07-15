# Frontend Integration Guide

Run the backend:

```powershell
cd backend
python -m uvicorn app.main:app --reload
```

Swagger: `http://localhost:8000/docs`

OpenAPI JSON: `http://localhost:8000/openapi.json`

Health check: `GET http://localhost:8000/api/health`

Use `data.checks.sample_data_loaded` to confirm the MVP sample judgments were
loaded before testing search screens.

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
patterns. Road-name text followed by a Korean amount expression such as
`123만 원` is not treated as an address.
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

## Validation Error Examples

All invalid request bodies use HTTP 400 with the common API error shape. Treat
`error.code` as the stable field for UI branching.

Missing required field:

```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Request validation failed.",
    "details": [
      {
        "type": "missing",
        "loc": ["body", "query"],
        "msg": "Field required"
      }
    ]
  }
}
```

Invalid search pagination:

```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Request validation failed.",
    "details": [
      {
        "type": "greater_than_equal",
        "loc": ["body", "page"],
        "msg": "Input should be greater than or equal to 1"
      }
    ]
  }
}
```

Production-like environments hide validation details:

```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Request validation failed.",
    "details": null
  }
}
```

Recommended client handling:

```typescript
function getErrorMessage(error: ApiError | null): string {
  if (!error) return "요청 처리 중 알 수 없는 오류가 발생했습니다.";

  if (error.code === "INVALID_REQUEST") {
    return "입력값을 다시 확인해 주세요.";
  }

  if (error.code === "CASE_NOT_FOUND") {
    return "판결문을 찾을 수 없습니다.";
  }

  return error.message;
}
```

## User Notice

This service is a reference tool for searching and understanding stored public or sample judgments. It is not legal advice and does not predict win/loss probability.
