from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ExplanationBase(BaseModel):
    problem_id: int
    content: str


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
            content=obj.content,
            created_at=obj.created_at,
            updated_at=obj.updated_at,
        )
