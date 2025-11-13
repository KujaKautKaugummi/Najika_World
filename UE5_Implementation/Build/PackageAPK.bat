@echo off
REM Package Automation Script: Android APK
REM Copyright Claude Code. All Rights Reserved.
REM Platform: Android (Xiaomi 11T Pro - Snapdragon 888)
REM Usage: PackageAPK.bat [Development|Shipping]

echo ========================================
echo Najika Digivice - Package Android APK
echo ========================================
echo.

REM Set default configuration
set BUILD_CONFIG=Development
if not "%1"=="" set BUILD_CONFIG=%1

REM Set UE5 paths
set UE5_EDITOR="C:\Program Files\Epic Games\UE_5.4\Engine\Binaries\Win64\UnrealEditor-Cmd.exe"
set UE5_UAT="C:\Program Files\Epic Games\UE_5.4\Engine\Build\BatchFiles\RunUAT.bat"

REM Set project path
set PROJECT_DIR=%~dp0..
set PROJECT_FILE=%PROJECT_DIR%\NajikaDigivice.uproject
set OUTPUT_DIR=%PROJECT_DIR%\Build\Android

echo Project: NajikaDigivice
echo Configuration: %BUILD_CONFIG%
echo Platform: Android (ARM64)
echo Target Device: Xiaomi 11T Pro (Snapdragon 888)
echo Output: %OUTPUT_DIR%
echo.

REM Check if UE5 UAT exists
if not exist %UE5_UAT% (
    echo ERROR: UnrealAutomationTool not found at %UE5_UAT%
    echo Please update UE5_UAT variable in this script
    pause
    exit /b 1
)

REM Check if project file exists
if not exist "%PROJECT_FILE%" (
    echo ERROR: Project file not found: %PROJECT_FILE%
    pause
    exit /b 1
)

REM Create output directory
if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

echo Packaging Android APK...
echo This may take 10-20 minutes...
echo.

REM Package for Android using UAT
call %UE5_UAT% BuildCookRun ^
    -project="%PROJECT_FILE%" ^
    -platform=Android ^
    -clientconfig=%BUILD_CONFIG% ^
    -cook ^
    -stage ^
    -package ^
    -archive ^
    -archivedirectory="%OUTPUT_DIR%" ^
    -build ^
    -pak ^
    -prereqs ^
    -nodebuginfo ^
    -targetplatform=Android_ASTC

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: APK packaging failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo APK packaged successfully!
echo Output: %OUTPUT_DIR%\NajikaDigivice-Android.apk
echo ========================================
echo.
echo Next steps:
echo 1. Connect your Xiaomi 11T Pro via USB
echo 2. Enable USB Debugging on device
echo 3. Run DeployToDevice.bat to install APK
echo.
pause
