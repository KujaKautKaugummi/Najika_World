@echo off
REM Master Build Script: Build Everything
REM Copyright Claude Code. All Rights Reserved.
REM Platform: Windows
REM Usage: BuildAll.bat

echo ========================================
echo Najika Digivice - Build All
echo ========================================
echo.

set BUILD_DIR=%~dp0

echo This script will:
echo 1. Build plugins
echo 2. Build project (C++)
echo 3. Run tests
echo 4. Package Android APK (optional)
echo.
echo Press any key to continue or Ctrl+C to cancel...
pause >nul

REM Step 1: Build Plugins
echo.
echo ========================================
echo Step 1/3: Building Plugins...
echo ========================================
call "%BUILD_DIR%\BuildPlugins.bat"
if %ERRORLEVEL% NEQ 0 (
    echo Plugin build failed!
    pause
    exit /b 1
)

REM Step 2: Build Project
echo.
echo ========================================
echo Step 2/3: Building Project...
echo ========================================
call "%BUILD_DIR%\BuildProject.bat" Development
if %ERRORLEVEL% NEQ 0 (
    echo Project build failed!
    pause
    exit /b 1
)

REM Step 3: Run Tests
echo.
echo ========================================
echo Step 3/3: Running Tests...
echo ========================================
call "%BUILD_DIR%\RunTests.bat"
if %ERRORLEVEL% NEQ 0 (
    echo Tests failed!
    pause
    exit /b 1
)

REM Optional: Package Android APK
echo.
echo ========================================
echo All builds completed successfully!
echo ========================================
echo.
echo Do you want to package Android APK? (Y/N)
set /p PACKAGE_APK=
if /i "%PACKAGE_APK%"=="Y" (
    echo.
    echo ========================================
    echo Packaging Android APK...
    echo ========================================
    call "%BUILD_DIR%\PackageAPK.bat" Development
    if %ERRORLEVEL% NEQ 0 (
        echo APK packaging failed!
        pause
        exit /b 1
    )
)

echo.
echo ========================================
echo SUCCESS! All tasks completed!
echo ========================================
echo.
echo Build artifacts:
echo - Plugins: ..\Plugins\Built\NajikaBackendClient
echo - Project: ..\Binaries\Win64\NajikaDigivice.exe
echo - Tests: ..\TestReports\index.html
if /i "%PACKAGE_APK%"=="Y" (
    echo - APK: ..\Build\Android\NajikaDigivice-Android.apk
)
echo.
pause
