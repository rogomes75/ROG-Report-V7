#!/usr/bin/env python3
"""
Test Minimal para app5.rogpoolservice.com
"""

import requests
import sys

def test_minimal_app():
    base_url = "https://app5.rogpoolservice.com"
    
    print(f"🧪 Testing MINIMAL ROG Pool Service at: {base_url}")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 3
    
    # Test 1: Root endpoint
    print("🌐 Testing root endpoint...")
    try:
        response = requests.get(base_url, timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Root endpoint: {data.get('message', 'OK')}")
            tests_passed += 1
        else:
            print(f"  ❌ Root endpoint error: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Root endpoint error: {e}")
    
    # Test 2: API endpoint
    print("🔗 Testing API endpoint...")
    try:
        response = requests.get(f"{base_url}/api/", timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ API endpoint: {data.get('message', 'OK')}")
            tests_passed += 1
        else:
            print(f"  ❌ API endpoint error: {response.status_code}")
    except Exception as e:
        print(f"  ❌ API endpoint error: {e}")
    
    # Test 3: Health endpoint
    print("🏥 Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/api/health", timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Health endpoint: {data.get('status', 'unknown')}")
            tests_passed += 1
        else:
            print(f"  ❌ Health endpoint error: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Health endpoint error: {e}")
    
    return tests_passed, total_tests

def main():
    print("🚀 ROG Pool Service - MINIMAL TEST (APP5)")
    print("=" * 60)
    
    passed, total = test_minimal_app()
    
    print("\n" + "=" * 60)
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED!")
        print("\n✅ Your minimal app is working!")
        print("🔗 Access: https://app5.rogpoolservice.com")
        print("🔗 API: https://app5.rogpoolservice.com/api/")
        print("🔗 Health: https://app5.rogpoolservice.com/api/health")
    elif passed > 0:
        print(f"⚠️  PARTIAL SUCCESS: {passed}/{total} tests passed")
        print("💡 App is partially working - check Railway logs")
    else:
        print("❌ ALL TESTS FAILED!")
        print("\n🔧 Check:")
        print("   - Railway deployment completed")
        print("   - No build errors in logs")
        print("   - Environment variables set")
    
    print("=" * 60)
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)