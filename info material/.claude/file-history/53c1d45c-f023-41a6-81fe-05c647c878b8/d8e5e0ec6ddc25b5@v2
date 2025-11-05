@echo off
REM WINDOWS DEFENDER AUSNAHME fuer Najika Training
REM Muss als Administrator ausgefuehrt werden!

echo ================================================================================
echo WINDOWS DEFENDER AUSNAHME HINZUFUEGEN
echo ================================================================================
echo.
echo Fuegt C:\Najika-World als Ausnahme hinzu, damit Training nicht blockiert wird.
echo.
echo WICHTIG: Rechtsklick auf diese Datei -^> "Als Administrator ausfuehren"
echo.
pause

REM Pruefe Admin-Rechte
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo.
    echo [FEHLER] Keine Admin-Rechte!
    echo Bitte Rechtsklick -^> "Als Administrator ausfuehren"
    echo.
    pause
    exit /b 1
)

echo.
echo Fuege Ausnahmen hinzu...
echo.

REM Ordner-Ausnahme
powershell -Command "Add-MpPreference -ExclusionPath 'C:\Najika-World'"
echo [OK] Ordner C:\Najika-World ausgeschlossen

REM Python-Prozess Ausnahme (optional)
powershell -Command "Add-MpPreference -ExclusionProcess 'python.exe'"
echo [OK] python.exe Prozess ausgeschlossen

echo.
echo ================================================================================
echo FERTIG! Windows Defender wird Najika-Training nicht mehr blockieren.
echo ================================================================================
echo.
echo Du kannst jetzt START_NIGHT_TRAINING.bat ausfuehren!
echo.
pause
