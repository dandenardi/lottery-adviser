# Deployment Guide - Render.com

Este guia detalha o processo completo de deploy do backend Lottery Adviser API no Render.com.

## Pré-requisitos

- Conta no [Render.com](https://render.com) (gratuita)
- Repositório GitHub com o código (`dandenardi/lottery-adviser`)
- Git configurado localmente

## Visão Geral

O deploy utiliza o arquivo `render.yaml` (Infrastructure as Code) que automaticamente cria:

- **Web Service**: FastAPI rodando com Gunicorn + Uvicorn workers
- **PostgreSQL Database**: Banco de dados gerenciado (1GB free tier)

## Passo a Passo

### 1. Preparar o Repositório

Certifique-se de que todas as alterações estão commitadas e enviadas para o GitHub:

```bash
cd c:\programming\lottery-adviser
git add .
git commit -m "Configure Render deployment"
git push origin main
```

### 2. Criar Conta no Render

1. Acesse [render.com](https://render.com)
2. Clique em "Get Started for Free"
3. Faça login com GitHub
4. Autorize o Render a acessar seus repositórios

### 3. Criar Novo Blueprint

1. No Dashboard do Render, clique em **"New +"** → **"Blueprint"**
2. Conecte seu repositório: `dandenardi/lottery-adviser`
3. Render detectará automaticamente o `backend/render.yaml`
4. Clique em **"Apply"**

O Render criará automaticamente:

- ✅ PostgreSQL database: `lottery-db`
- ✅ Web service: `lottery-adviser-api`

### 4. Configurar Variáveis de Ambiente Sensíveis

Algumas variáveis não devem estar no `render.yaml` por questões de segurança. Configure-as manualmente:

1. Acesse o serviço `lottery-adviser-api` no Dashboard
2. Vá em **"Environment"**
3. Adicione as seguintes variáveis (se aplicável):

```bash
# RevenueCat (opcional - apenas se já tiver configurado)
REVENUECAT_API_KEY=seu_api_key_aqui
REVENUECAT_WEBHOOK_SECRET=seu_webhook_secret_aqui
```

### 5. Aguardar o Deploy

O primeiro deploy pode levar 5-10 minutos:

1. Render fará o build instalando as dependências (`pip install -r requirements.txt`)
2. Criará o banco de dados PostgreSQL
3. Iniciará o serviço com Gunicorn

Acompanhe o progresso na aba **"Logs"**.

### 6. Verificar o Deploy

Após o deploy completar, você receberá uma URL como:

```
https://lottery-adviser-api.onrender.com
```

#### Teste os endpoints:

**1. Endpoint raiz:**

```bash
curl https://lottery-adviser-api.onrender.com/
```

Resposta esperada:

```json
{
  "message": "Welcome to Lottery Adviser API",
  "version": "1.0.0",
  "docs": "Documentation disabled in production"
}
```

**2. Health check:**

```bash
curl https://lottery-adviser-api.onrender.com/health
```

Resposta esperada:

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "database": "healthy",
  "timestamp": "2026-02-10T20:30:00.000Z"
}
```

**3. Último resultado da loteria:**

```bash
curl https://lottery-adviser-api.onrender.com/api/v1/lottery/latest
```

**4. Estatísticas:**

```bash
curl https://lottery-adviser-api.onrender.com/api/v1/lottery/statistics
```

**5. Gerar sugestões:**

```bash
curl -X POST https://lottery-adviser-api.onrender.com/api/v1/lottery/suggestions \
  -H "Content-Type: application/json" \
  -d '{"strategy": "balanced", "count": 3}'
```

### 7. Atualizar Frontend

Após confirmar que o backend está funcionando, atualize o arquivo `frontend/.env`:

```bash
# frontend/.env
EXPO_PUBLIC_API_BASE_URL=https://lottery-adviser-api.onrender.com
```

Depois, reinicie o Expo:

```bash
cd c:\programming\lottery-adviser\frontend
npm start
```

## Configurações Importantes

### Free Tier Limitations

O plano gratuito do Render tem algumas limitações:

- ⏰ **Sleep após 15 min de inatividade**: O serviço "dorme" após 15 minutos sem requisições
- 🐌 **Cold start**: Primeira requisição após sleep pode levar 30-60 segundos
- 💾 **750 horas/mês**: Suficiente para testes, mas não para produção 24/7
- 🗄️ **1GB de banco de dados**: Suficiente para ~100k resultados de loteria

### Scheduler Desabilitado

Por padrão, o scheduler está **desabilitado** (`SCHEDULER_ENABLED=false`) no `render.yaml` porque:

- O free tier entra em sleep, interrompendo tarefas agendadas
- Não é confiável para atualizações automáticas

**Alternativas:**

1. **Cron-job.org (Recomendado para free tier)**:
   - Crie uma conta em [cron-job.org](https://cron-job.org)
   - Configure um job para chamar `https://lottery-adviser-api.onrender.com/health` a cada 14 minutos
   - Isso mantém o serviço "acordado" e permite que o scheduler funcione

2. **Habilitar scheduler manualmente**:
   - No Render Dashboard, vá em Environment
   - Mude `SCHEDULER_ENABLED` para `true`
   - ⚠️ Só funcionará enquanto houver tráfego regular

3. **Upgrade para plano pago** ($7/mês):
   - Sem sleep mode
   - Scheduler funciona 24/7

### CORS Configuration

Atualmente configurado para aceitar **todas as origens** (`CORS_ORIGINS=*`) para facilitar testes.

**Para produção**, atualize no Render Dashboard:

```bash
# Exemplo com múltiplas origens
CORS_ORIGINS=https://seu-app.com,exp://seu-expo-app,https://outro-dominio.com
```

## Monitoramento

### Logs em Tempo Real

No Render Dashboard:

1. Acesse o serviço `lottery-adviser-api`
2. Clique em **"Logs"**
3. Veja logs em tempo real da aplicação

### Métricas

Na aba **"Metrics"**, você pode ver:

- CPU usage
- Memory usage
- Request count
- Response times

### Alertas

Configure alertas em **"Settings"** → **"Notifications"** para:

- Deploy failures
- Service crashes
- High error rates

## Atualizações

### Deploy Automático

Por padrão, o Render faz deploy automático quando você faz push para `main`:

```bash
git add .
git commit -m "Update feature X"
git push origin main
```

O Render detectará a mudança e fará o deploy automaticamente.

### Deploy Manual

Para desabilitar auto-deploy:

1. Vá em **"Settings"** → **"Build & Deploy"**
2. Desmarque "Auto-Deploy"
3. Use o botão **"Manual Deploy"** quando quiser atualizar

## Troubleshooting

### ❌ Build Failed

**Erro**: `ERROR: Could not find a version that satisfies the requirement...`

**Solução**: Verifique `requirements.txt` e certifique-se de que todas as versões são compatíveis com Python 3.11.

### ❌ Database Connection Error

**Erro**: `could not connect to server: Connection refused`

**Solução**:

1. Verifique se o banco `lottery-db` foi criado
2. Confirme que `DATABASE_URL` está sendo injetada automaticamente
3. Veja logs do banco de dados em "Databases" → "lottery-db" → "Logs"

### ❌ Health Check Failing

**Erro**: Health check retorna 503 ou timeout

**Solução**:

1. Verifique logs do serviço
2. Confirme que o serviço está rodando: `ps aux` nos logs
3. Teste localmente primeiro: `uvicorn app.main:app`

### ❌ CORS Error no Frontend

**Erro**: `Access to fetch at '...' from origin '...' has been blocked by CORS policy`

**Solução**:

1. Verifique `CORS_ORIGINS` no Render Dashboard
2. Adicione a origem do seu frontend
3. Para testes, use `CORS_ORIGINS=*`

### ❌ Service Sleeping

**Sintoma**: Primeira requisição muito lenta (30-60s)

**Solução**:

1. Configure cron-job.org para manter o serviço acordado
2. Ou faça upgrade para plano pago

### ❌ Scheduler Não Executa

**Sintoma**: Dados da loteria não atualizam automaticamente

**Solução**:

1. Verifique se `SCHEDULER_ENABLED=true`
2. Configure cron-job.org para evitar sleep
3. Ou chame manualmente `/api/v1/lottery/update` periodicamente

## Banco de Dados

### Acessar PostgreSQL

Para acessar o banco diretamente:

1. No Dashboard, vá em "Databases" → "lottery-db"
2. Copie a "External Connection String"
3. Use um cliente PostgreSQL (pgAdmin, DBeaver, etc.)

```bash
# Exemplo com psql
psql "postgresql://user:password@host.region.render.com/dbname"
```

### Backup

Render faz backups automáticos no plano gratuito, mas com retenção limitada.

Para backup manual:

```bash
pg_dump "postgresql://user:password@host.region.render.com/dbname" > backup.sql
```

### Migrations

Se você usar Alembic para migrations:

```bash
# Localmente, apontando para o banco de produção
export DATABASE_URL="postgresql://user:password@host.region.render.com/dbname"
alembic upgrade head
```

## Próximos Passos

1. ✅ Deploy do backend concluído
2. 🔄 Testar todos os endpoints
3. 📱 Atualizar frontend com a URL de produção
4. 🔐 Configurar RevenueCat (se aplicável)
5. 📊 Monitorar logs e métricas
6. 🚀 Deploy do frontend (Expo EAS ou similar)

## Recursos Úteis

- [Render Documentation](https://render.com/docs)
- [Render Free Tier Limits](https://render.com/docs/free)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [PostgreSQL on Render](https://render.com/docs/databases)
