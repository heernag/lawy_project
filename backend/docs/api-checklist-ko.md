# API 체크리스트

작성일: 2026-07-15

이 문서는 현재 백엔드 API가 원래 MVP 요구사항을 얼마나 만족하는지 확인하기 위한
한국어 체크리스트입니다.

## 상태 표시

- 완료: 현재 구현과 테스트가 존재함
- 부분 완료: 기본 구현은 있으나 문서/테스트/운영 검증이 더 필요함
- 남음: 아직 별도 작업 필요

## 공통

| 항목 | 상태 | 확인 내용 |
| --- | --- | --- |
| 공통 성공 응답 | 완료 | `success`, `data`, `error` 형식 사용 |
| 공통 실패 응답 | 완료 | `success: false`, `error.code`, `error.message` 사용 |
| 요청 검증 오류 통일 | 완료 | `INVALID_REQUEST`로 반환 |
| 운영 환경 검증 상세 숨김 | 완료 | production-like 환경에서 `details: null` |
| 에러 코드 상수 관리 | 완료 | `app.core.errors`, `ALL_ERROR_CODES` |
| CORS 설정 | 완료 | `CORS_ORIGINS` 환경변수 기반 |
| Swagger/OpenAPI | 완료 | FastAPI 기본 `/docs`, `/openapi.json` |

## 엔드포인트 체크리스트

### `GET /api/health`

상태: 완료

확인 내용:

- 서버 상태 반환
- 판결문 공급자 조회 가능 여부 확인
- 샘플 데이터 로드 여부 확인
- 공급자 오류 시 내부 예외를 노출하지 않음
- 진단 로직은 `HealthService`로 분리됨

### `POST /api/cases/analyze`

상태: 완료

확인 내용:

- 자연어 사건 문장 분석
- 사건 분야/유형 반환
- 당사자, 분쟁 대상, 사실관계, 법적 쟁점, 검색 키워드 반환
- 개인정보 탐지 결과 반환
- `sanitized_query` 반환
- 프롬프트 인젝션 의심 문구는 경고로만 반환
- 입력 길이 제한 적용

남은 보강:

- 실제 사용자 예시를 더 많이 추가해 분류 규칙 보강

### `POST /api/cases/search`

상태: 완료

확인 내용:

- 사건번호 정확 검색
- 키워드 검색
- 카테고리 필터
- 법원명 필터 구조
- 판결 결과 필터 구조
- 선고일 필터
- 페이지네이션
- 검색어 정규화
- 저장된 검색 인덱스 사용
- 무료 로컬 해시 임베딩 유사도 구현 완료

주의:

- 해시 임베딩은 검색 관련도 보조용이며 법률 의미 판단용이 아님

남은 보강:

- 공식 판결문 데이터 연동 전 데이터 출처 조건 확인
- 더 많은 샘플 판결문 기반 검색 품질 테스트

### `GET /api/cases/{case_id}`

상태: 완료

확인 내용:

- 저장된 판결문 상세 조회
- 존재하지 않는 판결문은 `CASE_NOT_FOUND`
- 원문, 출처, 사건 메타데이터 반환
- 존재하지 않는 판결문을 생성하지 않음

### `GET /api/cases/{case_id}/sections`

상태: 완료

확인 내용:

- 섹션 목록 반환
- 문단 목록 반환
- 안정적인 `section_id`, `paragraph_id` 반환
- 주문, 청구 취지, 이유, 인정 사실, 주장, 판단, 결론, 관련 법령 인식
- 번호가 붙은 제목 인식
- 항소/상고 관련 제목 인식

남은 보강:

- 실제 공개 판결문 형식 fixture 추가

### `POST /api/cases/{case_id}/summary`

상태: 완료

확인 내용:

- 판결문 요약 생성
- 이미 생성된 요약 재사용
- `force_regenerate` 지원
- 존재하지 않는 판결문은 `CASE_NOT_FOUND`

### `POST /api/cases/{case_id}/simplify`

상태: 완료

확인 내용:

- 판결문 문단별 쉬운 설명 생성
- 특정 섹션 타입만 처리 가능
- 기존 생성 결과 재사용
- 검증 상태와 경고 반환
- 존재하지 않는 판결문은 `CASE_NOT_FOUND`

### `GET /api/cases/{case_id}/simplified`

상태: 완료

확인 내용:

- 생성된 쉬운 설명 조회
- 저장된 결과 재사용
- 원문 문단과 쉬운 설명 연결

### `POST /api/cases/{case_id}/paragraphs/{paragraph_id}/simplify`

상태: 완료

확인 내용:

- 특정 문단만 다시 변환
- 전체 판결문을 다시 처리하지 않음
- 존재하지 않는 판결문 또는 문단은 오류 반환

### `GET /api/legal-terms/{term}`

상태: 완료

확인 내용:

- 법률 용어 일반 정의 반환
- 예시와 주의사항 반환

주의:

- 현재 없는 용어는 `INVALID_REQUEST`로 반환 중
- 추후 에러 코드를 더 엄밀히 하려면 `LEGAL_TERM_NOT_FOUND` 또는
  `CASE_NOT_FOUND`와 다른 전용 코드 검토 가능

### `GET /api/cases/{case_id}/legal-terms`

상태: 완료

확인 내용:

- 판결문 내 법률 용어 추출
- 문단 ID와 연결
- 추출 결과 저장 및 재사용

### `GET /api/cases/{case_id}/similar`

상태: 완료

확인 내용:

- 현재 판결문과 유사한 저장 판결문 조회
- 자기 자신은 결과에서 제외
- 유사도 점수는 판결 결과 예측이 아님

## 문서 체크리스트

| 문서 | 상태 | 파일 |
| --- | --- | --- |
| API 명세 | 부분 완료 | `backend/docs/api-spec.md` |
| 프론트 연동 가이드 | 부분 완료 | `backend/docs/frontend-integration.md` |
| 데이터 출처 정책 | 완료 | `backend/docs/data-source-policy.md` |
| AI 검증 정책 | 완료 | `backend/docs/ai-validation-policy.md` |
| 코드리뷰 노트 | 완료 | `backend/docs/code-review-notes.md` |
| 진행 현황 요약 | 완료 | `backend/docs/progress-summary-ko.md` |
| 작업 로그 | 완료 | `backend/docs/work-log-ko.md` |
| API 체크리스트 | 완료 | `backend/docs/api-checklist-ko.md` |
| 프론트 화면 흐름 가이드 | 완료 | `backend/docs/frontend-flow-ko.md` |
| Postman 또는 Bruno 파일 | 완료 | `backend/bruno` |
| README 실행 검증 | 완료 | `python -m pytest -v`, 앱 생성 확인 |

## 테스트 체크리스트

| 영역 | 상태 |
| --- | --- |
| 자연어 사건 분석 | 완료 |
| 개인정보 마스킹 | 완료 |
| 검색어 검증 | 완료 |
| 사건번호 검색 | 완료 |
| 필터 검색 | 완료 |
| 날짜 필터 | 완료 |
| 문단 분리 | 완료 |
| 쉬운 설명 생성 | 완료 |
| 검증 실패 탐지 | 완료 |
| 법률 용어 조회 | 완료 |
| 유사 판결문 조회 | 완료 |
| 헬스 체크 | 완료 |
| CORS | 완료 |
| 잘못된 요청 처리 | 완료 |
| 전체 사용자 흐름 | 완료 |

현재 확인된 테스트:

```text
85 passed, 1 warning
```

## 남은 작업량

현재 백엔드 MVP는 약 95% 완료입니다.

남은 작업은 약 5%입니다.

## 다음 우선순위

1. 최종 체크리스트 갱신 커밋
2. 필요 시 완전히 새 환경에서 의존성 설치부터 재검증
