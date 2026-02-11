# Troubleshooting: API Endpoints Returning 404

## Situação Atual

- ✅ `/health` funciona: https://lottery-adviser-api.onrender.com/health
- ❌ `/api/v1/results/latest` retorna 404
- ❌ `/api/v1/statistics` retorna 404

## Possíveis Causas

### 1. Deploy Não Completou ou Falhou

O Render pode não ter feito o deploy das mudanças mais recentes.

**Como verificar:**

1. Acesse https://dashboard.render.com
2. Clique no serviço `lottery-adviser-api`
3. Verifique o status:
   - **Verde "Live"**: Deploy completou
   - **Amarelo "Deploying"**: Ainda em progresso
   - **Vermelho "Failed"**: Deploy falhou

4. Clique em **"Events"** para ver o histórico de deploys
5. Verifique se o último commit (`94697bc - fix: remove duplicate /api/v1 prefix`) foi deployado

**Se o deploy falhou:**

- Clique em "Logs" para ver o erro
- Procure por erros de build ou runtime
- Pode ser necessário fazer deploy manual: botão "Manual Deploy" → "Deploy latest commit"

### 2. Cache do Render

O Render pode estar usando uma versão em cache do código.

**Solução:**

1. No Dashboard, vá em "Settings"
2. Role até "Build & Deploy"
3. Clique em "Clear build cache"
4. Depois clique em "Manual Deploy" → "Clear build cache & deploy"

### 3. Código Não Foi Commitado Corretamente

Verifique se as mudanças estão no GitHub:

```bash
# Verificar último commit
git log -1 --oneline

# Deve mostrar: 94697bc fix: remove duplicate /api/v1 prefix
```

Se não aparecer, faça:

```bash
git status
git add -A
git commit -m "fix: remove duplicate /api/v1 prefix from routers"
git push
```

### 4. Render Não Está Monitorando a Branch Correta

**Como verificar:**

1. No Dashboard, vá em "Settings"
2. Procure por "Branch"
3. Verifique se está em `main`
4. Se estiver em outra branch, mude para `main` e salve

## Teste Manual no Render

Você pode testar diretamente no shell do Render:

1. No Dashboard, clique em "Shell" (ícone de terminal)
2. Execute:

```bash
curl http://localhost:$PORT/api/v1/results/latest
```

Se funcionar no shell mas não externamente, o problema é de roteamento/proxy.

## Solução Temporária: Testar Localmente

Enquanto investigamos o Render, você pode testar o frontend com o backend local:

1. **Inicie o backend local:**

```bash
cd c:\programming\lottery-adviser\backend
.\venv\Scripts\activate
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

2. **Atualize `frontend/.env`:**

```bash
EXPO_PUBLIC_API_BASE_URL=http://localhost:8000
EXPO_PUBLIC_API_BASE_URL_MOBILE=http://192.168.0.109:8000
```

3. **Reinicie o Expo:**

```bash
# Pressione Ctrl+C no terminal do npm start
npm start
```

## Próximos Passos

1. ✅ Verificar status do deploy no Render Dashboard
2. ✅ Verificar logs para erros
3. ✅ Se necessário, fazer deploy manual com cache limpo
4. ✅ Testar endpoints após deploy completar
5. ✅ Se tudo funcionar, testar frontend
