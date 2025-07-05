from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.common.enums import CodeFileTypeEnum, ProgrammingLanguageEnum, SolutionStatusEnum


class SolutionBase(BaseModel):
    problem_id: int
    created_by: int
    last_edited_by: Optional[int] = None
    language_id: ProgrammingLanguageEnum = ProgrammingLanguageEnum.PYTHON
    description: Optional[str] = None
    source_code_type: CodeFileTypeEnum = CodeFileTypeEnum.TEXT
    source_code: str
    status: SolutionStatusEnum = SolutionStatusEnum.PENDING
    score: Optional[int] = None


class SolutionCreate(SolutionBase):
    pass


class SolutionUpdate(SolutionBase):
    pass


class SolutionOutput(SolutionBase):
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
            language_id=obj.language_id,
            description=obj.description,
            source_code_type=obj.source_code_type,
            source_code=obj.source_code,
            status=obj.status,
            score=obj.score,
            created_at=obj.created_at,
            updated_at=obj.updated_at,
        )
