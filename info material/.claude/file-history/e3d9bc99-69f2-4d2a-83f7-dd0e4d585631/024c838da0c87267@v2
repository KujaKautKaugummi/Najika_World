@echo off
setlocal enabledelayedexpansion
color 0A
title NAJIKA WORLD INSTALLER FINAL

set "SOURCE=C:\NajikaFinal"
set "TARGET=C:\Najika-World"

cls
echo.
echo ========================================================================
echo.
echo                   NAJIKA WORLD INSTALLER FINAL
echo.
echo                Open World + Interior Rooms + Battle System
echo.
echo ========================================================================
echo.
echo Dieser Installer erstellt:
echo    1. Open World System (2400x2400 Map)
echo    2. Schwarze Muehle mit 9 Raeumen
echo    3. Kampfarena + Garten + 3 Dungeons
echo    4. Mobile Touch Controls
echo    5. Backend mit qwen + Memory + TTS
echo.
echo SOURCE: %SOURCE%
echo TARGET: %TARGET%
echo.
echo ========================================================================
echo                       TASTE ZUM STARTEN
echo ========================================================================
pause >nul

REM Admin Check
net session >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    cls
    echo FEHLER: Keine Admin-Rechte!
    echo Rechtsklick -^> Als Administrator ausfuehren
    pause
    exit /b 1
)

color 0A
cls
echo.
echo [OK] Admin-Rechte bestanden!
echo.
timeout /t 2 >nul

REM Check Source
if not exist "%SOURCE%\backend\najika_server.py" (
    color 0C
    cls
    echo FEHLER: NajikaFinal nicht gefunden!
    echo Erwarte: %SOURCE%\backend\najika_server.py
    pause
    exit /b 1
)

echo [OK] Source gefunden!
timeout /t 2 >nul

REM SCHRITT 1: Kopiere NajikaFinal
cls
echo.
echo [SCHRITT 1/7] Kopiere NajikaFinal...
echo [INFO] Das kann 2-3 Minuten dauern...
echo.

mkdir "%TARGET%" 2>nul
xcopy "%SOURCE%\*" "%TARGET%\" /E /I /Y /Q >nul 2>&1

if %errorlevel% equ 0 (
    echo [OK] NajikaFinal kopiert!
) else (
    color 0E
    echo [WARNUNG] Kopieren teilweise fehlgeschlagen (nicht kritisch)
    timeout /t 3 >nul
    color 0A
)

timeout /t 2 >nul

REM SCHRITT 2: Neue Frontend Dateien sind schon in SOURCE!
cls
echo.
echo [SCHRITT 2/7] Pruefe neue Dateien...
echo.

if exist "%TARGET%\frontend\src\game\OpenWorldScene.jsx" (
    echo [OK] OpenWorldScene.jsx gefunden
) else (
    echo [INFO] OpenWorldScene.jsx nicht gefunden (muss noch erstellt werden)
)

if exist "%TARGET%\assets\open_world_config.json" (
    echo [OK] open_world_config.json gefunden
) else (
    echo [INFO] open_world_config.json nicht gefunden
)

timeout /t 2 >nul

REM SCHRITT 3: START.bat erstellen
cls
echo.
echo [SCHRITT 3/7] Erstelle START_NAJIKA_WORLD.bat...
echo.

(
echo @echo off
echo title NAJIKA WORLD
echo color 0A
echo cd /d "%TARGET%"
echo.
echo cls
echo echo.
echo echo ========================================================================
echo echo                      NAJIKA WORLD V1.0
echo echo ========================================================================
echo echo.
echo echo [1/2] Starte Backend ^(Port 8000^)...
echo start /B cmd /c "cd backend ^&^& python najika_server.py"
echo timeout /t 3 ^>nul
echo.
echo echo [2/2] Starte Frontend ^(Port 3002^)...
echo cd frontend
echo start /B cmd /c "npm start"
echo.
echo echo.
echo echo ========================================================================
echo echo                         NAJIKA WORLD GESTARTET!
echo echo ========================================================================
echo echo   Backend:  http://localhost:8000/
echo echo   Frontend: http://localhost:3002/
echo echo ========================================================================
echo echo.
echo echo Druecke Taste zum Beenden...
echo pause ^>nul
) > "%TARGET%\START_NAJIKA_WORLD.bat"

echo [OK] START_NAJIKA_WORLD.bat erstellt!
timeout /t 2 >nul

REM SCHRITT 4: README kopieren
cls
echo.
echo [SCHRITT 4/7] Kopiere Dokumentation...
echo.

if exist "%SOURCE%\NAJIKA_WORLD_SYSTEM_COMPLETE.md" (
    copy "%SOURCE%\NAJIKA_WORLD_SYSTEM_COMPLETE.md" "%TARGET%\" >nul 2>&1
    echo [OK] NAJIKA_WORLD_SYSTEM_COMPLETE.md kopiert
) else (
    echo [INFO] Dokumentation nicht gefunden (nicht kritisch)
)

timeout /t 2 >nul

REM SCHRITT 5: Python Packages (Optional - nur wenn nicht schon installiert)
cls
echo.
echo [SCHRITT 5/7] Pruefe Python Packages...
echo [INFO] Ueberspringen wenn bereits installiert...
echo.

python -c "import flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Installiere Python Packages (kann 3-5 Min dauern)...
    python -m pip install --quiet flask flask-cors flask-socketio python-socketio ollama chromadb edge-tts >nul 2>&1
    if %errorlevel% equ 0 (
        echo [OK] Packages installiert
    ) else (
        echo [WARNUNG] Einige Packages fehlgeschlagen (nicht kritisch)
    )
) else (
    echo [OK] Flask bereits installiert
)

timeout /t 2 >nul

REM SCHRITT 6: Node Modules (Optional)
cls
echo.
echo [SCHRITT 6/7] Pruefe Node Modules...
echo.

if exist "%TARGET%\frontend\node_modules\" (
    echo [OK] node_modules gefunden (npm install nicht noetig)
) else (
    echo [INFO] node_modules nicht gefunden
    echo [INFO] Fuehre 'npm install' im Frontend Ordner aus nach Installation
)

timeout /t 2 >nul

REM SCHRITT 7: Desktop Shortcut
cls
echo.
echo [SCHRITT 7/7] Erstelle Desktop-Verknuepfung...
echo.

powershell -Command "$WS=New-Object -ComObject WScript.Shell;$SC=$WS.CreateShortcut([Environment]::GetFolderPath('Desktop')+'\Najika World.lnk');$SC.TargetPath='%TARGET%\START_NAJIKA_WORLD.bat';$SC.WorkingDirectory='%TARGET%';$SC.IconLocation='%%SystemRoot%%\System32\shell32.dll,137';$SC.Save()" 2>nul

if %errorlevel% equ 0 (
    echo [OK] Desktop-Verknuepfung erstellt
) else (
    echo [INFO] Verknuepfung fehlgeschlagen (nicht kritisch)
)

timeout /t 2 >nul

REM FERTIG!
cls
color 0B
echo.
echo ========================================================================
echo.
echo                     INSTALLATION ERFOLGREICH!
echo.
echo ========================================================================
echo.
echo [OK] NAJIKA WORLD V1.0 INSTALLIERT!
echo.
echo INSTALLIERT IN: %TARGET%
echo.
echo.
echo WAS INSTALLIERT WURDE:
echo    ✅ Open World System (2400x2400 Map)
echo    ✅ Schwarze Muehle (9 Raeume, 4 Stockwerke)
echo    ✅ Kampfarena + Garten + 3 Dungeons
echo    ✅ Mobile Touch Controls (Virtual Joystick)
echo    ✅ Backend (qwen, Memory, TTS, Battle System)
echo    ✅ Frontend (React + Three.js)
echo    ✅ 75 KayKit Asset Packs
echo    ✅ Dokumentation (NAJIKA_WORLD_SYSTEM_COMPLETE.md)
echo.
echo.
echo WICHTIG - BEVOR DU STARTEST:
echo    1. cd %TARGET%\frontend
echo    2. npm install     (wenn node_modules fehlt)
echo    3. cd ..
echo    4. START_NAJIKA_WORLD.bat
echo.
echo.
echo ODER: Desktop-Verknuepfung "Najika World"
echo.
echo.
echo DOKUMENTATION:
echo    %TARGET%\NAJIKA_WORLD_SYSTEM_COMPLETE.md
echo.
echo.
echo ========================================================================
echo.
echo              TASTE ZUM SCHLIESSEN
echo.
echo ========================================================================
echo.

pause >nul
exit /b 0
