@echo off
REM Build Automation Script: Full Project Build
REM Copyright Claude Code. All Rights Reserved.
REM Platform: Windows
REM Usage: BuildProject.bat [Development|Shipping]

echo ========================================
echo Najika Digivice - Build Project
echo ========================================
echo.

REM Set default configuration
set BUILD_CONFIG=Development
if not "%1"=="" set BUILD_CONFIG=%1

REM Set UE5 paths
set UE5_EDITOR="C:\Program Files\Epic Games\UE_5.4\Engine\Binaries\Win64\UnrealEditor-Cmd.exe"
set UE5_BUILD_TOOL="C:\Program Files\Epic Games\UE_5.4\Engine\Binaries\DotNET\UnrealBuildTool\UnrealBuildTool.exe"

REM Set project path
set PROJECT_DIR=%~dp0..
set PROJECT_FILE=%PROJECT_DIR%\NajikaDigivice.uproject
set PROJECT_NAME=NajikaDigivice

echo Project: %PROJECT_NAME%
echo Configuration: %BUILD_CONFIG%
echo Platform: Win64
echo.

REM Check if UE5 Build Tool exists
if not exist %UE5_BUILD_TOOL% (
    echo ERROR: UnrealBuildTool not found at %UE5_BUILD_TOOL%
    echo Please update UE5_BUILD_TOOL variable in this script
    pause
    exit /b 1
)

REM Check if project file exists
if not exist "%PROJECT_FILE%" (
    echo ERROR: Project file not found: %PROJECT_FILE%
    pause
    exit /b 1
)

echo Building C++ project...
echo.

REM Build project using UnrealBuildTool
%UE5_BUILD_TOOL% %PROJECT_NAME% Win64 %BUILD_CONFIG% -project="%PROJECT_FILE%" -progress -noubtmakefiles

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Build successful!
echo Configuration: %BUILD_CONFIG%
echo Platform: Win64
echo ========================================
pause
