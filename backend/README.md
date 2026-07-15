# Easy Case Law Backend

Free-only FastAPI MVP for Korean case-law search and easy explanations.

This backend does not use paid LLM APIs, paid embedding APIs, paid vector databases, or paid case-data APIs.
Search uses local keyword matching and a free local hash-embedding fallback.

## Run

```powershell
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

On startup, the app creates the SQLite tables and loads `data/sample_cases.json` and `data/legal_terms.json` into the local database.

Swagger:

```text
http://localhost:8000/docs
```

OpenAPI JSON:

```text
http://localhost:8000/openapi.json
```

Bruno collection:

```text
backend/bruno
```

Korean frontend flow guide:

```text
backend/docs/frontend-flow-ko.md
```

## Test

```powershell
cd backend
python -m pytest -v
```

## Environment

Copy `.env.example` to `.env` if local overrides are needed.

```env
APP_ENV=development
DATABASE_URL=sqlite:///./easy_case_law.db
CORS_ORIGINS=http://localhost:5173
LOG_LEVEL=INFO
SIMILARITY_MODE=local_hash
CASE_PROVIDER=sample
```

## Scope

Included:

- case sentence analysis
- local sample case search
- local hash-embedding similarity fallback
- exact sample case-number search
- detail lookup
- section and paragraph splitting
- rule-based paragraph simplification
- protected-value validation
- built-in legal term glossary
- SQLite-backed glossary lookup
- CORS
- Swagger and OpenAPI

Excluded:

- frontend
- login
- payment
- admin pages
- paid AI APIs
- litigation outcome prediction
- unauthorized crawling
- non-public judgment access
