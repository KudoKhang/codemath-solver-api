from __future__ import annotations

from typing import Optional

from sqlalchemy import CheckConstraint, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.enums import CodeFileTypeEnum, SolutionStatusEnum
from app.db.models.base import BaseModel


class Solution(BaseModel):
    __tablename__ = "solutions"
    problem_id: Mapped[int] = mapped_column(ForeignKey("problems.id", ondelete="CASCADE"))
    created_by: Mapped[int] = mapped_column(ForeignKey("accounts.id", ondelete="RESTRICT"))
    last_edited_by: Mapped[Optional[int]] = mapped_column(ForeignKey("accounts.id", ondelete="SET NULL"))
    language_id: Mapped[int] = mapped_column(ForeignKey("programming_languages.id", ondelete="RESTRICT"))
    description: Mapped[Optional[str]] = mapped_column(Text)
    source_code_type: Mapped[CodeFileTypeEnum] = mapped_column(Integer, default=CodeFileTypeEnum.TEXT.value)
    source_code: Mapped[str] = mapped_column(Text)
    status: Mapped[SolutionStatusEnum] = mapped_column(Integer, default=SolutionStatusEnum.PENDING.value)
    score: Mapped[Optional[int]] = mapped_column(Integer)

    __table_args__ = (CheckConstraint("score IS NULL OR (score >= 0 AND score <= 100)", name="solution_score_range"),)

    # ORM relationships
    problem: Mapped["Problem"] = relationship("Problem", back_populates="solutions")
    creator: Mapped["Account"] = relationship("Account", foreign_keys=[created_by], back_populates="created_solutions")
    editor: Mapped[Optional["Account"]] = relationship(
        "Account", foreign_keys=[last_edited_by], back_populates="edited_solutions"
    )
    language: Mapped["ProgrammingLanguage"] = relationship("ProgrammingLanguage", back_populates="solutions")
