@echo off
REM ============================================
REM NAJIKA TASK CLEANUP - ADMIN ERFORDERLICH
REM ============================================

echo.
echo Starte Task Cleanup als Administrator...
echo.
echo WARNUNG: Dieses Script loescht ALLE Najika-Tasks
echo und erstellt nur die 2 richtigen neu!
echo.

powershell -ExecutionPolicy Bypass -Command "Start-Process powershell -ArgumentList '-NoExit -ExecutionPolicy Bypass -File C:\Najika\CLEANUP_ALL_TASKS.ps1' -Verb RunAs"

echo.
echo PowerShell-Fenster sollte sich als Admin oeffnen.
echo Bitte dort die Abfrage bestaetigen!
echo.
pause
