# ============================
# backend/app/models/disbursement.py
# ============================
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Numeric, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class DisbursementStatus(str, enum.Enum):
    REQUESTED = "DEMANDE"
    APPROVED = "APPROUVE"
    IN_PROGRESS = "EN_COURS"
    COMPLETED = "COMPLETE"
    REJECTED = "REJETE"
    SUSPENDED = "SUSPENDU"


class Disbursement(Base):
    __tablename__ = "disbursements"

    id = Column(Integer, primary_key=True, index=True)
    loan_id = Column(Integer, ForeignKey("loans.id"), nullable=False)
    disbursement_number = Column(Integer, nullable=False)  # 1st, 2nd, etc.
    
    # Disbursement details
    status = Column(Enum(DisbursementStatus), default=DisbursementStatus.REQUESTED)
    requested_amount = Column(Numeric(15, 2), nullable=False)
    approved_amount = Column(Numeric(15, 2))
    disbursed_amount = Column(Numeric(15, 2))
    
    # Dates
    request_date = Column(DateTime(timezone=True), nullable=False)
    approval_date = Column(DateTime(timezone=True))
    disbursement_date = Column(DateTime(timezone=True))
    
    # Work progress
    work_description = Column(Text)
    work_completion_percentage = Column(Integer, default=0)
    site_visit_date = Column(DateTime(timezone=True))
    site_visit_report = Column(Text)
    
    # BET (Bureau d'Études Techniques)
    bet_name = Column(String(200))
    bet_report_received = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    loan = relationship("Loan", back_populates="disbursements")
    documents = relationship("Document", back_populates="disbursement")