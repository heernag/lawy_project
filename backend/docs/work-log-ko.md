# 작업 로그

작성일: 2026-07-15

이 문서는 앞으로 작업할 때마다 무엇을 했는지 한국어로 남기는 기록입니다.

## 현재 원칙

- 유료 API로 넘기지 않는다.
- 판결문, 사건번호, 법률 조항, 출처를 지어내지 않는다.
- 구현 또는 문서 변경 후 가능한 검증을 실행한다.
- 작업 단위마다 이 문서 또는 관련 진행 문서를 업데이트한다.
- Git 커밋은 가능할 때마다 장 단위로 남긴다.

## 2026-07-15 작업 기록

### 1. 한국어 진행 현황 문서 작성

생성한 문서:

- `backend/docs/progress-summary-ko.md`

작업 내용:

- 지금까지 완료한 백엔드 기능을 한국어로 정리했다.
- 남은 작업량을 백엔드 MVP 기준 약 25%로 정리했다.
- 무료 버전 원칙을 다시 명시했다.
- 아직 커밋되지 않은 무료 로컬 해시 임베딩 검색 작업을 별도로 표시했다.

현재 확인한 테스트 상태:

```text
python -m pytest -q
84 passed, 1 warning
```

주의:

- `무료 로컬 해시 임베딩 검색` 작업과 이 진행 문서들은 아직 Git 커밋 전이다.
- 이전 Git 스테이징 시도는 Codex 사용량 제한 때문에 막혔다.

### 2. API 체크리스트 작성

생성한 문서:

- `backend/docs/api-checklist-ko.md`

작업 내용:

- 현재 실제 FastAPI 라우트 기준으로 API 목록을 정리했다.
- 각 API를 `완료`, `부분 완료`, `남음` 상태로 표시했다.
- 검색, 상세 조회, 문단 분리, 요약, 쉬운 설명, 법률 용어, 유사 판결문,
  헬스 체크의 구현 상태를 확인했다.
- Postman 또는 Bruno 테스트 파일이 아직 남은 작업임을 표시했다.
- 남은 작업량을 백엔드 MVP 기준 약 25%로 다시 정리했다.

### 3. Bruno 테스트 컬렉션 작성

생성한 위치:

- `backend/bruno`

작업 내용:

- 로컬 환경 변수 `base_url`, `case_id`, `paragraph_id`를 추가했다.
- 헬스 체크, 사건 분석, 판결문 검색, 상세 조회, 섹션 조회, 요약, 쉬운 설명,
  문단 하나 다시 변환, 법률 용어, 판결문 내 법률 용어, 유사 판결문 요청을
  Bruno 파일로 만들었다.
- 잘못된 검색 요청 예시도 추가해 `INVALID_REQUEST` 응답을 확인할 수 있게 했다.
- 프론트 연동 문서와 API 체크리스트에 Bruno 컬렉션 위치를 반영했다.

### 4. 프론트 화면 흐름 가이드 작성

생성한 문서:

- `backend/docs/frontend-flow-ko.md`

작업 내용:

- 프론트 화면별 추천 API 호출 순서를 정리했다.
- 사건 입력, 분석, 검색, 상세 조회, 문단 조회, 요약, 쉬운 설명, 법률 용어,
  유사 판결문 조회 흐름을 문서화했다.
- `similarity_score`를 승소 가능성처럼 보여주면 안 된다는 주의사항을 적었다.
- `validation_status`가 통과하지 않은 쉬운 설명은 검토 필요 상태로 보여야 한다는
  주의사항을 적었다.
- 프론트 연동 문서와 API 체크리스트에 새 가이드 위치를 반영했다.

### 5. README 기준 실행 검증

수정한 파일:

- `backend/README.md`
- `backend/.env.example`
- `backend/app/core/config.py`

작업 내용:

- README에 Bruno 컬렉션 위치와 프론트 화면 흐름 가이드 위치를 추가했다.
- 검색 방식 설명을 무료 로컬 해시 임베딩 기준으로 갱신했다.
- `SIMILARITY_MODE` 기본값을 `local_tfidf`에서 `local_hash`로 정리했다.
- 설정 기본값이 `local_hash`인지 확인하는 단위 테스트를 추가했다.

검증:

```text
python -m pytest -v
85 passed, 1 warning
```

앱 생성 확인:

```text
Easy Case Law Backend
```

### 6. MVP 최종 점검표 작성

생성한 문서:

- `backend/docs/mvp-final-check-ko.md`

작업 내용:

- 원래 MVP 완료 조건을 기준으로 현재 상태를 점검했다.
- 기능과 테스트는 대부분 통과했지만, Git 미커밋 작업 때문에 최종 완료로 보지
  않는다고 명시했다.
- 완료, 부분 완료, 남음 상태를 완료 조건별로 정리했다.
- 남은 필수 작업을 `미커밋 변경 스테이징`, `장 단위 커밋`, `커밋 후 전체 테스트`
  로 정리했다.

### 7. 미커밋 작업 커밋 완료

생성된 커밋:

- `a56ed3d feat: add free local hash embeddings`
- `4cabfd2 docs: verify README local setup`
- `1aa029f docs: add frontend handoff checklist`

작업 내용:

- 무료 로컬 해시 임베딩 검색 기능을 별도 커밋으로 정리했다.
- README 실행 검증과 `local_hash` 설정 변경을 별도 커밋으로 정리했다.
- Bruno 컬렉션, 프론트 흐름 가이드, API 체크리스트, MVP 최종 점검표를 문서 커밋으로
  정리했다.
- 커밋 후 전체 테스트를 다시 실행했다.

검증:

```text
python -m pytest -q
85 passed, 1 warning
```

### 8. 공식 판결문 데이터 출처 후보 점검표 보강

수정한 문서:

- `backend/docs/data-source-policy.md`

작업 내용:

- 국가법령정보 공동활용의 판례 목록/본문 조회 후보를 문서에 추가했다.
- 대한민국 법원 판결서 열람 페이지는 자동 크롤링 대상이 아니라 약관 확인 대상임을
  명시했다.
- 저장, 재배포, 원문 표시, 상업적 이용, 출처 표시 조건을 확인하기 전에는 실제
  provider를 구현하지 않는다고 적었다.
- 미래 구현도 `CaseProvider` 인터페이스 뒤에 붙여야 한다고 정리했다.

## 현재 미커밋 작업

- `backend/docs/api-checklist-ko.md`
- `backend/docs/data-source-policy.md`
- `backend/docs/mvp-final-check-ko.md`
- `backend/docs/progress-summary-ko.md`
- `backend/docs/work-log-ko.md`

## 다음에 이어서 할 작업

1. 최종 점검표 갱신 문서를 커밋한다.
2. 필요 시 완전히 새 환경에서 의존성 설치부터 재검증한다.
