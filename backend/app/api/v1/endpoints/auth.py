# ============================
# backend/app/api/v1/endpoints/auth.py
# ============================
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from pydantic import BaseModel

# Importer depuis la vraie structure
from app.database import get_db
from app.models.user import User
from app.core.security import create_access_token, verify_password
from app.config import settings

router = APIRouter()

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    message: str
    access_token: str
    token_type: str
    user: dict

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool

def authenticate_user(username: str, password: str, db: Session):
    """Fonction helper pour authentifier un utilisateur"""
    user = db.query(User).filter(
        (User.username == username) | 
        (User.email == username)
    ).first()
    
    if not user:
        return None
    
    if not verify_password(password, user.hashed_password):
        return None
    
    if not user.is_active:
        return None
        
    return user

@router.post("/login", response_model=LoginResponse)
def login_form(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Connexion utilisateur avec formulaire (pour Swagger UI)
    """
    user = authenticate_user(form_data.username, form_data.password, db)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nom d'utilisateur ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Créer le token d'accès
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=str(user.id), expires_delta=access_token_expires
    )
    
    # Mettre à jour la dernière connexion
    user.last_login = datetime.utcnow()
    db.commit()
    
    return LoginResponse(
        message="Connexion réussie",
        access_token=access_token,
        token_type="bearer",
        user={
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role.value,
            "is_active": user.is_active,
            "preferred_language": user.preferred_language
        }
    )

@router.post("/login-json", response_model=LoginResponse)
def login_json(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Connexion utilisateur avec JSON (pour le frontend React)
    """
    user = authenticate_user(login_data.username, login_data.password, db)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Créer le token d'accès
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=str(user.id), expires_delta=access_token_expires
    )
    
    # Mettre à jour la dernière connexion
    user.last_login = datetime.utcnow()
    db.commit()
    
    return LoginResponse(
        message="Connexion réussie",
        access_token=access_token,
        token_type="bearer",
        user={
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role.value,
            "is_active": user.is_active,
            "preferred_language": user.preferred_language
        }
    )

@router.post("/logout")
def logout():
    """
    Déconnexion utilisateur
    """
    return {"message": "Déconnexion réussie"}

@router.get("/me", response_model=UserResponse)
def get_current_user_info():
    """
    Obtenir les informations de l'utilisateur connecté
    """
    # TODO: Implement actual user retrieval logic with token verification
    return UserResponse(
        id=1,
        username="admin",
        email="admin@cfc.com",
        is_active=True
    )

@router.post("/refresh")
def refresh_token():
    """
    Renouveler le token d'accès
    """
    return {
        "access_token": "new-fake-jwt-token",
        "token_type": "bearer",
        "message": "Token renouvelé avec succès"
    }