# ============================
# backend/app/schemas/disbursement.py
# ============================
from __future__ import annotations

from typing import Optional
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, validator
from app.schemas.base import BaseSchema, TimestampedSchema
from app.models.disbursement import DisbursementStatus

class DisbursementBase(BaseSchema):
    requested_amount: Decimal = Field(..., gt=0, decimal_places=2)
    work_description: str = Field(..., min_length=10)
    work_completion_percentage: int = Field(0, ge=0, le=100)
    bet_name: Optional[str] = None

class DisbursementCreate(DisbursementBase):
    loan_id: int

class DisbursementUpdate(BaseSchema):
    status: Optional[DisbursementStatus] = None
    approved_amount: Optional[Decimal] = None
    disbursed_amount: Optional[Decimal] = None
    approval_date: Optional[datetime] = None
    disbursement_date: Optional[datetime] = None
    work_completion_percentage: Optional[int] = Field(None, ge=0, le=100)
    site_visit_date: Optional[datetime] = None
    site_visit_report: Optional[str] = None
    bet_report_received: Optional[bool] = None

class DisbursementInDB(DisbursementBase, TimestampedSchema):
    id: int
    loan_id: int
    disbursement_number: int
    status: DisbursementStatus
    request_date: datetime
    approved_amount: Optional[Decimal] = None
    disbursed_amount: Optional[Decimal] = None
    approval_date: Optional[datetime] = None
    disbursement_date: Optional[datetime] = None
    site_visit_date: Optional[datetime] = None
    site_visit_report: Optional[str] = None
    bet_report_received: bool = False

class DisbursementResponse(DisbursementInDB):
    pass

class DisbursementSummary(BaseSchema):
    id: int
    disbursement_number: int
    status: DisbursementStatus
    requested_amount: Decimal
    request_date: datetime
    work_completion_percentage: int