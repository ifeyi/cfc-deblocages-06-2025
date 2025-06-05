# ============================
# backend/app/models/__init__.py
# ============================
from app.models.client import Client
from app.models.loan import Loan, LoanType, LoanStatus
from app.models.disbursement import Disbursement, DisbursementStatus
from app.models.document import Document, DocumentType
from app.models.alert import Alert, AlertType, AlertStatus
from app.models.user import User, UserRole
from app.database import Base

__all__ = [
    "Base",
    "Client",
    "Loan",
    "LoanType",
    "LoanStatus",
    "Disbursement",
    "DisbursementStatus",
    "Document",
    "DocumentType",
    "Alert",
    "AlertType",
    "AlertStatus",
    "User",
    "UserRole",
]