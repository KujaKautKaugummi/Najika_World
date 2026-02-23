/**
 * NAJIKA FULLSCREEN AVATAR VIEW
 * Vollbild-Modus für Interaktion mit Najika
 */

const NajikaFullscreen = (function() {
    const API_BASE = window.API_BASE_URL || 'http://localhost:8000';

    let overlay = null;
    let isOpen = false;
    let currentMood = 'happy';
    let statusUpdateInterval = null;
    let chatMode = 'public'; // 'public' oder 'private' (Kätzchen)

    // Najika's Stimmungs-Sprites (Emojis als Platzhalter)
    const MOOD_SPRITES = {
        happy: '😊',
        excited: '🤩',
        sad: '😢',
        angry: '😤',
        tired: '😴',
        loving: '💜',
        thinking: '🤔',
        embarrassed: '😳',
        mischievous: '😏',
        hungry: '🍖',
        thirsty: '💧'
    };

    const MOOD_COLORS = {
        happy: '#FFD700',
        excited: '#FF6B6B',
        sad: '#4A9EFF',
        angry: '#FF4444',
        tired: '#9B59B6',
        loving: '#E91E63',
        thinking: '#00BCD4',
        embarrassed: '#FF69B4',
        mischievous: '#FF9800',
        hungry: '#8D6E63',
        thirsty: '#00BCD4'
    };

    /**
     * Erstellt das Fullscreen Overlay
     */
    function createOverlay() {
        if (overlay) return;

        overlay = document.createElement('div');
        overlay.id = 'najika-fullscreen-overlay';
        overlay.innerHTML = `
            <div class="najika-fs-container">
                <!-- Header -->
                <div class="najika-fs-header">
                    <div class="najika-fs-title">
                        <span class="najika-fs-name">NAJIKA</span>
                        <span class="najika-fs-status" id="najika-fs-status">Online</span>
                    </div>
                    <button class="najika-fs-close" onclick="NajikaFullscreen.close()">&times;</button>
                </div>

                <!-- Avatar Area -->
                <div class="najika-fs-avatar-area">
                    <div class="najika-fs-avatar" id="najika-fs-avatar">
                        <div class="najika-fs-sprite" id="najika-fs-sprite">😊</div>
                        <div class="najika-fs-mood" id="najika-fs-mood">Glücklich</div>
                    </div>

                    <!-- Stats Ring -->
                    <div class="najika-fs-stats">
                        <div class="stat-ring" data-stat="energy">
                            <span class="stat-icon">⚡</span>
                            <span class="stat-value" id="fs-stat-energy">100</span>
                        </div>
                        <div class="stat-ring" data-stat="hunger">
                            <span class="stat-icon">🍖</span>
                            <span class="stat-value" id="fs-stat-hunger">100</span>
                        </div>
                        <div class="stat-ring" data-stat="thirst">
                            <span class="stat-icon">💧</span>
                            <span class="stat-value" id="fs-stat-thirst">100</span>
                        </div>
                        <div class="stat-ring" data-stat="hygiene">
                            <span class="stat-icon">🚿</span>
                            <span class="stat-value" id="fs-stat-hygiene">100</span>
                        </div>
                        <div class="stat-ring" data-stat="happiness">
                            <span class="stat-icon">💜</span>
                            <span class="stat-value" id="fs-stat-happiness">100</span>
                        </div>
                    </div>
                </div>

                <!-- Chat Area -->
                <div class="najika-fs-chat">
                    <div class="najika-fs-messages" id="najika-fs-messages">
                        <div class="najika-fs-message najika-msg">
                            <span class="msg-sender">Najika</span>
                            <span class="msg-text">Hey! Schön dich zu sehen! 💜</span>
                        </div>
                    </div>
                    <div class="najika-fs-input-area">
                        <input type="text" id="najika-fs-input" placeholder="Nachricht an Najika..." />
                        <button id="najika-fs-send">Senden</button>
                    </div>
                </div>

                <!-- Quick Actions -->
                <div class="najika-fs-actions">
                    <button class="action-btn" onclick="NajikaFullscreen.action('feed')">🍖 Füttern</button>
                    <button class="action-btn" onclick="NajikaFullscreen.action('drink')">💧 Trinken</button>
                    <button class="action-btn" onclick="NajikaFullscreen.action('wash')">🚿 Waschen</button>
                    <button class="action-btn" onclick="NajikaFullscreen.action('sleep')">💤 Schlafen</button>
                    <button class="action-btn" onclick="NajikaFullscreen.action('praise')">💖 Loben</button>
                </div>
            </div>
        `;

        // Styles
        const styles = document.createElement('style');
        styles.textContent = `
            #najika-fullscreen-overlay {
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f0f23 100%);
                z-index: 100000;
                display: none;
                font-family: 'Segoe UI', sans-serif;
            }

            .najika-fs-container {
                display: flex;
                flex-direction: column;
                height: 100%;
                max-width: 600px;
                margin: 0 auto;
                padding: 10px;
            }

            .najika-fs-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 15px;
                background: rgba(0,0,0,0.5);
                border-radius: 15px;
                margin-bottom: 15px;
            }

            .najika-fs-title {
                display: flex;
                align-items: center;
                gap: 15px;
            }

            .najika-fs-name {
                font-size: 28px;
                font-weight: bold;
                color: #FFD700;
                text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
            }

            .najika-fs-status {
                font-size: 14px;
                padding: 5px 15px;
                border-radius: 20px;
                background: #4CAF50;
                color: #000;
                font-weight: bold;
            }

            .najika-fs-close {
                background: #FF4444;
                border: none;
                color: white;
                width: 40px;
                height: 40px;
                border-radius: 50%;
                font-size: 24px;
                cursor: pointer;
                transition: transform 0.2s;
            }

            .najika-fs-close:hover {
                transform: scale(1.1);
            }

            .najika-fs-avatar-area {
                flex: 0 0 auto;
                display: flex;
                flex-direction: column;
                align-items: center;
                padding: 30px;
                background: rgba(0,0,0,0.3);
                border-radius: 20px;
                margin-bottom: 15px;
            }

            .najika-fs-avatar {
                text-align: center;
            }

            .najika-fs-sprite {
                font-size: 150px;
                animation: najikaBounce 2s ease-in-out infinite;
            }

            @keyframes najikaBounce {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-10px); }
            }

            .najika-fs-mood {
                font-size: 18px;
                color: #FFD700;
                margin-top: 10px;
            }

            .najika-fs-stats {
                display: flex;
                gap: 20px;
                margin-top: 20px;
                flex-wrap: wrap;
                justify-content: center;
            }

            .stat-ring {
                display: flex;
                flex-direction: column;
                align-items: center;
                padding: 10px 15px;
                background: rgba(0,0,0,0.5);
                border-radius: 10px;
                min-width: 60px;
            }

            .stat-icon {
                font-size: 24px;
            }

            .stat-value {
                font-size: 16px;
                color: #fff;
                font-weight: bold;
            }

            .najika-fs-chat {
                flex: 1;
                display: flex;
                flex-direction: column;
                background: rgba(0,0,0,0.5);
                border-radius: 15px;
                overflow: hidden;
                margin-bottom: 15px;
            }

            .najika-fs-messages {
                flex: 1;
                overflow-y: auto;
                padding: 15px;
                display: flex;
                flex-direction: column;
                gap: 10px;
            }

            .najika-fs-message {
                padding: 10px 15px;
                border-radius: 15px;
                max-width: 85%;
            }

            .najika-fs-message.najika-msg {
                align-self: flex-start;
                background: linear-gradient(135deg, #FFD700, #FFA500);
                color: #000;
            }

            .najika-fs-message.user-msg {
                align-self: flex-end;
                background: #2196F3;
                color: #fff;
            }

            .msg-sender {
                display: block;
                font-size: 11px;
                font-weight: bold;
                opacity: 0.8;
                margin-bottom: 5px;
            }

            .msg-text {
                font-size: 14px;
            }

            .najika-fs-input-area {
                display: flex;
                padding: 10px;
                gap: 10px;
                border-top: 1px solid rgba(255,255,255,0.1);
            }

            #najika-fs-input {
                flex: 1;
                padding: 12px 15px;
                border: none;
                border-radius: 25px;
                background: rgba(255,255,255,0.1);
                color: #fff;
                font-size: 14px;
            }

            #najika-fs-input::placeholder {
                color: rgba(255,255,255,0.5);
            }

            #najika-fs-send {
                padding: 12px 25px;
                border: none;
                border-radius: 25px;
                background: #4CAF50;
                color: #fff;
                font-weight: bold;
                cursor: pointer;
                transition: background 0.2s;
            }

            #najika-fs-send:hover {
                background: #45a049;
            }

            .najika-fs-actions {
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
                justify-content: center;
                padding: 10px;
                background: rgba(0,0,0,0.3);
                border-radius: 15px;
            }

            .action-btn {
                padding: 12px 20px;
                border: none;
                border-radius: 25px;
                background: rgba(255, 215, 0, 0.2);
                color: #FFD700;
                font-size: 14px;
                cursor: pointer;
                transition: all 0.2s;
            }

            .action-btn:hover {
                background: rgba(255, 215, 0, 0.4);
                transform: translateY(-2px);
            }
        `;

        document.head.appendChild(styles);
        document.body.appendChild(overlay);

        // Event Listeners
        document.getElementById('najika-fs-send').addEventListener('click', sendMessage);
        document.getElementById('najika-fs-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
        document.getElementById('najika-fs-input').addEventListener('keydown', (e) => {
            e.stopPropagation();
        });
    }

    /**
     * Öffnet die Fullscreen View
     */
    function open() {
        if (!overlay) createOverlay();
        overlay.style.display = 'block';
        isOpen = true;

        // Start status updates
        updateStatus();
        statusUpdateInterval = setInterval(updateStatus, 5000);

        // Focus input
        setTimeout(() => {
            document.getElementById('najika-fs-input').focus();
        }, 100);

        // Log to Najika
        if (window.NajikaLogger) {
            NajikaLogger.action('Fullscreen View geöffnet');
        }

        console.log('[NajikaFullscreen] Opened');
    }

    /**
     * Schließt die Fullscreen View
     */
    function close() {
        if (overlay) {
            overlay.style.display = 'none';
        }
        isOpen = false;

        if (statusUpdateInterval) {
            clearInterval(statusUpdateInterval);
            statusUpdateInterval = null;
        }

        console.log('[NajikaFullscreen] Closed');
    }

    /**
     * Aktualisiert Najika's Status
     */
    async function updateStatus() {
        try {
            const response = await fetch(`${API_BASE}/api/state/najika`);
            const data = await response.json();

            if (data) {
                // Update stats
                document.getElementById('fs-stat-energy').textContent = Math.round(data.energy || 0);
                document.getElementById('fs-stat-hunger').textContent = Math.round(data.hunger || 0);
                document.getElementById('fs-stat-thirst').textContent = Math.round(data.thirst || 0);
                document.getElementById('fs-stat-hygiene').textContent = Math.round(data.hygiene || 0);
                document.getElementById('fs-stat-happiness').textContent = Math.round(data.happiness || 0);

                // Determine mood based on stats
                let mood = 'happy';
                if (data.hunger < 30) mood = 'hungry';
                else if (data.thirst < 30) mood = 'thirsty';
                else if (data.energy < 30) mood = 'tired';
                else if (data.hygiene < 30) mood = 'embarrassed';
                else if (data.happiness > 80) mood = 'excited';
                else if (data.happiness < 30) mood = 'sad';

                updateMood(mood);
            }
        } catch (error) {
            console.error('[NajikaFullscreen] Status update failed:', error);
        }
    }

    /**
     * Aktualisiert Najika's Stimmung
     */
    function updateMood(mood) {
        currentMood = mood;
        const sprite = document.getElementById('najika-fs-sprite');
        const moodText = document.getElementById('najika-fs-mood');

        if (sprite && MOOD_SPRITES[mood]) {
            sprite.textContent = MOOD_SPRITES[mood];
            sprite.style.textShadow = `0 0 30px ${MOOD_COLORS[mood]}`;
        }

        const moodNames = {
            happy: 'Glücklich',
            excited: 'Aufgeregt',
            sad: 'Traurig',
            angry: 'Wütend',
            tired: 'Müde',
            loving: 'Verliebt',
            thinking: 'Nachdenklich',
            embarrassed: 'Verlegen',
            mischievous: 'Frech',
            hungry: 'Hungrig',
            thirsty: 'Durstig'
        };

        if (moodText) {
            moodText.textContent = moodNames[mood] || mood;
            moodText.style.color = MOOD_COLORS[mood];
        }
    }

    /**
     * Sendet eine Nachricht an Najika
     */
    async function sendMessage() {
        const input = document.getElementById('najika-fs-input');
        const message = input.value.trim();
        if (!message) return;

        input.value = '';

        // Codewort "kätzchen" / "kaetzchen" → NSFW Mode
        const msgLower = message.toLowerCase();
        if (msgLower === 'kätzchen' || msgLower === 'kaetzchen') {
            chatMode = 'private';
            addMessage('System', 'Kaetzchen-Modus aktiviert... *schnurr*', 'system');
            return;
        }
        if (msgLower === 'normal' || msgLower === 'sfw') {
            chatMode = 'public';
            addMessage('System', 'Normaler Modus aktiviert.', 'system');
            return;
        }

        // Add user message
        addMessage('Mr.K', message, 'user');

        try {
            const response = await fetch(`${API_BASE}/api/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message, mode: chatMode })
            });

            const data = await response.json();
            if (data.response) {
                addMessage('Najika', data.response, 'najika');

                // Update mood: Server-Mood hat Priorität, sonst Text-Erkennung
                if (data.mood) {
                    updateMood(data.mood);
                } else if (data.response.includes('💜') || data.response.includes('liebe')) {
                    updateMood('loving');
                } else if (data.response.includes('😳') || data.response.includes('peinlich')) {
                    updateMood('embarrassed');
                }

                // Mind Hooks: Companion-Animationen
                if (data.hooks && window.Companion3D) {
                    data.hooks.forEach(hook => {
                        if (hook.type === 'ANIMATION') Companion3D.playAnimation(hook.content || hook.trigger);
                        if (hook.type === 'GESTURE') Companion3D.playAnimation(hook.content || 'wave');
                    });
                }
            }
        } catch (error) {
            addMessage('System', 'Verbindungsfehler', 'najika');
        }
    }

    /**
     * Fügt eine Nachricht hinzu
     */
    function addMessage(sender, text, type) {
        const messages = document.getElementById('najika-fs-messages');
        const msgDiv = document.createElement('div');
        msgDiv.className = `najika-fs-message ${type === 'user' ? 'user-msg' : 'najika-msg'}`;
        msgDiv.innerHTML = `
            <span class="msg-sender">${sender}</span>
            <span class="msg-text">${text}</span>
        `;
        messages.appendChild(msgDiv);
        messages.scrollTop = messages.scrollHeight;
    }

    /**
     * Führt eine Aktion aus
     */
    async function action(actionType) {
        try {
            const response = await fetch(`${API_BASE}/api/v2/care/${actionType}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });

            const data = await response.json();

            // Show response
            if (data.msg) {
                addMessage('Najika', data.msg, 'najika');
            }

            // Update status
            updateStatus();

            // Log
            if (window.NajikaLogger) {
                NajikaLogger.action(`Aktion: ${actionType}`);
            }
        } catch (error) {
            addMessage('System', 'Aktion fehlgeschlagen', 'najika');
        }
    }

    // Create toggle button
    function createToggleButton() {
        const btn = document.createElement('button');
        btn.id = 'najika-fullscreen-btn';
        btn.innerHTML = '👤';
        btn.title = 'Najika Vollbild';
        btn.style.cssText = `
            position: fixed;
            top: 80px;
            right: 20px;
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, #FFD700, #FFA500);
            border: none;
            border-radius: 50%;
            font-size: 24px;
            cursor: pointer;
            z-index: 9999;
            box-shadow: 0 0 15px rgba(255, 215, 0, 0.5);
            transition: transform 0.2s;
        `;
        btn.addEventListener('click', open);
        btn.addEventListener('mouseenter', () => btn.style.transform = 'scale(1.1)');
        btn.addEventListener('mouseleave', () => btn.style.transform = 'scale(1)');
        document.body.appendChild(btn);
    }

    // Initialize when DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', createToggleButton);
    } else {
        createToggleButton();
    }

    console.log('[NajikaFullscreen] Initialized');

    // Export
    return {
        open,
        close,
        action,
        isOpen: () => isOpen,
        updateMood
    };
})();

// Global export
window.NajikaFullscreen = NajikaFullscreen;
window.openNajikaFullscreen = NajikaFullscreen.open;
