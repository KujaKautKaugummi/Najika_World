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
echo [2/4] Starte Najika Backend Server (Port 8000)...
cd /d "%NAJIKA_DIR%backend"
start "Najika Server" cmd /k "python najika_server.py"
timeout /t 3 /nobreak >nul
echo     Backend Server gestartet!

echo.
echo [3/4] Starte Digivice Web-Server (Port 8080)...
cd /d "%NAJIKA_DIR%digivice"
start "Digivice Server" cmd /k "python -m http.server 8080"
timeout /t 2 /nobreak >nul
echo     Digivice Server gestartet!

echo.
echo [4/4] Oeffne Najika World im Browser...
timeout /t 2 /nobreak >nul
start "" "http://localhost:8080/najika_world_UNIFIED.html"

echo.
echo ═══════════════════════════════════════════════════════════════════════
echo  NAJIKA WORLD GESTARTET!
echo ═══════════════════════════════════════════════════════════════════════
echo.
echo  Browser:     http://localhost:8080/najika_world_UNIFIED.html
echo  Backend API: http://localhost:8000/
echo  Digivice:    http://localhost:8080/
echo.
echo  CLI starten: najika.bat (im Projektordner)
echo.
echo  Zum Beenden: Schliesse dieses Fenster oder druecke STRG+C
echo ═══════════════════════════════════════════════════════════════════════
echo.

pause
