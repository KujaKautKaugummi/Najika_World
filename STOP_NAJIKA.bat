@echo off
title STOP NAJIKA WORLD
color 0C
echo.
echo ========================================================================
echo                      NAJIKA WORLD - NOTFALL STOP
echo ========================================================================
echo.
echo [WARNUNG] Dies stoppt alle Najika Prozesse!
echo           Nur im Notfall verwenden!
echo.
echo           Normal: Einfach Backend-Fenster schliessen.
echo.
pause
echo.
echo [1/2] Stoppe Python Prozesse (najika_server.py)...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq Najika Backend*" 2>nul
if %ERRORLEVEL% EQU 0 (
    echo       [OK] Backend gestoppt
) else (
    echo       [INFO] Kein Backend gefunden
)

echo [2/2] Stoppe alle Python Prozesse auf Port 8000...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    taskkill /F /PID %%a 2>nul
)
echo       [OK] Port 8000 freigegeben

echo.
echo ========================================================================
echo                      NAJIKA WORLD GESTOPPT
echo ========================================================================
echo.
pause
