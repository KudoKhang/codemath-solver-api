from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.common.enums import ContentFormatEnum, PlatformEnum, ProblemDifficultyEnum


class ProblemBase(BaseModel):
    platform_id: Optional[PlatformEnum] = PlatformEnum.CODEMATH
    platform_specific_code: str
    title: str
    difficulty: Optional[ProblemDifficultyEnum] = None
    description: Optional[str] = None
    content_format: Optional[ContentFormatEnum] = None
    content: str
    created_by: int
    last_edited_by: Optional[int] = None

    class Config:
        use_enum_values = True


class ProblemCreate(ProblemBase):
    pass


class ProblemUpdate(ProblemBase):
    pass


class ProblemOutput(ProblemBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_orm_obj(cls, obj):
        return cls(
            id=obj.id,
            platform_id=obj.platform_id,
            platform_specific_code=obj.platform_specific_code,
            title=obj.title,
            difficulty=obj.difficulty,
            description=obj.description,
            content_format=obj.content_format,
            content=obj.content,
            created_by=obj.created_by,
            last_edited_by=obj.last_edited_by,
            created_at=obj.created_at,
            updated_at=obj.updated_at,
        )
