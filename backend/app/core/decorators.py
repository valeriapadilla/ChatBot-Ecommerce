import logging
import functools
from typing import Callable, Any
from fastapi import HTTPException

logger = logging.getLogger(__name__)

def handle_product_errors(func: Callable) -> Callable:
    """Decorator to handle common product service errors."""
    @functools.wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error in {func.__name__}")
    return wrapper

def handle_auth_errors(func: Callable) -> Callable:
    """Decorator to handle authentication errors."""
    @functools.wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        try:
            return await func(*args, **kwargs)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Authentication error in {func.__name__}: {str(e)}")
            raise HTTPException(status_code=401, detail="Authentication failed")
    return wrapper

def log_user_activity(user_id_field: str = "current_user"):
    """Decorator to log user activity."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            # Extract user_id from kwargs
            user = kwargs.get(user_id_field)
            user_id = user.id if user else "anonymous"
            
            logger.info(f"User {user_id} accessing {func.__name__}")
            result = await func(*args, **kwargs)
            logger.info(f"User {user_id} completed {func.__name__}")
            return result
        return wrapper
    return decorator 