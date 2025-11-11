# CHECK NAJIKA TRAINING STATUS

Write-Host "="*80 -ForegroundColor Green
Write-Host "NAJIKA TRAINING STATUS CHECK" -ForegroundColor Yellow
Write-Host "="*80 -ForegroundColor Green
Write-Host ""

# Master Training Task
Write-Host "[1] MASTER TRAINING LAUNCHER:" -ForegroundColor Cyan
try {
    $task1 = Get-ScheduledTask -TaskName "NajikaMasterTrainingLauncher" -ErrorAction Stop
    $info1 = Get-ScheduledTaskInfo -TaskName "NajikaMasterTrainingLauncher" -ErrorAction Stop

    Write-Host "   Task Name: $($task1.TaskName)" -ForegroundColor Gray
    Write-Host "   State: $($task1.State)" -ForegroundColor $(if($task1.State -eq 'Running'){'Green'}else{'Yellow'})
    Write-Host "   Last Run: $($info1.LastRunTime)" -ForegroundColor Gray
    Write-Host "   Next Run: $($info1.NextRunTime)" -ForegroundColor Gray
    Write-Host "   Last Result: $($info1.LastTaskResult)" -ForegroundColor Gray
} catch {
    Write-Host "   ERROR: Task nicht gefunden!" -ForegroundColor Red
}

Write-Host ""

# Night Training Task
Write-Host "[2] INTENSIVE NIGHT TRAINING:" -ForegroundColor Cyan
try {
    $task2 = Get-ScheduledTask -TaskName "NajikaIntensiveNightTraining" -ErrorAction Stop
    $info2 = Get-ScheduledTaskInfo -TaskName "NajikaIntensiveNightTraining" -ErrorAction Stop

    Write-Host "   Task Name: $($task2.TaskName)" -ForegroundColor Gray
    Write-Host "   State: $($task2.State)" -ForegroundColor $(if($task2.State -eq 'Ready'){'Green'}else{'Yellow'})
    Write-Host "   Last Run: $($info2.LastRunTime)" -ForegroundColor Gray
    Write-Host "   Next Run: $($info2.NextRunTime)" -ForegroundColor Gray
    Write-Host "   Last Result: $($info2.LastTaskResult)" -ForegroundColor Gray

    # Trigger Details
    $triggers = $task2.Triggers
    Write-Host "   Trigger: $($triggers[0].CimClass.CimClassName)" -ForegroundColor Gray
    if($triggers[0].StartBoundary) {
        Write-Host "   Start Time: $($triggers[0].StartBoundary)" -ForegroundColor Gray
    }
} catch {
    Write-Host "   ERROR: Task nicht gefunden!" -ForegroundColor Red
}

Write-Host ""
Write-Host "="*80 -ForegroundColor Green
