/**
 * NAJIKA SYSTEM MONITOR - Real-time Status Dashboard
 * Zeigt Najika Status, Server Status, Training Progress etc.
 */

const SystemMonitor = {
    isOpen: false,
    overlay: null,
    updateInterval: null,

    open() {
        if (this.isOpen) return;
        this.isOpen = true;

        this.overlay = document.createElement('div');
        this.overlay.id = 'systemMonitorOverlay';
        this.overlay.innerHTML = `
            <div class="system-monitor-container">
                <!-- Header -->
                <div class="system-monitor-header">
                    <div class="header-left">
                        <span class="terminal-icon">⬢</span>
                        <span class="title">SYSTEM MONITOR</span>
                        <span class="status-indicator">●</span>
                    </div>
                    <div class="header-actions">
                        <button class="header-btn" onclick="SystemMonitor.refresh()" title="Aktualisieren">🔄</button>
                        <button class="header-btn" onclick="SystemMonitor.toggleAutoRefresh()" title="Auto-Refresh" id="autoRefreshBtn">⏸️</button>
                    </div>
                    <button class="close-btn" onclick="SystemMonitor.close()">✕</button>
                </div>

                <!-- Main Grid -->
                <div class="system-monitor-main">
                    <!-- Left Column: Najika Status -->
                    <div class="monitor-panel">
                        <div class="panel-header">
                            <span>🐊 NAJIKA STATUS</span>
                        </div>
                        <div class="panel-content" id="najikaStatusPanel">
                            <div class="loading-spinner">⟳ Lädt...</div>
                        </div>
                    </div>

                    <!-- Right Column: Server Status -->
                    <div class="monitor-panel">
                        <div class="panel-header">
                            <span>🖥️ SERVER STATUS</span>
                        </div>
                        <div class="panel-content" id="serverStatusPanel">
                            <div class="loading-spinner">⟳ Lädt...</div>
                        </div>
                    </div>

                    <!-- Bottom Left: Training Status -->
                    <div class="monitor-panel">
                        <div class="panel-header">
                            <span>📚 TRAINING STATUS</span>
                        </div>
                        <div class="panel-content" id="trainingStatusPanel">
                            <div class="loading-spinner">⟳ Lädt...</div>
                        </div>
                    </div>

                    <!-- Bottom Right: Memory & Security -->
                    <div class="monitor-panel">
                        <div class="panel-header">
                            <span>🔒 MEMORY & SECURITY</span>
                        </div>
                        <div class="panel-content" id="securityStatusPanel">
                            <div class="loading-spinner">⟳ Lädt...</div>
                        </div>
                    </div>
                </div>

                <!-- Footer -->
                <div class="system-monitor-footer">
                    <div class="footer-info">
                        <span id="lastUpdateTime">Letztes Update: --:--:--</span>
                        <span id="autoRefreshStatus">Auto-Refresh: AN (5s)</span>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(this.overlay);

        // Load initial data
        this.loadAllData();

        // Start auto-refresh
        this.startAutoRefresh();
    },

    close() {
        if (!this.isOpen) return;
        this.isOpen = false;

        this.stopAutoRefresh();

        if (this.overlay) {
            this.overlay.remove();
            this.overlay = null;
        }
    },

    async loadAllData() {
        await Promise.all([
            this.loadNajikaStatus(),
            this.loadServerStatus(),
            this.loadTrainingStatus(),
            this.loadSecurityStatus()
        ]);

        this.updateLastUpdateTime();
    },

    async loadNajikaStatus() {
        const panel = document.getElementById('najikaStatusPanel');
        if (!panel) return;

        try {
            const response = await fetch('http://localhost:8001/api/state/najika');
            const data = await response.json();

            if (data.najika) {
                const n = data.najika;
                panel.innerHTML = `
                    <div class="stat-row">
                        <span class="stat-label">NAME:</span>
                        <span class="stat-value">${n.name || 'Najika'}</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">LEVEL:</span>
                        <span class="stat-value">${n.level || 1}</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">XP:</span>
                        <span class="stat-value">${n.xp || 0} / ${n.xp_next || 100}</span>
                    </div>
                    <div class="stat-separator"></div>
                    <div class="stat-row">
                        <span class="stat-label">HUNGER:</span>
                        <span class="stat-bar">${this.renderBar(n.hunger || 0)}</span>
                        <span class="stat-value">${Math.round(n.hunger || 0)}%</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">THIRST:</span>
                        <span class="stat-bar">${this.renderBar(n.thirst || 0)}</span>
                        <span class="stat-value">${Math.round(n.thirst || 0)}%</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">ENERGY:</span>
                        <span class="stat-bar">${this.renderBar(n.energy || 0)}</span>
                        <span class="stat-value">${Math.round(n.energy || 0)}%</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">HYGIENE:</span>
                        <span class="stat-bar">${this.renderBar(n.hygiene || 0)}</span>
                        <span class="stat-value">${Math.round(n.hygiene || 0)}%</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">HAPPINESS:</span>
                        <span class="stat-bar">${this.renderBar(n.happiness || 0)}</span>
                        <span class="stat-value">${Math.round(n.happiness || 0)}%</span>
                    </div>
                    <div class="stat-separator"></div>
                    <div class="stat-row">
                        <span class="stat-label">DISCIPLINE:</span>
                        <span class="stat-value">${Math.round(n.discipline || 0)}%</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">MOOD:</span>
                        <span class="stat-value">${n.mood || 'Normal'}</span>
                    </div>
                `;
            } else {
                panel.innerHTML = '<div class="error-text">❌ Keine Daten</div>';
            }
        } catch (error) {
            panel.innerHTML = `<div class="error-text">❌ ${error.message}</div>`;
        }
    },

    async loadServerStatus() {
        const panel = document.getElementById('serverStatusPanel');
        if (!panel) return;

        try {
            const response = await fetch('http://localhost:8001/api/status');
            const data = await response.json();

            panel.innerHTML = `
                <div class="stat-row">
                    <span class="stat-label">OLLAMA:</span>
                    <span class="stat-value status-${data.ollama_online ? 'online' : 'offline'}">
                        ${data.ollama_online ? '✓ ONLINE' : '✗ OFFLINE'}
                    </span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">MODEL:</span>
                    <span class="stat-value">${data.ollama_model || 'N/A'}</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">CLOUD MODE:</span>
                    <span class="stat-value status-${data.cloud_mode ? 'online' : 'offline'}">
                        ${data.cloud_mode ? '✓ ENABLED' : '✗ DISABLED'}
                    </span>
                </div>
                <div class="stat-separator"></div>
                <div class="stat-row">
                    <span class="stat-label">UPTIME:</span>
                    <span class="stat-value">${this.formatUptime(data.uptime || 0)}</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">VERSION:</span>
                    <span class="stat-value">${data.version || 'v1.0'}</span>
                </div>
            `;
        } catch (error) {
            panel.innerHTML = `<div class="error-text">❌ ${error.message}</div>`;
        }
    },

    async loadTrainingStatus() {
        const panel = document.getElementById('trainingStatusPanel');
        if (!panel) return;

        try {
            const response = await fetch('http://localhost:8001/api/training/status');
            const data = await response.json();

            const training = data.training || {};
            panel.innerHTML = `
                <div class="stat-row">
                    <span class="stat-label">STATUS:</span>
                    <span class="stat-value status-${training.active ? 'online' : 'offline'}">
                        ${training.active ? '⟳ LÄUFT' : '⏸ PAUSIERT'}
                    </span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">MODE:</span>
                    <span class="stat-value">${training.mode || 'N/A'}</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">PROGRESS:</span>
                    <span class="stat-value">${training.progress || 0}%</span>
                </div>
                <div class="stat-separator"></div>
                <div class="stat-row">
                    <span class="stat-label">GESAMT:</span>
                    <span class="stat-value">${training.total_sessions || 0} Sessions</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">ERFOLGE:</span>
                    <span class="stat-value">${training.successful || 0}</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">FEHLER:</span>
                    <span class="stat-value">${training.failed || 0}</span>
                </div>
            `;
        } catch (error) {
            panel.innerHTML = `<div class="error-text">❌ ${error.message}</div>`;
        }
    },

    async loadSecurityStatus() {
        const panel = document.getElementById('securityStatusPanel');
        if (!panel) return;

        try {
            const [securityResp, memoryResp] = await Promise.all([
                fetch('http://localhost:8001/api/security/status'),
                fetch('http://localhost:8001/api/memory/export')
            ]);

            const security = await securityResp.json();
            const memory = await memoryResp.json();

            panel.innerHTML = `
                <div class="stat-row">
                    <span class="stat-label">SECURITY:</span>
                    <span class="stat-value status-online">
                        ${security.alcatraz_active ? '✓ ALCATRAZ ACTIVE' : '✗ DISABLED'}
                    </span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">VPN:</span>
                    <span class="stat-value status-${security.vpn_active ? 'online' : 'offline'}">
                        ${security.vpn_active ? '✓ CONNECTED' : '✗ DISCONNECTED'}
                    </span>
                </div>
                <div class="stat-separator"></div>
                <div class="stat-row">
                    <span class="stat-label">MEMORY:</span>
                    <span class="stat-value">${memory.total_memories || 0} Einträge</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">GRÖSSE:</span>
                    <span class="stat-value">${this.formatBytes(memory.size_bytes || 0)}</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">LETZTER CHAT:</span>
                    <span class="stat-value">${this.formatTime(memory.last_chat || 0)}</span>
                </div>
            `;
        } catch (error) {
            panel.innerHTML = `<div class="error-text">❌ ${error.message}</div>`;
        }
    },

    renderBar(value) {
        const percent = Math.min(100, Math.max(0, value));
        const filled = Math.round(percent / 10);
        const empty = 10 - filled;

        let color = 'bar-green';
        if (percent < 30) color = 'bar-red';
        else if (percent < 60) color = 'bar-yellow';

        return `<span class="${color}">${'█'.repeat(filled)}${'░'.repeat(empty)}</span>`;
    },

    formatUptime(seconds) {
        const hours = Math.floor(seconds / 3600);
        const mins = Math.floor((seconds % 3600) / 60);
        return `${hours}h ${mins}m`;
    },

    formatBytes(bytes) {
        if (bytes === 0) return '0 B';
        const k = 1024;
        const sizes = ['B', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
    },

    formatTime(timestamp) {
        if (!timestamp) return 'N/A';
        const date = new Date(timestamp * 1000);
        return date.toLocaleTimeString('de-DE');
    },

    updateLastUpdateTime() {
        const display = document.getElementById('lastUpdateTime');
        if (display) {
            const now = new Date();
            display.textContent = `Letztes Update: ${now.toLocaleTimeString('de-DE')}`;
        }
    },

    refresh() {
        notify('🔄 Aktualisiere...', 'info');
        this.loadAllData();
    },

    startAutoRefresh() {
        this.stopAutoRefresh();
        this.updateInterval = setInterval(() => {
            this.loadAllData();
        }, 5000); // Alle 5 Sekunden

        const statusDisplay = document.getElementById('autoRefreshStatus');
        if (statusDisplay) {
            statusDisplay.textContent = 'Auto-Refresh: AN (5s)';
        }

        const btn = document.getElementById('autoRefreshBtn');
        if (btn) {
            btn.textContent = '⏸️';
            btn.title = 'Auto-Refresh Pausieren';
        }
    },

    stopAutoRefresh() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
            this.updateInterval = null;
        }

        const statusDisplay = document.getElementById('autoRefreshStatus');
        if (statusDisplay) {
            statusDisplay.textContent = 'Auto-Refresh: AUS';
        }

        const btn = document.getElementById('autoRefreshBtn');
        if (btn) {
            btn.textContent = '▶️';
            btn.title = 'Auto-Refresh Starten';
        }
    },

    toggleAutoRefresh() {
        if (this.updateInterval) {
            this.stopAutoRefresh();
            notify('Auto-Refresh pausiert', 'info');
        } else {
            this.startAutoRefresh();
            notify('Auto-Refresh gestartet', 'success');
        }
    }
};

// Global verfügbar machen
window.SystemMonitor = SystemMonitor;
