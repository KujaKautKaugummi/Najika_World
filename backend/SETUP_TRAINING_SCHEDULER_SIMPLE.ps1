# NAJIKA TRAINING - WINDOWS TASK SCHEDULER SETUP
# BOMBENFEST - LAEUFT EWIG!

Write-Host "=" -ForegroundColor Green
Write-Host "NAJIKA TRAINING - TASK SCHEDULER SETUP" -ForegroundColor Yellow
Write-Host "=" -ForegroundColor Green

# Config
$TaskName = "NajikaMasterTrainingLauncher"
$PythonScript = "C:\Najika_World\backend\NAJIKA_MASTER_TRAINING_LAUNCHER.py"
$WorkingDir = "C:\Najika_World\backend"

# Loesche alte Task
Write-Host "[1] Loesche alte Task..." -ForegroundColor Cyan
try {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue
    Write-Host "OK: Alte Task geloescht" -ForegroundColor Green
} catch {
    Write-Host "INFO: Keine alte Task gefunden" -ForegroundColor Gray
}

# Erstelle neue Task
Write-Host "[2] Erstelle neue Task..." -ForegroundColor Cyan

$action = New-ScheduledTaskAction -Execute "python" -Argument $PythonScript -WorkingDirectory $WorkingDir

$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Hours 1)

$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -RunLevel Highest

Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Force

Write-Host "OK: Task erstellt!" -ForegroundColor Green

# Starte Task
Write-Host "[3] Starte Task..." -ForegroundColor Cyan
Start-ScheduledTask -TaskName $TaskName
Write-Host "OK: Task gestartet!" -ForegroundColor Green

# Zeige Status
Write-Host "[4] Status:" -ForegroundColor Cyan
$task = Get-ScheduledTask -TaskName $TaskName
Write-Host "State: $($task.State)" -ForegroundColor Gray
Write-Host "Next Run: $($task.NextRunTime)" -ForegroundColor Gray

Write-Host ""
Write-Host "FERTIG! Training laeuft jetzt stuendlich!" -ForegroundColor Yellow
Write-Host ""
