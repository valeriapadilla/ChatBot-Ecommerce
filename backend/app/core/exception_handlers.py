import logging
from typing import Dict, Any
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from app.exceptions.chat_exceptions import ChatException, ChatValidationException, ChatProcessingException

logger = logging.getLogger(__name__)


class ExceptionHandlers:
    """Exception handlers for the application."""
    
    @staticmethod
    async def chat_exception_handler(request: Request, exc: ChatException) -> JSONResponse:
        """Handle chat-specific exceptions."""
        logger.error(f"Chat exception: {str(exc)}")
        return JSONResponse(
            status_code=500,
            content={
                "error": "Chat service error",
                "detail": str(exc),
                "type": "chat_error"
            }
        )
    
    @staticmethod
    async def validation_exception_handler(request: Request, exc: ChatValidationException) -> JSONResponse:
        """Handle validation exceptions."""
        logger.warning(f"Validation error: {str(exc)}")
        return JSONResponse(
            status_code=400,
            content={
                "error": "Validation error",
                "detail": str(exc),
                "type": "validation_error"
            }
        )
    
    @staticmethod
    async def processing_exception_handler(request: Request, exc: ChatProcessingException) -> JSONResponse:
        """Handle processing exceptions."""
        logger.error(f"Processing error: {str(exc)}")
        return JSONResponse(
            status_code=500,
            content={
                "error": "Processing error",
                "detail": str(exc),
                "type": "processing_error"
            }
        )
    
    @staticmethod
    async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        """Handle HTTP exceptions."""
        logger.error(f"HTTP error {exc.status_code}: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": "HTTP error",
                "detail": exc.detail,
                "status_code": exc.status_code
            }
        )
    
    @staticmethod
    async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """Handle general exceptions."""
        logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "detail": "An unexpected error occurred",
                "type": "internal_error"
            }
        ) 