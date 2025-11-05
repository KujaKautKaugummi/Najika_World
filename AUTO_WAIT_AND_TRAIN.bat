@echo off
REM NAJIKA AUTO TRAINING - Wartet bis 00:00 und startet dann automatisch
REM Starte dieses Script jetzt - es wartet bis Mitternacht!

echo ================================================================================
echo NAJIKA AUTO TRAINING - WARTE BIS MITTERNACHT
echo ================================================================================
echo.
echo Dieses Script:
echo   1. Wartet bis 00:00 Uhr
echo   2. Startet dann automatisch das 8-10h Training
echo   3. Du kannst jetzt schlafen gehen!
echo.

cd /d "C:\Najika-World\backend"

:WAIT_LOOP
REM Aktuelle Stunde auslesen
for /f "tokens=1 delims=:" %%h in ("%TIME%") do set HOUR=%%h
REM Führende Nullen entfernen
set /a HOUR=1%HOUR% %% 100

echo [%TIME%] Warte... (Stunde: %HOUR%)

REM Wenn Stunde = 0 (Mitternacht), starte Training
if %HOUR%==0 goto START_TRAINING

REM Sonst: 5 Minuten warten und nochmal prüfen
timeout /t 300 /nobreak >nul
goto WAIT_LOOP

:START_TRAINING
echo.
echo ================================================================================
echo [%TIME%] MITTERNACHT! Training startet JETZT!
echo ================================================================================
echo.

python najika_intensive_night_training.py

echo.
echo [%TIME%] Training FERTIG!
echo Log: backend\training_night_log.json
echo.
pause
