import "../styles/recent-cases.css";
import { useState } from "react";
import { Link } from "react-router-dom";
import { FiClock, FiChevronRight } from "react-icons/fi";
import Header from "../components/Header.jsx";
import HamburgerMenu from "../components/HamburgerMenu.jsx";
const recentCases = [
  { id: "2024다12345", title: "임대차보증금 반환", viewed: "오늘 10:32" },
  { id: "2024도6789", title: "사기죄 성립 여부", viewed: "어제 18:05" },
  { id: "2024두13579", title: "과징금 부과 처분 취소", viewed: "2026.07.25" },
];
function RecentCasesPage(){const[menuOpen,setMenuOpen]=useState(false);return <div className="app"><Header onMenuOpen={()=>setMenuOpen(true)}/><HamburgerMenu isOpen={menuOpen} onClose={()=>setMenuOpen(false)}/><main className="simple-page"><div className="content-container"><div className="simple-page-heading"><span><FiClock/></span><div><h1>최근 본 판례</h1><p>최근 열어본 판례 기록입니다.</p></div></div><section className="list-card">{recentCases.map((item)=><Link className="recent-item" to={`/cases/${item.id}`} key={item.id}><div><h2>{item.title}</h2><p>{item.id}</p></div><span>{item.viewed}</span><FiChevronRight/></Link>)}</section></div></main></div>}
export default RecentCasesPage;
