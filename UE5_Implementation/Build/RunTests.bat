@echo off
REM Test Automation Script: Run All Tests
REM Copyright Claude Code. All Rights Reserved.
REM Platform: Windows
REM Usage: RunTests.bat [-quick]

echo ========================================
echo Najika Digivice - Run Tests
echo ========================================
echo.

REM Set UE5 paths
set UE5_EDITOR="C:\Program Files\Epic Games\UE_5.4\Engine\Binaries\Win64\UnrealEditor-Cmd.exe"

REM Set project path
set PROJECT_DIR=%~dp0..
set PROJECT_FILE=%PROJECT_DIR%\NajikaDigivice.uproject
set TEST_REPORT_DIR=%PROJECT_DIR%\TestReports

REM Set test filter (default: all Najika tests)
set TEST_FILTER=Najika

REM Check for -quick flag
if "%1"=="-quick" (
    set TEST_FILTER=Najika.Unit
    echo Running QUICK tests only Unit tests...
) else (
    echo Running ALL tests Unit + Integration...
)

echo.
echo Test Filter: %TEST_FILTER%
echo Report Output: %TEST_REPORT_DIR%
echo.

REM Create test report directory
if not exist "%TEST_REPORT_DIR%" mkdir "%TEST_REPORT_DIR%"

REM Check if UE5 Editor exists
if not exist %UE5_EDITOR% (
    echo ERROR: UE5 Editor not found at %UE5_EDITOR%
    echo Please update UE5_EDITOR variable in this script
    pause
    exit /b 1
)

REM Check if project file exists
if not exist "%PROJECT_FILE%" (
    echo ERROR: Project file not found: %PROJECT_FILE%
    pause
    exit /b 1
)

echo Running tests...
echo.

REM Run automation tests
%UE5_EDITOR% "%PROJECT_FILE%" ^
    -ExecCmds="Automation RunTests %TEST_FILTER%" ^
    -unattended ^
    -nopause ^
    -testexit="Automation Test Queue Empty" ^
    -log ^
    -ReportOutputPath="%TEST_REPORT_DIR%"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Some tests failed!
    echo Check test report at: %TEST_REPORT_DIR%
    pause
    exit /b 1
)

echo.
echo ========================================
echo All tests passed!
echo Report: %TEST_REPORT_DIR%\index.html
echo ========================================
pause
