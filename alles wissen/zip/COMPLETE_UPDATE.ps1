# ==============================================================================
# UPDATE_NAJIKA_AI.ps1
# Passt najika_ai.js für Single-Model System an
# ==============================================================================

$JSFile = "C:\NajikaCore\js\najika_ai.js"

Write-Host ""
Write-Host "=== UPDATE NAJIKA_AI.JS ===" -ForegroundColor Cyan
Write-Host ""

if (-not (Test-Path $JSFile)) {
    Write-Host "FEHLER: najika_ai.js nicht gefunden!" -ForegroundColor Red
    Write-Host "Erstelle neue Version..." -ForegroundColor Yellow
    
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
            console.error('✗ Config laden fehlgeschlagen:', e);
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
        // Prüfe ob NSFW-Trigger
        if (message.toLowerCase().includes('nsfw aktivieren')) {
            this.nsfwMode = true;
            return 'NSFW-Modus aktiviert. Ich kann jetzt freier sprechen.';
        }
        if (message.toLowerCase().includes('nsfw deaktivieren')) {
            this.nsfwMode = false;
            return 'NSFW-Modus deaktiviert. Zurück zum Standard-Modus.';
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
        // Nutze API für komplexe Anfragen
        const complexKeywords = ['erkläre', 'analysiere', 'vergleiche', 'erstelle', 'code', 'programmiere'];
        return complexKeywords.some(kw => message.toLowerCase().includes(kw));
    }
    
    async callLlama(message) {
        try {
            // Baue System-Prompt
            let systemPrompt = this.personality?.content || 'Du bist Najika.';
            
            if (this.nsfwMode) {
                systemPrompt += '\n\nNSFW MODE AKTIVIERT - Freie Sprache erlaubt.';
            }
            
            // Context aus History
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
            const reply = data.response || 'Keine Antwort erhalten.';
            
            this.conversationHistory.push({role: 'assistant', content: reply});
            
            return reply;
            
        } catch (error) {
            console.error('Llama Error:', error);
            return 'Entschuldigung, ich kann gerade nicht antworten. Ist Ollama aktiv?';
        }
    }
    
    async callAPI(message) {
        // Prüfe welche API verfügbar
        const openaiKey = localStorage.getItem('openai_key');
        const claudeKey = localStorage.getItem('claude_key');
        
        if (claudeKey) {
            return await this.callClaude(message, claudeKey);
        } else if (openaiKey) {
            return await this.callGPT(message, openaiKey);
        } else {
            // Fallback zu Llama
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

// Globale Instanz
window.najikaAI = new NajikaAI();

// Auto-Init
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.najikaAI.init();
    });
} else {
    window.najikaAI.init();
}
'@
    
    Set-Content $JSFile $newAI -Encoding UTF8
    Write-Host "✓ Neue najika_ai.js erstellt" -ForegroundColor Green
    
} else {
    # Backup
    Copy-Item $JSFile "$JSFile.backup" -Force
    Write-Host "✓ Backup erstellt: najika_ai.js.backup" -ForegroundColor Green
    
    # Update bestehende Datei
    $content = Get-Content $JSFile -Raw -Encoding UTF8
    
    # Ersetze Model-Logik
    $content = $content -replace "model\s*=\s*['\"]najika-nsfw['\"]", "model = 'najika'"
    $content = $content -replace "model_name:\s*['\"]najika-nsfw['\"]", "model_name: 'najika'"
    
    Set-Content $JSFile $content -Encoding UTF8
    Write-Host "✓ najika_ai.js aktualisiert" -ForegroundColor Green
}

Write-Host ""
Write-Host "=== UPDATE ABGESCHLOSSEN ===" -ForegroundColor Green
Write-Host ""

Read-Host "Enter für Teil 2 (Digivice Features)"
Write-Host ""
Write-Host "=== NAJIKA DIGIVICE - STATUS CHECK ===" -ForegroundColor Cyan
Write-Host ""

$features = @{
    "✓ 3D Digivice UI" = $true
    "✓ Najika 3D Model" = $true
    "✓ Stats System (HP/Hunger/Energy)" = $true
    "✓ Raum-System (7 Räume)" = $true
    "✓ KI-Chat (Llama)" = $true
    "✓ NSFW-System (Button + Codewort)" = $true
    "✓ Terminal (mit Passwort)" = $true
    "✓ API Keys Speicherung" = $true
    
    "⚠ KI-Routing (Llama/GPT/Claude)" = "Teilweise"
    "⚠ Smart Home Integration" = "Vorbereitet"
    "⚠ Sprachübersetzung" = "Noch nicht"
    "⚠ Bluetooth-Geräte" = "Noch nicht"
    "⚠ Video-Generierung" = "Noch nicht"
    "⚠ Fortnite-Sync" = "Noch nicht"
}

Write-Host "AKTUELLER STATUS:" -ForegroundColor Yellow
foreach ($feature in $features.Keys) {
    $status = $features[$feature]
    
    if ($status -eq $true) {
        Write-Host "  $feature" -ForegroundColor Green
    } elseif ($status -eq "Teilweise") {
        Write-Host "  $feature" -ForegroundColor Yellow
    } else {
        Write-Host "  $feature ($status)" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "PRIORITÄTEN FÜR HEUTE:" -ForegroundColor Cyan
Write-Host "  1. KI-Routing perfektionieren (GPT/Claude)" -ForegroundColor White
Write-Host "  2. Sprachübersetzung (Echtzeit)" -ForegroundColor White
Write-Host "  3. Smart Home Basics (Licht/Temp)" -ForegroundColor White
Write-Host "  4. Najika Persönlichkeit testen & feintunen" -ForegroundColor White
Write-Host ""

Write-Host "WAS WILLST DU ZUERST ANGEHEN?" -ForegroundColor Yellow
Write-Host "  [1] KI-Routing (GPT/Claude perfekt integrieren)" -ForegroundColor White
Write-Host "  [2] Sprachübersetzung (Google Translate API)" -ForegroundColor White
Write-Host "  [3] Smart Home (Basic Steuerung)" -ForegroundColor White
Write-Host "  [4] Najika Testing (Persönlichkeit optimieren)" -ForegroundColor White
Write-Host "  [5] Etwas anderes" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Deine Wahl (1-5)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "KI-ROUTING SETUP:" -ForegroundColor Cyan
        Write-Host "  - GPT-4 für komplexe Anfragen" -ForegroundColor White
        Write-Host "  - Claude für analytische Tasks" -ForegroundColor White
        Write-Host "  - Llama für Alltag (schnell)" -ForegroundColor White
        Write-Host ""
        Write-Host "Soll ich Script dafür erstellen? (j/n)" -ForegroundColor Yellow
    }
    "2" {
        Write-Host ""
        Write-Host "SPRACHÜBERSETZUNG:" -ForegroundColor Cyan
        Write-Host "  - Google Translate API" -ForegroundColor White
        Write-Host "  - Echtzeit in/aus allen Sprachen" -ForegroundColor White
        Write-Host "  - In Chat integriert" -ForegroundColor White
        Write-Host ""
        Write-Host "Soll ich Script dafür erstellen? (j/n)" -ForegroundColor Yellow
    }
    "3" {
        Write-Host ""
        Write-Host "SMART HOME:" -ForegroundColor Cyan
        Write-Host "  - Licht (Philips Hue / WLED)" -ForegroundColor White
        Write-Host "  - Temperatur (Thermostat)" -ForegroundColor White
        Write-Host "  - Home Assistant Integration" -ForegroundColor White
        Write-Host ""
        Write-Host "Welches System nutzt du? (Hue/WLED/HA/Andere)" -ForegroundColor Yellow
    }
    "4" {
        Write-Host ""
        Write-Host "NAJIKA TESTING:" -ForegroundColor Cyan
        Write-Host "  - ollama run najika" -ForegroundColor White
        Write-Host "  - Test-Szenarien durchspielen" -ForegroundColor White
        Write-Host "  - Persönlichkeit feintunen" -ForegroundColor White
        Write-Host ""
        Write-Host "Starte: ollama run najika" -ForegroundColor Green
    }
    "5" {
        Write-Host ""
        Write-Host "Was möchtest du angehen?" -ForegroundColor Yellow
    }
}

Write-Host ""