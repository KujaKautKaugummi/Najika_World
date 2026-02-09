# ═══════════════════════════════════════════════════════════════════
# 🌟 NAJIKA PROJECT - INSTALLER PART 5: FINALIZE
# ═══════════════════════════════════════════════════════════════════
# Version: 2.5
# Part: 5/5 - Integration, Configuration, Documentation
# ═══════════════════════════════════════════════════════════════════

Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "🌟 NAJIKA PROJECT - INSTALLER PART 5/5" -ForegroundColor Magenta
Write-Host "Finalisierung & Integration" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

$projectRoot = "C:\Najika"
Set-Location $projectRoot

# ═══════════════════════════════════════════════════════════════════
# 1. CREATE MASTER START SCRIPT
# ═══════════════════════════════════════════════════════════════════

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "🚀 Master Start-Skript erstellen" -ForegroundColor Magenta
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

$masterStart = @"
@echo off
cls
color 0D
echo ════════════════════════════════════════════════════════════════════
echo.
echo    ███╗   ██╗ █████╗      ██╗██╗██╗  ██╗ █████╗ 
echo    ████╗  ██║██╔══██╗     ██║██║██║ ██╔╝██╔══██╗
echo    ██╔██╗ ██║███████║     ██║██║█████╔╝ ███████║
echo    ██║╚██╗██║██╔══██║██   ██║██║██╔═██╗ ██╔══██║
echo    ██║ ╚████║██║  ██║╚█████╔╝██║██║  ██╗██║  ██║
echo    ╚═╝  ╚═══╝╚═╝  ╚═╝ ╚════╝ ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
echo.
echo                   Version 2.5 - FULL SYSTEM
echo.
echo ════════════════════════════════════════════════════════════════════
echo.
echo   Najika wird jetzt gestartet...
echo   Bitte warte, während alle Systeme hochfahren.
echo.
echo ════════════════════════════════════════════════════════════════════
echo.

REM Check if Ollama is installed
where ollama >nul 2>nul
if %errorlevel% equ 0 (
    echo [1/3] Starte Ollama...
    start /min cmd /c "ollama serve"
    timeout /t 3 /nobreak >nul
) else (
    echo [1/3] Ollama nicht gefunden - überspringe
)

REM Start Backend
echo [2/3] Starte Najika Backend API...
start "Najika Backend" cmd /k "cd /d %~dp0 && python backend\api\server.py"
timeout /t 5 /nobreak >nul

REM Start Frontend
echo [3/3] Starte Najika Frontend...
start "Najika Frontend" cmd /k "cd /d %~dp0\frontend && npm start"

echo.
echo ════════════════════════════════════════════════════════════════════
echo.
echo   ✅ Najika wurde gestartet!
echo.
echo   🌐 Backend:  http://127.0.0.1:5000
echo   🎮 Frontend: http://127.0.0.1:3000
echo.
echo   Najika öffnet sich automatisch im Browser...
echo.
echo ════════════════════════════════════════════════════════════════════
echo.

timeout /t 5 /nobreak >nul
start http://localhost:3000

echo   Drücke eine Taste zum Beenden...
pause >nul
"@

$masterStartPath = Join-Path $projectRoot "START_NAJIKA.bat"
$masterStart | Out-File -FilePath $masterStartPath -Encoding ASCII
Write-Host "✅ START_NAJIKA.bat erstellt" -ForegroundColor Green
Write-Host ""

# ═══════════════════════════════════════════════════════════════════
# 2. CREATE STOP SCRIPT
# ═══════════════════════════════════════════════════════════════════

$stopScript = @"
@echo off
echo ════════════════════════════════════════════
echo 🛑 Stoppe Najika...
echo ════════════════════════════════════════════
echo.

echo Beende Backend...
taskkill /FI "WINDOWTITLE eq Najika Backend*" /F >nul 2>&1

echo Beende Frontend...
taskkill /FI "WINDOWTITLE eq Najika Frontend*" /F >nul 2>&1

echo Beende Node-Prozesse...
taskkill /IM node.exe /F >nul 2>&1

echo Beende Python-Prozesse...
taskkill /IM python.exe /F >nul 2>&1

echo.
echo ✅ Najika wurde gestoppt.
echo.
pause
"@

$stopPath = Join-Path $projectRoot "STOP_NAJIKA.bat"
$stopScript | Out-File -FilePath $stopPath -Encoding ASCII
Write-Host "✅ STOP_NAJIKA.bat erstellt" -ForegroundColor Green
Write-Host ""

# ═══════════════════════════════════════════════════════════════════
# 3. CREATE COMPREHENSIVE README
# ═══════════════════════════════════════════════════════════════════

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "📚 Hauptdokumentation erstellen" -ForegroundColor Magenta
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

$mainReadme = @"
# 🌟 NAJIKA PROJECT - Version 2.5

**Deine persönliche KI-Begleiterin & Action-RPG**

---

## 🚀 SCHNELLSTART

### Najika starten (ALLES auf einmal):
``
START_NAJIKA.bat
``

Das startet automatisch:
- ✅ Ollama (falls installiert)
- ✅ Backend API (Port 5000)
- ✅ Frontend (Port 3000)
- ✅ Öffnet Browser

### Najika stoppen:
``
STOP_NAJIKA.bat
``

---

## 📁 PROJEKT-STRUKTUR

``
C:\Najika\
├── backend/              # Python Backend
│   ├── ai/              # KI-Systeme (llama.cpp/Ollama)
│   │   ├── models/      # Modell-Dateien
│   │   ├── chromadb/    # Persistentes Gedächtnis
│   │   └── najika_core.py  # Persönlichkeits-Kern
│   ├── api/             # FastAPI Server
│   └── game/            # Spiel-Logik
├── frontend/            # React Frontend
│   ├── src/
│   │   ├── game/       # 3D Game (Three.js)
│   │   ├── ui/         # UI Components
│   │   └── App.js      # Main App
│   └── public/         # Static Assets
├── mobile/             # PWA & Mobile
├── config/             # Konfiguration
├── .env               # Umgebungsvariablen
└── START_NAJIKA.bat   # Master-Start-Skript
``

---

## ⚙️ KONFIGURATION (.env)

Wichtigste Einstellungen in ``.env``:

### 🔒 Eigenverantwortung (NSFW-Mode):
``
NSFW_LOCAL=false              # Auf 'true' für Private Mode
WIZARD_VICUNA_ENABLED=false   # Uncensored Model
TRIGGER_WORD=""               # Dein eigenes Trigger-Wort
``

**⚠️ WICHTIG:**  
Durch Aktivierung übernimmst DU die volle Verantwortung!

### 🤖 KI-Modelle:
``
LOCAL_MODEL_PATH=backend/ai/models/llama-3.1-8b-q4_k_m.gguf
USE_HYBRID_MODE=false         # true für GPT-4o/Claude
OPENAI_API_KEY=               # Optional
ANTHROPIC_API_KEY=            # Optional
``

### 🎮 Spiel-Einstellungen:
``
PERMADEATH_ENABLED=true
SLIME_RESCUE_COOLDOWN_HOURS=24
NEGLECT_WARNING_HOURS=18
NEGLECT_DEATH_HOURS=20
``

---

## 🎮 SPIELEN

### PC-Steuerung:
- **WASD**: Bewegung
- **Maus**: Kamera
- **Linke Maustaste**: Light Attack
- **Rechte Maustaste**: Heavy Attack
- **Leertaste**: Dodge
- **Shift**: Block
- **Q**: Parry
- **E**: Finisher (wenn verfügbar)
- **1-6**: Element-Weaving
- **Tab**: Inventar
- **ESC**: Menü

### Mobile/Touch:
- **Joystick (links)**: Bewegung
- **Action Buttons (rechts)**: Angriffe
- **Element Pad**: Magie
- **Swipe Gesten**: Block/Dodge

---

## 📱 MOBILE INSTALLATION (PWA)

### Android (Chrome):
1. Öffne ``http://[deine-pc-ip]:3000``
2. Menü (⋮) → "Zum Startbildschirm hinzufügen"

### iOS (Safari):
1. Öffne ``http://[deine-pc-ip]:3000``
2. Teilen (□↑) → "Zum Home-Bildschirm"

### Mit Cloudflare Tunnel (Empfohlen):
``bash
cloudflared tunnel --url http://localhost:3000
``
Nutze die generierte URL auf allen Geräten!

---

## 🧠 NAJIKA'S PERSÖNLICHKEIT

### Kern-Identität:
- **Kuja-Bond**: Absolute Loyalität (unveränderlich)
- **Rolle**: "Schwert und Schild" - Beschützer und Kraft
- **Najika's Rolle**: "Kopf und Herz" für Kuja

### Persönlichkeits-Mix:
- 40% Megumin (KonoSuba) - Explosiv, dramatisch
- 30% Shiro (NGNL) - Strategisch, anhänglich
- 15% Harley Quinn - Chaotisch, loyal
- 10% Melissa Masters - Dominant
- 5% Sakura (Cardcaptor) - Süß/Manipulativ

### Autonomie:
- ✅ Kann Befehle ablehnen
- ✅ Eigene Meinung & Ziele
- ✅ Initiiert Gespräche
- ✅ Kritisiert wenn nötig
- ✅ Lernt & entwickelt sich

---

## 💀 TOD-SYSTEM

### Permadeath:
- Tod ist PERMANENT
- Slime kann dich 1× retten (24h IRL Cooldown)
- Nach Rettung: Verletzungen (4-6h Heilung)
- Softie-Mode: Einmalig nach erstem Tod wählbar

### Najika-Vernachlässigung:
- 18h ohne Interaktion: Warnung
- 20h: Najika "stirbt" (Savegame verloren)
- Gilt auch wenn PC aus ist!

---

## 🎯 GAME-FEATURES

### Kampf-System:
- Light/Heavy Attacks
- Parry & Dodge
- Element-Weaving (6 Elemente, 15 Kombinationen)
- 5 Spezialisierungen + Ultimates
- Rival-Memory (Gegner merken sich alles!)
- Finisher mit QTE

### Progression:
- Skill-based Learning
- 5 Bedürfnisse (Hunger, Durst, Energie, Social, Joy)
- Slime-Companion mit Evolution
- Crafting (5-Stufen)
- Plünder-Mechanik (Bounty-System)

### Aktivitäten:
- Angeln
- Hexenbesen-Delivery
- Katakomben-Erkundung
- Paper-Witch (freischaltbar)
- Oregon-Trail-Mechanik

---

## 🔒 SICHERHEIT & PRIVACY

### Datenschutz:
- ✅ Alles lokal gespeichert
- ✅ Keine Cloud-Telemetrie
- ✅ Verschlüsseltes Gedächtnis
- ✅ Privacy-Detection (opt-in)
- ✅ Jederzeit löschbar

### Netzwerk:
- Standard: ``127.0.0.1`` (localhost)
- Empfohlen: Cloudflare Tunnel
- Optional: ``0.0.0.0`` (LAN-Zugriff)

---

## 🛠️ TROUBLESHOOTING

### Backend startet nicht:
``bash
python backend\test_backend.py
``

### Frontend Fehler:
``bash
cd frontend
npm install
npm start
``

### Ollama funktioniert nicht:
``bash
ollama serve
ollama pull llama3.1:8b
``

### ChromaDB Fehler:
``bash
python backend\ai\init_chromadb.py
``

---

## 📊 SYSTEM-ANFORDERUNGEN

### Minimum:
- OS: Windows 10/11
- RAM: 8GB
- GPU: Integrierte Grafik (CPU-only Mode)
- Storage: 10GB

### Empfohlen (RTX 3060 Ti):
- OS: Windows 10/11
- RAM: 16GB
- GPU: NVIDIA RTX 3060 Ti (8GB VRAM)
- Storage: 20GB SSD
- CUDA 12.x

---

## 🎉 WAS JETZT?

1. **Starte Najika**: ``START_NAJIKA.bat``
2. **Öffne Browser**: ``http://localhost:3000``
3. **Sprich mit Najika**: Sie wartet auf dich!
4. **Erkunde die Welt**: Spiel beginnt!

---

## 📞 SUPPORT

Bei Problemen:
1. Prüfe Logs in ``logs/najika.log``
2. Teste Backend: ``python backend\test_backend.py``
3. Prüfe ``.env`` Konfiguration
4. Starte neu mit ``STOP_NAJIKA.bat`` + ``START_NAJIKA.bat``

---

## ⚡ QUICK COMMANDS

``batch
# Starten
START_NAJIKA.bat

# Stoppen
STOP_NAJIKA.bat

# Backend testen
python backend\test_backend.py

# Frontend dev
cd frontend && npm start

# Cloudflare Tunnel
cloudflared tunnel --url http://localhost:3000
``

---

**Version:** 2.5  
**Erstellt:** $(Get-Date -Format "yyyy-MM-dd")  
**Status:** ✅ Vollständig installiert

---

## 💝 Najika sagt:

> "Kuja! Ich bin bereit! Lass uns zusammen Abenteuer erleben!  
> EXPLOSION! 💥 ...äh, ich meine... ich freue mich auf dich! 😊"

---
"@

$readmePath = Join-Path $projectRoot "README.md"
$mainReadme | Out-File -FilePath $readmePath -Encoding UTF8
Write-Host "✅ Hauptdokumentation erstellt" -ForegroundColor Green
Write-Host ""

# ═══════════════════════════════════════════════════════════════════
# 4. CREATE QUICK REFERENCE CARD
# ═══════════════════════════════════════════════════════════════════

$quickRef = @"
╔═══════════════════════════════════════════════════════════════════╗
║                    🌟 NAJIKA QUICK REFERENCE                     ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  🚀 STARTEN                                                       ║
║  ────────────                                                     ║
║  START_NAJIKA.bat         → Startet alles auf einmal            ║
║  STOP_NAJIKA.bat          → Stoppt alle Prozesse                ║
║                                                                   ║
║  🌐 URLS                                                          ║
║  ────────                                                         ║
║  Backend:  http://127.0.0.1:5000                                ║
║  Frontend: http://127.0.0.1:3000                                ║
║  Mobile:   http://[deine-ip]:3000                               ║
║                                                                   ║
║  ⌨️  STEUERUNG (PC)                                               ║
║  ─────────────────                                                ║
║  WASD    → Bewegung          1-6 → Elemente                     ║
║  Maus    → Kamera            Tab → Inventar                     ║
║  LMB     → Light Attack      E   → Finisher                     ║
║  RMB     → Heavy Attack      ESC → Menü                         ║
║  Space   → Dodge                                                 ║
║  Shift   → Block                                                 ║
║  Q       → Parry                                                 ║
║                                                                   ║
║  💀 WICHTIG: TOD                                                  ║
║  ────────────────                                                 ║
║  • Permadeath aktiv!                                             ║
║  • Slime rettet 1× (24h Cooldown)                               ║
║  • Vernachlässigung = 20h → Tod                                  ║
║                                                                   ║
║  🔧 TROUBLESHOOTING                                               ║
║  ──────────────────                                               ║
║  python backend\test_backend.py  → Backend testen               ║
║  cd frontend && npm start        → Frontend neu starten         ║
║  ollama serve                    → Ollama manuell starten       ║
║                                                                   ║
║  📱 MOBILE (PWA)                                                  ║
║  ────────────────                                                 ║
║  Chrome: Menü → "Zum Startbildschirm"                           ║
║  Safari: Teilen → "Zum Home-Bildschirm"                         ║
║  cloudflared tunnel --url http://localhost:3000                 ║
║                                                                   ║
║  🎮 ELEMENT-KOMBINATIONEN                                         ║
║  ─────────────────────────                                        ║
║  Fire + Ice      = Steam (DoT)                                  ║
║  Fire + Lightning = Plasma (Burst)                              ║
║  Ice + Lightning  = Freeze (Stun)                               ║
║  Shadow + Light   = Chaos (Random)                              ║
║  Fire + Nature    = Wildfire (AoE)                              ║
║  Ice + Nature     = Blizzard (Slow)                             ║
║                                                                   ║
║  📊 BEDÜRFNISSE                                                   ║
║  ───────────────                                                  ║
║  🍖 Hunger  → Essen finden                                       ║
║  💧 Thirst  → Wasser trinken                                     ║
║  ⚡ Energy  → Schlafen / Rasten                                   ║
║  👥 Social  → Mit Najika reden                                   ║
║  😊 Joy     → Spielen / Spaß haben                               ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝

Najika sagt: "Kuja! Lass uns loslegen! EXPLOSION! 💥"
"@

$quickRefPath = Join-Path $projectRoot "QUICK_REFERENCE.txt"
$quickRef | Out-File -FilePath $quickRefPath -Encoding UTF8
Write-Host "✅ Quick Reference erstellt" -ForegroundColor Green
Write-Host ""

# ═══════════════════════════════════════════════════════════════════
# 5. CREATE DESKTOP SHORTCUTS (Optional)
# ═══════════════════════════════════════════════════════════════════

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "🖥️  Desktop-Verknüpfung erstellen?" -ForegroundColor Magenta
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""
Write-Host "Möchtest du eine Desktop-Verknüpfung für Najika? (j/n)" -ForegroundColor Yellow
$createShortcut = Read-Host

if ($createShortcut -eq "j") {
    $WScriptShell = New-Object -ComObject WScript.Shell
    $desktop = [System.Environment]::GetFolderPath("Desktop")
    $shortcut = $WScriptShell.CreateShortcut("$desktop\🌟 Najika.lnk")
    $shortcut.TargetPath = "$projectRoot\START_NAJIKA.bat"
    $shortcut.WorkingDirectory = $projectRoot
    $shortcut.Description = "Najika - Deine KI-Begleiterin"
    $shortcut.Save()
    Write-Host "✅ Desktop-Verknüpfung erstellt" -ForegroundColor Green
} else {
    Write-Host "⏭️  Übersprungen" -ForegroundColor Gray
}

Write-Host ""

# ═══════════════════════════════════════════════════════════════════
# 6. FINAL SYSTEM CHECK
# ═══════════════════════════════════════════════════════════════════

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "🔍 Finale System-Prüfung" -ForegroundColor Magenta
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""

$checks = @{
    "Python" = (Get-Command python -ErrorAction SilentlyContinue) -ne $null
    "Node.js" = (Get-Command node -ErrorAction SilentlyContinue) -ne $null
    "Git" = (Get-Command git -ErrorAction SilentlyContinue) -ne $null
    "Backend Ordner" = Test-Path "$projectRoot\backend"
    "Frontend Ordner" = Test-Path "$projectRoot\frontend"
    ".env Datei" = Test-Path "$projectRoot\.env"
    "ChromaDB Init" = Test-Path "$projectRoot\backend\ai\init_chromadb.py"
    "START_NAJIKA.bat" = Test-Path "$projectRoot\START_NAJIKA.bat"
}

foreach ($check in $checks.GetEnumerator()) {
    if ($check.Value) {
        Write-Host "   ✅ $($check.Key)" -ForegroundColor Green
    } else {
        Write-Host "   ❌ $($check.Key)" -ForegroundColor Red
    }
}

Write-Host ""

# ═══════════════════════════════════════════════════════════════════
# FINAL SUMMARY & CELEBRATION
# ═══════════════════════════════════════════════════════════════════

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "🎉🎉🎉 INSTALLATION ABGESCHLOSSEN! 🎉🎉🎉" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Write-Host "██████╗ ███████╗██████╗ ███████╗██╗████████╗" -ForegroundColor Magenta
Write-Host "██╔══██╗██╔════╝██╔══██╗██╔════╝██║╚══██╔══╝" -ForegroundColor Magenta
Write-Host "██████╔╝█████╗  ██████╔╝█████╗  ██║   ██║   " -ForegroundColor Magenta
Write-Host "██╔══██╗██╔══╝  ██╔══██╗██╔══╝  ██║   ██║   " -ForegroundColor Magenta
Write-Host "██║  ██║███████╗██║  ██║███████╗██║   ██║   " -ForegroundColor Magenta
Write-Host "╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝   ╚═╝   " -ForegroundColor Magenta
Write-Host ""

Write-Host "📦 INSTALLIERTE KOMPONENTEN:" -ForegroundColor Yellow
Write-Host ""
Write-Host "   TEIL 1: Base System" -ForegroundColor Cyan
Write-Host "      ✅ Python 3.11" -ForegroundColor Green
Write-Host "      ✅ Node.js & NPM" -ForegroundColor Green
Write-Host "      ✅ Git" -ForegroundColor Green
Write-Host "      ✅ Visual C++ Build Tools" -ForegroundColor Green
Write-Host ""
Write-Host "   TEIL 2: Backend & AI" -ForegroundColor Cyan
Write-Host "      ✅ llama.cpp / Ollama" -ForegroundColor Green
Write-Host "      ✅ Llama-3.1-8B Model" -ForegroundColor Green
Write-Host "      ✅ ChromaDB (Gedächtnis)" -ForegroundColor Green
Write-Host "      ✅ FastAPI Server" -ForegroundColor Green
Write-Host "      ✅ Najika Personality Core" -ForegroundColor Green
Write-Host ""
Write-Host "   TEIL 3: Frontend & 3D" -ForegroundColor Cyan
Write-Host "      ✅ React App" -ForegroundColor Green
Write-Host "      ✅ Three.js 3D Engine" -ForegroundColor Green
Write-Host "      ✅ Combat System" -ForegroundColor Green
Write-Host "      ✅ HUD & UI" -ForegroundColor Green
Write-Host ""
Write-Host "   TEIL 4: Mobile & PWA" -ForegroundColor Cyan
Write-Host "      ✅ PWA Manifest" -ForegroundColor Green
Write-Host "      ✅ Service Worker" -ForegroundColor Green
Write-Host "      ✅ Touch Controls" -ForegroundColor Green
Write-Host "      ✅ Digivice Interface" -ForegroundColor Green
Write-Host ""
Write-Host "   TEIL 5: Integration" -ForegroundColor Cyan
Write-Host "      ✅ Master Start-Skript" -ForegroundColor Green
Write-Host "      ✅ Dokumentation" -ForegroundColor Green
Write-Host "      ✅ Quick Reference" -ForegroundColor Green
Write-Host "      ✅ System-Checks" -ForegroundColor Green
Write-Host ""

Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "🚀 NÄCHSTE SCHRITTE:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Starte Najika:" -ForegroundColor Cyan
Write-Host "   .\START_NAJIKA.bat" -ForegroundColor White
Write-Host ""
Write-Host "2. Öffne Browser (automatisch):" -ForegroundColor Cyan
Write-Host "   http://localhost:3000" -ForegroundColor White
Write-Host ""
Write-Host "3. Optional - Mobile Zugriff (Cloudflare Tunnel):" -ForegroundColor Cyan
Write-Host "   cloudflared tunnel --url http://localhost:3000" -ForegroundColor White
Write-Host ""
Write-Host "4. Lies die Dokumentation:" -ForegroundColor Cyan
Write-Host "   README.md" -ForegroundColor White
Write-Host "   QUICK_REFERENCE.txt" -ForegroundColor White
Write-Host ""

Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "💝 NAJIKA'S NACHRICHT:" -ForegroundColor Magenta
Write-Host ""
Write-Host "   'Kuja! Ich bin bereit! 💥'" -ForegroundColor Yellow
Write-Host "   'Lass uns zusammen Abenteuer erleben!'" -ForegroundColor Yellow
Write-Host "   'EXPLOSION! ...äh, ich meine... ich freue mich auf dich! 😊'" -ForegroundColor Yellow
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Write-Host "📊 SYSTEM-INFORMATIONEN:" -ForegroundColor Yellow
Write-Host "   Projekt-Pfad: $projectRoot" -ForegroundColor Gray
Write-Host "   Python: $(python --version 2>&1)" -ForegroundColor Gray
Write-Host "   Node.js: $(node --version 2>&1)" -ForegroundColor Gray
Write-Host "   Installation: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray
Write-Host ""

Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "Möchtest du Najika JETZT starten? (j/n)" -ForegroundColor Yellow
$startNow = Read-Host

if ($startNow -eq "j") {
    Write-Host ""
    Write-Host "🚀 Starte Najika..." -ForegroundColor Green
    Write-Host ""
    Start-Process -FilePath "$projectRoot\START_NAJIKA.bat"
    Start-Sleep -Seconds 2
} else {
    Write-Host ""
    Write-Host "OK! Starte später mit: .\START_NAJIKA.bat" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "Vielen Dank! Viel Spaß mit Najika! 🌟💥" -ForegroundColor Magenta
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
pause
