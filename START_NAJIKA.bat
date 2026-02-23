@echo off
chcp 65001 >nul
color 0A
echo ============================================================
echo    🎮 NAJIKA WORLD - COMPLETE GAME STARTUP
echo    Combat Systems Update - 2026-02-17
echo ============================================================
echo.
echo [INFO] Startet BEIDE Server:
echo   - Flask Server (Port 8000) - Chat, TTS, Living System
echo   - FastAPI Server (Port 8001) - Game, Combat, Arena
echo.

REM Kill old processes
echo [1/3] Stopping old servers...
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM uvicorn.exe >nul 2>&1
timeout /t 2 /nobreak >nul

REM Start beide Server via Python Script
echo [2/3] Starting all backend servers...
cd /d "%~dp0backend"
start "NAJIKA Backend" python start_all_servers.py

REM Warte bis Server bereit sind
echo [3/3] Waiting for servers to be ready...
timeout /t 5 /nobreak >nul

echo.
echo ============================================================
echo  ✅ NAJIKA WORLD GESTARTET!
echo ============================================================
echo.
echo  URLS zum Öffnen:
echo.
echo  📱 GAME (Unity/3D):
echo     http://localhost:8001/digivice/najika_world_UNIFIED.html
echo.
echo  💬 CHAT (Flask):
echo     http://localhost:8000/digivice/
echo.
echo  🎮 COMBAT TEST:
echo     - F12 drücken (Console)
echo     - window.Real3DCombat eingeben
echo     - Sollte Object zurückgeben (nicht undefined!)
echo.

REM Browser automatisch öffnen
echo [+] Öffne Browser...
start http://localhost:8001/digivice/

echo  ⚠️  Zum Beenden: STRG+C in diesem Fenster
echo ============================================================
echo.
echo [LOG] Backend läuft. Fenster offen lassen!
echo.
pause
