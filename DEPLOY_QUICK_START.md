# 🚀 ROG Pool Service - Deploy Automático

## ⚡ Deploy em 1 Comando

```bash
./deploy.sh
```

## 📋 Scripts Disponíveis

| Script | Descrição | Uso |
|--------|-----------|-----|
| `./deploy.sh` | **Deploy completo automático** | `./deploy.sh` |
| `scripts/deploy_setup.py` | Setup completo com verificações | `python scripts/deploy_setup.py` |
| `scripts/quick_deploy.py` | Deploy rápido | `python scripts/quick_deploy.py` |
| `scripts/test_deployment.py` | Testar app no Railway | `python scripts/test_deployment.py URL` |

## 🎯 Processo Automatizado

1. **Execute o script:**
   ```bash
   ./deploy.sh
   ```

2. **Vá para Railway:**
   - Acesse https://railway.app
   - Conecte seu GitHub repo
   - Configure as variáveis do arquivo `.env.railway`
   - Deploy!

3. **Teste o deploy:**
   ```bash
   python scripts/test_deployment.py https://seu-app.railway.app
   ```

## 🔑 Credenciais Padrão

- **Admin:** admin / admin123
- **Test Admin:** testadmin / test123

## 📁 Arquivos Gerados

- `.env.railway` - Variáveis de ambiente para Railway
- `DEPLOYMENT_CHECKLIST.md` - Checklist completo
- `nixpacks.toml`, `railway.json`, `Procfile` - Configs Railway

## 🆘 Problemas?

1. **Build falhou no Railway:**
   - Verifique se todas as variáveis de ambiente estão configuradas
   - Check logs no Railway dashboard

2. **App não carrega:**
   - Verifique MONGO_URL e REACT_APP_BACKEND_URL
   - Confirme que banco de dados está conectado

3. **Login não funciona:**
   - Execute o teste: `python scripts/test_deployment.py URL`
   - Verifique logs do backend no Railway

---

**✨ Com estes scripts, seu deploy no Railway é 90% automatizado!**