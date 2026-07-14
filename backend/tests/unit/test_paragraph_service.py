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
