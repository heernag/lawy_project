import "../styles/header.css";
import { NavLink } from "react-router-dom";
import {
  FiBookmark,
  FiClock,
  FiBell,
  FiHelpCircle,
  FiHeadphones,
  FiSettings,
  FiX,
} from "react-icons/fi";

const menuItems = [
  { to: "/saved-cases", label: "저장한 판례", icon: FiBookmark },
  { to: "/recent-cases", label: "최근 본 판례", icon: FiClock },
  { to: "/notices", label: "공지사항", icon: FiBell },
  { to: "/faq", label: "자주 묻는 질문", icon: FiHelpCircle },
  { to: "/customer-service", label: "고객센터", icon: FiHeadphones },
  { to: "/settings", label: "설정", icon: FiSettings },
];

function HamburgerMenu({ isOpen, onClose }) {
  if (!isOpen) return null;

  return (
    <div
      className="menu-overlay"
      role="presentation"
      onClick={onClose}
    >
      <aside
        className="side-menu"
        aria-label="부가 메뉴"
        onClick={(event) => event.stopPropagation()}
      >
        <div className="side-menu-header">
          <strong>메뉴</strong>
          <button
            type="button"
            className="close-button"
            aria-label="메뉴 닫기"
            onClick={onClose}
          >
            <FiX />
          </button>
        </div>

        <nav className="side-menu-nav">
          {menuItems.map(({ to, label, icon: Icon }) => (
            <NavLink key={to} to={to} onClick={onClose}>
              <Icon />
              <span>{label}</span>
            </NavLink>
          ))}
        </nav>
      </aside>
    </div>
  );
}

export default HamburgerMenu;
