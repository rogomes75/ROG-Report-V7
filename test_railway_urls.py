#!/usr/bin/env python3
"""
Test com URL real do Railway
"""

import requests
import sys

def test_railway_url(base_url):
    print(f"🧪 Testing at: {base_url}")
    print("=" * 60)
    
    endpoints = [
        ("/", "Root"),
        ("/api/", "API Root"), 
        ("/health", "Health Check"),
        ("/test", "Test Endpoint"),
        ("/html", "HTML Page")
    ]
    
    passed = 0
    
    for endpoint, name in endpoints:
        print(f"🔗 Testing {name}...")
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=10, verify=False)
            if response.status_code == 200:
                if endpoint == "/html":
                    print(f"  ✅ {name}: HTML loaded")
                else:
                    data = response.json()
                    print(f"  ✅ {name}: {data.get('message', 'OK')}")
                passed += 1
            else:
                print(f"  ❌ {name}: Status {response.status_code}")
        except Exception as e:
            print(f"  ❌ {name}: {str(e)[:100]}...")
    
    return passed

# URLs possíveis do Railway
possible_urls = [
    "https://web-production-ee0ff.up.railway.app",
    "https://rog-report-v5.railway.app", 
    "https://rog-pool-service.railway.app"
]

def main():
    print("🚀 Testing Railway URLs")
    print("=" * 60)
    
    print("💡 Por favor, forneça a URL real do Railway Dashboard!")
    print("Testando URLs possíveis...")
    print()
    
    for url in possible_urls:
        print(f"Testando: {url}")
        passed = test_railway_url(url)
        if passed > 0:
            print(f"🎉 ENCONTREI! {passed} endpoints funcionando em: {url}")
            return True
        print()
    
    print("❌ Nenhuma URL funcionou.")
    print("💡 Verifique no Railway Dashboard qual é a URL correta.")
    return False

if __name__ == "__main__":
    main()