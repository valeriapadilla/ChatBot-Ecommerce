import time
import logging
from typing import Callable
from fastapi import Request, Response
from app.config.app_config import app_settings

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware:
    """Middleware for logging HTTP requests."""
    
    def __init__(self, app: Callable):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            start_time = time.time()
            
            # Log request
            logger.info(f"Request: {scope['method']} {scope['path']}")
            
            # Process request
            await self.app(scope, receive, send)
            
            # Log response time
            process_time = time.time() - start_time
            logger.info(f"Response: {scope['method']} {scope['path']} - {process_time:.3f}s")
        else:
            await self.app(scope, receive, send)


class CORSMiddleware:
    """Custom CORS middleware."""
    
    def __init__(self, app: Callable):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            # Add CORS headers
            headers = dict(scope.get("headers", []))
            
            # Allow all origins for development
            headers[b"access-control-allow-origin"] = b"*"
            headers[b"access-control-allow-methods"] = b"*"
            headers[b"access-control-allow-headers"] = b"*"
            
            scope["headers"] = [(k, v) for k, v in headers.items()]
        
        await self.app(scope, receive, send) 