@echo off
title NAJIKA INTENSIVE NIGHT TRAINING SETUP
color 0C

echo.
echo ========================================================================
echo              NAJIKA INTENSIVE NIGHT TRAINING SETUP
echo ========================================================================
echo.
echo Richtet 8-STUNDEN NACHT-TRAINING ein (00:00 - 08:00 Uhr)
echo.
echo WARNUNG: GPU wird VOLL ausgelastet!
echo          Rechner sollte diese Zeit nicht genutzt werden.
echo.
echo Ziel: Najika erreicht in 1 Monat Claude-Niveau!
echo.
pause

REM Check Admin-Rechte
net session >nul 2>&1
if %errorLevel% NEQ 0 (
    echo [FEHLER] Brauche Admin-Rechte!
    echo          Rechtsklick -^> Als Administrator ausfuehren
    pause
    exit /b 1
)

echo [1/2] Loesche alte Training-Tasks...

schtasks /delete /tn "NajikaTraining" /f >nul 2>&1
schtasks /delete /tn "NajikaCodeTraining" /f >nul 2>&1
schtasks /delete /tn "NajikaLoRATraining" /f >nul 2>&1

echo       [OK] Alte Tasks entfernt

echo [2/2] Erstelle INTENSIVE Night Training Task...
echo.

REM Task: Jeden Tag um 00:00 Uhr, 8 Stunden lang
schtasks /create /tn "NajikaIntensiveTraining" /tr "python C:\Najika-World\backend\najika_intensive_night_training.py" /sc daily /st 00:00 /ru "%USERNAME%" /rl HIGHEST /f

if %ERRORLEVEL% EQU 0 (
    echo       [OK] Intensive Training Task erstellt!
) else (
    echo       [FEHLER] Konnte Task nicht erstellen
    pause
    exit /b 1
)

echo.
echo ========================================================================
echo                    INTENSIVE TRAINING AKTIV!
echo ========================================================================
echo.
echo Najika trainiert jetzt JEDEN NACHT:
echo.
echo   Start:    00:00 Uhr
echo   Ende:     08:00 Uhr (automatisch)
echo   Dauer:    8 Stunden VOLLE GPU-Power!
echo.
echo TRAININGS-PHASEN:
echo   [00:00-02:00] Phase 1: LoRA Personality (4x 30min)
echo   [02:00-04:00] Phase 2: Code Training (8x 15min Katas)
echo   [04:00-06:00] Phase 3: Advanced Training (4x 30min)
echo   [06:00-08:00] Phase 4: Memory Enhancement (4x 30min)
echo.
echo ERGEBNIS:
echo   - Neue LoRA Checkpoints in lora_checkpoints/
echo   - Erweitertes Code-Wissen
echo   - Verbesserte ChromaDB Memory
echo   - Training-Log: backend/training_night_log.json
echo.
echo ZIEL: In 1 Monat Claude-Niveau erreichen! 🎓
echo.
echo Zum Verifizieren:
schtasks /query /tn "NajikaIntensiveTraining" /fo LIST | findstr "Task Name\|Next Run Time\|Status"
echo.
echo Zum Deaktivieren:
echo   schtasks /delete /tn "NajikaIntensiveTraining" /f
echo.
pause
