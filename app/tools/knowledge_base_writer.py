import json
import os
from typing import Any, Dict
from app.tools.base import BaseTool

class KnowledgeBaseWriterTool(BaseTool):
    name = "knowledge_base_writer"
    description = "Writes data to a local knowledge base JSON file"

    def run(self, inputs: Dict[str, Any]) -> str:
        content = inputs.get("content")
        filename = inputs.get("filename", "knowledge_base.json")
        
        # In a real app we might append or update. here we just overwrite or create.
        try:
            with open(filename, "w", encoding='utf-8') as f:
                json.dump(content, f, indent=2)
            return f"Successfully wrote to {filename}"
        except Exception as e:
            return f"Failed to write KB: {e}"
