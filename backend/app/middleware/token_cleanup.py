from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.services.auth.jwt_service import JWTService
import time

class TokenCleanupMiddleware(BaseHTTPMiddleware):
    """Middleware to periodically cleanup expired tokens from blacklist"""
    
    def __init__(self, app, cleanup_interval: int = 3600):  # Default: 1 hour
        super().__init__(app)
        self.cleanup_interval = cleanup_interval
        self.last_cleanup = time.time()
    
    async def dispatch(self, request: Request, call_next):
        current_time = time.time()
        if current_time - self.last_cleanup > self.cleanup_interval:
            JWTService.cleanup_expired_tokens()
            self.last_cleanup = current_time
        
        response = await call_next(request)
        return response 