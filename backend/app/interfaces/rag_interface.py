from abc import ABC, abstractmethod
from typing import List, Dict

class RAGServiceInterface(ABC):
    @abstractmethod
    def ask(self, user_id: str, message: str, history: List[Dict[str, str]] = None) -> str:
        pass
