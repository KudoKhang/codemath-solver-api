from __future__ import annotations

from typing import List, Optional

from sqlalchemy import CheckConstraint, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.enums import RoleEnum
from app.db.models.base import BaseModel


class Account(BaseModel):
    __tablename__ = "accounts"
    username: Mapped[str] = mapped_column(String(50), unique=True)
    fullname: Mapped[Optional[str]] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[RoleEnum] = mapped_column(Integer, default=RoleEnum.USER.value)
    is_active: Mapped[bool] = mapped_column(default=True, server_default="true")
    credits: Mapped[int] = mapped_column(Integer, default=0, server_default="0")

    __table_args__ = (CheckConstraint("credits >= 0", name="credits_must_be_non_negative"),)

    # Reverse relationships
    created_problems: Mapped[List["Problem"]] = relationship(
        "Problem", foreign_keys="Problem.created_by", back_populates="creator"
    )
    edited_problems: Mapped[List["Problem"]] = relationship(
        "Problem", foreign_keys="Problem.last_edited_by", back_populates="editor"
    )
    created_solutions: Mapped[List["Solution"]] = relationship(
        "Solution", foreign_keys="Solution.created_by", back_populates="creator", cascade="all, delete-orphan"
    )
    edited_solutions: Mapped[List["Solution"]] = relationship(
        "Solution", foreign_keys="Solution.last_edited_by", back_populates="editor"
    )
    created_explanations: Mapped[List["Explanation"]] = relationship(
        "Explanation", foreign_keys="Explanation.created_by", back_populates="creator", cascade="all, delete-orphan"
    )
    edited_explanations: Mapped[List["Explanation"]] = relationship(
        "Explanation", foreign_keys="Explanation.last_edited_by", back_populates="editor"
    )
    credit_transactions: Mapped[List["CreditTransaction"]] = relationship(
        "CreditTransaction", back_populates="account", cascade="all, delete-orphan"
    )
