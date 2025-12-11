# app/services/llm_service.py
import json
from openai import AsyncOpenAI, APIConnectionError
from app.core.config import settings
from typing import Optional
import datetime

class LLMService:
    def __init__(self):
        self.client = AsyncOpenAI(
            base_url=settings.LLM_BASE_URL,
            api_key=settings.LLM_API_KEY
        )
        self.model_id: str = settings.LLM_DEFAULT_MODEL
    async def _ensure_model_id(self):
        try:
            models_list = await self.client.models.list()
            
            if models_list.data:
                found_model = models_list.data[0].id
                self.model_id = found_model
            else:
                print("No models found, using default.")
                
        except Exception as e:
            print(f"Failed to fetch models from vLLM: {e}")
            pass
    async def generate_text(self, prompt: str, max_tokens: int = 1000, temperature: float = 0.3, return_json: bool = True) -> str:
        await self._ensure_model_id()
        try:
            timestamp = datetime.datetime.now().isoformat()
            response = await self.client.chat.completions.create(
                model=self.model_id,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Output the final answer only. Do NOT output any explanations or additional text."
                            "Thank you"
                            f"{timestamp}"
                        )
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=max_tokens,
                temperature=temperature,
            )
            
            raw = response.choices[0].message.content.strip()
            if "assistantfinal" in raw.lower():
                final_answer = raw.split("assistantfinal")[-1].strip()
                raw = final_answer
            else:
                raw = raw.strip()

            print("=== Response ===")
            print(raw)
            return raw
        except Exception as e:
            print(f"LLM Generation Error: {e}")
            return f"An error occurred: {str(e)}"

llm_service = LLMService()