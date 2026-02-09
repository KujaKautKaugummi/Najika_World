@echo off
title Najika CLI - Beautiful Edition
chcp 65001 >nul
color 0D

REM ========================================
REM   NAJIKA CLI - BEAUTIFUL EDITION
REM   Gothic-Lolita Terminal Interface
REM ========================================

REM Check if message provided
if "%~1"=="" (
    REM Show help via Python CLI
    python "C:\Najika_World\backend\najika_cli_beautiful.py"
    exit /b
)

REM Run beautiful CLI
python "C:\Najika_World\backend\najika_cli_beautiful.py" %*
