@echo off
title Najika World - Complete Game (9 Regions + Full Content)
color 0B

echo ========================================
echo   NAJIKA WORLD - COMPLETE GAME
echo ========================================
echo.
echo   9.6km x 9.6km Open World (1.75x Fortnite BR!)
echo   9 Regions - Full Content
echo   ~90 NPCs with Najika Reactions
echo   ~200 Items (Weapons, Armor, etc)
echo   ~80 Quests (Oregon Trail Style)
echo   ~45 Enemies + 9 Boss Fights
echo ========================================
echo.
echo Starting game...
echo.
echo Game will open at:
echo   http://localhost:5173/najika_world_UNIFIED.html
echo.
echo Controls:
echo   WASD - Movement (80 units/s, fast!)
echo   Mouse - Look around
echo   E - Interact with NPCs
echo   Q/E/SPACE/C/X/V - Combat (MANUAL mode)
echo   Tab - Switch Combat Mode (MANUAL/ASSIST/AUTO)
echo.
echo Press CTRL+C to stop
echo ========================================
echo.

cd C:\Najika_World\digivice

start http://localhost:5173/najika_world_UNIFIED.html

python -m http.server 5173
