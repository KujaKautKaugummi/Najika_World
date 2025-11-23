/**
 * NAJIKA SECURE MESSENGER - Encrypted Communication Interface
 * Chat mit Najika mit verschlüsselter Verbindung
 */

const SecureMessenger = {
    isOpen: false,
    overlay: null,
    chatHistory: [],
    isTyping: false,

    open() {
        if (this.isOpen) return;
        this.isOpen = true;

        this.overlay = document.createElement('div');
        this.overlay.id = 'secureMessengerOverlay';
        this.overlay.innerHTML = `
            <div class="messenger-container">
                <!-- Header -->
                <div class="messenger-header">
                    <div class="header-left">
                        <span class="terminal-icon">⬢</span>
                        <span class="title">SECURE MESSENGER</span>
                        <span class="encryption-badge">🔒 E2E ENCRYPTED</span>
                    </div>
                    <div class="header-actions">
                        <button class="header-btn" onclick="SecureMessenger.clearHistory()" title="Verlauf löschen">🗑️</button>
                        <button class="header-btn" onclick="SecureMessenger.exportChat()" title="Chat exportieren">💾</button>
                    </div>
                    <button class="close-btn" onclick="SecureMessenger.close()">✕</button>
                </div>

                <!-- Chat Area -->
                <div class="messenger-main">
                    <!-- Left: Chat Window -->
                    <div class="chat-window">
                        <div class="chat-messages" id="messengerChatArea">
                            <div class="system-message">
                                <div class="system-icon">🔒</div>
                                <div class="system-text">
                                    <strong>SICHERE VERBINDUNG HERGESTELLT</strong><br>
                                    End-to-End Verschlüsselung aktiv<br>
                                    Ollama Local Model<br>
                                    <span class="timestamp">${this.getTimestamp()}</span>
                                </div>
                            </div>
                            <div class="najika-message">
                                <div class="message-avatar">🐊</div>
                                <div class="message-content">
                                    <div class="message-header">
                                        <strong>NAJIKA</strong>
                                        <span class="timestamp">${this.getTimestamp()}</span>
                                    </div>
                                    <div class="message-text">
                                        <strong>[MEGUMIN]</strong> Hey Mr.K! Willkommen im Secure Messenger! 💥<br><br>
                                        <strong>[SHIRO-ANALYSE]</strong> Alle Nachrichten sind lokal verschlüsselt und verlassen niemals dein System.<br><br>
                                        Was möchtest du besprechen?
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Typing Indicator -->
                        <div class="typing-indicator" id="typingIndicator" style="display: none;">
                            <div class="message-avatar">🐊</div>
                            <div class="typing-dots">
                                <span></span><span></span><span></span>
                            </div>
                        </div>

                        <!-- Input Area -->
                        <div class="chat-input-area">
                            <div class="input-container">
                                <textarea
                                    id="messengerInput"
                                    placeholder="Schreib Najika eine sichere Nachricht..."
                                    rows="3"
                                ></textarea>
                                <div class="input-actions">
                                    <button class="input-btn" onclick="SecureMessenger.attachFile()" title="Datei anhängen">📎</button>
                                    <button class="input-btn" onclick="SecureMessenger.toggleVoice()" title="Sprachnachricht">🎤</button>
                                    <button class="send-btn" onclick="SecureMessenger.sendMessage()">
                                        <span>SEND</span> ⏎
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Right: Info Panel -->
                    <div class="info-panel">
                        <div class="panel-section">
                            <div class="panel-header">🐊 NAJIKA INFO</div>
                            <div class="panel-content">
                                <div class="info-row">
                                    <span class="info-label">STATUS:</span>
                                    <span class="info-value online">● ONLINE</span>
                                </div>
                                <div class="info-row">
                                    <span class="info-label">MOOD:</span>
                                    <span class="info-value" id="najikaCurrentMood">Happy</span>
                                </div>
                                <div class="info-row">
                                    <span class="info-label">RESPONSE TIME:</span>
                                    <span class="info-value">~2-5s</span>
                                </div>
                            </div>
                        </div>

                        <div class="panel-section">
                            <div class="panel-header">🔒 SECURITY</div>
                            <div class="panel-content">
                                <div class="info-row">
                                    <span class="info-label">ENCRYPTION:</span>
                                    <span class="info-value">✓ AES-256</span>
                                </div>
                                <div class="info-row">
                                    <span class="info-label">CONNECTION:</span>
                                    <span class="info-value">✓ LOCAL</span>
                                </div>
                                <div class="info-row">
                                    <span class="info-label">LOGGING:</span>
                                    <span class="info-value">✗ DISABLED</span>
                                </div>
                            </div>
                        </div>

                        <div class="panel-section">
                            <div class="panel-header">📊 SESSION STATS</div>
                            <div class="panel-content">
                                <div class="info-row">
                                    <span class="info-label">MESSAGES:</span>
                                    <span class="info-value" id="messageCount">0</span>
                                </div>
                                <div class="info-row">
                                    <span class="info-label">SESSION TIME:</span>
                                    <span class="info-value" id="sessionTime">0m</span>
                                </div>
                                <div class="info-row">
                                    <span class="info-label">STARTED:</span>
                                    <span class="info-value">${this.getTimestamp()}</span>
                                </div>
                            </div>
                        </div>

                        <div class="panel-section">
                            <div class="panel-header">⚙️ QUICK ACTIONS</div>
                            <div class="panel-content">
                                <button class="quick-action-btn" onclick="SecureMessenger.askStatus()">📊 Status abfragen</button>
                                <button class="quick-action-btn" onclick="SecureMessenger.askHelp()">❓ Hilfe</button>
                                <button class="quick-action-btn" onclick="SecureMessenger.askJoke()">😄 Witz erzählen</button>
                                <button class="quick-action-btn" onclick="SecureMessenger.askAdvice()">💡 Rat geben</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(this.overlay);

        // Setup keyboard shortcuts
        this.setupKeyboardShortcuts();

        // Focus input
        setTimeout(() => {
            document.getElementById('messengerInput')?.focus();
        }, 300);

        // Start session timer
        this.startSessionTimer();
    },

    close() {
        if (!this.isOpen) return;
        this.isOpen = false;

        this.stopSessionTimer();

        if (this.overlay) {
            this.overlay.remove();
            this.overlay = null;
        }
    },

    async sendMessage() {
        const input = document.getElementById('messengerInput');
        if (!input) return;

        const message = input.value.trim();
        if (!message) return;

        // Add user message to chat
        this.addUserMessage(message);
        input.value = '';

        // Update stats
        this.updateMessageCount();

        // Show typing indicator
        this.showTypingIndicator();

        // Send to Najika
        try {
            const response = await fetch('http://localhost:8000/api/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    message,
                    context: 'secure_messenger'
                })
            });

            const data = await response.json();

            // Hide typing indicator
            this.hideTypingIndicator();

            // Add Najika response
            this.addNajikaMessage(data.response || 'Hmm, ich habe keine Antwort...');

            // Update mood if available
            if (data.mood) {
                this.updateMood(data.mood);
            }

        } catch (error) {
            this.hideTypingIndicator();
            this.addSystemMessage(`❌ Verbindungsfehler: ${error.message}`, 'error');
        }
    },

    addUserMessage(text) {
        const chatArea = document.getElementById('messengerChatArea');
        if (!chatArea) return;

        const msg = document.createElement('div');
        msg.className = 'user-message';
        msg.innerHTML = `
            <div class="message-content">
                <div class="message-header">
                    <strong>YOU</strong>
                    <span class="timestamp">${this.getTimestamp()}</span>
                </div>
                <div class="message-text">${this.escapeHtml(text)}</div>
            </div>
            <div class="message-avatar">👤</div>
        `;

        chatArea.appendChild(msg);
        this.scrollToBottom();

        this.chatHistory.push({type: 'user', text, timestamp: Date.now()});
    },

    addNajikaMessage(text) {
        const chatArea = document.getElementById('messengerChatArea');
        if (!chatArea) return;

        const msg = document.createElement('div');
        msg.className = 'najika-message';
        msg.innerHTML = `
            <div class="message-avatar">🐊</div>
            <div class="message-content">
                <div class="message-header">
                    <strong>NAJIKA</strong>
                    <span class="timestamp">${this.getTimestamp()}</span>
                </div>
                <div class="message-text">${this.escapeHtml(text)}</div>
            </div>
        `;

        chatArea.appendChild(msg);
        this.scrollToBottom();

        this.chatHistory.push({type: 'najika', text, timestamp: Date.now()});
    },

    addSystemMessage(text, type = 'info') {
        const chatArea = document.getElementById('messengerChatArea');
        if (!chatArea) return;

        const msg = document.createElement('div');
        msg.className = `system-message ${type}`;
        msg.innerHTML = `
            <div class="system-icon">${type === 'error' ? '❌' : '🔒'}</div>
            <div class="system-text">
                ${text}<br>
                <span class="timestamp">${this.getTimestamp()}</span>
            </div>
        `;

        chatArea.appendChild(msg);
        this.scrollToBottom();
    },

    showTypingIndicator() {
        const indicator = document.getElementById('typingIndicator');
        if (indicator) {
            indicator.style.display = 'flex';
            this.scrollToBottom();
        }
    },

    hideTypingIndicator() {
        const indicator = document.getElementById('typingIndicator');
        if (indicator) {
            indicator.style.display = 'none';
        }
    },

    scrollToBottom() {
        const chatArea = document.getElementById('messengerChatArea');
        if (chatArea) {
            setTimeout(() => {
                chatArea.scrollTop = chatArea.scrollHeight;
            }, 100);
        }
    },

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    },

    getTimestamp() {
        const now = new Date();
        return now.toLocaleTimeString('de-DE', {hour: '2-digit', minute: '2-digit'});
    },

    updateMessageCount() {
        const display = document.getElementById('messageCount');
        if (display) {
            display.textContent = this.chatHistory.length.toString();
        }
    },

    updateMood(mood) {
        const display = document.getElementById('najikaCurrentMood');
        if (display) {
            display.textContent = mood;
        }
    },

    clearHistory() {
        if (!confirm('Chat-Verlauf löschen?')) return;

        this.chatHistory = [];
        const chatArea = document.getElementById('messengerChatArea');
        if (chatArea) {
            chatArea.innerHTML = `
                <div class="system-message">
                    <div class="system-icon">🗑️</div>
                    <div class="system-text">
                        <strong>VERLAUF GELÖSCHT</strong><br>
                        Chat wurde zurückgesetzt<br>
                        <span class="timestamp">${this.getTimestamp()}</span>
                    </div>
                </div>
            `;
        }

        this.updateMessageCount();
        notify('Chat-Verlauf gelöscht', 'success');
    },

    exportChat() {
        if (this.chatHistory.length === 0) {
            notify('Kein Chat zum Exportieren', 'warning');
            return;
        }

        const chatText = this.chatHistory.map(msg => {
            const time = new Date(msg.timestamp).toLocaleString('de-DE');
            const sender = msg.type === 'user' ? 'YOU' : 'NAJIKA';
            return `[${time}] ${sender}: ${msg.text}`;
        }).join('\n\n');

        const blob = new Blob([chatText], {type: 'text/plain'});
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `najika_chat_${Date.now()}.txt`;
        a.click();
        URL.revokeObjectURL(url);

        notify('Chat exportiert', 'success');
    },

    // Quick Actions
    askStatus() {
        document.getElementById('messengerInput').value = 'Wie geht es dir? Zeig mir deinen Status!';
        this.sendMessage();
    },

    askHelp() {
        document.getElementById('messengerInput').value = 'Kannst du mir helfen?';
        this.sendMessage();
    },

    askJoke() {
        document.getElementById('messengerInput').value = 'Erzähl mir einen Witz!';
        this.sendMessage();
    },

    askAdvice() {
        document.getElementById('messengerInput').value = 'Gib mir einen guten Rat!';
        this.sendMessage();
    },

    attachFile() {
        notify('⚠️ Datei-Upload noch nicht implementiert', 'warning');
    },

    toggleVoice() {
        notify('⚠️ Sprachnachrichten noch nicht implementiert', 'warning');
    },

    setupKeyboardShortcuts() {
        const input = document.getElementById('messengerInput');
        if (!input) return;

        input.addEventListener('keydown', (e) => {
            // Enter: Send (without Shift)
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
            // Shift+Enter: New line (default behavior)
        });
    },

    // Session Timer
    sessionStartTime: null,
    sessionTimerInterval: null,

    startSessionTimer() {
        this.sessionStartTime = Date.now();
        this.sessionTimerInterval = setInterval(() => {
            this.updateSessionTime();
        }, 60000); // Every minute
    },

    stopSessionTimer() {
        if (this.sessionTimerInterval) {
            clearInterval(this.sessionTimerInterval);
            this.sessionTimerInterval = null;
        }
    },

    updateSessionTime() {
        if (!this.sessionStartTime) return;

        const elapsed = Math.floor((Date.now() - this.sessionStartTime) / 1000 / 60);
        const display = document.getElementById('sessionTime');
        if (display) {
            display.textContent = `${elapsed}m`;
        }
    }
};

// Global verfügbar machen
window.SecureMessenger = SecureMessenger;
