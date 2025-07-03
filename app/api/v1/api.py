from fastapi import APIRouter

from app.api.v1.endpoints import explanations, lectures, problems, solutions

api_router = APIRouter()
api_router.include_router(problems.router, prefix="/problems", tags=["problems"])
api_router.include_router(solutions.router, prefix="/solutions", tags=["solutions"])
api_router.include_router(explanations.router, prefix="/explanations", tags=["explanations"])
api_router.include_router(lectures.router, prefix="/lectures", tags=["lectures"])
