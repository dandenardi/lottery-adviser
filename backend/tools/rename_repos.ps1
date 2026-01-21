# Script para renomear repositórios durante migração do monorepo
# Este script deve ser executado de C:\programming\

Write-Host "🔄 Iniciando renomeação dos repositórios..." -ForegroundColor Cyan
Write-Host ""

# Verificar se estamos no diretório correto
$currentDir = Get-Location
if ($currentDir.Path -ne "C:\programming") {
    Write-Host "❌ ERRO: Este script deve ser executado de C:\programming\" -ForegroundColor Red
    Write-Host "   Diretório atual: $currentDir" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Execute:" -ForegroundColor Cyan
    Write-Host "   cd C:\programming" -ForegroundColor White
    Write-Host "   .\lottery-adviser-api\tools\rename_repos.ps1" -ForegroundColor White
    exit 1
}

# Verificar se os diretórios existem
$apiDir = "lottery-adviser-api"
$oldDir = "lottery-adviser"

if (-not (Test-Path $apiDir)) {
    Write-Host "❌ ERRO: Diretório '$apiDir' não encontrado!" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $oldDir)) {
    Write-Host "⚠️  AVISO: Diretório '$oldDir' não encontrado." -ForegroundColor Yellow
    Write-Host "   Pulando backup do repositório antigo." -ForegroundColor Yellow
    $skipBackup = $true
} else {
    $skipBackup = $false
}

# Mostrar plano
Write-Host "📋 Plano de renomeação:" -ForegroundColor Cyan
Write-Host ""
if (-not $skipBackup) {
    Write-Host "   1. lottery-adviser → lottery-adviser-old-backup" -ForegroundColor White
}
Write-Host "   2. lottery-adviser-api → lottery-adviser" -ForegroundColor White
Write-Host ""

# Confirmar com usuário
$confirmation = Read-Host "Deseja continuar? (S/N)"
if ($confirmation -ne "S" -and $confirmation -ne "s") {
    Write-Host "❌ Operação cancelada pelo usuário." -ForegroundColor Yellow
    exit 0
}

Write-Host ""

# Executar renomeação
try {
    if (-not $skipBackup) {
        Write-Host "📦 Fazendo backup: lottery-adviser → lottery-adviser-old-backup" -ForegroundColor Cyan
        Rename-Item -Path $oldDir -NewName "lottery-adviser-old-backup" -ErrorAction Stop
        Write-Host "   ✅ Backup criado com sucesso!" -ForegroundColor Green
    }
    
    Write-Host "🔄 Renomeando: lottery-adviser-api → lottery-adviser" -ForegroundColor Cyan
    Rename-Item -Path $apiDir -NewName "lottery-adviser" -ErrorAction Stop
    Write-Host "   ✅ Renomeado com sucesso!" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "🎉 Migração concluída com sucesso!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📍 Próximos passos:" -ForegroundColor Cyan
    Write-Host "   1. cd C:\programming\lottery-adviser\apps\api" -ForegroundColor White
    Write-Host "   2. python -m venv venv" -ForegroundColor White
    Write-Host "   3. venv\Scripts\activate" -ForegroundColor White
    Write-Host "   4. pip install -r requirements.txt" -ForegroundColor White
    Write-Host "   5. copy .env.example .env" -ForegroundColor White
    Write-Host "   6. uvicorn app.main:app --reload" -ForegroundColor White
    Write-Host ""
    
} catch {
    Write-Host ""
    Write-Host "❌ ERRO durante a renomeação:" -ForegroundColor Red
    Write-Host "   $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 Possíveis soluções:" -ForegroundColor Yellow
    Write-Host "   - Feche todos os programas que possam estar usando os diretórios" -ForegroundColor White
    Write-Host "   - Feche o VS Code, terminal, ou qualquer explorador de arquivos" -ForegroundColor White
    Write-Host "   - Tente novamente" -ForegroundColor White
    exit 1
}
