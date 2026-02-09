@echo off
REM ═══════════════════════════════════════════════════════════════════════════════════════
REM  NAJIKA CODE CLI - SETUP
REM
REM  Dieses Script richtet Najika Code ein, damit du es wie Claude Code nutzen kannst!
REM  Nach dem Setup kannst du von überall "najika" aufrufen.
REM ═══════════════════════════════════════════════════════════════════════════════════════

echo.
echo  ╔══════════════════════════════════════════════════════════════════╗
echo  ║                                                                  ║
echo  ║     ███╗   ██╗ █████╗      ██╗██╗██╗  ██╗ █████╗                 ║
echo  ║     ████╗  ██║██╔══██╗     ██║██║██║ ██╔╝██╔══██╗                ║
echo  ║     ██╔██╗ ██║███████║     ██║██║█████╔╝ ███████║                ║
echo  ║     ██║╚██╗██║██╔══██║██   ██║██║██╔═██╗ ██╔══██║                ║
echo  ║     ██║ ╚████║██║  ██║╚█████╔╝██║██║  ██╗██║  ██║                ║
echo  ║     ╚═╝  ╚═══╝╚═╝  ╚═╝ ╚════╝ ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝                ║
echo  ║                                                                  ║
echo  ║              CODE CLI - SETUP WIZARD                             ║
echo  ║                                                                  ║
echo  ╚══════════════════════════════════════════════════════════════════╝
echo.

set NAJIKA_DIR=%~dp0

echo [1/4] Pruefe Python Installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo     FEHLER: Python nicht gefunden!
    echo     Bitte installiere Python von python.org
    pause
    exit /b 1
)
echo     OK: Python gefunden!

echo.
echo [2/4] Installiere benoetigte Pakete...
pip install colorama requests >nul 2>&1
echo     OK: Pakete installiert!

echo.
echo [3/4] Pruefe Ollama...
ollama list >nul 2>&1
if errorlevel 1 (
    echo     WARNUNG: Ollama nicht gefunden!
    echo     Najika kann trotzdem als Datei-Tool genutzt werden.
    echo     Fuer AI-Features: Installiere Ollama von ollama.ai
) else (
    echo     OK: Ollama gefunden!

    REM Pruefe ob najika-wizard existiert
    ollama list | findstr "najika-wizard" >nul 2>&1
    if errorlevel 1 (
        echo     INFO: Najika-Wizard Model nicht gefunden.
        echo     Nutze hermes3:8b als Fallback.
    ) else (
        echo     OK: Najika-Wizard Model vorhanden!
    )
)

echo.
echo [4/4] Erstelle globalen Befehl...

REM Erstelle Verzeichnis fuer globale Scripts
if not exist "%USERPROFILE%\bin" mkdir "%USERPROFILE%\bin"

REM Kopiere najika.bat
copy /Y "%NAJIKA_DIR%najika.bat" "%USERPROFILE%\bin\najika.bat" >nul 2>&1
if errorlevel 1 (
    echo     WARNUNG: Konnte nicht nach %%USERPROFILE%%\bin kopieren
) else (
    echo     OK: najika.bat nach %%USERPROFILE%%\bin kopiert!
)

REM Erstelle Wrapper der auf das richtige Verzeichnis zeigt
echo @echo off> "%USERPROFILE%\bin\najika.bat"
echo set NAJIKA_DIR=%NAJIKA_DIR%>> "%USERPROFILE%\bin\najika.bat"
echo python "%%NAJIKA_DIR%%backend\najika_code.py" %%*>> "%USERPROFILE%\bin\najika.bat"

echo.
echo ═══════════════════════════════════════════════════════════════════
echo  SETUP ABGESCHLOSSEN!
echo ═══════════════════════════════════════════════════════════════════
echo.
echo  WICHTIG: Fuege %%USERPROFILE%%\bin zum PATH hinzu:
echo.
echo  1. Windows-Taste + R
echo  2. "sysdm.cpl" eingeben
echo  3. Tab "Erweitert" ^> "Umgebungsvariablen"
echo  4. Bei "Path" (Benutzer) ^> "Bearbeiten" ^> "Neu"
echo  5. Eintragen: %%USERPROFILE%%\bin
echo  6. OK klicken und CMD neu starten
echo.
echo  ODER schnell in PowerShell (als Admin):
echo    [Environment]::SetEnvironmentVariable("PATH", $env:PATH + ";$env:USERPROFILE\bin", "User")
echo.
echo  Danach kannst du von ueberall "najika" aufrufen!
echo.
echo  BEFEHLE:
echo    najika              - Interaktiver Modus
echo    najika "Frage"      - Einzel-Anfrage
echo    najika --scan       - Projekt scannen
echo    najika --search X   - Suche nach X
echo    najika --todos      - Alle TODOs finden
echo    najika --treasures  - Verlorene Schaetze finden
echo    najika --help       - Hilfe anzeigen
echo.
echo ═══════════════════════════════════════════════════════════════════
echo.

pause
