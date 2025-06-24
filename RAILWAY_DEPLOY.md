# ROG Pool Service - Deploy Guide para Railway

## 📋 Pré-requisitos
- Conta no Railway (railway.app)
- Conta no GitHub
- Código commitado no GitHub

## 🚀 Passo a Passo para Deploy

### 1. **Configurar Variáveis de Ambiente no Railway**

No dashboard do Railway, adicione estas variáveis:

```bash
# Database (escolha uma opção)
# Opção A: MongoDB Atlas (recomendado)
MONGO_URL=mongodb+srv://usuario:senha@cluster.mongodb.net/

# Opção B: Railway MongoDB Plugin
DATABASE_URL=mongodb://mongo:27017

# Database Name
DB_NAME=pool_maintenance_db

# Frontend URL (substitua pela URL do seu app Railway)
REACT_APP_BACKEND_URL=https://seu-app-name.railway.app

# Security
SECRET_KEY=pool_maintenance_secret_key_2024

# Production
NODE_ENV=production
PYTHON_ENV=production
```

### 2. **Deploy Steps**

1. **Push para GitHub**: Certifique-se que todos os arquivos estão no GitHub
2. **Conectar no Railway**: 
   - Acesse railway.app
   - Click "Start a New Project"
   - Escolha "Deploy from GitHub repo"
   - Selecione seu repositório

3. **Configurar Build**: O Railway deve detectar automaticamente os arquivos de configuração

### 3. **Banco de Dados**

**Opção A - MongoDB Atlas (Recomendado):**
1. Crie uma conta no MongoDB Atlas
2. Crie um cluster gratuito
3. Configure uma database chamada `pool_maintenance_db`
4. Obtenha a connection string
5. Configure MONGO_URL no Railway

**Opção B - Railway MongoDB Plugin:**
1. No Railway, adicione o MongoDB plugin
2. Use DATABASE_URL=mongodb://mongo:27017

### 4. **Credenciais Padrão**

Após deploy, use estas credenciais:
- **Admin**: admin / admin123  
- **Test Admin**: testadmin / test123

### 5. **URLs Importantes**

- **Frontend**: https://seu-app.railway.app
- **API**: https://seu-app.railway.app/api
- **Health Check**: https://seu-app.railway.app/api/

## 🔧 Arquivos de Configuração Incluídos

- `nixpacks.toml` - Configuração de build para Railway
- `railway.json` - Configurações do Railway  
- `Procfile` - Comando de start
- `.env.example` - Exemplo de variáveis de ambiente

## 🐛 Troubleshooting

**Build Failed:**
- Verifique se todas as dependências estão no package.json e requirements.txt
- Confirme que os arquivos de configuração estão no root do projeto

**App não inicia:**
- Verifique as variáveis de ambiente
- Confirme a MONGO_URL está correta
- Check os logs do Railway

**Frontend não carrega:**
- Verifique se REACT_APP_BACKEND_URL está configurada
- Confirme que o build do React foi executado

## 📞 Suporte

Se houver problemas, verifique:
1. Logs no Railway dashboard
2. Variáveis de ambiente configuradas
3. Conexão com banco de dados
4. Build executou com sucesso