# NAJIKA INTENSIVE NIGHT TRAINING - TÄGLICH 00:00 UHR
# 8 STUNDEN GPU-TRAINING - JEDEN TAG!

Write-Host "=" -ForegroundColor Green
Write-Host "NAJIKA INTENSIVE NIGHT TRAINING - TASK SETUP" -ForegroundColor Yellow
Write-Host "=" -ForegroundColor Green

# Config
$TaskName = "NajikaIntensiveNightTraining"
$PythonScript = "C:\Najika_World\backend\najika_intensive_night_training.py"
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

# Action: Python-Skript ausfuehren
$action = New-ScheduledTaskAction `
    -Execute "python" `
    -Argument "`"$PythonScript`"" `
    -WorkingDirectory $WorkingDir

# Trigger: TÄGLICH um 00:00 Uhr!
$trigger = New-ScheduledTaskTrigger -Daily -At "00:00"

# Settings: 10 Stunden Timeout (da Training bis zu 10h dauern kann)
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable:$false `
    -DontStopOnIdleEnd `
    -ExecutionTimeLimit (New-TimeSpan -Hours 10) `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 15)

# Principal: Mit hoechsten Rechten
$principal = New-ScheduledTaskPrincipal `
    -UserId $env:USERNAME `
    -LogonType Interactive `
    -RunLevel Highest

# Registriere Task
try {
    Register-ScheduledTask `
        -TaskName $TaskName `
        -Action $action `
        -Trigger $trigger `
        -Settings $settings `
        -Principal $principal `
        -Force

    Write-Host "OK: Task erstellt!" -ForegroundColor Green
    Write-Host "   - Startet: TAEGLICH um 00:00 Uhr" -ForegroundColor Gray
    Write-Host "   - Dauer: bis zu 10 Stunden (00:00-10:00)" -ForegroundColor Gray
    Write-Host "   - GPU: INTENSIV (RTX 3060 Ti voll ausgelastet)" -ForegroundColor Gray
    Write-Host "   - Auto-Restart: 3x bei Fehler (alle 15 Min)" -ForegroundColor Gray
} catch {
    Write-Host "FEHLER beim Erstellen der Task: $_" -ForegroundColor Red
    exit 1
}

# Zeige Status
Write-Host "[3] Task-Status:" -ForegroundColor Cyan

try {
    $task = Get-ScheduledTask -TaskName $TaskName
    Write-Host "   - Name: $($task.TaskName)" -ForegroundColor Gray
    Write-Host "   - State: $($task.State)" -ForegroundColor Gray
    Write-Host "   - Last Run: $($task.LastRunTime)" -ForegroundColor Gray
    Write-Host "   - Next Run: $($task.NextRunTime)" -ForegroundColor Gray
} catch {
    Write-Host "Warnung: Konnte Status nicht laden: $_" -ForegroundColor Yellow
}

# Info über Training-Phasen
Write-Host ""
Write-Host "="*80 -ForegroundColor Green
Write-Host "TRAINING-PHASEN (10 Stunden total):" -ForegroundColor Yellow
Write-Host "="*80 -ForegroundColor Green
Write-Host ""
Write-Host "Phase 1 (00:00-02:00): LoRA Personality Training (4x 30min)" -ForegroundColor Cyan
Write-Host "Phase 2 (02:00-04:00): Code Training Intensive (8x 15min)" -ForegroundColor Cyan
Write-Host "Phase 3 (04:00-06:00): Advanced Training (4x 30min)" -ForegroundColor Cyan
Write-Host "Phase 4 (06:00-08:00): Memory Enhancement (4x 30min)" -ForegroundColor Cyan
Write-Host "Phase 5 (08:00-10:00): Project Knowledge Training (4x 30min)" -ForegroundColor Cyan
Write-Host ""
Write-Host "Naechster Start: $($task.NextRunTime)" -ForegroundColor Yellow
Write-Host ""
Write-Host "Logs:" -ForegroundColor Cyan
Write-Host "  - C:\Najika_World\backend\training_night_log.json" -ForegroundColor Gray
Write-Host ""
Write-Host "NAJIKA LERNT JEDEN TAG 8-10 STUNDEN IN DER NACHT! 🔥" -ForegroundColor Yellow
Write-Host ""

# Fertig
Write-Host "Setup abgeschlossen!" -ForegroundColor Gray
