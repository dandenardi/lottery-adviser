# Frontend Integration - Quick Guide

## ✅ Configuração Concluída

O frontend já está configurado para usar o backend em produção:

**URL de Produção**: `https://lottery-adviser-api.onrender.com`

## 🚀 Como Testar

### 1. Reiniciar o Expo

```bash
cd c:\programming\lottery-adviser\frontend
npm start
```

### 2. Aguardar "Cold Start"

> [!IMPORTANT]
> **Primeira requisição pode demorar 30-60 segundos** porque o serviço gratuito do Render entra em "sleep" após 15 minutos de inatividade.

### 3. Testar Funcionalidades

- **Tela Inicial**: Deve carregar o último resultado da loteria
- **Estatísticas**: Deve mostrar números mais/menos sorteados
- **Sugestões**: Deve gerar sugestões baseadas em estratégias

## 🔄 Alternar entre Local e Produção

Edite `frontend/.env`:

**Para Produção (atual)**:

```bash
EXPO_PUBLIC_API_BASE_URL=https://lottery-adviser-api.onrender.com
EXPO_PUBLIC_API_BASE_URL_MOBILE=https://lottery-adviser-api.onrender.com
```

**Para Desenvolvimento Local**:

```bash
EXPO_PUBLIC_API_BASE_URL=http://localhost:8000
EXPO_PUBLIC_API_BASE_URL_MOBILE=http://192.168.0.109:8000
```

Depois de alterar, reinicie o Expo (`npm start`).

## 📊 Endpoints Disponíveis

| Endpoint                 | Descrição           |
| ------------------------ | ------------------- |
| `/api/v1/results/latest` | Último resultado    |
| `/api/v1/statistics`     | Estatísticas gerais |
| `/api/v1/suggestions`    | Gerar sugestões     |
| `/api/v1/history`        | Histórico paginado  |
| `/health`                | Health check        |

## ⚠️ Limitações do Free Tier

- **Sleep Mode**: Serviço dorme após 15 min sem uso
- **Cold Start**: Primeira requisição lenta (30-60s)
- **Rate Limit**: 3 sugestões/dia para usuários free

## 🐛 Troubleshooting

### Erro: "Network Error"

- Verifique se a URL está correta no `.env`
- Aguarde 60s (cold start)
- Verifique logs do Render

### Erro: "CORS"

- Já configurado para aceitar todas as origens
- Se persistir, verifique `CORS_ORIGINS` no Render Dashboard

### Timeout

- Aumente o timeout em `services/api.ts` (linha 58):
  ```typescript
  timeout: 30000, // 30 segundos
  ```
