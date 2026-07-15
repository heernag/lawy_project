# MVP 최종 점검표

작성일: 2026-07-15

이 문서는 원래 요청한 백엔드 MVP 완료 조건을 기준으로 현재 상태를 점검한
문서입니다.

## 현재 결론

현재 백엔드 MVP는 기능 기준으로 대부분 구현되어 있습니다.

다만 Git 커밋이 막힌 미커밋 작업이 남아 있어 최종 완료로 보기는 어렵습니다.

현재 추정:

- 완료율: 약 85%
- 남은 작업: 약 15%

## 검증 결과

최근 확인한 테스트:

```text
python -m pytest -q
85 passed, 1 warning
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
| Swagger 확인 | 완료 | FastAPI `/docs` |
| OpenAPI JSON 확인 | 완료 | FastAPI `/openapi.json` |
| 사건 문장 분석 | 완료 | `POST /api/cases/analyze`, 테스트 존재 |
| 개인정보 탐지/마스킹 | 완료 | 전화번호, 주민등록번호 형식, 이메일, 도로명 주소 |
| 실제 저장 판결문만 검색 | 완료 | 샘플/DB provider 기반 |
| 사건번호 검색 | 완료 | 사건번호 정확 검색 테스트 |
| 키워드 검색 | 완료 | 로컬 검색 테스트 |
| 벡터 유사도 검색 | 부분 완료 | 무료 로컬 해시 임베딩 구현, 아직 미커밋 |
| 판결문 상세 원문 반환 | 완료 | `GET /api/cases/{case_id}` |
| 문단 단위 반환 | 완료 | `GET /api/cases/{case_id}/sections` |
| 쉬운 설명과 원문 문단 연결 | 완료 | paragraph ID 기반 |
| 금액/날짜/사건번호/판결 결과 검증 | 완료 | `legal_text_validator` 테스트 |
| 검증 실패 상태 반환 | 완료 | simplification validation 결과 |
| 법률 용어 설명 API | 완료 | `GET /api/legal-terms/{term}` |
| 존재하지 않는 판결문 생성 방지 | 완료 | missing case 테스트 |
| CORS 설정 | 완료 | CORS integration test |
| `.env` Git 제외 | 완료 | `.env.example`만 제공 |
| 프론트 연동 문서 | 완료 | `frontend-integration.md`, `frontend-flow-ko.md` |
| Bruno 테스트 컬렉션 | 완료 | `backend/bruno` |
| README 실행 가이드 | 완료 | README 갱신 및 테스트 명령 검증 |
| 모든 변경 커밋 | 남음 | Git write approval 제한으로 미커밋 |

## 아직 완료로 표시하지 않는 이유

아래 작업이 아직 커밋되지 않았습니다.

- 무료 로컬 해시 임베딩 provider
- 로컬 유사도 검색 변경
- 관련 테스트
- Bruno 컬렉션
- 한국어 진행 문서들
- README 및 `.env.example` 업데이트

따라서 기능과 테스트는 통과하지만, Git 기준으로는 아직 완료 상태가 아닙니다.

## 남은 필수 작업

1. Git 사용 가능 시 현재 미커밋 변경을 스테이징한다.
2. 장 단위로 커밋한다.
3. 커밋 후 전체 테스트를 다시 실행한다.
4. 이 최종 점검표의 Git 상태를 완료로 갱신한다.

## 남은 선택 작업

아래는 무료 MVP 이후 또는 안정화 단계에서 해도 됩니다.

- 주소 마스킹 fixture 추가
- 실제 공개 판결문 형식 기반 섹션 분리 fixture 추가
- OpenAPI 기반 TypeScript 타입 자동 생성 검토
- 공식 공공데이터 API 약관 확인 후 provider 추가
- Alembic 운영 마이그레이션 정리

## 최종 한 줄

현재 상태는 “기능 검증은 통과했지만, 미커밋 작업 때문에 최종 완료 전 단계”입니다.
