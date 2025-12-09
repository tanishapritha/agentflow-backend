import json
from typing import Any, Dict
from app.tools.base import BaseTool
from app.llm.openai_provider import OpenAIProvider

class QuizGeneratorTool(BaseTool):
    name = "quiz_generator"
    description = "Generates a multiple choice quiz from text."

    def __init__(self, llm_provider: OpenAIProvider = None):
        self.llm = llm_provider or OpenAIProvider()

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        text_content = inputs.get("text_content", "")
        if not text_content:
            return []

        prompt = f"""
        Generate a quiz based on the following text.
        Return strictly a JSON array of objects. 
        Each object must have:
        - "question": string
        - "options": list of strings (4 options)
        - "answer": string (the correct option content)

        Text:
        {text_content[:2000]}  # limit context for now
        """

        response = self.llm.generate(prompt, system_prompt="You are a quiz generator. Output ONLY JSON.")
        
        # Clean up potential markdown formatting
        cleaned_response = response.strip()
        if cleaned_response.startswith("```json"):
            cleaned_response = cleaned_response[7:]
        if cleaned_response.endswith("```"):
            cleaned_response = cleaned_response[:-3]
        
        try:
            quiz_data = json.loads(cleaned_response)
            return quiz_data
        except json.JSONDecodeError:
            return [{"error": "Failed to parse LLM output", "raw": response}]
