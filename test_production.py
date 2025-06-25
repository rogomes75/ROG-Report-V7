#!/usr/bin/env python3
"""
Test específico para app5.rogpoolservice.com
"""

import requests
import time
import sys

def test_app():
    base_url = "https://app5.rogpoolservice.com"
    api_url = f"{base_url}/api"
    
    print(f"🧪 Testing ROG Pool Service at: {base_url}")
    print("=" * 60)
    
    # Test 1: Frontend
    print("🌐 Testing frontend...")
    try:
        response = requests.get(base_url, timeout=30)
        if response.status_code == 200:
            print(f"  ✅ Frontend accessible (status: {response.status_code})")
        else:
            print(f"  ❌ Frontend error: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ Frontend connection error: {e}")
        return False
    
    # Test 2: API Health
    print("🏥 Testing API...")
    try:
        response = requests.get(f"{api_url}/", timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ API responding: {data.get('message', 'OK')}")
        else:
            print(f"  ❌ API error: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ API connection error: {e}")
        return False
    
    # Test 3: Health Check
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{api_url}/health", timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Health check: {data.get('status')} - DB: {data.get('database')}")
            return True
        else:
            print(f"  ⚠️  Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ Health check error: {e}")
        return False

def main():
    print("🚀 ROG Pool Service - Production Test (APP5)")
    print("=" * 60)
    
    success = test_app()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 ALL TESTS PASSED!")
        print("\n💡 Your simplified app is working correctly!")
        print("🔗 Access at: https://app5.rogpoolservice.com")
        print("🔗 API at: https://app5.rogpoolservice.com/api/")
    else:
        print("❌ TESTS FAILED!")
        print("\n🔧 Possible issues:")
        print("   - Check Railway deployment logs")
        print("   - Verify MongoDB plugin is added")
        print("   - Check Railway environment variables")
        print("   - Ensure build completed successfully")
    
    print("=" * 60)
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)