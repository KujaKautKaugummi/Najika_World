@echo off
setlocal enabledelayedexpansion

echo ==============================================================
echo     NAJIKA INTELLIGENT SEARCH - 2-STUFEN ANALYSE
echo ==============================================================
echo.
echo STUFE 1: Finde bestehende Zusammenfassungen
echo STUFE 2: Basierend darauf intensive Suche
echo.

set "SEARCH_DIR=%~dp0"
set "SUMMARY_FILE=%~dp0NAJIKA_SUMMARIES.txt"
set "FINAL_FILE=%~dp0NAJIKA_INTELLIGENT_REPORT.txt"

echo Ordner: %SEARCH_DIR%
echo.
echo ==============================================================
echo.

REM ======================================================================
REM STUFE 1: FINDE ZUSAMMENFASSUNGEN
REM ======================================================================

echo [STUFE 1] Suche nach Zusammenfassungen...
echo.

(
echo ########## NAJIKA_INTELLIGENT_ANALYSIS ##########
echo CREATED: %date% %time%
echo.
echo ########## PHASE_1_SUMMARIES ##########
echo.
) > "%SUMMARY_FILE%"

set /a SUMMARY_COUNT=0

REM Suche nach Zusammenfassungs-Markern
for /R "%SEARCH_DIR%" %%F in (*.txt *.md) do (

    REM Suche nach typischen Zusammenfassungs-Schluesselwoertern
    findstr /I /C:"zusammenfassung" /C:"summary" /C:"overview" /C:"konzept" /C:"grundidee" /C:"basis" "%%F" >nul 2>&1

    if !errorlevel! EQU 0 (
        set /a SUMMARY_COUNT+=1
        echo [FOUND] Zusammenfassung in: %%~nxF

        (
            echo.
            echo === SUMMARY_SOURCE: %%~nxF ===
            echo PATH: %%F
            echo.
        ) >> "%SUMMARY_FILE%"

        REM Extrahiere Zusammenfassungs-Abschnitte (erste 50 Zeilen nach Marker)
        set /a LINE_NUM=0
        set /a EXTRACT=0
        set /a EXTRACTED=0

        for /F "usebackq delims=" %%L in ("%%F") do (
            set /a LINE_NUM+=1
            set "LINE=%%L"

            REM Pruefe ob Zusammenfassungs-Abschnitt beginnt
            echo !LINE! | findstr /I /C:"zusammenfassung" /C:"summary" /C:"overview" >nul 2>&1
            if !errorlevel! EQU 0 (
                set /a EXTRACT=1
                set /a EXTRACTED=0
            )

            REM Extrahiere wenn im Modus
            if !EXTRACT! EQU 1 (
                if !EXTRACTED! LSS 50 (
                    echo %%L >> "%SUMMARY_FILE%"
                    set /a EXTRACTED+=1
                ) else (
                    set /a EXTRACT=0
                )
            )
        )

        echo. >> "%SUMMARY_FILE%"
        echo --- END_SUMMARY --- >> "%SUMMARY_FILE%"
        echo. >> "%SUMMARY_FILE%"
    )
)

echo.
echo Gefunden: %SUMMARY_COUNT% Zusammenfassungen
echo.

REM ======================================================================
REM STUFE 2: INTELLIGENTE KEYWORD-EXTRAKTION
REM ======================================================================

echo [STUFE 2] Analysiere Zusammenfassungen...
echo.

REM Baue intelligente Keyword-Liste aus den Zusammenfassungen
set "SMART_KEYWORDS="

REM Basis-Keywords (immer wichtig)
set "CORE=najika kuja opus"

REM Suche in Zusammenfassungen nach haeufigen wichtigen Begriffen
for %%K in (explosion crafting fishing farming digivice muehle wizard training skill weaving fortnite uefn kaykit memory bond lernsystem 8-staedte file-island oregon-trail digimon-world) do (
    findstr /I /C:"%%K" "%SUMMARY_FILE%" >nul 2>&1
    if !errorlevel! EQU 0 (
        set "SMART_KEYWORDS=!SMART_KEYWORDS! %%K"
        echo   [RELEVANT] %%K gefunden in Zusammenfassungen
    )
)

echo.
echo Intelligente Keywords: %CORE% !SMART_KEYWORDS!
echo.

REM ======================================================================
REM STUFE 3: INTENSIVE SUCHE MIT SMART KEYWORDS
REM ======================================================================

echo [STUFE 3] Intensive Suche basierend auf Analyse...
echo.

(
    echo.
    echo ########## PHASE_2_DETAILED_SEARCH ##########
    echo BASED_ON: %SUMMARY_COUNT% summaries analyzed
    echo SMART_KEYWORDS: %CORE% !SMART_KEYWORDS!
    echo.
) > "%FINAL_FILE%"

set /a TOTAL=0
set /a RELEVANT=0

for /R "%SEARCH_DIR%" %%F in (*.txt *.md *.py *.js *.json) do (
    set /a TOTAL+=1

    REM Ueberspringen wenn zu gross
    set "SIZE=%%~zF"
    if !SIZE! LSS 512000 (

        REM Pruefe auf Core Keywords
        findstr /I /C:"najika" /C:"kuja" /C:"opus" "%%F" >nul 2>&1

        if !errorlevel! EQU 0 (

            REM Zaehle Smart Keywords
            set /a MATCH_COUNT=0
            set "MATCHED_KEYWORDS="

            for %%K in (%CORE% !SMART_KEYWORDS!) do (
                findstr /I /C:"%%K" "%%F" >nul 2>&1
                if !errorlevel! EQU 0 (
                    set /a MATCH_COUNT+=1
                    set "MATCHED_KEYWORDS=!MATCHED_KEYWORDS! %%K"
                )
            )

            REM Nur hochrelevante Dateien (mind. 3 Matches)
            if !MATCH_COUNT! GEQ 3 (
                set /a RELEVANT+=1
                echo [RELEVANT] %%~nxF ^(!MATCH_COUNT! keywords^)

                (
                    echo.
                    echo ########## RELEVANT_FILE ##########
                    echo NAME: %%~nxF
                    echo PATH: %%F
                    echo SIZE: !SIZE! bytes
                    echo RELEVANCE: !MATCH_COUNT! keywords
                    echo KEYWORDS: !MATCHED_KEYWORDS!
                    echo.
                    echo CONTENT_TYPE:
                ) >> "%FINAL_FILE%"

                REM Erkenne Content-Typ
                echo %%~nxF | findstr /I /C:"neu" /C:"1" >nul 2>&1
                if !errorlevel! EQU 0 (
                    echo   TYPE: NEU_1_BASIS_DOCUMENT ^(PRIORITY: HIGHEST^) >> "%FINAL_FILE%"
                )

                echo %%~nxF | findstr /I /C:"opus" >nul 2>&1
                if !errorlevel! EQU 0 (
                    echo   TYPE: OPUS_CODE ^(PRIORITY: HIGH^) >> "%FINAL_FILE%"
                )

                echo %%~nxF | findstr /I /C:"zusammenfassung" /C:"summary" >nul 2>&1
                if !errorlevel! EQU 0 (
                    echo   TYPE: SUMMARY_DOCUMENT ^(PRIORITY: HIGH^) >> "%FINAL_FILE%"
                )

                REM Extrahiere relevante Abschnitte (erste 30 Zeilen)
                (
                    echo.
                    echo CONTENT_SAMPLE:
                    echo --- First 30 lines ---
                ) >> "%FINAL_FILE%"

                set /a LINE_COUNT=0
                for /F "usebackq delims=" %%L in ("%%F") do (
                    set /a LINE_COUNT+=1
                    if !LINE_COUNT! LEQ 30 (
                        echo %%L >> "%FINAL_FILE%"
                    )
                )

                (
                    echo --- End sample ---
                    echo.
                    echo ########## END_FILE ##########
                    echo.
                ) >> "%FINAL_FILE%"
            )
        )
    )

    REM Progress
    set /a MOD=!TOTAL! %% 20
    if !MOD! EQU 0 (
        echo ... !TOTAL! Dateien geprueft
    )
)

REM ======================================================================
REM ZUSAMMENFASSUNG
REM ======================================================================

(
    echo.
    echo ########## FINAL_SUMMARY ##########
    echo.
    echo STUFE_1_SUMMARIES: %SUMMARY_COUNT% gefunden
    echo STUFE_2_SMART_KEYWORDS: %CORE% !SMART_KEYWORDS!
    echo STUFE_3_TOTAL_CHECKED: %TOTAL%
    echo STUFE_3_RELEVANT_FOUND: %RELEVANT%
    echo.
    echo EMPFEHLUNG:
    echo 1. Lies zuerst die Zusammenfassungen in: %SUMMARY_FILE%
    echo 2. Dann die relevanten Details in dieser Datei
    echo.
    echo ########## END_REPORT ##########
) >> "%FINAL_FILE%"

echo.
echo ==============================================================
echo ANALYSE ABGESCHLOSSEN
echo ==============================================================
echo.
echo STUFE 1: %SUMMARY_COUNT% Zusammenfassungen gefunden
echo STUFE 2: Intelligente Keywords extrahiert
echo STUFE 3: %RELEVANT% hochrelevante Dateien gefunden
echo          (von %TOTAL% geprueft)
echo.
echo ==============================================================
echo.
echo Reports erstellt:
echo   1. %SUMMARY_FILE%
echo   2. %FINAL_FILE%
echo.

if exist "%SUMMARY_FILE%" (
    echo Oeffne Zusammenfassungs-Report...
    start notepad "%SUMMARY_FILE%"
    timeout /t 2 /nobreak >nul
)

if exist "%FINAL_FILE%" (
    echo Oeffne Detail-Report...
    start notepad "%FINAL_FILE%"
)

echo.
echo ==============================================================
echo FERTIG! Druecke eine Taste...
echo ==============================================================
pause
