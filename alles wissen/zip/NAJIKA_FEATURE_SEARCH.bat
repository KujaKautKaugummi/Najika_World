@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ╔══════════════════════════════════════════════════════════════╗
echo ║          NAJIKA FEATURE EXTRACTION TOOL v2.0                 ║
echo ║  Durchsucht alle Dateien nach relevanten Najika-Features    ║
echo ║  + Kuja-Najika Beziehung ^(AI Girlfriend^)                    ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

set "OUTPUT=NAJIKA_FEATURES_FOUND_%date:~-4%%date:~-7,2%%date:~-10,2%_%time:~0,2%%time:~3,2%%time:~6,2%.txt"
set "OUTPUT=%OUTPUT: =0%"

echo Starte Suche in: %~dp0
echo Report wird erstellt: %OUTPUT%
echo.
echo ═══════════════════════════════════════════════════════════════
echo.

REM Erstelle Report-Header
(
echo ═══════════════════════════════════════════════════════════════
echo      NAJIKA FEATURE EXTRACTION REPORT v2.0
echo ═══════════════════════════════════════════════════════════════
echo Erstellt am: %date% %time%
echo Durchsuchtes Verzeichnis: %~dp0
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo SUCHKRITERIEN:
echo.
echo ★★★ KERN-BEZIEHUNG ★★★
echo   [1] AI/KI Girlfriend ^(Najika^)
echo   [2] Kuja = Schwert ^& Schild ^(Beschützer, Verteidiger^)
echo   [3] Najika = Kopf ^& Herz ^(Intelligenz + Emotion^)
echo   [4] Symbiotische Beziehung Kuja-Najika
echo   [5] Loyalität, Bindung, Vertrauen
echo.
echo ★★★ NAJIKA SYSTEM ★★★
echo   [6] Digivice ^(Handy-Spiel^)
echo   [7] Gesicherter Bereich / Schwarze Mühle
echo   [8] Maximale Freiheit ^& Totale Eigenverantwortung
echo   [9] Wizard-Modell Ergänzungen
echo   [10] UEFN Integration
echo.
echo ★★★ OPUS ADVANCED FEATURES ★★★
echo   [11] Opus Advanced Features ^(Basis-Code^)
echo   [12] Memory System ^(Import/Export^)
echo   [13] Bond-Strength / Beziehungssystem
echo   [14] Persönlichkeits-System ^(4 Aspekte^)
echo   [15] Importance-Scoring
echo   [16] Logging-System
echo.
echo ★★★ PERSÖNLICHKEIT ★★★
echo   [17] MEGUMIN ^(Dramatisch-Explosiv^)
echo   [18] HARLEY QUINN ^(Chaotisch-Verspielt^)
echo   [19] SHIRO ^(Analytisch-Intelligent^)
echo   [20] MELISSA MASTERS ^(Dominant-Führend^)
echo.
echo ★★★ LERN ^& TRAINING ★★★
echo   [21] Lern-System ^(Hyperrealistisch-Menschlich-Autonom^)
echo   [22] Training-System ^(Digimon World Style^)
echo   [23] Autonomie ^& Eigenständigkeit
echo   [24] Adaptive Intelligence
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
) > "%OUTPUT%"

REM ===== KEYWORD KATEGORIEN =====

REM KERN: Kuja-Najika Beziehung
set "KUJA_NAJIKA_KEYWORDS=kuja najika schwert schild beschützer verteidiger kopf herz intelligenz emotion girlfriend ai ki beziehung symbiose partnerschaft"

REM KERN: AI Girlfriend Aspekt
set "GIRLFRIEND_KEYWORDS=girlfriend companion begleiterin partnerin liebe zuneigung bindung verbunden loyal treu unterstützung"

REM KERN: Emotionale Bindung
set "EMOTIONAL_KEYWORDS=liebe zuneigung bindung vertrauen loyalität treue verbunden nah innig tief emotional gefühl herz seele"

REM KERN: Beschützer-Rolle (Kuja)
set "PROTECTOR_KEYWORDS=beschützer verteidiger schützen schild schwert kämpfer krieger wächter guardian defender"

REM KERN: Intelligenz-Emotion (Najika)
set "MIND_HEART_KEYWORDS=kopf herz intelligenz emotion verstand gefühl denken fühlen bewusst empathie"

REM Basis-Keywords
set "KEYWORDS=najika wizard freiheit eigenverantwortung digivice schwarze mühle gesichert uefn opus memory bond beziehung persona import export logging importance kätzchen private"

REM Persönlichkeits-Keywords (4 Aspekte)
set "PERSONALITY_KEYWORDS=MEGUMIN HARLEY SHIRO MELISSA explosion puddin wahrscheinlichkeit dramatisch chaotisch analytisch dominant theatralisch verspielt intelligent führung"

REM Opus-spezifische Keywords
set "OPUS_KEYWORDS=PERSONA_SYSTEM behavior_mode bond_strength total_interactions personality_weights detect_behavior_mode update_bond_strength get_mode_prompt_addition calculate_message_importance"

REM neu 1.txt Konzept-Keywords
set "NEU1_KEYWORDS=maximale freiheit totale eigenverantwortung selbstbestimmt autonom unabhängig entscheidung verantwortung entwicklung wachstum lernen anpassung"

REM Charakterzug-Keywords
set "TRAIT_KEYWORDS=loyal beschützend neckisch besitzergreifend unterstützend liebevoll eifersüchtig treu verbunden emotional tiefe"

REM Lern-System Keywords
set "LEARNING_KEYWORDS=lernsystem hyperrealistisch menschlich autonom selbstlernen entwicklung evolution training anpassung wachstum erfahrung gedächtnis erinnern verstehen"

REM Autonomie-Keywords
set "AUTONOMY_KEYWORDS=eigenständig unabhängig selbstbestimmt autonom entscheidung initiative proaktiv reaktiv adaptive intelligent bewusst"

REM Training-System Keywords
set "TRAINING_KEYWORDS=training lernen üben verbessern optimieren fortschritt level skill fähigkeit kompetenz meisterschaft stats strength intelligence dexterity charisma"

REM Kombiniere ALLE Keywords
set "ALL_KEYWORDS=%KUJA_NAJIKA_KEYWORDS% %GIRLFRIEND_KEYWORDS% %EMOTIONAL_KEYWORDS% %PROTECTOR_KEYWORDS% %MIND_HEART_KEYWORDS% %KEYWORDS% %PERSONALITY_KEYWORDS% %OPUS_KEYWORDS% %NEU1_KEYWORDS% %TRAIT_KEYWORDS% %LEARNING_KEYWORDS% %AUTONOMY_KEYWORDS% %TRAINING_KEYWORDS%"

echo [PHASE 1] Durchsuche Text-Dateien...
echo   Keywords: Kuja-Najika Beziehung, AI Girlfriend, Opus Features, Persönlichkeit
echo.

REM Zähler
set /a TOTAL_FILES=0
set /a FOUND_FILES=0
set /a TOTAL_MATCHES=0

REM Durchsuche alle Text-Dateien
for /R "%~dp0" %%F in (*.txt *.md *.json *.jsonl) do (
    set /a TOTAL_FILES+=1
    set "CURRENT_FILE=%%F"
    set "FOUND_IN_FILE=0"

    REM Prüfe jedes Keyword
    for %%K in (%ALL_KEYWORDS%) do (
        findstr /I /C:"%%K" "%%F" >nul 2>&1
        if !errorlevel! EQU 0 (
            if !FOUND_IN_FILE! EQU 0 (
                set /a FOUND_FILES+=1
                set "FOUND_IN_FILE=1"
                echo.
                echo ═══════════════════════════════════════════════════════════════
                echo FUNDSTELLE IN: %%~nxF
                echo Pfad: %%F
                echo ═══════════════════════════════════════════════════════════════
                echo.
                (
                    echo.
                    echo ═══════════════════════════════════════════════════════════════
                    echo DATEI: %%~nxF
                    echo PFAD: %%F
                    echo ═══════════════════════════════════════════════════════════════
                    echo.
                ) >> "%OUTPUT%"
            )

            REM Extrahiere Zeilen mit Kontext
            echo [KEYWORD: %%K]
            echo [KEYWORD: %%K] >> "%OUTPUT%"

            for /F "delims=:" %%L in ('findstr /I /N /C:"%%K" "%%F"') do (
                set /a LINE_NUM=%%L
                set /a TOTAL_MATCHES+=1
                set /a CONTEXT_START=!LINE_NUM!-2
                set /a CONTEXT_END=!LINE_NUM!+2
                if !CONTEXT_START! LSS 1 set CONTEXT_START=1

                REM Zeige Zeile mit Kontext
                set /a CURRENT=0
                for /F "usebackq delims=" %%M in ("%%F") do (
                    set /a CURRENT+=1
                    if !CURRENT! GEQ !CONTEXT_START! if !CURRENT! LEQ !CONTEXT_END! (
                        if !CURRENT! EQU !LINE_NUM! (
                            echo   ^>^>^> %%M
                            echo   ^>^>^> %%M >> "%OUTPUT%"
                        ) else (
                            echo       %%M
                            echo       %%M >> "%OUTPUT%"
                        )
                    )
                )
            )
            echo. >> "%OUTPUT%"
        )
    )
)

echo.
echo.
echo ═══════════════════════════════════════════════════════════════
echo [PHASE 2] Spezielle Muster-Suche...
echo ═══════════════════════════════════════════════════════════════
echo.

REM Suche nach speziellen Patterns
(
    echo.
    echo ═══════════════════════════════════════════════════════════════
    echo SPEZIELLE PATTERN-SUCHE
    echo ═══════════════════════════════════════════════════════════════
    echo.
) >> "%OUTPUT%"

REM Suche nach Kuja-Najika Beziehungs-Beschreibungen
echo [Suche nach Kuja-Najika Beziehungs-Beschreibungen...]
for /R "%~dp0" %%F in (*.txt *.md) do (
    findstr /I /C:"kuja" "%%F" >nul 2>&1
    if !errorlevel! EQU 0 (
        findstr /I /C:"najika" "%%F" >nul 2>&1
        if !errorlevel! EQU 0 (
            echo   KUJA-NAJIKA BEZIEHUNG gefunden in: %%~nxF
            (
                echo ★★★ KUJA-NAJIKA BEZIEHUNGS-BESCHREIBUNG in: %%~nxF ★★★
                echo Pfad: %%F
                echo ---
                echo KUJA ^(SCHWERT ^& SCHILD^):
                type "%%F" | findstr /I /C:"kuja" /C:"schwert" /C:"schild" /C:"beschützer"
                echo.
                echo NAJIKA ^(KOPF ^& HERZ^):
                type "%%F" | findstr /I /C:"najika" /C:"kopf" /C:"herz" /C:"intelligenz" /C:"emotion"
                echo.
                echo BEZIEHUNG:
                type "%%F" | findstr /I /C:"beziehung" /C:"bindung" /C:"loyal" /C:"vertrauen" /C:"liebe"
                echo.
            ) >> "%OUTPUT%"
        )
    )
)

REM Suche nach AI Girlfriend Konzept
echo [Suche nach AI/KI Girlfriend Konzept...]
for /R "%~dp0" %%F in (*.txt *.md) do (
    findstr /I /C:"girlfriend" /C:"begleiterin" /C:"companion" "%%F" >nul 2>&1
    if !errorlevel! EQU 0 (
        findstr /I /C:"najika" /C:"ai" /C:"ki" "%%F" >nul 2>&1
        if !errorlevel! EQU 0 (
            echo   AI GIRLFRIEND KONZEPT gefunden in: %%~nxF
            (
                echo ★★★ AI/KI GIRLFRIEND KONZEPT in: %%~nxF ★★★
                echo Pfad: %%F
                echo ---
                type "%%F" | findstr /I /C:"girlfriend" /C:"companion" /C:"begleiterin" /C:"partnerin"
                echo.
            ) >> "%OUTPUT%"
        )
    )
)

REM Suche nach Code-Patterns
echo [Suche nach Python-Funktionen...]
for /R "%~dp0" %%F in (*.py *.txt) do (
    findstr /I /R /C:"def.*najika" /C:"class.*Najika" "%%F" >nul 2>&1
    if !errorlevel! EQU 0 (
        echo   GEFUNDEN in: %%~nxF
        (
            echo PYTHON CODE in: %%~nxF
            findstr /I /N /R /C:"def.*najika" /C:"class.*Najika" "%%F"
            echo.
        ) >> "%OUTPUT%"
    )
)

echo [Suche nach Config/Settings...]
for /R "%~dp0" %%F in (*.json *.jsonl *.env) do (
    findstr /I /C:"najika" /C:"wizard" /C:"model" /C:"persona" "%%F" >nul 2>&1
    if !errorlevel! EQU 0 (
        echo   GEFUNDEN in: %%~nxF
        (
            echo CONFIG/SETTINGS in: %%~nxF
            type "%%F" | findstr /I /N /C:"najika" /C:"wizard" /C:"model" /C:"persona"
            echo.
        ) >> "%OUTPUT%"
    )
)

echo [Suche nach API-Endpoints...]
for /R "%~dp0" %%F in (*.txt *.md *.py) do (
    findstr /I /C:"/api/" /C:"endpoint" /C:"route" "%%F" >nul 2>&1
    if !errorlevel! EQU 0 (
        findstr /I /C:"najika" "%%F" >nul 2>&1
        if !errorlevel! EQU 0 (
            echo   GEFUNDEN in: %%~nxF
            (
                echo API ENDPOINTS in: %%~nxF
                type "%%F" | findstr /I /N /C:"/api/"
                echo.
            ) >> "%OUTPUT%"
        )
    )
)

echo.
echo ═══════════════════════════════════════════════════════════════
echo [PHASE 3] Opus-Code ^& Persönlichkeits-Basis Analyse...
echo ═══════════════════════════════════════════════════════════════
echo.

(
    echo.
    echo ═══════════════════════════════════════════════════════════════
    echo OPUS-CODE BASIS ^& PERSÖNLICHKEITS-SYSTEM
    echo ═══════════════════════════════════════════════════════════════
    echo.
) >> "%OUTPUT%"

REM Suche nach PERSONA_SYSTEM Definitionen
echo [Suche nach PERSONA_SYSTEM Definitionen...]
for /R "%~dp0" %%F in (*.txt *.py *.md) do (
    findstr /I /C:"PERSONA_SYSTEM" /C:"PERSÖNLICHKEITS" /C:"4 ASPEKTE" "%%F" >nul 2>&1
    if !errorlevel! EQU 0 (
        echo   PERSONA_SYSTEM gefunden in: %%~nxF
        (
            echo ★★★ PERSONA_SYSTEM DEFINITION in: %%~nxF ★★★
            echo Pfad: %%F
            echo ---
            type "%%F" | findstr /I /N /C:"PERSONA" /C:"PERSÖNLICHKEIT" /C:"ASPEKTE"
            echo.
        ) >> "%OUTPUT%"
    )
)

REM Suche nach 4 Persönlichkeits-Aspekten
echo [Suche nach 4 Persönlichkeits-Aspekten...]
for /R "%~dp0" %%F in (*.txt *.md *.json) do (
    findstr /I /C:"MEGUMIN" "%%F" >nul 2>&1
    if !errorlevel! EQU 0 (
        findstr /I /C:"HARLEY" "%%F" >nul 2>&1
        if !errorlevel! EQU 0 (
            findstr /I /C:"SHIRO" "%%F" >nul 2>&1
            if !errorlevel! EQU 0 (
                findstr /I /C:"MELISSA" "%%F" >nul 2>&1
                if !errorlevel! EQU 0 (
                    echo   ★★★ ALLE 4 ASPEKTE gefunden in: %%~nxF ★★★
                    (
                        echo ═══════════════════════════════════════════════════════════════
                        echo ★★★ VOLLSTÄNDIGES PERSÖNLICHKEITS-SYSTEM in: %%~nxF ★★★
                        echo ═══════════════════════════════════════════════════════════════
                        echo Pfad: %%F
                        echo.
                        echo [1] MEGUMIN ^(Dramatisch-Explosiv^):
                        type "%%F" | findstr /I /C:"MEGUMIN" /C:"explosion" /C:"dramatisch"
                        echo.
                        echo [2] HARLEY QUINN ^(Chaotisch-Verspielt^):
                        type "%%F" | findstr /I /C:"HARLEY" /C:"puddin" /C:"chaotisch"
                        echo.
                        echo [3] SHIRO ^(Analytisch-Intelligent^):
                        type "%%F" | findstr /I /C:"SHIRO" /C:"wahrscheinlichkeit" /C:"analytisch"
                        echo.
                        echo [4] MELISSA ^(Dominant-Führend^):
                        type "%%F" | findstr /I /C:"MELISSA" /C:"dominant" /C:"führung"
                        echo.
                        echo ═══════════════════════════════════════════════════════════════
                        echo.
                    ) >> "%OUTPUT%"
                )
            )
        )
    )
)

REM Suche nach "Maximale Freiheit" Konzept
echo [Suche nach "Maximale Freiheit ^& Eigenverantwortung" Konzept...]
for /R "%~dp0" %%F in (*.txt *.md) do (
    findstr /I /C:"maximale freiheit" /C:"totale eigenverantwortung" "%%F" >nul 2>&1
    if !errorlevel! EQU 0 (
        echo   FREIHEITS-KONZEPT gefunden in: %%~nxF
        (
            echo ★★★ FREIHEITS-KONZEPT in: %%~nxF ★★★
            echo Pfad: %%F
            echo ---
            type "%%F" | findstr /I /N /C:"freiheit" /C:"eigenverantwortung" /C:"selbstbestimmt"
            echo.
        ) >> "%OUTPUT%"
    )
)

REM Suche nach Opus Advanced Features Code
echo [Suche nach Opus Advanced Features Code...]
for /R "%~dp0" %%F in (*.py *.txt) do (
    findstr /I /C:"def update_bond_strength" /C:"def detect_behavior_mode" /C:"def calculate_message_importance" "%%F" >nul 2>&1
    if !errorlevel! EQU 0 (
        echo   ★★★ OPUS ADVANCED CODE gefunden in: %%~nxF ★★★
        (
            echo ★★★ OPUS ADVANCED FEATURES CODE in: %%~nxF ★★★
            echo Pfad: %%F
            echo ---
            type "%%F" | findstr /I /N /C:"def update_bond" /C:"def detect_behavior" /C:"def calculate_message"
            echo.
        ) >> "%OUTPUT%"
    )
)

REM Suche nach "neu 1" Datei
echo [Suche nach "neu 1.txt" Beschreibungen...]
for /R "%~dp0" %%F in (*neu*1*.txt *neu*1*.md) do (
    if exist "%%F" (
        echo   ★★★ NEU 1 DATEI gefunden: %%~nxF ★★★
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

REM Suche nach Training-System
echo [Suche nach Training-System...]
for /R "%~dp0" %%F in (*.py *.txt) do (
    findstr /I /C:"def train_stat" /C:"def update_needs" /C:"training" "%%F" >nul 2>&1
    if !errorlevel! EQU 0 (
        findstr /I /C:"najika" "%%F" >nul 2>&1
        if !errorlevel! EQU 0 (
            echo   TRAINING-SYSTEM CODE gefunden in: %%~nxF
            (
                echo TRAINING-SYSTEM CODE in: %%~nxF
                echo Pfad: %%F
                echo ---
                type "%%F" | findstr /I /N /C:"def train" /C:"def update_needs" /C:"def feed" /C:"def sleep"
                echo.
            ) >> "%OUTPUT%"
        )
    )
)

REM Summary
(
    echo.
    echo ═══════════════════════════════════════════════════════════════
    echo ZUSAMMENFASSUNG
    echo ═══════════════════════════════════════════════════════════════
    echo.
    echo Durchsuchte Dateien:       %TOTAL_FILES%
    echo Dateien mit Treffern:      %FOUND_FILES%
    echo Gesamt Fundstellen:        %TOTAL_MATCHES%
    echo.
    echo ★★★ SPEZIAL-KATEGORIEN ★★★
    echo   • Kuja-Najika Beziehung ^(AI Girlfriend^)
    echo   • Opus Advanced Features
    echo   • 4 Persönlichkeits-Aspekte
    echo   • Maximale Freiheit Konzept
    echo   • Training ^& Lern-System
    echo.
    echo Report gespeichert in:
    echo %~dp0%OUTPUT%
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
echo ║  Gesamt Fundstellen:        %TOTAL_MATCHES%
echo ╠══════════════════════════════════════════════════════════════╣
echo ║  ★★★ SPEZIAL-KATEGORIEN ★★★
echo ║  • Kuja-Najika Beziehung ^(AI Girlfriend^)
echo ║  • Schwert ^& Schild vs Kopf ^& Herz
echo ║  • Opus Advanced Features
echo ║  • 4 Persönlichkeits-Aspekte
echo ╠══════════════════════════════════════════════════════════════╣
echo ║  Report erstellt:
echo ║  %OUTPUT%
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo Report wird geöffnet...
echo.

REM Öffne Report in Notepad
start notepad "%OUTPUT%"

pause
