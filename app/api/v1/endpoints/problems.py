from fastapi import APIRouter, HTTPException
from app.services.crawler import leetcode_crawler

router = APIRouter()

@router.get("/{problem_title}")
async def fetch_problem(problem_title: str):
    """
    獲取 LeetCode 題目資料 (by problem title)
    Example: GET /api/v1/problems/two-sum
    """
    result = await leetcode_crawler.get_problem_detail(problem_title)
    
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
        
    return result

@router.get("/id/{problem_id}")
async def fetch_problem_by_id(problem_id: str):
    """
    根據 ID 獲取題目 
    Example: GET /api/v1/problems/id/1)
    """
    result = await leetcode_crawler.get_problem_by_id(problem_id)
    
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
        
    return result