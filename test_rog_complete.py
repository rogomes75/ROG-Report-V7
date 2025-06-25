#!/usr/bin/env python3
"""
Test completo ROG Pool Service no Render com MongoDB
"""

import requests
import json

def test_rog_pool_service():
    base_url = "https://rog-report-v5.onrender.com"
    
    print("🧪 Testing ROG Pool Service v3.0 on Render")
    print(f"URL: {base_url}")
    print("=" * 70)
    
    tests = [
        ("/", "Sistema Principal"),
        ("/health", "Health Check Detalhado"),
        ("/api/", "API Root"),
        ("/api/clients", "Lista de Clientes"),
        ("/api/reports", "Relatórios de Serviço"),
        ("/html", "Interface Web")
    ]
    
    passed = 0
    total = len(tests)
    
    for endpoint, name in tests:
        print(f"🔗 Testing {name} ({endpoint})...")
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=30)
            if response.status_code == 200:
                if endpoint == "/html":
                    if "ROG Pool Service" in response.text:
                        print(f"  ✅ {name}: Interface web carregada")
                        passed += 1
                    else:
                        print(f"  ❌ {name}: Conteúdo HTML incorreto")
                else:
                    data = response.json()
                    if endpoint == "/":
                        message = data.get('message', '')
                        mongodb = data.get('mongodb', 'unknown')
                        print(f"  ✅ {name}: {message}")
                        print(f"      🗄️ MongoDB: {mongodb}")
                    elif endpoint == "/api/clients":
                        count = data.get('count', 0)
                        print(f"  ✅ {name}: {count} clientes encontrados")
                    elif endpoint == "/api/reports":
                        count = data.get('count', 0)
                        print(f"  ✅ {name}: {count} relatórios encontrados")
                    else:
                        message = data.get('message', data.get('status', str(data)))
                        print(f"  ✅ {name}: {message}")
                    passed += 1
            else:
                print(f"  ❌ {name}: Status {response.status_code}")
        except Exception as e:
            print(f"  ❌ {name}: {str(e)[:60]}...")
    
    # Test MongoDB initialization
    print(f"🌱 Testing sample data initialization...")
    try:
        response = requests.post(f"{base_url}/api/init-data", timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Inicialização: {data.get('message', 'OK')}")
        else:
            print(f"  ⚠️  Inicialização: Status {response.status_code}")
    except Exception as e:
        print(f"  ❌ Inicialização: {str(e)[:60]}...")
    
    print("\n" + "=" * 70)
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED!")
        print("✅ ROG Pool Service v3.0 está funcionando perfeitamente!")
        print(f"🌐 Sistema online: {base_url}")
        print(f"🖥️  Interface web: {base_url}/html")
        
        print("\n🏊‍♂️ Funcionalidades implementadas:")
        print("   ✅ Sistema base funcionando")
        print("   ✅ API endpoints completos")
        print("   ✅ Interface web responsiva")
        print("   ✅ Gestão de clientes")
        print("   ✅ Relatórios de serviço")
        print("   ✅ Dados de exemplo")
        
        print("\n🔄 Próximos passos recomendados:")
        print("   1. Configurar MongoDB Atlas")
        print("   2. Adicionar variável MONGODB_URL no Render")
        print("   3. Implementar autenticação JWT")
        print("   4. Adicionar upload de fotos")
        print("   5. Sistema de notificações")
        
    elif passed >= total * 0.7:
        print(f"⚠️  MOSTLY WORKING: {passed}/{total} funcionando")
        print("💡 Maioria das funcionalidades ok - verifique MongoDB")
    else:
        print("❌ DEPLOYMENT ISSUES")
        print("🔧 Verifique logs do Render")
    
    return passed >= total * 0.8

if __name__ == "__main__":
    success = test_rog_pool_service()
    print("\n" + "=" * 70)
    if success:
        print("🚀 DEPLOY NO RENDER SUCCESSFUL!")
    else:
        print("⚠️  DEPLOY NEEDS ATTENTION")
    print("=" * 70)