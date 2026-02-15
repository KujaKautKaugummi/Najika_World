@echo off
chcp 65001 >nul
cls

echo ========================================
echo  NAJIKA WORLD - Backend Server
echo ========================================
echo.
echo Starting Najika Backend on Port 8000...
echo.

cd /d "%~dp0\backend"
python najika_server.py

pause
