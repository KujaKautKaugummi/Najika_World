# NAJIKA NIGHT TRAINING - TAEGLICH 00:00 UHR

Write-Host "NAJIKA NIGHT TRAINING SETUP" -ForegroundColor Yellow

$TaskName = "NajikaIntensiveNightTraining"
$PythonScript = "C:\Najika_World\backend\najika_intensive_night_training.py"
$WorkingDir = "C:\Najika_World\backend"

# Loesche alte Task
Write-Host "[1] Loesche alte Task..." -ForegroundColor Cyan
Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue

# Erstelle neue Task
Write-Host "[2] Erstelle neue Task..." -ForegroundColor Cyan

$action = New-ScheduledTaskAction -Execute "python" -Argument $PythonScript -WorkingDirectory $WorkingDir

$trigger = New-ScheduledTaskTrigger -Daily -At "00:00"

$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Hours 10)

$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -RunLevel Highest

Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Force

Write-Host "OK: Task erstellt!" -ForegroundColor Green

# Zeige Status
Write-Host "[3] Status:" -ForegroundColor Cyan
$task = Get-ScheduledTask -TaskName $TaskName
Write-Host "State: $($task.State)" -ForegroundColor Gray
Write-Host "Next Run: $($task.NextRunTime)" -ForegroundColor Gray

Write-Host ""
Write-Host "FERTIG! Nacht-Training startet taeglich um 00:00 Uhr!" -ForegroundColor Yellow
Write-Host "Dauer: 8-10 Stunden (Phase 1-5)" -ForegroundColor Gray
Write-Host ""
