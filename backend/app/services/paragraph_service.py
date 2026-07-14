from dataclasses import asdict, dataclass

@dataclass
class ParagraphResult:
    paragraph_id: str
    paragraph_order: int
    original_text: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class SectionResult:
    section_id: str
    section_type: str
    section_order: int
    original_text: str
    paragraphs: list[ParagraphResult]

    def to_dict(self) -> dict:
        data = asdict(self)
        data["paragraphs"] = [paragraph.to_dict() for paragraph in self.paragraphs]
        return data


class ParagraphService:
    HEADINGS = [
        "주문",
        "청구 취지",
        "이유",
        "인정 사실",
        "원고 주장",
        "피고 주장",
        "법원의 판단",
        "결론",
        "관련 법령",
    ]

    def split_sections(self, original_text: str) -> list[SectionResult]:
        lines = [line.strip() for line in original_text.splitlines() if line.strip()]
        sections: list[tuple[str, list[str]]] = []
        current_heading: str | None = None
        current_lines: list[str] = []

        for line in lines:
            if line in self.HEADINGS:
                if current_heading is not None:
                    sections.append((current_heading, current_lines))
                current_heading = line
                current_lines = []
            else:
                current_lines.append(line)

        if current_heading is not None:
            sections.append((current_heading, current_lines))

        if not sections:
            sections = [("원문", [original_text.strip()] if original_text.strip() else [])]

        return [self._build_section(section_order, heading, section_lines) for section_order, (heading, section_lines) in enumerate(sections, start=1)]

    def _build_section(self, section_order: int, heading: str, lines: list[str]) -> SectionResult:
        paragraphs = [
            ParagraphResult(
                paragraph_id=f"paragraph-{section_order}-{index}",
                paragraph_order=index,
                original_text=line,
            )
            for index, line in enumerate(lines, start=1)
        ]
        return SectionResult(
            section_id=f"section-{section_order}",
            section_type=heading,
            section_order=section_order,
            original_text="\n".join(lines),
            paragraphs=paragraphs,
        )
