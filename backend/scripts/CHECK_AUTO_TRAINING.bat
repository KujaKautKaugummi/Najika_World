@echo off
REM Überprüft ob Najika Training Tasks korrekt eingerichtet sind

echo ================================================================================
echo NAJIKA TRAINING - SYSTEM CHECK
echo ================================================================================
echo.

echo [CHECK 1/6] Suche nach Najika Training Tasks...
echo.
schtasks /Query | findstr "Najika"
echo.

echo ================================================================================
echo [CHECK 2/6] Details NajikaTraining09...
echo ================================================================================
schtasks /Query /TN "NajikaTraining09" /FO LIST /V 2>nul
if errorlevel 1 (
    echo [FEHLER] NajikaTraining09 nicht gefunden!
) else (
    echo [OK] NajikaTraining09 existiert
)
echo.

echo ================================================================================
echo [CHECK 3/6] Details NajikaTraining10...
echo ================================================================================
schtasks /Query /TN "NajikaTraining10" /FO LIST /V 2>nul
if errorlevel 1 (
    echo [FEHLER] NajikaTraining10 nicht gefunden!
) else (
    echo [OK] NajikaTraining10 existiert
)
echo.

echo ================================================================================
echo [CHECK 4/6] Details NajikaTraining11...
echo ================================================================================
schtasks /Query /TN "NajikaTraining11" /FO LIST /V 2>nul
if errorlevel 1 (
    echo [FEHLER] NajikaTraining11 nicht gefunden!
) else (
    echo [OK] NajikaTraining11 existiert
)
echo.

echo ================================================================================
echo [CHECK 5/6] Details NajikaTraining12...
echo ================================================================================
schtasks /Query /TN "NajikaTraining12" /FO LIST /V 2>nul
if errorlevel 1 (
    echo [FEHLER] NajikaTraining12 nicht gefunden!
) else (
    echo [OK] NajikaTraining12 existiert
)
echo.

echo ================================================================================
echo [CHECK 6/6] Details NajikaTraining13...
echo ================================================================================
schtasks /Query /TN "NajikaTraining13" /FO LIST /V 2>nul
if errorlevel 1 (
    echo [FEHLER] NajikaTraining13 nicht gefunden!
) else (
    echo [OK] NajikaTraining13 existiert
)
echo.

echo ================================================================================
echo ZUSAMMENFASSUNG
echo ================================================================================
echo.

REM Zähle Tasks
set count=0
schtasks /Query /TN "NajikaTraining09" >nul 2>&1
if not errorlevel 1 set /a count+=1

schtasks /Query /TN "NajikaTraining10" >nul 2>&1
if not errorlevel 1 set /a count+=1

schtasks /Query /TN "NajikaTraining11" >nul 2>&1
if not errorlevel 1 set /a count+=1

schtasks /Query /TN "NajikaTraining12" >nul 2>&1
if not errorlevel 1 set /a count+=1

schtasks /Query /TN "NajikaTraining13" >nul 2>&1
if not errorlevel 1 set /a count+=1

echo Gefundene Tasks: %count% / 5
echo.

if %count%==5 (
    echo [SUCCESS] ALLE TASKS KORREKT EINGERICHTET!
    echo.
    echo Najika Training startet automatisch:
    echo   - Jeden Montag-Freitag
    echo   - Um 09:00, 10:00, 11:00, 12:00, 13:00 Uhr
    echo   - Laeuft bis 14:00 Uhr
    echo.
    echo Du musst NICHTS mehr tun!
    echo PC muss nur an sein Mo-Fr 09:00-14:00
) else (
    echo [WARNUNG] Nicht alle Tasks gefunden!
    echo.
    echo Bitte Setup nochmal ausfuehren:
    echo   Rechtsklick auf SETUP_AUTO_TRAINING.bat
    echo   "Als Administrator ausfuehren"
)

echo.
echo ================================================================================
echo NAECHSTE SCHRITTE
echo ================================================================================
echo.
echo 1. Task Scheduler oeffnen (optional):
echo    Win+R -^> taskschd.msc
echo.
echo 2. Progress anzeigen:
echo    python najika_show_progress.py
echo.
echo 3. Manuell testen (jetzt):
echo    START_NAJIKA_TRAINING.bat
echo.
pause
