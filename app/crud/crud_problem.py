from app.db.models.problem import Problem

from .base import CRUDBase


class CRUDProblem(CRUDBase[Problem]):
    pass


crud_problem = CRUDProblem(Problem)
