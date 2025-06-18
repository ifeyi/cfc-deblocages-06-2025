# ============================
# backend/app/schemas/alert.py
# ============================
from __future__ import annotations

from typing import Optional
from datetime import datetime
from pydantic import Field
from app.schemas.base import BaseSchema, TimestampedSchema

class AlertBase(BaseSchema):
    loan_id: int
    alert_type: str
    severity: str = Field(..., pattern=r"^(RED|ORANGE|GREEN)$")
    message: str = Field(..., min_length=1, max_length=500)

class AlertCreate(AlertBase):
    pass

class AlertUpdate(BaseSchema):
    severity: Optional[str] = Field(None, pattern=r"^(RED|ORANGE|GREEN)$")
    message: Optional[str] = Field(None, min_length=1, max_length=500)
    status: Optional[str] = None
    resolved_at: Optional[datetime] = None
    acknowledged_at: Optional[datetime] = None

class AlertInDB(AlertBase, TimestampedSchema):
    id: int
    status: str
    resolved_at: Optional[datetime] = None
    acknowledged_at: Optional[datetime] = None

class AlertResponse(AlertInDB):
    pass

class AlertSummary(BaseSchema):
    id: int
    alert_type: str
    severity: str
    message: str
    status: str
    created_at: datetime