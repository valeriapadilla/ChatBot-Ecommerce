from datetime import datetime, timedelta
from typing import Set, Optional
import jwt
from app.config.app_config import app_settings

class TokenBlacklistService:
    """Service to manage blacklisted JWT tokens"""
    
    def __init__(self):
        self._blacklisted_tokens: Set[str] = set()
    
    def add_to_blacklist(self, token: str) -> None:
        """Add a token to the blacklist"""
        self._blacklisted_tokens.add(token)
    
    def is_blacklisted(self, token: str) -> bool:
        """Check if a token is blacklisted"""
        return token in self._blacklisted_tokens
    
    def cleanup_expired_tokens(self) -> None:
        """Remove expired tokens from blacklist"""
        current_time = datetime.utcnow()
        tokens_to_remove = set()
        
        for token in self._blacklisted_tokens:
            try:
                payload = jwt.decode(
                    token, 
                    app_settings.jwt_secret_key, 
                    algorithms=[app_settings.jwt_algorithm]
                )
                exp_timestamp = payload.get('exp')
                if exp_timestamp:
                    exp_time = datetime.fromtimestamp(exp_timestamp)
                    if exp_time < current_time:
                        tokens_to_remove.add(token)
            except jwt.PyJWTError:
                # Invalid token, remove it
                tokens_to_remove.add(token)
        
        self._blacklisted_tokens -= tokens_to_remove

token_blacklist = TokenBlacklistService() 