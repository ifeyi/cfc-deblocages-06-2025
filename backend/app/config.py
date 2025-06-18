# ============================
# backend/app/config.py
# ============================
import os
from typing import List, Optional
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, validator

def get_secret(secret_name: str, default: str = None) -> str:
    """
    Get secret from Docker secrets file or environment variable.
    
    Args:
        secret_name: Name of the secret (without _FILE suffix)
        default: Default value if neither secret file nor env var exists
    
    Returns:
        Secret value as string
    """
    # Check if there's a _FILE environment variable pointing to a secret file
    secret_file_path = os.getenv(f"{secret_name.upper()}_FILE")
    
    if secret_file_path and Path(secret_file_path).exists():
        try:
            with open(secret_file_path, 'r') as f:
                return f.read().strip()
        except Exception as e:
            print(f"Error reading secret file {secret_file_path}: {e}")
    
    # Fallback to regular environment variable
    return os.getenv(secret_name.upper(), default)

class Settings(BaseSettings):
    # Application settings
    PROJECT_NAME: str = "CFC Déblocages"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False

    # API settings
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "change-this-secret-key-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    ALGORITHM: str = "HS256"

    # Database
    DATABASE_URL: str = "postgresql://cfc_user:password@localhost:5432/cfc_deblocages"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # MinIO
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "admin"
    MINIO_SECRET_KEY: str = "password"
    MINIO_BUCKET_NAME: str = "cfc-documents"
    MINIO_SECURE: bool = False

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000", 
        "http://localhost"
    ]

    # Security
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1"]

    # Email
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = 587
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[str] = None
    EMAILS_FROM_NAME: Optional[str] = "CFC Déblocages"

    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    # i18n
    DEFAULT_LANGUAGE: str = "fr"
    SUPPORTED_LANGUAGES: List[str] = ["fr", "en"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Override settings with secrets if available
        self._load_secrets()
    
    def _load_secrets(self):
        """Load secrets from Docker secrets or environment variables"""
        
        # Load secret key
        secret_key = get_secret("secret_key")
        if secret_key:
            self.SECRET_KEY = secret_key
        
        # Load database password and rebuild DATABASE_URL
        db_password = get_secret("db_password")
        if db_password:
            # Parse existing DATABASE_URL to get components
            db_user = os.getenv("DB_USER", "cfc_user")
            db_name = os.getenv("DB_NAME", "cfc_deblocages")
            db_host = os.getenv("DB_HOST", "postgres")
            db_port = os.getenv("DB_PORT", "5432")
            
            self.DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        
        # Load Redis password and rebuild REDIS_URL
        redis_password = get_secret("redis_password")
        if redis_password:
            redis_host = os.getenv("REDIS_HOST", "redis")
            redis_port = os.getenv("REDIS_PORT", "6379")
            redis_db = os.getenv("REDIS_DB", "0")
            
            self.REDIS_URL = f"redis://:{redis_password}@{redis_host}:{redis_port}/{redis_db}"
            self.CELERY_BROKER_URL = self.REDIS_URL
            self.CELERY_RESULT_BACKEND = self.REDIS_URL
        
        # Load MinIO secret key
        minio_secret = get_secret("minio_secret_key")
        if minio_secret:
            self.MINIO_SECRET_KEY = minio_secret
        
        # Load SMTP password
        smtp_password = get_secret("smtp_password")
        if smtp_password:
            self.SMTP_PASSWORD = smtp_password

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()