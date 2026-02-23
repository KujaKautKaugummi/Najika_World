@echo off
chcp 65001 >nul
color 0B
title NAJIKA WORLD - Quick Game Start

REM ============================================================
REM  🚀 QUICK START - Nur FastAPI (Port 8001)
REM  Für schnelles Testen der Combat-Systeme
REM ============================================================

echo.
echo ============================================================
echo    🚀 NAJIKA - QUICK GAME START
echo    Nur FastAPI Server (Port 8001)
echo ============================================================
echo.

REM Kill old processes
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM uvicorn.exe >nul 2>&1
timeout /t 1 /nobreak >nul

REM Start nur FastAPI
echo [1/2] Starting FastAPI Server (Port 8001)...
cd /d "%~dp0"
start /min "FastAPI" cmd /c "uvicorn main:app --host 127.0.0.1 --port 8001 --reload"
timeout /t 3 /nobreak >nul

echo [2/2] Opening browser...
start http://localhost:8001/digivice/najika_world_UNIFIED.html

echo.
echo ============================================================
echo  ✅ GAME GESTARTET!
echo ============================================================
echo.
echo  URL: http://localhost:8001/digivice/najika_world_UNIFIED.html
echo.
echo  TEST-BEFEHLE (in Browser Console - F12):
echo    window.Real3DCombat          // Sollte Object sein
echo    window.EquipmentCombat       // Sollte Object sein
echo    window.OverworldEnemies      // Sollte Object sein
echo    window.UnifiedCombat         // Sollte undefined sein!
echo.
echo  ⚠️  Server läuft im Hintergrund
echo  ⚠️  Zum Beenden: STRG+C oder Fenster schließen
echo ============================================================
echo.
pause
