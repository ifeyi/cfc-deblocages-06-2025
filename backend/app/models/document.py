# ============================
# backend/app/models/document.py
# ============================
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class DocumentType(str, enum.Enum):
    # Client documents
    DEMANDE_MANUSCRITE = "DEMANDE_MANUSCRITE"
    CNI = "CNI_SIGNEE"
    CERTIFICAT_PROPRIETE = "CERTIFICAT_PROPRIETE"
    PLAN_LOCALISATION = "PLAN_LOCALISATION"
    CASIER_JUDICIAIRE = "CASIER_JUDICIAIRE"
    FACTURE_ENEO = "FACTURE_ENEO"
    
    # Loan documents
    CONTRAT_PRET = "CONTRAT_PRET"
    NOTIFICATION_ACCORD = "NOTIFICATION_ACCORD"
    CONVENTION_SIGNEE = "CONVENTION_SIGNEE"
    
    # Disbursement documents
    DEMANDE_DEBLOCAGE = "DEMANDE_DEBLOCAGE"
    RAPPORT_VISITE = "RAPPORT_VISITE"
    RAPPORT_BET = "RAPPORT_BET"
    
    # Insurance documents
    BIA_DGE = "BIA_DGE"
    BIA_INCENDIE = "BIA_INCENDIE"
    BIA_TRC = "BIA_TRC"
    
    # Other
    AUTRES = "AUTRES"


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    loan_id = Column(Integer, ForeignKey("loans.id"), nullable=True)
    disbursement_id = Column(Integer, ForeignKey("disbursements.id"), nullable=True)
    
    # Document details
    document_type = Column(Enum(DocumentType), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer)  # in bytes
    mime_type = Column(String(100))
    description = Column(Text)
    
    # Timestamps
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    uploaded_by = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    client = relationship("Client", back_populates="documents")
    loan = relationship("Loan", back_populates="documents")
    disbursement = relationship("Disbursement", back_populates="documents")
    uploader = relationship("User")