# ============================
# backend/app/core/celery_app.py
# ============================
from celery import Celery
from celery.schedules import crontab
from app.config import settings

celery_app = Celery(
    "cfc_deblocages",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
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