from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ExplanationBase(BaseModel):
    problem_id: int
    created_by: int
    last_edited_by: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    content: str
    upvotes: int = 0
    downvotes: int = 0


class ExplanationCreate(ExplanationBase):
    pass


class ExplanationUpdate(ExplanationBase):
    pass


class ExplanationInDBBase(ExplanationBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class ExplanationOutput(ExplanationBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_orm_obj(cls, obj):
        return cls(
            id=obj.id,
            problem_id=obj.problem_id,
            created_by=obj.created_by,
            last_edited_by=obj.last_edited_by,
            title=obj.title,
            description=obj.description,
            content=obj.content,
            upvotes=obj.upvotes,
            downvotes=obj.downvotes,
            created_at=obj.created_at,
            updated_at=obj.updated_at,
        )
