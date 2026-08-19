import "../styles/case-list.css";
import { useEffect, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import {
  FiAlertCircle,
  FiBookmark,
  FiCheckCircle,
  FiFilter,
  FiLoader,
  FiRefreshCw,
  FiSearch,
} from "react-icons/fi";

import Header from "../components/Header.jsx";
import HamburgerMenu from "../components/HamburgerMenu.jsx";
import caseSearchIllustration from "../assets/casefinder-illustration.png";
import { analyzeCase, searchCases } from "../api/cases";

const caseCategories = [
  { id: "all", label: "전체", value: null },
  { id: "civil", label: "민사", value: "민사" },
  { id: "criminal", label: "형사", value: "형사" },
  { id: "family", label: "가사", value: "가사" },
  { id: "labor", label: "노동", value: "노동" },
  { id: "administrative", label: "행정", value: "행정" },
  { id: "patent", label: "특허", value: "특허" },
  { id: "privacy", label: "개인정보", value: "개인정보" },
  { id: "finance", label: "금융·조세", value: "금융조세" },
  { id: "business", label: "기업", value: "기업" },
];

function formatDate(dateString) {
  if (!dateString) return "선고일 미상";
  return dateString.replaceAll("-", ".");
}

function readSavedIds() {
  try {
    return JSON.parse(localStorage.getItem("casefinder-saved-case-ids") || "[]");
  } catch {
    return [];
  }
}

function buildPageNumbers(currentPage, totalPages) {
  if (totalPages <= 5) {
    return Array.from({ length: totalPages }, (_, index) => index + 1);
  }

  let start = Math.max(1, currentPage - 2);
  let end = Math.min(totalPages, start + 4);
  start = Math.max(1, end - 4);

  const pages = [];
  for (let page = start; page <= end; page += 1) pages.push(page);
  return pages;
}

function CaseListPage() {
  const [menuOpen, setMenuOpen] = useState(false);
  const [searchParams, setSearchParams] = useSearchParams();
  const urlQuery = searchParams.get("q") ?? "";
  const analysisMode = searchParams.get("mode") === "analyze";

  const [keyword, setKeyword] = useState(urlQuery);
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [courtName, setCourtName] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [mobileFilterOpen, setMobileFilterOpen] = useState(false);
  const [savedCaseIds, setSavedCaseIds] = useState(readSavedIds);

  const [results, setResults] = useState([]);
  const [totalCount, setTotalCount] = useState(0);
  const [page, setPage] = useState(1);
  const [size, setSize] = useState(10);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [hasSearched, setHasSearched] = useState(false);

  const [analysisText, setAnalysisText] = useState("");
  const [analysisResult, setAnalysisResult] = useState(null);
  const [analysisLoading, setAnalysisLoading] = useState(false);
  const [analysisError, setAnalysisError] = useState("");

  const totalPages = Math.max(1, Math.ceil(totalCount / size));
  const visiblePages = buildPageNumbers(page, totalPages);

  async function performSearch(overrides = {}) {
    const nextKeyword = (overrides.query ?? keyword).trim();
    const nextCategory = overrides.category ?? selectedCategory;
    const nextCourt = overrides.court ?? courtName;
    const nextStartDate = overrides.startDate ?? startDate;
    const nextEndDate = overrides.endDate ?? endDate;
    const nextPage = overrides.page ?? page;
    const nextSize = overrides.size ?? size;

    if (nextKeyword.length < 2) {
      setError("검색어를 2자 이상 입력해주세요.");
      setResults([]);
      setTotalCount(0);
      setHasSearched(false);
      return;
    }

    if (nextStartDate && nextEndDate && nextStartDate > nextEndDate) {
      setError("시작일은 종료일보다 늦을 수 없습니다.");
      return;
    }

    const categoryValue =
      caseCategories.find((item) => item.id === nextCategory)?.value ?? null;

    setLoading(true);
    setError("");
    setHasSearched(true);

    try {
      const data = await searchCases({
        query: nextKeyword,
        category: categoryValue,
        court: nextCourt.trim() || null,
        startDate: nextStartDate || null,
        endDate: nextEndDate || null,
        judgmentResult: null,
        page: nextPage,
        size: nextSize,
      });

      setResults(data.results ?? []);
      setTotalCount(data.total_count ?? 0);
      setPage(data.page ?? nextPage);
      setSize(data.size ?? nextSize);
    } catch (requestError) {
      setResults([]);
      setTotalCount(0);
      setError(requestError.message || "판례 검색 중 오류가 발생했습니다.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    setKeyword(urlQuery);
    if (urlQuery.trim().length >= 2) {
      performSearch({ query: urlQuery, page: 1 });
    }
    // URL 검색어 변경 시 검색을 다시 수행합니다.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [urlQuery]);

  const handleSearch = (event) => {
    event.preventDefault();
    const trimmedKeyword = keyword.trim();

    if (trimmedKeyword.length < 2) {
      setError("검색어를 2자 이상 입력해주세요.");
      return;
    }

    const nextParams = new URLSearchParams(searchParams);
    nextParams.set("q", trimmedKeyword);
    nextParams.delete("mode");

    if (urlQuery === trimmedKeyword) {
      performSearch({ query: trimmedKeyword, page: 1 });
    } else {
      setSearchParams(nextParams);
    }
  };

  const handleCategoryChange = (categoryId) => {
    setSelectedCategory(categoryId);
    setPage(1);
    if (keyword.trim().length >= 2) {
      performSearch({ category: categoryId, page: 1 });
    }
  };

  const handleApplyFilters = () => {
    setMobileFilterOpen(false);
    setPage(1);
    performSearch({ page: 1 });
  };

  const handleReset = () => {
    setSelectedCategory("all");
    setCourtName("");
    setStartDate("");
    setEndDate("");
    setPage(1);

    if (keyword.trim().length >= 2) {
      performSearch({
        category: "all",
        court: "",
        startDate: "",
        endDate: "",
        page: 1,
      });
    }
  };

  const handleSaveCase = (caseId) => {
    setSavedCaseIds((currentIds) => {
      const nextIds = currentIds.includes(caseId)
        ? currentIds.filter((id) => id !== caseId)
        : [...currentIds, caseId];
      localStorage.setItem("casefinder-saved-case-ids", JSON.stringify(nextIds));
      return nextIds;
    });
  };

  const handlePageChange = (nextPage) => {
    if (nextPage < 1 || nextPage > totalPages || loading) return;
    setPage(nextPage);
    performSearch({ page: nextPage });
  };

  const handleSizeChange = (event) => {
    const nextSize = Number(event.target.value);
    setSize(nextSize);
    setPage(1);
    if (keyword.trim().length >= 2) {
      performSearch({ size: nextSize, page: 1 });
    }
  };

  const handleAnalyze = async (event) => {
    event.preventDefault();
    const trimmed = analysisText.trim();

    if (trimmed.length < 5) {
      setAnalysisError("사건 설명을 5자 이상 입력해주세요.");
      return;
    }

    setAnalysisLoading(true);
    setAnalysisError("");

    try {
      const data = await analyzeCase(trimmed);
      setAnalysisResult(data);
    } catch (requestError) {
      setAnalysisResult(null);
      setAnalysisError(requestError.message || "사건 분석 중 오류가 발생했습니다.");
    } finally {
      setAnalysisLoading(false);
    }
  };

  const handleSearchAnalyzedKeywords = () => {
    const nextKeyword = (analysisResult?.search_keywords ?? []).join(" ").trim();
    if (nextKeyword.length < 2) return;

    setKeyword(nextKeyword);
    const nextParams = new URLSearchParams(searchParams);
    nextParams.set("q", nextKeyword);
    nextParams.delete("mode");
    setSearchParams(nextParams);
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
                placeholder="검색어를 2자 이상 입력하세요"
                aria-label="판례 검색어"
                onChange={(event) => setKeyword(event.target.value)}
              />
              <button type="submit" aria-label="검색"><FiSearch /></button>
            </form>

            <div className="case-category-tabs" aria-label="사건 분야">
              {caseCategories.map((category) => (
                <button
                  key={category.id}
                  type="button"
                  className={selectedCategory === category.id ? "active" : ""}
                  onClick={() => handleCategoryChange(category.id)}
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

        {analysisMode && (
          <section className="case-analysis-section">
            <div className="case-analysis-panel">
              <div className="case-analysis-heading">
                <strong>내 상황으로 판례 찾기</strong>
                <p>사건 상황을 설명하면 검색에 사용할 핵심 정보를 정리합니다.</p>
              </div>

              <form onSubmit={handleAnalyze}>
                <textarea
                  value={analysisText}
                  onChange={(event) => setAnalysisText(event.target.value)}
                  placeholder="예: 전세 계약이 끝났는데 집주인이 보증금을 돌려주지 않습니다."
                  maxLength={2000}
                />
                <button type="submit" disabled={analysisLoading}>
                  {analysisLoading ? <FiLoader className="spin-icon" /> : <FiSearch />}
                  상황 분석하기
                </button>
              </form>

              {analysisError && (
                <div className="case-analysis-message error"><FiAlertCircle /> {analysisError}</div>
              )}

              {analysisResult && (
                <div className="case-analysis-result">
                  <div className="case-analysis-summary-row">
                    <span>{analysisResult.category || "분야 미분류"}</span>
                    <span>{analysisResult.sub_category || "세부 분류 없음"}</span>
                  </div>

                  {analysisResult.privacy_warnings?.length > 0 && (
                    <div className="case-analysis-message warning">
                      <FiAlertCircle />
                      <div>
                        {analysisResult.privacy_warnings.map((warning) => <p key={warning}>{warning}</p>)}
                      </div>
                    </div>
                  )}

                  <div className="case-analysis-block">
                    <strong>정리된 사건 내용</strong>
                    <p>{analysisResult.sanitized_query}</p>
                  </div>

                  {analysisResult.legal_issues?.length > 0 && (
                    <div className="case-analysis-block">
                      <strong>핵심 쟁점</strong>
                      <div className="case-analysis-tags">
                        {analysisResult.legal_issues.map((issue) => <span key={issue}>{issue}</span>)}
                      </div>
                    </div>
                  )}

                  {analysisResult.search_keywords?.length > 0 && (
                    <div className="case-analysis-block">
                      <strong>추천 검색어</strong>
                      <div className="case-analysis-tags">
                        {analysisResult.search_keywords.map((item) => <span key={item}>#{item}</span>)}
                      </div>
                      <button type="button" className="analysis-search-button" onClick={handleSearchAnalyzedKeywords}>
                        이 키워드로 판례 검색
                      </button>
                    </div>
                  )}
                </div>
              )}
            </div>
          </section>
        )}

        <section className="case-search-content">
          <div className="case-search-layout">
            <aside className={`case-filter-panel ${mobileFilterOpen ? "mobile-open" : ""}`}>
              <div className="case-filter-header">
                <h2>검색 필터</h2>
                <button type="button" onClick={handleReset}>초기화 <FiRefreshCw /></button>
              </div>

              <div className="filter-group">
                <h3>사건 분야</h3>
                <div className="filter-category-list">
                  {caseCategories.map((category) => (
                    <label key={category.id} className="filter-checkbox-row">
                      <input
                        type="radio"
                        name="case-category"
                        checked={selectedCategory === category.id}
                        onChange={() => setSelectedCategory(category.id)}
                      />
                      <span>{category.label}</span>
                    </label>
                  ))}
                </div>
              </div>

              <div className="filter-group">
                <label htmlFor="court-filter">법원명</label>
                <input
                  id="court-filter"
                  className="filter-text-input"
                  type="text"
                  value={courtName}
                  placeholder="예: 서울고법, 대법원"
                  onChange={(event) => setCourtName(event.target.value)}
                />
                <small className="filter-help">데이터에 저장된 법원명과 동일하게 입력하면 정확합니다.</small>
              </div>

              <div className="filter-group">
                <span className="filter-group-title">선고 기간</span>
                <div className="filter-date-grid">
                  <label>
                    <span>시작일</span>
                    <input type="date" value={startDate} onChange={(event) => setStartDate(event.target.value)} />
                  </label>
                  <label>
                    <span>종료일</span>
                    <input type="date" value={endDate} onChange={(event) => setEndDate(event.target.value)} />
                  </label>
                </div>
              </div>

              <button type="button" className="filter-submit-button" onClick={handleApplyFilters}>
                필터 적용
              </button>
            </aside>

            <div className="case-results-area">
              <div className="case-results-header">
                <h2>검색 결과 <strong>{totalCount.toLocaleString("ko-KR")}건</strong></h2>

                <div className="case-results-actions">
                  <button
                    type="button"
                    className="mobile-filter-button"
                    onClick={() => setMobileFilterOpen((current) => !current)}
                    aria-expanded={mobileFilterOpen}
                  >
                    <FiFilter /> 필터
                  </button>

                  <select aria-label="한 페이지 표시 개수" value={size} onChange={handleSizeChange}>
                    <option value="10">10개씩 보기</option>
                    <option value="20">20개씩 보기</option>
                    <option value="30">30개씩 보기</option>
                    <option value="50">50개씩 보기</option>
                  </select>
                </div>
              </div>

              {error && (
                <div className="case-api-message error">
                  <FiAlertCircle />
                  <div><strong>검색할 수 없습니다.</strong><p>{error}</p></div>
                </div>
              )}

              {loading ? (
                <div className="case-empty-result">
                  <FiLoader className="spin-icon" />
                  <h3>판례를 검색하고 있습니다.</h3>
                  <p>대용량 판례 데이터에서는 검색에 조금 더 시간이 걸릴 수 있습니다.</p>
                </div>
              ) : (
                <div className="case-result-list">
                  {results.length > 0 ? (
                    results.map((caseItem) => {
                      const isSaved = savedCaseIds.includes(caseItem.case_id);
                      const relevance = Math.round((caseItem.similarity_score ?? 0) * 100);

                      return (
                        <article className="case-result-card" key={caseItem.case_id}>
                          <div className="case-result-card-top">
                            <div className="case-result-badge-row">
                              <span className="case-result-category">{caseItem.category || "기타"}</span>
                              {caseItem.judgment_result && (
                                <span className="case-result-judgment">{caseItem.judgment_result}</span>
                              )}
                            </div>

                            <button
                              type="button"
                              className={`case-save-button ${isSaved ? "saved" : ""}`}
                              aria-label={isSaved ? "저장한 판례에서 제거" : "판례 저장"}
                              onClick={() => handleSaveCase(caseItem.case_id)}
                            >
                              <FiBookmark />
                            </button>
                          </div>

                          <Link className="case-result-main-link" to={`/cases/${caseItem.case_id}`}>
                            <h3>{caseItem.case_name || "사건명 없음"}</h3>
                            <div className="case-result-meta">
                              <span>{caseItem.court_name || "법원 정보 없음"}</span>
                              <span>{formatDate(caseItem.decision_date)}</span>
                              <span>{caseItem.case_number || caseItem.case_id}</span>
                            </div>

                            <p className="case-result-summary">{caseItem.summary || "요약 정보가 없습니다."}</p>

                            {(caseItem.main_issues ?? []).length > 0 && (
                              <div className="case-result-tags">
                                {caseItem.main_issues.map((tag) => <span key={tag}>#{tag}</span>)}
                              </div>
                            )}

                            <div className="case-relevance-row">
                              <FiCheckCircle />
                              <span>검색 관련도 {relevance}%</span>
                              {caseItem.similarity_reason && <small>{caseItem.similarity_reason}</small>}
                            </div>
                          </Link>
                        </article>
                      );
                    })
                  ) : hasSearched && !error ? (
                    <div className="case-empty-result">
                      <FiSearch />
                      <h3>검색 결과가 없습니다.</h3>
                      <p>검색어나 필터 조건을 다시 확인해주세요.</p>
                    </div>
                  ) : (
                    <div className="case-empty-result">
                      <FiSearch />
                      <h3>판례를 검색해보세요.</h3>
                      <p>백엔드 검색은 2자 이상의 검색어가 필요합니다.</p>
                    </div>
                  )}
                </div>
              )}

              {totalPages > 1 && (
                <nav className="case-pagination" aria-label="검색 결과 페이지">
                  <button type="button" aria-label="이전 페이지" disabled={page <= 1} onClick={() => handlePageChange(page - 1)}>‹</button>
                  {visiblePages.map((pageNumber) => (
                    <button
                      type="button"
                      key={pageNumber}
                      className={pageNumber === page ? "active" : ""}
                      onClick={() => handlePageChange(pageNumber)}
                    >
                      {pageNumber}
                    </button>
                  ))}
                  <button type="button" aria-label="다음 페이지" disabled={page >= totalPages} onClick={() => handlePageChange(page + 1)}>›</button>
                </nav>
              )}
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}

export default CaseListPage;
