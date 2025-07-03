from typing import List, Literal, Optional

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.schemas.explanation import ExplanationCreate, ExplanationUpdate
from app.schemas.problem import ProblemCreate, ProblemUpdate
from app.schemas.solution import SolutionCreate, SolutionUpdate
from app.services.explanation_service import ExplanationService
from app.services.problem_service import ProblemService
from app.services.solution_service import SolutionService


class ProblemOutputSchema(BaseModel):
    type: Literal["text", "image", "pdf"]
    content: str
    title: str
    description: Optional[str] = None


class LectureOutputSchema(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    content: Optional[str] = None
    codeAnswer: Optional[str] = None
    language: Optional[str] = None
    difficulty: str
    tags: List[str] = Field(default_factory=list)
    problem: ProblemOutputSchema


class LectureService:
    @staticmethod
    def get_lecture(db: Session, problem_code: str):
        problem = ProblemService.get_problem_by_code(db, problem_code)
        if not problem:
            return None
        explanation = ExplanationService.get_by_problem_id(db, problem.id)
        solution = SolutionService.get_accepted_solution_by_problem_id(db, problem.id)
        tags = [tag.name for tag in getattr(problem, "tags", [])]
        return LectureOutputSchema(
            id=str(problem.id),
            title=problem.title,
            description=explanation.content[:100] if explanation else None,
            content=explanation.content if explanation else None,
            codeAnswer=solution.code_file_url if solution else None,
            language=solution.language if solution else None,
            difficulty=problem.difficulty,
            tags=tags,
            problem=ProblemOutputSchema(
                type="pdf" if problem.problem_pdf_url else "text",
                content=problem.problem_pdf_url if problem.problem_pdf_url else problem.title,
                title=problem.title,
                description=explanation.content[:100] if explanation else None,
            ),
        )

    @staticmethod
    def create_or_update_lecture(db: Session, data, is_update=False):
        # 1. Create or update problem
        problem_in = ProblemCreate(
            problem_code=data.id,
            title=data.title,
            difficulty=data.difficulty,
            problem_pdf_url=data.problem.content if data.problem.type == "pdf" else None,
            source=None,
        )
        problem = ProblemService.get_problem_by_code(db, data.id)
        if not problem:
            problem = ProblemService.create_problem(db, problem_in)
        else:
            problem = ProblemService.update_problem(db, problem.id, ProblemUpdate(**problem_in.dict()))
        # 2. Create/update explanation
        if data.content:
            explanation_in = ExplanationCreate(problem_id=problem.id, content=data.content)
            explanation = ExplanationService.get_by_problem_id(db, problem.id)
            if not explanation:
                ExplanationService.create_explanation(db, explanation_in)
            else:
                ExplanationService.update_explanation(db, explanation.id, ExplanationUpdate(**explanation_in.dict()))
        # 3. Create/update solution
        if data.codeAnswer:
            solution_in = SolutionCreate(
                problem_id=problem.id,
                language=data.language if data.language else None,
                code_file_url=data.codeAnswer,
                is_accepted=True,
            )
            solution = SolutionService.get_accepted_solution_by_problem_id(db, problem.id)
            if not solution:
                SolutionService.create_solution(db, solution_in)
            else:
                SolutionService.update_solution(db, solution.id, SolutionUpdate(**solution_in.dict()))
        # 4. Tags (not implemented here)
        return problem.id

    @staticmethod
    def delete_lecture(db: Session, problem_code: str):
        problem = ProblemService.get_problem_by_code(db, problem_code)
        if not problem:
            return None
        ProblemService.delete_problem(db, problem.id)
        return problem.id

    @staticmethod
    def get_all_lectures(db: Session):
        from app.db.models.problem import Problem

        problems = db.query(Problem).all()
        lectures = []
        for problem in problems:
            explanation = ExplanationService.get_by_problem_id(db, problem.id)
            solution = SolutionService.get_accepted_solution_by_problem_id(db, problem.id)
            tags = [tag.name for tag in getattr(problem, "tags", [])]
            lectures.append(
                LectureOutputSchema(
                    id=str(problem.id),
                    title=problem.title,
                    description=explanation.content[:100] if explanation else None,
                    content=explanation.content if explanation else None,
                    codeAnswer=solution.code_file_url if solution else None,
                    language=solution.language if solution else None,
                    difficulty=problem.difficulty,
                    tags=tags,
                    problem=ProblemOutputSchema(
                        type="pdf" if problem.problem_pdf_url else "text",
                        content=problem.problem_pdf_url if problem.problem_pdf_url else problem.title,
                        title=problem.title,
                        description=explanation.content[:100] if explanation else None,
                    ),
                )
            )
        return lectures
