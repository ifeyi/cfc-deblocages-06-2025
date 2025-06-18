#!/usr/bin/env python3
"""
Final test to verify all schemas work
"""

def test_all_schemas():
    """Test that all schemas can be imported and used"""
    print("Testing all schema imports...")
    
    try:
        # Test base schemas
        from app.schemas.base import BaseSchema, TimestampedSchema
        print("✅ Base schemas imported")
        
        # Test client schemas
        from app.schemas.client import ClientResponse, ClientCreate, ClientWithLoans
        print("✅ Client schemas imported")
        
        # Test loan schemas  
        from app.schemas.loan import LoanResponse, LoanWithDetails, LoanSummary
        print("✅ Loan schemas imported")
        
        # Test disbursement schemas
        from app.schemas.disbursement import DisbursementResponse, DisbursementSummary
        print("✅ Disbursement schemas imported")
        
        # Test alert schemas
        from app.schemas.alert import AlertResponse, AlertSummary
        print("✅ Alert schemas imported")
        
        # Test the problematic schema
        print(f"LoanWithDetails fields: {LoanWithDetails.__annotations__}")
        print(f"ClientWithLoans fields: {ClientWithLoans.__annotations__}")
        
        # Test creating instances
        print("Testing schema instantiation...")
        
        # Test basic schemas work
        loan_data = {
            "id": 1,
            "loan_number": "L001",
            "client_id": 1,
            "loan_type": "CLASSIQUE",
            "amount": 1000000.00,
            "duration_months": 24,
            "grace_period_months": 6,
            "interest_rate": 12.5,
            "status": "APPROVED",
            "monthly_payment": 50000.00,
            "created_at": "2024-01-01T00:00:00",
            "client": {
                "id": 1,
                "name": "John Doe",
                "phone": "+237123456789",
                "email": "john@example.com"
            },
            "disbursements": [],
            "alerts": []
        }
        
        loan_with_details = LoanWithDetails(**loan_data)
        print(f"✅ LoanWithDetails created: {loan_with_details.loan_number}")
        
        return True
        
    except Exception as e:
        print(f"❌ Schema test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_api_import():
    """Test that the API endpoint can be imported"""
    print("\nTesting API endpoint import...")
    
    try:
        from app.api.v1.endpoints.loans import router
        print("✅ Loans router imported successfully")
        return True
    except Exception as e:
        print(f"❌ API import error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = True
    success &= test_all_schemas()
    success &= test_api_import()
    
    if success:
        print("\n🎉 All schema tests passed!")
    else:
        print("\n💥 Some tests failed!")
        
    print("\nTesting FastAPI app import...")
    try:
        from app.main import app
        print("✅ FastAPI app imported successfully")
    except Exception as e:
        print(f"❌ FastAPI app import error: {e}")
        import traceback
        traceback.print_exc()