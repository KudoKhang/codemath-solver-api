from __future__ import annotations

from typing import List, Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import BaseModel


class ProgrammingLanguage(BaseModel):
    __tablename__ = "programming_languages"
    name: Mapped[str] = mapped_column(String(50))
    version: Mapped[Optional[str]] = mapped_column(String(20))
    slug: Mapped[str] = mapped_column(String(50), unique=True)

    solutions: Mapped[List["Solution"]] = relationship("Solution", back_populates="language")
