# Easy Case Law Backend

무료 전용 FastAPI MVP입니다.

이 백엔드는 외부 유료 LLM, 유료 임베딩 API, 유료 벡터 DB, 유료 판례 API를 사용하지 않습니다.

## Run

```powershell
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Swagger:

```text
http://localhost:8000/docs
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
SIMILARITY_MODE=local_tfidf
CASE_PROVIDER=sample
```

## Scope

Included:

- case sentence analysis
- local sample case search
- exact sample case-number search
- detail lookup
- section and paragraph splitting
- rule-based paragraph simplification
- protected-value validation
- built-in legal term glossary
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
