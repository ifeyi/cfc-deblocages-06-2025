# ============================
# backend/app/schemas/auth.py
# ============================
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from app.models.user import UserRole


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None


class UserLogin(BaseModel):
    username: str
    password: str


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=200)
    password: str = Field(..., min_length=8)
    role: UserRole
    agency: Optional[str] = None
    preferred_language: str = Field("fr", pattern="^(fr|en)$")


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    role: UserRole
    agency: Optional[str] = None
    is_active: bool
    preferred_language: str
    
    class Config:
        from_attributes = True