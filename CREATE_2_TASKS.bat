@echo off
echo.
echo Erstelle 2 Training Tasks...
echo.

REM Nacht: 00:00, taeglich
schtasks /Create /TN "NajikaTrainingNacht" /TR "python C:\Najika\backend\najika_smart_training_scheduler.py --train" /SC DAILY /ST 00:00 /F
echo [OK] NajikaTrainingNacht

REM Tag: 08:00, Mo-Fr (via PowerShell wegen Wochentagen)
powershell -Command "$a=New-ScheduledTaskAction -Execute 'python' -Argument 'C:\Najika\backend\najika_smart_training_scheduler.py --train' -WorkingDirectory 'C:\Najika\backend'; $t=New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday,Tuesday,Wednesday,Thursday,Friday -At 08:00; $s=New-ScheduledTaskSettingsSet -ExecutionTimeLimit (New-TimeSpan -Hours 7); Register-ScheduledTask -TaskName 'NajikaTrainingTag' -Action $a -Trigger $t -Settings $s -Force" >nul
echo [OK] NajikaTrainingTag

echo.
echo Fertig!
pause
