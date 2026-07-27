import "../styles/settings.css";
import { useState } from "react";
import { FiMoon, FiSettings, FiBell } from "react-icons/fi";
import Header from "../components/Header.jsx";
import HamburgerMenu from "../components/HamburgerMenu.jsx";
function SettingsPage(){const[menuOpen,setMenuOpen]=useState(false);const[alerts,setAlerts]=useState(true);const[dark,setDark]=useState(false);return <div className="app"><Header onMenuOpen={()=>setMenuOpen(true)}/><HamburgerMenu isOpen={menuOpen} onClose={()=>setMenuOpen(false)}/><main className="simple-page"><div className="content-container narrow"><div className="simple-page-heading"><span><FiSettings/></span><div><h1>설정</h1><p>알림과 화면 설정을 관리합니다.</p></div></div><section className="settings-card"><div className="setting-row"><span><FiBell/></span><div><strong>서비스 알림</strong><p>공지사항과 저장한 판례 업데이트 알림</p></div><button type="button" className={alerts?"toggle active":"toggle"} onClick={()=>setAlerts(!alerts)}><span/></button></div><div className="setting-row"><span><FiMoon/></span><div><strong>다크 모드</strong><p>어두운 화면 테마 사용 예정</p></div><button type="button" className={dark?"toggle active":"toggle"} onClick={()=>setDark(!dark)}><span/></button></div></section></div></main></div>}
export default SettingsPage;
