@echo off
title NAJIKA QUICK TEST
color 0B

echo.
echo ================================================================================
echo                         NAJIKA QUICK SYSTEM TEST
echo ================================================================================
echo.

REM Test 1: LM Studio
echo [1/5] Testing LM Studio...
curl -s http://localhost:1234/v1/models >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo       [OK] LM Studio laeuft
) else (
    echo       [FAIL] LM Studio laeuft NICHT!
)

REM Test 2: Backend
echo [2/5] Testing Backend...
curl -s http://localhost:8000/api/health >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo       [OK] Backend laeuft
) else (
    echo       [FAIL] Backend laeuft NICHT!
    echo       Starte Backend mit: START_NAJIKA.bat
)

REM Test 3: Najika Status
echo [3/5] Testing Najika Status API...
curl -s http://localhost:8000/api/najika/status >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo       [OK] Najika Status API funktioniert
) else (
    echo       [FAIL] Najika Status API nicht erreichbar
)

REM Test 4: UI Files
echo [4/5] Testing UI Files...
curl -s http://localhost:8000/digivice/najika_world_UNIFIED.html >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo       [OK] UI Files erreichbar
) else (
    echo       [FAIL] UI Files nicht erreichbar
)

REM Test 5: Slime Arena API
echo [5/5] Testing Slime Arena API...
curl -s http://localhost:8000/api/slime-arena/leaderboard >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo       [OK] Slime Arena API funktioniert
) else (
    echo       [FAIL] Slime Arena API nicht erreichbar
)

echo.
echo ================================================================================
echo                              TEST COMPLETE
echo ================================================================================
echo.
echo Wenn Tests fehlschlagen:
echo 1. Starte Backend: START_NAJIKA.bat
echo 2. Starte LM Studio manuell
echo 3. Fuehre Test erneut aus
echo.
pause
