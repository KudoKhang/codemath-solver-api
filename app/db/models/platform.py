from __future__ import annotations

from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import BaseModel


class Platform(BaseModel):
    __tablename__ = "platforms"
    name: Mapped[str] = mapped_column(String(100), unique=True)

    problems: Mapped[List["Problem"]] = relationship("Problem", back_populates="platform")
