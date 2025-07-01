from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.explanation import ExplanationCreate, ExplanationOutput, ExplanationUpdate
from app.schemas.response import APIResponse
from app.services.explanation_service import ExplanationService

router = APIRouter()


@router.get("/", response_model=APIResponse)
def read_explanations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        data = ExplanationService.get_explanations(db, skip=skip, limit=limit)
        data = [ExplanationOutput.from_orm_obj(row) for row in data]
        return APIResponse.success(data=data, status_code=status.HTTP_200_OK)
    except HTTPException as exc:
        return APIResponse.failure(message=exc.detail, status_code=exc.status_code)


@router.get("/{explanation_id}", response_model=APIResponse)
def read_explanation(explanation_id: int, db: Session = Depends(get_db)):
    try:
        data = ExplanationService.get_explanation(db, explanation_id)
        data = ExplanationOutput.from_orm_obj(data)
        return APIResponse.success(data=data, status_code=status.HTTP_200_OK)
    except HTTPException as exc:
        return APIResponse.failure(message=exc.detail, status_code=exc.status_code)


@router.post("/", response_model=APIResponse)
def create_explanation(explanation_in: ExplanationCreate, db: Session = Depends(get_db)):
    try:
        data = ExplanationService.create_explanation(db, explanation_in)
        data = ExplanationOutput.from_orm_obj(data)
        return APIResponse.success(data=data, status_code=status.HTTP_201_CREATED)
    except HTTPException as exc:
        return APIResponse.failure(message=exc.detail, status_code=exc.status_code)


@router.put("/{explanation_id}", response_model=APIResponse)
def update_explanation(explanation_id: int, explanation_in: ExplanationUpdate, db: Session = Depends(get_db)):
    try:
        data = ExplanationService.update_explanation(db, explanation_id, explanation_in)
        data = ExplanationOutput.from_orm_obj(data)
        return APIResponse.success(data=data, status_code=status.HTTP_200_OK)
    except HTTPException as exc:
        return APIResponse.failure(message=exc.detail, status_code=exc.status_code)


@router.delete("/{explanation_id}", response_model=APIResponse)
def delete_explanation(explanation_id: int, db: Session = Depends(get_db)):
    try:
        data = ExplanationService.delete_explanation(db, explanation_id)
        data = ExplanationOutput.from_orm_obj(data)
        return APIResponse.success(data=data, status_code=status.HTTP_200_OK)
    except HTTPException as exc:
        return APIResponse.failure(message=exc.detail, status_code=exc.status_code)
