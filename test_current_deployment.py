#!/usr/bin/env python3
"""
Test Final para URL correta: web-production-ee0ff.up.railway.app
"""

import requests
import sys

def test_production_app():
    base_url = "https://web-production-ee0ff.up.railway.app"
    
    print(f"🧪 Testing ROG Pool Service at: {base_url}")
    print("=" * 70)
    
    endpoints = [
        ("/", "Root Endpoint", "ROG Pool Service is running!"),
        ("/api/", "API Root", "ROG Pool Service API"),
        ("/health", "Health Check", "healthy"),
        ("/test", "Test Endpoint", "Test endpoint working!"),
        ("/html", "HTML Page", None)  # HTML response
    ]
    
    passed = 0
    total = len(endpoints)
    
    for endpoint, name, expected in endpoints:
        print(f"🔗 Testing {name} ({endpoint})...")
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=30)
            if response.status_code == 200:
                if endpoint == "/html":
                    if "ROG Pool Service" in response.text:
                        print(f"  ✅ {name}: HTML page loaded successfully")
                        passed += 1
                    else:
                        print(f"  ❌ {name}: HTML content incorrect")
                else:
                    data = response.json()
                    message = data.get('message', data.get('status', str(data)))
                    print(f"  ✅ {name}: {message}")
                    passed += 1
            else:
                print(f"  ❌ {name}: Status {response.status_code}")
        except Exception as e:
            print(f"  ❌ {name}: {str(e)[:80]}...")
    
    return passed, total

def main():
    print("🚀 ROG Pool Service - PRODUCTION TEST")
    print("URL: https://web-production-ee0ff.up.railway.app")
    print("=" * 70)
    
    passed, total = test_production_app()
    
    print("\n" + "=" * 70)
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - DEPLOY SUCCESSFUL!")
        print("\n✅ Your ROG Pool Service is LIVE and working!")
        print("🌐 Production URL: https://web-production-ee0ff.up.railway.app")
        print("\n📋 Available Endpoints:")
        print("   🏠 Homepage: https://web-production-ee0ff.up.railway.app/")
        print("   🔗 API Root: https://web-production-ee0ff.up.railway.app/api/")
        print("   🏥 Health: https://web-production-ee0ff.up.railway.app/health")
        print("   🧪 Test: https://web-production-ee0ff.up.railway.app/test")
        print("   🌐 HTML: https://web-production-ee0ff.up.railway.app/html")
        
        print("\n🚀 READY FOR NEXT STEPS:")
        print("   1. Add MongoDB Plugin to Railway")
        print("   2. Implement authentication system")
        print("   3. Add pool service features")
        print("   4. Deploy React frontend")
        print("   5. Configure full-stack integration")
        
    elif passed > 0:
        print(f"⚠️  PARTIAL SUCCESS: {passed}/{total} endpoints working")
    else:
        print("❌ TESTS FAILED!")
    
    print("=" * 70)
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)