@echo off
title Najika World - Game Only (No Backend)
color 0B

echo ========================================
echo   NAJIKA WORLD - GAME ONLY
echo ========================================
echo.
echo   9.6km x 9.6km Open World (1.75x Fortnite BR!)
echo   9 Regions - Full Content
echo   Combat System - Realtime
echo.
echo   NOTE: Backend NOT started!
echo   Status: "Backend Offline" (red dot)
echo.
echo   Features OHNE Backend:
echo   - Open World Map (9.6km x 9.6km)
echo   - Combat System (Realtime)
echo   - Schwarze Muhle (4 Etagen: EG/OG/Turm/Keller)
echo   - Movement + Enemies
echo.
echo   Features MIT Backend (starte: START_NAJIKA_FULL.bat):
echo   - Najika AI Chat
echo   - Teleport System
echo   - Stats Sync
echo   - Voice Call (falls TTS)
echo ========================================
echo.
echo Starting game server...
echo.
echo Game will open at:
echo   http://localhost:5173/najika_world_UNIFIED.html
echo.
echo Controls:
echo   WASD - Movement (6-9 m/s)
echo   Shift - Sprint
echo   E - Interact (Mühle/Städte)
echo   Tab - Combat Mode (MANUAL/ASSIST/AUTO)
echo   Q/E/SPACE/C/X/V - Combat Actions
echo.
echo Press CTRL+C to stop
echo ========================================
echo.

cd C:\Najika_World\digivice

start http://localhost:5173/najika_world_UNIFIED.html

python -m http.server 5173
