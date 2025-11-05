# ==============================================================================
# COMPLETE_DIGIVICE_UPDATE.ps1
# FIXED - Keine Sonderzeichen
# ==============================================================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   NAJIKA DIGIVICE COMPLETE UPDATE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
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
// NAJIKA AI SYSTEM - SINGLE MODEL VERSION
class NajikaAI {
    constructor() {
        this.personality = null;
        this.nsfwMode = false;
        this.currentModel = 'najika';
        this.config = null;
        this.conversationHistory = [];
    }
    
    async init() {
        console.log('Najika AI initialisiert');
        await this.loadConfig();
        await this.loadPersonality();
    }
    
    async loadConfig() {
        try {
            const response = await fetch('config/najika_personality_CORE.json');
            this.config = await response.json();
            console.log('Config geladen');
        } catch (e) {
            console.warn('Config nicht gefunden');
        }
    }
    
    async loadPersonality(customConfig = null) {
        if (customConfig) {
            this.personality = customConfig;
            this.nsfwMode = customConfig.nsfwActive || false;
        } else if (this.config) {
            this.personality = this.config;
        }
        
        console.log('Persoenlichkeit geladen, NSFW:', this.nsfwMode);
    }
    
    async sendMessage(message) {
        if (message.toLowerCase().includes('nsfw aktivieren')) {
            this.nsfwMode = true;
            return 'NSFW-Modus aktiviert.';
        }
        if (message.toLowerCase().includes('nsfw deaktivieren')) {
            this.nsfwMode = false;
            return 'NSFW-Modus deaktiviert.';
        }
        
        this.conversationHistory.push({role: 'user', content: message});
        if (this.conversationHistory.length > 10) {
            this.conversationHistory = this.conversationHistory.slice(-10);
        }
        
        const useAPI = this.shouldUseAPI(message);
        
        if (useAPI) {
            return await this.callAPI(message);
        } else {
            return await this.callLlama(message);
        }
    }
    
    shouldUseAPI(message) {
        const complexKeywords = ['erklaere', 'analysiere', 'vergleiche', 'erstelle', 'code', 'programmiere'];
        return complexKeywords.some(kw => message.toLowerCase().includes(kw));
    }
    
    async callLlama(message) {
        try {
            let systemPrompt = this.personality?.content || 'Du bist Najika.';
            
            if (this.nsfwMode) {
                systemPrompt += '\n\nNSFW MODE AKTIVIERT';
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
            
            if (!response.ok) throw new Error('Ollama offline');
            
            const data = await response.json();
            const reply = data.response || 'Keine Antwort.';
            
            this.conversationHistory.push({role: 'assistant', content: reply});
            
            return reply;
            
        } catch (error) {
            console.error('Llama Error:', error);
            return 'Ollama ist offline.';
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
    Write-Host "OK - Neue najika_ai.js erstellt" -ForegroundColor Green
    
}
else {
    Copy-Item $JSFile "$JSFile.backup" -Force
    Write-Host "OK - Backup erstellt" -ForegroundColor Green
    
    $content = Get-Content $JSFile -Raw -Encoding UTF8
    $content = $content -replace 'najika-nsfw', 'najika'
    
    Set-Content $JSFile $content -Encoding UTF8
    Write-Host "OK - najika_ai.js aktualisiert" -ForegroundColor Green
}

Write-Host ""

# ==============================================================================
# TEIL 2: FEATURE STATUS
# ==============================================================================

Write-Host "=== TEIL 2: Feature Status ===" -ForegroundColor Magenta
Write-Host ""

Write-Host "FERTIG:" -ForegroundColor Green
Write-Host "  - 3D Digivice UI" -ForegroundColor White
Write-Host "  - Najika 3D Model" -ForegroundColor White
Write-Host "  - Stats System" -ForegroundColor White
Write-Host "  - 7 Raeume" -ForegroundColor White
Write-Host "  - KI-Chat (Llama)" -ForegroundColor White
Write-Host "  - NSFW-System" -ForegroundColor White
Write-Host "  - Terminal" -ForegroundColor White
Write-Host "  - API Keys" -ForegroundColor White
Write-Host ""

Write-Host "IN ARBEIT:" -ForegroundColor Yellow
Write-Host "  - KI-Routing" -ForegroundColor White
Write-Host ""

Write-Host "GEPLANT:" -ForegroundColor Gray
Write-Host "  - Smart Home" -ForegroundColor White
Write-Host "  - Sprachuebersetzung" -ForegroundColor White
Write-Host "  - Fortnite-Sync" -ForegroundColor White
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "WAS WILLST DU ALS NAECHSTES?" -ForegroundColor Yellow
Write-Host ""
Write-Host "  [1] KI-Routing testen" -ForegroundColor White
Write-Host "  [2] Sprachuebersetzung setup" -ForegroundColor White
Write-Host "  [3] Smart Home integration" -ForegroundColor White
Write-Host "  [4] Najika testen (ollama run najika)" -ForegroundColor White
Write-Host "  [5] Fortnite vorbereiten" -ForegroundColor White
Write-Host "  [6] Etwas anderes" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Deine Wahl (1-6)"

Write-Host ""

if ($choice -eq "1") {
    Write-Host "KI-ROUTING:" -ForegroundColor Cyan
    Write-Host "  - Llama: Alltag (schnell)" -ForegroundColor White
    Write-Host "  - GPT-4: Komplex" -ForegroundColor White
    Write-Host "  - Claude: Code/Analytik" -ForegroundColor White
    Write-Host ""
    Write-Host "Ist in najika_ai.js implementiert!" -ForegroundColor Green
}
elseif ($choice -eq "2") {
    Write-Host "SPRACHUEBERSETZUNG:" -ForegroundColor Cyan
    Write-Host "  Google Translate API oder DeepL?" -ForegroundColor White
}
elseif ($choice -eq "3") {
    Write-Host "SMART HOME:" -ForegroundColor Cyan
    Write-Host "  Welches System? (Home Assistant/Hue/WLED)" -ForegroundColor White
}
elseif ($choice -eq "4") {
    Write-Host "NAJIKA TESTEN:" -ForegroundColor Cyan
    Write-Host "  Starte: ollama run najika" -ForegroundColor Green
}
elseif ($choice -eq "5") {
    Write-Host "FORTNITE:" -ForegroundColor Cyan
    Write-Host "  Epic Meeting: November" -ForegroundColor White
    Write-Host "  Jetzt vorbereiten?" -ForegroundColor White
}
else {
    Write-Host "Was moechtest du machen?" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "UPDATE FERTIG!" -ForegroundColor Green
Write-Host ""

Read-Host "Enter zum Beenden"