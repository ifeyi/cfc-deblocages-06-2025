# ============================
# backend/app/schemas/__init__.py
# ============================
"""
Pydantic schemas for the CFC application.

This module handles all the data validation schemas used by the API.
"""

# Import base schemas first
from app.schemas.base import BaseSchema, TimestampedSchema

# Import all schemas in the right order to avoid circular imports
from app.schemas.client import (
    ClientBase,
    ClientCreate,
    ClientUpdate,
    ClientInDB,
    ClientResponse,
    ClientWithLoans,
)

from app.schemas.loan import (
    LoanBase,
    LoanCreate,
    LoanUpdate,
    LoanInDB,
    LoanResponse,
    LoanSummary,
    LoanWithDetails,
)

from app.schemas.disbursement import (
    DisbursementBase,
    DisbursementCreate,
    DisbursementUpdate,
    DisbursementInDB,
    DisbursementResponse,
    DisbursementSummary,
)

# Import alert schemas if they exist
try:
    from app.schemas.alert import (
        AlertBase,
        AlertCreate,
        AlertUpdate,
        AlertInDB,
        AlertResponse,
        AlertSummary,
    )
except ImportError:
    # Alert schemas don't exist yet
    pass

__all__ = [
    # Base schemas
    "BaseSchema",
    "TimestampedSchema",
    # Client schemas
    "ClientBase",
    "ClientCreate", 
    "ClientUpdate",
    "ClientInDB",
    "ClientResponse",
    "ClientWithLoans",
    # Loan schemas
    "LoanBase",
    "LoanCreate",
    "LoanUpdate",
    "LoanInDB", 
    "LoanResponse",
    "LoanSummary",
    "LoanWithDetails",
    # Disbursement schemas
    "DisbursementBase",
    "DisbursementCreate",
    "DisbursementUpdate",
    "DisbursementInDB",
    "DisbursementResponse", 
    "DisbursementSummary",
]