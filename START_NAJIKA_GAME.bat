@echo off
title Najika World - Complete Game (9 Regions + Full Content)
color 0B

echo ========================================
echo   NAJIKA WORLD - COMPLETE GAME
echo ========================================
echo.
echo   9600x9600 Open World
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
echo   http://localhost:5173/najika_world_v2.html
echo.
echo Controls:
echo   WASD - Movement
echo   Mouse - Look around
echo   E - Interact
echo   Q - Toggle Exterior/Interior
echo.
echo Press CTRL+C to stop
echo ========================================
echo.

cd C:\Najika_World\digivice

start http://localhost:5173/najika_world_v2.html

python -m http.server 5173
