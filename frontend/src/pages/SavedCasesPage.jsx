import "../styles/saved-cases.css";
import { useState } from "react";
import { Link } from "react-router-dom";
import { FiBookmark, FiChevronRight } from "react-icons/fi";
import Header from "../components/Header.jsx";
import HamburgerMenu from "../components/HamburgerMenu.jsx";

const savedCases = [
  { id: "2024다12345", title: "임대차보증금 반환", court: "대법원", date: "2025.03.14", category: "민사" },
  { id: "2024나24680", title: "교통사고 손해배상 청구", court: "서울고등법원", date: "2025.02.28", category: "민사" },
];

function SavedCasesPage() {
  const [menuOpen, setMenuOpen] = useState(false);
  const [items, setItems] = useState(savedCases);
  return <div className="app"><Header onMenuOpen={() => setMenuOpen(true)} /><HamburgerMenu isOpen={menuOpen} onClose={() => setMenuOpen(false)} />
    <main className="simple-page"><div className="content-container"><div className="simple-page-heading"><span><FiBookmark /></span><div><h1>저장한 판례</h1><p>관심 있는 판례를 모아서 확인할 수 있습니다.</p></div></div>
      <section className="list-card">{items.length ? items.map((item) => <article className="compact-case-item" key={item.id}><Link to={`/cases/${item.id}`}><span className="category-badge">{item.category}</span><div><h2>{item.title}</h2><p>{item.court} · {item.id} · {item.date}</p></div><FiChevronRight /></Link><button type="button" onClick={() => setItems((current) => current.filter((value) => value.id !== item.id))}>삭제</button></article>) : <div className="empty-state"><FiBookmark /><h2>저장한 판례가 없습니다.</h2><Link to="/cases">판례 찾아보기</Link></div>}</section>
    </div></main></div>;
}
export default SavedCasesPage;
