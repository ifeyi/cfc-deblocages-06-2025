# ============================
# backend/app/tasks.py
# ============================
from celery import shared_task
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.alert_service import AlertService
from app.services.notification_service import NotificationService
import logging

logger = logging.getLogger(__name__)

@shared_task
def check_all_alerts():
    """
    Tâche périodique pour vérifier toutes les alertes
    """
    logger.info("Starting alert check task")
    db = SessionLocal()
    try:
        alert_service = AlertService(db)
        alert_service.check_all_alerts()
        logger.info("Alert check completed successfully")
        return "Alert check completed"
    except Exception as e:
        logger.error(f"Error in alert check task: {e}")
        raise
    finally:
        db.close()

@shared_task
def send_alert_notifications(alert_id: int):
    """
    Envoyer les notifications pour une alerte
    """
    logger.info(f"Sending notifications for alert {alert_id}")
    db = SessionLocal()
    try:
        notification_service = NotificationService(db)
        result = notification_service.send_alert_notifications(alert_id)
        logger.info(f"Notifications sent for alert {alert_id}: {result}")
        return result
    except Exception as e:
        logger.error(f"Error sending notifications for alert {alert_id}: {e}")
        raise
    finally:
        db.close()

@shared_task
def send_daily_report():
    """
    Envoyer le rapport quotidien
    """
    logger.info("Generating daily report")
    db = SessionLocal()
    try:
        # TODO: Implement daily report generation
        alert_service = AlertService(db)
        summary = alert_service.get_alerts_summary()
        logger.info(f"Daily report generated: {summary}")
        return f"Daily report completed: {summary}"
    except Exception as e:
        logger.error(f"Error generating daily report: {e}")
        raise
    finally:
        db.close()

@shared_task
def cleanup_old_alerts():
    """
    Nettoyer les anciennes alertes résolues
    """
    logger.info("Cleaning up old alerts")
    db = SessionLocal()
    try:
        # TODO: Implement cleanup logic
        # For now, just log
        logger.info("Old alerts cleanup completed")
        return "Cleanup completed"
    except Exception as e:
        logger.error(f"Error cleaning up alerts: {e}")
        raise
    finally:
        db.close()