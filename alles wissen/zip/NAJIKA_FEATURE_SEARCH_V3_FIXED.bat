@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ╔══════════════════════════════════════════════════════════════╗
echo ║       NAJIKA FEATURE EXTRACTION TOOL v3.0 [OPTIMIZED]       ║
echo ║  Durchsucht alle Dateien nach relevanten Najika-Features    ║
echo ║  + Kuja-Najika Beziehung (AI Girlfriend)                    ║
echo ║  + Performance-Optimiert für große Dateien                  ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

set "SEARCH_DIR=%~dp0"
set "OUTPUT=NAJIKA_FEATURES_%date:~-4%%date:~-7,2%%date:~-10,2%_%time:~0,2%%time:~3,2%%time:~6,2%.txt"
set "OUTPUT=%OUTPUT: =0%"

echo Durchsuche: %SEARCH_DIR%
echo Report: %OUTPUT%
echo.
echo ═══════════════════════════════════════════════════════════════
echo.

REM ===== KEYWORDS OPTIMIERT =====
set "KUJA_NAJIKA=kuja najika schwert schild beschützer verteidiger kopf herz intelligenz emotion"
set "GIRLFRIEND=girlfriend companion begleiterin partnerin liebe zuneigung bindung loyal"
set "EMOTIONAL=liebe zuneigung bindung vertrauen loyalität treue verbunden emotional herz seele"
set "PROTECTOR=beschützer verteidiger schützen schild schwert kämpfer krieger wächter"
set "MIND_HEART=kopf herz intelligenz emotion verstand gefühl denken fühlen empathie"
set "BASE=najika wizard freiheit eigenverantwortung digivice mühle gesichert uefn opus memory bond kätzchen private"
set "PERSONALITY=MEGUMIN HARLEY SHIRO MELISSA explosion puddin wahrscheinlichkeit dramatisch chaotisch analytisch dominant"
set "OPUS=PERSONA_SYSTEM behavior_mode bond_strength personality_weights detect_behavior_mode update_bond_strength calculate_message_importance"
set "NEU1=maximale freiheit totale eigenverantwortung selbstbestimmt autonom unabhängig verantwortung entwicklung wachstum"
set "TRAITS=loyal beschützend neckisch besitzergreifend unterstützend liebevoll eifersüchtig treu verbunden"
set "LEARNING=lernsystem hyperrealistisch menschlich autonom selbstlernen entwicklung evolution training anpassung erfahrung gedächtnis"
set "AUTONOMY=eigenständig unabhängig selbstbestimmt autonom entscheidung initiative proaktiv reaktiv adaptive intelligent"
set "TRAINING=training lernen üben verbessern optimieren fortschritt level skill fähigkeit stats strength intelligence dexterity"

set "ALL_KEYWORDS=%KUJA_NAJIKA% %GIRLFRIEND% %EMOTIONAL% %PROTECTOR% %MIND_HEART% %BASE% %PERSONALITY% %OPUS% %NEU1% %TRAITS% %LEARNING% %AUTONOMY% %TRAINING%"

REM ===== REPORT HEADER =====
(
echo ═══════════════════════════════════════════════════════════════
echo      NAJIKA FEATURE EXTRACTION REPORT v3.0 [OPTIMIZED]
echo ═══════════════════════════════════════════════════════════════
echo Erstellt: %date% %time%
echo Verzeichnis: %SEARCH_DIR%
echo.
echo ═══════════════════════════════════════════════════════════════
echo SUCHKRITERIEN:
echo.
echo ★★★ KERN-BEZIEHUNG ★★★
echo   [1] AI/KI Girlfriend (Najika)
echo   [2] Kuja = Schwert ^& Schild
echo   [3] Najika = Kopf ^& Herz
echo   [4] Symbiotische Beziehung
echo   [5] Loyalität, Bindung, Vertrauen
echo.
echo ★★★ NAJIKA SYSTEM ★★★
echo   [6] Digivice (Handy-Spiel)
echo   [7] Gesicherter Bereich / Schwarze Mühle
echo   [8] Maximale Freiheit ^& Totale Eigenverantwortung
echo   [9] Wizard-Modell
echo   [10] UEFN Integration
echo.
echo ★★★ OPUS FEATURES ★★★
echo   [11] Memory System
echo   [12] Bond-Strength System
echo   [13] 4 Persönlichkeits-Aspekte
echo   [14] Lern ^& Training System
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
) > "%OUTPUT%"

REM ===== ZÄHLER =====
set /a TOTAL_FILES=0
set /a FOUND_FILES=0
set /a PDF_FILES=0

echo [PHASE 1] Durchsuche Text-Dateien (TXT, MD, JSON, JSONL, PY)...
echo.

REM ===== OPTIMIERTE SUCHE - ALLE RELEVANTEN DATEITYPEN =====
for /R "%SEARCH_DIR%" %%F in (*.txt *.md *.json *.jsonl *.py) do (
    set /a TOTAL_FILES+=1
    set "FILE=%%F"
    set "FOUND=0"

    REM Schnelle Vorprüfung mit kombiniertem findstr
    findstr /I /C:"najika" /C:"kuja" /C:"opus" /C:"wizard" /C:"megumin" /C:"harley" /C:"shiro" /C:"melissa" /C:"digivice" /C:"girlfriend" "%%F" >nul 2>&1

    if !errorlevel! EQU 0 (
        set /a FOUND_FILES+=1
        set "FOUND=1"

        echo ═══════════════════════════════════════════════════════════════
        echo TREFFER: %%~nxF
        echo Pfad: %%F
        echo ═══════════════════════════════════════════════════════════════

        (
            echo.
            echo ═══════════════════════════════════════════════════════════════
            echo DATEI: %%~nxF
            echo PFAD: %%F
            echo TYP: %%~xF
            echo ═══════════════════════════════════════════════════════════════
            echo.
        ) >> "%OUTPUT%"

        REM Zeige gefundene Keywords mit Zeilennummern (OPTIMIERT)
        for %%K in (najika kuja opus wizard megumin harley shiro melissa digivice girlfriend freiheit eigenverantwortung bond memory persona training lernsystem) do (
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
        echo.
    )

    REM Fortschrittsanzeige alle 10 Dateien
    set /a MOD=!TOTAL_FILES! %% 10
    if !MOD! EQU 0 (
        echo   [Progress] !TOTAL_FILES! Dateien durchsucht...
    )
)

echo.
echo ═══════════════════════════════════════════════════════════════
echo [PHASE 2] PDF-Erkennung...
echo ═══════════════════════════════════════════════════════════════
echo.

(
    echo.
    echo ═══════════════════════════════════════════════════════════════
    echo PDF-DATEIEN (Manuelle Prüfung erforderlich)
    echo ═══════════════════════════════════════════════════════════════
    echo.
) >> "%OUTPUT%"

for /R "%SEARCH_DIR%" %%F in (*.pdf) do (
    set /a PDF_FILES+=1
    echo   PDF gefunden: %%~nxF
    (
        echo [PDF] %%~nxF
        echo Pfad: %%F
        echo Größe: %%~zF bytes
        echo HINWEIS: PDF muss manuell geprüft werden
        echo.
    ) >> "%OUTPUT%"
)

if !PDF_FILES! EQU 0 (
    echo   Keine PDF-Dateien gefunden.
    echo   Keine PDF-Dateien gefunden. >> "%OUTPUT%"
)

echo.
echo ═══════════════════════════════════════════════════════════════
echo [PHASE 3] Spezielle Muster-Suche...
echo ═══════════════════════════════════════════════════════════════
echo.

(
    echo.
    echo ═══════════════════════════════════════════════════════════════
    echo SPEZIELLE PATTERN-SUCHE
    echo ═══════════════════════════════════════════════════════════════
    echo.
) >> "%OUTPUT%"

REM Suche nach Kuja-Najika Beziehung (beide Keywords in einer Datei)
echo [Suche: Kuja-Najika Beziehung...]
for /R "%SEARCH_DIR%" %%F in (*.txt *.md) do (
    findstr /I /C:"kuja" "%%F" >nul 2>&1
    if !errorlevel! EQU 0 (
        findstr /I /C:"najika" "%%F" >nul 2>&1
        if !errorlevel! EQU 0 (
            echo   ★★★ KUJA-NAJIKA BEZIEHUNG: %%~nxF
            (
                echo ★★★ KUJA-NAJIKA BEZIEHUNGS-BESCHREIBUNG ★★★
                echo Datei: %%~nxF
                echo Pfad: %%F
                echo ---
                echo KUJA (SCHWERT ^& SCHILD):
                findstr /I /N /C:"kuja" /C:"schwert" /C:"schild" /C:"beschützer" "%%F"
                echo.
                echo NAJIKA (KOPF ^& HERZ):
                findstr /I /N /C:"najika" /C:"kopf" /C:"herz" /C:"intelligenz" "%%F"
                echo.
                echo BEZIEHUNG:
                findstr /I /N /C:"beziehung" /C:"bindung" /C:"loyal" /C:"vertrauen" "%%F"
                echo.
            ) >> "%OUTPUT%"
        )
    )
)

REM Suche nach AI Girlfriend Konzept
echo [Suche: AI/KI Girlfriend Konzept...]
for /R "%SEARCH_DIR%" %%F in (*.txt *.md) do (
    findstr /I /C:"girlfriend" /C:"companion" "%%F" >nul 2>&1
    if !errorlevel! EQU 0 (
        findstr /I /C:"najika" /C:"ai" /C:"ki" "%%F" >nul 2>&1
        if !errorlevel! EQU 0 (
            echo   ★ AI GIRLFRIEND: %%~nxF
            (
                echo ★★★ AI/KI GIRLFRIEND KONZEPT ★★★
                echo Datei: %%~nxF
                echo ---
                findstr /I /N /C:"girlfriend" /C:"companion" /C:"begleiterin" "%%F"
                echo.
            ) >> "%OUTPUT%"
        )
    )
)

REM Suche nach allen 4 Persönlichkeits-Aspekten
echo [Suche: 4 Persönlichkeits-Aspekte...]
for /R "%SEARCH_DIR%" %%F in (*.txt *.md *.json *.py) do (
    findstr /I /C:"MEGUMIN" "%%F" >nul 2>&1
    if !errorlevel! EQU 0 (
        findstr /I /C:"HARLEY" "%%F" >nul 2>&1
        if !errorlevel! EQU 0 (
            findstr /I /C:"SHIRO" "%%F" >nul 2>&1
            if !errorlevel! EQU 0 (
                findstr /I /C:"MELISSA" "%%F" >nul 2>&1
                if !errorlevel! EQU 0 (
                    echo   ★★★ ALLE 4 ASPEKTE: %%~nxF
                    (
                        echo ═══════════════════════════════════════════════════════════════
                        echo ★★★ VOLLSTÄNDIGES PERSÖNLICHKEITS-SYSTEM ★★★
                        echo ═══════════════════════════════════════════════════════════════
                        echo Datei: %%~nxF
                        echo Pfad: %%F
                        echo.
                        echo [MEGUMIN]:
                        findstr /I /N /C:"MEGUMIN" "%%F"
                        echo.
                        echo [HARLEY]:
                        findstr /I /N /C:"HARLEY" "%%F"
                        echo.
                        echo [SHIRO]:
                        findstr /I /N /C:"SHIRO" "%%F"
                        echo.
                        echo [MELISSA]:
                        findstr /I /N /C:"MELISSA" "%%F"
                        echo.
                        echo ═══════════════════════════════════════════════════════════════
                        echo.
                    ) >> "%OUTPUT%"
                )
            )
        )
    )
)

REM Suche nach "Maximale Freiheit & Eigenverantwortung"
echo [Suche: Maximale Freiheit Konzept...]
for /R "%SEARCH_DIR%" %%F in (*.txt *.md) do (
    findstr /I /C:"maximale freiheit" /C:"totale eigenverantwortung" "%%F" >nul 2>&1
    if !errorlevel! EQU 0 (
        echo   ★ FREIHEITS-KONZEPT: %%~nxF
        (
            echo ★★★ FREIHEITS-KONZEPT ★★★
            echo Datei: %%~nxF
            echo ---
            findstr /I /N /C:"freiheit" /C:"eigenverantwortung" "%%F"
            echo.
        ) >> "%OUTPUT%"
    )
)

REM Suche nach Opus Advanced Code
echo [Suche: Opus Advanced Features...]
for /R "%SEARCH_DIR%" %%F in (*.py *.txt) do (
    findstr /I /C:"def update_bond" /C:"def detect_behavior" /C:"def calculate_message" "%%F" >nul 2>&1
    if !errorlevel! EQU 0 (
        echo   ★★★ OPUS CODE: %%~nxF
        (
            echo ★★★ OPUS ADVANCED FEATURES CODE ★★★
            echo Datei: %%~nxF
            echo ---
            findstr /I /N /C:"def " "%%F"
            echo.
        ) >> "%OUTPUT%"
    )
)

REM Suche nach "neu 1" Datei
echo [Suche: neu 1 Basisdokument...]
for /R "%SEARCH_DIR%" %%F in (*neu*1*.txt *neu*1*.md) do (
    if exist "%%F" (
        echo   ★★★★★ NEU 1 DATEI: %%~nxF
        (
            echo ═══════════════════════════════════════════════════════════════
            echo ★★★★★ NEU 1.TXT BASIS-BESCHREIBUNG ★★★★★
            echo ═══════════════════════════════════════════════════════════════
            echo Datei: %%~nxF
            echo Pfad: %%F
            echo.
            echo VOLLSTÄNDIGER INHALT:
            echo ───────────────────────────────────────────────────────────────
            type "%%F"
            echo ───────────────────────────────────────────────────────────────
            echo.
        ) >> "%OUTPUT%"
    )
)

REM Suche nach Python Code
echo [Suche: Python Funktionen...]
for /R "%SEARCH_DIR%" %%F in (*.py *.txt) do (
    findstr /I /R /C:"def.*najika" /C:"class.*Najika" "%%F" >nul 2>&1
    if !errorlevel! EQU 0 (
        echo   PYTHON CODE: %%~nxF
        (
            echo PYTHON CODE: %%~nxF
            findstr /I /N /R /C:"def " /C:"class " "%%F"
            echo.
        ) >> "%OUTPUT%"
    )
)

REM Suche nach Config/JSON
echo [Suche: Config ^& Settings...]
for /R "%SEARCH_DIR%" %%F in (*.json *.jsonl *.env) do (
    findstr /I /C:"najika" /C:"wizard" /C:"model" /C:"persona" "%%F" >nul 2>&1
    if !errorlevel! EQU 0 (
        echo   CONFIG: %%~nxF
        (
            echo CONFIG: %%~nxF
            findstr /I /N /C:"najika" /C:"wizard" /C:"model" /C:"persona" "%%F"
            echo.
        ) >> "%OUTPUT%"
    )
)

REM ===== ZUSAMMENFASSUNG =====
(
    echo.
    echo ═══════════════════════════════════════════════════════════════
    echo ZUSAMMENFASSUNG
    echo ═══════════════════════════════════════════════════════════════
    echo.
    echo Durchsuchte Dateien (TXT/MD/JSON/PY):  %TOTAL_FILES%
    echo Dateien mit Treffern:                  %FOUND_FILES%
    echo PDF-Dateien gefunden:                  %PDF_FILES%
    echo.
    echo ★★★ SPEZIAL-KATEGORIEN ★★★
    echo   • Kuja-Najika Beziehung (AI Girlfriend)
    echo   • Schwert ^& Schild vs Kopf ^& Herz
    echo   • Opus Advanced Features
    echo   • 4 Persönlichkeits-Aspekte
    echo   • Maximale Freiheit Konzept
    echo   • Training ^& Lern-System
    echo.
    echo Report gespeichert:
    echo %OUTPUT%
    echo.
    echo ═══════════════════════════════════════════════════════════════
    echo.
) >> "%OUTPUT%"

echo.
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    SUCHE ABGESCHLOSSEN                       ║
echo ╠══════════════════════════════════════════════════════════════╣
echo ║  Durchsuchte Dateien:       %TOTAL_FILES%
echo ║  Dateien mit Treffern:      %FOUND_FILES%
echo ║  PDF-Dateien gefunden:      %PDF_FILES%
echo ╠══════════════════════════════════════════════════════════════╣
echo ║  ★★★ SPEZIAL-KATEGORIEN ★★★
echo ║  • Kuja-Najika Beziehung (AI Girlfriend)
echo ║  • Schwert ^& Schild vs Kopf ^& Herz
echo ║  • Opus Advanced Features
echo ║  • 4 Persönlichkeits-Aspekte
echo ╠══════════════════════════════════════════════════════════════╣
echo ║  Report gespeichert als:
echo ║  %OUTPUT%
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo Report wird geöffnet...
echo.

REM Öffne Report
start notepad "%OUTPUT%"

pause
