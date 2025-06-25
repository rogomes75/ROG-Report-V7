#!/usr/bin/env python3
"""
Teste ultra simples para verificar Railway
"""

import requests
import time

def test_new_url():
    url = "https://web-production-210bd.up.railway.app"
    
    print("🧪 Testing Railway URL (New Project)")
    print(f"URL: {url}")
    print("=" * 50)
    
    for attempt in range(5):
        print(f"Attempt {attempt + 1}/5...")
        try:
            response = requests.get(url, timeout=30)
            print(f"  Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"  ✅ SUCCESS: {data}")
                return True
            elif response.status_code == 502:
                print(f"  ❌ 502 Bad Gateway - Server not responding")
            else:
                print(f"  ⚠️  Unexpected status: {response.status_code}")
                print(f"  Response: {response.text[:200]}")
        except Exception as e:
            print(f"  ❌ Error: {e}")
        
        if attempt < 4:
            print("  Waiting 30s for next attempt...")
            time.sleep(30)
    
    print("\n❌ All attempts failed!")
    print("\n🔧 Possible issues:")
    print("1. Railway service not starting properly")
    print("2. Build failed but showed as successful")
    print("3. Port binding issue")
    print("4. Requirements.txt issue")
    print("5. Git push not triggering redeploy")
    
    return False

if __name__ == "__main__":
    success = test_new_url()
    if not success:
        print("\n💡 Recommendations:")
        print("1. Check Railway Dashboard → Logs")
        print("2. Try manual redeploy")
        print("3. Check if service is actually running")
        print("4. Consider using different Railway region")