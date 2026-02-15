@echo off
chcp 65001 >nul 2>&1
title NAJIKA WORLD - Komplett-Start

echo.
echo  ╔══════════════════════════════════════════════════════════════════╗
echo  ║                                                                  ║
echo  ║     ███╗   ██╗ █████╗      ██╗██╗██╗  ██╗ █████╗                 ║
echo  ║     ████╗  ██║██╔══██╗     ██║██║██║ ██╔╝██╔══██╗                ║
echo  ║     ██╔██╗ ██║███████║     ██║██║█████╔╝ ███████║                ║
echo  ║     ██║╚██╗██║██╔══██║██   ██║██║██╔═██╗ ██╔══██║                ║
echo  ║     ██║ ╚████║██║  ██║╚█████╔╝██║██║  ██╗██║  ██║                ║
echo  ║     ╚═╝  ╚═══╝╚═╝  ╚═╝ ╚════╝ ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝                ║
echo  ║                                                                  ║
echo  ║                    WORLD - KOMPLETT START                        ║
echo  ║                                                                  ║
echo  ╚══════════════════════════════════════════════════════════════════╝
echo.

set NAJIKA_DIR=%~dp0

echo [1/4] Starte Ollama (falls nicht laeuft)...
tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I /N "ollama.exe">NUL
if "%ERRORLEVEL%"=="1" (
    start "" ollama serve
    timeout /t 3 /nobreak >nul
    echo     Ollama gestartet!
) else (
    echo     Ollama laeuft bereits!
)

echo.
echo [2/3] Starte Najika Backend Server (Port 8000)...
cd /d "%NAJIKA_DIR%backend"
start "Najika Server" cmd /k "python najika_server.py"
timeout /t 5 /nobreak >nul
echo     Backend Server gestartet!

echo.
echo [3/3] Oeffne Najika World im Browser...
start "" "http://localhost:8000/digivice/index.html"

echo.
echo ═══════════════════════════════════════════════════════════════════════
echo  NAJIKA WORLD GESTARTET!
echo ═══════════════════════════════════════════════════════════════════════
echo.
echo  Spiel:       http://localhost:8000/digivice/index.html
echo  Backend API: http://localhost:8000/
echo.
echo  CLI starten: najika.bat (im Projektordner)
echo.
echo  Zum Beenden: Schliesse dieses Fenster oder druecke STRG+C
echo ═══════════════════════════════════════════════════════════════════════
echo.

pause
