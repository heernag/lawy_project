import "../styles/home.css";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {
  FiBookOpen,
  FiBriefcase,
  FiCheckCircle,
  FiClock,
  FiDollarSign,
  FiFileText,
  FiHeart,
  FiHome,
  FiMapPin,
  FiMessageSquare,
  FiShare2,
  FiTruck,
  FiUsers,
} from "react-icons/fi";

import Header from "../components/Header.jsx";
import HamburgerMenu from "../components/HamburgerMenu.jsx";
import SearchBar from "../components/SearchBar.jsx";
import headerIllustration from "../assets/header_img.png";
import maleJudgeIllustration from "../assets/malejudge.svg";

const serviceFeatures = [
  {
    title: "판례 핵심 요약",
    description: "긴 판례에서 사건 배경과 핵심 쟁점을 정리해 보여줍니다.",
    icon: <FiFileText />,
  },
  {
    title: "쉬운 판례 설명",
    description: "주문과 법원의 판단을 이해하기 쉬운 표현으로 확인할 수 있어요.",
    icon: <FiBookOpen />,
  },
  {
    title: "전문 용어 풀이",
    description: "판례에 등장하는 법률 용어의 쉬운 뜻을 확인할 수 있습니다.",
    icon: <FiCheckCircle />,
  },
  {
    title: "저장 및 공유",
    description: "중요한 판례를 저장하고 현재 페이지 주소를 공유할 수 있습니다.",
    icon: <FiShare2 />,
  },
];

const categories = [
  { title: "임대차", description: "전세, 월세, 보증금", icon: FiHome },
  { title: "교통사고", description: "사고, 보험, 과실", icon: FiTruck },
  { title: "손해배상", description: "배상, 위자료, 청구", icon: FiDollarSign },
  { title: "이혼", description: "재산분할, 양육권", icon: FiHeart },
  { title: "근로계약", description: "해고, 임금, 근로조건", icon: FiBriefcase },
  { title: "상속", description: "유류분, 상속포기", icon: FiUsers },
  { title: "계약", description: "계약체결, 해지, 분쟁", icon: FiFileText },
  { title: "소송", description: "소송절차, 증거, 판결", icon: FiBookOpen },
];

function formatDate(dateString) {
  if (!dateString) return "선고일 미상";
  return dateString.replaceAll("-", ".");
}

function HomePage() {
  const [menuOpen, setMenuOpen] = useState(false);
  const [recentCases, setRecentCases] = useState([]);

  useEffect(() => {
    try {
      const stored = JSON.parse(localStorage.getItem("casefinder-recent-cases") || "[]");
      setRecentCases(Array.isArray(stored) ? stored.slice(0, 4) : []);
    } catch {
      setRecentCases([]);
    }
  }, []);

  return (
    <div className="app">
      <Header onMenuOpen={() => setMenuOpen(true)} />
      <HamburgerMenu isOpen={menuOpen} onClose={() => setMenuOpen(false)} />

      <main>
        <section className="hero-section">
          <div className="hero-inner">
            <div className="hero-content">
              <p className="hero-label">CASE FINDER</p>
              <h1>
                판례문을
                <br />
                찾아 드립니다
              </h1>
              <p className="hero-description">
                판례 검색부터 핵심 요약, 쉬운 설명, 법률용어 확인까지 한곳에서 이용하세요.
              </p>

              <SearchBar />

              <div className="quick-actions">
                <Link className="quick-action-card" to="/cases?mode=analyze">
                  <span className="quick-action-icon"><FiMessageSquare /></span>
                  <span>
                    <strong>내 상황으로 판례 찾기</strong>
                    <small>상황을 설명하면 핵심 쟁점과 추천 검색어를 정리합니다.</small>
                  </span>
                </Link>

                <Link className="quick-action-card" to="/court-map">
                  <span className="quick-action-icon"><FiMapPin /></span>
                  <span>
                    <strong>법원 위치 찾기</strong>
                    <small>법원 찾기 화면에서 위치 정보를 확인하세요.</small>
                  </span>
                </Link>
              </div>
            </div>

            <div className="home-hero-visual" aria-hidden="true">
              <img className="home-hero-symbols" src={headerIllustration} alt="" />
              <img className="home-hero-judge" src={maleJudgeIllustration} alt="" />
            </div>
          </div>
        </section>

        <section className="content-section" id="life-law">
          <div className="section-inner">
            <div className="section-heading">
              <h2>자주 찾는 생활 법률</h2>
              <Link to="/life-law">더보기 ›</Link>
            </div>

            <div className="category-grid">
              {categories.map(({ title, description, icon: Icon }) => (
                <Link
                  className="category-card"
                  to={`/life-law?category=${encodeURIComponent(title)}`}
                  key={title}
                >
                  <span className="category-icon"><Icon /></span>
                  <strong>{title}</strong>
                  <small>{description}</small>
                </Link>
              ))}
            </div>
          </div>
        </section>

        <section className="recent-case-section">
          <div className="section-inner">
            <div className="section-heading">
              <h2>최근 본 판례</h2>
              <Link to="/recent-cases">전체보기 ›</Link>
            </div>

            {recentCases.length > 0 ? (
              <div className="recent-case-grid">
                {recentCases.map((caseItem) => (
                  <Link
                    key={caseItem.case_id}
                    className="recent-case-card"
                    to={`/cases/${caseItem.case_id}`}
                  >
                    <span className="recent-case-category">판례</span>
                    <h3>{caseItem.case_name || "판례 상세"}</h3>
                    <div className="recent-case-meta">
                      <span>{caseItem.court_name || "법원 정보 없음"}</span>
                      <span>{formatDate(caseItem.decision_date)}</span>
                    </div>
                    <p className="recent-case-number">{caseItem.case_number || caseItem.case_id}</p>
                  </Link>
                ))}
              </div>
            ) : (
              <div className="home-recent-empty">
                <FiClock />
                <div>
                  <strong>아직 최근 본 판례가 없습니다.</strong>
                  <p>판례를 검색하고 상세 페이지를 열면 여기에 자동으로 표시됩니다.</p>
                </div>
                <Link to="/cases">판례 검색</Link>
              </div>
            )}
          </div>
        </section>

        <section className="service-feature-section">
          <div className="section-inner service-feature-grid">
            {serviceFeatures.map((feature) => (
              <article className="service-feature-item" key={feature.title}>
                <span className="service-feature-icon">{feature.icon}</span>
                <div>
                  <h3>{feature.title}</h3>
                  <p>{feature.description}</p>
                </div>
              </article>
            ))}
          </div>
        </section>

        <footer className="footer">
          <p>본 서비스는 일반적인 정보 제공을 목적으로 하며, 법률적 조언을 대체하지 않습니다.</p>
        </footer>
      </main>
    </div>
  );
}

export default HomePage;
