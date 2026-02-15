// =============================================================================
// DUNGEON UI SYSTEM - Keller-Testbed & Procedural Dungeons
// =============================================================================
// Backend: najika_dungeon_generator.py (BSP + Random Walk)
// APIs: /api/dungeon/generate, /api/dungeon/biomes, /api/dungeon/difficulties
// =============================================================================

class DungeonUI {
    constructor() {
        // ===== DUNGEON STATE =====
        this.currentDungeon = null;
        this.currentRoomId = 0;
        this.isOpen = false;
        this.isInCombat = false;

        // ===== PLAYER STATE =====
        this.playerHP = 100;
        this.playerMaxHP = 100;
        this.playerMP = 50;
        this.playerMaxMP = 50;

        // ===== UI ELEMENTS =====
        this.container = null;
        this.minimapCanvas = null;
        this.minimapCtx = null;

        // ===== ROOM TYPE ICONS =====
        this.roomIcons = {
            'entrance': '🚪',
            'combat': '⚔️',
            'loot': '💎',
            'trap': '⚠️',
            'puzzle': '🧩',
            'boss': '👹',
            'rest': '🏕️',
            'shop': '🛒',
            'secret': '❓',
            'corridor': '➡️',
            'exit': '🚪'
        };

        // ===== BIOME COLORS =====
        this.biomeColors = {
            'ice': { bg: '#1a2a3a', accent: '#87CEEB', floor: '#2a3a4a' },
            'desert': { bg: '#3a2a1a', accent: '#FFD700', floor: '#4a3a2a' },
            'swamp': { bg: '#1a2a1a', accent: '#32CD32', floor: '#2a3a2a' },
            'coast': { bg: '#1a2a3a', accent: '#00CED1', floor: '#2a3a4a' },
            'caves': { bg: '#1a1a2a', accent: '#9370DB', floor: '#2a2a3a' },
            'volcano': { bg: '#3a1a1a', accent: '#FF4500', floor: '#4a2a2a' },
            'forest': { bg: '#1a2a1a', accent: '#228B22', floor: '#2a3a2a' },
            'highland': { bg: '#2a2a3a', accent: '#DDA0DD', floor: '#3a3a4a' }
        };

        // ===== DIFFICULTY NAMES =====
        this.difficultyNames = {
            1: 'Tutorial',
            2: 'Leicht',
            3: 'Normal',
            4: 'Schwer',
            5: 'Albtraum',
            99: 'Endlos'
        };

        this.initStyles();
        console.log('[DungeonUI] System initialized');
    }

    // =========================================================================
    // STYLES
    // =========================================================================

    initStyles() {
        if (document.getElementById('dungeon-ui-styles')) return;

        const styles = document.createElement('style');
        styles.id = 'dungeon-ui-styles';
        styles.textContent = `
            #dungeon-container {
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                background: rgba(0, 0, 0, 0.95);
                z-index: 9000;
                display: none;
                flex-direction: column;
            }

            #dungeon-container.open {
                display: flex;
            }

            /* Header */
            .dungeon-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 15px 20px;
                background: linear-gradient(180deg, rgba(0,0,0,0.9) 0%, rgba(0,0,0,0.7) 100%);
                border-bottom: 2px solid #4CAF50;
            }

            .dungeon-title {
                color: #4CAF50;
                font-size: 24px;
                font-weight: bold;
                text-shadow: 0 0 10px #4CAF50;
            }

            .dungeon-info {
                display: flex;
                gap: 20px;
                color: #fff;
            }

            .dungeon-info-item {
                display: flex;
                align-items: center;
                gap: 5px;
            }

            .dungeon-close {
                background: #FF4444;
                border: none;
                color: #fff;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
            }

            .dungeon-close:hover {
                background: #FF6666;
            }

            /* Main Content */
            .dungeon-main {
                display: flex;
                flex: 1;
                overflow: hidden;
            }

            /* Minimap Panel */
            .dungeon-minimap-panel {
                width: 300px;
                background: rgba(20, 20, 30, 0.9);
                border-right: 2px solid #4CAF50;
                padding: 15px;
                display: flex;
                flex-direction: column;
            }

            .minimap-title {
                color: #4CAF50;
                font-size: 16px;
                margin-bottom: 10px;
                text-align: center;
            }

            #dungeon-minimap {
                flex: 1;
                background: #0a0a15;
                border-radius: 10px;
                border: 2px solid #333;
            }

            .minimap-legend {
                margin-top: 10px;
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 5px;
                font-size: 11px;
                color: #888;
            }

            .legend-item {
                display: flex;
                align-items: center;
                gap: 5px;
            }

            /* Room View Panel */
            .dungeon-room-panel {
                flex: 1;
                display: flex;
                flex-direction: column;
                padding: 20px;
            }

            .room-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
            }

            .room-title {
                color: #FFD700;
                font-size: 28px;
            }

            .room-type-badge {
                background: rgba(76, 175, 80, 0.3);
                color: #4CAF50;
                padding: 5px 15px;
                border-radius: 20px;
                font-size: 14px;
            }

            .room-content {
                flex: 1;
                background: rgba(30, 30, 40, 0.8);
                border-radius: 15px;
                padding: 20px;
                border: 2px solid #333;
                display: flex;
                flex-direction: column;
            }

            .room-description {
                color: #ccc;
                font-size: 16px;
                line-height: 1.6;
                margin-bottom: 20px;
            }

            /* Enemies */
            .room-enemies {
                margin-bottom: 20px;
            }

            .enemies-title {
                color: #FF4444;
                font-size: 18px;
                margin-bottom: 10px;
            }

            .enemy-list {
                display: flex;
                gap: 15px;
                flex-wrap: wrap;
            }

            .enemy-card {
                background: rgba(255, 68, 68, 0.2);
                border: 2px solid #FF4444;
                border-radius: 10px;
                padding: 15px;
                min-width: 150px;
                text-align: center;
            }

            .enemy-icon {
                font-size: 40px;
                margin-bottom: 10px;
            }

            .enemy-name {
                color: #FF4444;
                font-weight: bold;
            }

            .enemy-hp {
                color: #888;
                font-size: 12px;
            }

            /* Loot */
            .room-loot {
                margin-bottom: 20px;
            }

            .loot-title {
                color: #FFD700;
                font-size: 18px;
                margin-bottom: 10px;
            }

            .loot-list {
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
            }

            .loot-item {
                background: rgba(255, 215, 0, 0.2);
                border: 2px solid #FFD700;
                border-radius: 10px;
                padding: 10px 15px;
                cursor: pointer;
                transition: all 0.3s ease;
            }

            .loot-item:hover {
                transform: scale(1.05);
                box-shadow: 0 0 15px rgba(255, 215, 0, 0.5);
            }

            .loot-item.collected {
                opacity: 0.5;
                pointer-events: none;
            }

            /* Navigation */
            .room-navigation {
                display: flex;
                gap: 10px;
                justify-content: center;
                margin-top: auto;
                padding-top: 20px;
                border-top: 1px solid #333;
            }

            .nav-button {
                background: linear-gradient(135deg, #2d5a3d, #1e3a2a);
                border: 2px solid #4CAF50;
                color: #fff;
                padding: 15px 30px;
                border-radius: 10px;
                cursor: pointer;
                font-size: 16px;
                display: flex;
                align-items: center;
                gap: 10px;
                transition: all 0.3s ease;
            }

            .nav-button:hover:not(:disabled) {
                background: linear-gradient(135deg, #4CAF50, #2d5a3d);
                transform: translateY(-3px);
                box-shadow: 0 5px 15px rgba(76, 175, 80, 0.4);
            }

            .nav-button:disabled {
                opacity: 0.5;
                cursor: not-allowed;
            }

            .nav-button.combat {
                background: linear-gradient(135deg, #5a2d2d, #3a1e1e);
                border-color: #FF4444;
            }

            .nav-button.combat:hover:not(:disabled) {
                background: linear-gradient(135deg, #FF4444, #5a2d2d);
                box-shadow: 0 5px 15px rgba(255, 68, 68, 0.4);
            }

            /* Player Stats */
            .player-stats {
                display: flex;
                gap: 20px;
                padding: 10px 20px;
                background: rgba(0, 0, 0, 0.5);
                border-top: 2px solid #4CAF50;
            }

            .stat-bar {
                flex: 1;
                display: flex;
                flex-direction: column;
                gap: 5px;
            }

            .stat-label {
                display: flex;
                justify-content: space-between;
                font-size: 12px;
            }

            .stat-bar-bg {
                height: 20px;
                background: #333;
                border-radius: 10px;
                overflow: hidden;
            }

            .stat-bar-fill {
                height: 100%;
                transition: width 0.3s ease;
            }

            .stat-bar-fill.hp {
                background: linear-gradient(90deg, #FF4444, #FF8888);
            }

            .stat-bar-fill.mp {
                background: linear-gradient(90deg, #4444FF, #8888FF);
            }

            /* Combat Overlay */
            .combat-overlay {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(255, 0, 0, 0.1);
                display: none;
                align-items: center;
                justify-content: center;
                z-index: 100;
            }

            .combat-overlay.active {
                display: flex;
                animation: combatPulse 1s ease infinite alternate;
            }

            @keyframes combatPulse {
                from { background: rgba(255, 0, 0, 0.05); }
                to { background: rgba(255, 0, 0, 0.15); }
            }

            /* Room Cleared */
            .room-cleared-badge {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: rgba(76, 175, 80, 0.9);
                color: #fff;
                padding: 20px 40px;
                border-radius: 15px;
                font-size: 24px;
                font-weight: bold;
                animation: clearedPop 0.5s ease;
            }

            @keyframes clearedPop {
                from { transform: translate(-50%, -50%) scale(0); }
                to { transform: translate(-50%, -50%) scale(1); }
            }

            /* Mobile */
            @media (max-width: 768px) {
                .dungeon-main {
                    flex-direction: column;
                }

                .dungeon-minimap-panel {
                    width: 100%;
                    height: 200px;
                    border-right: none;
                    border-bottom: 2px solid #4CAF50;
                }

                .room-navigation {
                    flex-wrap: wrap;
                }

                .nav-button {
                    padding: 10px 20px;
                    font-size: 14px;
                }
            }
        `;
        document.head.appendChild(styles);
    }

    // =========================================================================
    // API CALLS
    // =========================================================================

    async generateDungeon(biome = 'caves', difficulty = 1, floor = 1, seed = null) {
        try {
            let url = `http://localhost:8001/api/dungeon/generate/${biome}/${difficulty}/${floor}`;
            if (seed) url += `?seed=${seed}`;

            const response = await fetch(url);
            if (!response.ok) throw new Error('Failed to generate dungeon');

            const data = await response.json();
            this.currentDungeon = data;
            this.currentRoomId = data.entrance_id || 0;

            // Mark entrance as discovered
            const entrance = this.getRoom(this.currentRoomId);
            if (entrance) entrance.discovered = true;

            console.log('[DungeonUI] Dungeon generated:', data);
            return data;
        } catch (error) {
            console.error('[DungeonUI] Error generating dungeon:', error);

            // Fallback: Generate a simple test dungeon
            return this.generateTestDungeon();
        }
    }

    generateTestDungeon() {
        // Simple test dungeon for offline testing
        this.currentDungeon = {
            seed: Date.now(),
            biome: 'caves',
            difficulty: 1,
            floor: 1,
            rooms: [
                {
                    id: 0, type: 'entrance', position: { x: 5, y: 5 },
                    width: 3, height: 3, connections: [1, 2],
                    cleared: true, discovered: true, enemies: [], loot: [], traps: []
                },
                {
                    id: 1, type: 'combat', position: { x: 10, y: 5 },
                    width: 4, height: 4, connections: [0, 3],
                    cleared: false, discovered: false,
                    enemies: [
                        { id: 1, name: 'Goblin', icon: '👺', hp: 30, maxHp: 30, attack: 5 },
                        { id: 2, name: 'Goblin', icon: '👺', hp: 30, maxHp: 30, attack: 5 }
                    ],
                    loot: [], traps: []
                },
                {
                    id: 2, type: 'loot', position: { x: 5, y: 10 },
                    width: 3, height: 3, connections: [0, 4],
                    cleared: false, discovered: false, enemies: [],
                    loot: [
                        { id: 1, name: 'Gold', icon: '💰', amount: 50 },
                        { id: 2, name: 'Heiltrank', icon: '🧪', amount: 1 }
                    ],
                    traps: []
                },
                {
                    id: 3, type: 'rest', position: { x: 15, y: 5 },
                    width: 3, height: 3, connections: [1, 5],
                    cleared: false, discovered: false, enemies: [], loot: [], traps: [],
                    special_feature: 'campfire'
                },
                {
                    id: 4, type: 'trap', position: { x: 5, y: 15 },
                    width: 3, height: 3, connections: [2, 5],
                    cleared: false, discovered: false, enemies: [],
                    loot: [{ id: 3, name: 'Schlüssel', icon: '🔑', amount: 1 }],
                    traps: [{ id: 1, name: 'Giftpfeile', damage: 20 }]
                },
                {
                    id: 5, type: 'boss', position: { x: 10, y: 15 },
                    width: 5, height: 5, connections: [3, 4],
                    cleared: false, discovered: false,
                    enemies: [
                        { id: 3, name: 'Dungeon-Herr', icon: '👹', hp: 150, maxHp: 150, attack: 15, isBoss: true }
                    ],
                    loot: [
                        { id: 4, name: 'Legendäres Schwert', icon: '⚔️', rarity: 'legendary' }
                    ],
                    traps: []
                }
            ],
            corridors: [],
            entrance_id: 0,
            boss_id: 5,
            exit_id: 5,
            total_rooms: 6
        };

        this.currentRoomId = 0;
        console.log('[DungeonUI] Test dungeon generated');
        return this.currentDungeon;
    }

    async getBiomes() {
        try {
            const response = await fetch('http://localhost:8001/api/dungeon/biomes');
            return await response.json();
        } catch (error) {
            return ['caves', 'forest', 'volcano', 'ice', 'desert', 'swamp', 'coast', 'highland'];
        }
    }

    async getDifficulties() {
        try {
            const response = await fetch('http://localhost:8001/api/dungeon/difficulties');
            return await response.json();
        } catch (error) {
            return [1, 2, 3, 4, 5, 99];
        }
    }

    // =========================================================================
    // ROOM MANAGEMENT
    // =========================================================================

    getRoom(roomId) {
        if (!this.currentDungeon) return null;
        return this.currentDungeon.rooms.find(r => r.id === roomId);
    }

    getCurrentRoom() {
        return this.getRoom(this.currentRoomId);
    }

    getConnectedRooms() {
        const current = this.getCurrentRoom();
        if (!current) return [];
        return current.connections.map(id => this.getRoom(id)).filter(r => r);
    }

    moveToRoom(roomId) {
        const room = this.getRoom(roomId);
        if (!room) return false;

        const current = this.getCurrentRoom();
        if (!current.connections.includes(roomId)) {
            console.log('[DungeonUI] Room not connected!');
            return false;
        }

        this.currentRoomId = roomId;
        room.discovered = true;

        // Check for traps
        if (room.traps && room.traps.length > 0 && !room.cleared) {
            this.triggerTraps(room);
        }

        this.render();
        return true;
    }

    // =========================================================================
    // COMBAT
    // =========================================================================

    hasEnemies(room) {
        return room.enemies && room.enemies.length > 0 && !room.cleared;
    }

    startCombat() {
        const room = this.getCurrentRoom();
        if (!this.hasEnemies(room)) return;

        this.isInCombat = true;
        console.log('[DungeonUI] Combat started!');

        // Integration with dungeon_combat.js if available
        if (window.dungeonCombat) {
            window.dungeonCombat.startBattle(room.enemies, () => {
                this.onCombatEnd(true);
            }, () => {
                this.onCombatEnd(false);
            });
        } else {
            // Simple fallback combat
            this.simpleCombat(room);
        }
    }

    simpleCombat(room) {
        // Very simple auto-combat for testing
        const totalEnemyHP = room.enemies.reduce((sum, e) => sum + e.hp, 0);
        const damage = Math.floor(totalEnemyHP * 0.3);

        this.playerHP = Math.max(0, this.playerHP - damage);

        if (this.playerHP > 0) {
            room.enemies = [];
            this.onCombatEnd(true);
        } else {
            this.onCombatEnd(false);
        }
    }

    onCombatEnd(victory) {
        this.isInCombat = false;
        const room = this.getCurrentRoom();

        if (victory) {
            room.cleared = true;
            room.enemies = [];
            console.log('[DungeonUI] Combat victory!');

            // Show loot if any
            if (room.loot && room.loot.length > 0) {
                this.showLootPopup(room.loot);
            }
        } else {
            console.log('[DungeonUI] Combat defeat!');
            this.close();
            // Show death screen or respawn
        }

        this.render();
    }

    // =========================================================================
    // TRAPS
    // =========================================================================

    triggerTraps(room) {
        if (!room.traps || room.traps.length === 0) return;

        let totalDamage = 0;
        room.traps.forEach(trap => {
            totalDamage += trap.damage || 10;
            console.log(`[DungeonUI] Trap triggered: ${trap.name}`);
        });

        this.playerHP = Math.max(0, this.playerHP - totalDamage);
        room.traps = []; // Traps are one-time

        // Show trap notification
        this.showNotification(`⚠️ Falle! -${totalDamage} HP`, 'danger');

        if (this.playerHP <= 0) {
            this.onCombatEnd(false);
        }
    }

    // =========================================================================
    // LOOT
    // =========================================================================

    collectLoot(lootId) {
        const room = this.getCurrentRoom();
        if (!room.loot) return;

        const lootIndex = room.loot.findIndex(l => l.id === lootId);
        if (lootIndex === -1) return;

        const loot = room.loot[lootIndex];
        room.loot.splice(lootIndex, 1);

        console.log(`[DungeonUI] Collected: ${loot.name}`);
        this.showNotification(`✨ ${loot.icon} ${loot.name} erhalten!`, 'success');

        // Add to inventory if available
        if (window.inventorySystem) {
            window.inventorySystem.addItem(loot);
        }

        this.render();
    }

    showLootPopup(loot) {
        if (!loot || loot.length === 0) return;
        // Gebündeltes Loot-Popup
        const lootText = loot.map(item => `${item.icon || '💎'} ${item.name}${item.amount ? ' x' + item.amount : ''}`).join(', ');
        if (typeof notify === 'function') {
            notify(`🎁 Beute: ${lootText}`, 'success');
        }
        loot.forEach(item => {
            this.showNotification(`💎 ${item.icon} ${item.name}`, 'loot');
        });
    }

    // =========================================================================
    // REST
    // =========================================================================

    rest() {
        const room = this.getCurrentRoom();
        if (room.type !== 'rest') return;

        const healAmount = Math.floor(this.playerMaxHP * 0.5);
        this.playerHP = Math.min(this.playerMaxHP, this.playerHP + healAmount);
        this.playerMP = this.playerMaxMP;

        room.cleared = true;

        this.showNotification(`🏕️ Ausgeruht! +${healAmount} HP`, 'success');
        this.render();
    }

    // =========================================================================
    // UI RENDERING
    // =========================================================================

    open() {
        if (!this.currentDungeon) {
            this.generateTestDungeon();
        }

        this.createUI();
        this.isOpen = true;
        this.container.classList.add('open');
        this.render();
    }

    close() {
        if (this.container) {
            this.container.classList.remove('open');
        }
        this.isOpen = false;
    }

    toggle() {
        if (this.isOpen) {
            this.close();
        } else {
            this.open();
        }
    }

    createUI() {
        if (document.getElementById('dungeon-container')) {
            this.container = document.getElementById('dungeon-container');
            return;
        }

        this.container = document.createElement('div');
        this.container.id = 'dungeon-container';

        this.container.innerHTML = `
            <div class="dungeon-header">
                <div class="dungeon-title">🏰 Dungeon</div>
                <div class="dungeon-info">
                    <div class="dungeon-info-item">
                        <span>🌍</span>
                        <span id="dungeon-biome">-</span>
                    </div>
                    <div class="dungeon-info-item">
                        <span>⚔️</span>
                        <span id="dungeon-difficulty">-</span>
                    </div>
                    <div class="dungeon-info-item">
                        <span>🏛️</span>
                        <span id="dungeon-floor">Etage -</span>
                    </div>
                    <div class="dungeon-info-item">
                        <span>📍</span>
                        <span id="dungeon-progress">0/0</span>
                    </div>
                </div>
                <button class="dungeon-close" onclick="dungeonUI.close()">✕ Schließen</button>
            </div>

            <div class="dungeon-main">
                <div class="dungeon-minimap-panel">
                    <div class="minimap-title">📍 Karte</div>
                    <canvas id="dungeon-minimap" width="270" height="300"></canvas>
                    <div class="minimap-legend">
                        <div class="legend-item">🚪 Eingang</div>
                        <div class="legend-item">⚔️ Kampf</div>
                        <div class="legend-item">💎 Schatz</div>
                        <div class="legend-item">⚠️ Falle</div>
                        <div class="legend-item">🏕️ Rast</div>
                        <div class="legend-item">👹 Boss</div>
                    </div>
                </div>

                <div class="dungeon-room-panel">
                    <div class="room-header">
                        <div class="room-title" id="room-title">-</div>
                        <div class="room-type-badge" id="room-type-badge">-</div>
                    </div>
                    <div class="room-content" id="room-content">
                        <div class="room-description" id="room-description">-</div>
                        <div class="room-enemies" id="room-enemies"></div>
                        <div class="room-loot" id="room-loot"></div>
                        <div class="room-navigation" id="room-navigation"></div>
                    </div>
                    <div class="combat-overlay" id="combat-overlay"></div>
                </div>
            </div>

            <div class="player-stats">
                <div class="stat-bar">
                    <div class="stat-label">
                        <span style="color: #FF4444;">❤️ HP</span>
                        <span id="hp-text">100/100</span>
                    </div>
                    <div class="stat-bar-bg">
                        <div class="stat-bar-fill hp" id="hp-bar" style="width: 100%;"></div>
                    </div>
                </div>
                <div class="stat-bar">
                    <div class="stat-label">
                        <span style="color: #4444FF;">💧 MP</span>
                        <span id="mp-text">50/50</span>
                    </div>
                    <div class="stat-bar-bg">
                        <div class="stat-bar-fill mp" id="mp-bar" style="width: 100%;"></div>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(this.container);

        // Get canvas
        this.minimapCanvas = document.getElementById('dungeon-minimap');
        this.minimapCtx = this.minimapCanvas.getContext('2d');
    }

    render() {
        if (!this.isOpen || !this.currentDungeon) return;

        this.renderHeader();
        this.renderMinimap();
        this.renderRoom();
        this.renderPlayerStats();
    }

    renderHeader() {
        const biomeNames = {
            'ice': 'Eisreich', 'desert': 'Wüste', 'swamp': 'Sumpf',
            'coast': 'Küste', 'caves': 'Höhlen', 'volcano': 'Vulkan',
            'forest': 'Wald', 'highland': 'Hochland'
        };

        document.getElementById('dungeon-biome').textContent =
            biomeNames[this.currentDungeon.biome] || this.currentDungeon.biome;
        document.getElementById('dungeon-difficulty').textContent =
            this.difficultyNames[this.currentDungeon.difficulty] || 'Unbekannt';
        document.getElementById('dungeon-floor').textContent =
            `Etage ${this.currentDungeon.floor}`;

        const cleared = this.currentDungeon.rooms.filter(r => r.cleared).length;
        document.getElementById('dungeon-progress').textContent =
            `${cleared}/${this.currentDungeon.rooms.length}`;
    }

    renderMinimap() {
        const ctx = this.minimapCtx;
        const canvas = this.minimapCanvas;
        const rooms = this.currentDungeon.rooms;

        // Clear
        ctx.fillStyle = '#0a0a15';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        if (rooms.length === 0) return;

        // Calculate bounds
        let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
        rooms.forEach(room => {
            minX = Math.min(minX, room.position.x);
            minY = Math.min(minY, room.position.y);
            maxX = Math.max(maxX, room.position.x + room.width);
            maxY = Math.max(maxY, room.position.y + room.height);
        });

        const padding = 20;
        const scaleX = (canvas.width - padding * 2) / (maxX - minX + 1);
        const scaleY = (canvas.height - padding * 2) / (maxY - minY + 1);
        const scale = Math.min(scaleX, scaleY, 15);

        const offsetX = padding + (canvas.width - padding * 2 - (maxX - minX) * scale) / 2;
        const offsetY = padding + (canvas.height - padding * 2 - (maxY - minY) * scale) / 2;

        // Draw connections first
        ctx.strokeStyle = '#333';
        ctx.lineWidth = 2;
        rooms.forEach(room => {
            if (!room.discovered) return;
            const x1 = offsetX + (room.position.x + room.width / 2 - minX) * scale;
            const y1 = offsetY + (room.position.y + room.height / 2 - minY) * scale;

            room.connections.forEach(connId => {
                const conn = this.getRoom(connId);
                if (!conn || !conn.discovered) return;

                const x2 = offsetX + (conn.position.x + conn.width / 2 - minX) * scale;
                const y2 = offsetY + (conn.position.y + conn.height / 2 - minY) * scale;

                ctx.beginPath();
                ctx.moveTo(x1, y1);
                ctx.lineTo(x2, y2);
                ctx.stroke();
            });
        });

        // Draw rooms
        rooms.forEach(room => {
            const x = offsetX + (room.position.x - minX) * scale;
            const y = offsetY + (room.position.y - minY) * scale;
            const w = room.width * scale;
            const h = room.height * scale;

            if (!room.discovered) {
                // Undiscovered
                ctx.fillStyle = '#222';
                ctx.fillRect(x, y, w, h);
                return;
            }

            // Room color based on type
            const colors = {
                'entrance': '#4CAF50',
                'combat': room.cleared ? '#666' : '#FF4444',
                'loot': room.cleared ? '#666' : '#FFD700',
                'trap': room.cleared ? '#666' : '#FF8800',
                'puzzle': '#9370DB',
                'boss': room.cleared ? '#666' : '#FF0000',
                'rest': room.cleared ? '#666' : '#00CED1',
                'shop': '#FFD700',
                'secret': '#9370DB',
                'exit': '#4CAF50'
            };

            ctx.fillStyle = colors[room.type] || '#555';
            ctx.fillRect(x, y, w, h);

            // Current room highlight
            if (room.id === this.currentRoomId) {
                ctx.strokeStyle = '#FFD700';
                ctx.lineWidth = 3;
                ctx.strokeRect(x - 2, y - 2, w + 4, h + 4);
            }

            // Room icon
            const icon = this.roomIcons[room.type] || '?';
            ctx.font = `${Math.min(w, h) * 0.6}px Arial`;
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillStyle = '#fff';
            ctx.fillText(icon, x + w / 2, y + h / 2);
        });
    }

    renderRoom() {
        const room = this.getCurrentRoom();
        if (!room) return;

        // Title
        const roomNames = {
            'entrance': 'Eingang',
            'combat': 'Kampfraum',
            'loot': 'Schatzkammer',
            'trap': 'Fallenraum',
            'puzzle': 'Rätselraum',
            'boss': 'Bosskammer',
            'rest': 'Rastplatz',
            'shop': 'Händler',
            'secret': 'Geheimraum',
            'exit': 'Ausgang'
        };

        document.getElementById('room-title').textContent =
            `${this.roomIcons[room.type]} ${roomNames[room.type] || 'Raum'}`;
        document.getElementById('room-type-badge').textContent =
            room.cleared ? '✅ Gesäubert' : roomNames[room.type];

        // Description
        const descriptions = {
            'entrance': 'Der Eingang zum Dungeon. Von hier aus beginnt dein Abenteuer.',
            'combat': 'Feinde lauern in diesem Raum. Bereite dich auf den Kampf vor!',
            'loot': 'Schätze glitzern im Dämmerlicht. Was wirst du finden?',
            'trap': 'Vorsicht! Dieser Raum könnte gefährlich sein.',
            'puzzle': 'Ein Rätsel wartet darauf, gelöst zu werden.',
            'boss': 'Eine mächtige Präsenz füllt den Raum. Der Dungeon-Herrscher erwartet dich!',
            'rest': 'Ein sicherer Ort zum Ausruhen und Heilen.',
            'shop': 'Ein mysteriöser Händler bietet seine Waren an.',
            'secret': 'Du hast einen verborgenen Raum entdeckt!',
            'exit': 'Der Ausgang des Dungeons. Deine Reise endet hier.'
        };

        document.getElementById('room-description').textContent =
            room.cleared ? 'Dieser Raum wurde bereits gesäubert.' : descriptions[room.type] || '';

        // Enemies
        const enemiesDiv = document.getElementById('room-enemies');
        if (this.hasEnemies(room)) {
            enemiesDiv.innerHTML = `
                <div class="enemies-title">👹 Feinde</div>
                <div class="enemy-list">
                    ${room.enemies.map(e => `
                        <div class="enemy-card ${e.isBoss ? 'boss' : ''}">
                            <div class="enemy-icon">${e.icon || '👾'}</div>
                            <div class="enemy-name">${e.name}</div>
                            <div class="enemy-hp">❤️ ${e.hp}/${e.maxHp}</div>
                        </div>
                    `).join('')}
                </div>
            `;
        } else {
            enemiesDiv.innerHTML = '';
        }

        // Loot
        const lootDiv = document.getElementById('room-loot');
        if (room.loot && room.loot.length > 0) {
            lootDiv.innerHTML = `
                <div class="loot-title">💎 Beute</div>
                <div class="loot-list">
                    ${room.loot.map(l => `
                        <div class="loot-item" onclick="dungeonUI.collectLoot(${l.id})">
                            ${l.icon || '📦'} ${l.name}
                            ${l.amount > 1 ? `x${l.amount}` : ''}
                        </div>
                    `).join('')}
                </div>
            `;
        } else {
            lootDiv.innerHTML = '';
        }

        // Navigation
        this.renderNavigation(room);
    }

    renderNavigation(room) {
        const navDiv = document.getElementById('room-navigation');
        let buttons = [];

        // Combat button if enemies
        if (this.hasEnemies(room)) {
            buttons.push(`
                <button class="nav-button combat" onclick="dungeonUI.startCombat()">
                    ⚔️ Kämpfen!
                </button>
            `);
        }

        // Rest button
        if (room.type === 'rest' && !room.cleared) {
            buttons.push(`
                <button class="nav-button" onclick="dungeonUI.rest()">
                    🏕️ Ausruhen
                </button>
            `);
        }

        // Connected rooms
        const connected = this.getConnectedRooms();
        connected.forEach(r => {
            const icon = r.discovered ? this.roomIcons[r.type] : '❓';
            const name = r.discovered ? (r.cleared ? '✅' : '') : 'Unbekannt';
            const disabled = this.hasEnemies(room) ? 'disabled' : '';

            buttons.push(`
                <button class="nav-button" onclick="dungeonUI.moveToRoom(${r.id})" ${disabled}>
                    ${icon} Raum ${r.id} ${name}
                </button>
            `);
        });

        // Exit button if at entrance
        if (room.type === 'entrance') {
            buttons.push(`
                <button class="nav-button" onclick="dungeonUI.close()">
                    🚪 Dungeon verlassen
                </button>
            `);
        }

        navDiv.innerHTML = buttons.join('');
    }

    renderPlayerStats() {
        const hpPercent = (this.playerHP / this.playerMaxHP) * 100;
        const mpPercent = (this.playerMP / this.playerMaxMP) * 100;

        document.getElementById('hp-bar').style.width = `${hpPercent}%`;
        document.getElementById('hp-text').textContent = `${this.playerHP}/${this.playerMaxHP}`;

        document.getElementById('mp-bar').style.width = `${mpPercent}%`;
        document.getElementById('mp-text').textContent = `${this.playerMP}/${this.playerMaxMP}`;
    }

    // =========================================================================
    // NOTIFICATIONS
    // =========================================================================

    showNotification(message, type = 'info') {
        const colors = {
            'success': '#4CAF50',
            'danger': '#FF4444',
            'loot': '#FFD700',
            'info': '#2196F3'
        };

        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 100px;
            left: 50%;
            transform: translateX(-50%);
            background: ${colors[type] || colors.info};
            color: #fff;
            padding: 15px 30px;
            border-radius: 10px;
            font-size: 18px;
            font-weight: bold;
            z-index: 10000;
            animation: notificationPop 0.3s ease;
            box-shadow: 0 5px 20px rgba(0,0,0,0.3);
        `;
        notification.textContent = message;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.style.animation = 'fadeOut 0.3s ease forwards';
            setTimeout(() => notification.remove(), 300);
        }, 2000);
    }

    // =========================================================================
    // DEBUG
    // =========================================================================

    debug() {
        console.log('=== DUNGEON DEBUG ===');
        console.log('Current Dungeon:', this.currentDungeon);
        console.log('Current Room:', this.getCurrentRoom());
        console.log('Connected Rooms:', this.getConnectedRooms());
        console.log('Player HP:', this.playerHP);
    }
}

// =========================================================================
// INITIALIZATION
// =========================================================================

// Global instance
window.dungeonUI = new DungeonUI();

// Keyboard shortcut (D key)
document.addEventListener('keydown', (e) => {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

    if (e.key === 'd' || e.key === 'D') {
        if (!e.ctrlKey && !e.altKey && !e.metaKey) {
            window.dungeonUI.toggle();
        }
    }
});

console.log('[DungeonUI] Press D to open dungeon UI');
