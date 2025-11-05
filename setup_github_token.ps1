# GitHub Token Setup für Najika-World
# Fragt nach dem GitHub Personal Access Token und konfiguriert Git

Write-Host "================================" -ForegroundColor Cyan
Write-Host "   GITHUB TOKEN SETUP" -ForegroundColor Magenta
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Dieses Script konfiguriert Ihr GitHub Token für das Najika-World Repository." -ForegroundColor Gray
Write-Host ""

# GitHub Token abfragen
Write-Host "Bitte geben Sie Ihren GitHub Personal Access Token ein:" -ForegroundColor Yellow
Write-Host "(Erstellen Sie einen unter: https://github.com/settings/tokens)" -ForegroundColor DarkGray
Write-Host ""
Write-Host "WICHTIG: Der Token wird sichtbar sein während Sie ihn eingeben!" -ForegroundColor Red
Write-Host ""
$tokenPlainText = Read-Host "GitHub Token"

if ([string]::IsNullOrWhiteSpace($tokenPlainText)) {
    Write-Host "❌ Kein Token eingegeben!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Drücken Sie eine Taste zum Beenden..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host ""
Write-Host "GitHub Username abfragen..." -ForegroundColor Cyan
$githubUsername = Read-Host "GitHub Username"

if ([string]::IsNullOrWhiteSpace($githubUsername)) {
    Write-Host "❌ Kein Username eingegeben!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Drücken Sie eine Taste zum Beenden..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host ""
Write-Host "Repository Name abfragen..." -ForegroundColor Cyan
$repoName = Read-Host "Repository Name (default: Najika-World)"
if ([string]::IsNullOrWhiteSpace($repoName)) { $repoName = "Najika-World" }

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "Konfiguriere Git..." -ForegroundColor Yellow

# Git Remote URL mit Token
$remoteUrl = "https://${tokenPlainText}@github.com/${githubUsername}/${repoName}.git"

# Prüfe ob Remote bereits existiert
$existingRemote = git remote get-url origin 2>$null

if ($existingRemote) {
    Write-Host "Remote 'origin' existiert bereits. Aktualisiere URL..." -ForegroundColor Yellow
    git remote set-url origin $remoteUrl
} else {
    Write-Host "Füge neuen Remote 'origin' hinzu..." -ForegroundColor Yellow
    git remote add origin $remoteUrl
}

Write-Host "✅ Git Remote konfiguriert!" -ForegroundColor Green
Write-Host ""

# Git Credentials speichern (optional)
Write-Host "Möchten Sie das Token im Git Credential Store speichern? (y/n)" -ForegroundColor Yellow
$saveCredentials = Read-Host "(Empfohlen, damit Sie das Token nicht jedes Mal eingeben müssen)"

if ($saveCredentials -eq "y") {
    git config credential.helper store
    Write-Host "✅ Credential Helper aktiviert!" -ForegroundColor Green
}

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "✅ Setup abgeschlossen!" -ForegroundColor Green
Write-Host ""
Write-Host "Sie können nun das Repository hochladen mit:" -ForegroundColor Cyan
Write-Host "  git add ." -ForegroundColor Gray
Write-Host "  git commit -m 'Initial commit'" -ForegroundColor Gray
Write-Host "  git push -u origin main" -ForegroundColor Gray
Write-Host ""
Write-Host "Oder führen Sie das Upload-Script aus:" -ForegroundColor Cyan
Write-Host "  .\upload_to_github.ps1" -ForegroundColor Gray
Write-Host ""

Write-Host "Drücken Sie eine Taste zum Beenden..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
