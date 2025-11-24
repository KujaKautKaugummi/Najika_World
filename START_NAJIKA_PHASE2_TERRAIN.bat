@echo off
title Najika World - Phase 2 (Terrain Variation - Experimental)
color 0E

echo ========================================
echo   NAJIKA WORLD - PHASE 2 (TERRAIN)
echo ========================================
echo.
echo   Mode: Terrain Variation (Experimental)
echo   Map: 9.6km x 9.6km
echo   Features: Mountains, Valleys, Vegetation
echo   Performance: Medium-High (GPU required)
echo.
echo   Frontend: http://localhost:5173
echo   File: najika_world_UNIFIED.html
echo ========================================
echo.

REM Setze USE_PHASE_2 auf true (Phase 2)
echo [1/2] Setting Phase 2 mode (Terrain Variation)...
powershell -Command "(Get-Content 'digivice/najika_world_UNIFIED.html') -replace 'const USE_PHASE_2 = false;', 'const USE_PHASE_2 = true;' | Set-Content 'digivice/najika_world_UNIFIED.html'"
echo Done: Phase 2 (Terrain) activated!
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
echo   NAJIKA WORLD PHASE 2 LAUFT!
echo ========================================
echo.
echo   Mode: TERRAIN VARIATION (Experimental)
echo   URL: http://localhost:5173/najika_world_UNIFIED.html
echo.
echo   Features:
echo   - Terrain Variation (Mountains, Valleys)
echo   - Vegetation System (Trees, Grass)
echo   - Biome Effects (Fog, Lighting)
echo   - Region Streaming (Performance)
echo   - LOD System (3 Detail Levels)
echo.
echo   Performance: Medium-High (GPU required)
echo   Status: EXPERIMENTAL - May have issues!
echo.
echo   If errors occur: Use Phase 1 (Flat)
echo   Press CTRL+C to stop
echo ========================================
echo.

python -m http.server 5173
