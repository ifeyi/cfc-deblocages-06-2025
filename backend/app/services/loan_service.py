# backend/app/services/loan_service.py
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from decimal import Decimal
from sqlalchemy.orm import Session
from app.models import Loan, Alert, AlertType, AlertStatus
from app.models.loan import LoanStatus, LoanType
import logging

logger = logging.getLogger(__name__)


class LoanService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_loan(self, loan_data: Dict) -> Loan:
        """
        Créer un nouveau prêt avec calcul automatique de la mensualité
        """
        # Calculate monthly payment
        amount = Decimal(str(loan_data['amount']))
        rate = Decimal(str(loan_data['interest_rate'])) / 100 / 12
        duration = loan_data['duration_months']
        
        if rate > 0:
            monthly_payment = amount * (rate * (1 + rate) ** duration) / ((1 + rate) ** duration - 1)
        else:
            monthly_payment = amount / duration
        
        # Generate loan number
        loan_number = self._generate_loan_number(loan_data['loan_type'])
        
        # Calculate validity end date based on loan type
        validity_days = 60 if 'CLASSIQUE' in loan_data['loan_type'] else 90
        validity_end_date = datetime.now() + timedelta(days=validity_days)
        
        # Create loan
        loan = Loan(
            loan_number=loan_number,
            monthly_payment=monthly_payment,
            validity_end_date=validity_end_date,
            **loan_data
        )
        
        self.db.add(loan)
        self.db.commit()
        self.db.refresh(loan)
        
        # Create initial alert for validity tracking
        self._create_validity_alert(loan)
        
        return loan
    
    def _generate_loan_number(self, loan_type: str) -> str:
        """
        Générer un numéro de prêt unique
        Format: YYYY/AGENCY/SEQUENCE/TYPE
        """
        year = datetime.now().year
        agency_code = "102"  # TODO: Get from current user's agency
        
        # Get next sequence number
        last_loan = self.db.query(Loan).filter(
            Loan.loan_number.like(f"{year}/{agency_code}/%")
        ).order_by(Loan.id.desc()).first()
        
        if last_loan:
            last_sequence = int(last_loan.loan_number.split('/')[2])
            sequence = str(last_sequence + 1).zfill(7)
        else:
            sequence = "0000001"
        
        # Get type code
        type_codes = {
            LoanType.CLASSIC_ACQUIRER: "541",
            LoanType.CLASSIC_BUILDER: "542",
            LoanType.RENTAL_ORDINARY: "567",
            LoanType.YOUNG_LAND: "571"
        }
        type_code = type_codes.get(loan_type, "500")
        
        return f"{year}/{agency_code}/{sequence}/{type_code}"
    
    def _create_validity_alert(self, loan: Loan):
        """
        Créer une alerte pour suivre la validité de l'offre
        """
        alert = Alert(
            loan_id=loan.id,
            alert_type=AlertType.VALIDITY_WARNING,
            severity="ORANGE",
            message=f"L'offre de prêt {loan.loan_number} expire le {loan.validity_end_date.strftime('%d/%m/%Y')}"
        )
        self.db.add(alert)
        self.db.commit()
    
    def check_loan_validity(self, loan_id: int) -> Dict:
        """
        Vérifier la validité d'un prêt et créer des alertes si nécessaire
        """
        loan = self.db.query(Loan).filter(Loan.id == loan_id).first()
        if not loan:
            return {"error": "Loan not found"}
        
        days_remaining = (loan.validity_end_date - datetime.now()).days
        validity_days = 60 if 'CLASSIQUE' in loan.loan_type else 90
        
        # Check for orange alert (2/3 of time elapsed)
        if days_remaining <= validity_days / 3 and days_remaining > 5:
            self._create_or_update_alert(
                loan, 
                AlertType.VALIDITY_WARNING,
                "ORANGE",
                f"Attention: Il reste {days_remaining} jours avant l'expiration de l'offre"
            )
        
        # Check for red alert (5 days remaining)
        elif days_remaining <= 5 and days_remaining > 0:
            self._create_or_update_alert(
                loan,
                AlertType.VALIDITY_CRITICAL,
                "RED",
                f"URGENT: L'offre expire dans {days_remaining} jours!"
            )
        
        # Check if expired
        elif days_remaining <= 0:
            loan.status = LoanStatus.CANCELLED
            self.db.commit()
            return {"status": "expired", "message": "L'offre de prêt a expiré"}
        
        return {
            "status": "valid",
            "days_remaining": days_remaining,
            "expiry_date": loan.validity_end_date
        }
    
    def _create_or_update_alert(self, loan: Loan, alert_type: AlertType, severity: str, message: str):
        """
        Créer ou mettre à jour une alerte
        """
        existing_alert = self.db.query(Alert).filter(
            Alert.loan_id == loan.id,
            Alert.alert_type == alert_type,
            Alert.status != AlertStatus.RESOLVED
        ).first()
        
        if existing_alert:
            existing_alert.message = message
            existing_alert.severity = severity
        else:
            alert = Alert(
                loan_id=loan.id,
                alert_type=alert_type,
                severity=severity,
                message=message
            )
            self.db.add(alert)
        
        self.db.commit()

