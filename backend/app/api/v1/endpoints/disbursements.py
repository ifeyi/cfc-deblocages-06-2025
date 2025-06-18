# ============================
# backend/app/api/v1/endpoints/disbursements.py
# ============================
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.disbursement import DisbursementCreate, DisbursementUpdate, DisbursementResponse

router = APIRouter()

@router.get("/", response_model=List[DisbursementResponse])
def get_disbursements(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    loan_id: Optional[int] = Query(None),
    status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    Récupérer la liste des déblocages avec pagination et filtres
    """
    # TODO: Implement actual disbursement retrieval logic
    # from app.models import Disbursement
    # 
    # query = db.query(Disbursement)
    # 
    # if loan_id:
    #     query = query.filter(Disbursement.loan_id == loan_id)
    # if status:
    #     query = query.filter(Disbursement.status == status)
    # 
    # disbursements = query.offset(skip).limit(limit).all()
    # return disbursements
    
    return []

@router.post("/", response_model=DisbursementResponse, status_code=status.HTTP_201_CREATED)
def create_disbursement(
    disbursement_data: DisbursementCreate,
    db: Session = Depends(get_db),
):
    """
    Créer une nouvelle demande de déblocage
    """
    # TODO: Implement actual disbursement creation logic
    # from app.models import Loan
    # from app.services.disbursement_service import DisbursementService
    # 
    # # Verify loan exists
    # loan = db.query(Loan).filter(Loan.id == disbursement_data.loan_id).first()
    # if not loan:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="Prêt non trouvé"
    #     )
    # 
    # disbursement_service = DisbursementService(db)
    # disbursement = disbursement_service.create_disbursement(disbursement_data.dict())
    # return disbursement
    
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Création de déblocage non implémentée"
    )

@router.get("/{disbursement_id}", response_model=DisbursementResponse)
def get_disbursement(
    disbursement_id: int,
    db: Session = Depends(get_db),
):
    """
    Récupérer les détails d'un déblocage
    """
    # TODO: Implement actual disbursement retrieval logic
    # from app.models import Disbursement
    # 
    # disbursement = db.query(Disbursement).filter(Disbursement.id == disbursement_id).first()
    # if not disbursement:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="Déblocage non trouvé"
    #     )
    # return disbursement
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Déblocage non trouvé"
    )

@router.put("/{disbursement_id}", response_model=DisbursementResponse)
def update_disbursement(
    disbursement_id: int,
    disbursement_update: DisbursementUpdate,
    db: Session = Depends(get_db),
):
    """
    Mettre à jour un déblocage
    """
    # TODO: Implement actual disbursement update logic
    # from app.models import Disbursement
    # 
    # disbursement = db.query(Disbursement).filter(Disbursement.id == disbursement_id).first()
    # if not disbursement:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="Déblocage non trouvé"
    #     )
    # 
    # update_data = disbursement_update.dict(exclude_unset=True)
    # for field, value in update_data.items():
    #     setattr(disbursement, field, value)
    # 
    # db.commit()
    # db.refresh(disbursement)
    # return disbursement
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Déblocage non trouvé"
    )

@router.put("/{disbursement_id}/approve")
def approve_disbursement(
    disbursement_id: int,
    approved_amount: float,
    db: Session = Depends(get_db),
):
    """
    Approuver un déblocage
    """
    # TODO: Implement actual disbursement approval logic
    return {
        "message": f"Déblocage {disbursement_id} approuvé pour {approved_amount} FCFA",
        "disbursement_id": disbursement_id,
        "approved_amount": approved_amount
    }

@router.put("/{disbursement_id}/disburse")
def disburse_funds(
    disbursement_id: int,
    db: Session = Depends(get_db),
):
    """
    Effectuer le déblocage des fonds
    """
    # TODO: Implement actual fund disbursement logic
    return {
        "message": f"Fonds déblocés pour le déblocage {disbursement_id}",
        "disbursement_id": disbursement_id,
        "status": "DISBURSED"
    }