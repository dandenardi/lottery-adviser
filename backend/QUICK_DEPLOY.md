# 🚀 Quick Deploy Guide

## Passo a Passo Rápido

### 1️⃣ Commit e Push

```bash
cd c:\programming\lottery-adviser
git add .
git commit -m "Configure Render deployment"
git push origin main
```

### 2️⃣ Criar no Render

1. Acesse [render.com](https://render.com) e faça login com GitHub
2. Clique em **"New +"** → **"Blueprint"**
3. Selecione `dandenardi/lottery-adviser`
4. Clique em **"Apply"**

### 3️⃣ Aguardar Deploy

⏱️ 5-10 minutos para build completar

### 4️⃣ Testar

Você receberá uma URL como: `https://lottery-adviser-api.onrender.com`

```bash
# Teste rápido
curl https://lottery-adviser-api.onrender.com/health
```

### 5️⃣ Atualizar Frontend

Edite `frontend/.env`:

```
EXPO_PUBLIC_API_BASE_URL=https://lottery-adviser-api.onrender.com
```

## ⚠️ Importante

- **Sleep Mode**: Serviço dorme após 15 min sem uso (free tier)
- **CORS**: Configurado para aceitar todas as origens durante testes
- **Scheduler**: Desabilitado no free tier

## 📚 Documentação Completa

Ver [DEPLOYMENT.md](file:///c:/programming/lottery-adviser/backend/DEPLOYMENT.md) para guia detalhado.
