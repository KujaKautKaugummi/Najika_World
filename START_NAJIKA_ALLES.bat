@echo off
title NAJIKA WORLD - KOMPLETTSTART (OLLAMA)
color 0B
chcp 65001 >nul

echo ============================================================
echo   NAJIKA WORLD - KOMPLETTSTART (OLLAMA)
echo ============================================================
echo.

REM ===== SCHRITT 1: OLLAMA PRUEFEN/STARTEN =====
echo [1/4] Pruefe Ollama...

curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% equ 0 goto OLLAMA_OK

echo   [!] Ollama Server laeuft nicht
echo   [!] Starte Ollama...
start /B ollama serve >nul 2>&1
timeout /t 3 /nobreak >nul

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
color 0A
echo   [OK] Ollama Server laeuft auf Port 11434
echo.

REM ===== SCHRITT 2: MODELS PRUEFEN =====
echo [2/4] Pruefe Najika Models...
ollama list | findstr "najika-local" >nul
if %errorlevel% neq 0 (
    echo   [!] najika-local nicht gefunden - erstelle...
    ollama create najika-local -f backend/najika-local.Modelfile
)
echo   [OK] najika-local

ollama list | findstr "najika-nsfw" >nul
if %errorlevel% neq 0 (
    echo   [!] najika-nsfw nicht gefunden - erstelle...
    ollama create najika-nsfw -f backend/najika-nsfw.Modelfile
)
echo   [OK] najika-nsfw
echo.

REM ===== SCHRITT 3: ALTE PROZESSE BEENDEN =====
echo [3/4] Bereinige alte Prozesse auf Port 8000...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000.*LISTENING" 2^>nul') do taskkill /PID %%a /F >nul 2>&1
echo   [OK] Bereinigt
echo.

REM ===== SCHRITT 4: BACKEND STARTEN =====
echo [4/4] Starte Najika Backend...
start "Najika Backend" cmd /k "cd /d %~dp0backend && python najika_server.py"

echo.
echo   Warte auf Backend...

REM ===== WARTE BIS BACKEND WIRKLICH LAEUFT =====
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
curl -s http://localhost:8000/api/status >nul 2>&1
if %errorlevel% neq 0 (
    echo   [%RETRY%/30] Warte auf Backend...
    goto WAIT_BACKEND
)

color 0A
echo.
echo   [OK] Backend laeuft!
echo.

REM ===== BROWSER OEFFNEN =====
echo Oeffne Browser...
start http://localhost:8000/digivice/index.html

echo.
echo ============================================================
echo   NAJIKA WORLD LAEUFT!
echo ============================================================
echo.
echo   Ollama   : http://localhost:11434 (AI)
echo   Backend  : http://localhost:8000  (Server)
echo   Spiel    : http://localhost:8000/digivice/index.html
echo.
echo   MODELLE:
echo   - SFW Chat:  najika-local
echo   - NSFW Chat: najika-nsfw (Kaetzchen-Modus)
echo   - Tasks:     qwen2-instruct
echo.
echo   Dieses Fenster kann geschlossen werden.
echo ============================================================
pause
