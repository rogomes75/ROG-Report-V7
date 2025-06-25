#!/usr/bin/env python3
"""
URL Generator para Railway - Gera URL já escapada
"""

import urllib.parse

def generate_escaped_urls():
    print("🔧 MongoDB URL Generator para Railway")
    print("=" * 60)
    
    # Dados extraídos da sua imagem
    username = "rogomes75"
    password = "ricardo101"
    cluster = "cluster0.qprpnpj.mongodb.net"
    
    print(f"Username: {username}")
    print(f"Password: {password}")
    print(f"Cluster: {cluster}")
    print()
    
    # Escapar username e password
    username_escaped = urllib.parse.quote_plus(username)
    password_escaped = urllib.parse.quote_plus(password)
    
    print("URLs para testar no Railway:")
    print("=" * 60)
    
    # Opção 1: URL completa com database
    url1 = f"mongodb+srv://{username_escaped}:{password_escaped}@{cluster}/pool_maintenance_db?retryWrites=true&w=majority"
    print("OPÇÃO 1 (Com database):")
    print(url1)
    print()
    
    # Opção 2: URL sem database (mais simples)
    url2 = f"mongodb+srv://{username_escaped}:{password_escaped}@{cluster}/?retryWrites=true&w=majority"
    print("OPÇÃO 2 (Sem database específico):")
    print(url2)
    print()
    
    # Opção 3: URL mínima
    url3 = f"mongodb+srv://{username_escaped}:{password_escaped}@{cluster}"
    print("OPÇÃO 3 (Mínima):")
    print(url3)
    print()
    
    print("=" * 60)
    print("📋 TESTE NO RAILWAY:")
    print("1. Primeiro teste a OPÇÃO 2")
    print("2. Se não funcionar, teste a OPÇÃO 3")
    print("3. Se não funcionar, teste a OPÇÃO 1")
    print("=" * 60)
    
    return [url1, url2, url3]

def test_urls_locally():
    """Testa as URLs localmente para ver se são válidas"""
    urls = generate_escaped_urls()
    
    print("\n🧪 TESTE LOCAL DAS URLs:")
    print("=" * 60)
    
    for i, url in enumerate(urls, 1):
        try:
            from pymongo import MongoClient
            client = MongoClient(url, serverSelectionTimeoutMS=5000)
            # Tentar conectar
            client.server_info()
            print(f"✅ OPÇÃO {i}: URL válida - conectou com sucesso!")
            client.close()
        except Exception as e:
            print(f"❌ OPÇÃO {i}: {e}")
    
    print("=" * 60)

if __name__ == "__main__":
    try:
        test_urls_locally()
    except ImportError:
        print("PyMongo não disponível - apenas gerando URLs")
        generate_escaped_urls()