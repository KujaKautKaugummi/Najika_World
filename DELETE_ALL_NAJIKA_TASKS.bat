@echo off
echo.
echo Loesche ALLE Najika Tasks...
echo.

for /f "tokens=1* delims=\" %%a in ('schtasks /query /fo list ^| findstr /i "Najika"') do (
    schtasks /Delete /TN "%%b" /F >nul 2>&1
    if !errorlevel! == 0 echo Geloescht: %%b
)

echo.
echo Fertig!
pause
