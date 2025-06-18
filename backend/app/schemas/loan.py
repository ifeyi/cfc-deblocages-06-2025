# ============================
# backend/app/schemas/loan.py
# ============================
from __future__ import annotations

from typing import Optional, List, Any, Dict
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, validator
from app.schemas.base import BaseSchema, TimestampedSchema
from app.models.loan import LoanType, LoanStatus

class LoanBase(BaseSchema):
    loan_type: LoanType
    amount: Decimal = Field(..., gt=0, decimal_places=2)
    duration_months: int = Field(..., gt=0)
    grace_period_months: int = Field(0, ge=0)
    interest_rate: Decimal = Field(..., gt=0, decimal_places=2)
    property_title_number: Optional[str] = None
    property_location: Optional[str] = None
    life_insurance_company: Optional[str] = None
    fire_insurance_company: Optional[str] = None

class LoanCreate(LoanBase):
    client_id: int

class LoanUpdate(BaseSchema):
    status: Optional[LoanStatus] = None
    approval_date: Optional[datetime] = None
    signature_date: Optional[datetime] = None
    first_payment_date: Optional[datetime] = None
    validity_end_date: Optional[datetime] = None
    mortgage_amount: Optional[Decimal] = None

class LoanInDB(LoanBase, TimestampedSchema):
    id: int
    loan_number: str
    client_id: int
    status: LoanStatus
    monthly_payment: Decimal
    approval_date: Optional[datetime] = None
    signature_date: Optional[datetime] = None
    first_payment_date: Optional[datetime] = None
    validity_end_date: Optional[datetime] = None
    mortgage_amount: Optional[Decimal] = None

class LoanResponse(LoanInDB):
    pass

class LoanSummary(BaseSchema):
    id: int
    loan_number: str
    loan_type: LoanType
    status: LoanStatus
    amount: Decimal
    created_at: datetime

# Simplified version without forward references for now
class LoanWithDetails(LoanResponse):
    # Use Dict instead of specific schemas to avoid circular imports
    client: Dict[str, Any]
    disbursements: List[Dict[str, Any]] = []
    alerts: List[Dict[str, Any]] = []