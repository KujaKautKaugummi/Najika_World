# ==============================================================================
# COMPLETE_SETUP.ps1
# Macht alles auf einmal: Configs + NSFW + Prompts
# ==============================================================================

param(
    [string]$SourceDir = "C:\NajikaCore",
    [string]$TextFile = "C:\Users\0KKK0\Desktop\NN\najika_final.txt"
)

Write-Host ""
Write-Host "=== NAJIKA COMPLETE SETUP ===" -ForegroundColor Cyan
Write-Host ""

# Prüfe Pfade
if (-not (Test-Path $SourceDir)) {
    Write-Host "FEHLER: $SourceDir nicht gefunden!" -ForegroundColor Red
    exit
}

if (-not (Test-Path $TextFile)) {
    Write-Host "FEHLER: $TextFile nicht gefunden!" -ForegroundColor Red
    exit
}

Write-Host "Arbeitsverzeichnis: $SourceDir" -ForegroundColor White
Write-Host "Text-Datei: $TextFile" -ForegroundColor White
Write-Host ""

# Backup
$backupDir = "$SourceDir\_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
Write-Host "Erstelle Backup..." -ForegroundColor Yellow
Copy-Item -Path $SourceDir -Destination $backupDir -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "✓ Backup: $backupDir" -ForegroundColor Green
Write-Host ""

# ==============================================================================
# SCHRITT 1: CONFIGS ERSTELLEN
# ==============================================================================

Write-Host "=== SCHRITT 1: Configs erstellen ===" -ForegroundColor Magenta
Write-Host ""

$content = Get-Content $TextFile -Raw -Encoding UTF8

$explicitKeywords = @('fick', 'schwanz.*lut', 'anal.*penetr', 'deepthroat', 'sperma.*spritz', 'orgasmus.*beschreib', 'sex.*detail')
$lines = $content -split "`n"

$core = @()
$addon = @()

foreach ($line in $lines) {
    $line = $line.Trim()
    if ([string]::IsNullOrWhiteSpace($line)) { continue }
    
    $isExplicit = $false
    foreach ($kw in $explicitKeywords) {
        if ($line -match $kw) { $isExplicit = $true; break }
    }
    
    if ($isExplicit) { $addon += $line }
    else { $core += $line }
}

$coreConfig = @{
    meta = @{ version = "1.0-core"; type = "Core Personality" }
    content = ($core -join "`n")
}

$addonConfig = @{
    meta = @{ version = "1.0-addon"; type = "NSFW Addon"; requires_activation = $true }
    explicit_dialogues = ($addon -join "`n")
}

$coreConfig | ConvertTo-Json -Depth 10 | Set-Content "$SourceDir\config\najika_personality_CORE.json" -Encoding UTF8
$addonConfig | ConvertTo-Json -Depth 10 | Set-Content "$SourceDir\config\najika_nsfw_addon.json" -Encoding UTF8

Write-Host "✓ najika_personality_CORE.json" -ForegroundColor Green
Write-Host "✓ najika_nsfw_addon.json" -ForegroundColor Green
Write-Host ""

# ==============================================================================
# SCHRITT 2: NSFW CONTROLLER
# ==============================================================================

Write-Host "=== SCHRITT 2: NSFW Controller ===" -ForegroundColor Magenta
Write-Host ""

$nsfwController = @'
class NSFWModeController {
    constructor() { this.active = false; this.codewordBuffer = ''; }
    init() {
        console.log('NSFW Controller initialisiert');
        this.setupCodewordListener();
        this.setupButtonListener();
        this.loadCorePersonality();
    }
    setupCodewordListener() {
        document.addEventListener('keypress', (e) => {
            this.codewordBuffer += e.key.toLowerCase();
            setTimeout(() => this.codewordBuffer = '', 3000);
            if (this.codewordBuffer.includes('kätzchen')) {
                this.codewordBuffer = '';
                this.activateNSFW('codewort');
            }
        });
    }
    setupButtonListener() {
        const btn = document.getElementById('terminal-nsfw-btn');
        if (btn) btn.addEventListener('click', () => this.active ? this.deactivateNSFW() : this.activateNSFW('button'));
    }
    async loadCorePersonality() {
        try {
            const r = await fetch('config/najika_personality_CORE.json');
            if (r.ok) {
                this.core = await r.json();
                if (window.najikaAI?.loadPersonality) window.najikaAI.loadPersonality(this.core);
            }
        } catch (e) { console.error(e); }
    }
    async activateNSFW(method) {
        console.log(`NSFW aktiviert: ${method}`);
        try {
            const r = await fetch('config/najika_nsfw_addon.json');
            if (r.ok) {
                this.addon = await r.json();
                this.active = true;
                this.updateUI();
                if (window.najikaAI?.loadPersonality) {
                    window.najikaAI.loadPersonality({...this.core, nsfw: this.addon, nsfwActive: true});
                }
            }
        } catch (e) { console.error(e); }
    }
    deactivateNSFW() {
        console.log('NSFW deaktiviert');
        this.active = false;
        this.updateUI();
        if (window.najikaAI?.loadPersonality) window.najikaAI.loadPersonality(this.core);
    }
    updateUI() {
        const btn = document.getElementById('terminal-nsfw-btn');
        if (!btn) return;
        if (this.active) {
            btn.textContent = '🔴 NSFW Aktiv';
            btn.style.background = 'linear-gradient(145deg, #e74c3c, #c0392b)';
        } else {
            btn.textContent = '⚪ NSFW Inaktiv';
            btn.style.background = 'linear-gradient(145deg, #555, #333)';
        }
    }
}
window.nsfwController = new NSFWModeController();
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => window.nsfwController.init());
} else { window.nsfwController.init(); }
'@

Set-Content "$SourceDir\js\nsfw_controller.js" $nsfwController -Encoding UTF8
Write-Host "✓ nsfw_controller.js erstellt" -ForegroundColor Green
Write-Host ""

# ==============================================================================
# SCHRITT 3: HTML PATCHEN
# ==============================================================================

Write-Host "=== SCHRITT 3: HTML patchen ===" -ForegroundColor Magenta
Write-Host ""

$htmlFile = "$SourceDir\index_3d.html"

if (Test-Path $htmlFile) {
    $html = Get-Content $htmlFile -Raw -Encoding UTF8
    
    if ($html -notmatch 'nsfw_controller\.js') {
        $html = $html -replace '(</body>)', "    <script src=`"js/nsfw_controller.js`"></script>`n`$1"
        Write-Host "✓ Script-Tag eingefügt" -ForegroundColor Green
    }
    
    if ($html -notmatch 'terminal-nsfw-btn') {
        $button = "`n            <div class=`"modal-buttons`" style=`"margin-top: 15px;`">`n                <button class=`"modal-btn`" id=`"terminal-nsfw-btn`" style=`"width: 100%;`">⚪ NSFW Inaktiv</button>`n            </div>"
        $html = $html -replace '(</div>\s*</div>\s*<script type="importmap">)', "$button`n`$1"
        Write-Host "✓ NSFW-Button eingefügt" -ForegroundColor Green
    }
    
    Set-Content $htmlFile $html -Encoding UTF8
} else {
    Write-Host "⚠ index_3d.html nicht gefunden" -ForegroundColor Yellow
}

Write-Host ""

# ==============================================================================
# SCHRITT 4: PROMPTS
# ==============================================================================

Write-Host "=== SCHRITT 4: Prompts generieren ===" -ForegroundColor Magenta
Write-Host ""

$promptDir = "$SourceDir\prompts"
if (-not (Test-Path $promptDir)) {
    New-Item -Path $promptDir -ItemType Directory -Force | Out-Null
}

$master = @"
# NAJIKA MASTER PROMPT
$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')

$content
"@

Set-Content "$promptDir\MASTER_prompt.txt" $master -Encoding UTF8
Write-Host "✓ MASTER_prompt.txt" -ForegroundColor Green
Write-Host ""

# ==============================================================================
# FERTIG
# ==============================================================================

Write-Host "=== SETUP ABGESCHLOSSEN ===" -ForegroundColor Green
Write-Host ""
Write-Host "Erstellt:" -ForegroundColor Cyan
Write-Host "  ✓ config/najika_personality_CORE.json" -ForegroundColor White
Write-Host "  ✓ config/najika_nsfw_addon.json" -ForegroundColor White
Write-Host "  ✓ js/nsfw_controller.js" -ForegroundColor White
Write-Host "  ✓ prompts/MASTER_prompt.txt" -ForegroundColor White

if (Test-Path $htmlFile) {
    Write-Host "  ✓ index_3d.html (gepatcht)" -ForegroundColor White
}

Write-Host ""
Write-Host "STARTEN:" -ForegroundColor Yellow
Write-Host "  cd $SourceDir" -ForegroundColor White
Write-Host "  python -m http.server 8000" -ForegroundColor White
Write-Host "  Browser: http://localhost:8000/index_3d.html" -ForegroundColor White
Write-Host ""

Read-Host "Enter zum Beenden"