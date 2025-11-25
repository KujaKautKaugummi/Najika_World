@echo off
title Najika World - Phase 1 (Flat Terrain - Stable)
color 0B

echo ========================================
echo   NAJIKA WORLD - PHASE 1 (FLAT)
echo ========================================
echo.
echo   Mode: Flat Terrain (Stable)
echo   Map: 9.6km x 9.6km
echo   Regions: 9 (3x3 Grid)
echo   Performance: Best
echo.
echo   Frontend: http://localhost:5173
echo   File: najika_world_UNIFIED.html
echo ========================================
echo.

REM Setze USE_PHASE_2 auf false (Phase 1)
echo [1/2] Setting Phase 1 mode (Flat Terrain)...
powershell -Command "(Get-Content 'digivice/najika_world_UNIFIED.html') -replace 'const USE_PHASE_2 = true;', 'const USE_PHASE_2 = false;' | Set-Content 'digivice/najika_world_UNIFIED.html'"
echo Done: Phase 1 (Flat) activated!
echo.

REM Warte kurz
timeout /t 1 /nobreak >nul

REM Starte Frontend (HTTP Server + Browser)
echo [2/2] Starting game server (Port 5173)...
cd /d %~dp0digivice

REM Offne Browser
start http://localhost:5173/najika_world_UNIFIED.html

REM Starte HTTP Server (blockiert, daher am Ende)
echo.
echo ========================================
echo   NAJIKA WORLD PHASE 1 LAUFT!
echo ========================================
echo.
echo   Mode: FLAT TERRAIN (Stable)
echo   URL: http://localhost:5173/najika_world_UNIFIED.html
echo.
echo   Features:
echo   - Flat Map (9.6km x 9.6km)
echo   - 9 Regions (3x3 Grid)
echo   - 8 Cities + Goetterfels
echo   - Schwarze Muhle (4 Etagen: EG/OG/Turm/Keller)
echo   - Combat System + All Game Content (40 JSON)
echo.
echo   Performance: BEST (recommended!)
echo.
echo   Press CTRL+C to stop
echo ========================================
echo.

python -m http.server 5173
