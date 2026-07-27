import "../styles/case-list.css";
import { useMemo, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { FiBookmark, FiFilter, FiRefreshCw, FiSearch } from "react-icons/fi";

import Header from "../components/Header.jsx";
import HamburgerMenu from "../components/HamburgerMenu.jsx";
import caseSearchIllustration from "../assets/casefinder-illustration.png";

const caseCategories = [
  { id: "all", label: "전체", count: 124 },
  { id: "civil", label: "민사", count: 68 },
  { id: "criminal", label: "형사", count: 28 },
  { id: "administrative", label: "행정", count: 20 },
  { id: "family", label: "가사", count: 6 },
  { id: "constitutional", label: "헌법", count: 2 },
];

const caseData = [
  {
    id: "2024다12345",
    categoryId: "civil",
    category: "민사",
    title: "임대차보증금 반환",
    court: "대법원",
    date: "2025.03.14",
    caseNumber: "2024다12345",
    summary: "계약 종료 후 임대인이 보증금을 반환하지 않아 발생한 사건입니다.",
    tags: ["임대차", "보증금", "계약종료", "반환청구"],
  },
  {
    id: "2024도6789",
    categoryId: "criminal",
    category: "형사",
    title: "사기죄 성립 여부",
    court: "대법원",
    date: "2025.03.07",
    caseNumber: "2024도6789",
    summary:
      "피고인이 투자금을 편취할 목적으로 거짓말을 하였는지 여부가 쟁점입니다.",
    tags: ["사기죄", "투자사기", "기망행위", "편취"],
  },
  {
    id: "2024나24680",
    categoryId: "civil",
    category: "민사",
    title: "손해배상 청구",
    court: "서울고등법원",
    date: "2025.02.28",
    caseNumber: "2024나24680",
    summary: "교통사고로 인한 손해배상 청구 사건에서 과실 비율이 쟁점입니다.",
    tags: ["손해배상", "교통사고", "과실비율", "위자료"],
  },
  {
    id: "2024두13579",
    categoryId: "administrative",
    category: "행정",
    title: "과징금 부과 처분 취소",
    court: "대법원",
    date: "2025.02.20",
    caseNumber: "2024두13579",
    summary: "공정거래위원회의 과징금 부과 처분이 적법한지 여부가 쟁점입니다.",
    tags: ["과징금", "공정거래", "행정처분", "취소소송"],
  },
];

function CaseListPage() {
  const [menuOpen, setMenuOpen] = useState(false);
  const [searchParams, setSearchParams] = useSearchParams();

  const initialKeyword = searchParams.get("q") ?? "";

  const [keyword, setKeyword] = useState(initialKeyword);
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [selectedCourt, setSelectedCourt] = useState("all");
  const [selectedPeriod, setSelectedPeriod] = useState("all");
  const [sortOrder, setSortOrder] = useState("latest");
  const [mobileFilterOpen, setMobileFilterOpen] = useState(false);
  const [savedCaseIds, setSavedCaseIds] = useState([]);

  const filteredCases = useMemo(() => {
    const normalizedKeyword = keyword.trim().toLowerCase();

    return caseData.filter((caseItem) => {
      const matchesCategory =
        selectedCategory === "all" || caseItem.categoryId === selectedCategory;

      const matchesCourt =
        selectedCourt === "all" || caseItem.court === selectedCourt;

      const searchableText = [
        caseItem.title,
        caseItem.caseNumber,
        caseItem.summary,
        ...caseItem.tags,
      ]
        .join(" ")
        .toLowerCase();

      const matchesKeyword =
        !normalizedKeyword || searchableText.includes(normalizedKeyword);

      return matchesCategory && matchesCourt && matchesKeyword;
    });
  }, [keyword, selectedCategory, selectedCourt]);

  const handleSearch = (event) => {
    event.preventDefault();

    const trimmedKeyword = keyword.trim();

    if (trimmedKeyword) {
      setSearchParams({ q: trimmedKeyword });
    } else {
      setSearchParams({});
    }
  };

  const handleReset = () => {
    setKeyword("");
    setSelectedCategory("all");
    setSelectedCourt("all");
    setSelectedPeriod("all");
    setSortOrder("latest");
    setSearchParams({});
  };

  const handleSaveCase = (caseId) => {
    setSavedCaseIds((currentIds) =>
      currentIds.includes(caseId)
        ? currentIds.filter((id) => id !== caseId)
        : [...currentIds, caseId],
    );
  };

  return (
    <div className="app">
      <Header onMenuOpen={() => setMenuOpen(true)} />

      <HamburgerMenu isOpen={menuOpen} onClose={() => setMenuOpen(false)} />

      <main className="case-search-page">
        <section className="case-search-hero">
          <div className="case-search-hero-inner">
            <div className="case-search-heading">
              <h1>판례검색</h1>
              <p>사건명, 키워드, 사건번호로 판례를 찾아보세요.</p>
            </div>

            <form className="case-search-form" onSubmit={handleSearch}>
              <input
                type="search"
                value={keyword}
                placeholder="사건명, 키워드, 사건번호를 입력하세요"
                aria-label="판례 검색어"
                onChange={(event) => setKeyword(event.target.value)}
              />

              <button type="submit" aria-label="검색">
                <FiSearch />
              </button>
            </form>

            <div className="case-category-tabs">
              {caseCategories.map((category) => (
                <button
                  key={category.id}
                  type="button"
                  className={selectedCategory === category.id ? "active" : ""}
                  onClick={() => setSelectedCategory(category.id)}
                >
                  {category.label}
                </button>
              ))}
            </div>

            <div className="case-search-visual" aria-hidden="true">
              <img src={caseSearchIllustration} alt="" />
            </div>
          </div>
        </section>

        <section className="case-search-content">
          <div className="case-search-layout">
            <aside
              className={`case-filter-panel ${
                mobileFilterOpen ? "mobile-open" : ""
              }`}
            >
              <div className="case-filter-header">
                <h2>검색 필터</h2>

                <button type="button" onClick={handleReset}>
                  초기화
                  <FiRefreshCw />
                </button>
              </div>

              <div className="filter-group">
                <h3>사건 분야</h3>

                {caseCategories.map((category) => (
                  <label key={category.id} className="filter-checkbox-row">
                    <input
                      type="radio"
                      name="case-category"
                      checked={selectedCategory === category.id}
                      onChange={() => setSelectedCategory(category.id)}
                    />

                    <span>{category.label}</span>
                    <small>{category.count}</small>
                  </label>
                ))}
              </div>

              <div className="filter-group">
                <label htmlFor="court-filter">법원</label>

                <select
                  id="court-filter"
                  value={selectedCourt}
                  onChange={(event) => setSelectedCourt(event.target.value)}
                >
                  <option value="all">전체 법원</option>
                  <option value="대법원">대법원</option>
                  <option value="서울고등법원">서울고등법원</option>
                  <option value="서울중앙지방법원">서울중앙지방법원</option>
                </select>
              </div>

              <div className="filter-group">
                <label htmlFor="period-filter">선고 기간</label>

                <select
                  id="period-filter"
                  value={selectedPeriod}
                  onChange={(event) => setSelectedPeriod(event.target.value)}
                >
                  <option value="all">전체 기간</option>
                  <option value="1month">최근 1개월</option>
                  <option value="3months">최근 3개월</option>
                  <option value="1year">최근 1년</option>
                </select>
              </div>

              <div className="filter-group">
                <label htmlFor="sort-filter">정렬 방법</label>

                <select
                  id="sort-filter"
                  value={sortOrder}
                  onChange={(event) => setSortOrder(event.target.value)}
                >
                  <option value="latest">최신순</option>
                  <option value="oldest">오래된순</option>
                  <option value="relevance">관련도순</option>
                </select>
              </div>

              <button
                type="button"
                className="filter-submit-button"
                onClick={() => setMobileFilterOpen(false)}
              >
                검색하기
              </button>
            </aside>

            <div className="case-results-area">
              <div className="case-results-header">
                <h2>
                  검색 결과 <strong>124건</strong>
                </h2>

                <div className="case-results-actions">
                  <button
                    type="button"
                    className="mobile-filter-button"
                    onClick={() => setMobileFilterOpen((current) => !current)}
                  >
                    <FiFilter />
                    필터
                  </button>

                  <select aria-label="한 페이지 표시 개수" defaultValue="10">
                    <option value="10">10개씩 보기</option>
                    <option value="20">20개씩 보기</option>
                    <option value="30">30개씩 보기</option>
                  </select>
                </div>
              </div>

              <div className="case-result-list">
                {filteredCases.length > 0 ? (
                  filteredCases.map((caseItem) => {
                    const isSaved = savedCaseIds.includes(caseItem.id);

                    return (
                      <article className="case-result-card" key={caseItem.id}>
                        <div className="case-result-card-top">
                          <span
                            className={`case-result-category ${caseItem.categoryId}`}
                          >
                            {caseItem.category}
                          </span>

                          <button
                            type="button"
                            className={`case-save-button ${
                              isSaved ? "saved" : ""
                            }`}
                            aria-label={
                              isSaved ? "저장한 판례에서 제거" : "판례 저장"
                            }
                            onClick={() => handleSaveCase(caseItem.id)}
                          >
                            <FiBookmark />
                          </button>
                        </div>

                        <h3>{caseItem.title}</h3>

                        <div className="case-result-meta">
                          <span>{caseItem.court}</span>
                          <span>{caseItem.date}</span>
                          <span>{caseItem.caseNumber}</span>
                        </div>

                        <p className="case-result-summary">
                          {caseItem.summary}
                        </p>

                        <div className="case-result-tags">
                          {caseItem.tags.map((tag) => (
                            <span key={tag}>#{tag}</span>
                          ))}
                        </div>
                      </article>
                    );
                  })
                ) : (
                  <div className="case-empty-result">
                    <FiSearch />
                    <h3>검색 결과가 없습니다.</h3>
                    <p>검색어나 필터 조건을 다시 확인해주세요.</p>
                  </div>
                )}
              </div>

              <nav className="case-pagination" aria-label="검색 결과 페이지">
                <button type="button" aria-label="이전 페이지">
                  ‹
                </button>
                <button type="button" className="active">
                  1
                </button>
                <button type="button">2</button>
                <button type="button">3</button>
                <button type="button">4</button>
                <button type="button">5</button>
                <span>…</span>
                <button type="button">13</button>
                <button type="button" aria-label="다음 페이지">
                  ›
                </button>
              </nav>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}

export default CaseListPage;
