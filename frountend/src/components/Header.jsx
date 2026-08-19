import "../styles/header.css";
import { NavLink } from "react-router-dom";
import { FiMenu, FiUser } from "react-icons/fi";

import scaleIcon from "../assets/scales.svg";

function Header({ onMenuOpen }) {
  return (
    <header className="header">
      <div className="header-inner">
        <NavLink className="logo-button" to="/" aria-label="CaseFinder 홈">
          <span className="scale-icon" aria-hidden="true">
            <img src={scaleIcon} alt="" />
          </span>
          <span className="logo-text logo-text-desktop">판례문을 찾아 드립니다</span>
          <span className="logo-text logo-text-mobile">CaseFinder</span>
        </NavLink>

        <nav className="desktop-nav" aria-label="주요 메뉴">
          <NavLink to="/">홈</NavLink>
          <NavLink to="/cases">판례검색</NavLink>
          <NavLink to="/life-law">생활법률</NavLink>
          <NavLink to="/legal-terms">법용어</NavLink>
          <NavLink to="/court-map">법원 찾기</NavLink>
          <NavLink to="/community">커뮤니티</NavLink>
        </nav>

        <div className="header-actions">
          <button className="icon-button user-button" type="button" aria-label="사용자 메뉴">
            <FiUser />
          </button>

          <button
            className="icon-button menu-button"
            type="button"
            aria-label="메뉴 열기"
            onClick={onMenuOpen}
          >
            <FiMenu />
          </button>
        </div>
      </div>
    </header>
  );
}

export default Header;
