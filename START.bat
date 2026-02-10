@echo off
chcp 65001 >nul 2>&1
title NAJIKA WORLD - Komplett-Start
color 0A

echo.
echo  ========================================================
echo     _   _    _      _ ___ _  __    _
echo    ^| ^| ^| ^|  ^/ \    ^| ^|_ _^| ^|/ /  ^/ \
echo    ^| ^|_^| ^| / _ \   ^| ^|^| ^| ^| ' /  / _ \
echo    ^|  _  ^|/ ___ \  ^| ^|^| ^| ^| . \ / ___ \
echo    ^|_^| ^|_/_/   \_\_^| ^|___^|_^|\_/_/   \_\
echo              ^|__/
echo     W O R L D   -   K O M P L E T T   S T A R T
echo  ========================================================
echo.

set "NAJIKA_DIR=%~dp0"

:: ========== 1. Ollama ==========
echo  [1/3] Pruefe Ollama...
tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I "ollama.exe" >NUL
if "%ERRORLEVEL%"=="1" (
    echo        Starte Ollama...
    start "" /MIN ollama serve
    timeout /t 4 /nobreak >nul
    echo        Ollama gestartet!
) else (
    echo        Ollama laeuft bereits!
)

:: ========== 2. Backend ==========
echo.
echo  [2/3] Starte FastAPI Backend (Port 8000)...
cd /d "%NAJIKA_DIR%"
start "Najika Backend" /MIN cmd /k "title Najika Backend && cd /d "%NAJIKA_DIR%" && python backend\main_fastapi.py"
timeout /t 4 /nobreak >nul
echo        Backend gestartet!

:: ========== 3. Browser ==========
echo.
echo  [3/3] Oeffne Browser...
start "" "http://localhost:8000/digivice/"
timeout /t 1 /nobreak >nul

echo.
echo  ========================================================
echo   NAJIKA WORLD LAEUFT!
echo  ========================================================
echo.
echo   Spiel:       http://localhost:8000/digivice/
echo   API Docs:    http://localhost:8000/docs
echo   Ollama:      http://localhost:11434
echo.
echo   Chat:        Normal = SFW
echo                Tippe "kaetzchen" = NSFW Modus
echo.
echo   Stoppen:     Schliesse dieses Fenster
echo  ========================================================
echo.
echo  Druecke eine Taste zum Beenden...
pause >nul

:: Cleanup: Kill backend
taskkill /FI "WINDOWTITLE eq Najika Backend" /F >nul 2>&1
echo  Backend gestoppt. Tschuess!
timeout /t 2 >nul
