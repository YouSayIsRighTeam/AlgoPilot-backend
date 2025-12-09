import asyncio
from app.core.celery_app import celery_app
from app.services.llm_service import llm_service

@celery_app.task(name="generate_text_task")
def generate_text_task(prompt: str, max_tokens: int, temperature: float):
    print(f"[Worker] Processing: {prompt[:10]}...")
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            return loop.run_until_complete(llm_service.generate_text(prompt, max_tokens, temperature))
        else:
            return asyncio.run(llm_service.generate_text(prompt, max_tokens, temperature))
    except Exception as e:
        return f"Error: {str(e)}"