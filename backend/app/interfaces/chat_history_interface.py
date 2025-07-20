from abc import ABC, abstractmethod
from typing import List, Dict

class ChatHistoryServiceInterface(ABC):
    @abstractmethod
    def save_message(self, user_id: int, message_type: str, content: str, session_id: str):
        pass

    @abstractmethod
    def get_recent_history(self, user_id: int, session_id: str, limit: int = 10):
        pass

    @abstractmethod
    def get_recent_history_as_dict(self, user_id: int, session_id: str, limit: int = 10) -> List[Dict[str, str]]:
        pass
