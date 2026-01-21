# 🎉 Migração para Monorepo Concluída!

## ✅ O que foi feito

### 1. Estrutura de Diretórios Criada

```
lottery-adviser-api/ (renomear para lottery-adviser)
├── apps/
│   └── api/                    ✅ API movida para apps/api/
├── packages/
│   └── shared/                 ✅ Código compartilhado criado
│       ├── constants/          ✅ Constantes da loteria
│       └── data/              ✅ Dados históricos copiados
├── tools/                      ✅ Scripts utilitários
├── docs/                       ✅ Documentação consolidada
└── README.md                   ✅ README do monorepo
```

### 2. Arquivos Migrados

#### Da API (lottery-adviser-api → apps/api/)

- ✅ `app/` → `apps/api/app/`
- ✅ `scripts/` → `apps/api/scripts/`
- ✅ `requirements.txt` → `apps/api/requirements.txt`
- ✅ `render.yaml` → `apps/api/render.yaml`
- ✅ `.env.example` → `apps/api/.env.example`

#### Do Repositório Original (lottery-adviser → packages/shared/)

- ✅ Dados históricos → `packages/shared/data/loto_facil_asloterias_ate_concurso_3576_sorteio.xlsx`
- ✅ Scripts úteis → `apps/api/scripts/` (generate_suggestions.py, run_pipeline.py)
- ✅ Documentação → `docs/` (DEVELOPMENT.md, SETUP.md)

### 3. Novos Arquivos Criados

- ✅ `README.md` - Documentação principal do monorepo
- ✅ `.gitignore` - Configuração para Python + Node.js + Expo
- ✅ `docs/ARCHITECTURE.md` - Arquitetura e decisões de design
- ✅ `packages/shared/constants/lottery.py` - Constantes compartilhadas
- ✅ `packages/shared/constants/__init__.py` - Package init
- ✅ `packages/shared/__init__.py` - Package init

## 🔄 Próximos Passos

### Passo 1: Renomear o Repositório

```powershell
# No diretório C:\programming\
cd C:\programming
Rename-Item -Path "lottery-adviser-api" -NewName "lottery-adviser-temp"
Rename-Item -Path "lottery-adviser" -NewName "lottery-adviser-old-backup"
Rename-Item -Path "lottery-adviser-temp" -NewName "lottery-adviser"
```

### Passo 2: Atualizar Git Remote (se aplicável)

```bash
cd C:\programming\lottery-adviser
git remote -v  # Verificar remotes atuais
# Se necessário, atualizar o remote para o novo nome do repo
```

### Passo 3: Testar a API

```bash
cd C:\programming\lottery-adviser\apps\api

# Criar ambiente virtual
python -m venv venv
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Copiar .env
copy .env.example .env
# Editar .env com suas configurações

# Testar a API
uvicorn app.main:app --reload
```

Acesse: http://localhost:8000/docs

### Passo 4: Atualizar Imports (se necessário)

A API já deve funcionar sem mudanças, mas você pode opcionalmente atualizar para usar as constantes compartilhadas:

**Antes:**

```python
# Em apps/api/app/services/statistics_service.py
LOTTERY_MIN_NUMBER = 1
LOTTERY_MAX_NUMBER = 25
```

**Depois:**

```python
# Em apps/api/app/services/statistics_service.py
from packages.shared.constants import LOTTERY_MIN_NUMBER, LOTTERY_MAX_NUMBER
```

### Passo 5: Preparar para o Expo

Quando estiver pronto para criar o app mobile:

```bash
cd C:\programming\lottery-adviser\apps
npx create-expo-app mobile --template blank-typescript
cd mobile
npm install
```

### Passo 6: Configurar Shared Types (Futuro)

Para compartilhar types entre API e Mobile:

```bash
cd C:\programming\lottery-adviser\packages\shared
mkdir types
# Criar types TypeScript que refletem os schemas da API
```

## 📝 Arquivos que Podem Ser Deletados

Após confirmar que tudo está funcionando, você pode deletar do repositório antigo:

### No lottery-adviser-old-backup:

- ❌ Todos os arquivos de teste (`test_*.py`)
- ❌ Arquivos temporários (`check_*.py`, `file_info.json`, etc.)
- ❌ `venv/`, `__pycache__/`, `*.egg-info/`
- ❌ Código duplicado já migrado para a API

**Mantenha o backup por segurança até confirmar que tudo funciona!**

## 🎯 Estrutura Final Esperada

```
C:\programming\
├── lottery-adviser/              # Monorepo principal (ex lottery-adviser-api)
│   ├── apps/
│   │   ├── api/                 # FastAPI
│   │   └── mobile/              # Expo (futuro)
│   ├── packages/shared/
│   ├── tools/
│   └── docs/
│
└── lottery-adviser-old-backup/   # Backup do repo original
    └── (manter por segurança)
```

## ✨ Benefícios Alcançados

1. ✅ **Código Unificado**: Tudo em um único repositório
2. ✅ **Compartilhamento**: Constantes e dados centralizados
3. ✅ **Organização**: Estrutura clara com apps/ e packages/
4. ✅ **Documentação**: Consolidada e atualizada
5. ✅ **Preparado para Expo**: Estrutura pronta para adicionar mobile app
6. ✅ **Deploy Independente**: API e mobile podem ser deployados separadamente

## 🆘 Troubleshooting

### Problema: API não inicia

```bash
# Verificar se está no diretório correto
cd C:\programming\lottery-adviser\apps\api

# Verificar se o venv está ativado
venv\Scripts\activate

# Reinstalar dependências
pip install -r requirements.txt
```

### Problema: Imports não funcionam

```python
# Adicionar o root do monorepo ao PYTHONPATH
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
```

### Problema: Dados não encontrados

```python
# Atualizar path para os dados compartilhados
from pathlib import Path
DATA_PATH = Path(__file__).parent.parent.parent.parent / "packages/shared/data"
```

## 📞 Suporte

Se encontrar problemas:

1. Verifique a documentação em `docs/`
2. Revise este guia de migração
3. Consulte o backup em `lottery-adviser-old-backup/`

---

**Data da Migração**: 2026-01-19  
**Status**: ✅ Concluída  
**Próximo Passo**: Renomear repositório e testar API
