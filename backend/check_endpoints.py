#!/usr/bin/env python3
"""
Check which endpoint files are missing
"""
import os

def check_endpoints():
    """Check which endpoint files exist"""
    endpoints_dir = "/app/app/api/v1/endpoints"
    required_files = [
        "auth.py",
        "clients.py", 
        "loans.py",
        "disbursements.py",
        "documents.py",
        "alerts.py",
        "reports.py",
        "__init__.py"
    ]
    
    print(f"Checking endpoints directory: {endpoints_dir}")
    print("=" * 50)
    
    missing_files = []
    existing_files = []
    
    for file in required_files:
        file_path = os.path.join(endpoints_dir, file)
        if os.path.exists(file_path):
            print(f"✅ {file} exists")
            existing_files.append(file)
        else:
            print(f"❌ {file} MISSING")
            missing_files.append(file)
    
    print("\n" + "=" * 50)
    print(f"Summary: {len(existing_files)}/{len(required_files)} files exist")
    
    if missing_files:
        print(f"\nMissing files: {missing_files}")
        return False
    else:
        print("\n🎉 All endpoint files exist!")
        return True

def test_imports():
    """Test importing each endpoint"""
    print("\n" + "=" * 50)
    print("Testing endpoint imports...")
    
    endpoints = [
        "auth",
        "clients", 
        "loans",
        "disbursements",
        "documents",
        "alerts",
        "reports"
    ]
    
    success = True
    for endpoint in endpoints:
        try:
            module = __import__(f"app.api.v1.endpoints.{endpoint}", fromlist=[endpoint])
            if hasattr(module, 'router'):
                print(f"✅ {endpoint} imported successfully (has router)")
            else:
                print(f"⚠️  {endpoint} imported but no router found")
                success = False
        except ImportError as e:
            print(f"❌ {endpoint} import failed: {e}")
            success = False
        except Exception as e:
            print(f"❌ {endpoint} error: {e}")
            success = False
    
    return success

if __name__ == "__main__":
    files_exist = check_endpoints()
    
    if files_exist:
        imports_work = test_imports()
        
        if imports_work:
            print("\n🎉 All endpoints ready!")
            print("\nTesting API router...")
            try:
                from app.api.v1.api import api_router
                print(f"✅ API router imported with {len(api_router.routes)} routes")
                
                print("\nTesting main app...")
                from app.main import app
                print("✅ Main app imported successfully")
                
                print("\n🚀 Your FastAPI application should work!")
                
            except Exception as e:
                print(f"❌ API router/main app error: {e}")
                import traceback
                traceback.print_exc()
        else:
            print("\n💥 Some endpoint imports failed!")
    else:
        print("\n📝 Need to create missing endpoint files first!")