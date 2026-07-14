# Free Case Law Backend Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a free-only FastAPI backend MVP for Korean case-law search, case analysis, judgment detail lookup, paragraph simplification, validation, and frontend integration docs.

**Architecture:** FastAPI exposes thin REST routes. Services hold business logic, repositories isolate SQLite access, and providers isolate sample case data, rule-based analysis, rule-based simplification, and local similarity search. No paid LLM, paid embedding API, paid vector DB, or paid case data API is used.

**Tech Stack:** Python, FastAPI, Pydantic, SQLAlchemy, SQLite, pytest, httpx TestClient, local TF-IDF-style similarity using standard Python collections.

## Global Constraints

- 기본 실행에 유료 API 키가 필요하지 않아야 한다.
- OpenRouter, OpenAI, Anthropic, Gemini 등 외부 유료 LLM Provider는 MVP 구현 범위에서 제외한다.
- 외부 유료 임베딩 API를 사용하지 않는다.
- 벡터 검색은 로컬에서 실행 가능한 방식으로 구현한다.
- 판결문 데이터는 우선 `SampleCaseProvider`와 샘플 JSON을 사용한다.
- 공식 판례 API는 향후 확장 지점으로만 문서화하고, 이용 조건 확인 전에는 자동 호출하지 않는다.
- API 키가 없을 때 유료 서비스로 fallback하는 코드를 작성하지 않는다.
- 운영 전환 문서에서도 유료 서비스 사용을 권장 기본값으로 두지 않는다.
- 응답 JSON 필드는 `snake_case`로 유지한다.
- 사용자 입력 원문 전체를 로그에 남기지 않는다.
- 존재하지 않는 판결문, 사건번호, 법률 조항, 데이터 출처를 생성하지 않는다.

---

## File Structure

- Create `backend/app/main.py`: FastAPI app factory, router mounting, CORS.
- Create `backend/app/core/config.py`: environment settings with free-only defaults.
- Create `backend/app/core/responses.py`: common success/error response helpers.
- Create `backend/app/core/errors.py`: error code constants and API exception mapping.
- Create `backend/app/db/session.py`: SQLite engine and session dependency.
- Create `backend/app/db/base.py`: SQLAlchemy declarative base.
- Create `backend/app/models/case.py`: ORM models for cases, sections, paragraphs, summaries, legal terms.
- Create `backend/app/schemas/*.py`: Pydantic request/response schemas.
- Create `backend/app/providers/sample_case_provider.py`: reads `backend/data/sample_cases.json`.
- Create `backend/app/services/*.py`: analysis, search, detail, paragraph, simplification, validation, legal term services.
- Create `backend/app/repositories/*.py`: case and legal term persistence.
- Create `backend/app/api/routes/*.py`: route modules.
- Create `backend/data/sample_cases.json`: small sample data with clearly marked sample source.
- Create `backend/tests/unit/*.py`: unit tests.
- Create `backend/tests/integration/*.py`: API integration tests.
- Create `backend/docs/*.md`: API, frontend, data policy, validation policy docs.
- Create `backend/requirements.txt`, `backend/.env.example`, `backend/.gitignore`, `backend/README.md`.

---

### Task 1: Project Skeleton, Config, Common Responses

**Files:**
- Create: `backend/requirements.txt`
- Create: `backend/.env.example`
- Create: `backend/.gitignore`
- Create: `backend/app/__init__.py`
- Create: `backend/app/core/config.py`
- Create: `backend/app/core/errors.py`
- Create: `backend/app/core/responses.py`
- Create: `backend/app/main.py`
- Create: `backend/app/api/__init__.py`
- Create: `backend/app/api/routes/__init__.py`
- Create: `backend/app/api/routes/health.py`
- Test: `backend/tests/integration/test_health.py`

**Interfaces:**
- Produces: `get_settings() -> Settings`
- Produces: `api_success(data: Any) -> dict[str, Any]`
- Produces: `api_error(code: str, message: str, details: Any | None = None) -> dict[str, Any]`
- Produces: `create_app() -> FastAPI`

- [ ] **Step 1: Write the failing health test**

```python
from fastapi.testclient import TestClient

from app.main import create_app


def test_health_returns_common_success_response():
    client = TestClient(create_app())

    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "data": {"status": "ok"},
        "error": None,
    }
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd backend; pytest tests/integration/test_health.py -v`

Expected: FAIL because `app.main` does not exist.

- [ ] **Step 3: Add requirements**

```text
fastapi
uvicorn
pydantic
pydantic-settings
sqlalchemy
pytest
httpx
python-dotenv
```

- [ ] **Step 4: Add `.env.example`**

```env
APP_ENV=development
DATABASE_URL=sqlite:///./easy_case_law.db
CORS_ORIGINS=http://localhost:5173
LOG_LEVEL=INFO
SIMILARITY_MODE=local_tfidf
CASE_PROVIDER=sample
```

- [ ] **Step 5: Add `.gitignore`**

```gitignore
.env
__pycache__/
.pytest_cache/
*.pyc
*.db
chroma_db/
```

- [ ] **Step 6: Implement config**

```python
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    database_url: str = "sqlite:///./easy_case_law.db"
    cors_origins: str = "http://localhost:5173"
    log_level: str = "INFO"
    similarity_mode: str = "local_tfidf"
    case_provider: str = "sample"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
```

- [ ] **Step 7: Implement response helpers and errors**

```python
from typing import Any


def api_success(data: Any) -> dict[str, Any]:
    return {"success": True, "data": data, "error": None}


def api_error(code: str, message: str, details: Any | None = None) -> dict[str, Any]:
    return {
        "success": False,
        "data": None,
        "error": {"code": code, "message": message, "details": details},
    }
```

```python
INVALID_REQUEST = "INVALID_REQUEST"
CASE_NOT_FOUND = "CASE_NOT_FOUND"
CASE_PROVIDER_ERROR = "CASE_PROVIDER_ERROR"
SEARCH_FAILED = "SEARCH_FAILED"
SIMPLIFICATION_FAILED = "SIMPLIFICATION_FAILED"
VALIDATION_FAILED = "VALIDATION_FAILED"
INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
```

- [ ] **Step 8: Implement FastAPI app and health route**

```python
from fastapi import APIRouter

from app.core.responses import api_success

router = APIRouter()


@router.get("/health")
def health():
    return api_success({"status": "ok"})
```

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import health
from app.core.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="Easy Case Law Backend", version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(health.router, prefix="/api", tags=["health"])
    return app


app = create_app()
```

- [ ] **Step 9: Run test to verify it passes**

Run: `cd backend; pytest tests/integration/test_health.py -v`

Expected: PASS.

- [ ] **Step 10: Commit**

```bash
git add backend
git commit -m "feat: add free backend skeleton"
```

---

### Task 2: Database Models, Session, Sample Data Loading

**Files:**
- Create: `backend/app/db/base.py`
- Create: `backend/app/db/session.py`
- Create: `backend/app/models/__init__.py`
- Create: `backend/app/models/case.py`
- Create: `backend/app/repositories/case_repository.py`
- Create: `backend/app/providers/base_case_provider.py`
- Create: `backend/app/providers/sample_case_provider.py`
- Create: `backend/data/sample_cases.json`
- Test: `backend/tests/unit/test_sample_case_provider.py`
- Test: `backend/tests/integration/test_case_repository.py`

**Interfaces:**
- Consumes: `get_settings()`
- Produces: `CaseProvider.search_cases(query: str, filters: dict) -> list[dict]`
- Produces: `CaseProvider.get_case(case_id: str) -> dict | None`
- Produces: `CaseRepository.upsert_case(raw_case: dict) -> CaseDocument`
- Produces: `CaseRepository.get_case(case_id: str) -> CaseDocument | None`

- [ ] **Step 1: Write provider test**

```python
from pathlib import Path

from app.providers.sample_case_provider import SampleCaseProvider


def test_sample_provider_returns_only_cases_from_json():
    provider = SampleCaseProvider(Path("data/sample_cases.json"))

    results = provider.search_cases("노트북 환불", {})

    assert len(results) >= 1
    assert results[0]["case_id"].startswith("sample-")
    assert results[0]["source_name"] == "MVP sample data"
```

- [ ] **Step 2: Run provider test to verify it fails**

Run: `cd backend; pytest tests/unit/test_sample_case_provider.py -v`

Expected: FAIL because provider does not exist.

- [ ] **Step 3: Add sample data**

Create at least three sample cases. Use `sample-001`, `sample-002`, `sample-003`. Mark source as `MVP sample data` and source URL as empty string or local documentation reference. Do not use real 사건번호 unless verified.

- [ ] **Step 4: Implement provider interface and sample provider**

```python
from abc import ABC, abstractmethod
from typing import Any


class CaseProvider(ABC):
    @abstractmethod
    def search_cases(self, query: str, filters: dict[str, Any]) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def get_case(self, case_id: str) -> dict[str, Any] | None:
        raise NotImplementedError
```

```python
import json
from pathlib import Path
from typing import Any

from app.providers.base_case_provider import CaseProvider


class SampleCaseProvider(CaseProvider):
    def __init__(self, path: Path):
        self.path = path

    def _load(self) -> list[dict[str, Any]]:
        return json.loads(self.path.read_text(encoding="utf-8"))

    def search_cases(self, query: str, filters: dict[str, Any]) -> list[dict[str, Any]]:
        query_terms = [term for term in query.split() if term]
        cases = self._load()
        if not query_terms:
            return cases
        return [
            case
            for case in cases
            if any(term in case.get("original_text", "") or term in case.get("case_name", "") for term in query_terms)
        ]

    def get_case(self, case_id: str) -> dict[str, Any] | None:
        for case in self._load():
            if case.get("case_id") == case_id:
                return case
        return None
```

- [ ] **Step 5: Implement SQLAlchemy models**

Create ORM models matching the spec. Store `validation_warnings` as JSON text for SQLite portability.

- [ ] **Step 6: Implement repository**

Repository maps provider dictionaries into ORM rows and preserves source fields exactly as provided.

- [ ] **Step 7: Run tests**

Run: `cd backend; pytest tests/unit/test_sample_case_provider.py tests/integration/test_case_repository.py -v`

Expected: PASS.

- [ ] **Step 8: Commit**

```bash
git add backend
git commit -m "feat: add sample case persistence"
```

---

### Task 3: Paragraph Sectioning and Detail Lookup

**Files:**
- Create: `backend/app/services/paragraph_service.py`
- Create: `backend/app/services/case_detail_service.py`
- Create: `backend/app/schemas/case_detail.py`
- Create: `backend/app/api/routes/cases.py`
- Modify: `backend/app/main.py`
- Test: `backend/tests/unit/test_paragraph_service.py`
- Test: `backend/tests/integration/test_case_detail_api.py`

**Interfaces:**
- Produces: `ParagraphService.split_sections(original_text: str) -> list[SectionResult]`
- Produces: `CaseDetailService.get_case_detail(case_id: str) -> dict`
- Produces: `GET /api/cases/{case_id}`
- Produces: `GET /api/cases/{case_id}/sections`

- [ ] **Step 1: Write paragraph service tests**

```python
from app.services.paragraph_service import ParagraphService


def test_split_sections_preserves_order_and_original_text():
    text = "주문\n피고는 원고에게 500만 원을 지급하라.\n이유\n원고는 노트북을 구매하였다."

    sections = ParagraphService().split_sections(text)

    assert sections[0].section_type == "주문"
    assert sections[0].paragraphs[0].original_text == "피고는 원고에게 500만 원을 지급하라."
    assert sections[1].section_type == "이유"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd backend; pytest tests/unit/test_paragraph_service.py -v`

Expected: FAIL because service does not exist.

- [ ] **Step 3: Implement section result dataclasses**

```python
from dataclasses import dataclass


@dataclass
class ParagraphResult:
    paragraph_id: str
    paragraph_order: int
    original_text: str


@dataclass
class SectionResult:
    section_id: str
    section_type: str
    section_order: int
    original_text: str
    paragraphs: list[ParagraphResult]
```

- [ ] **Step 4: Implement deterministic section splitting**

Recognize exact section headings: `주문`, `청구 취지`, `이유`, `인정 사실`, `원고 주장`, `피고 주장`, `법원의 판단`, `결론`, `관련 법령`. If no heading is found, return one section with `section_type="원문"`.

- [ ] **Step 5: Implement detail service and routes**

Routes return stored case detail and generated sections in common response format. Missing case returns `CASE_NOT_FOUND`.

- [ ] **Step 6: Run tests**

Run: `cd backend; pytest tests/unit/test_paragraph_service.py tests/integration/test_case_detail_api.py -v`

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add backend
git commit -m "feat: add case detail and paragraph sectioning"
```

---

### Task 4: Rule-Based Case Analysis

**Files:**
- Create: `backend/app/schemas/case_analysis.py`
- Create: `backend/app/services/case_analysis_service.py`
- Modify: `backend/app/api/routes/cases.py`
- Test: `backend/tests/unit/test_case_analysis_service.py`
- Test: `backend/tests/integration/test_case_analysis_api.py`

**Interfaces:**
- Produces: `CaseAnalysisService.analyze(query: str) -> CaseAnalysisResult`
- Produces: `POST /api/cases/analyze`

- [ ] **Step 1: Write analysis tests**

```python
from app.services.case_analysis_service import CaseAnalysisService


def test_analyze_used_goods_refund_without_adding_facts():
    query = "중고 노트북을 구매했는데 제품이 고장 났고 판매자가 환불을 거부합니다."

    result = CaseAnalysisService().analyze(query)

    assert result.category == "민사"
    assert "매매계약" in result.sub_category
    assert "구매자" in result.parties
    assert "판매자" in result.parties
    assert "중고" in result.search_keywords
    assert all("폭행" not in fact for fact in result.facts)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd backend; pytest tests/unit/test_case_analysis_service.py -v`

Expected: FAIL because service does not exist.

- [ ] **Step 3: Implement schema**

Fields: `category`, `sub_category`, `parties`, `dispute_target`, `facts`, `legal_issues`, `search_keywords`, `legal_terms`, `privacy_warnings`.

- [ ] **Step 4: Implement rule-based analysis**

Use keyword maps:

- `해고`, `임금`, `퇴직금` -> 노동
- `전세`, `보증금`, `임대차` -> 민사/임대차
- `중고`, `구매`, `환불`, `하자` -> 민사/매매계약
- `교통사고`, `과실` -> 민사/손해배상
- `댓글`, `모욕` -> 형사/명예훼손 또는 모욕

Privacy warnings detect phone numbers, resident-registration-like numbers, and long address-like phrases.

- [ ] **Step 5: Add API route**

Validate query length from 1 to 2000 characters. Do not store the user query.

- [ ] **Step 6: Run tests**

Run: `cd backend; pytest tests/unit/test_case_analysis_service.py tests/integration/test_case_analysis_api.py -v`

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add backend
git commit -m "feat: add free rule-based case analysis"
```

---

### Task 5: Free Local Search

**Files:**
- Create: `backend/app/schemas/search.py`
- Create: `backend/app/services/case_search_service.py`
- Create: `backend/app/services/local_similarity_service.py`
- Modify: `backend/app/api/routes/cases.py`
- Test: `backend/tests/unit/test_local_similarity_service.py`
- Test: `backend/tests/unit/test_case_search_service.py`
- Test: `backend/tests/integration/test_case_search_api.py`

**Interfaces:**
- Produces: `LocalSimilarityService.score(query: str, document: str) -> float`
- Produces: `CaseSearchService.search(request: CaseSearchRequest) -> CaseSearchResponse`
- Produces: `POST /api/cases/search`
- Produces: `GET /api/cases/{case_id}/similar`

- [ ] **Step 1: Write local similarity test**

```python
from app.services.local_similarity_service import LocalSimilarityService


def test_similarity_scores_overlap_higher_than_unrelated_text():
    service = LocalSimilarityService()

    related = service.score("노트북 하자 환불", "중고 노트북에 하자가 있어 환불을 구한 사건")
    unrelated = service.score("노트북 하자 환불", "임금과 퇴직금 지급에 관한 사건")

    assert related > unrelated
    assert 0 <= related <= 1
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd backend; pytest tests/unit/test_local_similarity_service.py -v`

Expected: FAIL because service does not exist.

- [ ] **Step 3: Implement tokenizer and overlap score**

Tokenize Korean text by whitespace and punctuation. Compute normalized overlap. This is free and deterministic.

- [ ] **Step 4: Implement search service**

Priority:

1. Exact normalized `case_number`
2. Category filter match
3. Keyword overlap in case name, summary, issues, original text
4. Local similarity score
5. Source-preserving result metadata

- [ ] **Step 5: Implement search API**

Return `total_count`, `page`, `size`, `results`, `applied_filters`, `extracted_keywords`.

- [ ] **Step 6: Run tests**

Run: `cd backend; pytest tests/unit/test_local_similarity_service.py tests/unit/test_case_search_service.py tests/integration/test_case_search_api.py -v`

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add backend
git commit -m "feat: add free local case search"
```

---

### Task 6: Legal Terms and Summary

**Files:**
- Create: `backend/app/schemas/legal_terms.py`
- Create: `backend/app/schemas/summary.py`
- Create: `backend/app/repositories/legal_term_repository.py`
- Create: `backend/app/services/legal_term_service.py`
- Create: `backend/app/services/summary_service.py`
- Create: `backend/app/api/routes/legal_terms.py`
- Modify: `backend/app/api/routes/cases.py`
- Modify: `backend/app/main.py`
- Test: `backend/tests/unit/test_legal_term_service.py`
- Test: `backend/tests/unit/test_summary_service.py`
- Test: `backend/tests/integration/test_legal_terms_api.py`

**Interfaces:**
- Produces: `LegalTermService.get_term(term: str) -> dict | None`
- Produces: `LegalTermService.extract_terms(case_id: str) -> list[dict]`
- Produces: `SummaryService.summarize(case_id: str, force_regenerate: bool = False) -> dict`
- Produces: `GET /api/legal-terms/{term}`
- Produces: `GET /api/cases/{case_id}/legal-terms`
- Produces: `POST /api/cases/{case_id}/summary`

- [ ] **Step 1: Write legal term test**

```python
from app.services.legal_term_service import LegalTermService


def test_get_known_legal_term_has_easy_definition():
    result = LegalTermService().get_term("기각")

    assert result["term"] == "기각"
    assert "받아들이지" in result["easy_definition"]
    assert result["source"] == "MVP built-in glossary"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd backend; pytest tests/unit/test_legal_term_service.py -v`

Expected: FAIL because service does not exist.

- [ ] **Step 3: Implement built-in glossary**

Include at least: `원고`, `피고`, `기각`, `각하`, `인용`, `항소`, `상고`, `소멸시효`, `입증 책임`, `불법행위`, `채무불이행`, `손해배상`, `지연손해금`, `계약 해제`, `부당이득`, `하자담보책임`.

- [ ] **Step 4: Implement rule-based summary**

Summary may extract existing sections and sentences only. It must not add new facts. Unknown fields return empty string or empty list.

- [ ] **Step 5: Add APIs**

Legal term missing returns `CASE_NOT_FOUND` only for missing case and `INVALID_REQUEST` for unknown term.

- [ ] **Step 6: Run tests**

Run: `cd backend; pytest tests/unit/test_legal_term_service.py tests/unit/test_summary_service.py tests/integration/test_legal_terms_api.py -v`

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add backend
git commit -m "feat: add legal terms and rule-based summaries"
```

---

### Task 7: Rule-Based Simplification and Validation

**Files:**
- Create: `backend/app/schemas/simplification.py`
- Create: `backend/app/validators/legal_text_validator.py`
- Create: `backend/app/services/simplification_service.py`
- Modify: `backend/app/api/routes/cases.py`
- Test: `backend/tests/unit/test_legal_text_validator.py`
- Test: `backend/tests/unit/test_simplification_service.py`
- Test: `backend/tests/integration/test_simplification_api.py`

**Interfaces:**
- Produces: `LegalTextValidator.extract_protected_values(text: str) -> ProtectedValues`
- Produces: `LegalTextValidator.validate(original: str, simplified: str) -> ValidationResult`
- Produces: `SimplificationService.simplify_case(case_id: str, section_types: list[str] | None, force_regenerate: bool) -> dict`
- Produces: `POST /api/cases/{case_id}/simplify`
- Produces: `GET /api/cases/{case_id}/simplified`
- Produces: `POST /api/cases/{case_id}/paragraphs/{paragraph_id}/simplify`

- [ ] **Step 1: Write validation tests**

```python
from app.validators.legal_text_validator import LegalTextValidator


def test_validator_detects_changed_amount():
    validator = LegalTextValidator()
    result = validator.validate(
        "피고는 원고에게 5,000,000원을 지급하라.",
        "피고는 원고에게 3,000,000원을 지급해야 합니다.",
    )

    assert result.status == "review_required"
    assert "금액" in result.warnings[0]


def test_validator_passes_preserved_date_and_rate():
    validator = LegalTextValidator()
    result = validator.validate(
        "2025년 3월 1일부터 연 12%의 비율로 계산한 돈을 지급하라.",
        "2025년 3월 1일부터 연 12%의 지연이자를 지급해야 합니다.",
    )

    assert result.status == "passed"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd backend; pytest tests/unit/test_legal_text_validator.py -v`

Expected: FAIL because validator does not exist.

- [ ] **Step 3: Implement extraction regexes**

Extract:

- amounts: `\d{1,3}(,\d{3})*원`, `\d+만 원`
- dates: `\d{4}년 \d{1,2}월 \d{1,2}일`, `\d{4}-\d{2}-\d{2}`
- rates: `연 \d+%`, `\d+%`
- case numbers: Korean court case-number-like text only from stored samples
- legal articles: `제\d+조`
- parties: `원고`, `피고`
- result terms: `기각`, `각하`, `인용`, `지급하라`, `반환하라`

- [ ] **Step 4: Implement rule-based simplifier**

Replacement examples:

- `지급하라` -> `지급해야 합니다`
- `이에 대하여` -> `이 금액에 대해`
- `다 갚는 날까지` -> `실제로 모두 갚는 날까지`
- `연 12%의 비율로 계산한 돈` -> `연 12%의 지연이자`

If validation fails, return simplified text with `validation_status="review_required"` and warnings.

- [ ] **Step 5: Add APIs**

APIs operate only on stored paragraphs. They do not call external LLMs.

- [ ] **Step 6: Run tests**

Run: `cd backend; pytest tests/unit/test_legal_text_validator.py tests/unit/test_simplification_service.py tests/integration/test_simplification_api.py -v`

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add backend
git commit -m "feat: add free rule-based simplification validation"
```

---

### Task 8: Documentation, Full Integration Tests, Runbook

**Files:**
- Create: `backend/docs/api-spec.md`
- Create: `backend/docs/frontend-integration.md`
- Create: `backend/docs/data-source-policy.md`
- Create: `backend/docs/ai-validation-policy.md`
- Create: `backend/README.md`
- Test: `backend/tests/integration/test_full_flow.py`
- Test: `backend/tests/integration/test_cors.py`

**Interfaces:**
- Documents exact endpoint list, request examples, success examples, failure examples, error codes, TypeScript types, and free-only runtime constraints.

- [ ] **Step 1: Write full flow test**

```python
from fastapi.testclient import TestClient

from app.main import create_app


def test_full_flow_analyze_search_detail_simplify():
    client = TestClient(create_app())

    analyze = client.post("/api/cases/analyze", json={"query": "중고 노트북 하자 환불 거부"})
    assert analyze.status_code == 200

    search = client.post("/api/cases/search", json={"query": "중고 노트북 하자 환불", "page": 1, "size": 10})
    assert search.status_code == 200
    case_id = search.json()["data"]["results"][0]["case_id"]

    detail = client.get(f"/api/cases/{case_id}")
    assert detail.status_code == 200
    assert detail.json()["data"]["case_id"] == case_id

    simplified = client.post(f"/api/cases/{case_id}/simplify", json={"section_types": ["주문"], "force_regenerate": False})
    assert simplified.status_code == 200
    assert simplified.json()["data"]["case_id"] == case_id
```

- [ ] **Step 2: Run full test to verify current gaps**

Run: `cd backend; pytest tests/integration/test_full_flow.py -v`

Expected: PASS after Tasks 1-7 are complete.

- [ ] **Step 3: Write API spec docs**

Document every endpoint with method, path, request, response, error codes, and authentication status. State that authentication is not required for MVP.

- [ ] **Step 4: Write frontend integration docs**

Include TypeScript interfaces matching `snake_case` JSON fields. Include CORS setup and sample fetch calls.

- [ ] **Step 5: Write data source policy**

State that MVP uses `MVP sample data`, does not crawl, and does not activate official APIs until legal and usage conditions are verified.

- [ ] **Step 6: Write AI validation policy**

State that MVP uses no paid external LLM. Explain rule-based simplification and validation warnings.

- [ ] **Step 7: Write README**

Include:

```text
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
pytest -v
```

- [ ] **Step 8: Run full verification**

Run: `cd backend; pytest -v`

Expected: PASS.

- [ ] **Step 9: Commit**

```bash
git add backend
git commit -m "docs: add frontend integration and free runtime guide"
```

---

## Self-Review

Spec coverage:

- Free-only runtime is covered by Global Constraints and Tasks 1, 5, 7, 8.
- Sample data loading is covered by Task 2.
- Case analysis is covered by Task 4.
- Search and similar cases are covered by Task 5.
- Detail lookup and paragraph splitting are covered by Task 3.
- Simplification and validation are covered by Task 7.
- Legal terms and summary are covered by Task 6.
- CORS, Swagger, OpenAPI, and docs are covered by Tasks 1 and 8.
- Tests are included in every task.

Placeholder scan:

- No `TBD` or `TODO` markers are present.
- No paid provider is required.
- Official case APIs are documentation-only and not active code.

Type consistency:

- Route names, service names, and return concepts are consistent across tasks.
- JSON response shape remains `success`, `data`, `error`.
- API fields remain `snake_case`.
