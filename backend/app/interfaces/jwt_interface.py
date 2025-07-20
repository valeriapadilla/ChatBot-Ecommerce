from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from datetime import timedelta
from app.models.user import User

class JWTServiceInterface(ABC):
    @abstractmethod
    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        pass

    @abstractmethod
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def create_user_token(self, user: User) -> str:
        pass
