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
    
    yield
    
    # Shutdown
    logger.info("Shutting down CFC Déblocages application...")
    await redis_client.close()

# Create FastAPI instance avec encodage UTF-8 explicite
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
        },
        media_type="application/json; charset=utf-8"  # Encodage explicite
    )

# Root endpoint avec encodage correct
@app.get("/")
async def root(request: Request):
    return JSONResponse(
        content={
            "message": "Bienvenue sur l'API CFC Déblocages",
            "version": "1.0.0",
            "documentation": "/api/docs"
        },
        media_type="application/json; charset=utf-8"
    )

# Health check endpoint
@app.get("/health")
async def health_check():
    return JSONResponse(
        content={
            "status": "healthy",
            "service": "cfc-deblocages-api",
            "version": "1.0.0"
        },
        media_type="application/json; charset=utf-8"
    )

# Include API router
app.include_router(api_router, prefix="/api/v1")