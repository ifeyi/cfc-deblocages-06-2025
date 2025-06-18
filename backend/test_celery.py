#!/usr/bin/env python3
"""
Test Celery app loading
"""
import sys
import os

def test_celery_import():
    """Test if Celery app can be imported properly"""
    print("Testing Celery app import...")
    
    try:
        # Test importing the celery app
        from app.core.celery_app import celery_app
        print("✅ Successfully imported celery_app")
        
        # Test basic celery app properties
        print(f"Celery app name: {celery_app.main}")
        print(f"Broker URL: {celery_app.conf.broker_url}")
        print(f"Backend URL: {celery_app.conf.result_backend}")
        
        # Test importing tasks
        from app import tasks
        print("✅ Successfully imported tasks module")
        
        # Test task registration
        registered_tasks = list(celery_app.tasks.keys())
        print(f"Registered tasks: {len(registered_tasks)}")
        for task in registered_tasks:
            if task.startswith('app.tasks'):
                print(f"  - {task}")
        
        print("✅ Celery app test completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error testing Celery app: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_redis_connection():
    """Test Redis connection"""
    print("\nTesting Redis connection...")
    
    try:
        from app.core.celery_app import get_redis_url
        redis_url = get_redis_url()
        print(f"Redis URL: {redis_url.replace(':' + redis_url.split(':')[2].split('@')[0], ':***')}")
        
        # Test with redis-py
        import redis
        r = redis.from_url(redis_url)
        result = r.ping()
        print(f"✅ Redis ping successful: {result}")
        return True
        
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")
        return False

if __name__ == "__main__":
    success = True
    success &= test_celery_import()
    success &= test_redis_connection()
    
    if success:
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print("\n💥 Some tests failed!")
        sys.exit(1)