@echo off
title Najika World
cd /d "C:\Najika-World"
start /B python backend\game_server.py
timeout /t 3 >nul
start frontend\index.html
echo Server laeuft auf Port 7010
pause
