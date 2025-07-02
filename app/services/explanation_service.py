from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.crud.crud_explanation import crud_explanation
from app.schemas.explanation import ExplanationCreate, ExplanationUpdate

EXPLANATION_NOT_FOUND_MSG = "Explanation not found"


class ExplanationService:
    @staticmethod
    def get_explanations(db: Session, skip: int = 0, limit: int = 100):
        return crud_explanation.get_multi(db, skip=skip, limit=limit)

    @staticmethod
    def get_explanation(db: Session, explanation_id: int):
        db_explanation = crud_explanation.get(db, id=explanation_id)
        if not db_explanation:
            raise HTTPException(status_code=404, detail=EXPLANATION_NOT_FOUND_MSG)
        return db_explanation

    @staticmethod
    def create_explanation(db: Session, explanation_in: ExplanationCreate):
        try:
            return crud_explanation.create(db, obj_in=explanation_in)
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="Invalid problem_id: referenced problem does not exist.")

    @staticmethod
    def update_explanation(db: Session, explanation_id: int, explanation_in: ExplanationUpdate):
        db_explanation = crud_explanation.get(db, id=explanation_id)
        if not db_explanation:
            raise HTTPException(status_code=404, detail=EXPLANATION_NOT_FOUND_MSG)
        try:
            return crud_explanation.update(db, db_obj=db_explanation, obj_in=explanation_in)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=400, detail="Update would violate a unique constraint or invalid problem_id."
            )

    @staticmethod
    def delete_explanation(db: Session, explanation_id: int):
        db_explanation = crud_explanation.get(db, id=explanation_id)
        if not db_explanation:
            raise HTTPException(status_code=404, detail=EXPLANATION_NOT_FOUND_MSG)
        return crud_explanation.remove(db, id=explanation_id)

    @staticmethod
    def get_by_problem_id(db: Session, problem_id: int):
        from app.db.models.explanation import Explanation

        return db.query(Explanation).filter(Explanation.problem_id == problem_id).first()
