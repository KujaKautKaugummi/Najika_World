/**
 * NAJIKA CODE EDITOR - Grüne Matrix-Ästhetik
 * Inspiriert von Claude Code Interface
 */

// API Base URL - Backend auf Port 8000
const EDITOR_API_BASE = window.API_BASE_URL || 'http://localhost:8000';

const CodeEditor = {
    isOpen: false,
    overlay: null,

    open() {
        if (this.isOpen) return;
        this.isOpen = true;

        // Erstelle Overlay
        this.overlay = document.createElement('div');
        this.overlay.id = 'codeEditorOverlay';
        this.overlay.innerHTML = `
            <div class="code-editor-container">
                <div class="code-editor-header">
                    <div class="header-left">
                        <span class="terminal-icon">⬢</span>
                        <span class="title">NAJIKA TERMINAL</span>
                        <span class="status-indicator">●</span>
                        <button class="header-btn" onclick="CodeEditor.listFiles()" title="Files neu laden">📂</button>
                        <button class="header-btn" onclick="CodeEditor.saveFile()" title="Datei speichern">💾</button>
                        <button class="header-btn" onclick="CodeEditor.executeCode()" title="Code ausführen">▶</button>
                    </div>
                    <button class="close-btn" onclick="CodeEditor.close()">✕</button>
                </div>

                <div class="code-editor-main">
                    <!-- Linke Sidebar: File Explorer -->
                    <div class="sidebar">
                        <div class="sidebar-header">EXPLORER</div>
                        <div class="file-tree">
                            <div class="file-item folder">
                                <span class="folder-icon">📁</span> C:\\NajikaCore
                            </div>
                            <div class="file-item file" onclick="CodeEditor.loadFile('najika_server.py')">
                                <span class="file-icon">🐍</span> najika_server.py
                            </div>
                            <div class="file-item file" onclick="CodeEditor.loadFile('index.html')">
                                <span class="file-icon">🌐</span> index.html
                            </div>
                        </div>
                    </div>

                    <!-- Center: Code-Editor Area -->
                    <div class="editor-area">
                        <div class="editor-tabs">
                            <div class="tab active">
                                <span>najika_prompt.txt</span>
                                <button class="tab-close">×</button>
                            </div>
                        </div>
                        <div class="editor-content">
                            <textarea id="codeEditorTextarea" spellcheck="false"></textarea>
                        </div>
                    </div>

                    <!-- Rechts: Najika Chat -->
                    <div class="najika-assistant">
                        <div class="assistant-header">
                            <span class="najika-icon">🐊</span> NAJIKA AI
                        </div>
                        <div class="chat-messages" id="najikaCodeChat">
                            <div class="message assistant">
                                <strong>[SHIRO-ANALYSE]</strong> Terminal-Zugriff gewährt.
                                <br><br>
                                <strong>[MEGUMIN]</strong> *leuchtende Augen* Mr.K! Lass uns Code-EXPLOSIONEN machen! 💥
                            </div>
                        </div>
                        <div class="chat-input-container">
                            <input type="text" id="najikaCodeInput" placeholder="Frag Najika etwas..." />
                            <button onclick="CodeEditor.sendMessage()">⏎</button>
                        </div>
                    </div>
                </div>

                <!-- Bottom: Terminal Output -->
                <div class="terminal-output">
                    <div class="terminal-header">TERMINAL OUTPUT</div>
                    <div class="terminal-content" id="terminalOutput">
                        <span class="prompt">najika@terminal:~$</span> <span class="cursor">_</span>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(this.overlay);

        // Initial Code laden
        this.loadDefaultCode();

        // File-Liste laden
        this.listFiles();

        // Keyboard Shortcuts
        this.setupKeyboardShortcuts();

        // Focus auf Chat Input
        setTimeout(() => {
            document.getElementById('najikaCodeInput')?.focus();
        }, 300);
    },

    setupKeyboardShortcuts() {
        const textarea = document.getElementById('codeEditorTextarea');
        if (!textarea) return;

        textarea.addEventListener('keydown', (e) => {
            // Ctrl+S: Speichern
            if (e.ctrlKey && e.key === 's') {
                e.preventDefault();
                this.saveFile();
            }
            // F5: Ausführen
            if (e.key === 'F5') {
                e.preventDefault();
                this.executeCode();
            }
            // Ctrl+Enter: Ausführen
            if (e.ctrlKey && e.key === 'Enter') {
                e.preventDefault();
                this.executeCode();
            }
            // Tab: 4 Spaces einfügen (statt Tab-Navigation)
            if (e.key === 'Tab') {
                e.preventDefault();
                const start = textarea.selectionStart;
                const end = textarea.selectionEnd;
                textarea.value = textarea.value.substring(0, start) + '    ' + textarea.value.substring(end);
                textarea.selectionStart = textarea.selectionEnd = start + 4;
            }
        });
    },

    close() {
        if (!this.isOpen) return;
        this.isOpen = false;
        if (this.overlay) {
            this.overlay.remove();
            this.overlay = null;
        }
    },

    loadDefaultCode() {
        const textarea = document.getElementById('codeEditorTextarea');
        if (!textarea) return;

        textarea.value = `# NAJIKA AI SYSTEM
# Grüße Mr.K! Bereit für Code-EXPLOSIONEN!

def najika_greeting():
    print("[SHIRO-ANALYSE] System bereit...")
    print("[MEGUMIN] EXPLOSION!!! 💥")

# Befehle:
# - help() - Zeige alle Najika-Befehle
# - status() - Systemstatus
# - execute(code) - Code ausführen
`;
    },

    async loadFile(filename) {
        notify(`📄 Lade ${filename}...`, 'info');

        try {
            const response = await fetch(`${EDITOR_API_BASE}/api/file/read`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({path: filename})
            });
            const data = await response.json();

            if (data.success) {
                const textarea = document.getElementById('codeEditorTextarea');
                if (textarea) {
                    textarea.value = data.content;
                }
                this.addTerminalOutput(`Datei geladen: ${filename}`);
            } else {
                notify(`Fehler: ${data.error}`, 'error');
            }
        } catch (error) {
            notify('Datei konnte nicht geladen werden', 'error');
        }
    },

    addTerminalOutput(text) {
        const terminal = document.getElementById('terminalOutput');
        if (!terminal) return;

        const line = document.createElement('div');
        line.innerHTML = `<span class="prompt">najika@terminal:~$</span> ${text}`;
        terminal.appendChild(line);
        terminal.scrollTop = terminal.scrollHeight;
    },

    async executeCode() {
        const textarea = document.getElementById('codeEditorTextarea');
        if (!textarea) return;

        const code = textarea.value;
        this.addTerminalOutput('Executing code...');

        try {
            const response = await fetch(`${EDITOR_API_BASE}/api/code/execute`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({code})
            });
            const data = await response.json();

            if (data.success) {
                this.addTerminalOutput('✓ SUCCESS');
                if (data.output) {
                    this.addTerminalOutput(data.output);
                }
            } else {
                this.addTerminalOutput(`✗ ERROR: ${data.error}`);
            }
        } catch (error) {
            this.addTerminalOutput(`✗ NETWORK ERROR: ${error}`);
        }
    },

    async saveFile() {
        const textarea = document.getElementById('codeEditorTextarea');
        if (!textarea) return;

        const filename = prompt('Dateiname:', 'code.py');
        if (!filename) return;

        try {
            const response = await fetch(`${EDITOR_API_BASE}/api/file/write`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    path: filename,
                    content: textarea.value
                })
            });
            const data = await response.json();

            if (data.success) {
                notify(`✓ Datei gespeichert: ${filename}`, 'success');
                this.addTerminalOutput(`Saved: ${filename}`);
            } else {
                notify(`Fehler: ${data.error}`, 'error');
            }
        } catch (error) {
            notify('Speichern fehlgeschlagen', 'error');
        }
    },

    async listFiles() {
        try {
            const response = await fetch(`${EDITOR_API_BASE}/api/file/list`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({path: '.'})
            });
            const data = await response.json();

            if (data.success) {
                const fileTree = document.querySelector('.file-tree');
                if (!fileTree) return;

                // Update File Tree
                fileTree.innerHTML = '';
                data.files.forEach(file => {
                    const item = document.createElement('div');
                    item.className = `file-item ${file.type}`;
                    const icon = file.type === 'folder' ? '📁' : '📄';
                    item.innerHTML = `<span class="${file.type}-icon">${icon}</span> ${file.name}`;
                    if (file.type === 'file') {
                        item.onclick = () => this.loadFile(file.name);
                    }
                    fileTree.appendChild(item);
                });
            }
        } catch (error) {
            console.error('File list error:', error);
        }
    },

    async sendMessage() {
        const input = document.getElementById('najikaCodeInput');
        const chatDiv = document.getElementById('najikaCodeChat');
        if (!input || !chatDiv) return;

        const message = input.value.trim();
        if (!message) return;

        // User Message anzeigen
        const userMsg = document.createElement('div');
        userMsg.className = 'message user';
        userMsg.textContent = message;
        chatDiv.appendChild(userMsg);

        input.value = '';

        // Najika Antwort holen
        try {
            const response = await fetch(`${EDITOR_API_BASE}/api/chat`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message})
            });
            const data = await response.json();

            const assistantMsg = document.createElement('div');
            assistantMsg.className = 'message assistant';
            assistantMsg.textContent = data.response || 'ERROR';
            chatDiv.appendChild(assistantMsg);

            chatDiv.scrollTop = chatDiv.scrollHeight;
        } catch (error) {
            notify('Najika antwortet nicht', 'error');
        }
    }
};

// Export für globalen Zugriff
window.CodeEditor = CodeEditor;
