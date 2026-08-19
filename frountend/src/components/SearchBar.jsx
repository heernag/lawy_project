import "../styles/home.css";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { FiSearch } from "react-icons/fi";

function SearchBar() {
  const [keyword, setKeyword] = useState("");
  const navigate = useNavigate();

  const handleSubmit = (event) => {
    event.preventDefault();
    const trimmedKeyword = keyword.trim();

    if (trimmedKeyword.length < 2) {
      alert("검색어를 2자 이상 입력해주세요.");
      return;
    }

    navigate(`/cases?q=${encodeURIComponent(trimmedKeyword)}`);
  };

  return (
    <form className="search-box" onSubmit={handleSubmit}>
      <input
        type="search"
        value={keyword}
        placeholder="사건명, 키워드, 사건번호를 입력하세요"
        aria-label="판례 검색어"
        onChange={(event) => setKeyword(event.target.value)}
      />
      <button type="submit" aria-label="판례 검색">
        <FiSearch />
      </button>
    </form>
  );
}

export default SearchBar;
