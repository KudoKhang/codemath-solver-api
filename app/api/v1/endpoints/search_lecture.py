from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.response import APIResponse
from app.services.explanation_service import ExplanationService
from app.services.problem_service import ProblemService
from app.services.solution_service import SolutionService

router = APIRouter()


@router.get("/search_lecture", response_model=APIResponse)
def search_lecture(
    problem_code: str = Query(..., description="Problem code to search for"), db: Session = Depends(get_db)
):
    # 1. Get problem by code
    problem = ProblemService.get_problem_by_code(db, problem_code)
    if not problem:
        return APIResponse.failure(message="Problem not found", status_code=404)
    # 2. Get explanation (if any)
    explanation = ExplanationService.get_by_problem_id(db, problem.id)
    # 3. Get accepted solution (if any)
    solution = SolutionService.get_accepted_solution_by_problem_id(db, problem.id)
    # 4. Get tags (if relationship exists)
    tags = [tag.name for tag in getattr(problem, "tags", [])]
    # 5. Compose response
    lecture = {
        "id": str(problem.id),
        "title": problem.title,
        "description": explanation.content[:100] if explanation else None,
        "content": explanation.content if explanation else None,
        "codeAnswer": solution.code_file_url if solution else None,
        "language": solution.language if solution else None,
        "difficulty": problem.difficulty,
        "tags": tags,
        "problem": {
            "type": "pdf" if problem.problem_pdf_url else "text",
            "content": problem.problem_pdf_url if problem.problem_pdf_url else problem.title,
            "title": problem.title,
            "description": explanation.content[:100] if explanation else None,
        },
    }
    return APIResponse.success(data=lecture, status_code=status.HTTP_200_OK)
