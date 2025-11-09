@echo off
echo ============================================================
echo    NAJIKA - COMPLETE MOBILE ACCESS
echo    Domain: a2572.duckdns.org
echo ============================================================
echo.

REM Kill old processes
echo [1/4] Stopping old servers...
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM cloudflared.exe >nul 2>&1
timeout /t 2 /nobreak >nul

REM Update DuckDNS IP
echo [2/4] Updating DuckDNS IP...
powershell -Command "Invoke-WebRequest -Uri 'https://www.duckdns.org/update?domains=a2572&token=18300801-e8ad-4623-90c7-22002a8fa873&ip=' -UseBasicParsing | Out-Null"
echo     DuckDNS updated: a2572.duckdns.org

REM Start Najika Server
echo [3/4] Starting Najika Server on port 8000...
start /min "Najika Server" cmd /c "cd /d %~dp0backend && python najika_server.py"
timeout /t 5 /nobreak >nul

REM Start Cloudflare Tunnel
echo [4/4] Starting Cloudflare Tunnel...
echo.
echo ============================================================
echo  MOBILE URLS (kopiere eine auf dein Handy):
echo.
echo  LOKAL (im gleichen WLAN):
echo  http://192.168.178.68:8000/digivice/
echo.
echo  DuckDNS (braucht Port-Forwarding):
echo  http://a2572.duckdns.org:8000/digivice/
echo.
echo  CLOUDFLARE (von überall, ohne Port-Forwarding):
echo  Die URL erscheint gleich unten...
echo ============================================================
echo.

C:\cloudflared.exe tunnel --url http://localhost:8000

pause
