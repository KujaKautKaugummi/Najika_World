@echo off
title NAJIKA TRAINING
color 0C
cd /d "%~dp0"

cls
echo.
echo ========================================================================
echo                      NAJIKA TRAINING SYSTEM
echo ========================================================================
echo.
echo [INFO] Pruefe Ollama...
echo.

REM Pruefe ob Ollama laeuft
curl -s http://127.0.0.1:11434/api/tags >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [FEHLER] Ollama laeuft nicht!
    echo          Bitte starte Ollama zuerst.
    echo.
    pause
    exit /b 1
)
echo       [OK] Ollama laeuft!

echo.
echo ========================================================================
echo                    TRAINING-OPTIONEN
echo ========================================================================
echo.
echo   1. REAL TRAINING (Ollama mit echten Daten)
echo   2. AUTO TRAINING (Personality Videos)
echo   3. CODE TRAINING (Programming Tasks)
echo   4. STATUS anzeigen
echo   5. EXIT
echo.
echo ========================================================================
echo.

set /p choice="Waehle Option (1-5): "

if "%choice%"=="1" (
    echo.
    echo [START] NAJIKA REAL TRAINING...
    python NAJIKA_REAL_TRAINING.py
    goto end
)

if "%choice%"=="2" (
    echo.
    echo [START] NAJIKA AUTO TRAINING...
    python NAJIKA_AUTO_TRAINING.py
    goto end
)

if "%choice%"=="3" (
    echo.
    echo [START] NAJIKA CODE TRAINING...
    python najika_code_training_real.py
    goto end
)

if "%choice%"=="4" (
    echo.
    echo [STATUS] Pruefe Training-Daten...
    python -c "from pathlib import Path; td = Path('training_data_real'); print(f'Dateien: {len(list(td.rglob(\"*\") if td.exists() else []))}'); print(f'Groesse: {sum(f.stat().st_size for f in td.rglob(\"*\") if f.is_file() and td.exists()) / 1024**2:.0f} MB' if td.exists() else 'Keine Daten')"
    echo.
    pause
    goto start
)

if "%choice%"=="5" (
    echo.
    echo [EXIT] Tschuess!
    exit /b 0
)

echo.
echo [FEHLER] Ungueltige Wahl!
pause
goto start

:end
echo.
echo ========================================================================
echo                    TRAINING ABGESCHLOSSEN
echo ========================================================================
echo.
pause
