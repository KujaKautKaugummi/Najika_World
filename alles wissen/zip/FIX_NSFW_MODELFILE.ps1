# ==============================================================================
# FIX_NSFW_MODELFILE.ps1
# Repariert das kaputte Modelfile_NSFW
# ==============================================================================

$ModelfileDir = "C:\NajikaCore\prompts"

Write-Host ""
Write-Host "=== NSFW MODELFILE FIX ===" -ForegroundColor Cyan
Write-Host ""

# Prüfe ob Files existieren
if (-not (Test-Path "$ModelfileDir\Modelfile")) {
    Write-Host "FEHLER: Modelfile nicht gefunden!" -ForegroundColor Red
    Read-Host "Enter"
    exit
}

if (-not (Test-Path "$ModelfileDir\nsfw_addon_EDIT_ME.txt")) {
    Write-Host "WARNUNG: nsfw_addon_EDIT_ME.txt nicht gefunden - erstelle leere Version" -ForegroundColor Yellow
    $nsfwContent = "NSFW MODE - Manuell ergänzen"
} else {
    $nsfwContent = Get-Content "$ModelfileDir\nsfw_addon_EDIT_ME.txt" -Raw -Encoding UTF8
}

# Lese funktionierende Modelfile
$baseModelfile = Get-Content "$ModelfileDir\Modelfile" -Raw -Encoding UTF8

# Finde SYSTEM-Block Ende
if ($baseModelfile -match '(SYSTEM\s+"""[\s\S]*?)(""")') {
    $systemBlock = $Matches[1]
    
    # Erstelle NSFW Version
    $nsfwModelfile = $baseModelfile -replace '(SYSTEM\s+"""[\s\S]*?)(""")', @"
`$1

---
NSFW MODE ACTIVATED
Context: Adult roleplay between consenting partners

$nsfwContent
---

`$2
"@
    
    # Speichere
    Set-Content "$ModelfileDir\Modelfile_NSFW" $nsfwModelfile -Encoding UTF8
    
    Write-Host "✓ Modelfile_NSFW repariert" -ForegroundColor Green
    Write-Host ""
    
    # Zeige Preview
    Write-Host "PREVIEW (erste 500 Zeichen):" -ForegroundColor Cyan
    Write-Host $nsfwModelfile.Substring(0, [Math]::Min(500, $nsfwModelfile.Length)) -ForegroundColor Gray
    Write-Host ""
    
    # Erstelle Model
    Write-Host "Erstelle najika-nsfw Model..." -ForegroundColor Yellow
    
    Push-Location $ModelfileDir
    
    $result = ollama create najika-nsfw -f Modelfile_NSFW 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ najika-nsfw Model erstellt!" -ForegroundColor Green
    } else {
        Write-Host "FEHLER beim Erstellen:" -ForegroundColor Red
        Write-Host $result -ForegroundColor Red
        Write-Host ""
        Write-Host "Modelfile_NSFW wurde trotzdem gespeichert." -ForegroundColor Yellow
        Write-Host "Öffne mit: notepad $ModelfileDir\Modelfile_NSFW" -ForegroundColor Yellow
    }
    
    Pop-Location
    
} else {
    Write-Host "FEHLER: Konnte SYSTEM-Block nicht finden!" -ForegroundColor Red
    Write-Host "Modelfile hat unerwartete Struktur." -ForegroundColor Red
}

Write-Host ""
Write-Host "FERTIG!" -ForegroundColor Green
Write-Host ""
Write-Host "TESTEN:" -ForegroundColor Yellow
Write-Host "  ollama run najika        # SFW Version" -ForegroundColor White
Write-Host "  ollama run najika-nsfw   # NSFW Version" -ForegroundColor White
Write-Host ""

Read-Host "Enter zum Beenden"