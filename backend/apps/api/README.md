# Lottery Adviser API

FastAPI backend para análise de dados da Lotofácil e geração de sugestões.

## 🚀 Quick Start

### Instalação

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instalar dependências
pip install -r requirements.txt
```

### Configuração

```bash
# Copiar arquivo de exemplo
copy .env.example .env

# Editar .env com suas configurações
# Configurar DATABASE_URL, SECRET_KEY, etc.
```

### Executar

```bash
# Modo desenvolvimento
uvicorn app.main:app --reload

# Modo produção
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Acesse:

- **API**: http://localhost:8000
- **Documentação**: http://localhost:8000/docs
- **Redoc**: http://localhost:8000/redoc

## 📁 Estrutura

```
app/
├── api/                    # Endpoints da API
│   ├── v1/
│   │   ├── auth.py        # Autenticação
│   │   ├── suggestions.py # Sugestões de números
│   │   └── users.py       # Gerenciamento de usuários
│   └── deps.py            # Dependências
│
├── core/                   # Configuração central
│   ├── config.py          # Settings
│   ├── security.py        # JWT, hashing
│   └── database.py        # Conexão DB
│
├── models/                 # Modelos SQLAlchemy
│   ├── user.py
│   ├── subscription.py
│   └── suggestion.py
│
├── schemas/                # Pydantic schemas
│   ├── user.py
│   ├── auth.py
│   └── suggestion.py
│
├── services/               # Lógica de negócio
│   ├── statistics_service.py
│   ├── strategy_service.py
│   ├── subscription_service.py
│   └── rate_limit_service.py
│
└── main.py                # Entry point

scripts/
├── generate_suggestions.py  # CLI para gerar sugestões
├── run_pipeline.py          # Pipeline de análise
└── migrate_data.py          # Migração de dados
```

## 🔑 Variáveis de Ambiente

Configurar no arquivo `.env`:

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost/lottery_adviser

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000"]

# Rate Limiting
RATE_LIMIT_FREE_TIER=10
RATE_LIMIT_PREMIUM_TIER=100
```

## 📊 Endpoints Principais

### Autenticação

- `POST /api/v1/auth/register` - Registrar usuário
- `POST /api/v1/auth/login` - Login
- `GET /api/v1/auth/me` - Usuário atual

### Sugestões

- `POST /api/v1/suggestions/generate` - Gerar sugestões
- `GET /api/v1/suggestions/history` - Histórico de sugestões

### Usuários

- `GET /api/v1/users/me` - Perfil do usuário
- `PUT /api/v1/users/me` - Atualizar perfil

## 🎯 Estratégias de Sugestão

1. **Balanced** (Balanceada) - Mix de números quentes, frios e aleatórios
2. **Hot Numbers** - Prioriza números mais frequentes
3. **Cold Numbers** - Prioriza números menos frequentes
4. **Weighted Random** - Aleatória ponderada por frequência
5. **Recent Patterns** - Baseada em padrões recentes

## 🔧 Scripts CLI

### Gerar Sugestões

```bash
python scripts/generate_suggestions.py
```

Interativo, permite escolher estratégia e quantidade.

### Pipeline de Análise

```bash
python scripts/run_pipeline.py
```

Executa análise completa dos dados históricos.

## 🧪 Testes

```bash
# Instalar dependências de teste
pip install pytest pytest-cov

# Executar testes
pytest

# Com cobertura
pytest --cov=app
```

## 🚀 Deploy

### Render.com

O arquivo `render.yaml` está configurado para deploy automático.

```yaml
services:
  - type: web
    name: lottery-adviser-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Docker (Futuro)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📚 Documentação Adicional

- [Arquitetura do Monorepo](../../docs/ARCHITECTURE.md)
- [Guia de Desenvolvimento](../../docs/DEVELOPMENT.md)
- [Setup Completo](../../docs/SETUP.md)

## 🤝 Contribuindo

1. Criar branch para feature
2. Fazer mudanças
3. Testar localmente
4. Criar Pull Request

## 📝 Notas

- A API usa dados históricos de `../../packages/shared/data/`
- Constantes compartilhadas em `../../packages/shared/constants/`
- Rate limiting baseado em tier de assinatura (Free/Premium)

---

**Parte do monorepo lottery-adviser**
