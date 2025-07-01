from sqlalchemy.orm import Session

from app.db.models.solution import Solution
from app.schemas.solution import SolutionCreate, SolutionUpdate

from .base import CRUDBase


class CRUDSolution(CRUDBase[Solution]):
    def get(self, db: Session, id: int):
        return db.query(Solution).filter(Solution.id == id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(Solution).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: SolutionCreate):
        db_obj = Solution(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: Solution, obj_in: SolutionUpdate):
        for field, value in obj_in.dict(exclude_unset=True).items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, id: int):
        obj = db.query(Solution).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj


crud_solution = CRUDSolution(Solution)
