from fastapi import HTTPException
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.crud.crud_solution import crud_solution
from app.schemas.solution import SolutionCreate, SolutionUpdate


class SolutionService:
    @staticmethod
    def get_solutions(db: Session, skip: int = 0, limit: int = 100):
        return crud_solution.get_multi(db, skip=skip, limit=limit)

    @staticmethod
    def get_solution(db: Session, solution_id: int):
        db_solution = crud_solution.get(db, id=solution_id)
        if not db_solution:
            raise HTTPException(status_code=404, detail="Solution not found")
        return db_solution

    @staticmethod
    def create_solution(db: Session, solution_in: SolutionCreate):
        try:
            return crud_solution.create(db, obj_in=solution_in)
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="Invalid problem_id: referenced problem does not exist.")

    @staticmethod
    def update_solution(db: Session, solution_id: int, solution_in: SolutionUpdate):
        try:
            db_solution = crud_solution.get(db, id=solution_id)
            if not db_solution:
                raise HTTPException(status_code=404, detail="Solution not found")
            return crud_solution.update(db, db_obj=db_solution, obj_in=solution_in)
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="Update would violate a unique constraint.")

    @staticmethod
    def delete_solution(db: Session, solution_id: int):
        db_solution = crud_solution.get(db, id=solution_id)
        if not db_solution:
            raise HTTPException(status_code=404, detail="Solution not found")
        return crud_solution.remove(db, id=solution_id)

    @staticmethod
    def get_accepted_solution_by_problem_id(db: Session, problem_id: int):
        from app.db.models.solution import Solution

        return db.query(Solution).filter(Solution.problem_id == problem_id).order_by(desc(Solution.status)).first()
