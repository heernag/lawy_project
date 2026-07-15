from pathlib import Path
from typing import Any

from app.providers.sample_case_provider import SampleCaseProvider


class LegalTermService:
    GLOSSARY: dict[str, dict[str, str]] = {
        "원고": {"easy_definition": "소송을 제기한 사람입니다.", "example": "원고가 손해배상을 청구한다.", "caution": "항상 이기는 사람이라는 뜻은 아닙니다."},
        "피고": {"easy_definition": "소송을 당한 상대방입니다.", "example": "피고는 청구를 부인한다.", "caution": "형사사건의 피고인과 구분됩니다."},
        "기각": {"easy_definition": "법원이 청구를 검토했지만 받아들이지 않는다는 뜻입니다.", "example": "원고의 청구를 기각한다.", "caution": "기각과 각하는 의미가 다릅니다."},
        "각하": {"easy_definition": "요건을 갖추지 못해 내용을 본격적으로 판단하지 않고 끝내는 것입니다.", "example": "소를 각하한다.", "caution": "청구 내용이 틀렸다는 판단과 다를 수 있습니다."},
        "인용": {"easy_definition": "법원이 청구를 받아들인다는 뜻입니다.", "example": "원고의 청구를 인용한다.", "caution": "일부만 받아들여질 수도 있습니다."},
        "항소": {"easy_definition": "1심 판결에 불복해 상급 법원에 다시 판단을 구하는 절차입니다.", "example": "피고가 항소하였다.", "caution": "상고와 단계가 다릅니다."},
        "상고": {"easy_definition": "항소심 판결에 대해 대법원 판단을 구하는 절차입니다.", "example": "원고가 상고하였다.", "caution": "사실관계보다 법률 판단이 중심이 됩니다."},
        "소멸시효": {"easy_definition": "권리를 일정 기간 행사하지 않으면 청구하기 어려워지는 제도입니다.", "example": "손해배상청구권의 소멸시효가 문제 된다.", "caution": "권리마다 기간이 다를 수 있습니다."},
        "입증 책임": {"easy_definition": "어떤 사실을 증거로 밝혀야 하는 부담입니다.", "example": "원고에게 입증 책임이 있다.", "caution": "입증하지 못하면 불리한 판단을 받을 수 있습니다."},
        "불법행위": {"easy_definition": "고의나 과실로 다른 사람에게 손해를 입히는 행위입니다.", "example": "불법행위로 인한 손해배상.", "caution": "계약 위반과 구분될 수 있습니다."},
        "채무불이행": {"easy_definition": "계약이나 법률상 해야 할 의무를 제대로 이행하지 않는 것입니다.", "example": "대금 지급 의무를 이행하지 않았다.", "caution": "불법행위와 법적 근거가 다를 수 있습니다."},
        "손해배상": {"easy_definition": "손해를 입힌 사람이 그 손해를 금전 등으로 메우는 것입니다.", "example": "손해배상을 청구한다.", "caution": "손해와 책임이 인정되어야 합니다."},
        "지연손해금": {"easy_definition": "돈을 늦게 지급한 데 대해 추가로 부담하는 금액입니다.", "example": "연 12%의 지연손해금.", "caution": "이자율은 판결이나 법령에 따라 달라질 수 있습니다."},
        "계약 해제": {"easy_definition": "계약을 처음부터 없었던 것처럼 되돌리는 법적 조치입니다.", "example": "하자를 이유로 계약을 해제한다.", "caution": "단순 취소나 해지와 다를 수 있습니다."},
        "부당이득": {"easy_definition": "법률상 이유 없이 이익을 얻고 다른 사람에게 손해를 준 경우의 이익입니다.", "example": "부당이득 반환을 청구한다.", "caution": "이득과 손해 사이 관계가 문제 됩니다."},
        "하자담보책임": {"easy_definition": "매매 목적물에 문제가 있을 때 판매자가 부담할 수 있는 책임입니다.", "example": "하자담보책임에 따라 손해배상을 청구한다.", "caution": "하자 존재와 통지 시점이 중요할 수 있습니다."},
    }

    def __init__(self, provider: SampleCaseProvider | None = None):
        self.provider = provider or SampleCaseProvider(Path("data/sample_cases.json"))

    def get_term(self, term: str) -> dict[str, Any] | None:
        provider_getter = getattr(self.provider, "get_legal_term", None)
        if provider_getter is not None:
            provider_term = provider_getter(term)
            if provider_term is not None:
                return provider_term
        item = self.GLOSSARY.get(term)
        if item is None:
            return None
        return {"term": term, "source": "MVP built-in glossary", **item}

    def extract_terms(self, case_id: str) -> list[dict[str, Any]]:
        stored_terms = self._stored_case_terms(case_id)
        if stored_terms:
            return stored_terms
        case = self.provider.get_case(case_id)
        if case is None:
            return []
        results = []
        terms = self._available_terms()
        paragraphs = self._paragraphs(case)
        for term in terms:
            for paragraph in paragraphs:
                if term not in paragraph["original_text"]:
                    continue
                item = self.get_term(term)
                if item is None:
                    continue
                item = dict(item)
                item["context_meaning"] = f"현재 문단에서 '{term}' 표현이 사용되었습니다."
                item["paragraph_id"] = paragraph["paragraph_id"]
                results.append(item)
                break
        if not results:
            text = " ".join([case.get("original_text", ""), case.get("summary", ""), " ".join(case.get("main_issues", []))])
            for term in terms:
                if term in text:
                    item = self.get_term(term)
                    if item:
                        item = dict(item)
                        item["context_meaning"] = f"현재 판결문에서 '{term}' 표현이 사용되었습니다."
                        item["paragraph_id"] = None
                        results.append(item)
        self._persist_case_terms(case_id, results)
        return results

    def _available_terms(self) -> list[str]:
        provider_lister = getattr(self.provider, "list_legal_terms", None)
        if provider_lister is not None:
            provider_terms = provider_lister()
            if provider_terms:
                return [item["term"] for item in provider_terms]
        return list(self.GLOSSARY)

    def _stored_case_terms(self, case_id: str) -> list[dict[str, Any]]:
        getter = getattr(self.provider, "get_case_legal_terms", None)
        if getter is None:
            return []
        return getter(case_id)

    def _persist_case_terms(self, case_id: str, terms: list[dict[str, Any]]) -> None:
        writer = getattr(self.provider, "upsert_case_legal_terms", None)
        if writer is not None:
            writer(case_id, terms)

    def _paragraphs(self, case: dict[str, Any]) -> list[dict[str, Any]]:
        paragraphs = []
        for section in case.get("sections", []):
            paragraphs.extend(section.get("paragraphs", []))
        if paragraphs:
            return paragraphs
        return [{"paragraph_id": None, "original_text": case.get("original_text", "")}]
