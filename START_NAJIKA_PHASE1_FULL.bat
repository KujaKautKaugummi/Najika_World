@echo off
title Najika World - Phase 1 + Backend (Flat Terrain)
color 0B

echo ========================================
echo   NAJIKA WORLD - PHASE 1 + BACKEND
echo ========================================
echo.
echo   Mode: Flat Terrain + Backend
echo   Backend: http://localhost:8000
echo   Frontend: http://localhost:5173
echo.
echo   Starting Backend + Frontend...
echo ========================================
echo.

REM Setze USE_PHASE_2 auf false (Phase 1)
echo [1/3] Setting Phase 1 mode (Flat Terrain)...
powershell -Command "(Get-Content 'digivice/najika_world_UNIFIED.html') -replace 'const USE_PHASE_2 = true;', 'const USE_PHASE_2 = false;' | Set-Content 'digivice/najika_world_UNIFIED.html'"
echo Done: Phase 1 (Flat) activated!
echo.

REM Warte kurz
timeout /t 1 /nobreak >nul

REM Starte Backend (Najika Server) in neuem Fenster
echo [2/3] Starting Najika Backend (Port 8000)...
start "Najika Backend (Port 8000)" cmd /k "cd /d %~dp0backend && python najika_server.py"

REM Warte 3 Sekunden damit Backend Zeit hat zu starten
timeout /t 3 /nobreak >nul

REM Starte Frontend (HTTP Server + Browser)
echo [3/3] Starting Game Server (Port 5173)...
cd /d %~dp0digivice

REM Offne Browser
start http://localhost:5173/najika_world_UNIFIED.html

REM Starte HTTP Server (blockiert, daher am Ende)
echo.
echo ========================================
echo   NAJIKA WORLD PHASE 1 + BACKEND LAUFT!
echo ========================================
echo.
echo   Backend:  http://localhost:8000 (Fenster 1)
echo   Frontend: http://localhost:5173 (Fenster 2)
echo.
echo   Status: Backend Online (grüner Punkt)
echo   Mode: FLAT TERRAIN (Stable)
echo   Features: Chat, Teleport, Stats Sync, Voice
echo.
echo   Press CTRL+C to stop Frontend
echo   Schliesse "Backend" Fenster für Server
echo ========================================
echo.

python -m http.server 5173
