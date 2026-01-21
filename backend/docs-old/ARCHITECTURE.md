# Lottery Adviser - Monorepo Architecture

Este documento descreve a arquitetura do monorepo e as decisões de design.

## Estrutura do Monorepo

### Apps (`apps/`)

Contém as aplicações independentes que podem ser deployadas separadamente:

#### `apps/api/` - FastAPI Backend

- **Responsabilidade**: API REST para análise e sugestões de loteria
- **Stack**: Python, FastAPI, SQLAlchemy, Pandas
- **Deploy**: Render.com
- **Porta**: 8000

#### `apps/mobile/` - Expo React Native (Futuro)

- **Responsabilidade**: Aplicativo móvel iOS/Android
- **Stack**: TypeScript, Expo, React Native
- **Deploy**: App Store / Google Play

### Packages (`packages/`)

Código compartilhado entre as aplicações:

#### `packages/shared/`

- **`constants/`**: Constantes compartilhadas (números min/max, configurações)
- **`data/`**: Dados históricos da loteria
- **`types/`**: TypeScript types (futuro) para compartilhar com mobile

### Tools (`tools/`)

Scripts utilitários para desenvolvimento:

- Verificação de instalação
- Scripts de migração
- Ferramentas de análise

### Docs (`docs/`)

Documentação consolidada do projeto:

- Guias de desenvolvimento
- Decisões arquiteturais
- Setup e configuração

## Princípios de Design

### 1. Separação de Responsabilidades

- Cada app é independente e pode ser deployado separadamente
- Código compartilhado vive em `packages/`
- Ferramentas de desenvolvimento em `tools/`

### 2. DRY (Don't Repeat Yourself)

- Constantes definidas uma vez em `packages/shared/constants/`
- Dados históricos centralizados em `packages/shared/data/`
- Types compartilhados (futuro) para garantir consistência

### 3. Versionamento Sincronizado

- Mudanças na API e mobile podem ser commitadas juntas
- Facilita refactoring cross-app
- Histórico unificado do projeto

### 4. Deploy Independente

- API e mobile têm pipelines de deploy separados
- Cada app pode evoluir em seu próprio ritmo
- Rollback independente em caso de problemas

## Fluxo de Dados

```
┌─────────────────┐
│  Mobile App     │
│  (Expo)         │
└────────┬────────┘
         │
         │ HTTP/REST
         │
         ▼
┌─────────────────┐      ┌──────────────────┐
│  API            │─────▶│  Database        │
│  (FastAPI)      │      │  (PostgreSQL)    │
└────────┬────────┘      └──────────────────┘
         │
         │ Lê dados
         │
         ▼
┌─────────────────┐
│  Shared Data    │
│  (packages/)    │
└─────────────────┘
```

## Estratégias de Compartilhamento

### Python (API ↔ Shared)

```python
# Na API
from packages.shared.constants import LOTTERY_MIN_NUMBER, LOTTERY_MAX_NUMBER
```

### TypeScript (Mobile ↔ Shared) - Futuro

```typescript
// No mobile
import { LOTTERY_MIN_NUMBER, LOTTERY_MAX_NUMBER } from "@shared/constants";
```

## Convenções de Código

### Imports

- **Absolutos**: Preferir imports absolutos dentro de cada app
- **Shared**: Sempre importar de `packages.shared.*`

### Naming

- **Apps**: kebab-case para diretórios (`apps/api/`)
- **Packages**: snake_case para Python, camelCase para TypeScript
- **Constants**: UPPER_SNAKE_CASE

### Commits

- Prefixos: `api:`, `mobile:`, `shared:`, `docs:`
- Exemplo: `api: add rate limiting` ou `shared: update lottery constants`

## CI/CD

### GitHub Actions (Futuro)

```yaml
# .github/workflows/api-deploy.yml
- Trigger: mudanças em apps/api/ ou packages/shared/
- Deploy: Render.com

# .github/workflows/mobile-build.yml
- Trigger: mudanças em apps/mobile/ ou packages/shared/
- Build: Expo EAS
```

## Migração Histórica

Este monorepo foi criado a partir de dois repositórios separados:

1. **lottery-adviser** (original)
   - Código Python standalone
   - Scripts CLI
   - Dados históricos

2. **lottery-adviser-api** (API)
   - FastAPI backend
   - Sistema de autenticação
   - Endpoints REST

### O que foi consolidado:

- ✅ Dados históricos → `packages/shared/data/`
- ✅ Scripts CLI → `apps/api/scripts/`
- ✅ Documentação → `docs/`
- ✅ Constantes → `packages/shared/constants/`

### O que foi removido:

- ❌ Código duplicado (statistics, strategy generators)
- ❌ Arquivos de teste temporários
- ❌ Build artifacts

## Próximos Passos

1. **Criar app mobile** em `apps/mobile/`
2. **Configurar TypeScript types** em `packages/shared/types/`
3. **Setup CI/CD** com GitHub Actions
4. **Docker Compose** para desenvolvimento local
5. **Turborepo** para otimizar builds (opcional)

---

**Data da migração**: 2026-01-19
**Versão**: 0.1.0
