# 🚀 INSTRUÇÕES PARA ATUALIZAR O RENDER

## ❌ Problema Atual:
O Render ainda está servindo a versão antiga porque as mudanças não foram sincronizadas com o GitHub.

## ✅ SOLUÇÕES:

### **Opção A - Update Manual via GitHub (MAIS FÁCIL):**

1. **Vá para**: https://github.com/rogomes75/ROG-Report-V5
2. **Clique no arquivo `app.py`**
3. **Clique no ícone ✏️ (Edit)**
4. **Substitua todo o conteúdo** pelo código atualizado
5. **Scroll down** → **Commit changes**
6. **Render vai detectar** automaticamente e redesploy

### **Código atualizado para `app.py`:**
```python
# [Copie o conteúdo do arquivo /app/app.py que criei]
```

### **Código atualizado para `requirements.txt`:**
```
fastapi==0.104.1
uvicorn==0.24.0
motor==3.3.2
pydantic==2.5.0
python-dotenv==1.0.0
```

### **Opção B - Trigger Manual no Render:**

1. **Render Dashboard** → **rog-report-v5**
2. **Manual Deploy** → **Deploy Latest Commit**

### **Opção C - Reconnect GitHub:**

1. **Settings** → **GitHub**
2. **Disconnect** e **Reconnect**

## 🧪 **APÓS ATUALIZAÇÃO:**

Teste a nova versão:
```bash
python test_rog_complete.py
```

**Resultado esperado:**
- ✅ Sistema v3.0 funcionando
- ✅ MongoDB endpoints ativos
- ✅ Interface web completa
- ✅ Gestão de clientes
- ✅ Relatórios de serviço

## 🗄️ **CONFIGURAR MONGODB:**

Depois que a v3.0 estiver rodando:

1. **MongoDB Atlas** → Get connection string
2. **Render Dashboard** → **Environment Variables**
3. **Add**: `MONGODB_URL=sua_connection_string`
4. **Render redeploy** automaticamente

---

**💡 Recomendo a Opção A - mais simples e direto!**