# 무료 전용 판결문 검색 및 쉬운 법률 설명 백엔드 설계

## 1. 목표

일반 사용자가 자신의 법적 분쟁 상황을 자연어로 입력하면, 저장된 공개 또는 샘플 판결문 중 유사한 판결문을 검색하고 판결문 원문을 쉬운 한국어로 설명해주는 FastAPI 백엔드 MVP를 만든다.

이 MVP는 무료 실행을 기본 원칙으로 한다. 외부 유료 LLM API, 유료 임베딩 API, 유료 벡터 DB, 유료 판결문 데이터 서비스로 자동 전환하지 않는다.

## 2. 무료 전용 원칙

- 기본 실행에 유료 API 키가 필요하지 않아야 한다.
- OpenRouter, OpenAI, Anthropic, Gemini 등 외부 유료 LLM Provider는 MVP 구현 범위에서 제외한다.
- 외부 유료 임베딩 API를 사용하지 않는다.
- 벡터 검색은 로컬에서 실행 가능한 방식으로 구현한다.
- 판결문 데이터는 우선 `SampleCaseProvider`와 샘플 JSON을 사용한다.
- 공식 판례 API는 향후 확장 지점으로만 문서화하고, 이용 조건 확인 전에는 자동 호출하지 않는다.
- API 키가 없을 때 유료 서비스로 fallback하는 코드를 작성하지 않는다.
- 운영 전환 문서에서도 유료 서비스 사용을 권장 기본값으로 두지 않는다.

## 3. MVP 기능 범위

포함 기능:

- FastAPI 서버
- CORS 설정
- 공통 API 응답 형식
- SQLite 저장소
- 샘플 판결문 데이터 로드
- 자연어 사건 분석
- 검색 키워드 추출
- 사건번호 정확 검색
- 키워드 검색
- 로컬 유사도 검색
- 판결문 상세 조회
- 판결문 섹션 및 문단 분리
- 문단별 쉬운 설명 생성
- 쉬운 설명 검증
- 법률 용어 설명
- Swagger 및 OpenAPI 문서
- 프론트엔드 연동 문서
- 단위 테스트와 통합 테스트

제외 기능:

- 프론트엔드 구현
- 회원가입, 결제, 관리자 페이지
- 승소 가능성 또는 패소 가능성 예측
- 법률 자문 자동 생성
- 소송 전략 자동 결정
- 비공개 판결문 접근
- 대규모 자동 크롤링
- 외부 유료 LLM/임베딩/검색 서비스 연동

## 4. 데이터 확보 방식

### 4.1 SampleCaseProvider

MVP의 기본 데이터 공급자다. `data/sample_cases.json`에 저장된 샘플 판결문만 읽는다.

장점:

- 무료로 개발 가능
- 테스트 결과가 안정적
- 출처가 불확실한 데이터 수집 위험이 낮음
- 실제 저장된 판결문만 반환하는 요구사항을 검증하기 쉬움

단점:

- 검색 품질을 대규모 데이터로 검증하기 어렵다
- 운영용 판례 데이터로 바로 사용할 수 없다

### 4.2 공식 공공 API 후보

국가법령정보 공동활용 Open API, 공공데이터포털 판례 관련 API, 대한민국 법원 공개 판결문 서비스를 후보로 둔다.

MVP에서는 자동 호출하지 않는다. 구현 전에 다음 조건을 사람이 확인해야 한다.

- API 제공 여부
- 인증 방식
- 호출 제한
- 데이터 저장 가능 여부
- 재배포 가능 여부
- 원문 표시 가능 여부
- 상업적 이용 가능 여부
- 출처 표시 조건

### 4.3 수동 반입 데이터

이용 조건이 확인된 공개 판결문 파일을 관리자가 직접 JSON 형식으로 반입하는 방식을 향후 옵션으로 둔다.

## 5. 검색 방식

### 5.1 사건번호 정확 검색

사용자가 사건번호를 입력하면 `case_number` 필드에서 정확 일치 또는 정규화 일치를 우선 적용한다.

장점:

- 가장 정확하다
- 설명 가능하다

단점:

- 사건번호를 모르면 사용할 수 없다

### 5.2 키워드 검색

제목, 본문, 요약, 쟁점, 법률 용어를 대상으로 간단한 한국어 키워드 매칭을 수행한다.

장점:

- 무료 구현이 쉽다
- 디버깅이 쉽다
- 검색 이유를 설명하기 쉽다

단점:

- 표현이 달라지면 누락될 수 있다
- 형태소 분석 없이 구현하면 품질이 제한된다

### 5.3 로컬 유사도 검색

MVP에서는 외부 유료 임베딩 API 대신 로컬 TF-IDF 기반 유사도 또는 로컬 오픈소스 임베딩 모델을 선택 가능하게 설계한다. 기본값은 설치 부담이 낮은 TF-IDF 방식으로 둔다.

장점:

- 무료로 동작한다
- API 키가 필요 없다
- 테스트가 재현 가능하다

단점:

- 고급 의미 검색 품질은 유료 대형 모델보다 낮을 수 있다
- 한국어 법률 문장에 특화된 품질 튜닝이 필요할 수 있다

## 6. 추천 아키텍처

FastAPI를 API 계층으로 두고, 비즈니스 로직은 서비스, DB 접근은 Repository, 외부 또는 데이터 공급 기능은 Provider로 분리한다.

주요 계층:

- `api`: HTTP 요청과 응답
- `schemas`: Pydantic 요청/응답 모델
- `models`: SQLAlchemy ORM 모델
- `repositories`: DB 저장과 조회
- `providers`: 판결문 공급자, 설명 생성기, 유사도 검색기
- `services`: 사건 분석, 검색, 상세 조회, 문단 분리, 쉬운 설명, 검증, 법률 용어 처리
- `validators`: 금액, 날짜, 사건번호, 당사자, 판결 결과 검증

무료 전용 Provider:

- `SampleCaseProvider`
- `RuleBasedCaseAnalysisProvider`
- `RuleBasedSimplificationProvider`
- `LocalSimilarityProvider`

## 7. 데이터베이스 모델

### CaseDocument

- `id`
- `external_id`
- `case_number`
- `case_name`
- `court_name`
- `court_department`
- `decision_date`
- `category`
- `judgment_result`
- `order_text`
- `original_text`
- `source_name`
- `source_url`
- `source_updated_at`
- `created_at`
- `updated_at`

### CaseSection

- `id`
- `case_id`
- `section_type`
- `section_order`
- `original_text`

### CaseParagraph

- `id`
- `section_id`
- `paragraph_order`
- `original_text`
- `simplified_text`
- `validation_status`
- `validation_warnings`
- `simplified_at`

### CaseSummary

- `id`
- `case_id`
- `one_line_summary`
- `background`
- `plaintiff_claim`
- `defendant_claim`
- `court_reasoning`
- `judgment_result`
- `created_at`

### LegalTerm

- `id`
- `term`
- `easy_definition`
- `example`
- `caution`
- `source`

### CaseLegalTerm

- `id`
- `case_id`
- `term_id`
- `context_meaning`
- `paragraph_id`

### CaseEmbedding

MVP에서는 실제 벡터 DB 대신 로컬 유사도 인덱스 참조를 저장한다.

- `case_id`
- `paragraph_id`
- `document_type`
- `embedding_reference`

## 8. API 초안

- `GET /api/health`
- `POST /api/cases/analyze`
- `POST /api/cases/search`
- `GET /api/cases/{case_id}`
- `GET /api/cases/{case_id}/sections`
- `POST /api/cases/{case_id}/summary`
- `POST /api/cases/{case_id}/simplify`
- `GET /api/cases/{case_id}/simplified`
- `POST /api/cases/{case_id}/paragraphs/{paragraph_id}/simplify`
- `GET /api/legal-terms/{term}`
- `GET /api/cases/{case_id}/legal-terms`
- `GET /api/cases/{case_id}/similar`

공통 성공 응답:

```json
{
  "success": true,
  "data": {},
  "error": null
}
```

공통 실패 응답:

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

## 9. 판결문 원문 처리 흐름

1. `SampleCaseProvider`가 샘플 JSON을 읽는다.
2. 필수 메타데이터를 검증한다.
3. 판결문을 SQLite에 저장한다.
4. 원문을 정규화한다.
5. 주문, 청구 취지, 이유, 인정 사실, 법원의 판단, 결론 등 섹션을 탐지한다.
6. 섹션 내부 문단을 순서대로 분리한다.
7. 검색용 텍스트를 만든다.
8. 로컬 유사도 검색 인덱스를 갱신한다.

섹션 탐지가 실패하면 원문을 임의로 해석하지 않고 `원문` 섹션으로 보존한다.

## 10. 쉬운 설명 생성 흐름

MVP에서는 외부 LLM을 사용하지 않는다. 규칙 기반 쉬운 설명 생성기를 사용한다.

1. 문단 원문 조회
2. 사건번호, 날짜, 금액, 비율, 법률 조항, 당사자 표현 추출
3. 보호 토큰 생성
4. 법률 표현을 쉬운 표현으로 치환
5. 보호 토큰 복원
6. 검증 서비스 실행
7. 통과 시 `passed`
8. 위험이 있으면 `review_required`

규칙 기반 생성기가 처리하기 어려운 문단은 무리하게 의역하지 않고 검토 필요 상태로 반환한다.

## 11. 생성 결과 검증

검증은 룰 기반으로 수행한다.

- 사건번호 일치
- 날짜 일치
- 금액 일치
- 비율 및 이자율 일치
- 법률 조항 번호 일치
- 원고와 피고 역할 일치
- 주문 내용 일치
- 승소, 패소, 기각, 각하, 인용 표현 보존
- 부정 표현 보존
- 법적 의무 주체 보존
- 원문에 없는 핵심 사실 추가 여부
- 원문 핵심 내용 삭제 여부

검증 실패 시 `validation_status`는 `review_required`로 반환하고, 정확한 변환처럼 표시하지 않는다.

## 12. 프론트엔드 연동

- Swagger: `/docs`
- OpenAPI JSON: `/openapi.json`
- 응답 필드: `snake_case`
- CORS 허용 주소: `CORS_ORIGINS`
- 개인정보 주의 문구 제공
- 법률 자문이 아니라는 안내 문구 제공
- TypeScript 타입 예시 제공
- Bruno 또는 Postman 테스트 파일 제공

## 13. 예상 폴더 구조

```text
backend/
├─ app/
│  ├─ api/
│  ├─ core/
│  ├─ db/
│  ├─ models/
│  ├─ schemas/
│  ├─ repositories/
│  ├─ providers/
│  ├─ services/
│  ├─ validators/
│  ├─ prompts/
│  └─ main.py
├─ data/
│  └─ sample_cases.json
├─ tests/
│  ├─ unit/
│  └─ integration/
├─ docs/
│  ├─ api-spec.md
│  ├─ frontend-integration.md
│  ├─ data-source-policy.md
│  └─ ai-validation-policy.md
├─ requirements.txt
├─ .env.example
├─ .gitignore
└─ README.md
```

## 14. 테스트 계획

단위 테스트:

- 자연어 사건 분석
- 사건 분야 분류
- 검색 키워드 추출
- 사건번호 검색
- 키워드 검색
- 로컬 유사도 계산
- 문단 분리
- 숫자, 날짜, 금액, 비율, 법률 조항 추출
- 쉬운 설명 검증
- 법률 용어 조회

통합 테스트:

- 사건 분석부터 검색까지
- 검색부터 상세 조회까지
- 상세 조회부터 문단 분리까지
- 쉬운 설명 생성과 검증까지
- 존재하지 않는 사건 조회
- 잘못된 입력 처리
- CORS 동작
- 페이지네이션

반드시 테스트할 검증 사례:

- 금액이 달라지는 경우
- 날짜가 달라지는 경우
- 원고와 피고가 바뀌는 경우
- 기각이 인용으로 바뀌는 경우
- 지급 의무 주체가 바뀌는 경우
- 원문에 없는 사실이 추가되는 경우
- 부정 표현이 사라지는 경우

## 15. 구현 순서

1. 프로젝트 기본 구조 생성
2. 설정, CORS, 공통 응답, 에러 코드 작성
3. SQLite DB 연결
4. SQLAlchemy 모델 작성
5. 샘플 판결문 JSON 작성
6. 샘플 데이터 로더 작성
7. Repository 작성
8. 문단 분리 서비스 작성
9. 사건 분석 서비스 작성
10. 검색 서비스 작성
11. 로컬 유사도 검색 작성
12. 상세 조회 API 작성
13. 법률 용어 API 작성
14. 규칙 기반 쉬운 설명 생성 작성
15. 검증 서비스 작성
16. 요약 API 작성
17. 테스트 작성
18. 문서 작성
19. 실행 확인

## 16. 승인 기준

이 설계가 승인되면 다음 단계에서 구현 계획을 작성한다. 구현 계획 승인 후에만 실제 백엔드 코드를 작성한다.
