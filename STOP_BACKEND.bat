@echo off
chcp 65001 >nul
cls

echo ========================================
echo  NAJIKA WORLD - Stop Backend
echo ========================================
echo.
echo Stopping all Python processes on port 8000...
echo.

:: Find and kill process on port 8000
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    echo Killing process: %%a
    taskkill /PID %%a /F
)

echo.
echo ========================================
echo Backend stopped!
echo ========================================
pause
