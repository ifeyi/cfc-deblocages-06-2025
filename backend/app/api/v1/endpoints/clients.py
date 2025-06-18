# ============================
# backend/app/api/v1/endpoints/clients.py
# ============================
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.client import ClientCreate, ClientUpdate, ClientResponse, ClientWithLoans

router = APIRouter()

@router.get("/", response_model=List[ClientResponse])
def get_clients(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    search: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    """
    Récupérer la liste des clients avec pagination et filtres
    """
    # TODO: Implement actual client retrieval logic
    # from app.models import Client
    # query = db.query(Client)
    # 
    # if search:
    #     query = query.filter(Client.name.contains(search))
    # if is_active is not None:
    #     query = query.filter(Client.is_active == is_active)
    # 
    # clients = query.offset(skip).limit(limit).all()
    # return clients
    
    return []

@router.post("/", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create_client(
    client_data: ClientCreate,
    db: Session = Depends(get_db),
):
    """
    Créer un nouveau client
    """
    # TODO: Implement actual client creation logic
    # from app.models import Client
    # from app.services.client_service import ClientService
    # 
    # client_service = ClientService(db)
    # client = client_service.create_client(client_data.dict())
    # return client
    
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Création de client non implémentée"
    )

@router.get("/{client_id}", response_model=ClientWithLoans)
def get_client(
    client_id: int,
    db: Session = Depends(get_db),
):
    """
    Récupérer les détails d'un client avec ses prêts
    """
    # TODO: Implement actual client retrieval logic
    # from app.models import Client
    # from sqlalchemy.orm import joinedload
    # 
    # client = db.query(Client).options(joinedload(Client.loans)).filter(Client.id == client_id).first()
    # if not client:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="Client non trouvé"
    #     )
    # return client
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Client non trouvé"
    )

@router.put("/{client_id}", response_model=ClientResponse)
def update_client(
    client_id: int,
    client_update: ClientUpdate,
    db: Session = Depends(get_db),
):
    """
    Mettre à jour un client
    """
    # TODO: Implement actual client update logic
    # from app.models import Client
    # 
    # client = db.query(Client).filter(Client.id == client_id).first()
    # if not client:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="Client non trouvé"
    #     )
    # 
    # update_data = client_update.dict(exclude_unset=True)
    # for field, value in update_data.items():
    #     setattr(client, field, value)
    # 
    # db.commit()
    # db.refresh(client)
    # return client
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Client non trouvé"
    )

@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(
    client_id: int,
    db: Session = Depends(get_db),
):
    """
    Supprimer un client (soft delete)
    """
    # TODO: Implement actual client deletion logic
    # from app.models import Client
    # 
    # client = db.query(Client).filter(Client.id == client_id).first()
    # if not client:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="Client non trouvé"
    #     )
    # 
    # client.is_active = False
    # db.commit()
    # return None
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Client non trouvé"
    )