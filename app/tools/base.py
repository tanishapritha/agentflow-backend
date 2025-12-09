from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseTool(ABC):
    name: str = "base_tool"
    description: str = "Base tool description"

    @abstractmethod
    def run(self, inputs: Dict[str, Any]) -> Any:
        pass
