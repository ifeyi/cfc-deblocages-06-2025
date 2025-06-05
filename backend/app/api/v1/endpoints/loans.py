
# ============================
# backend/app/api/v1/endpoints/loans.py
# ============================
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.api.deps import get_current_user, get_db
from app.models import User, Loan, Client
from app.schemas.loan import LoanCreate, LoanUpdate, LoanResponse, LoanWithDetails
from app.services.loan_service import LoanService

router = APIRouter()


@router.get("/", response_model=List[LoanResponse])
def get_loans(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status: Optional[str] = None,
    client_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupérer la liste des prêts avec pagination et filtres
    """
    query = db.query(Loan)
    
    if status:
        query = query.filter(Loan.status == status)
    
    if client_id:
        query = query.filter(Loan.client_id == client_id)
    
    loans = query.offset(skip).limit(limit).all()
    return loans


@router.post("/", response_model=LoanResponse, status_code=status.HTTP_201_CREATED)
def create_loan(
    loan_data: LoanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Créer un nouveau prêt
    """
    # Verify client exists
    client = db.query(Client).filter(Client.id == loan_data.client_id).first()
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    loan_service = LoanService(db)
    loan = loan_service.create_loan(loan_data.dict())
    
    return loan


@router.get("/{loan_id}", response_model=LoanWithDetails)
def get_loan(
    loan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupérer les détails d'un prêt
    """
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    
    if not loan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loan not found"
        )
    
    return loan


@router.put("/{loan_id}", response_model=LoanResponse)
def update_loan(
    loan_id: int,
    loan_update: LoanUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Mettre à jour un prêt
    """
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    
    if not loan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loan not found"
        )
    
    # Update loan fields
    update_data = loan_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(loan, field, value)
    
    db.commit()
    db.refresh(loan)
    
    return loan


@router.delete("/{loan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_loan(
    loan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Supprimer un prêt (soft delete)
    """
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    
    if not loan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loan not found"
        )
    
    # Soft delete by changing status
    loan.status = "CANCELLED"
    db.commit()
    
    return None