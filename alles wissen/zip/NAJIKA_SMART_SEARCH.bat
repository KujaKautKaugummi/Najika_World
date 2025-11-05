@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ==============================================================
echo     NAJIKA SMART SEARCH - INTELLIGENTE FILTERUNG
echo ==============================================================
echo.

set "SEARCH_DIR=%~dp0"
set "OUTPUT=NAJIKA_SMART_%date:~-4%%date:~-7,2%%date:~-10,2%_%time:~0,2%%time:~3,2%%time:~6,2%.txt"
set "OUTPUT=%OUTPUT: =0%"

echo Durchsuche: %SEARCH_DIR%
echo Report: %OUTPUT%
echo.

REM ====== INTELLIGENTE FILTER ======

REM 1. PRIORITAETS-KEYWORDS (müssen vorhanden sein)
set "PRIO_HIGH=najika kuja opus wizard neu-1"

REM 2. FEATURE-KEYWORDS (Gameplay-Features)
set "FEATURES=explosion weaving crafting fishing farming digimon-world oregon-trail fortnite"

REM 3. TECHNISCHE KEYWORDS
set "TECH=digivice muehle gesichert kaykit uefn three.js"

REM 4. DATEITYP-FILTER (nur wichtige Dateien)
set "EXTENSIONS=*.txt *.md *.py *.js"

REM 5. GROESSEN-LIMIT (Dateien > 500 KB überspringen)
set "MAX_SIZE=512000"

echo [FILTER AKTIV]
echo   - Nur Dateien mit Prioritaets-Keywords
echo   - Dateigroesse max. 500 KB
echo   - Nur TXT, MD, PY, JS
echo   - Relevanz-Scoring
echo.
echo ==============================================================
echo.

set /a TOTAL_FILES=0
set /a SKIPPED_LARGE=0
set /a SKIPPED_IRRELEVANT=0
set /a FOUND_FILES=0

REM Report Header
(
echo ==============================================================
echo    NAJIKA SMART SEARCH - FILTERED REPORT
echo ==============================================================
echo Erstellt: %date% %time%
echo.
echo FILTER:
echo   - Max. Dateigroesse: 500 KB
echo   - Nur relevante Dateitypen
echo   - Prioritaets-Keywords erforderlich
echo.
echo ==============================================================
echo.
) > "%OUTPUT%"

echo [PHASE 1] Schnelle Vorpruefung...
echo.

REM Hauptsuche mit intelligentem Filter
for /R "%SEARCH_DIR%" %%F in (%EXTENSIONS%) do (
    set /a TOTAL_FILES+=1
    set "FILE=%%F"
    set "SIZE=%%~zF"

    REM Filter 1: Dateigröße
    if !SIZE! GTR %MAX_SIZE% (
        set /a SKIPPED_LARGE+=1
        if !TOTAL_FILES! LEQ 100 (
            echo   [SKIP] %%~nxF ^(zu gross: !SIZE! bytes^)
        )
    ) else (
        REM Filter 2: Muss mindestens 1 Prioritäts-Keyword enthalten
        set "HAS_PRIO=0"

        for %%K in (%PRIO_HIGH%) do (
            findstr /I /C:"%%K" "%%F" >nul 2>&1
            if !errorlevel! EQU 0 (
                set "HAS_PRIO=1"
            )
        )

        if !HAS_PRIO! EQU 1 (
            set /a FOUND_FILES+=1

            echo [TREFFER] %%~nxF ^(!SIZE! bytes^)

            REM Berechne Relevanz-Score
            set /a SCORE=0

            (
                echo.
                echo ########## START_FILE ##########
                echo FILE_NAME: %%~nxF
                echo FILE_PATH: %%F
                echo FILE_SIZE: !SIZE!
                echo FILE_TYPE: %%~xF
                echo.
                echo KEYWORDS_FOUND:
            ) >> "%OUTPUT%"

            REM Prüfe alle wichtigen Keywords
            for %%K in (%PRIO_HIGH% %FEATURES% %TECH%) do (
                findstr /I /C:"%%K" "%%F" >nul 2>&1
                if !errorlevel! EQU 0 (
                    set /a SCORE+=1
                    echo   [+] %%K
                    echo KEYWORD: %%K >> "%OUTPUT%"
                )
            )

            (
                echo.
                echo RELEVANCE_SCORE: !SCORE!/20
                echo.
            ) >> "%OUTPUT%"

            REM Nur Top-Matches detailliert ausgeben
            if !SCORE! GEQ 5 (
                echo   ^> HIGH RELEVANCE ^(Score: !SCORE!^)
                (
                    echo.
                    echo CONTENT_SAMPLE_START:
                    echo --- First 20 lines ---
                    echo.
                ) >> "%OUTPUT%"

                REM Zeige nur erste 20 Zeilen als Sample
                set /a LINE_COUNT=0
                for /F "usebackq delims=" %%L in ("%%F") do (
                    set /a LINE_COUNT+=1
                    if !LINE_COUNT! LEQ 20 (
                        echo %%L >> "%OUTPUT%"
                    )
                )

                (
                    echo.
                    echo CONTENT_SAMPLE_END
                    echo NOTE: Full file at FILE_PATH above
                    echo.
                ) >> "%OUTPUT%"
            )

            echo ########## END_FILE ########## >> "%OUTPUT%"
            echo. >> "%OUTPUT%"

        ) else (
            set /a SKIPPED_IRRELEVANT+=1
        )
    )

    REM Progress alle 50 Dateien
    set /a MOD=!TOTAL_FILES! %% 50
    if !MOD! EQU 0 (
        echo   [Progress] !TOTAL_FILES! durchsucht, !FOUND_FILES! relevant
    )
)

echo.
echo [PHASE 2] Spezielle Dateien...
echo.

REM Suche speziell nach wichtigen Dateien
set /a SPECIAL_FOUND=0

(
    echo.
    echo ########## SPECIAL_FILES_START ##########
    echo.
) >> "%OUTPUT%"

REM neu 1 Datei
for /R "%SEARCH_DIR%" %%F in (*neu*1*.txt *neu*1*.md) do (
    if exist "%%F" (
        set /a SPECIAL_FOUND+=1
        echo   [SPECIAL] %%~nxF
        (
            echo SPECIAL_TYPE: NEU_1_DOCUMENT
            echo FILE_NAME: %%~nxF
            echo FILE_PATH: %%F
            echo PRIORITY: HIGHEST
            echo.
        ) >> "%OUTPUT%"
    )
)

REM Opus Dateien
for /R "%SEARCH_DIR%" %%F in (*opus*.txt *opus*.py *opus*.md) do (
    if exist "%%F" (
        set /a SPECIAL_FOUND+=1
        echo   [SPECIAL] %%~nxF
        (
            echo SPECIAL_TYPE: OPUS_CODE
            echo FILE_NAME: %%~nxF
            echo FILE_PATH: %%F
            echo PRIORITY: HIGH
            echo.
        ) >> "%OUTPUT%"
    )
)

echo ########## SPECIAL_FILES_END ########## >> "%OUTPUT%"
echo. >> "%OUTPUT%"

REM PDFs (nur auflisten, nicht durchsuchen)
echo.
echo [INFO] PDFs gefunden:
echo.

set /a PDF_COUNT=0
for /R "%SEARCH_DIR%" %%F in (*.pdf) do (
    set /a PDF_COUNT+=1
    if !PDF_COUNT! LEQ 10 (
        echo   [PDF] %%~nxF ^(%%~zF bytes^)
    )
)

if !PDF_COUNT! GTR 10 (
    echo   ... und !PDF_COUNT! weitere PDFs
)

REM Zusammenfassung
(
    echo.
    echo ==============================================================
    echo ZUSAMMENFASSUNG
    echo ==============================================================
    echo.
    echo Gesamt durchsucht:         %TOTAL_FILES%
    echo.
    echo GEFILTERT:
    echo   - Zu gross ^(^>500KB^):      %SKIPPED_LARGE%
    echo   - Nicht relevant:         %SKIPPED_IRRELEVANT%
    echo.
    echo GEFUNDEN:
    echo   - Relevante Dateien:      %FOUND_FILES%
    echo   - Spezielle Dateien:      %SPECIAL_FOUND%
    echo   - PDFs:                   %PDF_COUNT%
    echo.
    echo HINWEIS:
    echo Nur hochrelevante Matches wurden detailliert ausgegeben.
    echo Vollstaendige Pfade sind im Report.
    echo.
    echo ==============================================================
    echo.
) >> "%OUTPUT%"

echo.
echo ==============================================================
echo                  SUCHE ABGESCHLOSSEN
echo ==============================================================
echo   Gesamt durchsucht:     %TOTAL_FILES%
echo   Gefiltert ^(zu gross^):  %SKIPPED_LARGE%
echo   Gefiltert ^(irrelevant^): %SKIPPED_IRRELEVANT%
echo   Relevante Treffer:     %FOUND_FILES%
echo   Spezielle Dateien:     %SPECIAL_FOUND%
echo ==============================================================
echo.
echo Report: %OUTPUT%
echo.

if exist "%OUTPUT%" (
    echo Report erfolgreich erstellt!

    REM Zeige Dateigröße
    for %%A in ("%OUTPUT%") do (
        set "REPORT_SIZE=%%~zA"
        set /a REPORT_KB=!REPORT_SIZE! / 1024
        echo Report-Groesse: !REPORT_KB! KB ^(!REPORT_SIZE! bytes^)
    )

    echo.
    echo Oeffne Report in Notepad...
    start notepad "%OUTPUT%"
) else (
    echo FEHLER: Report wurde nicht erstellt!
)

echo.
echo Druecke eine Taste zum Schliessen...
pause
