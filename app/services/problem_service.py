from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.crud.crud_problem import crud_problem
from app.schemas.problem import ProblemCreate, ProblemUpdate

PROBLEM_NOT_FOUND_MSG = "Problem not found"


class ProblemService:
    @staticmethod
    def get_problems(db: Session, skip: int = 0, limit: int = 100):
        return crud_problem.get_multi(db, skip=skip, limit=limit)

    @staticmethod
    def get_problem(db: Session, problem_id: int):
        db_problem = crud_problem.get(db, id=problem_id)
        if not db_problem:
            raise HTTPException(status_code=404, detail=PROBLEM_NOT_FOUND_MSG)
        return db_problem

    @staticmethod
    def create_problem(db: Session, problem_in: ProblemCreate):
        try:
            return crud_problem.create(db, obj_in=problem_in)
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="Problem with this code or title already exists.")

    @staticmethod
    def update_problem(db: Session, problem_id: int, problem_in: ProblemUpdate):
        db_problem = crud_problem.get(db, id=problem_id)
        if not db_problem:
            raise HTTPException(status_code=404, detail=PROBLEM_NOT_FOUND_MSG)
        try:
            return crud_problem.update(db, db_obj=db_problem, obj_in=problem_in)
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="Update would violate a unique constraint.")

    @staticmethod
    def delete_problem(db: Session, problem_id: int):
        db_problem = crud_problem.get(db, id=problem_id)
        if not db_problem:
            raise HTTPException(status_code=404, detail=PROBLEM_NOT_FOUND_MSG)
        return crud_problem.remove(db, id=problem_id)
