# ============================
# backend/app/schemas/client.py
# ============================
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from app.schemas.base import BaseSchema, TimestampedSchema


class ClientBase(BaseSchema):
    name: str = Field(..., min_length=2, max_length=200)
    company_name: Optional[str] = Field(None, max_length=200)
    address: str = Field(..., min_length=5)
    phone: str = Field(..., pattern=r"^\+?[0-9\s\-()]+$")
    email: Optional[EmailStr] = None
    id_card_number: Optional[str] = Field(None, max_length=50)


class ClientCreate(ClientBase):
    pass


class ClientUpdate(BaseSchema):
    name: Optional[str] = Field(None, min_length=2, max_length=200)
    company_name: Optional[str] = Field(None, max_length=200)
    address: Optional[str] = Field(None, min_length=5)
    phone: Optional[str] = Field(None, pattern=r"^\+?[0-9\s\-()]+$")
    email: Optional[EmailStr] = None
    id_card_number: Optional[str] = Field(None, max_length=50)
    is_active: Optional[bool] = None


class ClientInDB(ClientBase, TimestampedSchema):
    id: int
    client_number: str
    is_active: bool = True


class ClientResponse(ClientInDB):
    pass


class ClientWithLoans(ClientResponse):
    loans: List["LoanSummary"] = []