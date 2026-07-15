# API Spec

Base URL: `http://localhost:8000`

All responses use:

```json
{
  "success": true,
  "data": {},
  "error": null
}
```

Errors use:

```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "CASE_NOT_FOUND",
    "message": "판결문을 찾을 수 없습니다.",
    "details": null
  }
}
```

Request body validation errors also use this common format with HTTP 400 and
`INVALID_REQUEST`; the frontend does not need a separate FastAPI 422 parser.
Malformed JSON bodies and missing required request fields use the same common
error format.
Validation `details` are included in `development`, `local`, and `test`
environments. In production-like environments, `details` are returned as `null`
to avoid exposing internal validation metadata.

## Endpoints

### `GET /api/health`

Returns server health.

### `POST /api/cases/analyze`

Analyzes a user dispute sentence and returns category, extracted facts,
keywords, and privacy handling fields. Response data includes `sanitized_query`
and `privacy_detections`. The MVP masks phone numbers, resident-registration
number patterns, email addresses, and clear Korean road-address patterns
locally with regular expressions.
Queries shorter than 5 characters or longer than 2000 characters return
`INVALID_REQUEST`. Prompt-injection-like phrases are not executed as
instructions; they are returned as `input_warnings` for client display.

Request:

```json
{
  "query": "중고 노트북을 구매했는데 제품이 고장 났고 판매자가 환불을 거부합니다."
}
```

### `POST /api/cases/search`

Request:

```json
{
  "query": "중고 노트북 하자 환불",
  "category": "민사",
  "court": null,
  "start_date": null,
  "end_date": null,
  "judgment_result": null,
  "page": 1,
  "size": 10
}
```

Search uses exact case-number matching, metadata filters, keyword overlap, and locally stored search-index text from SQLite. It does not call paid embedding APIs.
`query` is trimmed, repeated whitespace is collapsed, and the normalized value
must be between 2 and 500 characters.
`page` must be 1 or greater. `size` must be between 1 and 50.
`start_date` and `end_date` must use `YYYY-MM-DD`. If both are provided,
`start_date` must be earlier than or equal to `end_date`.

### `GET /api/cases/{case_id}`

Returns a stored sample case. Unknown IDs return `CASE_NOT_FOUND`.

### `GET /api/cases/{case_id}/sections`

Returns sections and paragraphs with stable paragraph IDs. Sections and paragraphs are loaded from SQLite after startup bootstrap.
The section splitter recognizes common headings such as `주문`, `청구 취지`,
`이유`, `원고 주장`, `피고 주장`, and `법원의 판단`, including simple
numbered forms like `1. 주문` and aliases like `원고의 주장`.

### `POST /api/cases/{case_id}/summary`

Request:

```json
{
  "force_regenerate": false
}
```

When `force_regenerate` is `false`, a stored summary is reused if one exists. When it is `true`, the rule-based summary is regenerated and stored in SQLite.

### `POST /api/cases/{case_id}/simplify`

Request:

```json
{
  "section_types": ["주문", "법원의 판단"],
  "force_regenerate": false
}
```

### `GET /api/cases/{case_id}/simplified`

Returns generated rule-based simplified paragraphs. If a paragraph was already simplified and stored, the stored result is reused.

### `POST /api/cases/{case_id}/paragraphs/{paragraph_id}/simplify`

Regenerates one paragraph and stores its simplified text, validation status, and warnings in SQLite.

### `GET /api/legal-terms/{term}`

Returns a legal term definition loaded from the SQLite-backed MVP glossary.

### `GET /api/cases/{case_id}/legal-terms`

Extracts legal terms from a stored sample case. Results include paragraph IDs when a term is found in a specific paragraph, and extracted case-term links are persisted in SQLite for reuse.

### `GET /api/cases/{case_id}/similar`

Returns locally similar stored sample cases. The score is not a prediction of litigation outcome.

## Error Codes

- `INVALID_REQUEST`
- `CASE_NOT_FOUND`
- `CASE_PROVIDER_ERROR`
- `SEARCH_FAILED`
- `SIMPLIFICATION_FAILED`
- `VALIDATION_FAILED`
- `RATE_LIMIT_EXCEEDED`
- `INTERNAL_SERVER_ERROR`
