// =============================================================================
// CHAT UI - Najika World Chat System (V2 - CSS-Based)
// =============================================================================

const API_BASE = window.API_BASE_URL || 'http://localhost:8001';

class ChatUI {
    constructor() {
        this.messages = [];
        this.isOpen = false;
        this.isTyping = false;
        this.chatMode = 'public'; // 'public' oder 'private' (Kätzchen)
        this.sessionId = localStorage.getItem('najika_chat_session') || null;
        this.createChatUI();
        this.loadChatHistory();
        this.setupKeyboardShortcuts();
        console.log('[ChatUI] V2 Initialized with CSS classes, session:', this.sessionId);
    }

    createChatUI() {
        // Chat Overlay (fullscreen backdrop)
        const overlay = document.createElement('div');
        overlay.id = 'chat-overlay';
        overlay.className = 'chat-overlay';
        overlay.innerHTML = `
            <div class="chat-window">
                <div class="chat-header">
                    <h2>💬 Chat mit Najika</h2>
                    <div style="display:flex;align-items:center;gap:8px;">
                        <button id="chat-mode-btn" title="Modus wechseln" style="
                            background:transparent;border:1px solid #555;color:#aaa;
                            padding:4px 10px;border-radius:12px;cursor:pointer;
                            font-size:12px;transition:all 0.3s;font-family:inherit;
                        ">SFW</button>
                        <button class="chat-close" id="chat-close-btn">&times;</button>
                    </div>
                </div>

                <div class="chat-messages" id="chat-messages">
                    <!-- Messages will be inserted here -->
                </div>

                <div class="chat-typing" id="chat-typing">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>

                <div class="chat-input-area">
                    <input type="text" id="chat-input" placeholder="Nachricht an Najika..." autocomplete="off" />
                    <button id="chat-send-btn">Senden</button>
                </div>
            </div>
        `;
        document.body.appendChild(overlay);

        // Chat Toggle Button (FAB style, always visible when chat closed)
        const toggleBtn = document.createElement('button');
        toggleBtn.id = 'chat-toggle-btn';
        toggleBtn.innerHTML = '💬';
        toggleBtn.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, #4CAF50, #2E7D32);
            color: #fff;
            border: none;
            border-radius: 50%;
            font-size: 28px;
            cursor: pointer;
            z-index: 998;
            box-shadow: 0 4px 20px rgba(76, 175, 80, 0.5);
            transition: all 0.3s ease;
        `;
        toggleBtn.addEventListener('mouseenter', () => {
            toggleBtn.style.transform = 'scale(1.1)';
            toggleBtn.style.boxShadow = '0 6px 30px rgba(76, 175, 80, 0.7)';
        });
        toggleBtn.addEventListener('mouseleave', () => {
            toggleBtn.style.transform = 'scale(1)';
            toggleBtn.style.boxShadow = '0 4px 20px rgba(76, 175, 80, 0.5)';
        });
        toggleBtn.addEventListener('click', () => this.toggleChat());
        document.body.appendChild(toggleBtn);

        // Event Listeners
        document.getElementById('chat-close-btn').addEventListener('click', () => this.closeChat());
        document.getElementById('chat-send-btn').addEventListener('click', () => this.sendMessage());
        document.getElementById('chat-mode-btn').addEventListener('click', () => this.toggleChatMode());

        // Click outside to close
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) this.closeChat();
        });

        const input = document.getElementById('chat-input');

        // Enter to send
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Stop propagation for game controls
        input.addEventListener('keydown', (e) => e.stopPropagation());
        input.addEventListener('keyup', (e) => e.stopPropagation());

        input.addEventListener('focus', () => {
            window.chatInputFocused = true;
        });
        input.addEventListener('blur', () => {
            window.chatInputFocused = false;
        });
    }

    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isOpen) {
                this.closeChat();
            }
        });
    }

    toggleChatMode() {
        if (this.chatMode === 'public') {
            this.chatMode = 'private';
        } else {
            this.chatMode = 'public';
        }
        this.updateModeButton();
        const label = this.chatMode === 'private' ? 'Kaetzchen-Modus' : 'Normaler Modus';
        this.addMessage('System', `Modus gewechselt: ${label}`, 'system');
    }

    updateModeButton() {
        const btn = document.getElementById('chat-mode-btn');
        if (!btn) return;
        if (this.chatMode === 'private') {
            btn.textContent = 'NSFW';
            btn.style.background = 'rgba(220,20,60,0.3)';
            btn.style.borderColor = '#dc143c';
            btn.style.color = '#ff6b8a';
        } else {
            btn.textContent = 'SFW';
            btn.style.background = 'transparent';
            btn.style.borderColor = '#555';
            btn.style.color = '#aaa';
        }
    }

    toggleChat() {
        if (this.isOpen) {
            this.closeChat();
        } else {
            this.openChat();
        }
    }

    openChat() {
        const overlay = document.getElementById('chat-overlay');
        const toggleBtn = document.getElementById('chat-toggle-btn');
        const topBarBtn = document.getElementById('btn-chat');

        overlay.classList.add('active');
        if (toggleBtn) toggleBtn.style.display = 'none';
        if (topBarBtn) topBarBtn.classList.add('active');
        this.isOpen = true;

        // Focus input after animation
        setTimeout(() => {
            document.getElementById('chat-input').focus();
        }, 300);
    }

    closeChat() {
        const overlay = document.getElementById('chat-overlay');
        const toggleBtn = document.getElementById('chat-toggle-btn');
        const topBarBtn = document.getElementById('btn-chat');

        overlay.classList.remove('active');
        if (toggleBtn) toggleBtn.style.display = 'block';
        if (topBarBtn) topBarBtn.classList.remove('active');
        this.isOpen = false;
    }

    showTyping() {
        const typingEl = document.getElementById('chat-typing');
        if (typingEl) {
            typingEl.classList.add('active');
            this.isTyping = true;
        }
    }

    hideTyping() {
        const typingEl = document.getElementById('chat-typing');
        if (typingEl) {
            typingEl.classList.remove('active');
            this.isTyping = false;
        }
    }

    async sendMessage() {
        const input = document.getElementById('chat-input');
        const message = input.value.trim();
        if (!message) return;

        // Clear input
        input.value = '';

        // Codewort "kätzchen" / "kaetzchen" erkennen → Mode umschalten
        const msgLower = message.toLowerCase();
        if (msgLower === 'kätzchen' || msgLower === 'kaetzchen') {
            this.chatMode = 'private';
            this.updateModeButton();
            this.addMessage('System', 'Kaetzchen-Modus aktiviert... *schnurr*', 'system');
            return;
        }
        if (msgLower === 'normal' || msgLower === 'sfw') {
            this.chatMode = 'public';
            this.updateModeButton();
            this.addMessage('System', 'Normaler Modus aktiviert.', 'system');
            return;
        }

        // Add user message
        this.addMessage('Mr.K', message, 'user');

        // Show typing indicator
        this.showTyping();

        try {
            const response = await fetch(`${API_BASE}/api/v2/chat`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: message, mode: this.chatMode, session_id: this.sessionId, use_rag: true, use_mind: true})
            });

            this.hideTyping();

            // Check HTTP response status
            if (!response.ok) {
                console.error('[ChatUI] HTTP Error:', response.status, response.statusText);
                this.addMessage('System', `Server-Fehler (${response.status})`, 'system');
                return;
            }

            const data = await response.json();

            // Session-ID speichern für Gesprächs-Kontinuität
            if (data.session_id) {
                this.sessionId = data.session_id;
                localStorage.setItem('najika_chat_session', data.session_id);
            }

            if (data.response) {
                this.addMessage('Najika', data.response, 'assistant', data.mood);

                // ===== MIND HOOKS: Animationen/Gestik auslösen =====
                if (data.hooks && Array.isArray(data.hooks)) {
                    data.hooks.forEach(hook => {
                        if (hook.type === 'ANIMATION' && window.Companion3D) {
                            Companion3D.playAnimation(hook.content || hook.trigger);
                        }
                        if (hook.type === 'GESTURE' && window.Companion3D) {
                            Companion3D.playAnimation(hook.content || 'wave');
                        }
                    });
                }

                // Mind-Mood für Companion-Expression
                if (data.mood && window.Companion3D) {
                    const moodAnims = {
                        'happy': 'cheer', 'needy': 'wave', 'playful': 'dance',
                        'dominant': 'idle', 'possessive': 'idle'
                    };
                    const anim = moodAnims[data.mood];
                    if (anim && anim !== 'idle') {
                        Companion3D.playAnimation(anim);
                    }
                }
            } else if (data.error) {
                this.addMessage('System', 'Fehler: ' + data.error, 'system');
            } else {
                this.addMessage('System', 'Unerwartete Antwort vom Server', 'system');
            }
        } catch (error) {
            this.hideTyping();
            console.error('[ChatUI] Send error:', error);
            this.addMessage('System', 'Verbindungsfehler - ist der Server auf Port 8000 aktiv?', 'system');
        }
    }

    // Detect Najika's mood from message content
    detectMood(text) {
        const lowerText = text.toLowerCase();

        if (lowerText.includes('explosion') || lowerText.includes('💥')) {
            return { mood: 'explosion', emote: '💥', avatar: '🔥' };
        }
        if (lowerText.includes('liebe') || lowerText.includes('love') || lowerText.includes('❤') || lowerText.includes('mr. k')) {
            return { mood: 'love', emote: '💕', avatar: '💗' };
        }
        if (lowerText.includes('hmm') || lowerText.includes('interessant') || lowerText.includes('denke') || lowerText.includes('analyse')) {
            return { mood: 'thinking', emote: '🤔', avatar: '💭' };
        }
        if (lowerText.includes('hehe') || lowerText.includes('hihi') || lowerText.includes('spaß') || lowerText.includes('lustig')) {
            return { mood: 'happy', emote: '😊', avatar: '✨' };
        }
        // Default Najika mood
        return { mood: 'default', emote: '', avatar: '🎀' };
    }

    addMessage(sender, text, type = 'user', serverMood = null) {
        const container = document.getElementById('chat-messages');

        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${type}`;

        // Detect mood for Najika messages (Server-Mood hat Priorität)
        let mood = null;
        if (type === 'assistant') {
            if (serverMood) {
                // Server liefert echten Mood aus NajikaMind / Chat-Backend
                const moodMap = {
                    'happy': { mood: 'happy', emote: '😊', avatar: '✨' },
                    'excited': { mood: 'happy', emote: '😊', avatar: '✨' },
                    'needy': { mood: 'love', emote: '💕', avatar: '💗' },
                    'possessive': { mood: 'love', emote: '💕', avatar: '💗' },
                    'playful': { mood: 'happy', emote: '😊', avatar: '✨' },
                    'dominant': { mood: 'explosion', emote: '💥', avatar: '🔥' },
                    'explosive': { mood: 'explosion', emote: '💥', avatar: '🔥' },
                    'angry': { mood: 'explosion', emote: '💥', avatar: '🔥' },
                    'tsundere': { mood: 'thinking', emote: '🤔', avatar: '💭' },
                    'sad': { mood: 'love', emote: '😢', avatar: '💧' },
                    'tired': { mood: 'thinking', emote: '😴', avatar: '💤' },
                };
                mood = moodMap[serverMood] || this.detectMood(text);
            } else {
                mood = this.detectMood(text);
            }
            messageDiv.classList.add(`mood-${mood.mood}`);
        }

        // Avatar
        const avatar = document.createElement('div');
        avatar.className = 'chat-avatar';

        if (type === 'user') {
            avatar.textContent = '👤';
            avatar.title = 'Mr.K';
        } else if (type === 'assistant') {
            avatar.textContent = mood?.avatar || '🎀';
            avatar.title = 'Najika';
        } else {
            avatar.textContent = '⚙️';
            avatar.title = 'System';
        }

        // Bubble
        const bubble = document.createElement('div');
        bubble.className = 'chat-bubble';

        // Add explosion effect if detected
        if (mood?.mood === 'explosion') {
            bubble.classList.add('has-explosion');
        }

        // Optional: Add sender name for non-user messages
        if (type !== 'user') {
            const senderEl = document.createElement('div');
            senderEl.style.cssText = 'font-size: 11px; opacity: 0.7; margin-bottom: 4px; font-weight: bold;';
            senderEl.textContent = sender + (mood?.emote ? ' ' + mood.emote : '');
            bubble.appendChild(senderEl);
        }

        const textEl = document.createElement('div');
        textEl.textContent = text;
        bubble.appendChild(textEl);

        messageDiv.appendChild(avatar);
        messageDiv.appendChild(bubble);
        container.appendChild(messageDiv);

        // Scroll to bottom
        container.scrollTop = container.scrollHeight;

        // Store message
        this.messages.push({sender, text, type, timestamp: Date.now()});
    }

    async loadChatHistory() {
        try {
            const url = this.sessionId
                ? `${API_BASE}/api/v2/chat/history?session_id=${this.sessionId}`
                : `${API_BASE}/api/v2/chat/history`;
            const response = await fetch(url);

            if (!response.ok) {
                console.log('[ChatUI] History endpoint returned:', response.status);
                return;
            }

            const data = await response.json();
            const history = data.history || [];

            if (history.length > 0) {
                const recentMessages = history.slice(-20);
                recentMessages.forEach(msg => {
                    const type = msg.sender === 'Mr.K' ? 'user' : 'assistant';
                    this.addMessage(msg.sender, msg.message, type);
                });
            }
        } catch (error) {
            console.log('[ChatUI] No history loaded (server might be offline)');
        }
    }
}

// Initialize when DOM ready
document.addEventListener('DOMContentLoaded', () => {
    window.chatUI = new ChatUI();
});

// Also init if DOM already loaded
if (document.readyState !== 'loading') {
    if (!window.chatUI) {
        window.chatUI = new ChatUI();
    }
}
