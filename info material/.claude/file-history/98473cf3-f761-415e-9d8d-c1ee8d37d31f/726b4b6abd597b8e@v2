@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ==============================================================
echo     NAJIKA COMPLETE PROJECT SEARCH - SAUBERE VERSION
echo ==============================================================
echo.

set "SEARCH_DIR=%~dp0"
set "OUTPUT=NAJIKA_SEARCH_%date:~-4%%date:~-7,2%%date:~-10,2%_%time:~0,2%%time:~3,2%%time:~6,2%.txt"
set "OUTPUT=%OUTPUT: =0%"

echo Durchsuche: %SEARCH_DIR%
echo Report: %OUTPUT%
echo.
echo ==============================================================
echo.

REM Alle Keywords
set "KEYWORDS=najika kuja schwert schild kopf herz girlfriend daddy schlampe puddin megumin harley shiro melissa sakura digivice muehle windmuehle schwarze hollaendische gesichert gesicherter bereich explosion klasse skill weaving crafting fishing farming mining holzfaellen combat kampf oregon-trail digimon-world file-island 8-staedte fortnite sprint slide dash wall-climb vault parkour uefn kaykit three.js gltf glb fbx opus wizard kaetzchen private nsfw memory bond seelengefahrten assistant-mode training level xp use-based progression skill-tree talente hp mana stamina hunger durst muedigkeit magie zauber magieschule slime api endpoint def class function"

echo [PHASE 1] Durchsuche Text-Dateien...
echo.

set /a TOTAL_FILES=0
set /a FOUND_FILES=0

REM Report Header
(
echo ==============================================================
echo    NAJIKA COMPLETE PROJECT SEARCH REPORT
echo ==============================================================
echo Erstellt: %date% %time%
echo Verzeichnis: %SEARCH_DIR%
echo.
echo ==============================================================
echo.
) > "%OUTPUT%"

REM Hauptsuche
for /R "%SEARCH_DIR%" %%F in (*.txt *.md *.json *.jsonl *.py *.js *.html *.css) do (
    set /a TOTAL_FILES+=1

    findstr /I /C:"najika" /C:"kuja" /C:"digivice" /C:"muehle" /C:"crafting" /C:"fishing" /C:"explosion" /C:"weaving" /C:"fortnite" /C:"uefn" /C:"opus" "%%F" >nul 2>&1

    if !errorlevel! EQU 0 (
        set /a FOUND_FILES+=1

        echo [TREFFER] %%~nxF

        (
            echo.
            echo ==============================================================
            echo DATEI: %%~nxF
            echo ==============================================================
            echo Pfad: %%F
            echo Groesse: %%~zF bytes
            echo.
        ) >> "%OUTPUT%"

        REM Zeige gefundene Keywords
        for %%K in (%KEYWORDS%) do (
            findstr /I /N /C:"%%K" "%%F" >nul 2>&1
            if !errorlevel! EQU 0 (
                echo   [%%K] gefunden
                (
                    echo [KEYWORD: %%K]
                    findstr /I /N /C:"%%K" "%%F"
                    echo.
                ) >> "%OUTPUT%"
            )
        )
    )

    set /a MOD=!TOTAL_FILES! %% 10
    if !MOD! EQU 0 (
        echo   [Progress] !TOTAL_FILES! Dateien...
    )
)

echo.
echo [PHASE 2] PDFs...
echo.

set /a PDF_FILES=0

(
    echo.
    echo ==============================================================
    echo PDF-DATEIEN
    echo ==============================================================
    echo.
) >> "%OUTPUT%"

for /R "%SEARCH_DIR%" %%F in (*.pdf) do (
    set /a PDF_FILES+=1
    echo   [PDF] %%~nxF
    (
        echo [PDF] %%~nxF
        echo Pfad: %%F
        echo Groesse: %%~zF bytes
        echo.
    ) >> "%OUTPUT%"
)

echo.
echo [PHASE 3] Bilder und 3D-Assets...
echo.

set /a IMAGE_FILES=0

(
    echo.
    echo ==============================================================
    echo BILDER UND 3D-ASSETS
    echo ==============================================================
    echo.
) >> "%OUTPUT%"

for /R "%SEARCH_DIR%" %%F in (*.png *.jpg *.jpeg *.gif *.bmp *.webp *.glb *.gltf *.fbx *.obj) do (
    set /a IMAGE_FILES+=1
    echo   [ASSET] %%~nxF
    (
        echo [ASSET] %%~nxF
        echo Pfad: %%F
        echo Typ: %%~xF
        echo Groesse: %%~zF bytes
        echo.
    ) >> "%OUTPUT%"
)

REM Zusammenfassung
(
    echo.
    echo ==============================================================
    echo ZUSAMMENFASSUNG
    echo ==============================================================
    echo.
    echo Text-Dateien durchsucht:  %TOTAL_FILES%
    echo Dateien mit Treffern:     %FOUND_FILES%
    echo PDFs:                      %PDF_FILES%
    echo Bilder/3D-Assets:          %IMAGE_FILES%
    echo.
    echo ==============================================================
    echo.
) >> "%OUTPUT%"

echo.
echo ==============================================================
echo                  SUCHE ABGESCHLOSSEN
echo ==============================================================
echo   Text-Dateien:          %TOTAL_FILES%
echo   Treffer:               %FOUND_FILES%
echo   PDFs:                  %PDF_FILES%
echo   Assets:                %IMAGE_FILES%
echo ==============================================================
echo.
echo Report: %OUTPUT%
echo.

if exist "%OUTPUT%" (
    echo Report erfolgreich erstellt!
    echo Oeffne Report in Notepad...
    start notepad "%OUTPUT%"
) else (
    echo FEHLER: Report wurde nicht erstellt!
    echo Pfad: %OUTPUT%
)

echo.
echo Druecke eine Taste zum Schliessen...
pause
