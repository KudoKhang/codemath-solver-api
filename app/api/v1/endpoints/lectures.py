from typing import List, Literal, Optional

from fastapi import APIRouter, Body, Depends, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.response import APIResponse
from app.services.lecture_service import LectureService

router = APIRouter()


class ProblemInputSchema(BaseModel):
    type: Literal["text", "image", "pdf"]
    content: str
    title: str
    description: Optional[str] = None


class LectureInputSchema(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    content: Optional[str] = None
    codeAnswer: Optional[str] = None
    language: Optional[str] = None
    difficulty: str
    tags: List[str] = Field(default_factory=list)
    problem: ProblemInputSchema


@router.get("/", response_model=APIResponse)
def get_lectures(db: Session = Depends(get_db)):
    lectures = LectureService.get_all_lectures(db)
    return APIResponse.success(data=lectures, status_code=status.HTTP_200_OK)


@router.get("/{platform_id}/{platform_specific_code}", response_model=APIResponse)
def get_lecture(platform_id: int, platform_specific_code: str, db: Session = Depends(get_db)):
    lecture = LectureService.get_lecture(db, platform_id, platform_specific_code)
    if not lecture:
        return APIResponse.failure(message="Problem not found", status_code=404)
    return APIResponse.success(data=lecture, status_code=status.HTTP_200_OK)


@router.post("/", response_model=APIResponse)
def create_lecture(data: LectureInputSchema = Body(...), db: Session = Depends(get_db)):
    lecture_id = LectureService.create_or_update_lecture(db, data, is_update=False)
    return APIResponse.success(data={"id": lecture_id}, status_code=status.HTTP_201_CREATED)


@router.put("/{platform_id}/{platform_specific_code}", response_model=APIResponse)
def update_lecture(
    platform_id: int, platform_specific_code: str, data: LectureInputSchema = Body(...), db: Session = Depends(get_db)
):
    # Ensure the input schema matches the path params
    data.problem.platform_id = platform_id
    data.problem.platform_specific_code = platform_specific_code
    lecture_id = LectureService.create_or_update_lecture(db, data, is_update=True)
    return APIResponse.success(data={"id": lecture_id}, status_code=status.HTTP_200_OK)


@router.delete("/{platform_id}/{platform_specific_code}", response_model=APIResponse)
def delete_lecture(platform_id: int, platform_specific_code: str, db: Session = Depends(get_db)):
    lecture_id = LectureService.delete_lecture(db, platform_id, platform_specific_code)
    if not lecture_id:
        return APIResponse.failure(message="Problem not found", status_code=404)
    return APIResponse.success(data={"id": lecture_id}, status_code=status.HTTP_200_OK)
