@echo off
REM ========================================
REM NAJIKA MERGE - STEP 3: TEST
REM Testet die zusammengeführte Installation
REM ========================================

echo.
echo ========================================
echo    NAJIKA MERGE - TESTEN
echo ========================================
echo.

echo Teste neue Struktur...
echo.

REM Test 1: Backend existiert
echo [Test 1/5] Backend Ordner...
if exist "C:\Najika\backend\najika_server.py" (
    echo ✓ Backend existiert
) else (
    echo ✗ FEHLER: Backend nicht gefunden!
    goto :error
)

REM Test 2: Frontend existiert
echo [Test 2/5] Frontend Ordner...
if exist "C:\Najika\frontend\package.json" (
    echo ✓ Frontend existiert
) else (
    echo ✗ FEHLER: Frontend nicht gefunden!
    goto :error
)

REM Test 3: Launcher existiert
echo [Test 3/5] Launcher...
if exist "C:\Najika\START_NAJIKA.bat" (
    echo ✓ Launcher existiert
) else (
    echo ✗ FEHLER: Launcher nicht gefunden!
    goto :error
)

REM Test 4: Docs existiert
echo [Test 4/5] Dokumentation...
if exist "C:\Najika\DOCS" (
    echo ✓ DOCS Ordner existiert
) else (
    echo ! WARNUNG: DOCS Ordner fehlt
)

REM Test 5: README existiert
echo [Test 5/5] README...
if exist "C:\Najika\README.md" (
    echo ✓ README existiert
) else (
    echo ! WARNUNG: README fehlt
)

echo.
echo ========================================
echo    ALLE TESTS BESTANDEN!
echo ========================================
echo.
echo Struktur ist korrekt!
echo.
echo NÄCHSTER SCHRITT:
echo 1. Starte START_NAJIKA.bat
echo 2. Warte bis beide Server laufen
echo 3. Öffne http://localhost:3002
echo 4. Teste Commands (1-4 Keys)
echo 5. Teste "START BATTLE" Button
echo.
echo Wenn alles funktioniert:
echo - C:\NajikaCore\ kann gelöscht werden
echo - Backup in C:\Najika_Backups\ behalten
echo.
pause
goto :eof

:error
echo.
echo ========================================
echo    TEST FEHLGESCHLAGEN!
echo ========================================
echo.
echo Bitte Merge wiederholen oder Backup wiederherstellen!
echo.
pause
exit /b 1
