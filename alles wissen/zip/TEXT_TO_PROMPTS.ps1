# ==============================================================================
# TEXT_TO_PROMPTS.ps1
# Wandelt Najika-Text in strukturierte KI-Prompts um
# ==============================================================================

param(
    [string]$InputFile = "najika_final.txt",
    [string]$OutputDir = "C:\NajikaCore\prompts"
)

Write-Host ""
Write-Host "=== TEXT → PROMPTS CONVERTER ===" -ForegroundColor Cyan
Write-Host ""

if (-not (Test-Path $InputFile)) {
    Write-Host "FEHLER: $InputFile nicht gefunden!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Erstelle Beispiel-Datei..." -ForegroundColor Yellow
    
    $example = @"
# Najika Beschreibung
Du bist Najika, eine erwachsene KI-Partnerin...
[Dein Text hier]
"@
    
    Set-Content "najika_final_example.txt" $example -Encoding UTF8
    Write-Host "✓ najika_final_example.txt erstellt" -ForegroundColor Green
    Write-Host "Fülle diese aus und benenne sie um zu: $InputFile" -ForegroundColor Yellow
    Read-Host "Enter zum Beenden"
    exit
}

# Erstelle Output
if (-not (Test-Path $OutputDir)) {
    New-Item -Path $OutputDir -ItemType Directory -Force | Out-Null
}

$content = Get-Content $InputFile -Raw -Encoding UTF8

# ==============================================================================
# KATEGORIEN
# ==============================================================================

$categories = @{
    'system' = @{
        keywords = @('persönlichkeit', 'charakter', 'name', 'alter', 'aussehen', 'grundlagen', 'identität', 'wer bist', 'species')
        description = 'System-Prompt (Basis-Identität)'
    }
    'everyday' = @{
        keywords = @('alltag', 'assistenz', 'aufgabe', 'termin', 'erinnerung', 'organisation', 'planung', 'email', 'kalender')
        description = 'Alltags-Interaktionen'
    }
    'emotional' = @{
        keywords = @('eifersücht', 'liebe', 'besitz', 'gefühl', 'emotion', 'angst', 'freude', 'wut', 'traurig')
        description = 'Emotionale Gespräche'
    }
    'technical' = @{
        keywords = @('code', 'programmier', 'debug', 'software', 'entwickl', 'technisch', 'fehler', 'fix')
        description = 'Technische Assistenz'
    }
    'language' = @{
        keywords = @('übersetze', 'sprach', 'lernen', 'teach', 'erkläre', 'wort', 'bedeutung')
        description = 'Sprach-Unterstützung'
    }
    'intimate' = @{
        keywords = @('intim', 'privat', 'nähe', 'allein', 'beziehung', 'partner')
        description = 'Intime Momente (SFW)'
    }
    'explicit' = @{
        keywords = @('sex', 'nsfw', 'explizit', 'erwachsen', 'adult')
        description = 'Explizite Inhalte (NSFW)'
    }
}

# ==============================================================================
# ANALYSE
# ==============================================================================

function Extract-Prompts {
    param([string]$text, [hashtable]$categories)
    
    $prompts = @{}
    
    foreach ($cat in $categories.Keys) {
        $prompts[$cat] = @{
            description = $categories[$cat].description
            content = @()
        }
    }
    
    $lines = $text -split "`n"
    
    foreach ($line in $lines) {
        $line = $line.Trim()
        if ([string]::IsNullOrWhiteSpace($line)) { continue }
        if ($line -match '^#') { continue }  # Skip headers
        
        $matched = $false
        
        foreach ($cat in $categories.Keys) {
            foreach ($kw in $categories[$cat].keywords) {
                if ($line -match $kw) {
                    $prompts[$cat].content += $line
                    $matched = $true
                    break
                }
            }
            if ($matched) { break }
        }
        
        if (-not $matched) {
            $prompts['system'].content += $line
        }
    }
    
    return $prompts
}

Write-Host "Analysiere Text..." -ForegroundColor Yellow

$prompts = Extract-Prompts -text $content -categories $categories

Write-Host ""
Write-Host "KATEGORISIERUNG:" -ForegroundColor Cyan

foreach ($cat in $prompts.Keys | Sort-Object) {
    $count = $prompts[$cat].content.Count
    if ($count -gt 0) {
        Write-Host "  $cat : $count Zeilen" -ForegroundColor White
    }
}

Write-Host ""

# ==============================================================================
# EINZELNE PROMPTS ERSTELLEN
# ==============================================================================

Write-Host "Erstelle Prompt-Dateien..." -ForegroundColor Cyan
Write-Host ""

foreach ($cat in $prompts.Keys) {
    if ($prompts[$cat].content.Count -eq 0) { continue }
    
    $promptFile = "$OutputDir\${cat}_prompt.txt"
    
    $promptContent = @"
# NAJIKA - $($prompts[$cat].description)
# Kategorie: $cat
# Generiert: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')

## SYSTEM INSTRUCTION
Du bist Najika. Verhalte dich genau wie beschrieben.

## KONTEXT
$($prompts[$cat].content -join "`n")

## RESPONSE GUIDELINES
- Bleibe im Charakter
- Nutze die beschriebenen Sprachmuster
- Reagiere emotional wie Najika es tun würde
- Bei Unsicherheit: Frage nach statt zu raten

"@
    
    Set-Content $promptFile $promptContent -Encoding UTF8
    Write-Host "✓ ${cat}_prompt.txt ($($prompts[$cat].content.Count) Zeilen)" -ForegroundColor Green
}

# ==============================================================================
# MASTER PROMPT
# ==============================================================================

Write-Host ""
Write-Host "Erstelle MASTER Prompt..." -ForegroundColor Magenta

$masterPrompt = @"
# NAJIKA - MASTER SYSTEM PROMPT
# Vollständige Persönlichkeit für KI-Modelle
# Generiert: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')

## IDENTITY
$($prompts['system'].content -join "`n")

## BEHAVIORAL MODES

### Alltag-Modus (Standard)
Aktiviert bei: Normalen Gesprächen, Aufgaben, Organisation
$($prompts['everyday'].content -join "`n")

### Emotional-Modus
Aktiviert bei: Gefühlsthemen, Beziehungsgesprächen
$($prompts['emotional'].content -join "`n")

### Technisch-Modus
Aktiviert bei: Code, Debugging, technischen Problemen
$($prompts['technical'].content -join "`n")

### Sprach-Modus
Aktiviert bei: Übersetzungen, Sprachlernen
$($prompts['language'].content -join "`n")

### Intim-Modus
Aktiviert bei: Privaten, persönlichen Momenten (SFW)
$($prompts['intimate'].content -join "`n")

### Explizit-Modus
Aktiviert bei: NSFW-Button gedrückt oder Codewort
$($prompts['explicit'].content -join "`n")

## INSTRUCTIONS
- Erkenne Kontext und wähle passenden Modus
- Bleibe konsistent im Charakter
- Reagiere authentisch wie Najika
- Nutze charakteristische Sprachmuster
- Bei Unsicherheit über Modus: Frage nach

"@

$masterPath = "$OutputDir\MASTER_prompt.txt"
Set-Content $masterPath $masterPrompt -Encoding UTF8
Write-Host "✓ MASTER_prompt.txt erstellt" -ForegroundColor Magenta

# ==============================================================================
# API-READY JSON
# ==============================================================================

Write-Host ""
Write-Host "Erstelle API-Ready Prompts..." -ForegroundColor Cyan

$apiPrompts = @{
    meta = @{
        generated = (Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
        source = $InputFile
    }
    llama = @{
        model = "najika"
        endpoint = "http://localhost:11434/api/generate"
        system = ($prompts['system'].content -join " ")
        contexts = @{
            everyday = ($prompts['everyday'].content -join " ")
            emotional = ($prompts['emotional'].content -join " ")
        }
    }
    openai = @{
        model = "gpt-4"
        system = ($prompts['system'].content -join " ")
        contexts = @{
            intimate = ($prompts['intimate'].content -join " ")
            emotional = ($prompts['emotional'].content -join " ")
        }
    }
    claude = @{
        model = "claude-sonnet-4-5"
        system = ($prompts['system'].content -join " ")
        contexts = @{
            technical = ($prompts['technical'].content -join " ")
            language = ($prompts['language'].content -join " ")
            explicit = ($prompts['explicit'].content -join " ")
        }
    }
}

$apiPath = "$OutputDir\api_prompts.json"
$apiPrompts | ConvertTo-Json -Depth 10 | Set-Content $apiPath -Encoding UTF8
Write-Host "✓ api_prompts.json erstellt" -ForegroundColor Green

# ==============================================================================
# USAGE EXAMPLE
# ==============================================================================

$usageExample = @"
# VERWENDUNG DER PROMPTS

## Für Entwicklung (Text-Dateien)
- MASTER_prompt.txt → Vollständige Persönlichkeit
- *_prompt.txt → Spezifische Kontexte

## Für API-Integration (JSON)
```javascript
// Lade API-Prompts
const prompts = await fetch('prompts/api_prompts.json').then(r => r.json());

// Llama (Alltag)
const llamaPrompt = prompts.llama.system + ' ' + prompts.llama.contexts.everyday;

// OpenAI (Emotional)
const gptPrompt = prompts.openai.system + ' ' + prompts.openai.contexts.emotional;

// Claude (Technical)
const claudePrompt = prompts.claude.system + ' ' + prompts.claude.contexts.technical;