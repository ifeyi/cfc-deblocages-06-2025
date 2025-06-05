# ============================
# backend/app/models/loan.py
# ============================
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum, ForeignKey, Numeric, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class LoanType(str, enum.Enum):
    CLASSIC_ACQUIRER = "PRET_CLASSIQUE_ACQUEREUR"
    CLASSIC_BUILDER = "PRET_CLASSIQUE_CONSTRUCTEUR"
    RENTAL_ORDINARY = "PRET_LOCATIF_ORDINAIRE"
    YOUNG_LAND = "FONCIER_CLASSIQUE_JEUNES"


class LoanStatus(str, enum.Enum):
    DRAFT = "BROUILLON"
    APPROVED = "APPROUVE"
    IN_PROGRESS = "EN_COURS"
    DISBURSING = "DEBLOCAGE"
    COMPLETED = "COMPLETE"
    CANCELLED = "ANNULE"
    SUSPENDED = "SUSPENDU"


class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    loan_number = Column(String(100), unique=True, index=True, nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    
    # Loan details
    loan_type = Column(Enum(LoanType), nullable=False)
    status = Column(Enum(LoanStatus), default=LoanStatus.DRAFT, nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    duration_months = Column(Integer, nullable=False)
    grace_period_months = Column(Integer, default=0)
    interest_rate = Column(Numeric(5, 2), nullable=False)
    monthly_payment = Column(Numeric(15, 2), nullable=False)
    
    # Dates
    approval_date = Column(DateTime(timezone=True))
    signature_date = Column(DateTime(timezone=True))
    first_payment_date = Column(DateTime(timezone=True))
    validity_end_date = Column(DateTime(timezone=True))
    
    # Mortgage details
    mortgage_amount = Column(Numeric(15, 2))
    property_title_number = Column(String(100))
    property_location = Column(Text)
    
    # Insurance
    life_insurance_company = Column(String(100))
    fire_insurance_company = Column(String(100))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    client = relationship("Client", back_populates="loans")
    disbursements = relationship("Disbursement", back_populates="loan")
    documents = relationship("Document", back_populates="loan")
    alerts = relationship("Alert", back_populates="loan")