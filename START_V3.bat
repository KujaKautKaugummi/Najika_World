@echo off
chcp 65001 >nul 2>&1
title NAJIKA WORLD - START
color 0A

echo.
echo  ============================================================
echo     NAJIKA WORLD - START (Neuer PC Setup)
echo  ============================================================
echo.

set "NAJIKA_DIR=%~dp0"
set "VENV_PYTHON=%NAJIKA_DIR%venv\Scripts\python.exe"

:: Pruefe venv
if not exist "%VENV_PYTHON%" (
    color 0C
    echo   [FEHLER] venv nicht gefunden!
    echo   Erwartet: %VENV_PYTHON%
    echo   Bitte erstelle venv mit Python 3.12
    pause
    exit /b 1
)

:: ========== 1. OLLAMA ==========
echo  [1/3] Pruefe Ollama...
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% equ 0 goto OLLAMA_OK

echo        Starte Ollama...
start /B /MIN ollama serve >nul 2>&1
timeout /t 5 /nobreak >nul

curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo.
    echo   [FEHLER] Ollama konnte nicht gestartet werden!
    pause
    exit /b 1
)

:OLLAMA_OK
echo        [OK] Ollama laeuft

:: Pruefe Najika Models
ollama list | findstr "najika-natural" >nul
if %errorlevel% neq 0 (
    echo        Erstelle najika-natural...
    cd /d "%NAJIKA_DIR%"
    ollama create najika-natural -f backend\najika-natural.Modelfile
)
ollama list | findstr "najika-nsfw-natural" >nul
if %errorlevel% neq 0 (
    echo        Erstelle najika-nsfw-natural...
    cd /d "%NAJIKA_DIR%"
    ollama create najika-nsfw-natural -f backend\najika-nsfw-natural.Modelfile
)
echo        [OK] Najika Models verfuegbar
echo.

:: ========== 2. PORT BEREINIGEN ==========
echo  [2/3] Bereinige Port 8000...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000.*LISTENING" 2^>nul') do taskkill /PID %%a /F >nul 2>&1
timeout /t 1 /nobreak >nul
echo        [OK] Port 8000 frei
echo.

:: ========== 3. BACKEND STARTEN (FastAPI + Uvicorn) ==========
echo  [3/3] Starte Najika FastAPI Backend (Port 8000)...
cd /d "%NAJIKA_DIR%"
start "Najika Backend" /MIN cmd /k "title Najika Backend - FastAPI (Port 8000) && \"%NAJIKA_DIR%venv\Scripts\python.exe\" -m uvicorn backend.main_fastapi:app --host 127.0.0.1 --port 8000"

echo        Warte auf Backend...
set RETRY=0
:WAIT_BACKEND
set /a RETRY+=1
if %RETRY% gtr 30 (
    color 0C
    echo.
    echo   [FEHLER] Backend startet nicht!
    echo   Pruefe das Backend-Fenster auf Fehler.
    pause
    exit /b 1
)
timeout /t 1 /nobreak >nul
curl -s http://127.0.0.1:8000/health >nul 2>&1
if %errorlevel% neq 0 goto WAIT_BACKEND

:: ========== FERTIG ==========
color 0A
echo.
echo  ============================================================
echo    NAJIKA WORLD LAEUFT! (FastAPI)
echo  ============================================================
echo.
echo    Frontend: http://127.0.0.1:8000/digivice/
echo    Health:   http://127.0.0.1:8000/health
echo    API Docs: http://127.0.0.1:8000/docs
echo    Ollama:   http://localhost:11434
echo.
echo    Models:   najika-natural (SFW)
echo              najika-nsfw-natural (Kaetzchen-Modus)
echo              qwen2:7b (Tasks/Code)
echo.
start "" "http://127.0.0.1:8000/digivice/"
echo.
echo    Zum Stoppen: Druecke eine Taste
echo  ============================================================
echo.
pause >nul

:: Cleanup
taskkill /FI "WINDOWTITLE eq Najika Backend*" /F >nul 2>&1
echo  Backend gestoppt. Tschuess!
timeout /t 2 >nul
