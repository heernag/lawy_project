# MVP 최종 점검표

작성일: 2026-07-15

이 문서는 원래 요청한 백엔드 MVP 완료 조건을 기준으로 현재 상태를 점검한
문서입니다.

## 현재 결론

현재 백엔드 MVP는 기능 기준으로 대부분 구현되어 있고, 이전에 남아 있던
미커밋 작업도 장 단위로 커밋되었습니다.

현재 추정:

- 완료율: 약 95%
- 남은 작업: 약 5%

## 검증 결과

최근 확인한 테스트:

```text
python -m pytest -q
93 passed, 1 warning
```

README 기준 실행 검증:

```text
python -m pytest -v
85 passed, 1 warning
```

앱 생성 확인:

```text
Easy Case Law Backend
```

## 완료 조건별 점검

| 완료 조건 | 상태 | 근거 |
| --- | --- | --- |
| FastAPI 서버 구조 | 완료 | `app/main.py`, README 실행 방법 |
| Swagger 확인 | 완료 | FastAPI `/docs`, OpenAPI 계약 테스트 |
| OpenAPI JSON 확인 | 완료 | FastAPI `/openapi.json`, 핵심 경로/공통 응답 스키마 테스트 |
| 사건 문장 분석 | 완료 | `POST /api/cases/analyze`, 테스트 존재 |
| 개인정보 탐지/마스킹 | 완료 | 전화번호, 주민등록번호 형식, 이메일, 도로명 주소, 주소 오탐 방지 fixture |
| 실제 저장 판결문만 검색 | 완료 | 샘플/DB provider 기반 |
| 사건번호 검색 | 완료 | 사건번호 정확 검색 테스트 |
| 키워드 검색 | 완료 | 로컬 검색 테스트 |
| 벡터 유사도 검색 | 완료 | 무료 로컬 해시 임베딩 구현 및 커밋 |
| 판결문 상세 원문 반환 | 완료 | `GET /api/cases/{case_id}` |
| 문단 단위 반환 | 완료 | `GET /api/cases/{case_id}/sections`, 형사/행정 섹션 fixture |
| 쉬운 설명과 원문 문단 연결 | 완료 | paragraph ID 기반 |
| 금액/날짜/사건번호/판결 결과 검증 | 완료 | `legal_text_validator` 테스트 |
| 검증 실패 상태 반환 | 완료 | simplification validation 결과 |
| 법률 용어 설명 API | 완료 | `GET /api/legal-terms/{term}` |
| 존재하지 않는 판결문 생성 방지 | 완료 | missing case 테스트 |
| CORS 설정 | 완료 | CORS integration test |
| `.env` Git 제외 | 완료 | `.env.example`만 제공 |
| 프론트 연동 문서 | 완료 | `frontend-integration.md`, `frontend-flow-ko.md`, TypeScript 계약 예시 테스트 |
| Bruno 테스트 컬렉션 | 완료 | `backend/bruno` |
| README 실행 가이드 | 완료 | README 갱신 및 테스트 명령 검증 |
| 모든 변경 커밋 | 완료 | 최근 작업은 장 단위 커밋으로 정리됨 |

## 커밋 완료 내역

이전에 남아 있던 미커밋 작업은 아래 커밋으로 정리되었습니다.

- `a56ed3d feat: add free local hash embeddings`
- `4cabfd2 docs: verify README local setup`
- `1aa029f docs: add frontend handoff checklist`
- `4641046 docs: update final MVP checklist`
- `759ee3a docs: expand official data source review policy`
- `23c1cf4 test: add address masking false positive fixtures`
- `docs: refresh korean progress notes`
- `test: add judgment section heading fixtures`
- `docs: lock frontend TypeScript contract examples`
- `test: add OpenAPI contract checks`

커밋 전 전체 테스트도 다시 통과했습니다.

## 남은 필수 작업

1. 필요하면 완전히 새 환경에서 의존성 설치부터 재검증한다.

## 남은 선택 작업

아래는 무료 MVP 이후 또는 안정화 단계에서 해도 됩니다.

- 주소 마스킹 fixture 추가
- 실제 공개 판결문 형식 기반 섹션 분리 fixture 추가 보강
- OpenAPI 기반 TypeScript 타입 자동 생성 검토
- 공식 공공데이터 API 약관 확인 후 provider 추가
- Alembic 운영 마이그레이션 정리

## 최종 한 줄

현재 상태는 “무료 백엔드 MVP 기능은 거의 완료되었고, 남은 것은 선택적 새 환경
재검증과 안정화 fixture 보강”입니다.
