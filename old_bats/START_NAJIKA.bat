@echo off
chcp 65001 >nul
title NAJIKA WORLD
color 0A

echo.
echo   ========================================
echo   NAJIKA WORLD
echo   ========================================
echo.

REM Ollama im Hintergrund
start /B ollama serve 2>nul

REM Port freigeben
for /f "tokens=5" %%a in ('netstat -ano 2^>nul ^| findstr ":8000.*LISTEN"') do taskkill /F /PID %%a >nul 2>&1

echo   Backend startet...
echo   Browser oeffnet automatisch wenn bereit.
echo.

REM Backend starten und auf Port warten
cd /d "C:\Najika_World\backend"
start /B python najika_server.py

:WAIT
ping -n 2 127.0.0.1 >nul
netstat -ano | findstr ":8000.*LISTEN" >nul
if errorlevel 1 goto WAIT

echo   ========================================
echo   BACKEND LAEUFT!
echo   ========================================
echo.
start "" "http://localhost:8000/digivice/index.html"
echo   Browser geoeffnet!
echo.
echo   Druecke eine Taste zum Beenden...
pause >nul
taskkill /F /IM python.exe >nul 2>&1
