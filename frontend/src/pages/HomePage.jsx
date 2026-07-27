import "../styles/home.css";
import { useState } from "react";
import { Link } from "react-router-dom";
import {
  FiCamera,
  FiMapPin,
  FiHome,
  FiTruck,
  FiDollarSign,
  FiHeart,
  FiBriefcase,
  FiUsers,
  FiFileText,
  FiBookOpen,
  FiCheckCircle,
  FiShare2,
} from "react-icons/fi";


import Header from "../components/Header.jsx";
import HamburgerMenu from "../components/HamburgerMenu.jsx";
import SearchBar from "../components/SearchBar.jsx";
import headerIllustration from "../assets/header_img.png";
import maleJudgeIllustration from "../assets/malejudge.svg";

const recentCases = [
  {
    category: "민사",
    title: "임대차보증금 반환",
    court: "대법원",
    date: "2025.03.14",
    caseNumber: "2024다12345",
    summary: "계약 종료 후 임대인이 보증금을 반환하지 않아 발생한 사건...",
  },
  {
    category: "형사",
    title: "사기죄 성립 여부",
    court: "대법원",
    date: "2025.03.07",
    caseNumber: "2024도6789",
    summary: "피고인이 투자금을 편취할 목적으로 거짓말을 하였는지 여부가 쟁점...",
  },
  {
    category: "민사",
    title: "손해배상 청구",
    court: "서울고등법원",
    date: "2025.02.28",
    caseNumber: "2024나24680",
    summary: "교통사고로 인한 손해배상 청구 사건에서 과실 비율이 쟁점...",
  },
  {
    category: "행정",
    title: "과징금 부과 처분 취소",
    court: "대법원",
    date: "2025.02.20",
    caseNumber: "2024두13579",
    summary: "공정거래위원회의 과징금 부과 처분의 적법성 여부가 쟁점...",
  },
];

const serviceFeatures = [
  {
    title: "AI 요약·해석",
    description: "복잡한 판례를 쉽게 요약해 드립니다.",
    icon: <FiFileText />,
  },
  {
    title: "관련 법령 연결",
    description: "관련 법령과 조문을 함께 확인할 수 있어요.",
    icon: <FiBookOpen />,
  },
  {
    title: "전문 용어 풀이",
    description: "어려운 법률 용어를 쉽게 설명해 드립니다.",
    icon: <FiCheckCircle />,
  },
  {
    title: "저장 및 공유",
    description: "중요한 판례를 저장하고 공유할 수 있습니다.",
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
  { title: "법률조언", description: "법률상담, 조언, 대리", icon: FiCheckCircle },
  { title: "공유물", description: "공유물 분할, 관리", icon: FiShare2 },
];

function HomePage() {
  const [menuOpen, setMenuOpen] = useState(false);

  const handleImageUpload = (event) => {
    const file = event.target.files?.[0];
    if (!file) return;
    alert(`${file.name} 파일이 선택되었습니다.`);
  };

  return (
    <div className="app">
      <Header onMenuOpen={() => setMenuOpen(true)} />
      <HamburgerMenu
        isOpen={menuOpen}
        onClose={() => setMenuOpen(false)}
      />

      <main>
        <section className="hero-section">
          <div className="hero-inner">
            <div className="hero-content">
              <p className="hero-label">AI LEGAL CASE FINDER</p>
              <h1>
                판례문을
                <br />
                찾아 드립니다
              </h1>
              <p className="hero-description">
                어려운 판례도 AI가 쉽고 정확하게 요약·해석해 드립니다.
              </p>

              <SearchBar />

              <div className="quick-actions">
                <label className="quick-action-card upload-card">
                  <span className="quick-action-icon">
                    <FiCamera />
                  </span>
                  <span>
                    <strong>이미지로 검색</strong>
                    <small>판결문이나 사진을 올려 관련 판례를 찾아보세요.</small>
                  </span>
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleImageUpload}
                  />
                </label>

                <Link className="quick-action-card" to="/court-map">
                  <span className="quick-action-icon">
                    <FiMapPin />
                  </span>
                  <span>
                    <strong>법원 위치 찾기</strong>
                    <small>전국 법원의 위치와 교통정보를 확인하세요.</small>
                  </span>
                </Link>
              </div>
            </div>

            <div className="home-hero-visual" aria-hidden="true">
              <img
                className="home-hero-symbols"
                src={headerIllustration}
                alt=""
              />
              <img
                className="home-hero-judge"
                src={maleJudgeIllustration}
                alt=""
              />
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
                  <span className="category-icon">
                    <Icon />
                  </span>
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
              <h2>최근 주요 판례</h2>
              <Link to="/cases">더보기 ›</Link>
            </div>
        
            <div className="recent-case-grid">
              {recentCases.map((caseItem) => (
                <Link
                  key={caseItem.caseNumber}
                  className="recent-case-card"
                  to={`/cases/${caseItem.caseNumber}`}
                >
                  <span
                    className={`recent-case-category ${caseItem.category}`}
                  >
                    {caseItem.category}
                  </span>
        
                  <h3>{caseItem.title}</h3>
        
                  <div className="recent-case-meta">
                    <span>{caseItem.court}</span>
                    <span>{caseItem.date}</span>
                  </div>
        
                  <p className="recent-case-number">
                    {caseItem.caseNumber}
                  </p>
        
                  <p className="recent-case-summary">
                    {caseItem.summary}
                  </p>
                </Link>
              ))}
            </div>
          </div>
        </section>
        
        <section className="service-feature-section">
          <div className="section-inner service-feature-grid">
            {serviceFeatures.map((feature) => (
              <article className="service-feature-item" key={feature.title}>
                <span className="service-feature-icon">
                  {feature.icon}
                </span>
        
                <div>
                  <h3>{feature.title}</h3>
                  <p>{feature.description}</p>
                </div>
              </article>
            ))}
          </div>
        </section>
        
        <footer className="footer">
          <p>
            본 서비스는 일반적인 정보 제공을 목적으로 하며,
            법률적 조언을 대체하지 않습니다.
          </p>
        </footer>
      </main>
    </div>
  );
}

export default HomePage;
