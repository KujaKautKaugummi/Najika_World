@echo off
echo ================================================
echo    NAJIKA - START MIT CLOUDFLARE TUNNEL
echo ================================================
echo.

REM Najika Server starten (Hintergrund)
echo [1/2] Starte Najika Server...
start /min cmd /c "cd /d %~dp0backend && python najika_server.py"

REM 3 Sekunden warten
timeout /t 3 /nobreak >nul

REM Check ob cloudflared existiert
if not exist "C:\cloudflared.exe" (
    echo.
    echo [ERROR] cloudflared.exe nicht gefunden!
    echo.
    echo Bitte zuerst installieren:
    echo 1. Oeffne PowerShell als Admin
    echo 2. Fuehre aus:
    echo    Invoke-WebRequest -Uri "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe" -OutFile "C:\cloudflared.exe"
    echo.
    pause
    exit /b 1
)

REM Cloudflare Tunnel starten
echo [2/2] Starte Cloudflare Tunnel...
echo.
echo ================================================
echo  WICHTIG: Kopiere die URL unten!
echo  Oeffne sie auf deinem Handy!
echo ================================================
echo.

C:\cloudflared.exe tunnel --url http://localhost:8000

pause
