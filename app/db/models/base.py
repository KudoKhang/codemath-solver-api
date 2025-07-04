import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Table
from sqlalchemy.orm import Mapped, declarative_base, mapped_column
from sqlalchemy.sql import func

Base = declarative_base()

problem_tags_table = Table(
    "problem_tags",
    Base.metadata,
    Column("problem_id", Integer, ForeignKey("problems.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)


class TimestampMixin:
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


class BaseModel(Base, TimestampMixin):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
