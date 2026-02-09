@echo off
title FLUTTER SDK SETUP für Najika Digivice
color 0B
cd /d "%~dp0"

echo.
echo ================================================================================
echo                 FLUTTER SDK INSTALLATION für Najika Digivice
echo ================================================================================
echo.
echo Dieses Script lädt Flutter herunter und konfiguriert es.
echo.

REM Prüfe ob Flutter bereits installiert ist
where flutter >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Flutter ist bereits installiert!
    flutter --version
    echo.
    goto :BUILD_APP
)

echo [INFO] Flutter nicht gefunden - starte Download...
echo.

REM Setze Flutter Pfad
set FLUTTER_DIR=C:\flutter
set FLUTTER_ZIP=%TEMP%\flutter_windows.zip

REM Prüfe ob bereits heruntergeladen
if exist "%FLUTTER_DIR%\bin\flutter.bat" (
    echo [OK] Flutter bereits in %FLUTTER_DIR% vorhanden
    goto :ADD_PATH
)

REM Download Flutter
echo [1/4] Lade Flutter SDK herunter...
echo       (ca. 1.1 GB - kann einige Minuten dauern)
echo.

REM Nutze curl für den Download
curl -L -o "%FLUTTER_ZIP%" "https://storage.googleapis.com/flutter_infra_release/releases/stable/windows/flutter_windows_3.24.5-stable.zip"

if not exist "%FLUTTER_ZIP%" (
    echo [ERROR] Download fehlgeschlagen!
    echo         Bitte Flutter manuell von https://flutter.dev/docs/get-started/install herunterladen.
    pause
    exit /b 1
)

echo.
echo [2/4] Entpacke Flutter SDK nach %FLUTTER_DIR%...
echo       (kann einige Minuten dauern)
echo.

REM Erstelle Zielverzeichnis
if not exist "C:\" mkdir "C:\" 2>nul

REM Entpacke mit PowerShell
powershell -Command "Expand-Archive -Path '%FLUTTER_ZIP%' -DestinationPath 'C:\' -Force"

if not exist "%FLUTTER_DIR%\bin\flutter.bat" (
    echo [ERROR] Entpacken fehlgeschlagen!
    pause
    exit /b 1
)

echo [OK] Flutter entpackt!

:ADD_PATH
echo.
echo [3/4] Füge Flutter zum PATH hinzu...

REM Füge zum User PATH hinzu
setx PATH "%PATH%;%FLUTTER_DIR%\bin" >nul 2>&1

REM Temporär für diese Session
set PATH=%PATH%;%FLUTTER_DIR%\bin

echo [OK] PATH aktualisiert!
echo.

echo [4/4] Führe Flutter doctor aus...
echo.

call "%FLUTTER_DIR%\bin\flutter.bat" doctor

echo.
echo ================================================================================
echo                      FLUTTER INSTALLATION ABGESCHLOSSEN!
echo ================================================================================
echo.
echo Flutter wurde nach %FLUTTER_DIR% installiert.
echo.
echo WICHTIG: Öffne ein NEUES Terminal damit der PATH aktiv wird!
echo.

:BUILD_APP
echo.
echo ================================================================================
echo                        APK BUILD OPTIONEN
echo ================================================================================
echo.
echo Was möchtest du tun?
echo.
echo [1] Flutter pub get (Dependencies installieren)
echo [2] APK bauen (Master Edition)
echo [3] APK bauen (Trusted Edition)
echo [4] APK bauen (Public Edition)
echo [5] Alle 3 Versionen bauen
echo [6] Beenden
echo.

set /p CHOICE="Wähle (1-6): "

if "%CHOICE%"=="1" goto :PUB_GET
if "%CHOICE%"=="2" goto :BUILD_MASTER
if "%CHOICE%"=="3" goto :BUILD_TRUSTED
if "%CHOICE%"=="4" goto :BUILD_PUBLIC
if "%CHOICE%"=="5" goto :BUILD_ALL
if "%CHOICE%"=="6" goto :END

echo Ungültige Auswahl!
goto :BUILD_APP

:PUB_GET
echo.
echo [INFO] Installiere Dependencies...
cd "%~dp0flutter_app\najika_digivice"
call flutter pub get
echo [OK] Dependencies installiert!
goto :BUILD_APP

:BUILD_MASTER
echo.
echo [INFO] Baue Master Edition...
cd "%~dp0flutter_app\najika_digivice"
call flutter build apk --release
echo.
echo [OK] APK erstellt: build\app\outputs\flutter-apk\app-release.apk
if not exist "%~dp0builds" mkdir "%~dp0builds"
copy "build\app\outputs\flutter-apk\app-release.apk" "%~dp0builds\najika_digivice_master.apk" >nul
echo [OK] Kopiert nach: builds\najika_digivice_master.apk
goto :BUILD_APP

:BUILD_TRUSTED
echo.
echo [INFO] Baue Trusted Edition...
echo [TODO] build_config.dart auf trusted setzen...
cd "%~dp0flutter_app\najika_digivice"
call flutter build apk --release
if not exist "%~dp0builds" mkdir "%~dp0builds"
copy "build\app\outputs\flutter-apk\app-release.apk" "%~dp0builds\najika_digivice_trusted.apk" >nul
echo [OK] Kopiert nach: builds\najika_digivice_trusted.apk
goto :BUILD_APP

:BUILD_PUBLIC
echo.
echo [INFO] Baue Public Edition...
echo [TODO] build_config.dart auf public setzen...
cd "%~dp0flutter_app\najika_digivice"
call flutter build apk --release
if not exist "%~dp0builds" mkdir "%~dp0builds"
copy "build\app\outputs\flutter-apk\app-release.apk" "%~dp0builds\najika_digivice_public.apk" >nul
echo [OK] Kopiert nach: builds\najika_digivice_public.apk
goto :BUILD_APP

:BUILD_ALL
echo.
echo [INFO] Baue alle 3 Versionen...
cd "%~dp0build_scripts"
powershell -ExecutionPolicy Bypass -File "build_all_versions.ps1"
goto :BUILD_APP

:END
echo.
echo Auf Wiedersehen!
pause
