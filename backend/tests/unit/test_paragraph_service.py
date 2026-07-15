from app.services.paragraph_service import ParagraphService


def test_split_sections_preserves_order_and_original_text():
    text = "주문\n피고는 원고에게 500만 원을 지급하라.\n이유\n원고는 노트북을 구매하였다."

    sections = ParagraphService().split_sections(text)

    assert sections[0].section_type == "주문"
    assert sections[0].paragraphs[0].original_text == "피고는 원고에게 500만 원을 지급하라."
    assert sections[1].section_type == "이유"


def test_split_sections_returns_original_section_when_headings_are_missing():
    text = "섹션 제목 없이 작성된 판결문 문단입니다."

    sections = ParagraphService().split_sections(text)

    assert len(sections) == 1
    assert sections[0].section_type == "원문"
    assert sections[0].paragraphs[0].original_text == text


def test_split_sections_accepts_numbered_common_headings():
    text = "\n".join(
        [
            "1. 주문",
            "피고는 원고에게 100만 원을 지급하라.",
            "2. 청구취지",
            "원고는 손해배상을 구한다.",
            "가. 이유",
            "다음과 같은 이유로 판단한다.",
        ]
    )

    sections = ParagraphService().split_sections(text)

    assert [section.section_type for section in sections] == ["주문", "청구 취지", "이유"]
    assert sections[0].paragraphs[0].original_text == "피고는 원고에게 100만 원을 지급하라."
    assert sections[1].paragraphs[0].original_text == "원고는 손해배상을 구한다."
    assert sections[2].paragraphs[0].original_text == "다음과 같은 이유로 판단한다."


def test_split_sections_normalizes_party_argument_headings():
    text = "\n".join(
        [
            "1. 원고의 주장",
            "원고는 계약 해제를 주장한다.",
            "2. 피고의 주장",
            "피고는 하자가 없었다고 다툰다.",
            "3. 법원의 판단",
            "법원은 피고의 책임을 인정한다.",
        ]
    )

    sections = ParagraphService().split_sections(text)

    assert [section.section_type for section in sections] == ["원고 주장", "피고 주장", "법원의 판단"]
    assert sections[0].paragraphs[0].original_text == "원고는 계약 해제를 주장한다."
    assert sections[1].paragraphs[0].original_text == "피고는 하자가 없었다고 다툰다."
    assert sections[2].paragraphs[0].original_text == "법원은 피고의 책임을 인정한다."


def test_split_sections_normalizes_conclusion_and_law_headings():
    text = "\n".join(
        [
            "4. 결론",
            "따라서 원고의 청구는 이유 있다.",
            "5. 적용법령",
            "민법 제390조",
        ]
    )

    sections = ParagraphService().split_sections(text)

    assert [section.section_type for section in sections] == ["결론", "관련 법령"]
    assert sections[0].paragraphs[0].original_text == "따라서 원고의 청구는 이유 있다."
    assert sections[1].paragraphs[0].original_text == "민법 제390조"
