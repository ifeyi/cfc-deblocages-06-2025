# ============================
# backend/app/models/alert.py
# ============================
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class AlertType(str, enum.Enum):
    # Mise en place alerts
    VALIDITY_WARNING = "VALIDITY_WARNING"  # Orange alert
    VALIDITY_CRITICAL = "VALIDITY_CRITICAL"  # Red alert
    
    # Disbursement alerts
    WORK_DELAY_WARNING = "WORK_DELAY_WARNING"
    WORK_DELAY_CRITICAL = "WORK_DELAY_CRITICAL"
    
    # Repayment alerts
    REPAYMENT_UPCOMING = "REPAYMENT_UPCOMING"
    REPAYMENT_IMMINENT = "REPAYMENT_IMMINENT"
    
    # Document alerts
    MISSING_DOCUMENT = "MISSING_DOCUMENT"
    DOCUMENT_EXPIRY = "DOCUMENT_EXPIRY"


class AlertStatus(str, enum.Enum):
    PENDING = "PENDING"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    RESOLVED = "RESOLVED"
    ESCALATED = "ESCALATED"


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    loan_id = Column(Integer, ForeignKey("loans.id"), nullable=False)
    
    # Alert details
    alert_type = Column(Enum(AlertType), nullable=False)
    status = Column(Enum(AlertStatus), default=AlertStatus.PENDING)
    severity = Column(String(20))  # ORANGE or RED
    message = Column(Text, nullable=False)
    
    # Dates
    triggered_at = Column(DateTime(timezone=True), server_default=func.now())
    acknowledged_at = Column(DateTime(timezone=True))
    resolved_at = Column(DateTime(timezone=True))
    
    # Notification status
    email_sent = Column(Boolean, default=False)
    sms_sent = Column(Boolean, default=False)
    
    # Relationships
    loan = relationship("Loan", back_populates="alerts")
    acknowledged_by = Column(Integer, ForeignKey("users.id"))