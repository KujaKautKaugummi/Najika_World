@echo off
echo ================================================================================
echo NAJIKA AUTO-TRAINING AKTIVIEREN v2.0
echo ================================================================================
echo.
echo Schedule:
echo - Code Training:  TAEGLICH ab 08:00 Uhr (~45 Min)
echo - LoRA Training:  SONNTAG ab 08:00 Uhr (~2h, blockiert GPU)
echo - Failsafe:       Stuendlich
echo.
echo Der Launcher wird STUENDLICH aufgerufen und prueft selbst
echo ob die richtige Uhrzeit/Tag fuer Training ist.
echo.
echo WICHTIG: Benoetigt Administrator-Rechte!
echo.
pause
echo.
echo [1/4] Loesche alte Tasks falls vorhanden...
schtasks /Delete /TN "NajikaTraining16h" /F 2>nul
schtasks /Delete /TN "NajikaMasterTrainingLauncher" /F 2>nul
echo.
echo [2/4] Erstelle neuen Task...
schtasks /Create /TN "NajikaMasterTrainingLauncher" /TR "python C:\Najika_World\backend\NAJIKA_MASTER_TRAINING_LAUNCHER.py" /SC HOURLY /ST 08:00 /F
echo.
echo [3/4] Pruefe Task-Status...
schtasks /Query /TN "NajikaMasterTrainingLauncher" /V /FO LIST
echo.
echo [4/4] Starte ersten Run jetzt...
python C:\Najika_World\backend\NAJIKA_MASTER_TRAINING_LAUNCHER.py
echo.
echo ================================================================================
echo FERTIG! Training-Schedule:
echo   Code:  Taeglich ab 08:00 (1x pro Tag)
echo   LoRA:  Sonntag ab 08:00 (1x pro Woche)
echo ================================================================================
echo.
echo Task deaktivieren: schtasks /Change /TN "NajikaMasterTrainingLauncher" /DISABLE
echo Task aktivieren:   schtasks /Change /TN "NajikaMasterTrainingLauncher" /ENABLE
echo.
pause
