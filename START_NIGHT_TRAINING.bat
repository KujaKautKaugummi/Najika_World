@echo off
REM NAJIKA NIGHT TRAINING - Manuelle Aktivierung
REM Starte dieses Script wenn du schlafen gehst!

echo ================================================================================
echo NAJIKA INTENSIVE NIGHT TRAINING
echo ================================================================================
echo.
echo Dieses Training laeuft 8-10 Stunden (5 Phasen):
echo   Phase 1: LoRA Personality (2h)
echo   Phase 2: Code Training (2h)
echo   Phase 3: Advanced Training (2h)
echo   Phase 4: Memory Enhancement (2h)
echo   Phase 5: Project Knowledge - 258M Zeichen! (2h)
echo.
echo Training startet JETZT und laeuft bis fertig!
echo Du kannst PC anlassen und schlafen gehen.
echo.
echo Druecke eine Taste um Training zu starten...
pause >nul

cd /d "C:\Najika-World\backend"

echo.
echo [%TIME%] Training START!
echo.

python najika_intensive_night_training.py

echo.
echo [%TIME%] Training FERTIG!
echo.
echo Log gespeichert in: backend\training_night_log.json
echo.
pause
