# ============================================
# NAJIKA TASK CLEANUP - LOESCHT ALLE ALTEN
# ============================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Red
Write-Host " WARNUNG: TASK CLEANUP!" -ForegroundColor Red
Write-Host "========================================" -ForegroundColor Red
Write-Host ""
Write-Host "Es wurden 33 Najika-Tasks gefunden!" -ForegroundColor Yellow
Write-Host "Das sind viel zu viele alte Tasks." -ForegroundColor Yellow
Write-Host ""
Write-Host "Dieses Script loescht ALLE Najika-Tasks" -ForegroundColor Red
Write-Host "und erstellt nur die 2 richtigen neu:" -ForegroundColor Green
Write-Host "  - NajikaTrainingNacht (00:00)" -ForegroundColor Cyan
Write-Host "  - NajikaTrainingTag (08:00, Mo-Fr)" -ForegroundColor Cyan
Write-Host ""

$confirm = Read-Host "Fortfahren? (J/N)"
if ($confirm -ne "J" -and $confirm -ne "j") {
    Write-Host "Abgebrochen." -ForegroundColor Yellow
    exit
}

Write-Host ""
Write-Host "Loesche alle Najika-Tasks..." -ForegroundColor Yellow

# Hole alle Najika-Tasks
$tasks = Get-ScheduledTask | Where-Object {$_.TaskName -like "Najika*"}

$count = 0
foreach ($task in $tasks) {
    try {
        Unregister-ScheduledTask -TaskName $task.TaskName -Confirm:$false
        Write-Host "  [OK] Geloescht: $($task.TaskName)" -ForegroundColor Gray
        $count++
    } catch {
        Write-Host "  [FEHLER] Konnte nicht loeschen: $($task.TaskName)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "$count Tasks geloescht." -ForegroundColor Green
Write-Host ""
Write-Host "Erstelle die 2 richtigen Tasks..." -ForegroundColor Yellow

# Task 1: NACHT
$action1 = New-ScheduledTaskAction -Execute "python" -Argument "C:\Najika\backend\najika_smart_training_scheduler.py --train" -WorkingDirectory "C:\Najika\backend"
$trigger1 = New-ScheduledTaskTrigger -Daily -At "00:00"
$settings1 = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Hours 8)

Register-ScheduledTask -TaskName "NajikaTrainingNacht" -Action $action1 -Trigger $trigger1 -Settings $settings1 -Force | Out-Null
Write-Host "  [OK] NajikaTrainingNacht erstellt" -ForegroundColor Green

# Task 2: TAG
$action2 = New-ScheduledTaskAction -Execute "python" -Argument "C:\Najika\backend\najika_smart_training_scheduler.py --train" -WorkingDirectory "C:\Najika\backend"
$trigger2 = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday,Tuesday,Wednesday,Thursday,Friday -At "08:00"
$settings2 = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Hours 7)

Register-ScheduledTask -TaskName "NajikaTrainingTag" -Action $action2 -Trigger $trigger2 -Settings $settings2 -Force | Out-Null
Write-Host "  [OK] NajikaTrainingTag erstellt" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host " CLEANUP ABGESCHLOSSEN!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Aktive Tasks:" -ForegroundColor White
Get-ScheduledTask | Where-Object {$_.TaskName -like "Najika*"} | Format-Table TaskName, State -AutoSize

Write-Host ""
Write-Host "Druecke eine Taste..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
