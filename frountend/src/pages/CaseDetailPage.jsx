import "../styles/case-detail.css";
import { useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import {
  FiAlertCircle,
  FiArrowLeft,
  FiBookOpen,
  FiBookmark,
  FiCheckCircle,
  FiExternalLink,
  FiFileText,
  FiLoader,
  FiShare2,
} from "react-icons/fi";

import Header from "../components/Header.jsx";
import HamburgerMenu from "../components/HamburgerMenu.jsx";
import {
  getCaseDetail,
  getCaseLegalTerms,
  getSimilarCases,
  simplifyCase,
  summarizeCase,
} from "../api/cases";

const tabs = [
  { id: "summary", label: "핵심 요약" },
  { id: "simple", label: "쉬운 설명" },
  { id: "original", label: "판결 원문" },
  { id: "terms", label: "법률 용어" },
  { id: "similar", label: "유사 판례" },
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

function CaseDetailPage() {
  const [menuOpen, setMenuOpen] = useState(false);
  const { caseId } = useParams();

  const [detail, setDetail] = useState(null);
  const [detailLoading, setDetailLoading] = useState(true);
  const [detailError, setDetailError] = useState("");
  const [saved, setSaved] = useState(false);

  const [activeTab, setActiveTab] = useState("summary");
  const [summary, setSummary] = useState(null);
  const [simplified, setSimplified] = useState(null);
  const [terms, setTerms] = useState(null);
  const [similarCases, setSimilarCases] = useState(null);
  const [tabLoading, setTabLoading] = useState(false);
  const [tabError, setTabError] = useState("");

  const sourceLinkAvailable = useMemo(
    () => Boolean(detail?.source_url?.startsWith("http")),
    [detail],
  );

  useEffect(() => {
    let cancelled = false;

    async function loadDetail() {
      setDetailLoading(true);
      setDetailError("");

      try {
        const data = await getCaseDetail(caseId);
        if (cancelled) return;
        setDetail(data);
        setSaved(readSavedIds().includes(data.case_id));

        try {
          const currentRecent = JSON.parse(
            localStorage.getItem("casefinder-recent-cases") || "[]",
          );
          const nextRecent = [
            {
              case_id: data.case_id,
              case_name: data.case_name,
              case_number: data.case_number,
              court_name: data.court_name,
              decision_date: data.decision_date,
              viewed_at: new Date().toISOString(),
            },
            ...currentRecent.filter((item) => item.case_id !== data.case_id),
          ].slice(0, 20);
          localStorage.setItem("casefinder-recent-cases", JSON.stringify(nextRecent));
        } catch {
          // 최근 본 판례 저장 실패는 상세 조회 자체를 막지 않습니다.
        }
      } catch (error) {
        if (!cancelled) {
          setDetailError(error.message || "판례 상세 정보를 불러오지 못했습니다.");
        }
      } finally {
        if (!cancelled) setDetailLoading(false);
      }
    }

    loadDetail();
    return () => {
      cancelled = true;
    };
  }, [caseId]);

  useEffect(() => {
    if (!detail) return;
    let cancelled = false;

    async function loadTabData() {
      setTabError("");

      if (activeTab === "original") return;
      if (activeTab === "summary" && summary) return;
      if (activeTab === "simple" && simplified) return;
      if (activeTab === "terms" && terms) return;
      if (activeTab === "similar" && similarCases) return;

      setTabLoading(true);
      try {
        if (activeTab === "summary") {
          const data = await summarizeCase(caseId);
          if (!cancelled) setSummary(data);
        }

        if (activeTab === "simple") {
          const data = await simplifyCase(caseId, ["주문", "법원의 판단"]);
          if (!cancelled) setSimplified(data);
        }

        if (activeTab === "terms") {
          const data = await getCaseLegalTerms(caseId);
          if (!cancelled) setTerms(data);
        }

        if (activeTab === "similar") {
          const data = await getSimilarCases(caseId);
          if (!cancelled) setSimilarCases(data);
        }
      } catch (error) {
        if (!cancelled) {
          setTabError(error.message || "정보를 불러오지 못했습니다.");
        }
      } finally {
        if (!cancelled) setTabLoading(false);
      }
    }

    loadTabData();
    return () => {
      cancelled = true;
    };
  }, [activeTab, caseId, detail, simplified, similarCases, summary, terms]);

  const handleSave = () => {
    if (!detail) return;

    const ids = readSavedIds();
    const nextIds = ids.includes(detail.case_id)
      ? ids.filter((id) => id !== detail.case_id)
      : [...ids, detail.case_id];

    localStorage.setItem("casefinder-saved-case-ids", JSON.stringify(nextIds));
    setSaved(nextIds.includes(detail.case_id));
  };

  const handleShare = async () => {
    const shareData = {
      title: detail?.case_name || "CaseFinder 판례",
      text: detail?.summary || "",
      url: window.location.href,
    };

    try {
      if (navigator.share) {
        await navigator.share(shareData);
      } else {
        await navigator.clipboard.writeText(window.location.href);
        alert("현재 판례 주소를 복사했습니다.");
      }
    } catch {
      // 사용자가 공유 창을 닫은 경우에는 별도 오류를 표시하지 않습니다.
    }
  };

  const renderTabContent = () => {
    if (tabLoading) {
      return (
        <div className="detail-tab-state">
          <FiLoader className="detail-loading-icon" />
          <p>정보를 불러오고 있습니다.</p>
        </div>
      );
    }

    if (tabError) {
      return (
        <div className="detail-tab-state error">
          <FiAlertCircle />
          <strong>정보를 불러오지 못했습니다.</strong>
          <p>{tabError}</p>
        </div>
      );
    }

    if (activeTab === "summary") {
      const data = summary;
      if (!data) return null;

      return (
        <div className="detail-summary-content">
          <div className="detail-highlight-box">
            <strong>한 줄 요약</strong>
            <p>{data.one_line_summary || detail.summary}</p>
          </div>

          {data.background && (
            <section className="detail-text-section">
              <h3>사건 배경</h3>
              <p>{data.background}</p>
            </section>
          )}

          {data.plaintiff_claim && (
            <section className="detail-text-section">
              <h3>원고의 주장</h3>
              <p>{data.plaintiff_claim}</p>
            </section>
          )}

          {data.defendant_claim && (
            <section className="detail-text-section">
              <h3>피고의 주장</h3>
              <p>{data.defendant_claim}</p>
            </section>
          )}

          {data.main_issues?.length > 0 && (
            <section className="detail-text-section">
              <h3>핵심 쟁점</h3>
              <ul className="detail-issue-list">
                {data.main_issues.map((issue) => (
                  <li key={issue}>{issue}</li>
                ))}
              </ul>
            </section>
          )}

          {data.court_reasoning && (
            <section className="detail-text-section">
              <h3>법원의 판단</h3>
              <p>{data.court_reasoning}</p>
            </section>
          )}

          <div className="notice-box">
            자동 생성된 핵심 요약은 판례 이해를 돕기 위한 참고 정보입니다. 실제 판단에는 원문을 함께 확인해주세요.
          </div>
        </div>
      );
    }

    if (activeTab === "simple") {
      const paragraphs = simplified?.paragraphs ?? [];
      return paragraphs.length > 0 ? (
        <div className="simplified-list">
          {paragraphs.map((paragraph) => (
            <article className="simplified-card" key={paragraph.paragraph_id}>
              <div className="simplified-card-head">
                <strong>쉬운 판례 설명</strong>
                <span
                  className={
                    paragraph.validation_status === "passed"
                      ? "validation-badge passed"
                      : "validation-badge warning"
                  }
                >
                  {paragraph.validation_status === "passed" ? (
                    <><FiCheckCircle /> 검증 완료</>
                  ) : (
                    <><FiAlertCircle /> 확인 필요</>
                  )}
                </span>
              </div>
              <div className="simplified-compare">
                <div>
                  <span>원문</span>
                  <p>{paragraph.original_text}</p>
                </div>
                <div>
                  <span>쉬운 설명</span>
                  <p>{paragraph.simplified_text}</p>
                </div>
              </div>
              {paragraph.warnings?.length > 0 && (
                <div className="simplified-warning">
                  {paragraph.warnings.join(" · ")}
                </div>
              )}
            </article>
          ))}
        </div>
      ) : (
        <div className="detail-tab-state">
          <FiFileText />
          <p>현재 표시할 쉬운 설명이 없습니다.</p>
        </div>
      );
    }

    if (activeTab === "original") {
      return (
        <div className="original-case-text">
          <pre>{detail.original_text || "판결 원문이 없습니다."}</pre>
        </div>
      );
    }

    if (activeTab === "terms") {
      const termItems = terms?.terms ?? [];
      return termItems.length > 0 ? (
        <div className="detail-term-list">
          {termItems.map((item) => (
            <article className="detail-term-card" key={`${item.term}-${item.paragraph_id || "case"}`}>
              <strong>{item.term}</strong>
              {item.easy_definition && <p>{item.easy_definition}</p>}
              {item.context_meaning && <small>{item.context_meaning}</small>}
            </article>
          ))}
        </div>
      ) : (
        <div className="detail-tab-state">
          <FiBookOpen />
          <p>이 판례에서 추출된 법률 용어가 없습니다.</p>
        </div>
      );
    }

    const items = similarCases?.results ?? [];
    return items.length > 0 ? (
      <div className="similar-case-list">
        {items.map((item) => (
          <Link className="similar-case-card" to={`/cases/${item.case_id}`} key={item.case_id}>
            <div>
              <span>{item.category}</span>
              <strong>{item.case_name}</strong>
              <p>{item.court_name} · {formatDate(item.decision_date)} · {item.case_number}</p>
            </div>
            <small>관련도 {Math.round((item.similarity_score ?? 0) * 100)}%</small>
          </Link>
        ))}
      </div>
    ) : (
      <div className="detail-tab-state">
        <FiFileText />
        <p>현재 표시할 유사 판례가 없습니다.</p>
      </div>
    );
  };

  return (
    <div className="app">
      <Header onMenuOpen={() => setMenuOpen(true)} />
      <HamburgerMenu isOpen={menuOpen} onClose={() => setMenuOpen(false)} />

      <main className="detail-page">
        <div className="content-container">
          <Link className="back-link" to="/cases">
            <FiArrowLeft /> 판례검색으로 돌아가기
          </Link>

          {detailLoading ? (
            <div className="detail-status-card">
              <FiLoader className="detail-loading-icon" />
              <h1>판례를 불러오고 있습니다.</h1>
            </div>
          ) : detailError ? (
            <div className="detail-status-card error">
              <FiAlertCircle />
              <h1>판례를 찾을 수 없습니다.</h1>
              <p>{detailError}</p>
              <Link to="/cases">판례검색으로 이동</Link>
            </div>
          ) : (
            <>
              <section className="detail-hero-card">
                <div>
                  <div className="detail-badge-row">
                    <span className="category-badge">{detail.category}</span>
                    {detail.judgment_result && (
                      <span className="judgment-result-badge">
                        {detail.judgment_result}
                      </span>
                    )}
                  </div>
                  <h1>{detail.case_name}</h1>
                  <p>
                    {detail.court_name} · {detail.case_number} · {formatDate(detail.decision_date)}
                  </p>
                </div>

                <div className="detail-actions">
                  <button type="button" onClick={handleSave} className={saved ? "active" : ""}>
                    <FiBookmark /> {saved ? "저장됨" : "저장"}
                  </button>
                  <button type="button" onClick={handleShare}>
                    <FiShare2 /> 공유
                  </button>
                </div>
              </section>

              <div className="detail-grid">
                <div className="detail-main-column">
                  <section className="detail-card detail-tab-card">
                    <div className="detail-tabs" role="tablist" aria-label="판례 상세 보기">
                      {tabs.map((tab) => (
                        <button
                          key={tab.id}
                          type="button"
                          role="tab"
                          aria-selected={activeTab === tab.id}
                          className={activeTab === tab.id ? "active" : ""}
                          onClick={() => setActiveTab(tab.id)}
                        >
                          {tab.label}
                        </button>
                      ))}
                    </div>
                    <div className="detail-tab-body">{renderTabContent()}</div>
                  </section>
                </div>

                <aside className="detail-sidebar">
                  <section className="detail-card case-info-card">
                    <h2>기본 정보</h2>
                    <dl>
                      <div><dt>법원</dt><dd>{detail.court_name || "-"}</dd></div>
                      <div><dt>재판부</dt><dd>{detail.court_department || "-"}</dd></div>
                      <div><dt>사건번호</dt><dd>{detail.case_number || "-"}</dd></div>
                      <div><dt>선고일</dt><dd>{formatDate(detail.decision_date)}</dd></div>
                      <div><dt>사건분류</dt><dd>{detail.category || "-"}</dd></div>
                      <div><dt>판결 결과</dt><dd>{detail.judgment_result || "-"}</dd></div>
                    </dl>
                  </section>

                  {detail.order_text && (
                    <section className="detail-card case-order-card">
                      <h2>주문</h2>
                      <p className="detail-order-text">{detail.order_text}</p>
                    </section>
                  )}

                  <section className="detail-card case-source-card">
                    <h2>출처</h2>
                    <p>{detail.source_name || "출처 정보 없음"}</p>
                    {sourceLinkAvailable && (
                      <a href={detail.source_url} target="_blank" rel="noreferrer">
                        원문 출처 열기 <FiExternalLink />
                      </a>
                    )}
                  </section>
                </aside>
              </div>
            </>
          )}
        </div>
      </main>
    </div>
  );
}

export default CaseDetailPage;
