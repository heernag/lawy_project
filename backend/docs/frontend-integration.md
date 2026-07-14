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

## User Notice

This service is a reference tool for searching and understanding stored public or sample judgments. It is not legal advice and does not predict win/loss probability.
