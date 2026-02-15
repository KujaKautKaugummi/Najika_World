@echo off
chcp 65001 >nul
cls

echo.
echo    ███╗   ██╗ █████╗      ██╗██╗██╗  ██╗ █████╗
echo    ████╗  ██║██╔══██╗     ██║██║██║ ██╔╝██╔══██╗
echo    ██╔██╗ ██║███████║     ██║██║█████╔╝ ███████║
echo    ██║╚██╗██║██╔══██║██   ██║██║██╔═██╗ ██╔══██║
echo    ██║ ╚████║██║  ██║╚█████╔╝██║██║  ██╗██║  ██║
echo    ╚═╝  ╚═══╝╚═╝  ╚═╝ ╚════╝ ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
echo.
echo    NAJIKA WORLD - Magic/Skill System V3
echo    ========================================
echo.

cd /d "%~dp0"

:menu
echo    [1] Start Backend Only
echo    [2] Start Complete System (Backend + Browser)
echo    [3] Run Tests
echo    [4] Open API Docs (Backend must be running)
echo    [5] Check Integration
echo    [0] Exit
echo.
set /p choice="    Select option: "

if "%choice%"=="1" goto start_backend
if "%choice%"=="2" goto start_complete
if "%choice%"=="3" goto run_tests
if "%choice%"=="4" goto open_docs
if "%choice%"=="5" goto check_integration
if "%choice%"=="0" goto end
goto menu

:start_backend
cls
echo Starting Backend...
start "Najika Backend" cmd /k "cd /d %~dp0 && python backend\main_fastapi.py"
timeout /t 2 >nul
goto menu

:start_complete
cls
echo Starting Complete System...
start "Najika Backend" cmd /k "cd /d %~dp0 && python backend\main_fastapi.py"
timeout /t 3 >nul
start http://localhost:8000/digivice/
echo Complete system started!
timeout /t 2 >nul
goto menu

:run_tests
cls
python CHECK_INTEGRATION.py
echo.
pause
goto menu

:open_docs
cls
echo Opening API Docs...
start http://localhost:8000/docs
timeout /t 1 >nul
goto menu

:check_integration
cls
python CHECK_INTEGRATION.py
echo.
pause
goto menu

:end
echo.
echo Goodbye!
timeout /t 1 >nul
exit
