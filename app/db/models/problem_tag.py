from sqlalchemy import Column, ForeignKey, Integer

from app.db.base import Base


class ProblemTag(Base):
    __tablename__ = "problem_tags"
    problem_id = Column(Integer, ForeignKey("problems.id", ondelete="CASCADE"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)
