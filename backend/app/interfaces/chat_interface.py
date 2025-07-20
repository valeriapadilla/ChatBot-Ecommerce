from abc import ABC, abstractmethod
from typing import List
from app.schemas.chat import ChatRequest, ChatMessage


class ChatServiceInterface(ABC):
    """Interface for chat service operations."""
    
    @abstractmethod
    def process_chat_request(self, request: ChatRequest) -> str:
        """Process a chat request and return the response."""
        pass


class HistoryConverterInterface(ABC):
    """Interface for history conversion operations."""
    
    @abstractmethod
    def convert_history(self, history: List[ChatMessage]) -> List[dict]:
        """Convert ChatMessage objects to dictionary format."""
        pass


class RequestValidatorInterface(ABC):
    """Interface for request validation operations."""
    
    @abstractmethod
    def validate_request(self, request: ChatRequest) -> None:
        """Validate chat request parameters."""
        pass 