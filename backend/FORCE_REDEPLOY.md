# Forçando Redeploy no Render

## Problema Identificado

O commit `94697bc` (fix: remove duplicate /api/v1 prefix from routers) foi feito push para o GitHub, mas o Render não está fazendo deploy automático.

## Soluções

### 1. Commit Vazio (Trigger Automático)

Criar um commit vazio para forçar o Render a detectar mudanças:

```bash
git commit --allow-empty -m "chore: trigger Render redeploy"
git push
```

Isso deve fazer o Render detectar a mudança e iniciar um novo deploy.

### 2. Deploy Manual no Dashboard

Se o commit vazio não funcionar:

1. Acesse https://dashboard.render.com
2. Clique no serviço `lottery-adviser-api`
3. Clique no botão **"Manual Deploy"** no canto superior direito
4. Selecione **"Deploy latest commit"**
5. Aguarde o deploy completar (3-5 minutos)

### 3. Clear Build Cache + Deploy

Se ainda não funcionar, pode ser cache:

1. No Dashboard, vá em **"Settings"**
2. Role até **"Build & Deploy"**
3. Clique em **"Clear build cache"**
4. Volte para a página principal do serviço
5. Clique em **"Manual Deploy"** → **"Clear build cache & deploy"**

## Verificar Deploy

Após o deploy completar:

1. Verifique que o status está **"Live"** (verde)
2. Clique em **"Logs"** e procure por:
   ```
   🚀 Starting Lottery Adviser API v1.0.0
   ```
3. Teste o endpoint:
   ```bash
   curl https://lottery-adviser-api.onrender.com/api/v1/results/latest
   ```

Se retornar JSON com dados da loteria, está funcionando!

## Configuração de Auto-Deploy

Verifique se o auto-deploy está habilitado:

1. No Dashboard, vá em **"Settings"**
2. Procure por **"Auto-Deploy"**
3. Certifique-se de que está **ENABLED**
4. Verifique se a branch é **"main"**

Se estava desabilitado, habilite e faça um novo commit vazio para testar.
