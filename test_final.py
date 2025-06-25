#!/usr/bin/env python3
"""
Test Final para app5.rogpoolservice.com - Versão Python Puro
"""

import requests
import sys

def test_python_app():
    base_url = "https://app5.rogpoolservice.com"
    
    print(f"🧪 Testing PYTHON-ONLY ROG Pool Service at: {base_url}")
    print("=" * 70)
    
    endpoints = [
        ("/", "Root"),
        ("/api/", "API Root"),
        ("/health", "Health Check"),
        ("/test", "Test Endpoint"),
        ("/html", "HTML Page")
    ]
    
    passed = 0
    total = len(endpoints)
    
    for endpoint, name in endpoints:
        print(f"🔗 Testing {name} ({endpoint})...")
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=30)
            if response.status_code == 200:
                if endpoint == "/html":
                    print(f"  ✅ {name}: HTML page loaded")
                else:
                    data = response.json()
                    print(f"  ✅ {name}: {data.get('message', data.get('status', 'OK'))}")
                passed += 1
            else:
                print(f"  ❌ {name}: Status {response.status_code}")
        except Exception as e:
            print(f"  ❌ {name}: {e}")
    
    return passed, total

def main():
    print("🚀 ROG Pool Service - FINAL PYTHON TEST (APP5)")
    print("=" * 70)
    
    passed, total = test_python_app()
    
    print("\n" + "=" * 70)
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED!")
        print("\n✅ Your Python app is working perfectly!")
        print("🔗 Access: https://app5.rogpoolservice.com")
        print("🌐 HTML: https://app5.rogpoolservice.com/html")
        print("🔗 API: https://app5.rogpoolservice.com/api/")
        print("🏥 Health: https://app5.rogpoolservice.com/health")
        print("🧪 Test: https://app5.rogpoolservice.com/test")
    elif passed > 0:
        print(f"⚠️  PARTIAL SUCCESS: {passed}/{total} endpoints working")
        print("💡 Some endpoints are working - Railway deployment is progressing")
    else:
        print("❌ ALL TESTS FAILED!")
        print("\n🔧 Final troubleshooting:")
        print("   - Check if Railway deployment completed")
        print("   - Verify build logs for errors")
        print("   - Ensure Python runtime is detected")
        print("   - Check Railway service status")
    
    print("=" * 70)
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)