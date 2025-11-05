@echo off
REM ========================================
REM NAJIKA MERGE - STEP 1: BACKUP
REM Erstellt Backups von beiden Projekten
REM ========================================

echo.
echo ========================================
echo    NAJIKA MERGE - BACKUP ERSTELLEN
echo ========================================
echo.

REM Hole aktuelles Datum/Zeit
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"
set "datestamp=%YYYY%-%MM%-%DD%_%HH%-%Min%-%Sec%"

REM Backup-Pfade
set "BACKUP_DIR=C:\Najika_Backups"
set "BACKUP_NAJIKA=%BACKUP_DIR%\Najika_%datestamp%"
set "BACKUP_CORE=%BACKUP_DIR%\NajikaCore_%datestamp%"

echo Erstelle Backup-Verzeichnis...
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

echo.
echo [1/2] Backup von C:\Najika...
echo Ziel: %BACKUP_NAJIKA%
xcopy "C:\Najika" "%BACKUP_NAJIKA%\" /E /I /H /Y /Q
if %ERRORLEVEL% NEQ 0 (
    echo FEHLER: Backup von Najika fehlgeschlagen!
    pause
    exit /b 1
)
echo ✓ Najika gesichert

echo.
echo [2/2] Backup von C:\NajikaCore...
echo Ziel: %BACKUP_CORE%
xcopy "C:\NajikaCore" "%BACKUP_CORE%\" /E /I /H /Y /Q
if %ERRORLEVEL% NEQ 0 (
    echo FEHLER: Backup von NajikaCore fehlgeschlagen!
    pause
    exit /b 1
)
echo ✓ NajikaCore gesichert

echo.
echo ========================================
echo    BACKUP ERFOLGREICH!
echo ========================================
echo.
echo Backup-Ordner: %BACKUP_DIR%
echo.
echo Gesichert:
echo - %BACKUP_NAJIKA%
echo - %BACKUP_CORE%
echo.
echo Weiter mit MERGE_02_EXECUTE.bat
echo.
pause
