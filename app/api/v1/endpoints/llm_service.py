# app/api/v1/endpoints/llm.py
from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel
from app.services.llm_service import llm_service
from celery.result import AsyncResult
from app.worker.tasks import generate_text_task

router = APIRouter()

API_KEY = "ouo"

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

class LLMRequest(BaseModel):
    prompt: str
    max_tokens: int = 1000
    temperature: float = 0.3
    return_json: bool = False

class LLMResponse(BaseModel):
    generated_text: str
    used_model: str

@router.post("/generate-async", dependencies=[Depends(verify_api_key)])
async def generate_text_async(request: LLMRequest):
    """
    Put LLM request to queue (Retuen: task's ID)
    """
    task = generate_text_task.delay(
        prompt=request.prompt,
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        return_json=request.return_json
    )
    
    return {
        "task_id": task.id,
        "status": "Queued",
        "message": "The task has been scheduled. Please use [task_id] to query the results."
    }

@router.get("/result/{task_id}")
async def get_task_result(task_id: str):
    """
    query result by task's ID
    """
    task_result = AsyncResult(task_id)
    
    response = {
        "task_id": task_id,
        "status": task_result.status, # PENDING, STARTED, SUCCESS, FAILURE
        "result": None
    }

    if task_result.ready():
        if task_result.successful():
            response["result"] = task_result.result
        else:
            response["status"] = "FAILURE"
            response["error"] = str(task_result.result)
    
    return response

@router.post("/generate")
async def generate_text(request: LLMRequest):
    """
    call LLM with prompt
    """
    result = await llm_service.generate_text(prompt=request.prompt)

    print("result:", result)

    return {
        "generated_text": result
    }