#!/usr/bin/env python3
"""
Test ROG Pool Service no Render
"""

import requests

def test_render_deployment():
    base_url = "https://rog-report-v5.onrender.com"
    
    print("🧪 Testing ROG Pool Service on Render")
    print(f"URL: {base_url}")
    print("=" * 60)
    
    endpoints = [
        ("/", "Root Endpoint"),
        ("/health", "Health Check"),
        ("/api/", "API Root")
    ]
    
    passed = 0
    total = len(endpoints)
    
    for endpoint, name in endpoints:
        print(f"🔗 Testing {name} ({endpoint})...")
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=30)
            if response.status_code == 200:
                data = response.json()
                message = data.get('message', data.get('status', str(data)))
                print(f"  ✅ {name}: {message}")
                passed += 1
            else:
                print(f"  ❌ {name}: Status {response.status_code}")
        except Exception as e:
            print(f"  ❌ {name}: {str(e)[:60]}...")
    
    print("\n" + "=" * 60)
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED!")
        print("✅ ROG Pool Service is running perfectly on Render!")
        print(f"🌐 Live URL: {base_url}")
        print("\n🚀 Ready for next steps:")
        print("   1. Add MongoDB integration")
        print("   2. Implement authentication")
        print("   3. Add pool service features")
        
    elif passed > 0:
        print(f"⚠️  PARTIAL SUCCESS: {passed}/{total} working")
    else:
        print("❌ DEPLOYMENT FAILED")
    
    return passed == total

if __name__ == "__main__":
    test_render_deployment()