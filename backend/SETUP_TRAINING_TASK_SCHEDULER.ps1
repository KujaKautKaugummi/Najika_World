# 🔥🔥🔥 NAJIKA TRAINING - WINDOWS TASK SCHEDULER SETUP 🔥🔥🔥
# BOMBENFEST - LÄUFT EWIG!

Write-Host "="*80 -ForegroundColor Green
Write-Host "NAJIKA TRAINING - WINDOWS TASK SCHEDULER SETUP" -ForegroundColor Yellow
Write-Host "="*80 -ForegroundColor Green

# Directories
$NajikaDir = "C:\Najika_World"
$BackendDir = "$NajikaDir\backend"
$PythonExe = "python"  # Nutzt System-Python
$MasterLauncher = "$BackendDir\NAJIKA_MASTER_TRAINING_LAUNCHER.py"

# Task Names
$TaskName = "NajikaMasterTrainingLauncher"

# ===== 1. LÖSCHE ALTE TASKS (Falls vorhanden) =====

Write-Host ""
Write-Host "[1] Lösche alte Tasks..." -ForegroundColor Cyan

try {
    $existingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    if ($existingTask) {
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
        Write-Host "✅ Alte Task gelöscht: $TaskName" -ForegroundColor Green
    } else {
        Write-Host "ℹ️ Keine alte Task gefunden" -ForegroundColor Gray
    }
} catch {
    Write-Host "⚠️ Fehler beim Löschen: $_" -ForegroundColor Yellow
}

# ===== 2. ERSTELLE HAUPT-TASK (STUENDLICH, 24/7) =====

Write-Host ""
Write-Host "[2] Erstelle Haupt-Task (stuendlich, 24/7)..." -ForegroundColor Cyan

# Action: Python-Skript ausführen
$action = New-ScheduledTaskAction `
    -Execute $PythonExe `
    -Argument "`"$MasterLauncher`"" `
    -WorkingDirectory $BackendDir

# Trigger: Stündlich, 24/7, EWIG!
$trigger = New-ScheduledTaskTrigger `
    -Once `
    -At (Get-Date) `
    -RepetitionInterval (New-TimeSpan -Hours 1) `
    -RepetitionDuration ([TimeSpan]::MaxValue)

# Settings: BOMBENFEST!
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable:$false `
    -DontStopOnIdleEnd `
    -RestartCount 999 `
    -RestartInterval (New-TimeSpan -Minutes 10) `
    -ExecutionTimeLimit (New-TimeSpan -Hours 3)

# Principal: Mit höchsten Rechten
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

    Write-Host "✅ Task erstellt: $TaskName" -ForegroundColor Green
    Write-Host "   - Läuft: STÜNDLICH (24/7)" -ForegroundColor Gray
    Write-Host "   - Start: JETZT" -ForegroundColor Gray
    Write-Host "   - Auto-Restart: 999x (alle 10 Min bei Fehler)" -ForegroundColor Gray
    Write-Host "   - Timeout: 3 Stunden" -ForegroundColor Gray
} catch {
    Write-Host "❌ FEHLER beim Erstellen der Task: $_" -ForegroundColor Red
    exit 1
}

# ===== 3. STARTE TASK SOFORT =====

Write-Host ""
Write-Host "[3] Starte Task sofort..." -ForegroundColor Cyan

try {
    Start-ScheduledTask -TaskName $TaskName
    Write-Host "✅ Task gestartet!" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Fehler beim Starten: $_" -ForegroundColor Yellow
}

# ===== 4. ZEIGE STATUS =====

Write-Host ""
Write-Host "[4] Task-Status:" -ForegroundColor Cyan

try {
    $task = Get-ScheduledTask -TaskName $TaskName
    Write-Host "   - Name: $($task.TaskName)" -ForegroundColor Gray
    Write-Host "   - State: $($task.State)" -ForegroundColor Gray
    Write-Host "   - Last Run: $($task.LastRunTime)" -ForegroundColor Gray
    Write-Host "   - Next Run: $($task.NextRunTime)" -ForegroundColor Gray
} catch {
    Write-Host "⚠️ Konnte Status nicht laden: $_" -ForegroundColor Yellow
}

# ===== FERTIG! =====

Write-Host ""
Write-Host "="*80 -ForegroundColor Green
Write-Host "✅✅✅ TASK SCHEDULER SETUP ABGESCHLOSSEN! ✅✅✅" -ForegroundColor Yellow
Write-Host "="*80 -ForegroundColor Green
Write-Host ""
Write-Host "NAJIKA TRAINING LÄUFT JETZT:" -ForegroundColor Cyan
Write-Host "  - LoRA-Training: alle 7 Tage" -ForegroundColor Gray
Write-Host "  - Coding-Training: täglich" -ForegroundColor Gray
Write-Host "  - Failsafe-Check: stündlich" -ForegroundColor Gray
Write-Host ""
Write-Host "Logs:" -ForegroundColor Cyan
Write-Host "  - C:\NajikaCore\training\master_launcher.log" -ForegroundColor Gray
Write-Host "  - C:\NajikaCore\training\training.log" -ForegroundColor Gray
Write-Host ""
Write-Host "BOMBENFEST - LÄUFT EWIG! 🔥🔥🔥" -ForegroundColor Yellow
Write-Host ""

# Warte auf Tastendruck
Write-Host "Drücke eine Taste zum Beenden..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
