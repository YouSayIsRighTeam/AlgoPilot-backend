from fastapi import APIRouter
from app.api.v1.endpoints import system, problems, submission, llm_service

api_router = APIRouter()
api_router.include_router(system.router, prefix="/system", tags=["System"])
api_router.include_router(problems.router, prefix="/problems", tags=["Problems"])
api_router.include_router(submission.router, prefix="/submission", tags=["Submission"])
api_router.include_router(llm_service.router, prefix="/llm", tags=["LLM"])