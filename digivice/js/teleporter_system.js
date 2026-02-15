/**
 * TELEPORTER SYSTEM - Najika World
 * ===================================
 *
 * 8 Teleporter für die 8 Regionen:
 * 1. Götterfels (Startgebiet)
 * 2. Kristallwald
 * 3. Wüstenruinen
 * 4. Frostvulkan
 * 5. Dschungeltempel
 * 6. Unterwasserhöhlen
 * 7. Himmelsinseln
 * 8. Schattenlande
 *
 * Features:
 * - Fast Travel zwischen Regionen
 * - Muss erst freigeschaltet werden (Discovery)
 * - Kostet Gold (oder kostenlos nach Upgrade)
 * - Ladezeit-Simulation
 * - Schöne UI mit Region-Preview
 */

(function() {
    'use strict';

    // ==========================================
    // TELEPORTER KONFIGURATION
    // ==========================================

    const REGIONS = {
        goetterfels: {
            id: 'goetterfels',
            name: 'Götterfels',
            icon: '🏔️',
            description: 'Startgebiet - Die Schwarze Mühle',
            position: { x: 0, y: 50, z: 0 },
            unlocked: true,  // Immer freigeschaltet
            cost: 0,  // Kein Teleport-Cost zur Basis
            color: '#8b4513',
            background: 'linear-gradient(135deg, #654321, #8b7355)'
        },
        kristallwald: {
            id: 'kristallwald',
            name: 'Kristallwald',
            icon: '🌲💎',
            description: 'Magischer Wald mit Kristallbäumen',
            position: { x: 2000, y: 50, z: 1500 },
            unlocked: false,
            cost: 50,
            color: '#4a90e2',
            background: 'linear-gradient(135deg, #667eea, #764ba2)'
        },
        wuestenruinen: {
            id: 'wuestenruinen',
            name: 'Wüstenruinen',
            icon: '🏜️🏛️',
            description: 'Alte Pyramiden und Sandstürme',
            position: { x: -2000, y: 50, z: 2000 },
            unlocked: false,
            cost: 75,
            color: '#f4a460',
            background: 'linear-gradient(135deg, #FFD700, #FFA500)'
        },
        frostvulkan: {
            id: 'frostvulkan',
            name: 'Frostvulkan',
            icon: '🌋❄️',
            description: 'Gefrorener Vulkan im ewigen Winter',
            position: { x: -1500, y: 150, z: -2500 },
            unlocked: false,
            cost: 100,
            color: '#87ceeb',
            background: 'linear-gradient(135deg, #00bcd4, #2196F3)'
        },
        dschungeltempel: {
            id: 'dschungeltempel',
            name: 'Dschungeltempel',
            icon: '🌴⛩️',
            description: 'Überwucherter Tempel der Alten',
            position: { x: 1800, y: 50, z: -1800 },
            unlocked: false,
            cost: 75,
            color: '#228b22',
            background: 'linear-gradient(135deg, #4CAF50, #8BC34A)'
        },
        unterwasserhoehlen: {
            id: 'unterwasserhoehlen',
            name: 'Unterwasserhöhlen',
            icon: '🌊🐚',
            description: 'Geheimnisvolle Höhlen unter dem Meer',
            position: { x: 3000, y: -50, z: 500 },
            unlocked: false,
            cost: 125,
            color: '#1e90ff',
            background: 'linear-gradient(135deg, #0066ff, #00ccff)'
        },
        himmelsinseln: {
            id: 'himmelsinseln',
            name: 'Himmelsinseln',
            icon: '☁️🏝️',
            description: 'Schwebende Inseln in den Wolken',
            position: { x: -500, y: 500, z: 2500 },
            unlocked: false,
            cost: 150,
            color: '#f0f8ff',
            background: 'linear-gradient(135deg, #87ceeb, #e0f7ff)'
        },
        schattenlande: {
            id: 'schattenlande',
            name: 'Schattenlande',
            icon: '🌑💀',
            description: 'Dunkles Reich der Untoten',
            position: { x: 0, y: 50, z: -3000 },
            unlocked: false,
            cost: 200,
            color: '#483d8b',
            background: 'linear-gradient(135deg, #330066, #663399)'
        }
    };

    // ==========================================
    // TELEPORTER STATE
    // ==========================================

    const state = {
        unlockedRegions: ['goetterfels'],  // Startgebiet immer unlocked
        currentRegion: 'goetterfels',
        isTeleporting: false,
        teleportCount: 0,
        goldSpent: 0,
        hasUnlimitedPass: false  // Upgrade: Unbegrenztes Teleportieren
    };

    // ==========================================
    // TELEPORTER CLASS
    // ==========================================

    class TeleporterSystem {
        constructor() {
            this.loadState();
            this.createUI();
        }

        loadState() {
            try {
                const saved = JSON.parse(localStorage.getItem('najika_teleporter_state') || '{}');
                if (saved.unlockedRegions) state.unlockedRegions = saved.unlockedRegions;
                if (saved.currentRegion) state.currentRegion = saved.currentRegion;
                if (saved.teleportCount) state.teleportCount = saved.teleportCount;
                if (saved.goldSpent) state.goldSpent = saved.goldSpent;
                if (saved.hasUnlimitedPass) state.hasUnlimitedPass = saved.hasUnlimitedPass;

                // Unlock regions based on state
                state.unlockedRegions.forEach(id => {
                    if (REGIONS[id]) REGIONS[id].unlocked = true;
                });
            } catch (e) {
                console.error('❌ Fehler beim Laden des Teleporter-States:', e);
            }
        }

        saveState() {
            const saveData = {
                unlockedRegions: state.unlockedRegions,
                currentRegion: state.currentRegion,
                teleportCount: state.teleportCount,
                goldSpent: state.goldSpent,
                hasUnlimitedPass: state.hasUnlimitedPass
            };
            localStorage.setItem('najika_teleporter_state', JSON.stringify(saveData));
        }

        createUI() {
            if (document.getElementById('teleporter-ui')) return;

            const ui = document.createElement('div');
            ui.id = 'teleporter-ui';
            ui.className = 'teleporter-ui hidden';
            ui.innerHTML = `
                <div class="teleporter-panel">
                    <div class="teleporter-header">
                        <h2>🌍 Fast Travel</h2>
                        <div class="teleporter-stats">
                            <span>Reisen: ${state.teleportCount}</span>
                            <span>Ausgegeben: ${state.goldSpent}G</span>
                        </div>
                        <button class="teleporter-close" onclick="TeleporterSystem.close()">✖</button>
                    </div>
                    <div class="teleporter-content">
                        <div class="region-grid" id="region-grid">
                            ${this.renderRegionGrid()}
                        </div>
                    </div>
                    <div class="teleporter-footer">
                        <div class="current-region">
                            Aktuell: <span id="current-region-name">${REGIONS[state.currentRegion].name}</span>
                        </div>
                        ${state.hasUnlimitedPass ?
                            '<div class="unlimited-pass">♾️ Unbegrenzter Reise-Pass aktiv!</div>' :
                            '<button class="buy-pass-btn" onclick="TeleporterSystem.buyUnlimitedPass()">♾️ Unbegrenzter Pass (5000G)</button>'
                        }
                    </div>
                </div>
            `;

            document.body.appendChild(ui);
            this.addStyles();
        }

        renderRegionGrid() {
            return Object.values(REGIONS).map(region => {
                const isLocked = !region.unlocked;
                const isCurrent = region.id === state.currentRegion;
                const cost = state.hasUnlimitedPass ? 0 : region.cost;

                return `
                    <div class="region-card ${isLocked ? 'locked' : ''} ${isCurrent ? 'current' : ''}"
                         data-region="${region.id}"
                         onclick="${isLocked ? '' : `TeleporterSystem.teleportTo('${region.id}')`}"
                         style="background: ${region.background}">
                        <div class="region-icon">${region.icon}</div>
                        <div class="region-name">${region.name}</div>
                        <div class="region-description">${region.description}</div>
                        ${isCurrent ?
                            '<div class="region-badge current-badge">📍 Du bist hier</div>' :
                            isLocked ?
                                '<div class="region-badge locked-badge">🔒 Gesperrt</div>' :
                                `<div class="region-cost">${cost > 0 ? cost + 'G' : 'Kostenlos'}</div>`
                        }
                    </div>
                `;
            }).join('');
        }

        addStyles() {
            if (document.getElementById('teleporter-styles')) return;

            const styles = document.createElement('style');
            styles.id = 'teleporter-styles';
            styles.textContent = `
                .teleporter-ui {
                    position: fixed;
                    top: 0; left: 0; right: 0; bottom: 0;
                    background: rgba(0, 0, 0, 0.9);
                    z-index: 20000;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }
                .teleporter-ui.hidden { display: none; }

                .teleporter-panel {
                    background: linear-gradient(145deg, #1a1a2e, #16213e);
                    border: 3px solid #667eea;
                    border-radius: 15px;
                    width: 90%;
                    max-width: 1200px;
                    max-height: 90vh;
                    overflow-y: auto;
                    box-shadow: 0 10px 50px rgba(102, 126, 234, 0.5);
                }

                .teleporter-header {
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    padding: 20px;
                    border-radius: 12px 12px 0 0;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    flex-wrap: wrap;
                    gap: 15px;
                }

                .teleporter-header h2 {
                    margin: 0;
                    color: white;
                    font-size: 28px;
                }

                .teleporter-stats {
                    display: flex;
                    gap: 20px;
                    color: white;
                    font-size: 14px;
                }

                .teleporter-close {
                    background: rgba(255, 255, 255, 0.2);
                    border: none;
                    color: white;
                    font-size: 24px;
                    width: 40px;
                    height: 40px;
                    border-radius: 50%;
                    cursor: pointer;
                    transition: all 0.3s;
                }

                .teleporter-close:hover {
                    background: rgba(255, 255, 255, 0.3);
                    transform: rotate(90deg);
                }

                .teleporter-content {
                    padding: 30px;
                }

                .region-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
                    gap: 20px;
                }

                .region-card {
                    border-radius: 12px;
                    padding: 20px;
                    cursor: pointer;
                    transition: all 0.3s;
                    position: relative;
                    border: 3px solid rgba(255, 255, 255, 0.2);
                    min-height: 180px;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    text-align: center;
                }

                .region-card:not(.locked):not(.current):hover {
                    transform: translateY(-5px);
                    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
                    border-color: rgba(255, 255, 255, 0.6);
                }

                .region-card.locked {
                    opacity: 0.5;
                    cursor: not-allowed;
                    filter: grayscale(0.8);
                }

                .region-card.current {
                    border-color: #4CAF50;
                    box-shadow: 0 0 30px rgba(76, 175, 80, 0.5);
                }

                .region-icon {
                    font-size: 64px;
                    margin-bottom: 15px;
                }

                .region-name {
                    font-size: 22px;
                    font-weight: bold;
                    color: white;
                    margin-bottom: 10px;
                    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
                }

                .region-description {
                    font-size: 14px;
                    color: rgba(255, 255, 255, 0.9);
                    margin-bottom: 15px;
                }

                .region-cost {
                    background: rgba(0, 0, 0, 0.5);
                    padding: 8px 15px;
                    border-radius: 20px;
                    font-weight: bold;
                    color: #FFD700;
                    font-size: 16px;
                }

                .region-badge {
                    background: rgba(0, 0, 0, 0.7);
                    padding: 8px 15px;
                    border-radius: 20px;
                    font-weight: bold;
                    font-size: 14px;
                }

                .current-badge {
                    background: rgba(76, 175, 80, 0.8);
                    color: white;
                }

                .locked-badge {
                    background: rgba(100, 100, 100, 0.8);
                    color: #ccc;
                }

                .teleporter-footer {
                    background: rgba(0, 0, 0, 0.3);
                    padding: 20px;
                    border-radius: 0 0 12px 12px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    flex-wrap: wrap;
                    gap: 15px;
                }

                .current-region {
                    color: white;
                    font-size: 16px;
                }

                .current-region span {
                    color: #4CAF50;
                    font-weight: bold;
                }

                .unlimited-pass {
                    color: #FFD700;
                    font-weight: bold;
                    font-size: 16px;
                }

                .buy-pass-btn {
                    background: linear-gradient(135deg, #FFD700, #FFA500);
                    color: #000;
                    border: none;
                    padding: 12px 24px;
                    border-radius: 10px;
                    font-weight: bold;
                    font-size: 16px;
                    cursor: pointer;
                    transition: all 0.3s;
                }

                .buy-pass-btn:hover {
                    transform: scale(1.05);
                    box-shadow: 0 5px 20px rgba(255, 215, 0, 0.5);
                }

                /* Teleport Animation Overlay */
                .teleport-animation {
                    position: fixed;
                    top: 0; left: 0; right: 0; bottom: 0;
                    background: radial-gradient(circle, rgba(102, 126, 234, 0.8), rgba(0, 0, 0, 0.9));
                    z-index: 25000;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    animation: teleport-fade-in 0.5s;
                }

                @keyframes teleport-fade-in {
                    from { opacity: 0; }
                    to { opacity: 1; }
                }

                .teleport-spinner {
                    font-size: 80px;
                    animation: spin 2s linear infinite;
                }

                @keyframes spin {
                    from { transform: rotate(0deg); }
                    to { transform: rotate(360deg); }
                }

                .teleport-text {
                    color: white;
                    font-size: 28px;
                    font-weight: bold;
                    margin-top: 30px;
                    text-shadow: 0 0 20px rgba(255, 255, 255, 0.8);
                }
            `;

            document.head.appendChild(styles);
        }

        open() {
            const ui = document.getElementById('teleporter-ui');
            if (ui) {
                // Refresh grid
                const grid = document.getElementById('region-grid');
                if (grid) grid.innerHTML = this.renderRegionGrid();

                // Update current region display
                const currentNameEl = document.getElementById('current-region-name');
                if (currentNameEl) currentNameEl.textContent = REGIONS[state.currentRegion].name;

                ui.classList.remove('hidden');
            }
        }

        close() {
            const ui = document.getElementById('teleporter-ui');
            if (ui) ui.classList.add('hidden');
        }

        teleportTo(regionId) {
            if (state.isTeleporting) return;

            const region = REGIONS[regionId];
            if (!region || !region.unlocked || region.id === state.currentRegion) return;

            const cost = state.hasUnlimitedPass ? 0 : region.cost;

            // Check gold (if we have player data)
            if (cost > 0 && window.player && window.player.gold < cost) {
                notify(`❌ Nicht genug Gold! Benötigt: ${cost}G`, 'error');
                return;
            }

            state.isTeleporting = true;

            // Show teleport animation
            this.showTeleportAnimation(region);

            // Deduct gold
            if (cost > 0 && window.player) {
                window.player.gold -= cost;
                state.goldSpent += cost;
            }

            // Teleport after animation
            setTimeout(() => {
                this.performTeleport(region);
                state.teleportCount++;
                this.saveState();
                state.isTeleporting = false;
            }, 2500);
        }

        showTeleportAnimation(region) {
            const animation = document.createElement('div');
            animation.className = 'teleport-animation';
            animation.innerHTML = `
                <div style="text-align: center;">
                    <div class="teleport-spinner">🌀</div>
                    <div class="teleport-text">Reise nach ${region.name}...</div>
                </div>
            `;

            document.body.appendChild(animation);

            setTimeout(() => animation.remove(), 2500);
        }

        performTeleport(region) {
            state.currentRegion = region.id;

            // Teleport player - versuche verschiedene Character-Referenzen
            const character = window.Scene3D?.characterGroup;
            if (character) {
                // Setze nur X/Z, Y wird von updateCharacterHeight() automatisch korrigiert
                character.position.x = region.position.x;
                character.position.z = region.position.z;
                // Y auf safe Wert setzen (wird nächsten Frame korrigiert)
                character.position.y = Math.max(region.position.y, 10);
                console.log(`✨ Teleportiert nach: ${region.name} (${region.position.x}, ${region.position.z})`);
            } else if (window.player && window.player.mesh) {
                window.player.mesh.position.set(region.position.x, region.position.y, region.position.z);
                console.log(`✨ Teleportiert nach: ${region.name} (fallback player.mesh)`);
            } else {
                console.warn('Kein Character gefunden zum Teleportieren!');
            }

            // Notify systems
            if (window.WorldManager) {
                window.WorldManager.onRegionChange(region.id);
            }

            this.close();
        }

        unlockRegion(regionId) {
            const region = REGIONS[regionId];
            if (!region || region.unlocked) return;

            region.unlocked = true;
            if (!state.unlockedRegions.includes(regionId)) {
                state.unlockedRegions.push(regionId);
            }

            this.saveState();
            console.log(`🔓 Region freigeschaltet: ${region.name}`);

            // Show notification
            this.showUnlockNotification(region);
        }

        showUnlockNotification(region) {
            const notification = document.createElement('div');
            notification.style.cssText = `
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: linear-gradient(135deg, #4CAF50, #8BC34A);
                color: white;
                padding: 30px;
                border-radius: 15px;
                font-size: 24px;
                font-weight: bold;
                text-align: center;
                z-index: 30000;
                box-shadow: 0 10px 50px rgba(76, 175, 80, 0.7);
                animation: unlock-appear 0.5s;
            `;
            notification.innerHTML = `
                <div style="font-size: 64px; margin-bottom: 15px;">${region.icon}</div>
                <div>🔓 Region freigeschaltet!</div>
                <div style="font-size: 20px; margin-top: 10px;">${region.name}</div>
            `;

            document.body.appendChild(notification);

            setTimeout(() => notification.remove(), 3000);
        }

        buyUnlimitedPass() {
            if (state.hasUnlimitedPass) {
                notify('✅ Du hast bereits den unbegrenzten Reise-Pass!', 'info');
                return;
            }

            const cost = 5000;

            if (window.player && window.player.gold < cost) {
                notify(`❌ Nicht genug Gold! Benötigt: ${cost}G`, 'error');
                return;
            }

            // Kauf ohne blocking confirm - Button wurde bereits bewusst geklickt
            notify(`♾️ Reise-Pass wird gekauft für ${cost}G...`, 'info');

            if (window.player) {
                window.player.gold -= cost;
            }

            state.hasUnlimitedPass = true;
            this.saveState();

            notify('✅ Unbegrenzter Reise-Pass gekauft! Alle Teleportationen sind jetzt kostenlos!', 'success');
            this.open();  // Refresh UI
        }

        // ==========================================
        // PUBLIC API
        // ==========================================

        getState() {
            return { ...state, regions: REGIONS };
        }

        getCurrentRegion() {
            return REGIONS[state.currentRegion];
        }

        isRegionUnlocked(regionId) {
            return REGIONS[regionId]?.unlocked || false;
        }
    }

    // ==========================================
    // GLOBAL INSTANCE
    // ==========================================

    window.TeleporterSystem = new TeleporterSystem();

    // Keyboard shortcut: M für Map/Teleporter (NICHT wenn Combat aktiv!)
    document.addEventListener('keydown', (e) => {
        if (e.key === 'm' || e.key === 'M') {
            // Skip wenn in Combat (M = Mode Toggle im Combat)
            if (window.Real3DCombat?.isActive?.() || window.combatActive) return;
            // Skip wenn in Input-Feld
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
            const ui = document.getElementById('teleporter-ui');
            if (ui) {
                if (ui.classList.contains('hidden')) {
                    window.TeleporterSystem.open();
                } else {
                    window.TeleporterSystem.close();
                }
            }
        }
    });

    console.log('🌍 Teleporter System loaded!');
    console.log('   📍 8 Regionen verfügbar');
    console.log('   🗝️ Taste M zum Öffnen');

})();
