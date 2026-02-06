/**
 * World Map UI - Najika World
 * ============================
 *
 * Interaktive Weltkarte mit allen 9 Regionen
 * Fast Travel, Region Info, Quest Marker
 *
 * Copyright: Najika World
 * Author: Claude Code (CLI)
 * Date: 2026-01-24
 */

class WorldMapUI {
    constructor() {
        this.apiBase = '/api/world';
        this.isOpen = false;
        this.selectedRegion = null;
        this.playerPosition = { x: 0, z: 0 };
        this.unlockedTravelPoints = ['schwarze_muehle'];

        // Die 9 Regionen von Najika World (3x3 Grid, 9.6km x 9.6km)
        this.regions = [
            { id: 'samtmoos_tiefwald', name: 'Samtmoos-Tiefwald', x: 0, y: 0, color: '#228B22', icon: '🌲', desc: 'Dichter Wald mit mystischen Pilzen' },
            { id: 'kristallhoehen', name: 'Kristallhöhen', x: 1, y: 0, color: '#87CEEB', icon: '💎', desc: 'Schwebende Kristallinseln' },
            { id: 'funkensiedlung', name: 'Funkensiedlung', x: 2, y: 0, color: '#FF6347', icon: '🔥', desc: 'Stadt der Schmiede und Feuer' },
            { id: 'nebelmarsch', name: 'Nebelmarsch', x: 0, y: 1, color: '#708090', icon: '🌫️', desc: 'Mysteriöse Sümpfe im Nebel' },
            { id: 'reichderdrei', name: 'Reich der Drei', x: 1, y: 1, color: '#FFD700', icon: '👑', desc: 'Zentrale Hauptstadt - Schwarze Mühle' },
            { id: 'aschental', name: 'Aschental', x: 2, y: 1, color: '#2F4F4F', icon: '🌋', desc: 'Vulkanische Ödnis' },
            { id: 'salzige_bucht', name: 'Salzige Bucht', x: 0, y: 2, color: '#4169E1', icon: '⚓', desc: 'Hafenstadt und Fischereidorf' },
            { id: 'dampfhain', name: 'Dampfhain', x: 1, y: 2, color: '#8B4513', icon: '⚙️', desc: 'Steampunk-Technologie' },
            { id: 'runenheim', name: 'Runenheim', x: 2, y: 2, color: '#9932CC', icon: '🔮', desc: 'Magierakademie und Ruinen' }
        ];

        this.init();
    }

    init() {
        this.createUI();
        this.attachEventListeners();
        console.log('✅ World Map UI geladen');
    }

    createUI() {
        const container = document.createElement('div');
        container.id = 'world-map-container';
        container.className = 'world-map-container hidden';
        container.innerHTML = `
            <div class="world-map-panel">
                <div class="wm-header">
                    <h2>🗺️ Weltkarte - Najika World</h2>
                    <div class="wm-coords" id="wm-coords">Position: 0, 0</div>
                    <button class="wm-close-btn" id="wm-close-btn">✖</button>
                </div>

                <div class="wm-content">
                    <!-- Karte -->
                    <div class="wm-map-area">
                        <div class="wm-map-grid" id="wm-map-grid">
                            ${this.regions.map(r => `
                                <div class="wm-region"
                                     data-region="${r.id}"
                                     style="background: ${r.color}; grid-column: ${r.x + 1}; grid-row: ${r.y + 1};"
                                     onclick="window.worldMapUI.selectRegion('${r.id}')">
                                    <span class="region-icon">${r.icon}</span>
                                    <span class="region-name">${r.name}</span>
                                </div>
                            `).join('')}
                            <div class="wm-player-marker" id="wm-player-marker">📍</div>
                        </div>
                    </div>

                    <!-- Info Panel -->
                    <div class="wm-info-panel" id="wm-info-panel">
                        <h3>Region auswählen</h3>
                        <p>Klicke auf eine Region für Details</p>
                    </div>
                </div>

                <div class="wm-footer">
                    <button class="wm-btn" id="wm-travel-btn" disabled>
                        🚀 Schnellreise
                    </button>
                    <button class="wm-btn secondary" onclick="window.worldMapUI.close()">
                        Schließen
                    </button>
                </div>
            </div>
        `;

        // Styles
        const styles = document.createElement('style');
        styles.textContent = `
            .world-map-container {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.9);
                z-index: 10000;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .world-map-container.hidden {
                display: none;
            }
            .world-map-panel {
                background: linear-gradient(135deg, #1a1a2e 0%, #0f0f1a 100%);
                border: 2px solid #667eea;
                border-radius: 15px;
                width: 95%;
                max-width: 1000px;
                max-height: 90vh;
                overflow: hidden;
                box-shadow: 0 10px 50px rgba(102,126,234,0.4);
            }
            .wm-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 15px 20px;
                background: linear-gradient(90deg, #667eea, #764ba2);
            }
            .wm-header h2 {
                margin: 0;
                color: white;
            }
            .wm-coords {
                background: rgba(0,0,0,0.3);
                padding: 5px 15px;
                border-radius: 15px;
                color: #aaa;
                font-size: 12px;
            }
            .wm-close-btn {
                background: rgba(255,255,255,0.2);
                border: none;
                color: white;
                font-size: 20px;
                width: 35px;
                height: 35px;
                border-radius: 50%;
                cursor: pointer;
            }
            .wm-content {
                display: grid;
                grid-template-columns: 2fr 1fr;
                gap: 20px;
                padding: 20px;
            }
            .wm-map-area {
                background: rgba(0,0,0,0.5);
                border-radius: 10px;
                padding: 20px;
                position: relative;
            }
            .wm-map-grid {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                grid-template-rows: repeat(3, 1fr);
                gap: 5px;
                aspect-ratio: 1;
                position: relative;
            }
            .wm-region {
                border-radius: 8px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                transition: all 0.3s;
                opacity: 0.8;
                border: 2px solid transparent;
            }
            .wm-region:hover {
                opacity: 1;
                transform: scale(1.02);
                z-index: 1;
            }
            .wm-region.selected {
                border-color: #FFD700;
                box-shadow: 0 0 20px rgba(255,215,0,0.5);
                opacity: 1;
            }
            .region-icon {
                font-size: 30px;
                margin-bottom: 5px;
            }
            .region-name {
                font-size: 11px;
                color: white;
                text-shadow: 1px 1px 2px black;
                text-align: center;
            }
            .wm-player-marker {
                position: absolute;
                font-size: 24px;
                transform: translate(-50%, -50%);
                filter: drop-shadow(0 0 5px gold);
                animation: pulse 2s infinite;
                pointer-events: none;
            }
            @keyframes pulse {
                0%, 100% { transform: translate(-50%, -50%) scale(1); }
                50% { transform: translate(-50%, -50%) scale(1.2); }
            }
            .wm-info-panel {
                background: rgba(0,0,0,0.5);
                border-radius: 10px;
                padding: 20px;
            }
            .wm-info-panel h3 {
                margin: 0 0 10px 0;
                color: #667eea;
            }
            .wm-info-panel p {
                color: #aaa;
                margin: 5px 0;
            }
            .wm-info-panel .region-detail {
                margin-top: 15px;
                padding-top: 15px;
                border-top: 1px solid rgba(255,255,255,0.1);
            }
            .wm-info-panel .detail-row {
                display: flex;
                justify-content: space-between;
                padding: 5px 0;
                color: #ccc;
            }
            .wm-footer {
                display: flex;
                gap: 10px;
                padding: 15px 20px;
                background: rgba(0,0,0,0.3);
                justify-content: center;
            }
            .wm-btn {
                padding: 12px 30px;
                background: linear-gradient(135deg, #667eea, #764ba2);
                border: none;
                color: white;
                border-radius: 8px;
                cursor: pointer;
                font-size: 14px;
                transition: all 0.2s;
            }
            .wm-btn:hover:not(:disabled) {
                transform: scale(1.05);
            }
            .wm-btn:disabled {
                opacity: 0.5;
                cursor: not-allowed;
            }
            .wm-btn.secondary {
                background: linear-gradient(135deg, #555, #333);
            }
            .travel-point {
                position: absolute;
                width: 12px;
                height: 12px;
                background: #FFD700;
                border-radius: 50%;
                border: 2px solid white;
            }
            .travel-point.locked {
                background: #555;
                border-color: #333;
            }
        `;

        document.head.appendChild(styles);
        document.body.appendChild(container);

        this.updatePlayerMarker();
    }

    attachEventListeners() {
        // M-Taste zum Öffnen
        document.addEventListener('keydown', (e) => {
            if (e.key === 'm' || e.key === 'M') {
                if (!e.target.matches('input, textarea')) {
                    this.toggle();
                }
            }
            if (e.key === 'Escape' && this.isOpen) {
                this.close();
            }
        });

        // Close Button
        document.getElementById('wm-close-btn')?.addEventListener('click', () => this.close());

        // Travel Button
        document.getElementById('wm-travel-btn')?.addEventListener('click', () => this.travelToSelected());
    }

    selectRegion(regionId) {
        this.selectedRegion = this.regions.find(r => r.id === regionId);

        // UI Update
        document.querySelectorAll('.wm-region').forEach(el => {
            el.classList.remove('selected');
            if (el.dataset.region === regionId) {
                el.classList.add('selected');
            }
        });

        // Info Panel Update
        const panel = document.getElementById('wm-info-panel');
        if (panel && this.selectedRegion) {
            const r = this.selectedRegion;
            const canTravel = this.unlockedTravelPoints.includes(r.id) || r.id === 'reichderdrei';

            panel.innerHTML = `
                <h3>${r.icon} ${r.name}</h3>
                <p>${r.desc}</p>
                <div class="region-detail">
                    <div class="detail-row">
                        <span>Koordinaten:</span>
                        <span>${r.x * 3200}, ${r.y * 3200}</span>
                    </div>
                    <div class="detail-row">
                        <span>Schnellreise:</span>
                        <span>${canTravel ? '✅ Verfügbar' : '🔒 Gesperrt'}</span>
                    </div>
                    <div class="detail-row">
                        <span>Entdeckt:</span>
                        <span>${canTravel ? '100%' : '???'}</span>
                    </div>
                </div>
            `;

            // Travel Button aktivieren
            const travelBtn = document.getElementById('wm-travel-btn');
            if (travelBtn) {
                travelBtn.disabled = !canTravel;
            }
        }
    }

    updatePlayerMarker() {
        const marker = document.getElementById('wm-player-marker');
        const grid = document.getElementById('wm-map-grid');
        if (!marker || !grid) return;

        // Konvertiere Weltposition zu Grid-Position
        const gridX = (this.playerPosition.x + 4800) / 9600 * 100;
        const gridY = (this.playerPosition.z + 4800) / 9600 * 100;

        marker.style.left = `${gridX}%`;
        marker.style.top = `${gridY}%`;

        // Coords Update
        const coords = document.getElementById('wm-coords');
        if (coords) {
            coords.textContent = `Position: ${Math.round(this.playerPosition.x)}, ${Math.round(this.playerPosition.z)}`;
        }
    }

    setPlayerPosition(x, z) {
        this.playerPosition = { x, z };
        this.updatePlayerMarker();
    }

    async travelToSelected() {
        if (!this.selectedRegion) return;

        const r = this.selectedRegion;
        const targetX = r.x * 3200 - 3200; // Center of region
        const targetZ = r.y * 3200 - 3200;

        this.close();

        // Teleport via API oder direkt
        try {
            const response = await fetch('/api/world-map/travel', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    player_id: 1,
                    target_region: r.id,
                    target_x: targetX,
                    target_z: targetZ
                })
            });

            if (response.ok) {
                // Teleport im Frontend
                if (typeof teleportPlayer === 'function') {
                    teleportPlayer(targetX, 5, targetZ);
                } else if (window.character) {
                    window.character.position.set(targetX, 5, targetZ);
                }

                this.setPlayerPosition(targetX, targetZ);

                if (typeof notify === 'function') {
                    notify(`🚀 Reise nach ${r.name}!`, 'success');
                }
            }
        } catch (e) {
            // Fallback: Direkt teleportieren
            if (window.character) {
                window.character.position.set(targetX, 5, targetZ);
                this.setPlayerPosition(targetX, targetZ);
            }
            console.log('Teleport zu', r.name, targetX, targetZ);
        }
    }

    toggle() {
        if (this.isOpen) {
            this.close();
        } else {
            this.open();
        }
    }

    open() {
        const container = document.getElementById('world-map-container');
        if (container) {
            container.classList.remove('hidden');
            this.isOpen = true;

            // Aktuelle Position updaten
            if (window.character) {
                this.setPlayerPosition(window.character.position.x, window.character.position.z);
            }
        }
    }

    close() {
        const container = document.getElementById('world-map-container');
        if (container) {
            container.classList.add('hidden');
            this.isOpen = false;
        }
    }

    // Unlock Travel Point
    unlockTravelPoint(regionId) {
        if (!this.unlockedTravelPoints.includes(regionId)) {
            this.unlockedTravelPoints.push(regionId);
            if (typeof notify === 'function') {
                const region = this.regions.find(r => r.id === regionId);
                notify(`🗺️ Neuer Schnellreisepunkt: ${region?.name}!`, 'success');
            }
        }
    }
}

// Initialize
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.worldMapUI = new WorldMapUI();
    });
} else {
    window.worldMapUI = new WorldMapUI();
}

window.WorldMapUI = WorldMapUI;

console.log('✅ World Map UI geladen - Drücke M zum Öffnen');
