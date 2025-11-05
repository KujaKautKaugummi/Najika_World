@echo off
echo ========================================
echo NAJIKA CODE TRAINING TASK ERSTELLEN
echo ========================================
echo.

REM Alte Task loeschen falls vorhanden
schtasks /delete /tn "NajikaCodeTraining" /f >nul 2>&1

REM Neue Task erstellen: Taeglich 08:00 Uhr, 12h Dauer
schtasks /create /tn "NajikaCodeTraining" /tr "python C:\NajikaFinal\backend\najika_daily_training.py" /sc daily /st 08:00 /du 12:00 /f

echo.
echo [OK] Task "NajikaCodeTraining" erstellt!
echo      Start: 08:00 Uhr taeglich
echo      Dauer: 12 Stunden (bis 20:00 Uhr)
echo.
pause
