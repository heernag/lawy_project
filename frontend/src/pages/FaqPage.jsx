import "../styles/faq.css";
import { useState } from "react";
import { FiChevronDown, FiHelpCircle } from "react-icons/fi";
import Header from "../components/Header.jsx";
import HamburgerMenu from "../components/HamburgerMenu.jsx";
const faqs=[{q:"AI 판례 요약은 법률 상담을 대신하나요?",a:"아니요. AI 요약은 판례 이해를 돕기 위한 참고 정보이며 구체적인 사건은 전문가 상담이 필요합니다."},{q:"판례를 저장하려면 로그인이 필요한가요?",a:"현재 화면은 프론트엔드 데모이며, 추후 로그인 기능과 함께 저장 데이터가 계정에 연결됩니다."},{q:"사건번호로도 검색할 수 있나요?",a:"판례검색 화면에서 사건명, 키워드, 사건번호를 모두 검색할 수 있도록 구성했습니다."}];
function FaqPage(){const[menuOpen,setMenuOpen]=useState(false);const[open,setOpen]=useState(0);return <div className="app"><Header onMenuOpen={()=>setMenuOpen(true)}/><HamburgerMenu isOpen={menuOpen} onClose={()=>setMenuOpen(false)}/><main className="simple-page"><div className="content-container narrow"><div className="simple-page-heading"><span><FiHelpCircle/></span><div><h1>자주 묻는 질문</h1><p>서비스 이용 중 궁금한 내용을 확인하세요.</p></div></div><section className="faq-list">{faqs.map((item,index)=><article className={open===index?"faq-item open":"faq-item"} key={item.q}><button type="button" onClick={()=>setOpen(open===index?-1:index)}><strong>Q. {item.q}</strong><FiChevronDown/></button>{open===index&&<p>{item.a}</p>}</article>)}</section></div></main></div>}
export default FaqPage;
