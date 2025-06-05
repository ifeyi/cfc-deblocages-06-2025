# ============================
# backend/app/models/client.py
# ============================
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    client_number = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(200), nullable=False)
    company_name = Column(String(200), nullable=True)
    address = Column(Text, nullable=False)
    phone = Column(String(50), nullable=False)
    email = Column(String(100), nullable=True)
    id_card_number = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    loans = relationship("Loan", back_populates="client")
    documents = relationship("Document", back_populates="client")