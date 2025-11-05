# ==============================================================================
# INSTALL_NAJIKA_NSFW.ps1
# Integriert NSFW-System in funktionierende Version
# ==============================================================================

param(
    [string]$WorkingDir = "C:\NajikaCore",
    [switch]$Backup = $true
)

Write-Host ""
Write-Host "=== NAJIKA NSFW-SYSTEM INSTALLATION ===" -ForegroundColor Cyan
Write-Host ""

# Prüfe Arbeitsverzeichnis
if (-not (Test-Path $WorkingDir)) {
    Write-Host "FEHLER: $WorkingDir nicht gefunden!" -ForegroundColor Red
    Write-Host "Erstelle Verzeichnis..." -ForegroundColor Yellow
    New-Item -Path $WorkingDir -ItemType Directory -Force | Out-Null
}

# Backup erstellen
if ($Backup) {
    $backupDir = "$WorkingDir\_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
    Write-Host "Erstelle Backup: $backupDir" -ForegroundColor Yellow
    
    if (Test-Path "$WorkingDir\index_3d.html") {
        Copy-Item -Path $WorkingDir -Destination $backupDir -Recurse -Force -ErrorAction SilentlyContinue
        Write-Host "✓ Backup erstellt" -ForegroundColor Green
    } else {
        Write-Host "⚠ Keine Dateien zum Backup gefunden" -ForegroundColor Yellow
    }
    Write-Host ""
}

# ==============================================================================
# 1. VERZEICHNISSTRUKTUR SICHERSTELLEN
# ==============================================================================

Write-Host "Prüfe Verzeichnisstruktur..." -ForegroundColor Cyan

$dirs = @(
    "$WorkingDir\js",
    "$WorkingDir\config",
    "$WorkingDir\css",
    "$WorkingDir\assets\characters",
    "$WorkingDir\assets\rooms"
)

foreach ($dir in $dirs) {
    if (-not (Test-Path $dir)) {
        New-Item -Path $dir -ItemType Directory -Force | Out-Null
        Write-Host "✓ $dir erstellt" -ForegroundColor Green
    }
}

Write-Host ""

# ==============================================================================
# 2. NSFW CONTROLLER ERSTELLEN
# ==============================================================================

Write-Host "Erstelle NSFW Controller..." -ForegroundColor Cyan

$nsfwController = @'
// ==============================================================================
// NAJIKA NSFW MODE CONTROLLER
// ==============================================================================

class NSFWModeController {
    constructor() {
        this.active = false;
        this.codewordBuffer = '';
        this.codewordTimeout = null;
        this.personality = {
            core: null,
            addon: null
        };
    }
    
    init() {
        console.log('🔧 NSFW Controller initialisiert');
        this.setupCodewordListener();
        this.setupButtonListener();
        this.loadState();
        
        // Lade initiale Persönlichkeit (nur Core)
        this.loadCorePersonality();
    }
    
    // ================================================================
    // CODEWORT ERKENNUNG
    // ================================================================
    
    setupCodewordListener() {
        document.addEventListener('keypress', (e) => {
            this.codewordBuffer += e.key.toLowerCase();
            
            clearTimeout(this.codewordTimeout);
            this.codewordTimeout = setTimeout(() => {
                this.codewordBuffer = '';
            }, 3000);
            
            if (this.codewordBuffer.includes('kätzchen')) {
                this.codewordBuffer = '';
                this.activateNSFW('codewort');
            }
        });
    }
    
    // ================================================================
    // TERMINAL BUTTON
    // ================================================================
    
    setupButtonListener() {
        const btn = document.getElementById('terminal-nsfw-btn');
        if (btn) {
            btn.addEventListener('click', () => {
                if (this.active) {
                    this.deactivateNSFW();
                } else {
                    this.activateNSFW('button');
                }
            });
        } else {
            console.warn('⚠ NSFW-Button nicht gefunden in HTML');
        }
    }
    
    // ================================================================
    // PERSÖNLICHKEIT LADEN
    // ================================================================
    
    async loadCorePersonality() {
        try {
            const response = await fetch('config/najika_personality_CORE.json');
            if (response.ok) {
                this.personality.core = await response.json();
                console.log('✓ Core Persönlichkeit geladen');
                
                if (window.najikaAI && window.najikaAI.loadPersonality) {
                    window.najikaAI.loadPersonality(this.personality.core);
                }
            }
        } catch (error) {
            console.error('✗ Fehler beim Laden der Core Persönlichkeit:', error);
        }
    }
    
    async loadNSFWAddon() {
        try {
            const response = await fetch('config/najika_nsfw_addon.json');
            if (response.ok) {
                this.personality.addon = await response.json();
                console.log('✓ NSFW-Addon geladen');
                return true;
            }
        } catch (error) {
            console.error('✗ Fehler beim Laden des NSFW-Addons:', error);
            return false;
        }
    }
    
    // ================================================================
    // AKTIVIERUNG
    // ================================================================
    
    async activateNSFW(method) {
        console.log(`🔴 NSFW aktiviert via: ${method}`);
        
        // Lade Addon
        const addonLoaded = await this.loadNSFWAddon();
        
        if (!addonLoaded) {
            console.error('✗ NSFW-Addon konnte nicht geladen werden');
            return;
        }
        
        this.active = true;
        this.updateUI();
        this.mergePersonalities();
        this.saveState();
        this.showNajikaReaction('activation');
    }
    
    // ================================================================
    // DEAKTIVIERUNG
    // ================================================================
    
    deactivateNSFW() {
        console.log('⚪ NSFW deaktiviert');
        
        this.active = false;
        this.personality.addon = null;
        
        this.updateUI();
        this.mergePersonalities();
        this.saveState();
        this.showNajikaReaction('deactivation');
    }
    
    // ================================================================
    // PERSÖNLICHKEITEN MERGEN
    // ================================================================
    
    mergePersonalities() {
        if (!window.najikaAI || !window.najikaAI.loadPersonality) {
            console.warn('⚠ najikaAI nicht verfügbar');
            return;
        }
        
        if (this.active && this.personality.addon) {
            // Merge Core + Addon
            const merged = {
                ...this.personality.core,
                nsfw: this.personality.addon,
                nsfwActive: true
            };
            window.najikaAI.loadPersonality(merged);
            console.log('✓ Core + NSFW-Addon aktiv');
        } else {
            // Nur Core
            window.najikaAI.loadPersonality(this.personality.core);
            console.log('✓ Nur Core aktiv');
        }
    }
    
    // ================================================================
    // UI UPDATE
    // ================================================================
    
    updateUI() {
        const btn = document.getElementById('terminal-nsfw-btn');
        if (!btn) return;
        
        if (this.active) {
            btn.textContent = '🔴 NSFW Aktiv';
            btn.style.background = 'linear-gradient(145deg, #e74c3c, #c0392b)';
            btn.style.boxShadow = '0 0 15px rgba(231, 76, 60, 0.5)';
        } else {
            btn.textContent = '⚪ NSFW Inaktiv';
            btn.style.background = 'linear-gradient(145deg, #555, #333)';
            btn.style.boxShadow = 'none';
        }
    }
    
    // ================================================================
    // NAJIKA REAKTION
    // ================================================================
    
    showNajikaReaction(type) {
        const chatBox = document.getElementById('chat-messages');
        if (!chatBox) return;
        
        const msg = document.createElement('div');
        msg.className = 'chat-msg najika';
        
        if (type === 'activation') {
            // Reaktion aus Config laden (falls vorhanden)
            const reaction = this.personality.addon?.meta?.activation_response || '😈';
            msg.innerHTML = `<strong>Najika:</strong> ${reaction}`;
        } else {
            const reaction = this.personality.addon?.meta?.deactivation_response || 'Okay...';
            msg.innerHTML = `<strong>Najika:</strong> ${reaction}`;
        }
        
        chatBox.appendChild(msg);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
    
    // ================================================================
    // SPEICHER-PERSISTENZ
    // ================================================================
    
    saveState() {
        localStorage.setItem('nsfw_active', this.active);
        localStorage.setItem('nsfw_timestamp', Date.now());
    }
    
    loadState() {
        const saved = localStorage.getItem('nsfw_active');
        const timestamp = parseInt(localStorage.getItem('nsfw_timestamp') || 0);
        const age = Date.now() - timestamp;
        
        // Wenn weniger als 1 Stunde alt → reaktivieren
        if (saved === 'true' && age < 3600000) {
            setTimeout(() => {
                this.activateNSFW('auto-restore');
            }, 1000);
        }
    }
}

// ====================================================================
// GLOBALE INSTANZ & AUTO-INIT
// ====================================================================

window.nsfwController = new NSFWModeController();

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.nsfwController.init();
    });
} else {
    window.nsfwController.init();
}
'@

$nsfwPath = "$WorkingDir\js\nsfw_controller.js"
Set-Content $nsfwPath $nsfwController -Encoding UTF8
Write-Host "✓ nsfw_controller.js erstellt" -ForegroundColor Green

# ==============================================================================
# 3. HTML MODIFIZIEREN
# ==============================================================================

Write-Host ""
Write-Host "Modifiziere HTML..." -ForegroundColor Cyan

$htmlFile = "$WorkingDir\index_3d.html"

if (Test-Path $htmlFile) {
    $html = Get-Content $htmlFile -Raw -Encoding UTF8
    $modified = $false
    
    # Script-Tag einfügen
    if ($html -notmatch 'nsfw_controller\.js') {
        $scriptTag = '    <script src="js/nsfw_controller.js"></script>'
        $html = $html -replace '(</body>)', "$scriptTag`n`$1"
        $modified = $true
        Write-Host "✓ NSFW Controller Script eingefügt" -ForegroundColor Green
    } else {
        Write-Host "✓ Script bereits vorhanden" -ForegroundColor Green
    }
    
    # NSFW-Button einfügen
    if ($html -notmatch 'terminal-nsfw-btn') {
        # Suche nach Terminal Buttons
        if ($html -match '(<button.*?id="terminal-export-btn".*?</button>)') {
            $buttonHtml = @'

            <div class="modal-buttons" style="margin-top: 15px; border-top: 1px solid #333; padding-top: 15px;">
                <button class="modal-btn" id="terminal-nsfw-btn" style="width: 100%; font-size: 16px; padding: 15px;">
                    ⚪ NSFW Inaktiv
                </button>
            </div>
'@
            $html = $html -replace '(</div>\s*</div>\s*<script type="importmap">)', "$buttonHtml`n`$1"
            $modified = $true
            Write-Host "✓ NSFW-Button eingefügt" -ForegroundColor Green
        } else {
            Write-Host "⚠ Terminal Buttons Section nicht gefunden - manuell einfügen" -ForegroundColor Yellow
        }
    } else {
        Write-Host "✓ Button bereits vorhanden" -ForegroundColor Green
    }
    
    if ($modified) {
        Set-Content $htmlFile $html -Encoding UTF8
        Write-Host "✓ HTML gespeichert" -ForegroundColor Green
    }
} else {
    Write-Host "⚠ index_3d.html nicht gefunden - überspringe HTML-Änderungen" -ForegroundColor Yellow
}

# ==============================================================================
# 4. NAJIKA_AI.JS ANPASSEN
# ==============================================================================

Write-Host ""
Write-Host "Passe najika_ai.js an..." -ForegroundColor Cyan

$aiFile = "$WorkingDir\js\najika_ai.js"

if (Test-Path $aiFile) {
    $aiJs = Get-Content $aiFile -Raw -Encoding UTF8
    $modified = $false
    
    if ($aiJs -notmatch 'loadPersonality\s*\(') {
        # Füge loadPersonality Funktion hinzu
        $loadFunc = @'

    loadPersonality(config) {
        console.log('📝 Lade Persönlichkeit:', config.meta?.type || 'unknown');
        this.personality = config;
        
        if (config.nsfwActive) {
            console.log('🔴 NSFW-Modus aktiv');
            this.nsfwMode = true;
        } else {
            console.log('⚪ Standard-Modus');
            this.nsfwMode = false;
        }
        
        // System-Prompt aktualisieren
        this.updateSystemPrompt();
    }
    
    updateSystemPrompt() {
        if (!this.personality) return;
        
        let prompt = this.personality.content || '';
        
        if (this.nsfwMode && this.personality.nsfw) {
            prompt += '\n\n' + (this.personality.nsfw.explicit_dialogues || '');
        }
        
        this.systemPrompt = prompt;
    }
'@
        
        # Füge vor letzter Klammer ein
        $aiJs = $aiJs -replace '(\}\s*$)', "$loadFunc`n`$1"
        $modified = $true
        Write-Host "✓ loadPersonality Funktion hinzugefügt" -ForegroundColor Green
    } else {
        Write-Host "✓ loadPersonality bereits vorhanden" -ForegroundColor Green
    }
    
    if ($modified) {
        Set-Content $aiFile $aiJs -Encoding UTF8
    }
} else {
    Write-Host "⚠ najika_ai.js nicht gefunden" -ForegroundColor Yellow
}

# ==============================================================================
# FERTIG
# ==============================================================================

Write-Host ""
Write-Host "=== INSTALLATION ABGESCHLOSSEN ===" -ForegroundColor Green
Write-Host ""
Write-Host "Dateien erstellt/geändert:" -ForegroundColor Cyan
Write-Host "  ✓ js/nsfw_controller.js" -ForegroundColor White

if (Test-Path $htmlFile) {
    Write-Host "  ✓ index_3d.html" -ForegroundColor White
}
if (Test-Path $aiFile) {
    Write-Host "  ✓ js/najika_ai.js" -ForegroundColor White
}

Write-Host ""
Write-Host "Benötigte Configs:" -ForegroundColor Cyan

$coreConfig = "$WorkingDir\config\najika_personality_CORE.json"
$nsfwConfig = "$WorkingDir\config\najika_nsfw_addon.json"

if (Test-Path $coreConfig) {
    Write-Host "  ✓ najika_personality_CORE.json vorhanden" -ForegroundColor Green
} else {
    Write-Host "  ✗ najika_personality_CORE.json FEHLT!" -ForegroundColor Red
    Write-Host "    → Erstelle mit AUTO_SORT_NAJIKA.ps1" -ForegroundColor Yellow
}

if (Test-Path $nsfwConfig) {
    Write-Host "  ✓ najika_nsfw_addon.json vorhanden" -ForegroundColor Green
} else {
    Write-Host "  ✗ najika_nsfw_addon.json FEHLT!" -ForegroundColor Red
    Write-Host "    → Erstelle mit AUTO_SORT_NAJIKA.ps1" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "NÄCHSTE SCHRITTE:" -ForegroundColor Yellow
Write-Host "  1. Configs erstellen (falls noch nicht vorhanden)" -ForegroundColor White
Write-Host "  2. Python Server starten: python -m http.server 8000" -ForegroundColor White
Write-Host "  3. Browser: http://localhost:8000/index_3d.html" -ForegroundColor White
Write-Host "  4. Terminal öffnen (Passwort: najika2025)" -ForegroundColor White
Write-Host "  5. NSFW-Button testen oder 'Kätzchen' tippen" -ForegroundColor White
Write-Host ""

Read-Host "Enter zum Beenden"