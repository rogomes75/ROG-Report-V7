#!/usr/bin/env python3
"""
Test específico para app1.rogpoolservice.com
"""

import requests
import time
import sys

def test_app():
    base_url = "https://app1.rogpoolservice.com"
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
    
    # Test 3: Authentication
    print("🔐 Testing login...")
    try:
        login_data = {"username": "admin", "password": "admin123"}
        response = requests.post(f"{api_url}/auth/login", json=login_data, timeout=30)
        if response.status_code == 200:
            data = response.json()
            if "access_token" in data:
                print("  ✅ Login working - admin user authenticated")
                token = data["access_token"]
                
                # Test authenticated endpoint
                headers = {"Authorization": f"Bearer {token}"}
                response = requests.get(f"{api_url}/auth/me", headers=headers, timeout=30)
                if response.status_code == 200:
                    user = response.json()
                    print(f"  ✅ User profile: {user.get('username')} ({user.get('role')})")
                else:
                    print(f"  ⚠️  User profile failed: {response.status_code}")
                
                return True
            else:
                print("  ❌ Login response invalid")
                return False
        else:
            print(f"  ❌ Login failed: {response.status_code}")
            if response.status_code == 401:
                print("    💡 Admin user might not be created in database")
            elif response.status_code == 500:
                print("    💡 Possible database connection issue")
            return False
    except Exception as e:
        print(f"  ❌ Login error: {e}")
        return False

def main():
    print("🚀 ROG Pool Service - Production Test")
    print("=" * 60)
    
    success = test_app()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 ALL TESTS PASSED!")
        print("\n💡 Your app is working correctly!")
        print("🔑 Login at: https://app1.rogpoolservice.com")
        print("   Username: admin")
        print("   Password: admin123")
    else:
        print("❌ TESTS FAILED!")
        print("\n🔧 Possible issues:")
        print("   - Check Railway environment variables")
        print("   - Verify MongoDB connection")
        print("   - Check Railway logs for errors")
        print("   - Ensure all services are running")
    
    print("=" * 60)
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)