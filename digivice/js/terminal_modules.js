/**
 * NAJIKA TERMINAL MODULE SYSTEM
 * Framework für wechselbare Module im Terminal-Raum
 * Module: Code-Editor, Messenger, System-Monitor, File-Manager
 */

const TerminalModules = {
    currentModule: null,
    modules: {
        'code-editor': {
            name: 'Code-Editor',
            icon: '💻',
            color: '#0f0',
            init: () => {
                if (window.CodeEditor && typeof window.CodeEditor.open === 'function') {
                    CodeEditor.open();
                }
            },
            close: () => {
                if (window.CodeEditor && typeof window.CodeEditor.close === 'function') {
                    CodeEditor.close();
                }
            }
        },
        'messenger': {
            name: 'Secure Messenger',
            icon: '💬',
            color: '#0f0',
            init: () => {
                if (window.SecureMessenger && typeof window.SecureMessenger.open === 'function') {
                    SecureMessenger.open();
                }
            },
            close: () => {
                if (window.SecureMessenger && typeof window.SecureMessenger.close === 'function') {
                    SecureMessenger.close();
                }
            }
        },
        'system-monitor': {
            name: 'System Monitor',
            icon: '📊',
            color: '#0f0',
            init: () => {
                if (window.SystemMonitor && typeof window.SystemMonitor.open === 'function') {
                    SystemMonitor.open();
                }
            },
            close: () => {
                if (window.SystemMonitor && typeof window.SystemMonitor.close === 'function') {
                    SystemMonitor.close();
                }
            }
        },
        'file-manager': {
            name: 'File Manager',
            icon: '📁',
            color: '#0f0',
            init: () => {
                if (window.FileManager && typeof window.FileManager.open === 'function') {
                    FileManager.open();
                }
            },
            close: () => {
                if (window.FileManager && typeof window.FileManager.close === 'function') {
                    FileManager.close();
                }
            }
        }
    },

    // Modul-Switcher UI
    switcherOverlay: null,

    openSwitcher() {
        if (this.switcherOverlay) return;

        this.switcherOverlay = document.createElement('div');
        this.switcherOverlay.id = 'terminalModuleSwitcher';
        this.switcherOverlay.innerHTML = `
            <div class="module-switcher-container">
                <div class="switcher-header">
                    <span class="terminal-icon">⬢</span> TERMINAL MODULE
                    <button class="close-btn" onclick="TerminalModules.closeSwitcher()">✕</button>
                </div>
                <div class="module-grid">
                    ${this.generateModuleButtons()}
                </div>
                <div class="switcher-footer">
                    <span class="hint">← Swipe → oder Tasten 1-4</span>
                </div>
            </div>
        `;

        document.body.appendChild(this.switcherOverlay);

        // Touch-Swipe Events
        this.setupSwipeGestures();

        // Keyboard Shortcuts (1-4)
        this.setupModuleShortcuts();
    },

    generateModuleButtons() {
        let html = '';
        let index = 1;
        for (const [key, module] of Object.entries(this.modules)) {
            const active = this.currentModule === key ? 'active' : '';
            html += `
                <button class="module-button ${active}" onclick="TerminalModules.switchToModule('${key}')">
                    <div class="module-icon" style="color: ${module.color}">${module.icon}</div>
                    <div class="module-name">${module.name}</div>
                    <div class="module-key">[${index}]</div>
                </button>
            `;
            index++;
        }
        return html;
    },

    closeSwitcher() {
        if (this.switcherOverlay) {
            this.switcherOverlay.remove();
            this.switcherOverlay = null;
        }
        this.removeSwipeListeners();
        this.removeKeyboardListeners();
    },

    switchToModule(moduleKey) {
        // Schließe aktuelles Modul
        if (this.currentModule && this.modules[this.currentModule]) {
            this.modules[this.currentModule].close();
        }

        // Öffne neues Modul
        if (this.modules[moduleKey]) {
            this.currentModule = moduleKey;
            this.modules[moduleKey].init();
            this.closeSwitcher();
            notify(`🟢 ${this.modules[moduleKey].name} aktiviert`, 'success');
        }
    },

    // Swipe-Gestures (Touch)
    setupSwipeGestures() {
        const container = document.querySelector('.module-switcher-container');
        if (!container) return;

        let touchStartX = 0;
        let touchEndX = 0;

        container.addEventListener('touchstart', (e) => {
            touchStartX = e.changedTouches[0].screenX;
        }, { passive: true });

        container.addEventListener('touchend', (e) => {
            touchEndX = e.changedTouches[0].screenX;
            this.handleSwipe(touchStartX, touchEndX);
        }, { passive: true });

        // Mouse-Swipe (für Desktop-Test)
        let mouseDown = false;
        let mouseStartX = 0;

        container.addEventListener('mousedown', (e) => {
            mouseDown = true;
            mouseStartX = e.clientX;
        });

        container.addEventListener('mouseup', (e) => {
            if (mouseDown) {
                mouseDown = false;
                this.handleSwipe(mouseStartX, e.clientX);
            }
        });

        this.swipeContainer = container;
    },

    handleSwipe(startX, endX) {
        const diff = startX - endX;
        const threshold = 50; // Mindest-Swipe-Distanz

        if (Math.abs(diff) < threshold) return;

        const moduleKeys = Object.keys(this.modules);
        const currentIndex = moduleKeys.indexOf(this.currentModule);

        if (diff > 0) {
            // Swipe Left → Nächstes Modul
            const nextIndex = (currentIndex + 1) % moduleKeys.length;
            this.switchToModule(moduleKeys[nextIndex]);
        } else {
            // Swipe Right → Vorheriges Modul
            const prevIndex = (currentIndex - 1 + moduleKeys.length) % moduleKeys.length;
            this.switchToModule(moduleKeys[prevIndex]);
        }
    },

    removeSwipeListeners() {
        // Cleanup wird durch remove() automatisch gemacht
    },

    // Keyboard Shortcuts (1-4 für Module)
    setupModuleShortcuts() {
        this.keydownHandler = (e) => {
            const moduleKeys = Object.keys(this.modules);
            const keyNum = parseInt(e.key);

            if (keyNum >= 1 && keyNum <= moduleKeys.length) {
                e.preventDefault();
                this.switchToModule(moduleKeys[keyNum - 1]);
            }

            // ESC: Switcher schließen
            if (e.key === 'Escape') {
                this.closeSwitcher();
            }
        };

        document.addEventListener('keydown', this.keydownHandler);
    },

    removeKeyboardListeners() {
        if (this.keydownHandler) {
            document.removeEventListener('keydown', this.keydownHandler);
            this.keydownHandler = null;
        }
    },

    // Placeholder für noch nicht implementierte Module
    showPlaceholder(moduleName, description) {
        const placeholder = document.createElement('div');
        placeholder.id = 'modulePlaceholder';
        placeholder.innerHTML = `
            <div class="placeholder-container">
                <div class="placeholder-content">
                    <div class="placeholder-title">${moduleName}</div>
                    <div class="placeholder-desc">${description}</div>
                    <div class="placeholder-status">🚧 IN ENTWICKLUNG 🚧</div>
                    <button class="placeholder-btn" onclick="TerminalModules.openSwitcher()">
                        Anderes Modul wählen
                    </button>
                </div>
            </div>
        `;
        document.body.appendChild(placeholder);
    },

    closePlaceholder() {
        const placeholder = document.getElementById('modulePlaceholder');
        if (placeholder) {
            placeholder.remove();
        }
    }
};

// Global verfügbar machen
window.TerminalModules = TerminalModules;
