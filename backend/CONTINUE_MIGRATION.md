# 🚀 Continuação da Migração - Guia Rápido

## Status Atual

✅ **Concluído:**

- Estrutura do monorepo criada
- API movida para `apps/api/`
- Packages compartilhados criados em `packages/shared/`
- Documentação consolidada em `docs/`
- Script de renomeação criado

⏳ **Pendente:**

- Renomear repositórios
- Testar a API
- Atualizar imports (opcional)

---

## Passo 1: Renomear Repositórios

### Opção A: Usar o Script Automatizado (Recomendado)

```powershell
# Abra um PowerShell NOVO (feche VS Code e outros programas primeiro!)
cd C:\programming
.\lottery-adviser-api\tools\rename_repos.ps1
```

O script irá:

1. Fazer backup: `lottery-adviser` → `lottery-adviser-old-backup`
2. Renomear: `lottery-adviser-api` → `lottery-adviser`

### Opção B: Renomeação Manual

```powershell
cd C:\programming

# Backup do repo antigo
Rename-Item -Path "lottery-adviser" -NewName "lottery-adviser-old-backup"

# Renomear o novo monorepo
Rename-Item -Path "lottery-adviser-api" -NewName "lottery-adviser"
```

---

## Passo 2: Testar a API

```powershell
# Navegar para o diretório da API
cd C:\programming\lottery-adviser\apps\api

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
copy .env.example .env
# Edite o arquivo .env com suas configurações

# Iniciar a API
uvicorn app.main:app --reload
```

Acesse: http://localhost:8000/docs

---

## Passo 3: Verificar Funcionalidades

### Endpoints para testar:

1. **Health Check**
   - GET `/health`
   - Deve retornar status OK

2. **Estatísticas**
   - GET `/api/v1/statistics/frequency`
   - Deve retornar frequências dos números

3. **Sugestões**
   - POST `/api/v1/suggestions/generate`
   - Body: `{"strategy": "balanced", "num_games": 1}`

---

## Passo 4: Atualizar Imports (Opcional)

Você pode atualizar a API para usar as constantes compartilhadas:

### Arquivos a atualizar:

1. **`apps/api/app/services/statistics_service.py`**
2. **`apps/api/scripts/generate_suggestions.py`**

### Mudança:

**Antes:**

```python
LOTTERY_MIN_NUMBER = 1
LOTTERY_MAX_NUMBER = 25
LOTTERY_NUMBERS_PER_GAME = 15
```

**Depois:**

```python
from packages.shared.constants import (
    LOTTERY_MIN_NUMBER,
    LOTTERY_MAX_NUMBER,
    LOTTERY_NUMBERS_PER_GAME
)
```

> **Nota:** Isso requer adicionar o root do monorepo ao PYTHONPATH:
>
> ```python
> import sys
> from pathlib import Path
> sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
> ```

---

## Passo 5: Preparar para Expo (Futuro)

Quando estiver pronto para criar o app mobile:

```bash
cd C:\programming\lottery-adviser\apps
npx create-expo-app mobile --template blank-typescript
cd mobile
npm install
```

---

## 🆘 Troubleshooting

### Erro: "Não é possível renomear - arquivo em uso"

**Solução:**

1. Feche **TODOS** os programas:
   - VS Code
   - Terminais
   - Explorador de arquivos
   - Git clients
2. Tente novamente

### Erro: "ModuleNotFoundError" ao importar de packages.shared

**Solução:**

```python
# Adicione no início do arquivo
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
```

### API não inicia

**Verificações:**

```powershell
# 1. Verificar se está no diretório correto
pwd  # Deve ser: C:\programming\lottery-adviser\apps\api

# 2. Verificar se venv está ativado
# Deve aparecer (venv) no prompt

# 3. Reinstalar dependências
pip install -r requirements.txt --force-reinstall

# 4. Verificar .env
cat .env  # Verificar se as variáveis estão configuradas
```

---

## 📁 Estrutura Final

```
C:\programming\
├── lottery-adviser/                    # ← Monorepo principal
│   ├── apps/
│   │   └── api/                       # FastAPI
│   ├── packages/
│   │   └── shared/                    # Código compartilhado
│   ├── tools/                         # Scripts utilitários
│   └── docs/                          # Documentação
│
└── lottery-adviser-old-backup/        # ← Backup (manter por segurança)
```

---

## ✅ Checklist de Conclusão

- [ ] Repositórios renomeados
- [ ] API testada e funcionando
- [ ] Endpoints principais verificados
- [ ] Documentação revisada
- [ ] Backup do repo antigo mantido
- [ ] (Opcional) Imports atualizados para usar packages/shared

---

## 📞 Próximos Passos

Após concluir esta migração:

1. **Commit das mudanças**

   ```bash
   cd C:\programming\lottery-adviser
   git add .
   git commit -m "chore: complete monorepo migration"
   ```

2. **Atualizar remote (se aplicável)**

   ```bash
   git remote -v
   # Atualizar se necessário
   ```

3. **Começar desenvolvimento do mobile**
   - Ver Passo 5 acima

---

**Data:** 2026-01-19  
**Status:** Pronto para renomeação e testes  
**Próximo:** Execute o Passo 1
