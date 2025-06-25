#!/usr/bin/env python3
"""
MongoDB URL Fixer - Corrige caracteres especiais na connection string
"""

import urllib.parse

def fix_mongo_url():
    print("🔧 MongoDB URL Fixer")
    print("=" * 50)
    
    # Sua URL atual (baseada na imagem)
    original_url = "mongodb+srv://rogomes75:ricardo101@cluster0.qprpnpj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    
    print("URL Original:")
    print(original_url)
    print()
    
    # Extrair componentes
    try:
        if original_url.startswith('mongodb+srv://'):
            # Remove o prefixo
            without_prefix = original_url.replace('mongodb+srv://', '')
            
            # Dividir em auth@host
            parts = without_prefix.split('@', 1)
            if len(parts) == 2:
                auth_part = parts[0]  # rogomes75:ricardo101
                url_part = parts[1]   # cluster0.qprpnpj.mongodb.net/...
                
                # Dividir username:password
                username, password = auth_part.split(':', 1)
                
                print(f"Username: {username}")
                print(f"Password: {password}")
                print()
                
                # Encode username e password
                username_encoded = urllib.parse.quote_plus(username)
                password_encoded = urllib.parse.quote_plus(password)
                
                print(f"Username encoded: {username_encoded}")
                print(f"Password encoded: {password_encoded}")
                print()
                
                # Reconstruir URL
                fixed_url = f"mongodb+srv://{username_encoded}:{password_encoded}@{url_part}"
                
                # Adicionar database name se não estiver presente
                if '/?' in fixed_url and 'pool_maintenance_db' not in fixed_url:
                    fixed_url = fixed_url.replace('/?', '/pool_maintenance_db?')
                elif '?' in fixed_url and '/pool_maintenance_db' not in fixed_url:
                    # Inserir database name antes dos parâmetros
                    parts = fixed_url.split('?')
                    fixed_url = parts[0] + '/pool_maintenance_db?' + parts[1]
                
                print("🎯 URL CORRIGIDA:")
                print(fixed_url)
                print()
                print("=" * 50)
                print("📋 COPIE ESTA URL E COLE NO RAILWAY:")
                print("=" * 50)
                print(fixed_url)
                print("=" * 50)
                
                return fixed_url
    
    except Exception as e:
        print(f"Erro ao processar URL: {e}")
        return None

if __name__ == "__main__":
    fix_mongo_url()