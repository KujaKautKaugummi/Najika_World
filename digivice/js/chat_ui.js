// =============================================================================
// CHAT UI - Najika World Chat System
// =============================================================================

class ChatUI {
    constructor() {
        this.messages = [];
        this.isOpen = false;
        this.createChatUI();
        this.loadChatHistory();
        this.setupKeyboardShortcuts();

        console.log('[ChatUI] Initialized');
    }

    createChatUI() {
        // Chat Container
        const chatContainer = document.createElement('div');
        chatContainer.id = 'chat-container';
        chatContainer.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 350px;
            height: 450px;
            background: rgba(0, 0, 0, 0.95);
            border: 2px solid #4CAF50;
            border-radius: 10px;
            display: flex;
            flex-direction: column;
            z-index: 500;
            font-family: monospace;
            display: none;
        `;

        chatContainer.innerHTML = `
            <div id="chat-header" style="
                background: #4CAF50;
                color: #000;
                padding: 10px;
                font-weight: bold;
                border-radius: 8px 8px 0 0;
                display: flex;
                justify-content: space-between;
                align-items: center;
            ">
                <span>💬 Chat mit Najika</span>
                <button id="chat-close-btn" style="
                    background: transparent;
                    border: none;
                    color: #000;
                    font-size: 20px;
                    cursor: pointer;
                    font-weight: bold;
                ">×</button>
            </div>

            <div id="chat-messages" style="
                flex: 1;
                overflow-y: auto;
                padding: 10px;
                display: flex;
                flex-direction: column;
                gap: 8px;
            "></div>

            <div id="chat-input-container" style="
                padding: 10px;
                border-top: 1px solid #333;
                display: flex;
                gap: 8px;
            ">
                <input type="text" id="chat-input" placeholder="Nachricht an Najika..." style="
                    flex: 1;
                    background: #222;
                    color: #fff;
                    border: 1px solid #444;
                    padding: 8px;
                    border-radius: 5px;
                    font-family: monospace;
                    font-size: 13px;
                " />
                <button id="chat-send-btn" style="
                    background: #4CAF50;
                    color: #000;
                    border: none;
                    padding: 8px 15px;
                    border-radius: 5px;
                    cursor: pointer;
                    font-weight: bold;
                    font-family: monospace;
                ">Send</button>
            </div>
        `;

        document.body.appendChild(chatContainer);

        // Chat Toggle Button (always visible)
        const chatToggleBtn = document.createElement('button');
        chatToggleBtn.id = 'chat-toggle-btn';
        chatToggleBtn.innerHTML = '💬';
        chatToggleBtn.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 60px;
            height: 60px;
            background: #4CAF50;
            color: #fff;
            border: none;
            border-radius: 50%;
            font-size: 28px;
            cursor: pointer;
            z-index: 499;
            box-shadow: 0 0 15px rgba(76, 175, 80, 0.5);
            transition: all 0.3s ease;
        `;
        chatToggleBtn.addEventListener('click', () => this.toggleChat());
        document.body.appendChild(chatToggleBtn);

        // Event Listeners
        document.getElementById('chat-close-btn').addEventListener('click', () => this.closeChat());
        document.getElementById('chat-send-btn').addEventListener('click', () => this.sendMessage());
        document.getElementById('chat-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });
    }

    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // T key to open chat (like MMOs)
            if (e.key === 't' || e.key === 'T') {
                // Don't open if already typing in input
                if (document.activeElement.tagName === 'INPUT') return;

                e.preventDefault();
                this.openChat();
            }

            // Escape to close chat
            if (e.key === 'Escape' && this.isOpen) {
                this.closeChat();
            }
        });
    }

    toggleChat() {
        if (this.isOpen) {
            this.closeChat();
        } else {
            this.openChat();
        }
    }

    openChat() {
        const chatContainer = document.getElementById('chat-container');
        const chatToggleBtn = document.getElementById('chat-toggle-btn');

        chatContainer.style.display = 'flex';
        chatToggleBtn.style.display = 'none';
        this.isOpen = true;

        // Focus input
        setTimeout(() => {
            document.getElementById('chat-input').focus();
        }, 100);
    }

    closeChat() {
        const chatContainer = document.getElementById('chat-container');
        const chatToggleBtn = document.getElementById('chat-toggle-btn');

        chatContainer.style.display = 'none';
        chatToggleBtn.style.display = 'block';
        this.isOpen = false;
    }

    async sendMessage() {
        const input = document.getElementById('chat-input');
        const message = input.value.trim();

        if (!message) return;

        // Clear input
        input.value = '';

        // Add user message to UI
        this.addMessage('Mr.K', message, 'user');

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: message})
            });

            const data = await response.json();

            if (data.ok) {
                // Add Najika's response
                this.addMessage('Najika', data.response, 'najika');
            } else {
                this.addMessage('System', 'Fehler: ' + (data.error || 'Unbekannter Fehler'), 'system');
            }
        } catch (error) {
            console.error('[ChatUI] Send error:', error);
            this.addMessage('System', 'Verbindungsfehler', 'system');
        }
    }

    addMessage(sender, text, type = 'user') {
        const messagesContainer = document.getElementById('chat-messages');

        const messageDiv = document.createElement('div');
        messageDiv.style.cssText = `
            padding: 8px;
            border-radius: 8px;
            max-width: 80%;
            word-wrap: break-word;
            ${type === 'user' ? 'align-self: flex-end; background: #2196F3; color: #fff;' : ''}
            ${type === 'najika' ? 'align-self: flex-start; background: #FFD700; color: #000;' : ''}
            ${type === 'system' ? 'align-self: center; background: #666; color: #fff; font-size: 11px;' : ''}
        `;

        const senderSpan = document.createElement('div');
        senderSpan.style.cssText = `
            font-weight: bold;
            font-size: 11px;
            margin-bottom: 4px;
            opacity: 0.8;
        `;
        senderSpan.textContent = sender;

        const textDiv = document.createElement('div');
        textDiv.style.fontSize = '13px';
        textDiv.textContent = text;

        if (type !== 'system') {
            messageDiv.appendChild(senderSpan);
        }
        messageDiv.appendChild(textDiv);

        messagesContainer.appendChild(messageDiv);

        // Auto-scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;

        // Store message
        this.messages.push({sender, text, type, timestamp: Date.now()});
    }

    async loadChatHistory() {
        try {
            const response = await fetch('/api/chat/history');
            const data = await response.json();

            if (data.ok && data.history && data.history.length > 0) {
                // Load last 20 messages
                const recentMessages = data.history.slice(-20);
                recentMessages.forEach(msg => {
                    this.addMessage(msg.sender, msg.message, msg.sender === 'Mr.K' ? 'user' : 'najika');
                });
            }
        } catch (error) {
            console.error('[ChatUI] Failed to load history:', error);
        }
    }
}

// Initialize when DOM ready
document.addEventListener('DOMContentLoaded', () => {
    window.chatUI = new ChatUI();
});

// Also init if DOM already loaded
if (document.readyState !== 'loading') {
    window.chatUI = new ChatUI();
}
