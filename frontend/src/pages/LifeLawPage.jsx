import "../styles/life-law.css";
import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import {
  FiSearch,
  FiHome,
  FiTruck,
  FiDollarSign,
  FiUsers,
  FiBriefcase,
  FiShoppingCart,
  FiShield,
  FiEye,
  FiChevronRight,
  FiBookOpen,
  FiHeadphones,
} from "react-icons/fi";

import Header from "../components/Header.jsx";
import HamburgerMenu from "../components/HamburgerMenu.jsx";
import lifeLawIllustration from "../assets/lifelaw_img.png";

const categories = [
  {
    id: "housing",
    title: "주거·임대차",
    description: "임대차 계약, 보증금 분쟁 등",
    icon: FiHome,
  },
  {
    id: "traffic",
    title: "교통사고·보험",
    description: "교통사고, 보험 처리, 보상 등",
    icon: FiTruck,
  },
  {
    id: "finance",
    title: "금전·채무",
    description: "대출, 채무, 사기, 채권·채무 관계 등",
    icon: FiDollarSign,
  },
  {
    id: "family",
    title: "가족·상속",
    description: "이혼, 상속, 유언, 양육권 등",
    icon: FiUsers,
  },
  {
    id: "labor",
    title: "근로·노동",
    description: "근로계약, 임금, 해고, 산업재해 등",
    icon: FiBriefcase,
  },
  {
    id: "consumer",
    title: "소비자·계약",
    description: "소비자 피해, 계약 해지, 위약금 등",
    icon: FiShoppingCart,
  },
  {
    id: "other",
    title: "기타 생활법률",
    description: "개인정보, 명예훼손, 스토킹 등",
    icon: FiShield,
  },
];

const lifeLawContents = [
  {
    id: 1,
    categoryId: "housing",
    category: "주거·임대차",
    title: "전세 보증금을 돌려받지 못했어요. 어떻게 해야 하나요?",
    summary:
      "임대차 계약이 종료되었는데도 임대인이 보증금을 반환하지 않는 경우, 내용증명 발송부터 지급명령과 소송까지 단계별 해결 방법을 안내해드립니다.",
    views: "12.4K",
    icon: FiHome,
  },
  {
    id: 2,
    categoryId: "traffic",
    category: "교통사고·보험",
    title: "교통사고 가해자가 합의해주지 않아요. 소송해야 하나요?",
    summary:
      "가해자와 합의가 되지 않는 경우 피해자가 진행할 수 있는 보험 처리와 손해배상 청구 방법을 알려드립니다.",
    views: "8.7K",
    icon: FiTruck,
  },
  {
    id: 3,
    categoryId: "finance",
    category: "금전·채무",
    title: "빌려준 돈을 받지 못했어요. 어떤 방법이 있나요?",
    summary:
      "차용증이나 계좌이체 내역이 있는 경우 내용증명 발송부터 지급명령 신청까지 필요한 절차를 소개합니다.",
    views: "7.2K",
    icon: FiDollarSign,
  },
  {
    id: 4,
    categoryId: "family",
    category: "가족·상속",
    title: "부모님 재산 상속, 어떻게 진행되나요?",
    summary:
      "상속 순위, 상속포기, 한정승인 등 상속 절차와 필요한 서류를 쉽게 설명해드립니다.",
    views: "6.1K",
    icon: FiUsers,
  },
  {
    id: 5,
    categoryId: "labor",
    category: "근로·노동",
    title: "퇴직금을 받지 못했어요. 어떻게 해야 하나요?",
    summary:
      "퇴직금 지급 기준과 미지급 시 노동청 진정 또는 민사소송 절차를 안내해드립니다.",
    views: "5.8K",
    icon: FiBriefcase,
  },
];

const popularContents = [
  "임대차 계약 해지 통보 방법",
  "전세 보증금 반환 절차",
  "교통사고 합의 요령",
  "내용증명 작성 방법",
  "채무 불이행 대응 방법",
];

function LifeLawPage() {
  const [menuOpen, setMenuOpen] = useState(false);
  const [keyword, setKeyword] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [selectedTab, setSelectedTab] = useState("all");

  const filteredContents = useMemo(() => {
    const normalizedKeyword = keyword.trim().toLowerCase();

    return lifeLawContents.filter((content) => {
      const categoryMatched =
        selectedCategory === "all" || content.categoryId === selectedCategory;

      const keywordMatched =
        !normalizedKeyword ||
        content.title.toLowerCase().includes(normalizedKeyword) ||
        content.summary.toLowerCase().includes(normalizedKeyword) ||
        content.category.toLowerCase().includes(normalizedKeyword);

      return categoryMatched && keywordMatched;
    });
  }, [keyword, selectedCategory]);

  const handleSearch = (event) => {
    event.preventDefault();
  };

  return (
    <div className="app">
      <Header onMenuOpen={() => setMenuOpen(true)} />

      <HamburgerMenu isOpen={menuOpen} onClose={() => setMenuOpen(false)} />

      <main className="life-law-page">
        <section className="life-law-hero">
          <div className="life-law-hero-inner">
            <div className="life-law-hero-content">
              <h1>생활법률</h1>

              <p>
                일상생활에서 꼭 알아야 할 법률 정보를
                <br className="mobile-line-break" />
                쉽고 친절하게 알려드립니다.
              </p>

              <form className="life-law-search-form" onSubmit={handleSearch}>
                <input
                  type="search"
                  value={keyword}
                  placeholder="궁금한 생활법률을 검색해보세요"
                  aria-label="생활법률 검색"
                  onChange={(event) => setKeyword(event.target.value)}
                />

                <button type="submit" aria-label="검색">
                  <FiSearch />
                </button>
              </form>
            </div>

            <div className="life-law-hero-visual" aria-hidden="true">
              <img src={lifeLawIllustration} alt="" />
            </div>
          </div>
        </section>

        <section className="life-law-category-section">
          <div className="life-law-container">
            <div className="life-law-category-grid">
              {categories.map(({ id, title, description, icon: Icon }) => (
                <button
                  key={id}
                  type="button"
                  className={`life-law-category-card ${
                    selectedCategory === id ? "active" : ""
                  }`}
                  onClick={() =>
                    setSelectedCategory((currentCategory) =>
                      currentCategory === id ? "all" : id,
                    )
                  }
                >
                  <span className={`life-law-category-icon ${id}`}>
                    <Icon />
                  </span>

                  <strong>{title}</strong>
                  <small>{description}</small>
                </button>
              ))}
            </div>
          </div>
        </section>

        <section className="life-law-main-section">
          <div className="life-law-container life-law-layout">
            <div className="life-law-content-panel">
              <div className="life-law-tabs">
                <button
                  type="button"
                  className={selectedTab === "all" ? "active" : ""}
                  onClick={() => setSelectedTab("all")}
                >
                  전체
                </button>

                <button
                  type="button"
                  className={selectedTab === "question" ? "active" : ""}
                  onClick={() => setSelectedTab("question")}
                >
                  자주 찾는 질문
                </button>

                <button
                  type="button"
                  className={selectedTab === "latest" ? "active" : ""}
                  onClick={() => setSelectedTab("latest")}
                >
                  최신 콘텐츠
                </button>
              </div>

              <div className="life-law-content-list">
                {filteredContents.length > 0 ? (
                  filteredContents.map(
                    ({ id, title, summary, category, views, icon: Icon }) => (
                      <Link
                        key={id}
                        className="life-law-content-item"
                        to={`/life-law/${id}`}
                      >
                        <span className="life-law-content-icon">
                          <Icon />
                        </span>

                        <div className="life-law-content-text">
                          <h2>{title}</h2>
                          <p>{summary}</p>
                        </div>

                        <div className="life-law-content-meta">
                          <span>{category}</span>

                          <small>
                            <FiEye />
                            {views}
                          </small>
                        </div>

                        <FiChevronRight className="life-law-content-arrow" />
                      </Link>
                    ),
                  )
                ) : (
                  <div className="life-law-empty">
                    <FiSearch />
                    <h2>검색 결과가 없습니다.</h2>
                    <p>다른 검색어 또는 분야를 선택해주세요.</p>
                  </div>
                )}
              </div>

              <button className="life-law-more-button" type="button">
                더보기
              </button>
            </div>

            <aside className="life-law-side-panel">
              <section className="life-law-side-card">
                <h2>많이 찾는 생활법률</h2>

                <ol className="popular-law-list">
                  {popularContents.map((content, index) => (
                    <li key={content}>
                      <span>{index + 1}</span>
                      <button type="button">{content}</button>
                    </li>
                  ))}
                </ol>
              </section>

              <section className="life-law-guide-card">
                <h2>생활법률 가이드</h2>

                <div className="guide-card-content">
                  <div>
                    <strong>생활법률 가이드북</strong>
                    <p>
                      일상에서 꼭 알아야 할
                      <br />
                      법률 상식을 모았습니다.
                    </p>

                    <button type="button">가이드북 다운로드</button>
                  </div>

                  <FiBookOpen />
                </div>
              </section>

              <section className="life-law-support-card">
                <div>
                  <h2>도움이 더 필요하신가요?</h2>
                  <p>대한법률구조공단에서 무료 법률 상담을 받아보세요.</p>

                  <button type="button">상담 신청하기</button>
                </div>

                <FiHeadphones />
              </section>
            </aside>
          </div>
        </section>
      </main>
    </div>
  );
}

export default LifeLawPage;
