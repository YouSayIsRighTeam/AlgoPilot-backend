# app/services/llm_service.py
import json
from openai import AsyncOpenAI, APIConnectionError
from app.core.config import settings
from typing import Optional
import datetime
import requests

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
        url = "http://ollma.coltengroup.org/api/chat"
        payload = {
            "model": "gpt-oss:120b-cloud",  
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "stream": False 
        }

        try:
            response = requests.post(url, json=payload)

            if response.status_code == 200:
                response_data = response.json()

                print("response:", response_data['message']['content'])
                return response_data['message']['content']
            else:
                print(f"Error: {response.status_code}")
                print(response.text)
                return response.text

        except requests.exceptions.ConnectionError:
            print("Error")
            return "error"

llm_service = LLMService()