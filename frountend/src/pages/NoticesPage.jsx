import "../styles/notices.css";
import { useState } from "react";
import { FiBell, FiChevronRight } from "react-icons/fi";
import Header from "../components/Header.jsx";
import HamburgerMenu from "../components/HamburgerMenu.jsx";
const notices=[{id:1,title:"CaseFinder 서비스 베타 오픈 안내",date:"2026.07.27",important:true},{id:2,title:"판례 검색 기능 업데이트 안내",date:"2026.07.25"},{id:3,title:"개인정보 처리방침 개정 안내",date:"2026.07.20"}];
function NoticesPage(){const[menuOpen,setMenuOpen]=useState(false);return <div className="app"><Header onMenuOpen={()=>setMenuOpen(true)}/><HamburgerMenu isOpen={menuOpen} onClose={()=>setMenuOpen(false)}/><main className="simple-page"><div className="content-container"><div className="simple-page-heading"><span><FiBell/></span><div><h1>공지사항</h1><p>서비스 업데이트와 주요 안내를 확인합니다.</p></div></div><section className="list-card">{notices.map((item)=><button className="notice-item" key={item.id} type="button"><span>{item.important?"중요":"공지"}</span><strong>{item.title}</strong><small>{item.date}</small><FiChevronRight/></button>)}</section></div></main></div>}
export default NoticesPage;
