@echo off
chcp 65001 >nul
cls

echo ========================================
echo  NAJIKA WORLD - Complete Start
echo ========================================
echo.
echo 1. Starting Backend Server...
echo 2. Opening Browser...
echo.

cd /d "%~dp0"

:: Start Backend in new window
start "Najika Backend" cmd /k "cd /d %~dp0backend && python najika_server.py"

:: Wait 3 seconds for server to start
timeout /t 3 /nobreak >nul

:: Open Browser
start http://localhost:8000/digivice/

echo.
echo ========================================
echo  Backend running in separate window
echo  Browser opened: http://localhost:8000/digivice/
echo ========================================
echo.
echo Press any key to open API docs...
pause >nul

start http://localhost:8000/docs

echo.
echo Backend is running!
echo Press any key to exit this window...
pause >nul
