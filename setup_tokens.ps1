# Najika World - Token Setup Script
# Fragt nach allen benötigten API-Tokens und speichert sie sicher

Write-Host "================================" -ForegroundColor Cyan
Write-Host "   NAJIKA TOKEN SETUP" -ForegroundColor Magenta
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Pfad zur .env Datei
$envFile = Join-Path $PSScriptRoot ".env"
$backendEnvFile = Join-Path $PSScriptRoot "backend\.env"

# Funktion zum sicheren Eingeben von Tokens
function Get-SecureToken {
    param (
        [string]$TokenName,
        [string]$Description,
        [bool]$Required = $true
    )

    Write-Host "[$TokenName]" -ForegroundColor Yellow
    Write-Host "  $Description" -ForegroundColor Gray

    if (-not $Required) {
        Write-Host "  (Optional - Enter drücken zum Überspringen)" -ForegroundColor DarkGray
    }

    $token = Read-Host "  Token eingeben"

    if ([string]::IsNullOrWhiteSpace($token) -and $Required) {
        Write-Host "  ⚠️  Dieser Token ist erforderlich!" -ForegroundColor Red
        return Get-SecureToken -TokenName $TokenName -Description $Description -Required $Required
    }

    return $token
}

# Funktion zum Speichern der .env Datei
function Save-EnvFile {
    param (
        [hashtable]$Tokens,
        [string]$FilePath
    )

    $envContent = @"
# Najika World Environment Configuration
# Generiert am: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

"@

    foreach ($key in $Tokens.Keys) {
        if (-not [string]::IsNullOrWhiteSpace($Tokens[$key])) {
            $envContent += "$key=$($Tokens[$key])`n"
        }
    }

    Set-Content -Path $FilePath -Value $envContent -Encoding UTF8
    Write-Host "✅ Gespeichert: $FilePath" -ForegroundColor Green
}

# Sammle alle Tokens
$tokens = @{}

Write-Host "Bitte geben Sie die benötigten API-Tokens ein:" -ForegroundColor Cyan
Write-Host ""

# Anthropic Claude API (für AI)
$tokens["ANTHROPIC_API_KEY"] = Get-SecureToken `
    -TokenName "ANTHROPIC_API_KEY" `
    -Description "Claude API Key (für Najikas KI-Funktionen)" `
    -Required $false

Write-Host ""

# OpenAI API (optional, falls verwendet)
$tokens["OPENAI_API_KEY"] = Get-SecureToken `
    -TokenName "OPENAI_API_KEY" `
    -Description "OpenAI API Key (optional für zusätzliche Features)" `
    -Required $false

Write-Host ""

# Backend Konfiguration
Write-Host "Backend Konfiguration:" -ForegroundColor Cyan
$backendHost = Read-Host "Backend Host (default: 127.0.0.1)"
if ([string]::IsNullOrWhiteSpace($backendHost)) { $backendHost = "127.0.0.1" }
$tokens["BACKEND_HOST"] = $backendHost

$backendPort = Read-Host "Backend Port (default: 5000)"
if ([string]::IsNullOrWhiteSpace($backendPort)) { $backendPort = "5000" }
$tokens["BACKEND_PORT"] = $backendPort

Write-Host ""

# Ollama Konfiguration
Write-Host "Ollama Konfiguration (für lokales AI-Modell):" -ForegroundColor Cyan
$useOllama = Read-Host "Ollama verwenden? (y/n, default: y)"
if ([string]::IsNullOrWhiteSpace($useOllama) -or $useOllama -eq "y") {
    $tokens["USE_OLLAMA"] = "true"

    $ollamaUrl = Read-Host "Ollama URL (default: http://127.0.0.1:11434)"
    if ([string]::IsNullOrWhiteSpace($ollamaUrl)) { $ollamaUrl = "http://127.0.0.1:11434" }
    $tokens["OLLAMA_URL"] = $ollamaUrl

    $ollamaModel = Read-Host "Ollama Model Name (default: najika-local)"
    if ([string]::IsNullOrWhiteSpace($ollamaModel)) { $ollamaModel = "najika-local" }
    $tokens["OLLAMA_MODEL"] = $ollamaModel
} else {
    $tokens["USE_OLLAMA"] = "false"
}

Write-Host ""

# ChromaDB Konfiguration
Write-Host "ChromaDB Konfiguration (für Najikas Gedächtnis):" -ForegroundColor Cyan
$chromaPath = Read-Host "ChromaDB Pfad (default: ./backend/chromadb)"
if ([string]::IsNullOrWhiteSpace($chromaPath)) { $chromaPath = "./backend/chromadb" }
$tokens["CHROMADB_PATH"] = $chromaPath

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan

# Speichere .env Dateien
Save-EnvFile -Tokens $tokens -FilePath $envFile
Save-EnvFile -Tokens $tokens -FilePath $backendEnvFile

Write-Host ""
Write-Host "🎉 Token-Setup abgeschlossen!" -ForegroundColor Green
Write-Host ""
Write-Host "Die Tokens wurden gespeichert in:" -ForegroundColor Cyan
Write-Host "  - $envFile" -ForegroundColor Gray
Write-Host "  - $backendEnvFile" -ForegroundColor Gray
Write-Host ""
Write-Host "⚠️  WICHTIG: .env Dateien sind in .gitignore und werden NICHT commited!" -ForegroundColor Yellow
Write-Host ""
Write-Host "Nächste Schritte:" -ForegroundColor Cyan
Write-Host "  1. Backend starten: python backend/api/server.py" -ForegroundColor Gray
Write-Host "  2. Frontend starten: cd frontend && npm start" -ForegroundColor Gray
Write-Host "  3. Browser öffnen: http://localhost:3000" -ForegroundColor Gray
Write-Host ""

# Zeige Token-Status (ohne die echten Werte zu zeigen)
Write-Host "Token-Status:" -ForegroundColor Cyan
foreach ($key in $tokens.Keys) {
    $status = if ([string]::IsNullOrWhiteSpace($tokens[$key])) { "❌ Nicht gesetzt" } else { "✅ Gesetzt" }
    Write-Host "  $key`: $status" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Drücken Sie eine Taste zum Beenden..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
