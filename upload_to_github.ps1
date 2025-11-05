# Upload Najika-World zu GitHub
# Automatisches Script zum Hochladen des Repositories

Write-Host "================================" -ForegroundColor Cyan
Write-Host "   NAJIKA-WORLD -> GITHUB" -ForegroundColor Magenta
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Prüfe ob Git konfiguriert ist
$remote = git remote get-url origin 2>$null

if (-not $remote) {
    Write-Host "❌ Kein Git Remote gefunden!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Bitte führen Sie zuerst aus:" -ForegroundColor Yellow
    Write-Host "  .\setup_github_token.ps1" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Drücken Sie eine Taste zum Beenden..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host "✅ Git Remote gefunden: $remote" -ForegroundColor Green
Write-Host ""

# Zeige aktuelle Branch
$currentBranch = git branch --show-current
Write-Host "📍 Aktuelle Branch: $currentBranch" -ForegroundColor Cyan
Write-Host ""

# Zeige Status
Write-Host "📊 Git Status:" -ForegroundColor Cyan
git status --short
Write-Host ""

# Frage ob fortfahren
Write-Host "Möchten Sie das Repository jetzt hochladen? (y/n)" -ForegroundColor Yellow
$confirm = Read-Host

if ($confirm -ne "y") {
    Write-Host "Abgebrochen." -ForegroundColor Red
    exit 0
}

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "Starte Upload..." -ForegroundColor Yellow
Write-Host ""

# Stage alle Dateien (außer .gitignore)
Write-Host "📦 Stage Dateien..." -ForegroundColor Cyan
git add .

# Zeige was gestaged wurde
Write-Host ""
Write-Host "Dateien zum Commit:" -ForegroundColor Cyan
git status --short
Write-Host ""

# Commit Message
Write-Host "Commit Message eingeben:" -ForegroundColor Yellow
$commitMsg = Read-Host "(default: 'Update Najika-World')"
if ([string]::IsNullOrWhiteSpace($commitMsg)) { $commitMsg = "Update Najika-World" }

Write-Host ""
Write-Host "💾 Erstelle Commit..." -ForegroundColor Cyan
git commit -m "$commitMsg"

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Commit fehlgeschlagen!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Drücken Sie eine Taste zum Beenden..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host "✅ Commit erstellt!" -ForegroundColor Green
Write-Host ""

# Push zu GitHub
Write-Host "🚀 Pushe zu GitHub..." -ForegroundColor Cyan
Write-Host "(Dies kann einige Minuten dauern...)" -ForegroundColor DarkGray
Write-Host ""

git push -u origin $currentBranch

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ Push fehlgeschlagen!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Mögliche Probleme:" -ForegroundColor Yellow
    Write-Host "  - Token ist abgelaufen oder ungültig" -ForegroundColor Gray
    Write-Host "  - Repository existiert nicht auf GitHub" -ForegroundColor Gray
    Write-Host "  - Keine Berechtigung für dieses Repository" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Führen Sie erneut aus: .\setup_github_token.ps1" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Drücken Sie eine Taste zum Beenden..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "🎉 Upload erfolgreich!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Zeige Repository URL
$repoUrl = $remote -replace "https://.*@", "https://"
Write-Host "Ihr Repository:" -ForegroundColor Cyan
Write-Host "  $repoUrl" -ForegroundColor Gray
Write-Host ""

Write-Host "Drücken Sie eine Taste zum Beenden..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
