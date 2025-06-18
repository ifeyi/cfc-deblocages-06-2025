# ============================
# backend/app/services/alert_service.py
# ============================
from typing import List, Optional, Dict
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models import Alert, Loan, Disbursement, AlertType, AlertStatus
from app.models.loan import LoanStatus
from app.models.disbursement import DisbursementStatus
import logging

logger = logging.getLogger(__name__)


class AlertService:
    def __init__(self, db: Session):
        self.db = db
    
    def check_all_alerts(self):
        """
        Vérifier tous les prêts et créer des alertes si nécessaire
        """
        self._check_validity_alerts()
        self._check_disbursement_alerts()
        self._check_repayment_alerts()
    
    def _check_validity_alerts(self):
        """
        Vérifier les alertes de validité des offres
        """
        active_loans = self.db.query(Loan).filter(
            Loan.status.in_([LoanStatus.APPROVED, LoanStatus.IN_PROGRESS])
        ).all()
        
        for loan in active_loans:
            days_remaining = (loan.validity_end_date - datetime.now()).days
            
            # Determine alert threshold based on loan type
            if 'CLASSIQUE' in loan.loan_type:
                orange_threshold = 40  # 2/3 of 60 days
                red_threshold = 5
            else:
                orange_threshold = 60  # 2/3 of 90 days
                red_threshold = 5
            
            if days_remaining <= red_threshold and days_remaining > 0:
                self._create_alert(
                    loan.id,
                    AlertType.VALIDITY_CRITICAL,
                    "RED",
                    f"URGENT: L'offre de prêt expire dans {days_remaining} jours!"
                )
            elif days_remaining <= orange_threshold and days_remaining > red_threshold:
                self._create_alert(
                    loan.id,
                    AlertType.VALIDITY_WARNING,
                    "ORANGE",
                    f"Attention: Il reste {days_remaining} jours avant l'expiration de l'offre"
                )
    
    def _check_disbursement_alerts(self):
        """
        Vérifier les alertes de déblocage
        """
        active_disbursements = self.db.query(Disbursement).join(Loan).filter(
            Disbursement.status == DisbursementStatus.IN_PROGRESS,
            Loan.status == LoanStatus.DISBURSING
        ).all()
        
        for disbursement in active_disbursements:
            loan = disbursement.loan
            
            # Check work progress vs time elapsed
            if disbursement.request_date:
                days_elapsed = (datetime.now() - disbursement.request_date).days
                expected_completion = min(days_elapsed * 3, 100)  # 3% per day expected
                
                if disbursement.work_completion_percentage < expected_completion - 20:
                    self._create_alert(
                        loan.id,
                        AlertType.WORK_DELAY_WARNING,
                        "ORANGE",
                        f"Retard constaté sur les travaux: {disbursement.work_completion_percentage}% réalisé"
                    )
    
    def _check_repayment_alerts(self):
        """
        Vérifier les alertes de remboursement
        """
        loans_with_grace = self.db.query(Loan).filter(
            Loan.status == LoanStatus.DISBURSING,
            Loan.grace_period_months > 0,
            Loan.first_payment_date.isnot(None)
        ).all()
        
        for loan in loans_with_grace:
            # Calculate end of grace period
            grace_end = loan.first_payment_date + timedelta(days=30 * loan.grace_period_months)
            days_until_payment = (grace_end - datetime.now()).days
            
            if days_until_payment <= 30 and days_until_payment > 0:
                self._create_alert(
                    loan.id,
                    AlertType.REPAYMENT_UPCOMING,
                    "ORANGE",
                    f"Le remboursement commence dans {days_until_payment} jours"
                )
            elif days_until_payment <= 7 and days_until_payment > 0:
                self._create_alert(
                    loan.id,
                    AlertType.REPAYMENT_IMMINENT,
                    "RED",
                    f"URGENT: Le remboursement commence dans {days_until_payment} jours!"
                )
    
    def _create_alert(self, loan_id: int, alert_type: AlertType, severity: str, message: str):
        """
        Créer une alerte si elle n'existe pas déjà
        """
        existing = self.db.query(Alert).filter(
            Alert.loan_id == loan_id,
            Alert.alert_type == alert_type,
            Alert.status != AlertStatus.RESOLVED
        ).first()
        
        if not existing:
            alert = Alert(
                loan_id=loan_id,
                alert_type=alert_type,
                severity=severity,
                message=message
            )
            self.db.add(alert)
            self.db.commit()
            
            # Import here to avoid circular imports
            from app.tasks import send_alert_notifications
            
            # Schedule notification using Celery task
            send_alert_notifications.delay(alert.id)
            logger.info(f"✅ Alert {alert.id} created and notification scheduled")
    
    def get_alerts_summary(self) -> Dict:
        """
        Obtenir un résumé des alertes actives
        """
        alerts = self.db.query(Alert).filter(
            Alert.status.in_([AlertStatus.PENDING, AlertStatus.ACKNOWLEDGED])
        ).all()
        
        summary = {
            "total": len(alerts),
            "by_severity": {
                "RED": len([a for a in alerts if a.severity == "RED"]),
                "ORANGE": len([a for a in alerts if a.severity == "ORANGE"])
            },
            "by_type": {},
            "by_status": {}
        }
        
        for alert in alerts:
            # Count by type
            alert_type = alert.alert_type.value
            summary["by_type"][alert_type] = summary["by_type"].get(alert_type, 0) + 1
            
            # Count by status
            status = alert.status.value
            summary["by_status"][status] = summary["by_status"].get(status, 0) + 1
        
        return summary
    
    def resolve_alert(self, alert_id: int) -> bool:
        """
        Marquer une alerte comme résolue
        """
        try:
            alert = self.db.query(Alert).filter(Alert.id == alert_id).first()
            if alert:
                alert.status = AlertStatus.RESOLVED
                alert.resolved_at = datetime.now()
                self.db.commit()
                logger.info(f"Alert {alert_id} marked as resolved")
                return True
            else:
                logger.warning(f"Alert {alert_id} not found")
                return False
        except Exception as e:
            logger.error(f"Error resolving alert {alert_id}: {str(e)}")
            return False
    
    def acknowledge_alert(self, alert_id: int) -> bool:
        """
        Marquer une alerte comme acquittée
        """
        try:
            alert = self.db.query(Alert).filter(Alert.id == alert_id).first()
            if alert:
                alert.status = AlertStatus.ACKNOWLEDGED
                alert.acknowledged_at = datetime.now()
                self.db.commit()
                logger.info(f"Alert {alert_id} acknowledged")
                return True
            else:
                logger.warning(f"Alert {alert_id} not found")
                return False
        except Exception as e:
            logger.error(f"Error acknowledging alert {alert_id}: {str(e)}")
            return False