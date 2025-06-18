# ============================
# backend/app/api/v1/api.py
# ============================
from fastapi import APIRouter
from app.api.v1.endpoints import auth, clients, loans, disbursements, documents, alerts, reports

api_router = APIRouter()

# Include all endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(clients.router, prefix="/clients", tags=["Clients"])
api_router.include_router(loans.router, prefix="/loans", tags=["Loans"])
api_router.include_router(disbursements.router, prefix="/disbursements", tags=["Disbursements"])
api_router.include_router(documents.router, prefix="/documents", tags=["Documents"])
api_router.include_router(alerts.router, prefix="/alerts", tags=["Alerts"])
api_router.include_router(reports.router, prefix="/reports", tags=["Reports"])