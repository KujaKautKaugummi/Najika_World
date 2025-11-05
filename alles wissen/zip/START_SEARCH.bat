@echo off
cls
echo ==============================================================
echo          NAJIKA PROJECT SEARCH
echo ==============================================================
echo.
echo Starte Suche im Ordner: %~dp0
echo.
echo Das Script durchsucht alle Dateien nach:
echo   - Najika Projekt-Komponenten
echo   - Gameplay-Mechaniken
echo   - Klassen und Skills
echo   - Crafting, Fishing, Farming
echo   - Digivice System
echo   - Schwarze Muehle
echo   - UEFN Komponenten
echo   - Und VIEL mehr!
echo.
echo ==============================================================
echo.
echo Druecke eine beliebige Taste zum Starten...
pause >nul

echo.
echo Starte Suche...
echo.

call "%~dp0NAJIKA_SEARCH.bat"
