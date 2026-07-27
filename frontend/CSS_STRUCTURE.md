# CaseFinder CSS 구조

- `src/styles/common.css`: 색상 변수와 `.app` 전역 스타일
- `src/styles/shared-page.css`: 서브 페이지 공통 컨테이너와 제목, 카드 스타일
- `src/styles/header.css`: Header, HamburgerMenu
- `src/styles/home.css`: 홈 화면과 SearchBar
- `src/styles/case-list.css`: 판례검색 목록
- `src/styles/case-detail.css`: 판례 상세
- `src/styles/life-law.css`: 생활법률
- `src/styles/legal-terms.css`: 법률용어
- `src/styles/court-map.css`: 법원 찾기
- `src/styles/community.css`: 커뮤니티
- `src/styles/saved-cases.css`: 저장한 판례
- `src/styles/recent-cases.css`: 최근 본 판례
- `src/styles/notices.css`: 공지사항
- `src/styles/faq.css`: 자주 묻는 질문
- `src/styles/customer-service.css`: 고객센터
- `src/styles/settings.css`: 설정

`main.jsx`는 공통 CSS만 불러오며, 각 페이지와 컴포넌트는 자신에게 필요한 CSS 파일을 직접 import합니다.
