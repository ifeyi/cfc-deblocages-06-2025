# ============================
# backend/app/core/celery_app.py
# ============================
import os
from pathlib import Path
from celery import Celery
from celery.schedules import crontab
from urllib.parse import quote_plus

def get_secret(secret_name: str, default: str = None) -> str:
    """Get secret from Docker secrets file or environment variable."""
    secret_file_path = os.getenv(f"{secret_name.upper()}_FILE")
    if secret_file_path and Path(secret_file_path).exists():
        try:
            with open(secret_file_path, 'r') as f:
                return f.read().strip()
        except Exception as e:
            print(f"Error reading secret file {secret_file_path}: {e}")
            return os.getenv(secret_name.upper(), default)
    return os.getenv(secret_name.upper(), default)

def get_redis_url() -> str:
    """Build Redis URL with secrets support and proper URL encoding."""
    redis_password = get_secret("redis_password")
    redis_host = os.getenv("REDIS_HOST", "redis")
    redis_port = os.getenv("REDIS_PORT", "6379")
    redis_db = os.getenv("REDIS_DB", "0")
    
    if redis_password:
        # URL encode the password to handle special characters
        encoded_password = quote_plus(redis_password)
        redis_url = f"redis://:{encoded_password}@{redis_host}:{redis_port}/{redis_db}"
        print(f"Using Redis URL with password: redis://:***@{redis_host}:{redis_port}/{redis_db}")
    else:
        redis_url = f"redis://{redis_host}:{redis_port}/{redis_db}"
        print(f"Using Redis URL without password: {redis_url}")
    
    return redis_url

# Get Redis URL
redis_url = get_redis_url()

# If we couldn't build from secrets, use a fallback
if not redis_url or redis_url == "redis://redis:6379/0":
    redis_url = "redis://redis:6379/0"

celery_app = Celery(
    "cfc_deblocages",
    broker=redis_url,
    backend=redis_url,
    include=['app.tasks']
)

# Configure Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Africa/Douala',
    enable_utc=True,
    beat_schedule={
        'check-alerts-every-hour': {
            'task': 'app.tasks.check_all_alerts',
            'schedule': crontab(minute=0),  # Every hour
        },
        'send-daily-report': {
            'task': 'app.tasks.send_daily_report',
            'schedule': crontab(hour=8, minute=0),  # Every day at 8 AM
        },
        'cleanup-old-alerts': {
            'task': 'app.tasks.cleanup_old_alerts',
            'schedule': crontab(hour=2, minute=0),  # Every day at 2 AM
        },
    }
)