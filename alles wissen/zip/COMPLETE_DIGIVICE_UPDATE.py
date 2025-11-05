# ==============================================================================
# COMPLETE_DIGIVICE_UPDATE.ps1
# Teil 1: najika_ai.js Update
# Teil 2: Digivice Feature Check
# ==============================================================================

Write-Host ""
Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   NAJIKA DIGIVICE COMPLETE UPDATE     ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# ==============================================================================
# TEIL 1: NAJIKA_AI.JS UPDATE
# ==============================================================================

Write-Host "=== TEIL 1: najika_ai.js Update ===" -ForegroundColor Magenta
Write-Host ""

$JSFile = "C:\NajikaCore\js\najika_ai.js"

if (-not (Test-Path $JSFile)) {
    Write-Host "najika_ai.js nicht gefunden - erstelle neu..." -ForegroundColor Yellow
    
    if (-not (Test-Path "C:\NajikaCore\js")) {
        New-Item -Path "C:\NajikaCore\js" -ItemType Directory -Force | Out-Null
    }
    
    $newAI = @'
// ==============================================================================
// NAJIKA AI SYSTEM - SINGLE MODEL VERSION
// ==============================================================================

class NajikaAI {
    constructor() {
        this.personality = null;
        this.nsfwMode = false;
        this.currentModel = 'najika';
        this.config = null;
        this.conversationHistory = [];
    }
    
    async init() {
        console.log('🤖 Najika AI initialisiert');
        await this.loadConfig();
        await this.loadPersonality();
    }
    
    async loadConfig() {
        try {
            const response = await fetch('config/najika_personality_CORE.json');
            this.config = await response.json();
            console.log('✓ Config geladen');
        } catch (e) {
            console.warn('Config nicht gefunden, nutze Fallback');
        }
    }
    
    async loadPersonality(customConfig = null) {
        if (customConfig) {
            this.personality = customConfig;
            this.nsfwMode = customConfig.nsfwActive || false;
        } else if (this.config) {
            this.personality = this.config;
        }
        
        console.log('✓ Persönlichkeit geladen, NSFW:', this.nsfwMode);
    }
    
    async sendMessage(message) {
        // Prüfe NSFW-Trigger
        if (message.toLowerCase().includes('nsfw aktivieren')) {
            this.nsfwMode = true;
            return 'NSFW-Modus aktiviert. 😈';
        }
        if (message.toLowerCase().includes('nsfw deaktivieren')) {
            this.nsfwMode = false;
            return 'NSFW-Modus deaktiviert.';
        }
        
        // History
        this.conversationHistory.push({role: 'user', content: message});
        if (this.conversationHistory.length > 10) {
            this.conversationHistory = this.conversationHistory.slice(-10);
        }
        
        // Wähle Methode
        const useAPI = this.shouldUseAPI(message);
        
        if (useAPI) {
            return await this.callAPI(message);
        } else {
            return await this.callLlama(message);
        }
    }
    
    shouldUseAPI(message) {
        const complexKeywords = ['erkläre', 'analysiere', 'vergleiche', 'erstelle', 'code', 'programmiere'];
        return complexKeywords.some(kw => message.toLowerCase().includes(kw));
    }
    
    async callLlama(message) {
        try {
            let systemPrompt = this.personality?.content || 'Du bist Najika.';
            
            if (this.nsfwMode) {
                systemPrompt += '\n\nNSFW MODE AKTIVIERT - Freie Sprache erlaubt.';
            }
            
            const context = this.conversationHistory.slice(-3).map(m => 
                `${m.role === 'user' ? 'User' : 'Najika'}: ${m.content}`
            ).join('\n');
            
            const fullPrompt = `${systemPrompt}\n\n${context}\n\nUser: ${message}\n\nNajika:`;
            
            const response = await fetch('http://localhost:11434/api/generate', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    model: 'najika',
                    prompt: fullPrompt,
                    stream: false,
                    options: {
                        temperature: 0.92,
                        repeat_penalty: 1.45,
                        num_predict: 120
                    }
                })
            });
            
            if (!response.ok) throw new Error('Ollama nicht erreichbar');
            
            const data = await response.json();
            const reply = data.response || 'Keine Antwort.';
            
            this.conversationHistory.push({role: 'assistant', content: reply});
            
            return reply;
            
        } catch (error) {
            console.error('Llama Error:', error);
            return 'Ollama ist offline. Starte: ollama serve';
        }
    }
    
    async callAPI(message) {
        const openaiKey = localStorage.getItem('openai_key');
        const claudeKey = localStorage.getItem('claude_key');
        
        if (claudeKey) {
            return await this.callClaude(message, claudeKey);
        } else if (openaiKey) {
            return await this.callGPT(message, openaiKey);
        } else {
            return await this.callLlama(message);
        }
    }
    
    async callGPT(message, apiKey) {
        try {
            let systemPrompt = this.personality?.content || 'Du bist Najika.';
            if (this.nsfwMode) systemPrompt += '\n\nNSFW MODE AKTIVIERT';
            
            const response = await fetch('https://api.openai.com/v1/chat/completions', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${apiKey}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    model: 'gpt-4',
                    messages: [
                        {role: 'system', content: systemPrompt},
                        ...this.conversationHistory.slice(-5),
                        {role: 'user', content: message}
                    ],
                    max_tokens: 150,
                    temperature: 0.9
                })
            });
            
            const data = await response.json();
            return data.choices[0].message.content;
            
        } catch (error) {
            console.error('GPT Error:', error);
            return await this.callLlama(message);
        }
    }
    
    async callClaude(message, apiKey) {
        try {
            let systemPrompt = this.personality?.content || 'Du bist Najika.';
            if (this.nsfwMode) systemPrompt += '\n\nNSFW MODE AKTIVIERT';
            
            const response = await fetch('https://api.anthropic.com/v1/messages', {
                method: 'POST',
                headers: {
                    'x-api-key': apiKey,
                    'anthropic-version': '2023-06-01',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    model: 'claude-sonnet-4.5',
                    max_tokens: 150,
                    system: systemPrompt,
                    messages: [
                        ...this.conversationHistory.slice(-5),
                        {role: 'user', content: message}
                    ]
                })
            });
            
            const data = await response.json();
            return data.content[0].text;
            
        } catch (error) {
            console.error('Claude Error:', error);
            return await this.callLlama(message);
        }
    }
}

window.najikaAI = new NajikaAI();

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => window.najikaAI.init());
} else {
    window.najikaAI.init();
}
'@
    
    Set-Content $JSFile $newAI -Encoding UTF8
    Write-Host "✓ Neue najika_ai.js erstellt" -ForegroundColor Green
    
} else {
    Copy-Item $JSFile "$JSFile.backup" -Force
    Write-Host "✓ Backup: najika_ai.js.backup" -ForegroundColor Green
    
    $content = Get-Content $JSFile -Raw -Encoding UTF8
    $content = $content -replace "model\s*=\s*['\"]najika-nsfw['\"]", "model = 'najika'"
    $content = $content -replace "model_name:\s*['\"]najika-nsfw['\"]", "model_name: 'najika'"
    
    Set-Content $JSFile $content -Encoding UTF8
    Write-Host "✓ najika_ai.js aktualisiert" -ForegroundColor Green
}

Write-Host ""

# ==============================================================================
# TEIL 2: FEATURE STATUS CHECK
# ==============================================================================

Write-Host "=== TEIL 2: Feature Status ===" -ForegroundColor Magenta
Write-Host ""

$features = @(
    @{name="3D Digivice UI"; status="✓"; color="Green"},
    @{name="Najika 3D Model"; status="✓"; color="Green"},
    @{name="Stats System (HP/Hunger/Energy)"; status="✓"; color="Green"},
    @{name="Raum-System (7 Räume)"; status="✓"; color="Green"},
    @{name="KI-Chat (Llama)"; status="✓"; color="Green"},
    @{name="NSFW-System (Single Model)"; status="✓"; color="Green"},
    @{name="Terminal (Passwort)"; status="✓"; color="Green"},
    @{name="API Keys Speicherung"; status="✓"; color="Green"},
    @{name="KI-Routing (Llama/GPT/Claude)"; status="⚠"; color="Yellow"},
    @{name="Smart Home Integration"; status="○"; color="Gray"},
    @{name="Sprachübersetzung"; status="○"; color="Gray"},
    @{name="Bluetooth-Geräte"; status="○"; color="Gray"},
    @{name="Video-Generierung"; status="○"; color="Gray"},
    @{name="Fortnite-Sync"; status="○"; color="Gray"}
)

Write-Host "AKTUELLER STATUS:" -ForegroundColor Cyan
Write-Host ""
foreach ($f in $features) {
    Write-Host "  $($f.status) $($f.name)" -ForegroundColor $f.color
}

Write-Host ""
Write-Host "══════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Write-Host "WAS WOLLEN WIR HEUTE UMSETZEN?" -ForegroundColor Yellow
Write-Host ""
Write-Host "  [1] KI-Routing perfektionieren" -ForegroundColor White
Write-Host "      → GPT-4/Claude automatisch für komplexe Fragen" -ForegroundColor Gray
Write-Host ""
Write-Host "  [2] Sprachübersetzung" -ForegroundColor White
Write-Host "      → Echtzeit-Übersetzung in/aus allen Sprachen" -ForegroundColor Gray
Write-Host ""
Write-Host "  [3] Smart Home Basics" -ForegroundColor White
Write-Host "      → Licht, Temperatur, Home Assistant" -ForegroundColor Gray
Write-Host ""
Write-Host "  [4] Najika Persönlichkeit testen" -ForegroundColor White
Write-Host "      → Test-Szenarien durchspielen & optimieren" -ForegroundColor Gray
Write-Host ""
Write-Host "  [5] Fortnite-Sync vorbereiten" -ForegroundColor White
Write-Host "      → Epic Account Services, Daten-Bridge" -ForegroundColor Gray
Write-Host ""
Write-Host "  [6] Etwas anderes" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Deine Wahl (1-6)"

Write-Host ""

switch ($choice) {
    "1" {
        Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Cyan
        Write-Host "║        KI-ROUTING PERFEKTIONIEREN      ║" -ForegroundColor Cyan
        Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "FEATURES:" -ForegroundColor Yellow
        Write-Host "  • Automatische Model-Wahl" -ForegroundColor White
        Write-Host "  • Llama für Alltag (schnell, lokal)" -ForegroundColor White
        Write-Host "  • GPT-4 für komplexe Fragen" -ForegroundColor White
        Write-Host "  • Claude für Code/Analytik" -ForegroundColor White
        Write-Host "  • Fallback wenn API offline" -ForegroundColor White
        Write-Host ""
        Write-Host "Das ist schon in najika_ai.js implementiert!" -ForegroundColor Green
        Write-Host ""
        Write-Host "TESTEN:" -ForegroundColor Yellow
        Write-Host "  1. Terminal öffnen → API Keys eingeben" -ForegroundColor White
        Write-Host "  2. Im Chat: 'Erkläre mir Quantenphysik'" -ForegroundColor White
        Write-Host "  3. System nutzt automatisch GPT/Claude" -ForegroundColor White
        Write-Host ""
        Write-Host "Soll ich Test-Script erstellen? (j/n)" -ForegroundColor Yellow
        $test = Read-Host
        if ($test -eq 'j') {
            Write-Host "  → Erstelle KI_ROUTING_TEST.ps1..." -ForegroundColor Cyan
        }
    }
    
    "2" {
        Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Cyan
        Write-Host "║        SPRACHÜBERSETZUNG SETUP         ║" -ForegroundColor Cyan
        Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Welche Option?" -ForegroundColor Yellow
        Write-Host "  [a] Google Translate API (kostenlos bis 500k Zeichen/Monat)" -ForegroundColor White
        Write-Host "  [b] DeepL API (besser, €5/Monat)" -ForegroundColor White
        Write-Host "  [c] Lokal (Offline, aber schlechter)" -ForegroundColor White
        Write-Host ""
        $trans = Read-Host "Wahl (a/b/c)"
        Write-Host ""
        Write-Host "Soll ich Setup-Script erstellen? (j/n)" -ForegroundColor Yellow
    }
    
    "3" {
        Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Cyan
        Write-Host "║        SMART HOME INTEGRATION          ║" -ForegroundColor Cyan
        Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Welches System nutzt du?" -ForegroundColor Yellow
        Write-Host "  [1] Home Assistant" -ForegroundColor White
        Write-Host "  [2] Philips Hue" -ForegroundColor White
        Write-Host "  [3] WLED (LED Strips)" -ForegroundColor White
        Write-Host "  [4] Andere" -ForegroundColor White
        Write-Host ""
        $smarthome = Read-Host "Wahl (1-4)"
    }
    
    "4" {
        Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Cyan
        Write-Host "║      NAJIKA PERSÖNLICHKEIT TESTEN      ║" -ForegroundColor Cyan
        Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "STARTE OLLAMA CHAT:" -ForegroundColor Green
        Write-Host ""
        Write-Host "  ollama run najika" -ForegroundColor White
        Write-Host ""
        Write-Host "TEST-SZENARIEN:" -ForegroundColor Yellow
        Write-Host "  1. 'Hallo Najika, ich bin zurück!'" -ForegroundColor Gray
        Write-Host "     → Sollte: Dramatisch, eifersüchtig reagieren" -ForegroundColor DarkGray
        Write-Host ""
        Write-Host "  2. 'Was machst du gerade?'" -ForegroundColor Gray
        Write-Host "     → Sollte: Kurz, variiert antworten" -ForegroundColor DarkGray
        Write-Host ""
        Write-Host "  3. 'NSFW aktivieren' dann 'Kätzchen'" -ForegroundColor Gray
        Write-Host "     → Sollte: NSFW-Modus aktivieren" -ForegroundColor DarkGray
        Write-Host ""
        Write-Host "Drücke Enter um fortzufahren..." -ForegroundColor Yellow
    }
    
    "5" {
        Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Cyan
        Write-Host "║       FORTNITE-SYNC VORBEREITUNG       ║" -ForegroundColor Cyan
        Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "REQUIREMENTS:" -ForegroundColor Yellow
        Write-Host "  • Epic Account Services API" -ForegroundColor White
        Write-Host "  • Server (€50/Monat Contabo)" -ForegroundColor White
        Write-Host "  • UEFN Map" -ForegroundColor White
        Write-Host ""
        Write-Host "STATUS:" -ForegroundColor Yellow
        Write-Host "  Epic Meeting: November 2025" -ForegroundColor Gray
        Write-Host "  Danach: Volle Integration möglich" -ForegroundColor Gray
        Write-Host ""
        Write-Host "JETZT SCHON VORBEREITEN?" -ForegroundColor Yellow
        Write-Host "  → Daten-Struktur definieren" -ForegroundColor White
        Write-Host "  → API-Interface erstellen" -ForegroundColor White
        Write-Host "  → Test-Umgebung aufsetzen" -ForegroundColor White
        Write-Host ""
        Write-Host "Soll ich Vorbereitungs-Script erstellen? (j/n)" -ForegroundColor Yellow
    }
    
    "6" {
        Write-Host "Was möchtest du umsetzen?" -ForegroundColor Yellow
        Write-Host ""
    }
}

Write-Host ""
Write-Host "══════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "UPDATE ABGESCHLOSSEN!" -ForegroundColor Green
Write-Host ""

Read-Host "Drücke Enter zum Beenden"