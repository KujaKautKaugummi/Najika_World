# ==============================================================================
# AUTO_SORT_NAJIKA.ps1 - ZWEI-SCHICHT-SYSTEM
# Kern (immer aktiv) + NSFW-Addon (per Button)
# ==============================================================================

param(
    [string]$InputFile = "najika_final.txt",
    [string]$OutputDir = "C:\NajikaCore\config"
)

Write-Host ""
Write-Host "=== NAJIKA AUTO-SORTIERER (Zwei-Schicht) ===" -ForegroundColor Cyan
Write-Host ""

# Prüfe Input
if (-not (Test-Path $InputFile)) {
    Write-Host "FEHLER: $InputFile nicht gefunden!" -ForegroundColor Red
    exit
}

$content = Get-Content $InputFile -Raw -Encoding UTF8

# ==============================================================================
# FILTER-REGELN
# ==============================================================================

$explicitKeywords = @(
    # Nur SEHR explizite Inhalte → NSFW-Addon
    'fick', 'schwanz.*lut', 'anal.*penetr', 'deepthroat',
    'sperma.*spritz', 'orgasmus.*beschreib', 'sex.*detail',
    'bluetooth.*vibrat', 'explicit.*dialog'
)

$coreKeywords = @(
    # Alles andere → Kern (auch sexuelle Themen, nur nicht ultra-explizit)
    'persönlichkeit', 'aussehen', 'eifersüchtig', 'besitzergreifend',
    'dominant', 'explosiv', 'megumin', 'assistenz', 'sprache',
    'code', 'smart.*home', 'intim', 'nsfw', 'sex', 'pervers'
)

# ==============================================================================
# ANALYSE
# ==============================================================================

function Analyze-Content {
    param([string]$text)
    
    $lines = $text -split "`n"
    $result = @{
        core = @()
        nsfwAddon = @()
        public = @()
    }
    
    foreach ($line in $lines) {
        $line = $line.Trim()
        if ([string]::IsNullOrWhiteSpace($line)) { continue }
        
        $explicitScore = 0
        
        # Prüfe ob SEHR explizit
        foreach ($kw in $explicitKeywords) {
            if ($line -match $kw) {
                $explicitScore += 3
            }
        }
        
        if ($explicitScore -ge 3) {
            # Sehr explizit → NSFW-Addon
            $result.nsfwAddon += $line
        } else {
            # Alles andere → Kern
            $result.core += $line
            
            # Auch für Public (wenn clean genug)
            $isClean = $true
            foreach ($kw in $explicitKeywords) {
                if ($line -match $kw) { $isClean = $false }
            }
            if ($isClean -and $line -notmatch 'sex|pervers|intim') {
                $result.public += $line
            }
        }
    }
    
    return $result
}

Write-Host "Analysiere..." -ForegroundColor Yellow

$analysis = Analyze-Content -text $content

Write-Host ""
Write-Host "ERGEBNISSE:" -ForegroundColor Cyan
Write-Host "  Kern (immer aktiv): $($analysis.core.Count) Zeilen" -ForegroundColor Green
Write-Host "  NSFW-Addon (per Button): $($analysis.nsfwAddon.Count) Zeilen" -ForegroundColor Red
Write-Host "  Öffentlich (später): $($analysis.public.Count) Zeilen" -ForegroundColor Yellow
Write-Host ""

# ==============================================================================
# KONFIGS ERSTELLEN
# ==============================================================================

# KERN-CONFIG (dein Standard - alles drin)
$coreConfig = @{
    meta = @{
        version = "1.0-core"
        type = "Complete Core Personality"
        description = "Najika komplett - immer aktiv"
    }
    personality = @{
        name = "Najika"
        base = "Megumin-inspired adult character"
        age = "Adult (ageless witch)"
        traits = @(
            "Explosive/dramatic",
            "Possessive/jealous", 
            "Dominant",
            "Analytical",
            "Loyal to obsession"
        )
    }
    features = @{
        assistant = $true
        language = $true
        programming = $true
        smart_home = $true
        intimate_personality = $true
        nsfw_capable = $true
    }
    content = ($analysis.core -join "`n")
}

# NSFW-ADDON (nur wenn Button aktiviert)
$nsfwAddon = @{
    meta = @{
        version = "1.0-addon"
        type = "NSFW Explicit Addon"
        requires_activation = $true
        activation = @{
            codewort = "Kätzchen"
            button = "Terminal → NSFW Button"
            auto_suggest = "Wenn allein erkannt"
        }
    }
    explicit_dialogues = ($analysis.nsfwAddon -join "`n")
    bluetooth_enabled = $true
}

# ÖFFENTLICHE VERSION (später für Epic)
$publicConfig = @{
    meta = @{
        version = "1.0-public"
        type = "Public Safe Version"
        description = "Für Epic/Nutzer - ohne kritisches"
    }
    personality = @{
        name = "Najika"
        base = "Megumin-inspired"
        traits = @("Dramatic", "Loyal", "Protective")
    }
    features = @{
        assistant = $true
        language = $true
        programming = $true
        nsfw = $false
    }
    content = ($analysis.public -join "`n")
}

# Speichern
$corePath = "$OutputDir\najika_personality_CORE.json"
$addonPath = "$OutputDir\najika_nsfw_addon.json"
$publicPath = "$OutputDir\najika_personality_PUBLIC.json"

$coreConfig | ConvertTo-Json -Depth 10 | Set-Content $corePath -Encoding UTF8
$nsfwAddon | ConvertTo-Json -Depth 10 | Set-Content $addonPath -Encoding UTF8
$publicConfig | ConvertTo-Json -Depth 10 | Set-Content $publicPath -Encoding UTF8

Write-Host "FERTIG!" -ForegroundColor Green
Write-Host ""
Write-Host "Erstellt:" -ForegroundColor Cyan
Write-Host "  ✓ KERN: $corePath" -ForegroundColor Green
Write-Host "    → Immer aktiv, komplette Najika" -ForegroundColor Gray
Write-Host ""
Write-Host "  ✓ ADDON: $addonPath" -ForegroundColor Red
Write-Host "    → Nur wenn NSFW-Button aktiviert" -ForegroundColor Gray
Write-Host ""
Write-Host "  ✓ PUBLIC: $publicPath" -ForegroundColor Yellow
Write-Host "    → Später für Epic (clean)" -ForegroundColor Gray
Write-Host ""

Read-Host "Enter zum Beenden"