# backend/app/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

from app.config import settings
from app.database import engine
from app.api.v1.api import api_router
from app.core.i18n import setup_i18n, get_translation
from app.core.celery_app import celery_app
import redis.asyncio as redis
from contextlib import asynccontextmanager
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestion du cycle de vie de l'application
    """
    # Startup
    logger.info("Starting up CFC Déblocages application...")
    
    # Initialize Redis for rate limiting
    redis_client = redis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis_client)
    
    # Setup i18n
    setup_i18n()
    
    # Initialize database tables
    # Note: In production, use Alembic migrations instead
    # from app.models import Base
    # Base.metadata.create_all(bind=engine)
    
    yield
    
    # Shutdown
    logger.info("Shutting down CFC Déblocages application...")
    await redis_client.close()


# Create FastAPI instance
app = FastAPI(
    title="CFC Déblocages API",
    description="API de gestion des déblocages du Crédit Foncier du Cameroun",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Add middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

if settings.ENVIRONMENT == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.ALLOWED_HOSTS
    )

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception handler caught: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "message": str(exc) if settings.DEBUG else "Une erreur s'est produite"
        }
    )

# Root endpoint
@app.get("/")
async def root(request: Request):
    _ = get_translation(request)
    return {
        "message": _("Bienvenue sur l'API CFC Déblocages"),
        "version": "1.0.0",
        "documentation": "/api/docs"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "cfc-deblocages-api",
        "version": "1.0.0"
    }

# Include API router
app.include_router(api_router, prefix="/api/v1")

# ============================
# backend/app/config.py
# ============================
import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, validator


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
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
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
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()