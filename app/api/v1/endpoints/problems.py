from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.problem import ProblemCreate, ProblemOutput, ProblemUpdate
from app.schemas.response import APIResponse
from app.services.problem_service import ProblemService

router = APIRouter()



@router.get("/", response_model=APIResponse)
def read_problems(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    data = ProblemService.get_problems(db, skip=skip, limit=limit)
    data = [ProblemOutput.from_orm_obj(row) for row in data]
    return APIResponse.success(data=data, status_code=status.HTTP_200_OK)


@router.get("/{problem_id}", response_model=APIResponse)
def read_problem(problem_id: int, db: Session = Depends(get_db)):
    data = ProblemService.get_problem(db, problem_id)
    data = ProblemOutput.from_orm_obj(data)
    return APIResponse.success(data=data, status_code=status.HTTP_200_OK)


@router.post("/", response_model=APIResponse)
def create_problem(problem_in: ProblemCreate, db: Session = Depends(get_db)):
    try:
        data = ProblemService.create_problem(db, problem_in)
        data = ProblemOutput.from_orm_obj(data)
        return APIResponse.success(data=data, status_code=status.HTTP_201_CREATED)
    except HTTPException as exc:
        return APIResponse.failure(message=exc.detail, status_code=exc.status_code)


@router.put("/{problem_id}", response_model=APIResponse)
def update_problem(problem_id: int, problem_in: ProblemUpdate, db: Session = Depends(get_db)):
    try:
        data = ProblemService.update_problem(db, problem_id, problem_in)
        data = ProblemOutput.from_orm_obj(data)
        return APIResponse.success(data=data, status_code=status.HTTP_200_OK)
    except HTTPException as exc:
        return APIResponse.failure(message=exc.detail, status_code=exc.status_code)


@router.delete("/{problem_id}", response_model=APIResponse)
def delete_problem(problem_id: int, db: Session = Depends(get_db)):
    try:
        data = ProblemService.delete_problem(db, problem_id)
        data = ProblemOutput.from_orm_obj(data)
        return APIResponse.success(data=data, status_code=status.HTTP_200_OK)
    except HTTPException as exc:
        return APIResponse.failure(message=exc.detail, status_code=exc.status_code)
