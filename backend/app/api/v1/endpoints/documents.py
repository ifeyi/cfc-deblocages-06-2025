# ============================
# backend/app/api/v1/endpoints/documents.py
# ============================
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.api.deps import get_db

router = APIRouter()

@router.get("/")
def get_documents(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    loan_id: Optional[int] = Query(None),
    client_id: Optional[int] = Query(None),
    document_type: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """
    Récupérer la liste des documents avec filtres
    """
    # TODO: Implement actual document retrieval logic
    # from app.models import Document
    # 
    # query = db.query(Document)
    # 
    # if loan_id:
    #     query = query.filter(Document.loan_id == loan_id)
    # if client_id:
    #     query = query.filter(Document.client_id == client_id)
    # if document_type:
    #     query = query.filter(Document.document_type == document_type)
    # 
    # documents = query.offset(skip).limit(limit).all()
    # return documents
    
    return []

@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    loan_id: Optional[int] = Form(None),
    client_id: Optional[int] = Form(None),
    document_type: str = Form(...),
    description: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    """
    Télécharger un document
    """
    # TODO: Implement actual document upload logic
    # from app.services.document_service import DocumentService
    # 
    # # Validate file type and size
    # allowed_types = ["application/pdf", "image/jpeg", "image/png", "application/msword"]
    # if file.content_type not in allowed_types:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Type de fichier non autorisé"
    #     )
    # 
    # document_service = DocumentService(db)
    # document = await document_service.upload_document(
    #     file, loan_id, client_id, document_type, description
    # )
    # return document
    
    return {
        "message": "Document téléchargé avec succès",
        "filename": file.filename,
        "content_type": file.content_type,
        "size": file.size,
        "document_type": document_type,
        "loan_id": loan_id,
        "client_id": client_id
    }

@router.get("/{document_id}")
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
):
    """
    Récupérer les métadonnées d'un document
    """
    # TODO: Implement actual document retrieval logic
    # from app.models import Document
    # 
    # document = db.query(Document).filter(Document.id == document_id).first()
    # if not document:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="Document non trouvé"
    #     )
    # return document
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Document non trouvé"
    )

@router.get("/{document_id}/download")
async def download_document(
    document_id: int,
    db: Session = Depends(get_db),
):
    """
    Télécharger un document
    """
    # TODO: Implement actual document download logic
    # from app.models import Document
    # from app.services.document_service import DocumentService
    # 
    # document = db.query(Document).filter(Document.id == document_id).first()
    # if not document:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="Document non trouvé"
    #     )
    # 
    # document_service = DocumentService(db)
    # file_stream = document_service.get_document_stream(document)
    # 
    # return StreamingResponse(
    #     file_stream,
    #     media_type=document.content_type,
    #     headers={"Content-Disposition": f"attachment; filename={document.filename}"}
    # )
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Document non trouvé"
    )

@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
):
    """
    Supprimer un document
    """
    # TODO: Implement actual document deletion logic
    # from app.models import Document
    # from app.services.document_service import DocumentService
    # 
    # document = db.query(Document).filter(Document.id == document_id).first()
    # if not document:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="Document non trouvé"
    #     )
    # 
    # document_service = DocumentService(db)
    # document_service.delete_document(document)
    # return None
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Document non trouvé"
    )

@router.get("/types/list")
def get_document_types():
    """
    Récupérer la liste des types de documents
    """
    return {
        "document_types": [
            "PIECE_IDENTITE",
            "JUSTIFICATIF_REVENUS",
            "TITRE_PROPRIETE",
            "PLAN_TRAVAUX",
            "DEVIS",
            "FACTURE",
            "RAPPORT_VISITE",
            "CONTRAT",
            "AUTRE"
        ]
    }