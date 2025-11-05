@echo off
title NAJIKA TRAINING - JETZT
color 0E

echo.
echo ========================================================================
echo                      NAJIKA TRAINING - SOFORT
echo ========================================================================
echo.
echo Fuehrt alle Trainings-Systeme JETZT aus
echo.
pause

cd /d "C:\Najika-World\backend"

echo [1/3] Persoenlichkeits-Training...
python najika_complete_training_session.py
if %ERRORLEVEL% EQU 0 (
    echo       [OK] Persoenlichkeits-Training abgeschlossen
) else (
    echo       [FEHLER] Persoenlichkeits-Training fehlgeschlagen
)
echo.

echo [2/3] Code-Training...
python najika_code_training_real.py
if %ERRORLEVEL% EQU 0 (
    echo       [OK] Code-Training abgeschlossen
) else (
    echo       [FEHLER] Code-Training fehlgeschlagen
)
echo.

echo [3/3] LoRA-Training...
python najika_lora_training_3b.py
if %ERRORLEVEL% EQU 0 (
    echo       [OK] LoRA-Training abgeschlossen
) else (
    echo       [FEHLER] LoRA-Training fehlgeschlagen
)
echo.

echo ========================================================================
echo                      TRAINING ABGESCHLOSSEN!
echo ========================================================================
echo.
echo Check Ergebnisse:
echo   - lora_checkpoints/     (neue Checkpoints)
echo   - code_training_progress.json
echo   - chroma_db/            (erweiterte Memory)
echo.
pause
