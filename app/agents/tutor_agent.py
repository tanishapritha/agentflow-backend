from typing import Dict, Any
from app.agents.base import BaseAgent
from app.llm.openai_provider import OpenAIProvider

class TutorAgent(BaseAgent):
    """
    Agent responsible for summarizing lessons and explaining concepts.
    """
    def __init__(self, llm_provider: OpenAIProvider = None):
        self.llm = llm_provider or OpenAIProvider()

    def run(self, inputs: Dict[str, Any]) -> str:
        text = inputs.get("text_content", "")
        task = inputs.get("task", "summarize")

        if task == "summarize":
            prompt = f"Summarize the following lesson content accurately and concisely:\n\n{text[:3000]}"
            return self.llm.generate(prompt, system_prompt="You are an expert tutor.")
        
        return "Unknown task"
