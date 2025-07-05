from typing import List, Optional

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.common.enums import ContentFormatEnum, ProblemDifficultyEnum, ProgrammingLanguageEnum
from app.schemas.explanation import ExplanationCreate, ExplanationUpdate
from app.schemas.problem import ProblemCreate, ProblemUpdate
from app.schemas.solution import SolutionCreate, SolutionUpdate
from app.services.explanation_service import ExplanationService
from app.services.problem_service import ProblemService
from app.services.solution_service import SolutionService


class ProblemOutputSchema(BaseModel):
    id: int
    platform_id: Optional[int] = None
    platform_specific_code: str
    title: str
    difficulty: ProblemDifficultyEnum = None
    description: Optional[str] = None
    content_format: ContentFormatEnum = None  # noqa: F821
    content: str
    created_by: int
    last_edited_by: Optional[int] = None


class LectureOutputSchema(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    content: Optional[str] = None
    codeAnswer: Optional[str] = None
    language_id: ProgrammingLanguageEnum = None
    difficulty: ProblemDifficultyEnum = None
    tags: List[str] = Field(default_factory=list)
    problem: ProblemOutputSchema
    explanation: Optional[dict] = None
    solution: Optional[dict] = None


class LectureService:
    @staticmethod
    def get_lecture(db: Session, platform_id: int, platform_specific_code: str):
        problem = ProblemService.get_problem_by_platform_and_code(db, platform_id, platform_specific_code)
        if not problem:
            return None
        explanation = ExplanationService.get_by_problem_id(db, problem.id)
        solution = SolutionService.get_accepted_solution_by_problem_id(db, problem.id)
        tags = [tag.name for tag in getattr(problem, "tags", [])]
        return LectureOutputSchema(
            id=problem.id,
            title=problem.title,
            description=problem.description,
            content=problem.content,
            codeAnswer=solution.source_code if solution else None,
            language_id=(
                solution.language_id
                if solution and solution.language_id is not None
                else list(ProgrammingLanguageEnum)[0]
            ),
            difficulty=problem.difficulty,
            tags=tags,
            problem=ProblemOutputSchema(
                id=problem.id,
                platform_id=problem.platform_id,
                platform_specific_code=problem.platform_specific_code,
                title=problem.title,
                difficulty=problem.difficulty,
                description=problem.description,
                content_format=problem.content_format,
                content=problem.content,
                created_by=problem.created_by,
                last_edited_by=problem.last_edited_by,
            ),
            explanation=(explanation if isinstance(explanation, dict) or explanation is None else explanation.__dict__),
            solution=(solution if isinstance(solution, dict) or solution is None else solution.__dict__),
        )

    @staticmethod
    def create_or_update_lecture(db: Session, data, is_update=False):
        # 1. Create or update problem
        problem_in = ProblemCreate(
            platform_id=data.problem.platform_id,
            platform_specific_code=data.problem.platform_specific_code,
            title=data.title,
            difficulty=data.difficulty,
            description=data.description,
            content_format=data.problem.content_format,
            content=data.problem.content,
            created_by=data.problem.created_by,
            last_edited_by=data.problem.last_edited_by,
        )
        problem = ProblemService.get_problem_by_platform_and_code(
            db, data.problem.platform_id, data.problem.platform_specific_code
        )
        if not problem:
            problem = ProblemService.create_problem(db, problem_in)
        else:
            problem = ProblemService.update_problem(db, problem.id, ProblemUpdate(**problem_in.dict()))
        # 2. Create/update explanation
        if data.content:
            explanation_in = ExplanationCreate(
                problem_id=problem.id,
                created_by=data.problem.created_by,
                last_edited_by=data.problem.last_edited_by,
                title=data.title,
                description=data.description,
                content=data.content,
                upvotes=0,
                downvotes=0,
            )
            explanation = ExplanationService.get_by_problem_id(db, problem.id)
            if not explanation:
                ExplanationService.create_explanation(db, explanation_in)
            else:
                ExplanationService.update_explanation(db, explanation.id, ExplanationUpdate(**explanation_in.dict()))
        # 3. Create/update solution
        if data.codeAnswer:
            solution_in = SolutionCreate(
                problem_id=problem.id,
                created_by=data.problem.created_by,
                last_edited_by=data.problem.last_edited_by,
                language_id=data.language_id,
                description=data.description,
                source_code_type=None,
                source_code=data.codeAnswer,
                status="PENDING",
                score=None,
            )
            solution = SolutionService.get_accepted_solution_by_problem_id(db, problem.id)
            if not solution:
                SolutionService.create_solution(db, solution_in)
            else:
                SolutionService.update_solution(db, solution.id, SolutionUpdate(**solution_in.dict()))
        # 4. Tags (not implemented here)
        return problem.id

    @staticmethod
    def delete_lecture(db: Session, platform_id: int, platform_specific_code: str):
        problem = ProblemService.get_problem_by_platform_and_code(db, platform_id, platform_specific_code)
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
                    id=problem.id,
                    title=problem.title,
                    description=problem.description,
                    content=problem.content,
                    codeAnswer=solution.source_code if solution else None,
                    language_id=solution.language_id if solution else None,
                    difficulty=problem.difficulty,
                    tags=tags,
                    problem=ProblemOutputSchema(
                        id=problem.id,
                        platform_id=problem.platform_id,
                        platform_specific_code=problem.platform_specific_code,
                        title=problem.title,
                        difficulty=problem.difficulty,
                        description=problem.description,
                        content_format=problem.content_format,
                        content=problem.content,
                        created_by=problem.created_by,
                        last_edited_by=problem.last_edited_by,
                    ),
                    explanation=(
                        explanation if isinstance(explanation, dict) or explanation is None else explanation.__dict__
                    ),
                    solution=(solution if isinstance(solution, dict) or solution is None else solution.__dict__),
                )
            )
        return lectures
