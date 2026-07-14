from datetime import UTC, date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )


class CaseDocument(Base, TimestampMixin):
    __tablename__ = "case_documents"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    external_id: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    case_number: Mapped[str] = mapped_column(String(128), index=True)
    case_name: Mapped[str] = mapped_column(String(255), index=True)
    court_name: Mapped[str] = mapped_column(String(255), default="")
    court_department: Mapped[str] = mapped_column(String(255), default="")
    decision_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    category: Mapped[str] = mapped_column(String(64), index=True, default="")
    judgment_result: Mapped[str] = mapped_column(String(128), default="")
    order_text: Mapped[str] = mapped_column(Text, default="")
    original_text: Mapped[str] = mapped_column(Text)
    summary: Mapped[str] = mapped_column(Text, default="")
    main_issues: Mapped[str] = mapped_column(Text, default="[]")
    source_name: Mapped[str] = mapped_column(String(255), default="")
    source_url: Mapped[str] = mapped_column(Text, default="")
    source_updated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    sections: Mapped[list["CaseSection"]] = relationship(back_populates="case", cascade="all, delete-orphan")
    summary_row: Mapped["CaseSummary | None"] = relationship(back_populates="case", cascade="all, delete-orphan")


class CaseSection(Base):
    __tablename__ = "case_sections"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    case_id: Mapped[str] = mapped_column(ForeignKey("case_documents.id"), index=True)
    section_type: Mapped[str] = mapped_column(String(64))
    section_order: Mapped[int] = mapped_column(Integer)
    original_text: Mapped[str] = mapped_column(Text)

    case: Mapped[CaseDocument] = relationship(back_populates="sections")
    paragraphs: Mapped[list["CaseParagraph"]] = relationship(back_populates="section", cascade="all, delete-orphan")


class CaseParagraph(Base):
    __tablename__ = "case_paragraphs"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    section_id: Mapped[str] = mapped_column(ForeignKey("case_sections.id"), index=True)
    paragraph_order: Mapped[int] = mapped_column(Integer)
    original_text: Mapped[str] = mapped_column(Text)
    simplified_text: Mapped[str] = mapped_column(Text, default="")
    validation_status: Mapped[str] = mapped_column(String(64), default="not_generated")
    validation_warnings: Mapped[str] = mapped_column(Text, default="[]")
    simplified_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    section: Mapped[CaseSection] = relationship(back_populates="paragraphs")


class CaseSummary(Base):
    __tablename__ = "case_summaries"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    case_id: Mapped[str] = mapped_column(ForeignKey("case_documents.id"), unique=True, index=True)
    one_line_summary: Mapped[str] = mapped_column(Text, default="")
    background: Mapped[str] = mapped_column(Text, default="")
    plaintiff_claim: Mapped[str] = mapped_column(Text, default="")
    defendant_claim: Mapped[str] = mapped_column(Text, default="")
    court_reasoning: Mapped[str] = mapped_column(Text, default="")
    judgment_result: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))

    case: Mapped[CaseDocument] = relationship(back_populates="summary_row")


class LegalTerm(Base):
    __tablename__ = "legal_terms"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    term: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    easy_definition: Mapped[str] = mapped_column(Text)
    example: Mapped[str] = mapped_column(Text, default="")
    caution: Mapped[str] = mapped_column(Text, default="")
    source: Mapped[str] = mapped_column(String(255), default="MVP built-in glossary")


class CaseLegalTerm(Base):
    __tablename__ = "case_legal_terms"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    case_id: Mapped[str] = mapped_column(ForeignKey("case_documents.id"), index=True)
    term_id: Mapped[str] = mapped_column(ForeignKey("legal_terms.id"), index=True)
    context_meaning: Mapped[str] = mapped_column(Text, default="")
    paragraph_id: Mapped[str | None] = mapped_column(ForeignKey("case_paragraphs.id"), nullable=True)


class CaseEmbedding(Base):
    __tablename__ = "case_embeddings"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    case_id: Mapped[str] = mapped_column(ForeignKey("case_documents.id"), index=True)
    paragraph_id: Mapped[str | None] = mapped_column(ForeignKey("case_paragraphs.id"), nullable=True)
    document_type: Mapped[str] = mapped_column(String(64))
    embedding_reference: Mapped[str] = mapped_column(Text)
