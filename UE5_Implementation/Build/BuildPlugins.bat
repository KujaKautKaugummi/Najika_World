@echo off
REM Build Automation Script: NajikaBackendClient Plugin
REM Copyright Claude Code. All Rights Reserved.
REM Platform: Windows
REM Usage: BuildPlugins.bat

echo ========================================
echo Najika Digivice - Build Plugins
echo ========================================
echo.

REM Set UE5 Editor path (adjust if needed)
set UE5_EDITOR="C:\Program Files\Epic Games\UE_5.4\Engine\Binaries\Win64\UnrealEditor-Cmd.exe"

REM Set project path
set PROJECT_DIR=%~dp0..
set PROJECT_FILE=%PROJECT_DIR%\NajikaDigivice.uproject
set PLUGIN_DIR=%PROJECT_DIR%\Plugins\NajikaBackendClient

echo Project Directory: %PROJECT_DIR%
echo Plugin Directory: %PLUGIN_DIR%
echo.

REM Check if UE5 Editor exists
if not exist %UE5_EDITOR% (
    echo ERROR: UE5 Editor not found at %UE5_EDITOR%
    echo Please update UE5_EDITOR variable in this script
    pause
    exit /b 1
)

REM Check if plugin directory exists
if not exist "%PLUGIN_DIR%" (
    echo ERROR: Plugin directory not found: %PLUGIN_DIR%
    pause
    exit /b 1
)

echo Building NajikaBackendClient plugin...
echo.

REM Build plugin using UnrealBuildTool
%UE5_EDITOR% "%PROJECT_FILE%" -run=BuildPlugin -plugin="%PLUGIN_DIR%\NajikaBackendClient.uplugin" -package="%PROJECT_DIR%\Plugins\Built\NajikaBackendClient" -rocket

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Plugin build failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Plugin build successful!
echo Output: %PROJECT_DIR%\Plugins\Built\NajikaBackendClient
echo ========================================
pause
