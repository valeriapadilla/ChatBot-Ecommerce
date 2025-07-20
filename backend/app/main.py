from app.core.app_factory import AppFactory

# Create FastAPI application
app = AppFactory.create_app()

if __name__ == "__main__":
    import uvicorn
    from app.config.app_config import app_settings
    
    uvicorn.run(
        "app.main:app",
        host=app_settings.host,
        port=app_settings.port,
        reload=app_settings.reload,
        log_level=app_settings.log_level
    )
