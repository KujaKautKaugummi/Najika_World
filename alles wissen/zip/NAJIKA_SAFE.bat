@echo off
setlocal enabledelayedexpansion

echo ==============================================================
echo     NAJIKA SAFE SEARCH - Sichere 2-Stufen Analyse
echo ==============================================================
echo.

set "SEARCH_DIR=%~dp0"
set "STAGE1=%~dp0NAJIKA_STAGE1_SUMMARIES.txt"
set "STAGE2=%~dp0NAJIKA_STAGE2_DETAILED.txt"

echo Ordner: %SEARCH_DIR%
echo.

REM ======================================================================
REM STUFE 1: FINDE DATEIEN MIT ZUSAMMENFASSUNGEN
REM ======================================================================

echo [STUFE 1] Suche Zusammenfassungs-Dateien...
echo.

(
echo ########## STAGE_1_SUMMARY_FILES ##########
echo CREATED: %date% %time%
echo.
) > "%STAGE1%"

set /a SUMMARY_FILES=0

for /R "%SEARCH_DIR%" %%F in (*.txt *.md) do (

    REM Nur Dateien unter 1 MB
    set "SIZE=%%~zF"
    if !SIZE! LSS 1048576 (

        REM Suche nach Zusammenfassungs-Markern (sicher mit findstr)
        findstr /I /M /C:"zusammenfassung" /C:"summary" /C:"overview" /C:"konzept" "%%F" >nul 2>&1

        if !errorlevel! EQU 0 (
            set /a SUMMARY_FILES+=1
            echo [FOUND] %%~nxF

            (
                echo.
                echo FILE_WITH_SUMMARY: %%~nxF
                echo PATH: %%F
                echo SIZE: !SIZE!
                echo.
            ) >> "%STAGE1%"
        )
    )
)

(
    echo.
    echo TOTAL_SUMMARY_FILES: %SUMMARY_FILES%
    echo.
) >> "%STAGE1%"

echo Gefunden: %SUMMARY_FILES% Dateien mit Zusammenfassungen
echo.

REM ======================================================================
REM STUFE 2: SUCHE RELEVANTE DATEIEN MIT CORE KEYWORDS
REM ======================================================================

echo [STUFE 2] Suche relevante Dateien...
echo.

(
echo ########## STAGE_2_RELEVANT_FILES ##########
echo.
echo FILTER:
echo   - Core Keywords: najika, kuja, opus
echo   - Feature Keywords: explosion, crafting, digivice, wizard
echo   - Max Size: 500 KB
echo.
) > "%STAGE2%"

set /a TOTAL=0
set /a RELEVANT=0

for /R "%SEARCH_DIR%" %%F in (*.txt *.md *.py *.js *.json) do (
    set /a TOTAL+=1

    REM Filter: Max 500 KB
    set "SIZE=%%~zF"
    if !SIZE! LSS 512000 (

        REM Pruefe Core Keywords
        findstr /I /M /C:"najika" "%%F" >nul 2>&1
        if !errorlevel! EQU 0 (

            REM Zaehle weitere Keywords
            set /a SCORE=1

            findstr /I /M /C:"kuja" "%%F" >nul 2>&1
            if !errorlevel! EQU 0 set /a SCORE+=1

            findstr /I /M /C:"opus" "%%F" >nul 2>&1
            if !errorlevel! EQU 0 set /a SCORE+=1

            findstr /I /M /C:"wizard" "%%F" >nul 2>&1
            if !errorlevel! EQU 0 set /a SCORE+=1

            findstr /I /M /C:"explosion" "%%F" >nul 2>&1
            if !errorlevel! EQU 0 set /a SCORE+=1

            findstr /I /M /C:"crafting" "%%F" >nul 2>&1
            if !errorlevel! EQU 0 set /a SCORE+=1

            findstr /I /M /C:"digivice" "%%F" >nul 2>&1
            if !errorlevel! EQU 0 set /a SCORE+=1

            REM Nur wenn Score >= 2 (mindestens najika + 1 weiteres)
            if !SCORE! GEQ 2 (
                set /a RELEVANT+=1
                echo [RELEVANT] %%~nxF ^(Score: !SCORE!^)

                (
                    echo.
                    echo ########## RELEVANT_FILE ##########
                    echo NAME: %%~nxF
                    echo PATH: %%F
                    echo SIZE: !SIZE!
                    echo SCORE: !SCORE!
                    echo.
                    echo KATEGORIE:
                ) >> "%STAGE2%"

                REM Erkenne Kategorie
                echo %%~nxF | findstr /I /C:"neu" >nul 2>&1
                if !errorlevel! EQU 0 (
                    echo   KATEGORIE: NEU_1_DOKUMENT ^(PRIORITAET: HOECHSTE^) >> "%STAGE2%"
                )

                echo %%~nxF | findstr /I /C:"opus" >nul 2>&1
                if !errorlevel! EQU 0 (
                    echo   KATEGORIE: OPUS_CODE ^(PRIORITAET: HOCH^) >> "%STAGE2%"
                )

                echo %%~nxF | findstr /I /C:"zusammenfassung" /C:"summary" >nul 2>&1
                if !errorlevel! EQU 0 (
                    echo   KATEGORIE: ZUSAMMENFASSUNG ^(PRIORITAET: HOCH^) >> "%STAGE2%"
                )

                echo ########## END_FILE ########## >> "%STAGE2%"
            )
        )
    )

    REM Progress
    set /a MOD=!TOTAL! %% 50
    if !MOD! EQU 0 (
        echo ... !TOTAL! geprueft
    )
)

(
    echo.
    echo ########## SUMMARY ##########
    echo TOTAL_CHECKED: %TOTAL%
    echo RELEVANT_FOUND: %RELEVANT%
    echo ########## END ##########
) >> "%STAGE2%"

echo.
echo ==============================================================
echo ANALYSE ABGESCHLOSSEN
echo ==============================================================
echo.
echo STUFE 1: %SUMMARY_FILES% Zusammenfassungs-Dateien
echo STUFE 2: %RELEVANT% relevante Dateien
echo          (von %TOTAL% geprueft)
echo.
echo ==============================================================
echo.
echo Reports erstellt:
echo   1. %STAGE1%
echo   2. %STAGE2%
echo.

if exist "%STAGE1%" (
    echo Oeffne Stufe 1 Report...
    start notepad "%STAGE1%"
    timeout /t 2 /nobreak >nul
)

if exist "%STAGE2%" (
    echo Oeffne Stufe 2 Report...
    start notepad "%STAGE2%"
)

echo.
echo ==============================================================
echo Druecke eine Taste...
echo ==============================================================
pause
