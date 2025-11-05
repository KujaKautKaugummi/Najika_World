# ═══════════════════════════════════════════════════════════════════
# 🌟 NAJIKA PROJECT - INSTALLER PART 1: BASE SETUP
# ═══════════════════════════════════════════════════════════════════
# Version: 2.5
# Part: 1/5 - Base System Setup
# Description: Installs Python, Node.js, Git, and system dependencies
# ═══════════════════════════════════════════════════════════════════

Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "🌟 NAJIKA PROJECT - INSTALLER PART 1/5" -ForegroundColor Magenta
Write-Host "Base System Setup (Python, Node.js, Git, CUDA)" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# ═══════════════════════════════════════════════════════════════════
# 1. CHECK FOR ADMIN RIGHTS
# ═══════════════════════════════════════════════════════════════════

$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "❌ FEHLER: Dieser Installer benötigt Administrator-Rechte!" -ForegroundColor Red
    Write-Host "Bitte starte PowerShell als Administrator und führe das Skript erneut aus." -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "✅ Administrator-Rechte bestätigt" -ForegroundColor Green
Write-Host ""

# ═══════════════════════════════════════════════════════════════════
# 2. SET PROJECT DIRECTORY
# ═══════════════════════════════════════════════════════════════════

$projectRoot = "C:\Najika"
Write-Host "📁 Projekt-Verzeichnis: $projectRoot" -ForegroundColor Cyan

if (-not (Test-Path $projectRoot)) {
    New-Item -Path $projectRoot -ItemType Directory -Force | Out-Null
    Write-Host "✅ Projekt-Verzeichnis erstellt" -ForegroundColor Green
} else {
    Write-Host "⚠️  Projekt-Verzeichnis existiert bereits" -ForegroundColor Yellow
}

Set-Location $projectRoot
Write-Host ""

# ═══════════════════════════════════════════════════════════════════
# 3. CHECK/INSTALL CHOCOLATEY
# ═══════════════════════════════════════════════════════════════════

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "🍫 Chocolatey Package Manager" -ForegroundColor Magenta
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

if (!(Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Host "📦 Installiere Chocolatey..." -ForegroundColor Yellow
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    
    # Refresh environment
    $env:ChocolateyInstall = Convert-Path "$((Get-Command choco).Path)\..\.."
    Import-Module "$env:ChocolateyInstall\helpers\chocolateyProfile.psm1"
    refreshenv
    
    Write-Host "✅ Chocolatey installiert" -ForegroundColor Green
} else {
    Write-Host "✅ Chocolatey bereits installiert" -ForegroundColor Green
}

Write-Host ""

# ═══════════════════════════════════════════════════════════════════
# 4. INSTALL PYTHON 3.11
# ═══════════════════════════════════════════════════════════════════

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "🐍 Python 3.11 Installation" -ForegroundColor Magenta
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "📦 Installiere Python 3.11..." -ForegroundColor Yellow
    choco install python311 -y --force
    refreshenv
    Write-Host "✅ Python 3.11 installiert" -ForegroundColor Green
} else {
    $pythonVersion = python --version
    Write-Host "✅ Python bereits installiert: $pythonVersion" -ForegroundColor Green
}

# Upgrade pip
Write-Host "📦 Aktualisiere pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet
Write-Host "✅ pip aktualisiert" -ForegroundColor Green
Write-Host ""

# ═══════════════════════════════════════════════════════════════════
# 5. INSTALL NODE.JS & NPM
# ═══════════════════════════════════════════════════════════════════

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "📦 Node.js & NPM Installation" -ForegroundColor Magenta
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

if (!(Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "📦 Installiere Node.js LTS..." -ForegroundColor Yellow
    choco install nodejs-lts -y --force
    refreshenv
    Write-Host "✅ Node.js installiert" -ForegroundColor Green
} else {
    $nodeVersion = node --version
    $npmVersion = npm --version
    Write-Host "✅ Node.js bereits installiert: $nodeVersion" -ForegroundColor Green
    Write-Host "✅ NPM bereits installiert: v$npmVersion" -ForegroundColor Green
}

Write-Host ""

# ═══════════════════════════════════════════════════════════════════
# 6. INSTALL GIT
# ═══════════════════════════════════════════════════════════════════

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "📚 Git Installation" -ForegroundColor Magenta
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

if (!(Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "📦 Installiere Git..." -ForegroundColor Yellow
    choco install git -y --force
    refreshenv
    Write-Host "✅ Git installiert" -ForegroundColor Green
} else {
    $gitVersion = git --version
    Write-Host "✅ Git bereits installiert: $gitVersion" -ForegroundColor Green
}

Write-Host ""

# ═══════════════════════════════════════════════════════════════════
# 7. CHECK CUDA / GPU
# ═══════════════════════════════════════════════════════════════════

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "🎮 GPU & CUDA Check (RTX 3060 Ti)" -ForegroundColor Magenta
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

if (Get-Command nvidia-smi -ErrorAction SilentlyContinue) {
    Write-Host "✅ NVIDIA GPU gefunden" -ForegroundColor Green
    nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader
    Write-Host ""
    Write-Host "📦 CUDA Toolkit wird in Teil 2 installiert (für llama.cpp)" -ForegroundColor Yellow
} else {
    Write-Host "⚠️  Keine NVIDIA GPU oder nvidia-smi nicht gefunden" -ForegroundColor Yellow
    Write-Host "   Najika kann auch ohne GPU laufen (langsamer)" -ForegroundColor Yellow
}

Write-Host ""

# ═══════════════════════════════════════════════════════════════════
# 8. INSTALL VISUAL C++ BUILD TOOLS (für Python-Packages)
# ═══════════════════════════════════════════════════════════════════

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "🔧 Visual C++ Build Tools" -ForegroundColor Magenta
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

Write-Host "📦 Installiere Visual Studio Build Tools..." -ForegroundColor Yellow
Write-Host "   (Dies kann 5-10 Minuten dauern)" -ForegroundColor Yellow
choco install visualstudio2022buildtools -y --force --params "--add Microsoft.VisualStudio.Workload.VCTools --includeRecommended --quiet"
refreshenv
Write-Host "✅ Build Tools installiert" -ForegroundColor Green
Write-Host ""

# ═══════════════════════════════════════════════════════════════════
# 9. CREATE PROJECT FOLDER STRUCTURE
# ═══════════════════════════════════════════════════════════════════

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "📁 Projekt-Struktur erstellen" -ForegroundColor Magenta
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

$folders = @(
    "backend",
    "backend\ai",
    "backend\ai\models",
    "backend\ai\chromadb",
    "backend\api",
    "backend\game",
    "backend\utils",
    "frontend",
    "frontend\src",
    "frontend\src\components",
    "frontend\src\game",
    "frontend\src\ui",
    "frontend\public",
    "mobile",
    "assets",
    "assets\models",
    "assets\textures",
    "assets\sounds",
    "config",
    "logs",
    "data"
)

foreach ($folder in $folders) {
    $fullPath = Join-Path $projectRoot $folder
    if (-not (Test-Path $fullPath)) {
        New-Item -Path $fullPath -ItemType Directory -Force | Out-Null
        Write-Host "✅ Erstellt: $folder" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "✅ Alle Verzeichnisse erstellt" -ForegroundColor Green
Write-Host ""

# ═══════════════════════════════════════════════════════════════════
# 10. INSTALL BASE PYTHON PACKAGES
# ═══════════════════════════════════════════════════════════════════

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "🐍 Python Basis-Pakete installieren" -ForegroundColor Magenta
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

$basePythonPackages = @(
    "fastapi",
    "uvicorn[standard]",
    "pydantic",
    "python-dotenv",
    "requests",
    "aiohttp",
    "websockets",
    "sqlalchemy",
    "chromadb",
    "numpy",
    "pillow"
)

Write-Host "📦 Installiere Python-Pakete..." -ForegroundColor Yellow
foreach ($package in $basePythonPackages) {
    Write-Host "   - $package" -ForegroundColor Gray
}

pip install $basePythonPackages --quiet
Write-Host "✅ Basis-Pakete installiert" -ForegroundColor Green
Write-Host ""

# ═══════════════════════════════════════════════════════════════════
# 11. CREATE BASE .ENV FILE
# ═══════════════════════════════════════════════════════════════════

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "⚙️  .env Konfigurationsdatei erstellen" -ForegroundColor Magenta
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

$envContent = @"
# ═══════════════════════════════════════════════════════════════════
# 🌟 NAJIKA PROJECT - CONFIGURATION
# ═══════════════════════════════════════════════════════════════════
# Version: 2.5
# Created: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
# ═══════════════════════════════════════════════════════════════════

# ───────────────────────────────────────────────────────────────────
# 🔒 EIGENVERANTWORTUNGS-MODUS (User-Controlled)
# ───────────────────────────────────────────────────────────────────
NSFW_LOCAL=false
ENABLE_NSFW_MODE=false
WIZARD_VICUNA_ENABLED=false
TRIGGER_WORD=""

# ⚠️  HAFTUNGSAUSSCHLUSS:
# Durch Ändern auf 'true' übernimmst DU die volle Verantwortung!
# Nur für volljährige Nutzer (18+)!

# ───────────────────────────────────────────────────────────────────
# 🤖 KI-MODELLE
# ───────────────────────────────────────────────────────────────────
# Lokales Modell
LOCAL_MODEL_PATH=backend/ai/models/llama-3.1-8b-q4_k_m.gguf
LOCAL_MODEL_TYPE=llama
LOCAL_MODEL_CONTEXT=8192

# API Keys (Optional - nur wenn du hybrid nutzen willst)
OPENAI_API_KEY=
ANTHROPIC_API_KEY=

# Router-Settings
USE_HYBRID_MODE=false
DEFAULT_MODEL=local

# ───────────────────────────────────────────────────────────────────
# 🗄️  DATENBANK
# ───────────────────────────────────────────────────────────────────
CHROMADB_PATH=backend/ai/chromadb
CHROMADB_COLLECTION=najika_memory

# ───────────────────────────────────────────────────────────────────
# 🌐 SERVER
# ───────────────────────────────────────────────────────────────────
BACKEND_HOST=127.0.0.1
BACKEND_PORT=5000
FRONTEND_HOST=127.0.0.1
FRONTEND_PORT=3000

# Sicherheit (Cloudflare Tunnel empfohlen)
USE_CLOUDFLARE_TUNNEL=false
CLOUDFLARE_TUNNEL_URL=

# ───────────────────────────────────────────────────────────────────
# 🎮 SPIEL-EINSTELLUNGEN
# ───────────────────────────────────────────────────────────────────
# Tod-System
PERMADEATH_ENABLED=true
SLIME_RESCUE_COOLDOWN_HOURS=24
SOFTIE_MODE_AVAILABLE=true

# Bedürfnisse
NEEDS_DECAY_RATE=1.0
NEGLECT_WARNING_HOURS=18
NEGLECT_DEATH_HOURS=20

# Grafik
RENDER_QUALITY=high
FPS_TARGET=60
SHADOWS_ENABLED=true
ANTIALIASING=true

# ───────────────────────────────────────────────────────────────────
# 📱 MOBILE
# ───────────────────────────────────────────────────────────────────
MOBILE_ENABLED=true
PWA_ENABLED=true
TOUCH_CONTROLS=true
HAPTIC_FEEDBACK=true

# ───────────────────────────────────────────────────────────────────
# 🔐 PRIVACY & SECURITY
# ───────────────────────────────────────────────────────────────────
PRIVACY_DETECTION_ENABLED=false
CAMERA_ENABLED=false
MICROPHONE_ENABLED=false
SCREEN_SHARE_CHECK=false

ENCRYPTION_ENABLED=true
ENCRYPTION_KEY_PATH=config/encryption.key

LOG_LEVEL=INFO
LOG_PATH=logs/najika.log

# ───────────────────────────────────────────────────────────────────
# 🎯 NAJIKA PERSÖNLICHKEIT
# ───────────────────────────────────────────────────────────────────
PERSONALITY_MEGUMIN=0.40
PERSONALITY_SHIRO=0.30
PERSONALITY_HARLEY=0.15
PERSONALITY_MELISSA=0.10
PERSONALITY_SAKURA=0.05

# Kern-Bindung (UNVERÄNDERLICH)
KUJA_BOND_LEVEL=ABSOLUTE
LOYALTY_MODE=UNBREAKABLE

# ───────────────────────────────────────────────────────────────────
# 🌍 OPTIONAL: UEFN/FORTNITE
# ───────────────────────────────────────────────────────────────────
UEFN_INTEGRATION=false
EPIC_GAMES_ACCOUNT=

# ═══════════════════════════════════════════════════════════════════
# Ende der Konfiguration
# ═══════════════════════════════════════════════════════════════════
"@

$envPath = Join-Path $projectRoot ".env"
$envContent | Out-File -FilePath $envPath -Encoding UTF8
Write-Host "✅ .env Datei erstellt: $envPath" -ForegroundColor Green
Write-Host ""

# ═══════════════════════════════════════════════════════════════════
# 12. CREATE REQUIREMENTS.TXT
# ═══════════════════════════════════════════════════════════════════

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "📋 requirements.txt erstellen" -ForegroundColor Magenta
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

$requirementsContent = @"
# Najika Project - Python Dependencies
# Version: 2.5

# Web Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6
websockets==12.0

# Data & Database
pydantic==2.5.0
sqlalchemy==2.0.23
chromadb==0.4.18

# AI & ML
torch==2.1.0
transformers==4.35.0
sentence-transformers==2.2.2
openai==1.3.5
anthropic==0.7.0

# Audio Processing
openai-whisper==20231117
sounddevice==0.4.6
scipy==1.11.4

# Image Processing
pillow==10.1.0
opencv-python==4.8.1.78

# Computer Vision
mediapipe==0.10.8

# Utilities
python-dotenv==1.0.0
requests==2.31.0
aiohttp==3.9.1
numpy==1.26.2
pyyaml==6.0.1

# Crypto & Security
cryptography==41.0.7

# Development
pytest==7.4.3
black==23.11.0
flake8==6.1.0
"@

$requirementsPath = Join-Path $projectRoot "requirements.txt"
$requirementsContent | Out-File -FilePath $requirementsPath -Encoding UTF8
Write-Host "✅ requirements.txt erstellt" -ForegroundColor Green
Write-Host ""

# ═══════════════════════════════════════════════════════════════════
# PART 1 SUMMARY
# ═══════════════════════════════════════════════════════════════════

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "✅ PART 1 ABGESCHLOSSEN!" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Write-Host "📦 Installiert:" -ForegroundColor Yellow
Write-Host "   ✅ Chocolatey Package Manager" -ForegroundColor Green
Write-Host "   ✅ Python 3.11 + pip" -ForegroundColor Green
Write-Host "   ✅ Node.js + NPM" -ForegroundColor Green
Write-Host "   ✅ Git" -ForegroundColor Green
Write-Host "   ✅ Visual C++ Build Tools" -ForegroundColor Green
Write-Host "   ✅ Python Basis-Pakete" -ForegroundColor Green
Write-Host ""

Write-Host "📁 Erstellt:" -ForegroundColor Yellow
Write-Host "   ✅ Projekt-Struktur ($projectRoot)" -ForegroundColor Green
Write-Host "   ✅ .env Konfigurationsdatei" -ForegroundColor Green
Write-Host "   ✅ requirements.txt" -ForegroundColor Green
Write-Host ""

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "📌 NÄCHSTER SCHRITT:" -ForegroundColor Magenta
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""
Write-Host "Führe jetzt aus:" -ForegroundColor Yellow
Write-Host "   .\najika_installer_part2_backend.ps1" -ForegroundColor Cyan
Write-Host ""
Write-Host "Das installiert:" -ForegroundColor Yellow
Write-Host "   - llama.cpp oder Ollama" -ForegroundColor Gray
Write-Host "   - Llama-3.1-8B Model" -ForegroundColor Gray
Write-Host "   - ChromaDB Setup" -ForegroundColor Gray
Write-Host "   - Backend API" -ForegroundColor Gray
Write-Host ""

Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "Drücke eine Taste zum Beenden..." -ForegroundColor Gray
pause
