@echo off
echo ================================================
echo    NAJIKA - MOBILE ACCESS SETUP
echo ================================================
echo.

REM Kill any running Python servers
echo [1/3] Stopping old servers...
taskkill /F /IM python.exe >nul 2>&1

REM Wait a moment
timeout /t 2 /nobreak >nul

REM Start Najika Server
echo [2/3] Starting Najika Server...
start /min "Najika Server" cmd /c "cd /d %~dp0backend && python najika_server.py"

REM Wait for server to start
echo Waiting for server to start...
timeout /t 5 /nobreak >nul

REM Check if cloudflared exists
if not exist "C:\cloudflared.exe" (
    echo.
    echo [ERROR] cloudflared.exe not found!
    echo Please run this script as Administrator first.
    pause
    exit /b 1
)

REM Start Cloudflare Tunnel
echo [3/3] Starting Cloudflare Tunnel...
echo.
echo ================================================
echo  YOUR MOBILE URL WILL APPEAR BELOW!
echo  Copy it and open on your phone!
echo ================================================
echo.

C:\cloudflared.exe tunnel --url http://localhost:8000

pause
