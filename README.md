# Lottery Adviser - Monorepo

> Sistema de análise de dados históricos de loteria e geração de sugestões heurísticas

## 📁 Estrutura do Projeto

Este é um monorepo que contém:

- **`backend/`** - API FastAPI com toda a lógica de negócio
- **`frontend/`** - Futuro aplicativo React Native (planejado)

## 🚀 Quick Start

### Backend

```bash
cd backend
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env

# Rodar a API
uvicorn app.main:app --reload
```

### Scripts Standalone

```bash
cd backend
python scripts/generate_suggestions.py
python scripts/run_pipeline.py
```

## 📚 Documentação

- [Backend README](./backend/README.md) - Documentação completa da API
- [Setup Guide](./SETUP.md) - Guia de configuração detalhado
- [Development Guide](./DEVELOPMENT.md) - Guia para desenvolvedores

## 🏗️ Arquitetura

```
lottery-adviser/
├── backend/              # Backend FastAPI
│   ├── app/
│   │   ├── api/         # Endpoints REST
│   │   ├── core/        # Config e database
│   │   ├── models/      # SQLAlchemy models
│   │   ├── schemas/     # Pydantic schemas
│   │   └── services/    # Lógica de negócio
│   │       ├── collectors/   # Coleta de dados
│   │       ├── analysis/     # Análise estatística
│   │       ├── storage/      # Persistência
│   │       └── pipelines/    # Orquestração
│   ├── scripts/         # Scripts utilitários
│   ├── tests/           # Testes
│   └── data/            # Dados históricos
│
└── frontend/            # Futuro app React Native
```

## 🛠️ Tecnologias

### Backend

- **FastAPI** - Framework web moderno
- **SQLAlchemy** - ORM
- **PostgreSQL** - Database
- **Pandas** - Análise de dados
- **Pydantic** - Validação de dados

### Frontend (Planejado)

- **React Native** - Framework mobile
- **Expo** - Toolchain
- **TypeScript** - Type safety

## 📝 License

MIT
