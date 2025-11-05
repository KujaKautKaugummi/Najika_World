# ============================================
# LISTE ALLE NAJIKA TASKS
# ============================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " NAJIKA TASKS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$tasks = Get-ScheduledTask | Where-Object {$_.TaskName -like "Najika*"}

if ($tasks) {
    Write-Host "Gefundene Tasks: $($tasks.Count)" -ForegroundColor Yellow
    Write-Host ""

    foreach ($task in $tasks) {
        Write-Host "  Task: $($task.TaskName)" -ForegroundColor White
        Write-Host "    Status: $($task.State)" -ForegroundColor Gray

        # Hole Trigger-Info
        $taskInfo = Get-ScheduledTaskInfo -TaskName $task.TaskName -ErrorAction SilentlyContinue
        if ($taskInfo) {
            Write-Host "    Letzter Lauf: $($taskInfo.LastRunTime)" -ForegroundColor Gray
            Write-Host "    Naechster Lauf: $($taskInfo.NextRunTime)" -ForegroundColor Gray
        }
        Write-Host ""
    }
} else {
    Write-Host "Keine Najika-Tasks gefunden!" -ForegroundColor Green
}

Write-Host ""
Write-Host "Druecke eine Taste..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
