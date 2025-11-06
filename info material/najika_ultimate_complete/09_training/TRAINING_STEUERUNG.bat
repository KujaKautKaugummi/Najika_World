@echo off
REM ============================================
REM NAJIKA TRAINING STEUERUNG
REM Einfache Befehle zum Pausieren/Aktivieren
REM ============================================

echo.
echo =========================================
echo  NAJIKA TRAINING STEUERUNG
echo =========================================
echo.
echo [1] Status anzeigen
echo [2] Tag-Training PAUSIEREN (8-15 Uhr)
echo [3] Tag-Training AKTIVIEREN
echo [4] Training JETZT starten (manuell)
echo [5] Beenden
echo.

set /p choice="Wahl (1-5): "

if "%choice%"=="1" (
    python C:\Najika\backend\najika_smart_training_scheduler.py --status
    pause
    goto :eof
)

if "%choice%"=="2" (
    echo.
    echo Pausiere Tag-Training (08:00-15:00, Mo-Fr)...
    python C:\Najika\backend\najika_smart_training_scheduler.py --pause
    pause
    goto :eof
)

if "%choice%"=="3" (
    echo.
    echo Aktiviere Tag-Training wieder...
    python C:\Najika\backend\najika_smart_training_scheduler.py --resume
    pause
    goto :eof
)

if "%choice%"=="4" (
    echo.
    echo Starte Training manuell...
    python C:\Najika\backend\najika_smart_training_scheduler.py --train
    pause
    goto :eof
)

if "%choice%"=="5" (
    exit
)

echo Ungueltige Wahl!
pause
