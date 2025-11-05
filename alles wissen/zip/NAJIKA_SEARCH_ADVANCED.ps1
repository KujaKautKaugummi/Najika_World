# NAJIKA COMPLETE PROJECT SEARCH - ADVANCED POWERSHELL EDITION
# Erweiterte Suche mit PDF-Support, JSON-Parsing und strukturierter Ausgabe

param(
    [string]$SearchDir = $PSScriptRoot,
    [switch]$IncludePDF = $false,
    [switch]$Verbose = $false
)

$ErrorActionPreference = "Continue"

# Ausgabedatei
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$outputFile = Join-Path $SearchDir "NAJIKA_ADVANCED_$timestamp.txt"

Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  NAJIKA ADVANCED SEARCH - PowerShell Edition                ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""
Write-Host "Durchsuche: $SearchDir" -ForegroundColor Yellow
Write-Host "Report: $outputFile" -ForegroundColor Yellow
Write-Host ""

# ═══════════════════════════════════════════════════════════════
# KEYWORD KATEGORIEN
# ═══════════════════════════════════════════════════════════════

$keywords = @{
    # KERN
    "KujaNajika" = @("kuja", "najika", "schwert", "schild", "beschützer", "kopf", "herz", "girlfriend")
    "Persönlichkeit" = @("MEGUMIN", "HARLEY", "SHIRO", "MELISSA", "SAKURA", "explosion", "puddin", "chaotisch")

    # DIGIVICE
    "Digivice" = @("digivice", "app", "pwa", "handy-spiel", "handyspiel", "mobile", "tamagotchi", "module")
    "SchwarzeMühle" = @("mühle", "windmühle", "schwarze", "holländische", "dunkle", "gesichert", "bereich")

    # GAMEPLAY: Klassen
    "Klassen" = @("explosion-klasse", "magier", "krieger", "tank", "healer", "scout", "ranger", "assassin")

    # GAMEPLAY: Skills
    "Skills" = @("skill", "weaving", "weave-system", "zauber", "magie", "spell", "combo", "use-based")

    # GAMEPLAY: Crafting & Gathering
    "Crafting" = @("crafting", "handwerk", "rezept", "blueprint", "schmiede", "alchemie", "werkbank")
    "Gathering" = @("fishing", "farming", "mining", "gathering", "angeln", "ernten", "holzfällen", "erz")

    # GAMEPLAY: Combat
    "Combat" = @("kampf", "combat", "battle", "digimon-world", "oregon-trail", "boss", "raid", "dungeon")

    # GAMEPLAY: World
    "Welt" = @("file-island", "8-städte", "prozedural", "zone", "area", "biom", "event", "encounter")

    # GAMEPLAY: Movement
    "Movement" = @("fortnite", "sprint", "slide", "dash", "wall-climb", "vault", "parkour", "klettern")

    # GAMEPLAY: Progression
    "Progression" = @("level", "xp", "skill-tree", "talente", "stats", "strength", "intelligence", "hp", "mana")

    # GAMEPLAY: Magie
    "Magie" = @("magie", "zauber", "magieschule", "slime-rettung", "casting", "channeling", "ritual")

    # GAMEPLAY: Sozial
    "Sozial" = @("seelengefährten", "vertrautheits-xp", "emotions-shader", "koop-skills", "party", "team")

    # GAMEPLAY: Training
    "Training" = @("training", "bedürfnisse", "hunger", "durst", "müdigkeit", "glück", "feed", "sleep")

    # GAMEPLAY: Wirtschaft
    "Wirtschaft" = @("shop", "handel", "merchant", "vendor", "gold", "currency", "items", "equipment")

    # GAMEPLAY: Quests
    "Quests" = @("quest", "mission", "aufgabe", "objective", "achievement", "belohnung", "reward")

    # TECHNISCH: Engines
    "Engines" = @("three.js", "threejs", "webgl", "canvas", "python", "flask", "ollama")

    # TECHNISCH: UEFN
    "UEFN" = @("uefn", "fortnite", "creative", "verse", "epic-games", "map", "island")

    # TECHNISCH: Assets
    "Assets" = @("kaykit", "gltf", "glb", "fbx", "mesh", "texture", "material", "shader", "skelett")

    # TECHNISCH: Sync
    "Sync" = @("sync", "websocket", "cloud", "backup", "server", "client", "api", "session")

    # TECHNISCH: AI
    "AI" = @("ollama", "opus", "wizard", "llama", "model", "persona", "behavior", "bond", "memory")

    # BASIS
    "Konzepte" = @("maximale freiheit", "totale eigenverantwortung", "autonom", "selbstbestimmt", "legal")

    # SICHERHEIT
    "Sicherheit" = @("8-gebote", "verschlüsselung", "security", "ethik", "moral", "consent", "gdpr")

    # CODE
    "Code" = @("def ", "class ", "function ", "async ", "import ", "export ", "const ", "let ")

    # API
    "API" = @("/api/", "endpoint", "route", "handler", "controller", "get", "post", "put", "delete")

    # DATEIEN
    "Dateien" = @("najika_server", "digivice", "index.html", "3d_scene", "kaykit_loader", "minigames")

    # SPEZIAL
    "Spezial" = @("daddy", "schlampe", "puddin", "kätzchen", "private", "nsfw", "wizard")
}

# ═══════════════════════════════════════════════════════════════
# REPORT HEADER
# ═══════════════════════════════════════════════════════════════

$header = @"
═══════════════════════════════════════════════════════════════
   NAJIKA ADVANCED PROJECT SEARCH - PowerShell Edition
═══════════════════════════════════════════════════════════════
Erstellt: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
Verzeichnis: $SearchDir
PDF-Suche: $(if($IncludePDF){"Aktiviert"}else{"Deaktiviert"})

═══════════════════════════════════════════════════════════════
PROJEKT-STRUKTUR
═══════════════════════════════════════════════════════════════

[1] KI_AI_NAJIKA
    • Hauptgehirn, Steuerlogik
    • Opus & Wizard Modelle
    • Memory & Bond System

[2] DIGIVICE_APP
    • Mobile PWA
    • Gesicherter Bereich
    • Schwarze Mühle (alle Varianten)

[3] MODULE
    • Handyspiel-Module
    • Mini-Games
    • Tools & Features

[4] FORTNITE_UEFN
    • Maps & Assets
    • Verse Scripts

═══════════════════════════════════════════════════════════════
GAMEPLAY-SYSTEME
═══════════════════════════════════════════════════════════════

KLASSEN:
  • Explosion-Klasse (Megumin-Style)
  • Weitere: Magier, Krieger, Tank, Healer, etc.

SKILL-SYSTEME:
  • Skill Weaving
  • Use-Based Progression
  • Magieschulen & Slime-Rettung

CRAFTING & GATHERING:
  • Crafting, Fishing, Farming
  • Mining, Holzfällen

KAMPF:
  • Digimon World Style (Echtzeit-Anfeuerung)
  • Oregon Trail Events
  • Boss-Kämpfe, Raids, Dungeons

MOVEMENT:
  • Fortnite Movement (Sprint, Slide, Dash, Wall-Climb, Vault)

WELT:
  • File Island
  • 8 Städte
  • Prozedural-generierte Bereiche

═══════════════════════════════════════════════════════════════

"@

$header | Out-File -FilePath $outputFile -Encoding UTF8

# ═══════════════════════════════════════════════════════════════
# HAUPTSUCHE
# ═══════════════════════════════════════════════════════════════

Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  PHASE 1: Text-Dateien durchsuchen                          ║" -ForegroundColor Green
Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

$extensions = @("*.txt", "*.md", "*.json", "*.jsonl", "*.py", "*.js", "*.html", "*.css")
$allFiles = Get-ChildItem -Path $SearchDir -Recurse -Include $extensions -ErrorAction SilentlyContinue

$totalFiles = $allFiles.Count
$foundFiles = 0
$currentFile = 0

$results = @()

foreach ($file in $allFiles) {
    $currentFile++

    if ($currentFile % 10 -eq 0) {
        Write-Host "  [Progress] $currentFile / $totalFiles Dateien..." -ForegroundColor Gray
    }

    try {
        $content = Get-Content -Path $file.FullName -Raw -ErrorAction Stop

        $fileMatches = @()

        foreach ($category in $keywords.Keys) {
            foreach ($keyword in $keywords[$category]) {
                if ($content -match [regex]::Escape($keyword)) {
                    $fileMatches += @{
                        Category = $category
                        Keyword = $keyword
                        Count = ([regex]::Matches($content, [regex]::Escape($keyword), "IgnoreCase")).Count
                    }
                }
            }
        }

        if ($fileMatches.Count -gt 0) {
            $foundFiles++

            Write-Host "  [TREFFER] $($file.Name)" -ForegroundColor Yellow

            $results += @{
                File = $file
                Matches = $fileMatches
            }

            # Schreibe in Report
            $output = @"

═══════════════════════════════════════════════════════════════
DATEI: $($file.Name)
═══════════════════════════════════════════════════════════════
Pfad: $($file.FullName)
Größe: $([math]::Round($file.Length / 1KB, 2)) KB
Typ: $($file.Extension)

GEFUNDENE KEYWORDS:
"@
            $output | Out-File -FilePath $outputFile -Append -Encoding UTF8

            foreach ($match in $fileMatches) {
                "  [$($match.Category)] $($match.Keyword) ($($match.Count)x)" | Out-File -FilePath $outputFile -Append -Encoding UTF8
            }
        }

    } catch {
        if ($Verbose) {
            Write-Host "  [FEHLER] Kann $($file.Name) nicht lesen: $_" -ForegroundColor Red
        }
    }
}

Write-Host ""
Write-Host "Text-Dateien: $totalFiles durchsucht, $foundFiles Treffer" -ForegroundColor Green
Write-Host ""

# ═══════════════════════════════════════════════════════════════
# PDF-SUCHE (falls aktiviert)
# ═══════════════════════════════════════════════════════════════

if ($IncludePDF) {
    Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║  PHASE 2: PDF-Dateien                                       ║" -ForegroundColor Green
    Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Green
    Write-Host ""

    $pdfFiles = Get-ChildItem -Path $SearchDir -Recurse -Filter "*.pdf" -ErrorAction SilentlyContinue

    "`n`n═══════════════════════════════════════════════════════════════`nPDF-DATEIEN`n═══════════════════════════════════════════════════════════════`n" | Out-File -FilePath $outputFile -Append -Encoding UTF8

    foreach ($pdf in $pdfFiles) {
        Write-Host "  [PDF] $($pdf.Name) ($([math]::Round($pdf.Length / 1MB, 2)) MB)" -ForegroundColor Cyan

        $pdfInfo = @"

[PDF] $($pdf.Name)
Pfad: $($pdf.FullName)
Größe: $([math]::Round($pdf.Length / 1MB, 2)) MB
HINWEIS: PDF-Inhalt muss manuell geprüft werden

"@
        $pdfInfo | Out-File -FilePath $outputFile -Append -Encoding UTF8
    }

    Write-Host ""
    Write-Host "PDFs gefunden: $($pdfFiles.Count)" -ForegroundColor Green
    Write-Host ""
}

# ═══════════════════════════════════════════════════════════════
# BILDER & 3D ASSETS
# ═══════════════════════════════════════════════════════════════

Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  PHASE 3: Bilder & 3D-Assets                                ║" -ForegroundColor Green
Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

$assetExtensions = @("*.png", "*.jpg", "*.jpeg", "*.gif", "*.bmp", "*.webp", "*.glb", "*.gltf", "*.fbx", "*.obj")
$assetFiles = Get-ChildItem -Path $SearchDir -Recurse -Include $assetExtensions -ErrorAction SilentlyContinue

"`n`n═══════════════════════════════════════════════════════════════`nBILDER & 3D-ASSETS`n═══════════════════════════════════════════════════════════════`n" | Out-File -FilePath $outputFile -Append -Encoding UTF8

foreach ($asset in $assetFiles) {
    Write-Host "  [ASSET] $($asset.Name) ($($asset.Extension))" -ForegroundColor Magenta

    "[ASSET] $($asset.Name) | Typ: $($asset.Extension) | Größe: $([math]::Round($asset.Length / 1KB, 2)) KB | Pfad: $($asset.FullName)" | Out-File -FilePath $outputFile -Append -Encoding UTF8
}

Write-Host ""
Write-Host "Assets gefunden: $($assetFiles.Count)" -ForegroundColor Green
Write-Host ""

# ═══════════════════════════════════════════════════════════════
# ZUSAMMENFASSUNG
# ═══════════════════════════════════════════════════════════════

$summary = @"

═══════════════════════════════════════════════════════════════
ZUSAMMENFASSUNG
═══════════════════════════════════════════════════════════════

Text-Dateien durchsucht:  $totalFiles
Dateien mit Treffern:     $foundFiles
PDFs gefunden:            $(if($IncludePDF){$pdfFiles.Count}else{"(nicht durchsucht)"})
Bilder/3D-Assets:         $($assetFiles.Count)

KATEGORIEN MIT MEISTEN TREFFERN:
"@

$summary | Out-File -FilePath $outputFile -Append -Encoding UTF8

# Analysiere welche Kategorien am häufigsten vorkommen
$categoryStats = @{}
foreach ($result in $results) {
    foreach ($match in $result.Matches) {
        if (-not $categoryStats.ContainsKey($match.Category)) {
            $categoryStats[$match.Category] = 0
        }
        $categoryStats[$match.Category] += $match.Count
    }
}

$topCategories = $categoryStats.GetEnumerator() | Sort-Object Value -Descending | Select-Object -First 10

foreach ($cat in $topCategories) {
    "  • $($cat.Key): $($cat.Value) Vorkommen" | Out-File -FilePath $outputFile -Append -Encoding UTF8
}

@"

═══════════════════════════════════════════════════════════════
Report gespeichert: $outputFile
═══════════════════════════════════════════════════════════════

"@ | Out-File -FilePath $outputFile -Append -Encoding UTF8

Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                    SUCHE ABGESCHLOSSEN                       ║" -ForegroundColor Cyan
Write-Host "╠══════════════════════════════════════════════════════════════╣" -ForegroundColor Cyan
Write-Host "║  Text-Dateien:          $totalFiles" -ForegroundColor Cyan
Write-Host "║  Treffer:               $foundFiles" -ForegroundColor Cyan
Write-Host "║  Assets:                $($assetFiles.Count)" -ForegroundColor Cyan
Write-Host "╠══════════════════════════════════════════════════════════════╣" -ForegroundColor Cyan
Write-Host "║  Report: $outputFile" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Report öffnen
Start-Process notepad $outputFile

Write-Host "Drücke eine Taste zum Schließen..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
