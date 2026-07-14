import re
from dataclasses import dataclass


@dataclass
class ValidationResult:
    status: str
    warnings: list[str]


class LegalTextValidator:
    PATTERNS = {
        "금액": [r"\d{1,3}(?:,\d{3})*원", r"\d+만 원"],
        "날짜": [r"\d{4}년\s*\d{1,2}월\s*\d{1,2}일", r"\d{4}-\d{2}-\d{2}"],
        "비율": [r"연\s*\d+%", r"\d+%"],
        "법률 조항": [r"제\d+조"],
        "사건번호": [r"샘플-사건번호-\d+"],
    }

    def extract_protected_values(self, text: str) -> dict[str, list[str]]:
        values: dict[str, list[str]] = {}
        for label, patterns in self.PATTERNS.items():
            found: list[str] = []
            for pattern in patterns:
                found.extend(re.findall(pattern, text))
            values[label] = sorted(set(found))
        return values

    def validate(self, original: str, simplified: str) -> ValidationResult:
        warnings: list[str] = []
        original_values = self.extract_protected_values(original)
        simplified_values = self.extract_protected_values(simplified)
        for label, values in original_values.items():
            for value in values:
                if value not in simplified_values.get(label, []):
                    warnings.append(f"원문과 쉬운 설명의 {label}이 일치하지 않습니다: {value}")

        if self._party_direction(original) and self._party_direction(simplified):
            if self._party_direction(original) != self._party_direction(simplified):
                warnings.append("원고와 피고의 역할 또는 의무 방향이 바뀌었습니다.")

        for term in ["기각", "각하", "인용"]:
            if term in original and term not in simplified:
                warnings.append(f"판결 결과 표현이 보존되지 않았습니다: {term}")

        if ("아니" in original or "않" in original or "못" in original) and not (
            "아니" in simplified or "않" in simplified or "못" in simplified
        ):
            warnings.append("부정 표현이 쉬운 설명에서 사라졌을 수 있습니다.")

        return ValidationResult(status="review_required" if warnings else "passed", warnings=warnings)

    def _party_direction(self, text: str) -> str:
        if "피고는 원고에게" in text:
            return "defendant_to_plaintiff"
        if "원고는 피고에게" in text:
            return "plaintiff_to_defendant"
        return ""
