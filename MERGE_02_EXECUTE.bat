@echo off
REM ========================================
REM NAJIKA MERGE - STEP 2: EXECUTE
REM Führt die Zusammenführung durch
REM AKTUALISIERT: 26.10.2025 - Mit Voice & LoRA System
REM ========================================

echo.
echo ========================================
echo    NAJIKA MERGE - AUSFUEHREN
echo ========================================
echo.

REM Prüfe ob Backup existiert
if not exist "C:\Najika_Backups" (
    echo FEHLER: Kein Backup gefunden!
    echo Bitte erst MERGE_01_BACKUP.bat ausfuehren!
    pause
    exit /b 1
)

echo WARNUNG: Dieser Vorgang veraendert die Ordnerstruktur!
echo.
echo Quelle: C:\NajikaCore
echo Ziel:   C:\Najika\backend
echo.
echo Backup existiert in: C:\Najika_Backups
echo.
set /p confirm="Fortfahren? (J/N): "
if /i not "%confirm%"=="J" (
    echo Abgebrochen.
    pause
    exit /b 0
)

echo.
echo ========================================
echo    MERGE STARTEN
echo ========================================
echo.

REM =======================================
REM TEIL 1: ORDNERSTRUKTUR ERSTELLEN
REM =======================================

echo [1/12] Erstelle Backend-Ordnerstruktur...
if not exist "C:\Najika\backend" mkdir "C:\Najika\backend"
if not exist "C:\Najika\backend\voice" mkdir "C:\Najika\backend\voice"
if not exist "C:\Najika\backend\training" mkdir "C:\Najika\backend\training"
if not exist "C:\Najika\backend\import" mkdir "C:\Najika\backend\import"
if not exist "C:\Najika\backend\scripts" mkdir "C:\Najika\backend\scripts"
echo OK - Ordnerstruktur erstellt

REM =======================================
REM TEIL 2: CORE BACKEND FILES
REM =======================================

echo.
echo [2/12] Kopiere Core Backend-Files...
copy "C:\NajikaCore\najika_server.py" "C:\Najika\backend\" /Y >nul
copy "C:\NajikaCore\najika_battle.py" "C:\Najika\backend\" /Y >nul
copy "C:\NajikaCore\najika_living_system.py" "C:\Najika\backend\" /Y >nul
copy "C:\NajikaCore\najika_enhanced_personality.py" "C:\Najika\backend\" /Y >nul
copy "C:\NajikaCore\najika_memory_enhanced.py" "C:\Najika\backend\" /Y >nul
copy "C:\NajikaCore\najika_search.py" "C:\Najika\backend\" /Y >nul
copy "C:\NajikaCore\najika_tor.py" "C:\Najika\backend\" /Y >nul
copy "C:\NajikaCore\najika_security.py" "C:\Najika\backend\" /Y >nul
copy "C:\NajikaCore\najika_claude_code.py" "C:\Najika\backend\" /Y >nul
copy "C:\NajikaCore\najika_human_like_trainer.py" "C:\Najika\backend\" /Y >nul
copy "C:\NajikaCore\najika_autonomous_search.py" "C:\Najika\backend\" /Y >nul
if %ERRORLEVEL% NEQ 0 (
    echo FEHLER beim Kopieren der Core-Files!
    goto :error
)
echo OK - Core Backend-Files kopiert

REM =======================================
REM TEIL 3: VOICE SYSTEM
REM =======================================

echo.
echo [3/12] Kopiere Voice System...
copy "C:\NajikaCore\najika_tts.py" "C:\Najika\backend\voice\" /Y >nul
copy "C:\NajikaCore\najika_tts_edge.py" "C:\Najika\backend\voice\" /Y >nul
copy "C:\NajikaCore\najika_voice_clone.py" "C:\Najika\backend\voice\" /Y >nul
copy "C:\NajikaCore\accept_tts_license.py" "C:\Najika\backend\voice\" /Y >nul
if %ERRORLEVEL% NEQ 0 (
    echo WARNUNG: Voice-System teilweise fehlgeschlagen (nicht kritisch)
) else (
    echo OK - Voice System kopiert
)

REM =======================================
REM TEIL 4: TRAINING SYSTEM
REM =======================================

echo.
echo [4/12] Kopiere Training System...
copy "C:\NajikaCore\najika_lora_training.py" "C:\Najika\backend\training\" /Y >nul
copy "C:\NajikaCore\najika_lora_training_3b.py" "C:\Najika\backend\training\" /Y >nul 2>nul
copy "C:\NajikaCore\najika_lora_server.py" "C:\Najika\backend\training\" /Y >nul
copy "C:\NajikaCore\deploy_lora_to_ollama.py" "C:\Najika\backend\training\" /Y >nul
copy "C:\NajikaCore\export_lora_gguf.py" "C:\Najika\backend\training\" /Y >nul
copy "C:\NajikaCore\resume_lora_training.py" "C:\Najika\backend\training\" /Y >nul
copy "C:\NajikaCore\NAJIKA_TRAINING_ULTIMATE_FAILSAFE.py" "C:\Najika\backend\training\" /Y >nul
if %ERRORLEVEL% NEQ 0 (
    echo WARNUNG: Training-System teilweise fehlgeschlagen (nicht kritisch)
) else (
    echo OK - Training System kopiert
)

REM =======================================
REM TEIL 5: IMPORT SYSTEM
REM =======================================

echo.
echo [5/12] Kopiere Import System...
copy "C:\NajikaCore\najika_session_importer.py" "C:\Najika\backend\import\" /Y >nul
copy "C:\NajikaCore\najika_external_data_importer.py" "C:\Najika\backend\import\" /Y >nul
copy "C:\NajikaCore\najika_comprehensive_import.py" "C:\Najika\backend\import\" /Y >nul
copy "C:\NajikaCore\najika_design_importer.py" "C:\Najika\backend\import\" /Y >nul
copy "C:\NajikaCore\najika_personality_importer.py" "C:\Najika\backend\import\" /Y >nul
copy "C:\NajikaCore\najika_filter_conflicts.py" "C:\Najika\backend\import\" /Y >nul
if %ERRORLEVEL% NEQ 0 (
    echo WARNUNG: Import-System teilweise fehlgeschlagen (nicht kritisch)
) else (
    echo OK - Import System kopiert
)

REM =======================================
REM TEIL 6: UTILITY SCRIPTS
REM =======================================

echo.
echo [6/12] Kopiere Utility Scripts...
copy "C:\NajikaCore\*.bat" "C:\Najika\backend\scripts\" /Y >nul 2>nul
copy "C:\NajikaCore\analyze_*.py" "C:\Najika\backend\scripts\" /Y >nul 2>nul
copy "C:\NajikaCore\check_*.py" "C:\Najika\backend\scripts\" /Y >nul 2>nul
echo OK - Scripts kopiert

REM =======================================
REM TEIL 7: DATENBANKEN & DATA
REM =======================================

echo.
echo [7/12] Kopiere Datenbanken...
if exist "C:\NajikaCore\chroma_db" (
    xcopy "C:\NajikaCore\chroma_db" "C:\Najika\backend\chroma_db\" /E /I /Y /Q >nul
    echo OK - ChromaDB kopiert
) else (
    echo INFO - Keine ChromaDB gefunden (wird neu erstellt)
)

if exist "C:\NajikaCore\voice_data" (
    xcopy "C:\NajikaCore\voice_data" "C:\Najika\backend\voice_data\" /E /I /Y /Q >nul
    echo OK - Voice Data kopiert
) else (
    echo INFO - Keine Voice Data gefunden
)

if exist "C:\NajikaCore\training_data" (
    xcopy "C:\NajikaCore\training_data" "C:\Najika\backend\training_data\" /E /I /Y /Q >nul
    echo OK - Training Data kopiert
) else (
    echo INFO - Keine Training Data gefunden
)

REM =======================================
REM TEIL 8: CONFIG FILES
REM =======================================

echo.
echo [8/12] Kopiere Config...
if exist "C:\NajikaCore\.env" (
    copy "C:\NajikaCore\.env" "C:\Najika\backend\.env" /Y >nul
    echo OK - .env kopiert
) else (
    echo WARNUNG - Keine .env gefunden!
)

if exist "C:\NajikaCore\config" (
    xcopy "C:\NajikaCore\config" "C:\Najika\backend\config\" /E /I /Y /Q >nul 2>nul
    echo OK - Config kopiert
)

REM =======================================
REM TEIL 9: DOKUMENTATION
REM =======================================

echo.
echo [9/12] Erstelle DOCS Struktur...
if not exist "C:\Najika\DOCS" mkdir "C:\Najika\DOCS"
if not exist "C:\Najika\DOCS\backend" mkdir "C:\Najika\DOCS\backend"
if not exist "C:\Najika\DOCS\backend\training" mkdir "C:\Najika\DOCS\backend\training"
if not exist "C:\Najika\DOCS\backend\voice" mkdir "C:\Najika\DOCS\backend\voice"
if not exist "C:\Najika\DOCS\backend\v4" mkdir "C:\Najika\DOCS\backend\v4"
if not exist "C:\Najika\DOCS\design" mkdir "C:\Najika\DOCS\design"
if not exist "C:\Najika\DOCS\frontend" mkdir "C:\Najika\DOCS\frontend"
echo OK - DOCS Struktur erstellt

echo.
echo [10/12] Kopiere Dokumentation...
REM Training Docs
copy "C:\NajikaCore\NAJIKA_LORA*.md" "C:\Najika\DOCS\backend\training\" /Y >nul 2>nul
copy "C:\NajikaCore\NAJIKA_TRAINING*.md" "C:\Najika\DOCS\backend\training\" /Y >nul 2>nul
copy "C:\NajikaCore\NAJIKA_CURRENT_TRAINING.md" "C:\Najika\DOCS\backend\training\" /Y >nul 2>nul
copy "C:\NajikaCore\NAJIKA_ULTIMATE_LEARNING_SYSTEM.md" "C:\Najika\DOCS\backend\training\" /Y >nul 2>nul
copy "C:\NajikaCore\NAJIKA_MAXIMUM_POWER_SETUP.md" "C:\Najika\DOCS\backend\training\" /Y >nul 2>nul

REM Voice Docs
copy "C:\NajikaCore\NAJIKA_VOICE*.md" "C:\Najika\DOCS\backend\voice\" /Y >nul 2>nul

REM V4 Docs
copy "C:\NajikaCore\NAJIKA_V4*.md" "C:\Najika\DOCS\backend\v4\" /Y >nul 2>nul
copy "C:\NajikaCore\NAJIKA_COMBAT_SYSTEM_DESIGN.md" "C:\Najika\DOCS\backend\v4\" /Y >nul 2>nul

REM Design Documents
if exist "C:\NajikaCore\design_documents" (
    xcopy "C:\NajikaCore\design_documents" "C:\Najika\DOCS\design\" /E /I /Y /Q >nul
)

REM Alle anderen Docs
copy "C:\NajikaCore\*.md" "C:\Najika\DOCS\backend\" /Y >nul 2>nul

REM Frontend Docs verschieben
move "C:\Najika\NAJIKA_ENHANCED_DIGIMON_COMBAT.md" "C:\Najika\DOCS\frontend\" >nul 2>nul
move "C:\Najika\COMBAT_MODES_VERGLEICH.md" "C:\Najika\DOCS\frontend\" >nul 2>nul
move "C:\Najika\ORIGINAL_VS_NEU_VERGLEICH.md" "C:\Najika\DOCS\frontend\" >nul 2>nul

echo OK - Dokumentation kopiert

REM =======================================
REM TEIL 11: NEUER LAUNCHER
REM =======================================

echo.
echo [11/12] Erstelle neuen Launcher...
(
echo @echo off
echo REM ========================================
echo REM NAJIKA UNIFIED LAUNCHER
echo REM Startet Backend + Frontend
echo REM ========================================
echo.
echo echo ========================================
echo echo    NAJIKA - STARTING...
echo echo ========================================
echo.
echo REM Backend starten
echo echo [1/2] Starting Backend...
echo echo - Najika Server (Port 8000^)
echo echo - Voice System (Edge-TTS^)
echo echo - Battle System
echo echo.
echo cd backend
echo start /B python najika_server.py
echo cd ..
echo.
echo REM Warte 5 Sekunden
echo timeout /t 5 /nobreak ^>nul
echo.
echo REM Frontend starten
echo echo [2/2] Starting Frontend...
echo echo - React App (Port 3002^)
echo echo - Game UI
echo echo.
echo cd frontend
echo start /B npm start
echo cd ..
echo.
echo echo ========================================
echo echo    NAJIKA IS RUNNING!
echo echo ========================================
echo echo.
echo echo Frontend:  http://localhost:3002
echo echo Backend:   http://localhost:8000
echo echo.
echo echo Features:
echo echo - Command System (Digimon World Style^)
echo echo - Voice System (Edge-TTS, 4 Persoenlichkeiten^)
echo echo - Battle System mit Backend-Connection
echo echo - Finisher QTE (Button-Mashing^)
echo echo - LoRA Training (8B Adapter archiviert^)
echo echo.
echo echo Druecke STRG+C zum Beenden
echo pause
) > "C:\Najika\START_NAJIKA.bat"
echo OK - Launcher erstellt

REM =======================================
REM TEIL 12: README
REM =======================================

echo.
echo [12/12] Erstelle README.md...
(
echo # 🎮 Najika - Virtual Companion Game
echo.
echo **Enhanced Digimon World Style Combat + Voice AI + LoRA Training**
echo.
echo ---
echo.
echo ## 🚀 Quick Start
echo.
echo ```batch
echo START_NAJIKA.bat
echo ```
echo.
echo **URLs:**
echo - Frontend: http://localhost:3002
echo - Backend:  http://localhost:8000
echo.
echo ---
echo.
echo ## 📂 Project Structure
echo.
echo ```
echo C:\Najika\
echo ├── backend\               # Python Backend
echo │   ├── najika_server.py   # Main Server
echo │   ├── najika_battle.py   # Battle System
echo │   ├── voice\             # Voice/TTS System
echo │   ├── training\          # LoRA Training
echo │   ├── import\            # Data Import
echo │   └── scripts\           # Utility Scripts
echo ├── frontend\              # React Frontend
echo │   └── src\game\          # Game Logic
echo └── DOCS\                  # Documentation
echo ```
echo.
echo ---
echo.
echo ## ✨ Features
echo.
echo ### 🎮 Game System
echo - **Command System** - Digimon World 1 inspired
echo - **Evolution** - Rookie → Champion → Ultimate → Mega
echo - **4 Combat Commands** - Attack/Defend/Tech/Distance
echo - **Praise/Scold** - Relationship mechanics
echo - **Finisher QTE** - Button-mashing mini-game
echo - **3 Camera Modes** - Orbit/Third/First Person
echo.
echo ### 🔊 Voice System
echo - **Edge-TTS** - Text-to-Speech
echo - **4 Persönlichkeiten** - Megumin, Harley, Shiro, Melissa
echo - **Voice Cloning** - Custom voice training
echo.
echo ### 🤖 AI System
echo - **Ollama** - Local AI (najika-local^)
echo - **LoRA Adapter** - 8B, 586 Konversationen trainiert
echo - **ChromaDB** - Vector memory storage
echo - **Claude Code** - Optional cloud AI
echo.
echo ### ⚔️ Battle System
echo - **Backend-Connection** - Python API
echo - **Turn-based Combat** - Enemies, Skills, Items
echo - **Battle XP** - Drives evolution system
echo - **Timing System** - Perfect/Good/Bad timing
echo.
echo ---
echo.
echo ## 🎯 Controls
echo.
echo ### Orbit Cam (Tamer Mode^):
echo - **[1-4]** - Commands (Attack/Defend/Tech/Distance^)
echo - **[SPACE]** - Praise
echo - **[CTRL]** - Scold
echo - **[TAB]** - Override Toggle
echo - **[F]** - Finisher
echo - **[C]** - Camera Switch
echo.
echo ### Third/First Person (Action Mode^):
echo - **WASD** - Movement
echo - **Mouse** - Camera
echo - **LMB** - Light Attack
echo - **RMB** - Heavy Attack
echo - **SPACE** - Dodge
echo - **[C]** - Camera Switch
echo.
echo ---
echo.
echo ## 📊 Tech Stack
echo.
echo **Backend:**
echo - Python 3.11+
echo - Ollama (Local AI^)
echo - ChromaDB (Vector DB^)
echo - Edge-TTS (Voice^)
echo - Unsloth (LoRA Training^)
echo.
echo **Frontend:**
echo - React 18.2
echo - Three.js 0.168
echo - React Three Fiber 8.17
echo - React Three Drei 9.114
echo.
echo ---
echo.
echo ## 📖 Documentation
echo.
echo See `DOCS\` folder for detailed documentation:
echo - **frontend\** - Combat system, camera modes
echo - **backend\** - API, systems, configs
echo - **backend\training\** - LoRA training guides
echo - **backend\voice\** - Voice system setup
echo - **design\** - Design documents
echo.
echo ---
echo.
echo ## 🔧 Development
echo.
echo **Backend only:**
echo ```bash
echo cd backend
echo python najika_server.py
echo ```
echo.
echo **Frontend only:**
echo ```bash
echo cd frontend
echo npm start
echo ```
echo.
echo ---
echo.
echo ## 📝 Status
echo.
echo **✅ Implemented:**
echo - Command System (100%%^)
echo - Voice System (Edge-TTS^)
echo - Battle API Connection (100%%^)
echo - Finisher QTE (100%%^)
echo - LoRA Training (8B ready^)
echo - 3 Camera Modes (100%%^)
echo.
echo **⚠️ In Progress:**
echo - Enemy 3D Models
echo - Advanced Finisher (Timing Circles^)
echo - Evolution Animations
echo.
echo ---
echo.
echo **Last Updated:** 2025-10-26
echo **Version:** 1.0 (Unified^)
) > "C:\Najika\README.md"
echo OK - README erstellt

REM =======================================
REM FERTIG!
REM =======================================

echo.
echo ========================================
echo    MERGE ERFOLGREICH!
echo ========================================
echo.
echo Neue Struktur:
echo.
echo C:\Najika\
echo   ├── backend\         (VON NAJIKACORE)
echo   │   ├── voice\       (Voice System)
echo   │   ├── training\    (LoRA Training)
echo   │   ├── import\      (Import System)
echo   │   └── scripts\     (Utilities)
echo   ├── frontend\        (BLEIBT)
echo   ├── DOCS\            (Dokumentation sortiert)
echo   ├── START_NAJIKA.bat (NEUER Launcher)
echo   └── README.md        (NEU)
echo.
echo WICHTIG:
echo - C:\NajikaCore\ wurde NICHT geloescht
echo - Backup: C:\Najika_Backups\
echo.
echo Weiter mit MERGE_03_TEST.bat zum Testen!
echo.
pause
goto :eof

:error
echo.
echo ========================================
echo    FEHLER BEIM MERGE!
echo ========================================
echo.
echo Restore aus Backup:
echo 1. Gehe zu C:\Najika_Backups\
echo 2. Kopiere neuestes Backup zurueck
echo.
pause
exit /b 1
