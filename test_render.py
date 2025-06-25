#!/usr/bin/env python3
"""
Test Render Deploy
"""

import requests
import time

def test_render_url(render_url):
    print(f"🧪 Testing Render Deploy: {render_url}")
    print("=" * 60)
    
    endpoints = [
        ("/", "Root"),
        ("/health", "Health Check")
    ]
    
    for endpoint, name in endpoints:
        print(f"🔗 Testing {name} ({endpoint})...")
        try:
            response = requests.get(f"{render_url}{endpoint}", timeout=30)
            if response.status_code == 200:
                data = response.json()
                print(f"  ✅ {name}: {data.get('message', data.get('status', 'OK'))}")
            else:
                print(f"  ❌ {name}: Status {response.status_code}")
        except Exception as e:
            print(f"  ❌ {name}: {str(e)[:80]}...")
    
    print("\n" + "=" * 60)

# Exemplo de uso
if __name__ == "__main__":
    # Substitua pela URL real do Render quando estiver pronta
    render_url = input("Digite a URL do Render (ex: https://seu-app.onrender.com): ").strip()
    if render_url:
        test_render_url(render_url)
    else:
        print("💡 Exemplo de URL Render:")
        print("https://rog-pool-service.onrender.com")
        print("https://rog-pool-service-xyz.onrender.com")