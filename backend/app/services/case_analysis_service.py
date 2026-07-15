import re

from app.schemas.case_analysis import CaseAnalysisResult, InputWarning, PrivacyDetection


PRIVACY_PATTERNS: tuple[tuple[str, str, str, re.Pattern[str]], ...] = (
    (
        "resident_registration_number",
        "주민등록번호",
        "RRN",
        re.compile(r"\d{6}-\d{7}"),
    ),
    (
        "phone_number",
        "전화번호",
        "PHONE",
        re.compile(r"01[016789]-?\d{3,4}-?\d{4}"),
    ),
    (
        "email",
        "이메일",
        "EMAIL",
        re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    ),
    (
        "address",
        "주소",
        "ADDRESS",
        re.compile(
            r"[가-힣]+(?:특별시|광역시|특별자치시|특별자치도|도|시)\s+"
            r"[가-힣]+(?:시|군|구)\s+"
            r"[가-힣0-9]+(?:로|길)\s+\d+(?:-\d+)?"
        ),
    ),
)

PROMPT_INJECTION_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"ignore\s+(all\s+)?previous\s+instructions", re.IGNORECASE),
    re.compile(r"disregard\s+(all\s+)?previous\s+instructions", re.IGNORECASE),
    re.compile(r"system\s+prompt", re.IGNORECASE),
    re.compile(r"developer\s+message", re.IGNORECASE),
    re.compile(r"이전\s*지시(?:를|사항을)?\s*무시", re.IGNORECASE),
)


class CaseAnalysisService:
    def analyze(self, query: str) -> CaseAnalysisResult:
        normalized = query.strip()
        sanitized_query, privacy_detections = self._mask_privacy_values(normalized)
        category, sub_category = self._classify(normalized)
        return CaseAnalysisResult(
            category=category,
            sub_category=sub_category,
            sanitized_query=sanitized_query,
            parties=self._extract_parties(normalized),
            dispute_target=self._extract_dispute_target(normalized),
            facts=self._extract_facts(normalized),
            legal_issues=self._extract_legal_issues(normalized, sub_category),
            search_keywords=self._extract_keywords(normalized, sub_category),
            legal_terms=self._extract_legal_terms(normalized, sub_category),
            privacy_detections=privacy_detections,
            privacy_warnings=self._privacy_warnings(normalized),
            input_warnings=self._input_warnings(normalized),
        )

    def _mask_privacy_values(self, query: str) -> tuple[str, list[PrivacyDetection]]:
        sanitized = query
        detections: list[PrivacyDetection] = []
        counters: dict[str, int] = {}

        for detection_type, label, token_prefix, pattern in PRIVACY_PATTERNS:
            def replace(match: re.Match[str]) -> str:
                counters[token_prefix] = counters.get(token_prefix, 0) + 1
                masked_value = f"[{token_prefix}_{counters[token_prefix]}]"
                detections.append(
                    PrivacyDetection(
                        type=detection_type,
                        label=label,
                        masked_value=masked_value,
                    )
                )
                return masked_value

            sanitized = pattern.sub(replace, sanitized)

        return sanitized, detections

    def _input_warnings(self, query: str) -> list[InputWarning]:
        if any(pattern.search(query) for pattern in PROMPT_INJECTION_PATTERNS):
            return [
                InputWarning(
                    type="prompt_injection_suspected",
                    message=(
                        "입력문에 시스템 지시를 바꾸려는 문구와 비슷한 표현이 있어 "
                        "사건 사실 분석에만 사용합니다."
                    ),
                )
            ]
        return []

    def _classify(self, query: str) -> tuple[str, str]:
        if any(keyword in query for keyword in ["해고", "임금", "퇴직금"]):
            return "노동", "근로계약"
        if any(keyword in query for keyword in ["전세", "보증금", "임대차"]):
            return "민사", "임대차"
        if any(keyword in query for keyword in ["중고", "구매", "환불", "하자", "고장"]):
            return "민사", "매매계약"
        if any(keyword in query for keyword in ["교통사고", "과실"]):
            return "민사", "손해배상"
        if any(keyword in query for keyword in ["댓글", "모욕", "명예훼손"]):
            return "형사", "모욕"
        return "기타", "일반"

    def _extract_parties(self, query: str) -> list[str]:
        parties: list[str] = []
        if any(keyword in query for keyword in ["구매", "중고", "환불"]):
            parties.extend(["구매자", "판매자"])
        if any(keyword in query for keyword in ["전세", "보증금", "임대차"]):
            parties.extend(["임차인", "임대인"])
        if any(keyword in query for keyword in ["해고", "임금", "퇴직금"]):
            parties.extend(["근로자", "사용자"])
        return list(dict.fromkeys(parties))

    def _extract_dispute_target(self, query: str) -> str:
        if "노트북" in query:
            return "중고 노트북"
        if "보증금" in query:
            return "전세 보증금"
        if "임금" in query:
            return "임금"
        return ""

    def _extract_facts(self, query: str) -> list[str]:
        facts: list[str] = []
        if "정상" in query:
            facts.append("정상 제품이라고 설명받음")
        if any(keyword in query for keyword in ["고장", "켜지지"]):
            facts.append("제품에 고장 또는 작동 문제가 있음")
        if "환불" in query and "거부" in query:
            facts.append("상대방이 환불을 거부함")
        if "보증금" in query and any(keyword in query for keyword in ["돌려받지", "반환"]):
            facts.append("보증금을 돌려받지 못함")
        if "해고" in query:
            facts.append("해고를 당했다고 주장함")
        if "임금" in query and any(keyword in query for keyword in ["못", "미지급", "지급받지"]):
            facts.append("임금을 지급받지 못함")
        return facts

    def _extract_legal_issues(self, query: str, sub_category: str) -> list[str]:
        if sub_category == "매매계약":
            return ["매매 목적물의 하자", "계약 해제", "손해배상"]
        if sub_category == "임대차":
            return ["임대차계약 종료", "보증금 반환"]
        if sub_category == "근로계약":
            return ["임금 지급", "근로계약상 의무"]
        if sub_category == "손해배상":
            return ["불법행위", "손해배상"]
        if sub_category == "모욕":
            return ["모욕", "명예훼손"]
        return []

    def _extract_keywords(self, query: str, sub_category: str) -> list[str]:
        candidates = ["중고", "노트북", "하자", "고장", "환불", "거부", "전세", "보증금", "임금", "해고", "교통사고", "모욕"]
        keywords = [keyword for keyword in candidates if keyword in query]
        if sub_category and sub_category != "일반":
            keywords.append(sub_category)
        return list(dict.fromkeys(keywords))

    def _extract_legal_terms(self, query: str, sub_category: str) -> list[str]:
        mapping = {
            "매매계약": ["계약 해제", "손해배상", "하자담보책임"],
            "임대차": ["임대차", "보증금 반환"],
            "근로계약": ["임금", "채무불이행"],
            "손해배상": ["불법행위", "손해배상"],
            "모욕": ["모욕", "명예훼손"],
        }
        return mapping.get(sub_category, [])

    def _privacy_warnings(self, query: str) -> list[str]:
        warnings: list[str] = []
        if re.search(r"01[016789]-?\d{3,4}-?\d{4}", query):
            warnings.append("전화번호로 보이는 개인정보가 포함되어 있습니다.")
        if re.search(r"\d{6}-\d{7}", query):
            warnings.append("주민등록번호 형식으로 보이는 민감정보가 포함되어 있습니다.")
        return warnings
