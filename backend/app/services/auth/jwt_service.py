import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from app.models.user import User
from app.config.app_config import app_settings
from app.interfaces.jwt_interface import JWTServiceInterface

SECRET_KEY = app_settings.jwt_secret_key
ALGORITHM = app_settings.jwt_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = app_settings.jwt_access_token_expire_minutes

class JWTService(JWTServiceInterface):
    @staticmethod
    def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> Optional[Dict[str, Any]]:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.PyJWTError:
            return None
    
    @staticmethod
    def create_user_token(user: User) -> str:
        return JWTService.create_access_token(
            data={"sub": str(user.id), "email": user.email, "role": user.role}
        ) 