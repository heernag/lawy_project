# CaseFinder Frontend

React + Vite 기반 CaseFinder 프론트엔드입니다.

## 실행

```powershell
npm install
npm run dev
```

기본 주소:

```text
http://localhost:5173
```

## 백엔드 연결

`.env.example`을 복사해서 `.env`를 만들고 FastAPI 주소를 지정합니다.

```env
VITE_API_BASE_URL=http://localhost:8000
```

백엔드가 배포되어 있다면 로컬 주소 대신 배포 주소를 넣습니다.

## 판례 API 연결 화면

- `/cases`: `POST /api/cases/search`
- `/cases/:caseId`: `GET /api/cases/{case_id}` 및 요약/쉬운설명/법률용어/유사판례 API
- `/cases?mode=analyze`: `POST /api/cases/analyze`

## 모바일 정리

820px 이하에서는 다음 원칙을 적용합니다.

- 홈/판례검색/생활법률의 장식 이미지를 숨김
- 헤더는 `CaseFinder + 햄버거` 중심으로 축소
- 전체 주요 메뉴를 햄버거 안에서 접근 가능
- 판례 카드 메타데이터를 세로 배치해 사건번호·법원·선고일 가독성 확보
- 검색 카테고리는 가로 스크롤 탭으로 제공
- 상세 페이지 탭도 가로 스크롤, 원문은 작은 화면에서 자동 줄바꿈

## Git에 올리지 않는 파일

- `node_modules/`
- `dist/`
- `.env`
- 대용량 법률 ZIP 데이터

대용량 법률 데이터는 frontend 폴더에 두지 않습니다. 자세한 내용은 `docs/GIT_AND_LEGAL_DATA_GUIDE_KO.md`를 참고하세요.
