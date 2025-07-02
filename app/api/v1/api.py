from fastapi import APIRouter

from app.api.v1.endpoints import explanations, problems, search_lecture, solutions

api_router = APIRouter()
api_router.include_router(problems.router, prefix="/problems", tags=["problems"])
api_router.include_router(solutions.router, prefix="/solutions", tags=["solutions"])
api_router.include_router(explanations.router, prefix="/explanations", tags=["explanations"])
api_router.include_router(search_lecture.router, prefix="", tags=["search_lecture"])
