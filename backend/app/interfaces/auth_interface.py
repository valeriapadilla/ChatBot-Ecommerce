from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from app.models.user import User

class AuthServiceInterface(ABC):
    @abstractmethod
    def hash_password(self, password: str) -> str:
        pass

    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        pass

    @abstractmethod
    def create_user(self, db: Session, email: str, password: str, name: str = None) -> User:
        pass

    @abstractmethod
    def authenticate_user(self, db: Session, email: str, password: str) -> User:
        pass

    @abstractmethod
    def get_user_by_email(self, db: Session, email: str) -> User:
        pass

    @abstractmethod
    def get_user_by_id(self, db: Session, user_id: int) -> User:
        pass
