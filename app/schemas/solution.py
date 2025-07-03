from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator

from app.common.enums import LanguageEnum


class SolutionBase(BaseModel):
    problem_id: int
    language: Optional[LanguageEnum] = None
    code_file_url: Optional[str] = None
    description: Optional[str] = None
    is_accepted: Optional[bool] = False

    @field_validator("language", mode="before")
    def lowercase_language(cls, v):
        if isinstance(v, str):
            return v.lower()
        return v


class SolutionCreate(SolutionBase):
    pass


class SolutionUpdate(SolutionBase):
    pass


class SolutionInDBBase(SolutionBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class SolutionOutput(SolutionBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_orm_obj(cls, obj):
        return cls(
            id=obj.id,
            problem_id=obj.problem_id,
            language=obj.language,
            code_file_url=obj.code_file_url,
            description=obj.description,
            is_accepted=obj.is_accepted,
            created_at=obj.created_at,
            updated_at=obj.updated_at,
        )
