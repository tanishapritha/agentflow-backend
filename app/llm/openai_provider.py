import os
from typing import Optional
from openai import OpenAI
from app.llm.base_provider import BaseLLMProvider
from app.config import settings
from app.utils.logger import logger

class OpenAIProvider(BaseLLMProvider):
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        if not self.api_key:
            logger.warning("OPENAI_API_KEY not found. LLM calls will fail or return mock data.")
            self.client = None
        else:
            self.client = OpenAI(api_key=self.api_key)

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        if not self.client:
            return "MOCK OUTPUT: OpenAI API Key missing. Please config .env"
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini", # Using a fast modern model
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI Generate Error: {e}")
            return f"Error generating content: {e}"
