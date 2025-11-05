@echo off
setlocal enabledelayedexpansion

echo ==============================================================
echo     NAJIKA SMART SEARCH - FINALE VERSION
echo ==============================================================
echo.
echo Script startet...
echo.

REM Setze Variablen
set "SEARCH_DIR=%~dp0"
set "OUTPUT=%~dp0NAJIKA_RESULT.txt"

echo Ordner: %SEARCH_DIR%
echo Output: %OUTPUT%
echo.

REM Pruefe ob Ordner existiert
if not exist "%SEARCH_DIR%" (
    echo FEHLER: Ordner existiert nicht!
    pause
    exit /b 1
)

echo ==============================================================
echo.
echo Starte Suche...
echo.

REM Erstelle Report Header
(
echo ########## NAJIKA_SEARCH_REPORT ##########
echo TIMESTAMP: %date% %time%
echo DIRECTORY: %SEARCH_DIR%
echo.
) > "%OUTPUT%"

REM Zaehler
set /a TOTAL=0
set /a FOUND=0
set /a SKIPPED=0

echo [PHASE 1] Suche nach relevanten Dateien...
echo.

REM Suche nur wichtige Keywords
for /R "%SEARCH_DIR%" %%F in (*.txt *.md *.py *.js) do (
    set /a TOTAL+=1

    REM Ueberspringen wenn zu gross (>500KB)
    set "SIZE=%%~zF"
    if !SIZE! LSS 512000 (

        REM Pruefe auf wichtige Keywords
        findstr /I /C:"najika" /C:"kuja" /C:"opus" /C:"wizard" /C:"explosion" /C:"crafting" /C:"digivice" "%%F" >nul 2>&1

        if !errorlevel! EQU 0 (
            set /a FOUND+=1
            echo [MATCH] %%~nxF

            (
                echo.
                echo ########## FILE_START ##########
                echo NAME: %%~nxF
                echo PATH: %%F
                echo SIZE: !SIZE!
                echo ########## FILE_END ##########
            ) >> "%OUTPUT%"
        )
    ) else (
        set /a SKIPPED+=1
    )

    REM Progress
    set /a MOD=!TOTAL! %% 20
    if !MOD! EQU 0 (
        echo ... !TOTAL! Dateien geprueft
    )
)

echo.
echo Suche abgeschlossen!
echo.

REM Schreibe Zusammenfassung
(
    echo.
    echo ########## SUMMARY ##########
    echo TOTAL_CHECKED: %TOTAL%
    echo MATCHES_FOUND: %FOUND%
    echo SKIPPED_LARGE: %SKIPPED%
    echo ########## END ##########
) >> "%OUTPUT%"

echo ==============================================================
echo ERGEBNIS:
echo ==============================================================
echo   Geprueft:  %TOTAL%
echo   Gefunden:  %FOUND%
echo   Zu gross:  %SKIPPED%
echo ==============================================================
echo.

REM Pruefe ob Report erstellt wurde
if exist "%OUTPUT%" (
    echo Report erfolgreich erstellt!
    echo.
    echo Oeffne Report...
    start notepad "%OUTPUT%"
) else (
    echo FEHLER: Report nicht erstellt!
)

echo.
echo ==============================================================
echo FERTIG! Druecke eine Taste zum Schliessen...
echo ==============================================================
pause
