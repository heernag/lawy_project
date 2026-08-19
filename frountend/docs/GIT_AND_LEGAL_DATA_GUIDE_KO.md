# CaseFinder Git / 대용량 법률 데이터 관리 가이드

## 1. 권장 프로젝트 구조

```text
CaseFinder/
├─ frontend/
├─ backend/
│  ├─ app/
│  ├─ scripts/
│  │  └─ import_nia_zip_cases.py
│  └─ .env.example
├─ docs/
├─ .gitignore
└─ README.md
```

법률 원본 ZIP은 Git 저장소 밖에 둡니다.

```text
G:\
├─ CaseFinder\              # Git 저장소
└─ CaseFinder_data\         # Git 저장소 밖
   ├─ TL_01.일반판결.zip
   └─ TL_02.1-2.최종심.zip
```

## 2. 팀원별 데이터 위치

각 팀원은 법률 ZIP을 자기 PC의 원하는 위치에 둡니다.

예:

```text
D:\CaseFinder_data
G:\CaseFinder_data
H:\CaseFinder_data
```

백엔드의 `.env`에는 각자 실제 경로만 적습니다.

```env
NIA_DATA_DIR=G:\CaseFinder_data
```

`.env`는 Git에 올리지 않습니다. `.env.example`만 공유합니다.

## 3. 중요한 원칙

웹 브라우저가 ZIP을 직접 읽는 구조로 만들지 않습니다.

```text
NIA ZIP
  ↓ 최초/갱신 시 importer
DB(PostgreSQL 권장)
  ↓
FastAPI
  ↓
React/Vite
```

프론트엔드는 법률 ZIP 위치를 알 필요가 없습니다.

## 4. 로컬 백엔드와 팀원 접근

`127.0.0.1` 또는 `localhost`로 실행한 FastAPI는 실행한 PC에서만 접근 가능합니다.
다른 팀원이나 외부 사용자가 보려면 공용으로 접근 가능한 백엔드가 필요합니다.

개발 중 같은 네트워크에서만 공유할 경우 FastAPI를 `0.0.0.0`으로 바인딩할 수 있지만,
방화벽/네트워크 설정이 필요하고 인터넷 공개용 방식으로 권장하지 않습니다.

팀 프로젝트 공유는 배포 서버 + 공용 DB 구조를 권장합니다.

## 5. Git 작업 흐름

```powershell
git pull

git checkout -b feature/mobile-ui
# 파일 수정

git add .
git commit -m "feat: 모바일 UI 및 판례 API 연동 정리"
git push -u origin feature/mobile-ui
```

그 후 GitHub에서 Pull Request를 생성하고 검토 후 `main`에 병합합니다.

## 6. 절대 Git에 넣지 말 것

- 대용량 NIA ZIP
- `.env`
- `node_modules`
- 로컬 SQLite DB(공용 운영 DB로 쓰지 않는 경우)
- 임시 출력/캐시 파일
