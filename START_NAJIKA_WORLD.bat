@echo off
title NAJIKA WORLD v1.1
color 0A
cd /d "C:\Najika-World"

cls
echo.
echo ========================================================================
echo                      NAJIKA WORLD V1.1
echo ========================================================================
echo.
echo [INFO] Starte Najika World Server...
echo.

REM Pruefen ob Ollama laeuft
echo [1/3] Pruefe Ollama...
curl -s http://127.0.0.1:11434/api/tags >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [WARNUNG] Ollama scheint nicht zu laufen!
    echo           Bitte starte Ollama zuerst.
    echo.
    pause
    exit /b 1
)
echo       [OK] Ollama laeuft!

REM Backend starten
echo [2/3] Starte Backend Server (Port 8000)...
cd backend
start "Najika Backend" cmd /k "python najika_server.py"
cd ..
timeout /t 5 >nul

REM Browser oeffnen
echo [3/3] Oeffne Browser...
timeout /t 2 >nul
start http://localhost:8000/digivice/

echo.
echo ========================================================================
echo                    NAJIKA WORLD ERFOLGREICH GESTARTET!
echo ========================================================================
echo.
echo   Digivice UI:  http://localhost:8000/digivice/
echo   Backend API:  http://localhost:8000/api/
echo   Chat:         http://localhost:8000/digivice/#chat
echo.
echo   Optional React Frontend: http://localhost:3002/ (manual start)
echo.
echo ========================================================================
echo.
echo [HINWEIS] Backend-Fenster offen lassen!
echo           Schliesse DIESES Fenster zum Beenden.
echo.
pause >nul
