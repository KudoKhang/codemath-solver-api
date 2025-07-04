from __future__ import annotations

from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import BaseModel, problem_tags_table


class Tag(BaseModel):
    __tablename__ = "tags"
    name: Mapped[str] = mapped_column(String(50), unique=True)
    slug: Mapped[str] = mapped_column(String(50), unique=True)

    # Many-to-many relationship with Problem through ProblemTag
    problems: Mapped[List["Problem"]] = relationship("Problem", secondary=problem_tags_table, back_populates="tags")
