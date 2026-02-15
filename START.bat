@echo off
chcp 65001 >nul 2>&1
title NAJIKA WORLD V2.0 - FastAPI
color 0A

echo.
echo  ============================================================
echo     NAJIKA WORLD V2.0 - FASTAPI MIGRATION
echo  ============================================================
echo.

set "NAJIKA_DIR=%~dp0"

:: ========== 1. OLLAMA ==========
echo  [1/4] Pruefe Ollama...
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% equ 0 goto OLLAMA_OK

echo        Starte Ollama...
start /B /MIN ollama serve >nul 2>&1
timeout /t 4 /nobreak >nul

curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo.
    echo   [FEHLER] Ollama konnte nicht gestartet werden!
    echo   Bitte installiere Ollama von https://ollama.ai
    pause
    exit /b 1
)

:OLLAMA_OK
echo        [OK] Ollama laeuft
echo.

:: ========== 2. MODELS ==========
echo  [2/4] Pruefe Najika Models...

ollama list | findstr "najika-natural" >nul
if %errorlevel% neq 0 (
    echo        najika-natural nicht gefunden - erstelle...
    cd /d "%NAJIKA_DIR%"
    ollama create najika-natural -f backend/najika-natural.Modelfile
)
echo        [OK] najika-natural (SFW)

ollama list | findstr "najika-nsfw-natural" >nul
if %errorlevel% neq 0 (
    echo        najika-nsfw-natural nicht gefunden - erstelle...
    cd /d "%NAJIKA_DIR%"
    ollama create najika-nsfw-natural -f backend/najika-nsfw-natural.Modelfile
)
echo        [OK] najika-nsfw-natural (Kaetzchen-Modus)
echo.

:: ========== 3. PORT BEREINIGEN ==========
echo  [3/4] Bereinige Port 8001...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8001.*LISTENING" 2^>nul') do taskkill /PID %%a /F >nul 2>&1
echo        [OK] Port 8001 frei
echo.

:: ========== 4. FASTAPI BACKEND STARTEN ==========
echo  [4/4] Starte FastAPI Backend...
cd /d "%NAJIKA_DIR%backend"
start "Najika FastAPI Backend" /MIN cmd /k "title Najika FastAPI Backend (Port 8001) && python main_fastapi.py"

echo        Warte auf Backend...
set RETRY=0
:WAIT_BACKEND
set /a RETRY+=1
if %RETRY% gtr 30 (
    color 0C
    echo.
    echo   [FEHLER] Backend startet nicht nach 30 Sekunden!
    echo   Pruefe das Backend-Fenster auf Fehler.
    pause
    exit /b 1
)
timeout /t 1 /nobreak >nul
curl -s http://localhost:8001/health >nul 2>&1
if %errorlevel% neq 0 (
    echo        [%RETRY%/30] Warte...
    goto WAIT_BACKEND
)

:: ========== FERTIG ==========
color 0A
echo.
start "" "http://localhost:8001/"

echo  ============================================================
echo   NAJIKA WORLD V2.0 LAEUFT! (FASTAPI)
echo  ============================================================
echo.
echo   Frontend: http://localhost:8001/
echo   API Docs: http://localhost:8001/docs
echo   ReDoc:    http://localhost:8001/redoc
echo   Ollama:   http://localhost:11434
echo.
echo   NEUE FEATURES (2026-02-15):
echo   - Medicine Crafting UI (64 Fantasy-Pflanzen)
echo   - Companion Mode Choice (Aura vs Koerperlich)
echo   - Dynamic Factions UI (Voelker-Kriege)
echo   - Form Affinity System (Boni + Synergien)
echo   - Slime V3 System (Formwandler, Aura, Trust)
echo.
echo   Models:   najika-natural (SFW)
echo             najika-nsfw-natural (Kaetzchen-Modus)
echo.
echo   Stoppen:  Druecke eine Taste oder schliesse dieses Fenster
echo  ============================================================
echo.
pause >nul

:: Cleanup
taskkill /FI "WINDOWTITLE eq Najika FastAPI Backend*" /F >nul 2>&1
echo  Backend gestoppt. Tschuess!
timeout /t 2 >nul
