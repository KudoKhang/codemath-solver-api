from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator

from app.common.enums import DifficultyEnum


class ProblemBase(BaseModel):
    problem_code: str
    title: str
    source: Optional[str] = None
    difficulty: Optional[DifficultyEnum] = None
    problem_pdf_url: Optional[str] = None

    @field_validator("difficulty", mode="before")
    def lowercase_difficulty(cls, v):
        if isinstance(v, str):
            return v.lower()
        return v


class ProblemCreate(ProblemBase):
    pass


class ProblemUpdate(ProblemBase):
    pass


class ProblemInDBBase(ProblemBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class ProblemOutput(ProblemBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_orm_obj(cls, obj):
        return cls(
            id=obj.id,
            problem_code=obj.problem_code,
            title=obj.title,
            source=obj.source,
            difficulty=obj.difficulty,
            problem_pdf_url=obj.problem_pdf_url,
            created_at=obj.created_at,
            updated_at=obj.updated_at,
        )
