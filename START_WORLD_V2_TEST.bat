@echo off
REM ===================================================================
REM NAJIKA WORLD V2 - TEST SERVER (Port 8001)
REM ===================================================================
REM Startet separaten Server nur für World Manager V2 Test
REM Läuft parallel zum Hauptserver (Port 8000)
REM ===================================================================

echo.
echo ========================================
echo  NAJIKA WORLD V2 - TEST SERVER
echo ========================================
echo.
echo Startet Test-Server auf Port 8001...
echo.
echo WICHTIG:
echo  - Hauptserver (Port 8000) bleibt unberührt
echo  - V2 Test läuft parallel auf Port 8001
echo  - Browser: http://localhost:8001/najika_world_v2.html
echo.
echo ========================================
echo.

REM Absoluter Pfad zum digivice-Ordner
cd /d "%~dp0digivice"

REM Prüfe ob Ordner existiert
if not exist "najika_world_v2.html" (
    echo FEHLER: najika_world_v2.html nicht gefunden!
    echo Stelle sicher, dass die BAT-Datei im Najika_World Root liegt.
    pause
    exit /b 1
)

echo Server startet in: %cd%
echo.

REM Öffne Browser nach 2 Sekunden
start /min cmd /c "timeout /t 2 /nobreak >nul && start http://localhost:8001/najika_world_v2.html"

REM Starte Server
echo Python HTTP Server läuft auf Port 8001...
echo Drücke Strg+C zum Beenden
echo.
python -m http.server 8001

pause
