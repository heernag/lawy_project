import "../styles/case-detail.css";
import { useState } from "react";
import { Link, useParams } from "react-router-dom";
import { FiArrowLeft, FiBookmark, FiFileText, FiShare2 } from "react-icons/fi";
import Header from "../components/Header.jsx";
import HamburgerMenu from "../components/HamburgerMenu.jsx";

const caseDetails = {
  "2024다12345": {
    category: "민사",
    title: "임대차보증금 반환",
    court: "대법원",
    date: "2025.03.14",
    number: "2024다12345",
    issue: "임대차 계약 종료 후 임대인이 보증금을 반환하지 않은 경우 임차인이 보증금과 지연손해금을 청구할 수 있는지가 핵심 쟁점입니다.",
    result: "임대인은 계약 종료와 목적물 반환이 확인된 이후 보증금을 반환할 의무가 있다고 판단했습니다.",
  },
};

function CaseDetailPage() {
  const [menuOpen, setMenuOpen] = useState(false);
  const [saved, setSaved] = useState(false);
  const { caseId } = useParams();
  const detail = caseDetails[caseId] ?? {
    category: "판례",
    title: "판례 상세 정보",
    court: "법원",
    date: "확인 중",
    number: caseId,
    issue: "선택한 판례의 주요 쟁점과 사실관계를 정리하는 영역입니다.",
    result: "향후 판례 API가 연결되면 실제 판결 요지와 주문이 표시됩니다.",
  };

  return (
    <div className="app">
      <Header onMenuOpen={() => setMenuOpen(true)} />
      <HamburgerMenu isOpen={menuOpen} onClose={() => setMenuOpen(false)} />
      <main className="detail-page">
        <div className="content-container">
          <Link className="back-link" to="/cases"><FiArrowLeft /> 판례검색으로 돌아가기</Link>
          <section className="detail-hero-card">
            <div>
              <span className="category-badge">{detail.category}</span>
              <h1>{detail.title}</h1>
              <p>{detail.court} · {detail.number} · {detail.date}</p>
            </div>
            <div className="detail-actions">
              <button type="button" onClick={() => setSaved((value) => !value)} className={saved ? "active" : ""}><FiBookmark /> {saved ? "저장됨" : "저장"}</button>
              <button type="button"><FiShare2 /> 공유</button>
            </div>
          </section>
          <div className="detail-grid">
            <section className="detail-card ai-summary-card">
              <div className="detail-card-title"><FiFileText /><h2>AI 쉬운 요약</h2></div>
              <h3>무슨 사건인가요?</h3><p>{detail.issue}</p>
              <h3>법원은 어떻게 판단했나요?</h3><p>{detail.result}</p>
              <div className="notice-box">AI 요약은 이해를 돕기 위한 참고 정보이며 법률 자문을 대신하지 않습니다.</div>
            </section>
            <aside className="detail-card case-info-card">
              <h2>기본 정보</h2>
              <dl><div><dt>법원</dt><dd>{detail.court}</dd></div><div><dt>사건번호</dt><dd>{detail.number}</dd></div><div><dt>선고일</dt><dd>{detail.date}</dd></div><div><dt>사건분류</dt><dd>{detail.category}</dd></div></dl>
            </aside>
          </div>
        </div>
      </main>
    </div>
  );
}
export default CaseDetailPage;
