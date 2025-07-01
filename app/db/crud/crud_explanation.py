from sqlalchemy.orm import Session

from app.db.models.explanation import Explanation

from .base import CRUDBase


class CRUDExplanation(CRUDBase[Explanation]):
    def create(self, db: Session, obj_in):
        db_obj = Explanation(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, id: int):
        return db.query(Explanation).filter(Explanation.id == id).first()

    def update(self, db: Session, db_obj: Explanation, obj_in):
        for field, value in obj_in.dict(exclude_unset=True).items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, id: int):
        obj = db.query(Explanation).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj


crud_explanation = CRUDExplanation(Explanation)
