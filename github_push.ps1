# Schnelles GitHub Upload Script für Najika-World

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "  NAJIKA-WORLD -> GITHUB UPLOAD  " -ForegroundColor Magenta
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Eingaben sammeln
Write-Host "GitHub Token: " -NoNewline -ForegroundColor Yellow
$token = Read-Host

Write-Host "GitHub Username: " -NoNewline -ForegroundColor Yellow
$username = Read-Host

Write-Host "Repository Name [Najika-World]: " -NoNewline -ForegroundColor Yellow
$repo = Read-Host
if ([string]::IsNullOrWhiteSpace($repo)) { $repo = "Najika-World" }

Write-Host ""
Write-Host "==================================" -ForegroundColor Cyan

# Konfiguriere Remote
$remoteUrl = "https://${token}@github.com/${username}/${repo}.git"

Write-Host "Konfiguriere Git Remote..." -ForegroundColor Yellow

# Entferne alten Remote falls vorhanden
git remote remove origin 2>$null

# Füge neuen Remote hinzu
git remote add origin $remoteUrl

Write-Host "OK!" -ForegroundColor Green
Write-Host ""

# Zeige Status
Write-Host "Git Status:" -ForegroundColor Cyan
git status --short
Write-Host ""

# Stage alle Änderungen
Write-Host "Stage Dateien..." -ForegroundColor Yellow
git add .
Write-Host "OK!" -ForegroundColor Green
Write-Host ""

# Commit
Write-Host "Commit Message [Update Najika-World]: " -NoNewline -ForegroundColor Yellow
$msg = Read-Host
if ([string]::IsNullOrWhiteSpace($msg)) { $msg = "Update Najika-World" }

git commit -m "$msg"
Write-Host ""

# Push
Write-Host "Pushe zu GitHub..." -ForegroundColor Yellow
Write-Host "(Kann einige Minuten dauern...)" -ForegroundColor DarkGray
Write-Host ""

$branch = git branch --show-current
git push -u origin $branch

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "==================================" -ForegroundColor Cyan
    Write-Host "       ERFOLGREICH!" -ForegroundColor Green
    Write-Host "==================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Repository: https://github.com/${username}/${repo}" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "FEHLER beim Push!" -ForegroundColor Red
    Write-Host "Prüfen Sie Token und Repository-Name." -ForegroundColor Yellow
}

Write-Host ""
