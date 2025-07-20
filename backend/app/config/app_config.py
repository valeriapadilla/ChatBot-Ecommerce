import os
from typing import List
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    
    app_name: str = "RAG Chat API"
    app_version: str = "1.0.0"
    app_description: str = "A Retrieval-Augmented Generation (RAG) powered chat API"
    
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True
    log_level: str = "info"

    cors_origins: List[str] = ["*"]
    cors_credentials: bool = True
    cors_methods: List[str] = ["*"]
    cors_headers: List[str] = ["*"]
    
    api_prefix: str = "/api/v1"
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"

    postgres_host: str = ""
    postgres_port: str = ""
    postgres_user: str = ""
    postgres_password: str = ""
    postgres_db: str = ""

    openai_api_key: str = ""

    jwt_secret_key: str = ""
    jwt_algorithm: str = ""
    jwt_access_token_expire_minutes: int = 0
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    def __post_init__(self):
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required in environment variables")
        
        if not all([self.postgres_host, self.postgres_user, self.postgres_password, self.postgres_db]):
            raise ValueError("Database configuration is incomplete. Check environment variables.")
        
        if not self.jwt_secret_key or not self.jwt_algorithm or not self.jwt_access_token_expire_minutes:
            raise ValueError("JWT configuration is incomplete. Check environment variables.")

app_settings = AppSettings() 