# 프론트엔드 연동 흐름 가이드

작성일: 2026-07-15

이 문서는 프론트엔드 팀이 백엔드 API를 어떤 순서로 호출하면 되는지 정리한
한국어 연동 가이드입니다.

## 기본 서버 정보

로컬 백엔드 주소:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

OpenAPI JSON:

```text
http://localhost:8000/openapi.json
```

Bruno 테스트 컬렉션:

```text
backend/bruno
```

## 공통 응답 처리

모든 성공 응답은 다음 구조입니다.

```json
{
  "success": true,
  "data": {},
  "error": null
}
```

모든 실패 응답은 다음 구조입니다.

```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "INVALID_REQUEST",
    "message": "요청이 올바르지 않습니다.",
    "details": null
  }
}
```

프론트에서는 `error.message`보다 `error.code`를 기준으로 화면 상태를 나누는 것이
안전합니다.

## 권장 화면 흐름

### 1. 서버 상태 확인

앱 진입 또는 개발 환경 확인 시 호출합니다.

```http
GET /api/health
```

프론트에서 확인할 값:

- `data.status`
- `data.checks.case_provider`
- `data.checks.sample_data_loaded`

`sample_data_loaded`가 `false`이면 검색 화면에서 샘플 데이터가 준비되지 않았다는
안내를 보여주는 것이 좋습니다.

### 2. 사용자 사건 문장 분석

사용자가 자연어로 사건 내용을 입력하고 분석 버튼을 누르면 호출합니다.

```http
POST /api/cases/analyze
```

요청 예시:

```json
{
  "query": "중고 노트북을 구매했는데 제품이 고장 났고 판매자가 환불을 거부합니다."
}
```

프론트에서 사용할 주요 값:

- `data.category`
- `data.sub_category`
- `data.facts`
- `data.legal_issues`
- `data.search_keywords`
- `data.sanitized_query`
- `data.privacy_detections`
- `data.input_warnings`

주의:

- `sanitized_query`는 개인정보가 마스킹된 미리보기용입니다.
- `input_warnings`는 법률 판단이 아니라 입력 주의 문구로 보여줘야 합니다.

### 3. 판결문 검색

분석 결과의 `search_keywords` 또는 사용자가 직접 입력한 검색어로 호출합니다.

```http
POST /api/cases/search
```

요청 예시:

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

프론트에서 사용할 주요 값:

- `data.total_count`
- `data.page`
- `data.size`
- `data.results`
- `data.extracted_keywords`

검색 결과 카드에 표시하기 좋은 값:

- `case_name`
- `case_number`
- `court_name`
- `decision_date`
- `category`
- `judgment_result`
- `summary`
- `main_issues`
- `similarity_score`
- `similarity_reason`
- `source_name`

주의:

- `similarity_score`는 검색 관련도 점수입니다.
- 승소 가능성, 패소 가능성, 실제 결과 예측으로 표시하면 안 됩니다.

### 4. 판결문 상세 조회

검색 결과에서 사용자가 판결문을 선택하면 호출합니다.

```http
GET /api/cases/{case_id}
```

프론트에서 표시할 수 있는 값:

- 사건명
- 사건번호
- 법원명
- 선고일
- 판결 결과
- 주문
- 원문
- 출처

존재하지 않는 `case_id`이면 `CASE_NOT_FOUND`가 반환됩니다.

### 5. 판결문 섹션/문단 조회

원문을 섹션과 문단 단위로 보여주고 싶을 때 호출합니다.

```http
GET /api/cases/{case_id}/sections
```

프론트 표시 구조:

- 섹션 제목
- 문단 순서
- 원문 문단

`paragraph_id`는 특정 문단을 다시 쉬운 설명으로 변환할 때 사용합니다.

### 6. 판결문 요약

사용자가 요약 탭을 열거나 요약 버튼을 누르면 호출합니다.

```http
POST /api/cases/{case_id}/summary
```

요청 예시:

```json
{
  "force_regenerate": false
}
```

표시할 수 있는 값:

- 한 줄 요약
- 사건 배경
- 원고 주장
- 피고 주장
- 핵심 쟁점
- 법원의 판단
- 판결 결과
- 관련 법률 용어

### 7. 쉬운 판결문 생성

사용자가 쉬운 설명 보기를 누르면 호출합니다.

```http
POST /api/cases/{case_id}/simplify
```

요청 예시:

```json
{
  "section_types": ["주문", "법원의 판단"],
  "force_regenerate": false
}
```

프론트에서 반드시 같이 보여줄 값:

- `original_text`
- `simplified_text`
- `validation_status`
- `warnings`

주의:

- `validation_status`가 `passed`가 아니면 정확한 변환처럼 표시하면 안 됩니다.
- `warnings`가 있으면 검토 필요 상태로 보여주는 것이 안전합니다.

### 8. 생성된 쉬운 설명 조회

이미 만든 쉬운 설명을 다시 가져올 때 호출합니다.

```http
GET /api/cases/{case_id}/simplified
```

사용자가 상세 페이지를 다시 열었을 때 기존 결과를 재사용할 수 있습니다.

### 9. 문단 하나 다시 변환

특정 문단만 다시 처리할 때 호출합니다.

```http
POST /api/cases/{case_id}/paragraphs/{paragraph_id}/simplify
```

전체 판결문을 다시 처리하지 않고 선택한 문단만 업데이트할 수 있습니다.

### 10. 법률 용어 조회

사용자가 특정 용어를 클릭하면 호출합니다.

```http
GET /api/legal-terms/{term}
```

표시할 수 있는 값:

- 쉬운 정의
- 예시
- 주의사항
- 출처

### 11. 판결문 내 법률 용어 추출

판결문 상세 화면에서 어려운 용어 목록을 보여주고 싶을 때 호출합니다.

```http
GET /api/cases/{case_id}/legal-terms
```

응답에는 문단 ID가 포함될 수 있으므로, 원문 문단 하이라이트와 연결할 수 있습니다.

### 12. 유사 판결문 조회

현재 보고 있는 판결문과 비슷한 저장 판결문을 보여줄 때 호출합니다.

```http
GET /api/cases/{case_id}/similar
```

주의:

- 유사 판결문은 참고용 검색 결과입니다.
- 사용자의 사건 결과를 예측하는 기능이 아닙니다.

## 프론트 화면별 추천 API

| 화면 | 추천 API |
| --- | --- |
| 앱 초기화 | `GET /api/health` |
| 사건 입력 화면 | `POST /api/cases/analyze` |
| 검색 결과 화면 | `POST /api/cases/search` |
| 판결문 상세 화면 | `GET /api/cases/{case_id}` |
| 원문 문단 보기 | `GET /api/cases/{case_id}/sections` |
| 요약 탭 | `POST /api/cases/{case_id}/summary` |
| 쉬운 설명 탭 | `POST /api/cases/{case_id}/simplify` |
| 기존 쉬운 설명 조회 | `GET /api/cases/{case_id}/simplified` |
| 문단 재생성 버튼 | `POST /api/cases/{case_id}/paragraphs/{paragraph_id}/simplify` |
| 용어 팝업 | `GET /api/legal-terms/{term}` |
| 판결문 용어 목록 | `GET /api/cases/{case_id}/legal-terms` |
| 비슷한 판결문 영역 | `GET /api/cases/{case_id}/similar` |

## 사용자에게 보여줄 기본 안내 문구

```text
이 서비스는 공개 또는 샘플 판결문 검색과 이해를 돕기 위한 참고용 서비스이며,
법률 자문이나 소송 결과 예측을 제공하지 않습니다.
```

## 프론트 구현 시 주의사항

- 사용자의 원문 사건 내용은 필요한 요청에만 사용한다.
- 개인정보가 포함될 수 있으므로 전체 사건 내용을 브라우저 콘솔에 그대로 출력하지 않는다.
- `similarity_score`를 승소 가능성처럼 보여주지 않는다.
- `validation_status`가 실패 또는 검토 필요이면 쉬운 설명을 확정적 표현으로 보여주지 않는다.
- `error.details`는 운영 환경에서 `null`일 수 있으므로 필수 UI 로직에 사용하지 않는다.
- 존재하지 않는 판결문이나 문단을 백엔드가 새로 만들어내지 않는다는 점을 전제로 화면을 구성한다.
