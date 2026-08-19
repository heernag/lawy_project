import "../styles/header.css";
import { NavLink } from "react-router-dom";
import {
  FiBell,
  FiBookmark,
  FiBookOpen,
  FiClock,
  FiHeadphones,
  FiHelpCircle,
  FiHome,
  FiMapPin,
  FiMessageSquare,
  FiSearch,
  FiSettings,
  FiUsers,
  FiX,
} from "react-icons/fi";

const primaryItems = [
  { to: "/", label: "홈", icon: FiHome },
  { to: "/cases", label: "판례검색", icon: FiSearch },
  { to: "/life-law", label: "생활법률", icon: FiBookOpen },
  { to: "/legal-terms", label: "법용어", icon: FiMessageSquare },
  { to: "/court-map", label: "법원 찾기", icon: FiMapPin },
  { to: "/community", label: "커뮤니티", icon: FiUsers },
];

const secondaryItems = [
  { to: "/saved-cases", label: "저장한 판례", icon: FiBookmark },
  { to: "/recent-cases", label: "최근 본 판례", icon: FiClock },
  { to: "/notices", label: "공지사항", icon: FiBell },
  { to: "/faq", label: "자주 묻는 질문", icon: FiHelpCircle },
  { to: "/customer-service", label: "고객센터", icon: FiHeadphones },
  { to: "/settings", label: "설정", icon: FiSettings },
];

function MenuGroup({ title, items, onClose }) {
  return (
    <div className="side-menu-group">
      <span className="side-menu-label">{title}</span>
      <nav className="side-menu-nav">
        {items.map(({ to, label, icon: Icon }) => (
          <NavLink key={to} to={to} onClick={onClose}>
            <Icon />
            <span>{label}</span>
          </NavLink>
        ))}
      </nav>
    </div>
  );
}

function HamburgerMenu({ isOpen, onClose }) {
  if (!isOpen) return null;

  return (
    <div className="menu-overlay" role="presentation" onClick={onClose}>
      <aside
        className="side-menu"
        aria-label="전체 메뉴"
        onClick={(event) => event.stopPropagation()}
      >
        <div className="side-menu-header">
          <strong>CaseFinder</strong>
          <button type="button" className="close-button" aria-label="메뉴 닫기" onClick={onClose}>
            <FiX />
          </button>
        </div>

        <div className="side-menu-scroll">
          <MenuGroup title="주요 메뉴" items={primaryItems} onClose={onClose} />
          <MenuGroup title="내 메뉴" items={secondaryItems} onClose={onClose} />
        </div>
      </aside>
    </div>
  );
}

export default HamburgerMenu;
