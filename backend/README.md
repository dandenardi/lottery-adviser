# Lottery Adviser - Monorepo

> Sistema completo de análise e sugestões para Lotofácil com API FastAPI e aplicativo móvel Expo

## 📁 Estrutura do Projeto

```
lottery-adviser/
├── apps/
│   ├── api/                    # FastAPI Backend
│   │   ├── app/               # Código da aplicação
│   │   ├── scripts/           # Scripts CLI e utilitários
│   │   ├── requirements.txt   # Dependências Python
│   │   └── render.yaml        # Configuração Render.com
│   │
│   └── mobile/                # Expo/React Native App (em breve)
│       └── ...
│
├── packages/
│   └── shared/                # Código compartilhado
│       ├── constants/         # Constantes (min/max números, etc)
│       ├── data/             # Dados históricos da loteria
│       └── types/            # TypeScript types (futuro)
│
├── tools/                     # Scripts de desenvolvimento
│   └── verify_installation.py
│
├── docs/                      # Documentação
│   ├── DEVELOPMENT.md        # Decisões arquiteturais
│   ├── SETUP.md             # Guia de configuração
│   └── QUICKSTART-OLD.md    # Referência histórica
│
└── README.md                 # Este arquivo
```

## 🚀 Quick Start

### API (Backend)

```bash
# Navegar para o diretório da API
cd apps/api

# Criar ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
copy .env.example .env
# Editar .env com suas configurações

# Executar a API
uvicorn app.main:app --reload
```

A API estará disponível em: `http://localhost:8000`
Documentação interativa: `http://localhost:8000/docs`

### Mobile App (Em breve)

```bash
cd apps/mobile
npm install
npm start
```

## 📊 Funcionalidades

### API Backend

- ✅ Autenticação JWT
- ✅ Sistema de assinaturas (Free/Premium)
- ✅ Rate limiting por tier
- ✅ Análise estatística de histórico
- ✅ Geração de sugestões com 5 estratégias:
  - Balanceada (recomendada)
  - Hot Numbers (números quentes)
  - Cold Numbers (números frios)
  - Aleatória Ponderada
  - Padrões Recentes

### Mobile App (Planejado)

- [ ] Interface nativa iOS/Android
- [ ] Autenticação social (Google/Apple)
- [ ] Visualização de estatísticas
- [ ] Geração de sugestões
- [ ] Histórico de jogos
- [ ] Sistema de pagamento in-app

## 🛠️ Tecnologias

### Backend

- **FastAPI** - Framework web moderno e rápido
- **SQLAlchemy** - ORM para banco de dados
- **Pydantic** - Validação de dados
- **Pandas** - Análise de dados
- **JWT** - Autenticação

### Frontend (Planejado)

- **Expo** - Framework React Native
- **TypeScript** - Type safety
- **React Navigation** - Navegação
- **React Query** - State management

## 📚 Documentação

- [Guia de Desenvolvimento](docs/DEVELOPMENT.md) - Decisões arquiteturais e padrões
- [Setup Completo](docs/SETUP.md) - Configuração detalhada do ambiente
- [API Docs](http://localhost:8000/docs) - Documentação interativa (quando rodando)

## 🔧 Scripts Úteis

### API

```bash
# Gerar sugestões via CLI
cd apps/api
python scripts/generate_suggestions.py

# Executar pipeline de análise
python scripts/run_pipeline.py
```

### Ferramentas

```bash
# Verificar instalação
python tools/verify_installation.py
```

## 🌐 Deploy

### API (Render.com)

A API está configurada para deploy automático no Render.com via `apps/api/render.yaml`

### Mobile (Expo)

```bash
cd apps/mobile
eas build --platform all
eas submit
```

## 📦 Dados

Os dados históricos da Lotofácil estão em:

- `packages/shared/data/loto_facil_asloterias_ate_concurso_3576_sorteio.xlsx`

Contém todos os sorteios até o concurso 3576.

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto é privado e proprietário.

## 🎯 Roadmap

- [x] API Backend completa
- [x] Sistema de autenticação
- [x] Análise estatística
- [x] Geração de sugestões
- [ ] Aplicativo móvel Expo
- [ ] Sistema de pagamento
- [ ] Dashboard web
- [ ] Notificações push
- [ ] Compartilhamento de jogos

---

**Desenvolvido com ❤️ para ajudar jogadores da Lotofácil**
