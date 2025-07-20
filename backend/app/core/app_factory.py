import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.app_config import app_settings
from app.core.logging_config import LoggingConfig
from app.core.exception_handlers import ExceptionHandlers
from app.api.routers import chat, auth

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Starting RAG Chat API...")
    logger.info(f"Environment: {app_settings.app_name} v{app_settings.app_version}")
    yield
    # Shutdown
    logger.info("Shutting down RAG Chat API...")


class AppFactory:
    """Factory for creating FastAPI application."""
    
    @staticmethod
    def create_app() -> FastAPI:
        """Create and configure FastAPI application."""
        
        # Setup logging
        LoggingConfig.setup_logging()
        
        # Create FastAPI app
        app = FastAPI(
            title=app_settings.app_name,
            description=app_settings.app_description,
            version=app_settings.app_version,
            docs_url=app_settings.docs_url,
            redoc_url=app_settings.redoc_url,
            lifespan=lifespan
        )
        
        # Add CORS middleware
        app.add_middleware(
            CORSMiddleware,
            allow_origins=app_settings.cors_origins,
            allow_credentials=app_settings.cors_credentials,
            allow_methods=app_settings.cors_methods,
            allow_headers=app_settings.cors_headers,
        )
        
        # Register exception handlers
        AppFactory._register_exception_handlers(app)
        
        # Include routers
        AppFactory._include_routers(app)
        
        # Add root endpoint
        AppFactory._add_root_endpoint(app)
        
        logger.info("FastAPI application created successfully")
        return app
    
    @staticmethod
    def _register_exception_handlers(app: FastAPI) -> None:
        """Register exception handlers."""
        from app.exceptions.chat_exceptions import ChatException, ChatValidationException, ChatProcessingException
        
        app.add_exception_handler(ChatException, ExceptionHandlers.chat_exception_handler)
        app.add_exception_handler(ChatValidationException, ExceptionHandlers.validation_exception_handler)
        app.add_exception_handler(ChatProcessingException, ExceptionHandlers.processing_exception_handler)
        app.add_exception_handler(Exception, ExceptionHandlers.general_exception_handler)
        
        logger.info("Exception handlers registered")
    
    @staticmethod
    def _include_routers(app: FastAPI) -> None:
        """Include API routers."""
        app.include_router(auth.router, prefix=app_settings.api_prefix)
        app.include_router(chat.router, prefix=app_settings.api_prefix)
        logger.info(f"Routers included with prefix: {app_settings.api_prefix}")
    
    @staticmethod
    def _add_root_endpoint(app: FastAPI) -> None:
        """Add root endpoint with API information."""
        
        @app.get("/")
        async def root():
            """Root endpoint with API information."""
            return {
                "message": app_settings.app_name,
                "version": app_settings.app_version,
                "description": app_settings.app_description,
                "endpoints": {
                    "chat": f"{app_settings.api_prefix}/chat",
                    "docs": app_settings.docs_url,
                    "health": f"{app_settings.api_prefix}/chat/health"
                }
            }
        
        @app.get("/health")
        async def health_check():
            """Global health check endpoint."""
            return {
                "status": "healthy",
                "service": "rag-chat-api",
                "version": app_settings.app_version
            }
        
        logger.info("Root endpoints added") 