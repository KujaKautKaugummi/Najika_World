@echo off
title NAJIKA AUTO-TRAINING SETUP
color 0B

echo.
echo ========================================================================
echo                   NAJIKA AUTO-TRAINING SETUP
echo ========================================================================
echo.
echo Richtet automatisches naechtiches Training ein (23:00 Uhr)
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

echo [1/4] Erstelle Training Task...

REM Loesche alten Task falls vorhanden
schtasks /delete /tn "NajikaTraining" /f >nul 2>&1

REM Erstelle neuen Task - taeglich um 23:00 Uhr
schtasks /create /tn "NajikaTraining" /tr "python C:\Najika-World\backend\najika_complete_training_session.py" /sc daily /st 23:00 /ru "%USERNAME%" /f

if %ERRORLEVEL% EQU 0 (
    echo       [OK] Task erstellt
) else (
    echo       [FEHLER] Konnte Task nicht erstellen
    pause
    exit /b 1
)

echo [2/4] Erstelle Code-Training Task...

schtasks /create /tn "NajikaCodeTraining" /tr "python C:\Najika-World\backend\najika_code_training_real.py" /sc daily /st 23:30 /ru "%USERNAME%" /f

if %ERRORLEVEL% EQU 0 (
    echo       [OK] Code-Training Task erstellt
) else (
    echo       [FEHLER] Konnte Task nicht erstellen
)

echo [3/4] Erstelle LoRA-Training Task (alle 2 Tage)...

schtasks /create /tn "NajikaLoRATraining" /tr "python C:\Najika-World\backend\najika_lora_training_3b.py" /sc daily /mo 2 /st 00:00 /ru "%USERNAME%" /f

if %ERRORLEVEL% EQU 0 (
    echo       [OK] LoRA-Training Task erstellt
) else (
    echo       [FEHLER] Konnte Task nicht erstellen
)

echo [4/4] Verifiziere Tasks...
echo.

schtasks /query /tn "NajikaTraining" /fo LIST | findstr "Task Name\|Next Run Time\|Status"
echo.
schtasks /query /tn "NajikaCodeTraining" /fo LIST | findstr "Task Name\|Next Run Time\|Status"
echo.
schtasks /query /tn "NajikaLoRATraining" /fo LIST | findstr "Task Name\|Next Run Time\|Status"

echo.
echo ========================================================================
echo                      SETUP ERFOLGREICH!
echo ========================================================================
echo.
echo Najika trainiert jetzt automatisch:
echo   - 23:00 Uhr: Persoenlichkeits-Training
echo   - 23:30 Uhr: Code-Training
echo   - 00:00 Uhr: LoRA-Training (alle 2 Tage)
echo.
echo Zum Deaktivieren:
echo   schtasks /delete /tn "NajikaTraining" /f
echo   schtasks /delete /tn "NajikaCodeTraining" /f
echo   schtasks /delete /tn "NajikaLoRATraining" /f
echo.
pause
