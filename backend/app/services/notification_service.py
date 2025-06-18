# ============================
# backend/app/services/notification_service.py
# ============================
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging
from sqlalchemy.orm import Session
from app.models import Alert, Loan, Client

logger = logging.getLogger(__name__)


class NotificationService:
    def __init__(self, db: Session):
        self.db = db
    
    def send_email_notification(self, to_email: str, subject: str, message: str) -> bool:
        """
        Send email notification
        """
        try:
            # TODO: Implement actual email sending logic (SMTP, SendGrid, etc.)
            # For now, just log the notification
            logger.info(f"📧 Email notification sent to {to_email}")
            logger.info(f"📧 Subject: {subject}")
            logger.info(f"📧 Message: {message}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email notification: {str(e)}")
            return False
    
    def send_sms_notification(self, phone_number: str, message: str) -> bool:
        """
        Send SMS notification
        """
        try:
            # TODO: Implement actual SMS sending logic (Twilio, etc.)
            # For now, just log the notification
            logger.info(f"📱 SMS notification sent to {phone_number}")
            logger.info(f"📱 Message: {message}")
            return True
        except Exception as e:
            logger.error(f"Failed to send SMS notification: {str(e)}")
            return False
    
    def send_push_notification(self, user_id: int, title: str, message: str) -> bool:
        """
        Send push notification
        """
        try:
            # TODO: Implement actual push notification logic (Firebase, etc.)
            # For now, just log the notification
            logger.info(f"🔔 Push notification sent to user {user_id}")
            logger.info(f"🔔 Title: {title}")
            logger.info(f"🔔 Message: {message}")
            return True
        except Exception as e:
            logger.error(f"Failed to send push notification: {str(e)}")
            return False
    
    def send_alert_notifications(self, alert_id: int) -> Dict[str, bool]:
        """
        Send notifications for a specific alert (called from tasks.py)
        This is the main method called by the Celery task
        """
        try:
            # Get alert details from database
            alert = self.db.query(Alert).filter(Alert.id == alert_id).first()
            if not alert:
                logger.error(f"Alert {alert_id} not found")
                return {"error": True, "message": "Alert not found"}
            
            # Get loan and client information
            loan = self.db.query(Loan).filter(Loan.id == alert.loan_id).first()
            if not loan:
                logger.error(f"Loan {alert.loan_id} not found for alert {alert_id}")
                return {"error": True, "message": "Loan not found"}
            
            client = self.db.query(Client).filter(Client.id == loan.client_id).first()
            if not client:
                logger.error(f"Client {loan.client_id} not found for loan {loan.id}")
                return {"error": True, "message": "Client not found"}
            
            # Prepare notification content
            subject = f"🚨 Alerte CFC - {alert.alert_type.value}"
            message = self._format_alert_message(alert, loan, client)
            
            results = {}
            
            # Send email notification
            if client.email:
                results['email'] = self.send_email_notification(
                    to_email=client.email,
                    subject=subject,
                    message=message
                )
            
            # Send SMS notification if phone number available
            if client.phone:
                sms_message = self._format_sms_message(alert, loan, client)
                results['sms'] = self.send_sms_notification(
                    phone_number=client.phone,
                    message=sms_message
                )
            
            # Send push notification (if user has app)
            results['push'] = self.send_push_notification(
                user_id=client.id,
                title=f"Alerte - {alert.alert_type.value}",
                message=alert.message
            )
            
            # Also notify admin/managers
            results['admin_email'] = self.send_email_notification(
                to_email="admin@cfc-deblocages.com",  # TODO: Configure admin email
                subject=f"[CFC Admin] {subject}",
                message=self._format_admin_message(alert, loan, client)
            )
            
            logger.info(f"✅ Alert notifications sent for alert {alert_id}: {results}")
            return results
            
        except Exception as e:
            logger.error(f"Failed to send alert notifications for alert {alert_id}: {str(e)}")
            return {"error": True, "message": str(e)}
    
    def _format_alert_message(self, alert: Alert, loan: Loan, client: Client) -> str:
        """
        Format alert message for email
        """
        return f"""
Bonjour {client.first_name} {client.last_name},

Une alerte a été générée concernant votre dossier de prêt :

📋 Détails de l'alerte :
- Type : {alert.alert_type.value}
- Niveau : {alert.severity}
- Message : {alert.message}
- Date : {alert.created_at.strftime('%d/%m/%Y %H:%M')}

📄 Informations du prêt :
- Numéro de dossier : {loan.id}
- Type de prêt : {loan.loan_type}
- Montant : {loan.amount:,.0f} FCFA

ℹ️ Actions recommandées :
{self._get_recommended_actions(alert)}

Pour plus d'informations, veuillez contacter votre conseiller ou vous connecter à votre espace client.

Cordialement,
L'équipe CFC Déblocages
        """.strip()
    
    def _format_sms_message(self, alert: Alert, loan: Loan, client: Client) -> str:
        """
        Format alert message for SMS (shorter version)
        """
        severity_emoji = "🔴" if alert.severity == "RED" else "🟠"
        return f"{severity_emoji} CFC Alert: {alert.message} - Dossier #{loan.id}. Contactez votre conseiller."
    
    def _format_admin_message(self, alert: Alert, loan: Loan, client: Client) -> str:
        """
        Format alert message for admin notifications
        """
        return f"""
Nouvelle alerte générée dans le système CFC Déblocages :

🚨 Détails de l'alerte :
- ID : {alert.id}
- Type : {alert.alert_type.value}
- Niveau : {alert.severity}
- Message : {alert.message}
- Statut : {alert.status.value}
- Créée le : {alert.created_at.strftime('%d/%m/%Y %H:%M')}

👤 Client concerné :
- Nom : {client.first_name} {client.last_name}
- Email : {client.email}
- Téléphone : {client.phone}

💰 Prêt concerné :
- ID : {loan.id}
- Type : {loan.loan_type}
- Montant : {loan.amount:,.0f} FCFA
- Statut : {loan.status.value}

Veuillez prendre les mesures appropriées.

Système CFC Déblocages
        """.strip()
    
    def _get_recommended_actions(self, alert: Alert) -> str:
        """
        Get recommended actions based on alert type
        """
        action_map = {
            "VALIDITY_WARNING": "• Contactez votre conseiller pour renouveler l'offre\n• Préparez les documents manquants",
            "VALIDITY_CRITICAL": "• URGENT: Contactez immédiatement votre conseiller\n• L'offre expire très bientôt",
            "WORK_DELAY_WARNING": "• Vérifiez l'avancement des travaux\n• Contactez votre entrepreneur",
            "REPAYMENT_UPCOMING": "• Préparez votre premier remboursement\n• Vérifiez votre compte bancaire",
            "REPAYMENT_IMMINENT": "• URGENT: Premier remboursement dans quelques jours\n• Assurez-vous d'avoir les fonds nécessaires"
        }
        
        return action_map.get(alert.alert_type.value, "• Contactez votre conseiller pour plus d'informations")
    
    def get_notification_preferences(self, user_id: int) -> Dict[str, bool]:
        """
        Get user notification preferences
        """
        # TODO: Implement actual preferences retrieval from database
        # For now, return default preferences
        return {
            "email": True,
            "sms": False,
            "push": True
        }
    
    def update_notification_preferences(self, user_id: int, preferences: Dict[str, bool]) -> bool:
        """
        Update user notification preferences
        """
        try:
            # TODO: Implement actual preferences update in database
            logger.info(f"Updated notification preferences for user {user_id}: {preferences}")
            return True
        except Exception as e:
            logger.error(f"Failed to update notification preferences: {str(e)}")
            return False