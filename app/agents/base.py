from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseAgent(ABC):
    @abstractmethod
    def run(self, inputs: Dict[str, Any]) -> Any:
        pass
