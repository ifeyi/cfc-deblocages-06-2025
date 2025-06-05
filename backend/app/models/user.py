# ============================
# backend/app/models/user.py
# ============================
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    CHARGE_CLIENTELE = "CHARGE_CLIENTELE"
    ANALYSTE_PRETS = "ANALYSTE_PRETS"
    ADMINISTRATEUR_PRETS = "ADMINISTRATEUR_PRETS"
    CHARGE_REMBOURSEMENT = "CHARGE_REMBOURSEMENT"
    DIRECTEUR_AGENCE = "DIRECTEUR_AGENCE"
    READONLY = "READONLY"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(200), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    
    # User details
    role = Column(Enum(UserRole), nullable=False)
    agency = Column(String(100))
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    
    # Preferences
    preferred_language = Column(String(2), default="fr")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))
    
    # Relationships
    documents = relationship("Document", back_populates="uploader")