from __future__ import annotations

from typing import List, Optional

from sqlalchemy import ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Integer

from app.common.enums import ContentFormatEnum, ProblemDifficultyEnum
from app.db.models.base import BaseModel, problem_tags_table


class Problem(BaseModel):
    __tablename__ = "problems"
    platform_id: Mapped[Optional[int]] = mapped_column(ForeignKey("platforms.id", ondelete="SET NULL"))
    platform_specific_code: Mapped[str] = mapped_column(String(100))
    title: Mapped[str] = mapped_column(String(255))
    difficulty: Mapped[Optional[ProblemDifficultyEnum]] = mapped_column(Integer)
    description: Mapped[Optional[str]] = mapped_column(Text)
    content_format: Mapped[Optional[ContentFormatEnum]] = mapped_column(Integer)
    content: Mapped[str] = mapped_column(Text)
    created_by: Mapped[int] = mapped_column(ForeignKey("accounts.id", ondelete="RESTRICT"))
    last_edited_by: Mapped[Optional[int]] = mapped_column(ForeignKey("accounts.id", ondelete="SET NULL"))

    __table_args__ = (UniqueConstraint("platform_id", "platform_specific_code", name="uq_problem_on_platform"),)

    platform: Mapped[Optional["Platform"]] = relationship(back_populates="problems")
    creator: Mapped["Account"] = relationship(foreign_keys=[created_by], back_populates="created_problems")
    editor: Mapped[Optional["Account"]] = relationship(foreign_keys=[last_edited_by], back_populates="edited_problems")
    solutions: Mapped[List["Solution"]] = relationship(back_populates="problem")
    explanations: Mapped[List["Explanation"]] = relationship(back_populates="problem")
    tags: Mapped[List["Tag"]] = relationship("Tag", secondary=problem_tags_table, back_populates="problems")
