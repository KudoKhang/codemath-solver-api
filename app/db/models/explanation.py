from __future__ import annotations

from typing import Optional

from sqlalchemy import CheckConstraint, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import BaseModel


class Explanation(BaseModel):
    __tablename__ = "explanations"
    problem_id: Mapped[int] = mapped_column(ForeignKey("problems.id", ondelete="CASCADE"))
    created_by: Mapped[int] = mapped_column(ForeignKey("accounts.id", ondelete="RESTRICT"))
    last_edited_by: Mapped[Optional[int]] = mapped_column(ForeignKey("accounts.id", ondelete="SET NULL"))
    title: Mapped[Optional[str]] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text)
    content: Mapped[str] = mapped_column(Text)
    upvotes: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    downvotes: Mapped[int] = mapped_column(Integer, default=0, server_default="0")

    __table_args__ = (CheckConstraint("upvotes >= 0 AND downvotes >= 0", name="votes_must_be_non_negative"),)

    # ORM relationships
    problem: Mapped["Problem"] = relationship("Problem", back_populates="explanations")

    creator: Mapped["Account"] = relationship(
        "Account", foreign_keys=[created_by], back_populates="created_explanations"
    )
    editor: Mapped[Optional["Account"]] = relationship(
        "Account", foreign_keys=[last_edited_by], back_populates="edited_explanations"
    )
