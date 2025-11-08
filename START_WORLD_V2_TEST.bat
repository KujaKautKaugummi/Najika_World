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

cd digivice

echo Server startet...
python -m http.server 8001

pause
