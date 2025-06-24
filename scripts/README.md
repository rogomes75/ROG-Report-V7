# 🚀 ROG Pool Service - Deploy Scripts

Este diretório contém scripts automatizados para facilitar o deploy no Railway.

## 📋 Scripts Disponíveis

### 1. `deploy_setup.py` - Setup Completo
**Script principal que verifica e prepara tudo para deploy**

```bash
python scripts/deploy_setup.py
```

**O que faz:**
- ✅ Verifica pré-requisitos (Git, Node.js, Python)
- ✅ Valida estrutura do projeto
- ✅ Instala dependências e builda frontend
- ✅ Cria template de variáveis de ambiente
- ✅ Gera checklist de deploy
- ✅ Verifica configuração do Git

### 2. `railway_deploy.sh` - Deploy Bash Script
**Script em Shell para preparação rápida**

```bash
chmod +x scripts/railway_deploy.sh
./scripts/railway_deploy.sh
```

**O que faz:**
- 📦 Instala dependências
- 🏗️ Builda frontend
- 📝 Commita mudanças no Git
- 🚀 Prepara para deploy

### 3. `quick_deploy.py` - Deploy Rápido
**Para quando você quer fazer deploy rapidamente**

```bash
python scripts/quick_deploy.py
```

**O que faz:**
- ⚡ Versão simplificada do setup completo
- 🏗️ Build e commit automático
- 📋 Checklist rápido

### 4. `test_deployment.py` - Teste de Deploy
**Testa se seu deploy no Railway está funcionando**

```bash
python scripts/test_deployment.py https://seu-app.railway.app
```

**O que testa:**
- 🌐 Frontend carregando
- 🏥 API funcionando
- 🔐 Sistema de login
- 🗄️ Conexão com banco de dados
- 🔗 Endpoints principais

## 🎯 Workflow Recomendado

### Primeira vez:
```bash
# 1. Setup completo
python scripts/deploy_setup.py

# 2. Revisar arquivos gerados:
#    - .env.railway (variáveis de ambiente)
#    - DEPLOYMENT_CHECKLIST.md (checklist)

# 3. Push para GitHub
git push origin main

# 4. Deploy no Railway
# (conectar repo, configurar variáveis, deploy)

# 5. Testar deploy
python scripts/test_deployment.py https://seu-app.railway.app
```

### Deploys subsequentes:
```bash
# Deploy rápido
python scripts/quick_deploy.py
git push origin main

# Testar
python scripts/test_deployment.py https://seu-app.railway.app
```

## 📁 Arquivos Gerados

Os scripts criam estes arquivos automaticamente:

- `.env.railway` - Template de variáveis de ambiente
- `DEPLOYMENT_CHECKLIST.md` - Checklist completo
- `nixpacks.toml` - Configuração de build Railway
- `railway.json` - Configurações Railway
- `Procfile` - Comando de inicialização

## 🔧 Solução de Problemas

### Script não executa:
```bash
# Instalar dependências Python se necessário
pip install requests

# Dar permissão para scripts bash
chmod +x scripts/*.sh
```

### Build falha:
- Verificar se Node.js está instalado
- Verificar se está no diretório correto do projeto
- Verificar se frontend/package.json existe

### Teste de deploy falha:
- Verificar se app está rodando no Railway
- Verificar variáveis de ambiente
- Verificar logs no Railway dashboard

## 💡 Dicas

1. **Sempre execute os scripts do diretório raiz do projeto**
2. **Revise os arquivos .env.railway antes de configurar no Railway**
3. **Use o teste de deploy para verificar se tudo está funcionando**
4. **Mantenha suas credenciais de banco seguras**

## 🆘 Suporte

Se encontrar problemas:

1. Verifique se está no diretório correto
2. Confira se todas as dependências estão instaladas
3. Revise os logs do Railway
4. Verifique as variáveis de ambiente
5. Execute o teste de deploy para diagnóstico

---

**✨ Estes scripts automatizam 90% do processo de deploy, deixando apenas a configuração no Railway para você!**