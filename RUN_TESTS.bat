@echo off
chcp 65001 >nul
cls

echo ========================================
echo  NAJIKA WORLD - Test Suite
echo ========================================
echo.

cd /d "%~dp0"

echo Running Integration Check...
echo ========================================
python CHECK_INTEGRATION.py

echo.
echo.
echo ========================================
echo Do you want to run API tests?
echo (Backend must be running!)
echo ========================================
echo.
set /p run_api="Run API Tests? (y/n): "

if /i "%run_api%"=="y" (
    echo.
    echo Running API Tests...
    echo ========================================
    python TEST_MAGIC_SYSTEM_V3.py
)

echo.
echo ========================================
echo Tests completed!
echo ========================================
pause
