from sqlalchemy.orm import Session

from app.db.models.problem import Problem
from app.schemas.problem import ProblemCreate, ProblemUpdate

from .base import CRUDBase


class CRUDProblem(CRUDBase[Problem]):
    def get(self, db: Session, id: int):
        return db.query(Problem).filter(Problem.id == id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(Problem).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: ProblemCreate):
        db_obj = Problem(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: Problem, obj_in: ProblemUpdate):
        for field, value in obj_in.dict(exclude_unset=True).items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, id: int):
        obj = db.query(Problem).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

    def get_by_code(self, db: Session, problem_code: str):
        return db.query(Problem).filter(Problem.problem_code == problem_code).first()


crud_problem = CRUDProblem(Problem)
