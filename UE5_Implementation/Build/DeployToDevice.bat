@echo off
REM Deploy Automation Script: Install APK to Android Device
REM Copyright Claude Code. All Rights Reserved.
REM Platform: Android (Xiaomi 11T Pro)
REM Usage: DeployToDevice.bat

echo ========================================
echo Najika Digivice - Deploy to Android
echo ========================================
echo.

REM Set paths
set PROJECT_DIR=%~dp0..
set APK_DIR=%PROJECT_DIR%\Build\Android
set ADB="C:\Users\%USERNAME%\AppData\Local\Android\Sdk\platform-tools\adb.exe"

REM Find APK file
set APK_FILE=%APK_DIR%\NajikaDigivice-Android.apk

echo APK File: %APK_FILE%
echo.

REM Check if ADB exists
if not exist %ADB% (
    echo ERROR: ADB not found at %ADB%
    echo Please install Android SDK Platform Tools
    echo Download from: https://developer.android.com/studio/releases/platform-tools
    pause
    exit /b 1
)

REM Check if APK exists
if not exist "%APK_FILE%" (
    echo ERROR: APK file not found: %APK_FILE%
    echo Please run PackageAPK.bat first to create the APK
    pause
    exit /b 1
)

echo Checking for connected devices...
%ADB% devices
echo.

REM Wait for device
%ADB% wait-for-device
echo Device connected!
echo.

echo Installing APK...
%ADB% install -r "%APK_FILE%"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: APK installation failed!
    echo Make sure USB Debugging is enabled on your device
    pause
    exit /b 1
)

echo.
echo ========================================
echo APK installed successfully!
echo ========================================
echo.
echo Starting app...
%ADB% shell am start -n com.YourCompany.NajikaDigivice/com.epicgames.unreal.GameActivity

echo.
echo App launched on device!
echo.
echo To view logs:
echo   adb logcat -s UE
echo.
pause
