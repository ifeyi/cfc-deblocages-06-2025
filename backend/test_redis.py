#!/usr/bin/env python3
"""
Test Redis connection with Docker secrets
Run this script to debug Redis connection issues
"""
import os
import sys
from pathlib import Path
from urllib.parse import quote_plus

def get_secret(secret_name: str, default: str = None) -> str:
    """Get secret from Docker secrets file or environment variable."""
    secret_file_path = os.getenv(f"{secret_name.upper()}_FILE")
    if secret_file_path and Path(secret_file_path).exists():
        try:
            with open(secret_file_path, 'r') as f:
                return f.read().strip()
        except Exception as e:
            print(f"Error reading secret file {secret_file_path}: {e}")
            return os.getenv(secret_name.upper(), default)
    return os.getenv(secret_name.upper(), default)

def test_redis_connection():
    """Test Redis connection with current configuration"""
    print("=" * 50)
    print("Redis Connection Test")
    print("=" * 50)
    
    # Get configuration
    redis_host = os.getenv("REDIS_HOST", "redis")
    redis_port = os.getenv("REDIS_PORT", "6379")
    redis_db = os.getenv("REDIS_DB", "0")
    
    print(f"Redis Host: {redis_host}")
    print(f"Redis Port: {redis_port}")
    print(f"Redis DB: {redis_db}")
    
    # Get password from secret
    redis_password_file = os.getenv("REDIS_PASSWORD_FILE")
    print(f"Redis Password File: {redis_password_file}")
    
    redis_password = get_secret("redis_password")
    
    if redis_password:
        print(f"Password found: {'*' * len(redis_password)}")
        print(f"Password length: {len(redis_password)}")
        
        # Check for problematic characters
        problematic_chars = [':', '@', '/', '?', '#', '[', ']']
        found_chars = [char for char in problematic_chars if char in redis_password]
        if found_chars:
            print(f"⚠️  Found URL-problematic characters: {found_chars}")
        else:
            print("✅ No URL-problematic characters found")
        
        # Show URL encoding
        encoded_password = quote_plus(redis_password)
        if encoded_password != redis_password:
            print(f"Password needs encoding: {redis_password} -> {encoded_password}")
        else:
            print("Password doesn't need encoding")
    else:
        print("No password found")
    
    # Test connection
    print("\nTesting Redis connection...")
    
    try:
        import redis
        
        if redis_password:
            # Test with URL
            encoded_password = quote_plus(redis_password)
            redis_url = f"redis://:{encoded_password}@{redis_host}:{redis_port}/{redis_db}"
            print(f"Trying URL: redis://:***@{redis_host}:{redis_port}/{redis_db}")
            
            r = redis.from_url(redis_url)
            result = r.ping()
            print(f"✅ Redis connection successful: {result}")
        else:
            # Test without password
            redis_url = f"redis://{redis_host}:{redis_port}/{redis_db}"
            print(f"Trying URL: {redis_url}")
            
            r = redis.from_url(redis_url)
            result = r.ping()
            print(f"✅ Redis connection successful: {result}")
            
    except ImportError:
        print("❌ Redis package not installed. Install with: pip install redis")
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")
        
        # Additional debug info
        print(f"\nDebug info:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        
        # Try direct connection
        try:
            print("\nTrying direct connection...")
            r = redis.Redis(
                host=redis_host,
                port=int(redis_port),
                db=int(redis_db),
                password=redis_password,
                socket_connect_timeout=5,
                socket_timeout=5
            )
            result = r.ping()
            print(f"✅ Direct Redis connection successful: {result}")
        except Exception as e2:
            print(f"❌ Direct connection also failed: {e2}")

if __name__ == "__main__":
    test_redis_connection()