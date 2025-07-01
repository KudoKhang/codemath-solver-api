from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.response import APIResponse
from app.schemas.solution import SolutionCreate, SolutionOutput, SolutionUpdate
from app.services.solution_service import SolutionService

router = APIRouter()


@router.get("/", response_model=APIResponse)
def read_solutions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        data = SolutionService.get_solutions(db, skip=skip, limit=limit)
        data = [SolutionOutput.from_orm_obj(row) for row in data]
        return APIResponse.success(data=data, status_code=status.HTTP_200_OK)
    except HTTPException as exc:
        return APIResponse.failure(message=exc.detail, status_code=exc.status_code)


@router.get("/{solution_id}", response_model=APIResponse)
def read_solution(solution_id: int, db: Session = Depends(get_db)):
    try:
        data = SolutionService.get_solution(db, solution_id)
        data = SolutionOutput.from_orm_obj(data)
        return APIResponse.success(data=data, status_code=status.HTTP_200_OK)
    except HTTPException as exc:
        return APIResponse.failure(message=exc.detail, status_code=exc.status_code)


@router.post("/", response_model=APIResponse)
def create_solution(solution_in: SolutionCreate, db: Session = Depends(get_db)):
    try:
        data = SolutionService.create_solution(db, solution_in)
        data = SolutionOutput.from_orm_obj(data)
        return APIResponse.success(data=data, status_code=status.HTTP_201_CREATED)
    except HTTPException as exc:
        return APIResponse.failure(message=exc.detail, status_code=exc.status_code)


@router.put("/{solution_id}", response_model=APIResponse)
def update_solution(solution_id: int, solution_in: SolutionUpdate, db: Session = Depends(get_db)):
    try:
        data = SolutionService.update_solution(db, solution_id, solution_in)
        data = SolutionOutput.from_orm_obj(data)
        return APIResponse.success(data=data, status_code=status.HTTP_200_OK)
    except HTTPException as exc:
        return APIResponse.failure(message=exc.detail, status_code=exc.status_code)


@router.delete("/{solution_id}", response_model=APIResponse)
def delete_solution(solution_id: int, db: Session = Depends(get_db)):
    try:
        data = SolutionService.delete_solution(db, solution_id)
        data = SolutionOutput.from_orm_obj(data)
        return APIResponse.success(data=data, status_code=status.HTTP_200_OK)
    except HTTPException as exc:
        return APIResponse.failure(message=exc.detail, status_code=exc.status_code)
