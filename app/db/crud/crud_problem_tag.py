from app.db.models.problem_tag import ProblemTag

from .base import CRUDBase


class CRUDProblemTag(CRUDBase[ProblemTag]):
    pass


crud_problem_tag = CRUDProblemTag(ProblemTag)
