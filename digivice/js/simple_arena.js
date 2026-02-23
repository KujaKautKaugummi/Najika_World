/**
 * SIMPLE ARENA - Quick Fight gegen KayKit Gegner
 * ===============================================
 *
 * Einfaches Arena-System das direkt ins 3D Combat startet
 */

(function() {
    'use strict';

    // Verfügbare Gegner
    const ARENA_ENEMIES = {
        normal: [
            { id: 'skeleton_warrior', name: 'Skelett-Krieger', level: 5, hp: 150 },
            { id: 'skeleton_archer', name: 'Skelett-Bogenschütze', level: 5, hp: 120 },
            { id: 'skeleton_mage', name: 'Skelett-Magier', level: 6, hp: 100 },
            { id: 'orc_warrior', name: 'Ork-Krieger', level: 7, hp: 200 },
            { id: 'orc_shaman', name: 'Ork-Schamane', level: 7, hp: 150 }
        ],
        hard: [
            { id: 'golem', name: 'Stein-Golem', level: 10, hp: 500 },
            { id: 'dragon', name: 'Drache', level: 15, hp: 800 }
        ],
        boss: [
            { id: 'demon_lord', name: 'Dämonenlord', level: 20, hp: 1500 }
        ]
    };

    // ==================== ARENA UI ====================

    function createArenaUI() {
        const ui = document.createElement('div');
        ui.id = 'simple-arena-ui';
        ui.className = 'simple-arena-ui hidden';
        ui.innerHTML = `
            <div class="arena-overlay"></div>
            <div class="arena-content">
                <div class="arena-header">
                    <h2>⚔️ ARENA - Wähle deinen Gegner</h2>
                    <button class="arena-close" onclick="closeArena()">&times;</button>
                </div>

                <div class="arena-body">
                    <!-- Normal Difficulty -->
                    <div class="arena-section">
                        <h3>🟢 NORMAL</h3>
                        <div class="arena-enemies">
                            ${ARENA_ENEMIES.normal.map(enemy => `
                                <div class="arena-enemy-card" onclick="startArenaFight('${enemy.id}', 'normal')">
                                    <div class="enemy-name">${enemy.name}</div>
                                    <div class="enemy-stats">
                                        <span>Lvl ${enemy.level}</span>
                                        <span>❤️ ${enemy.hp}</span>
                                    </div>
                                    <button class="fight-btn">Kämpfen!</button>
                                </div>
                            `).join('')}
                        </div>
                    </div>

                    <!-- Hard Difficulty -->
                    <div class="arena-section">
                        <h3>🟡 SCHWER</h3>
                        <div class="arena-enemies">
                            ${ARENA_ENEMIES.hard.map(enemy => `
                                <div class="arena-enemy-card" onclick="startArenaFight('${enemy.id}', 'hard')">
                                    <div class="enemy-name">${enemy.name}</div>
                                    <div class="enemy-stats">
                                        <span>Lvl ${enemy.level}</span>
                                        <span>❤️ ${enemy.hp}</span>
                                    </div>
                                    <button class="fight-btn">Kämpfen!</button>
                                </div>
                            `).join('')}
                        </div>
                    </div>

                    <!-- Boss Difficulty -->
                    <div class="arena-section">
                        <h3>🔴 BOSS</h3>
                        <div class="arena-enemies">
                            ${ARENA_ENEMIES.boss.map(enemy => `
                                <div class="arena-enemy-card boss-card" onclick="startArenaFight('${enemy.id}', 'boss')">
                                    <div class="enemy-name">${enemy.name}</div>
                                    <div class="enemy-stats">
                                        <span>Lvl ${enemy.level}</span>
                                        <span>❤️ ${enemy.hp}</span>
                                    </div>
                                    <button class="fight-btn">Kämpfen!</button>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(ui);
        addArenaStyles();
    }

    // ==================== STYLES ====================

    function addArenaStyles() {
        if (document.getElementById('simple-arena-styles')) return;

        const style = document.createElement('style');
        style.id = 'simple-arena-styles';
        style.textContent = `
            .simple-arena-ui {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: 9999;
                font-family: Arial, sans-serif;
            }

            .simple-arena-ui.hidden {
                display: none;
            }

            .arena-overlay {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.8);
            }

            .arena-content {
                position: relative;
                width: 90%;
                max-width: 1000px;
                height: 80%;
                margin: 5% auto;
                background: linear-gradient(135deg, #2c1810 0%, #1a0f0a 100%);
                border: 3px solid #d4af37;
                border-radius: 15px;
                overflow: hidden;
                display: flex;
                flex-direction: column;
            }

            .arena-header {
                background: linear-gradient(90deg, #8b4513 0%, #654321 100%);
                padding: 15px 20px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 2px solid #d4af37;
            }

            .arena-header h2 {
                margin: 0;
                color: #ffd700;
                font-size: 24px;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
            }

            .arena-close {
                background: #8b0000;
                border: none;
                color: white;
                font-size: 32px;
                width: 40px;
                height: 40px;
                border-radius: 50%;
                cursor: pointer;
                transition: all 0.3s;
            }

            .arena-close:hover {
                background: #ff0000;
                transform: rotate(90deg);
            }

            .arena-body {
                flex: 1;
                overflow-y: auto;
                padding: 20px;
            }

            .arena-section {
                margin-bottom: 30px;
            }

            .arena-section h3 {
                color: #ffd700;
                font-size: 20px;
                margin-bottom: 15px;
                text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
            }

            .arena-enemies {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
                gap: 15px;
            }

            .arena-enemy-card {
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid #d4af37;
                border-radius: 10px;
                padding: 15px;
                cursor: pointer;
                transition: all 0.3s;
            }

            .arena-enemy-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 5px 15px rgba(212, 175, 55, 0.5);
                border-color: #ffd700;
            }

            .arena-enemy-card.boss-card {
                border-color: #ff0000;
                background: rgba(255, 0, 0, 0.1);
            }

            .arena-enemy-card.boss-card:hover {
                border-color: #ff4444;
                box-shadow: 0 5px 15px rgba(255, 0, 0, 0.5);
            }

            .enemy-name {
                color: #ffd700;
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 10px;
                text-align: center;
            }

            .enemy-stats {
                display: flex;
                justify-content: space-around;
                margin-bottom: 10px;
                color: #ccc;
                font-size: 14px;
            }

            .fight-btn {
                width: 100%;
                padding: 10px;
                background: #228b22;
                border: none;
                border-radius: 5px;
                color: white;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.3s;
            }

            .fight-btn:hover {
                background: #32cd32;
                transform: scale(1.05);
            }

            .boss-card .fight-btn {
                background: #8b0000;
            }

            .boss-card .fight-btn:hover {
                background: #ff0000;
            }
        `;

        document.head.appendChild(style);
    }

    // ==================== FUNCTIONS ====================

    window.openNemesisArena = function() {
        console.log('🏟️ Opening Arena...');

        // Create UI if not exists
        if (!document.getElementById('simple-arena-ui')) {
            createArenaUI();
        }

        // Show UI
        document.getElementById('simple-arena-ui').classList.remove('hidden');
    };

    window.closeArena = function() {
        const ui = document.getElementById('simple-arena-ui');
        if (ui) {
            ui.classList.add('hidden');
        }
    };

    window.startArenaFight = function(enemyId, difficulty) {
        console.log(`⚔️ Arena fight requested: ${enemyId} (${difficulty})`);

        // Find enemy data
        let enemy = null;
        const enemies = ARENA_ENEMIES[difficulty];
        if (enemies) {
            enemy = enemies.find(e => e.id === enemyId);
        }

        if (!enemy) {
            console.error('Enemy not found:', enemyId);
            return;
        }

        // Bestaetigungs-Dialog zeigen
        const diffColors = { normal: '#44ff44', hard: '#ffaa00', boss: '#ff4444' };
        const diffNames = { normal: 'NORMAL', hard: 'SCHWER', boss: 'BOSS' };
        const confirmDiv = document.createElement('div');
        confirmDiv.id = 'arena-confirm';
        confirmDiv.style.cssText = 'position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.85);display:flex;align-items:center;justify-content:center;z-index:10000;';
        confirmDiv.innerHTML = `
            <div style="background:#1a1a2e;border:2px solid ${diffColors[difficulty]};border-radius:16px;padding:30px;text-align:center;color:white;font-family:monospace;max-width:400px;">
                <h2 style="color:${diffColors[difficulty]};margin:0 0 15px;">⚔️ ARENA KAMPF</h2>
                <div style="font-size:18px;margin:10px 0;">${enemy.name}</div>
                <div style="color:#aaa;margin:5px 0;">Level ${enemy.level} | ❤️ ${enemy.hp} HP</div>
                <div style="color:${diffColors[difficulty]};margin:5px 0;font-weight:bold;">${diffNames[difficulty]}</div>
                <div style="margin-top:20px;display:flex;gap:15px;justify-content:center;">
                    <button id="arena-confirm-yes" style="background:${diffColors[difficulty]};color:${difficulty === 'normal' ? 'black' : 'white'};border:none;padding:12px 30px;border-radius:8px;font-size:16px;cursor:pointer;font-weight:bold;">KAEMPFEN!</button>
                    <button id="arena-confirm-no" style="background:#333;color:white;border:1px solid #666;padding:12px 30px;border-radius:8px;font-size:16px;cursor:pointer;">Abbrechen</button>
                </div>
            </div>
        `;
        document.body.appendChild(confirmDiv);

        document.getElementById('arena-confirm-no').onclick = () => {
            confirmDiv.remove();
        };

        document.getElementById('arena-confirm-yes').onclick = () => {
            confirmDiv.remove();
            closeArena();

            if (window.showNotification) {
                window.showNotification(`⚔️ Kampf gegen ${enemy.name}!`, 'info');
            }

            // Start 3D Combat
            if (window.Real3DCombat && window.Real3DCombat.startCombat) {
                const scene = window.getScene ? window.getScene() : (window.scene || null);
                const playerPos = window.character?.position || { x: 4800, y: 0, z: 4800 };

                if (scene) {
                    window.Real3DCombat.startCombat([{
                        id: enemy.id,
                        name: enemy.name,
                        level: enemy.level,
                        hp: enemy.hp,
                        maxHp: enemy.hp,
                        type: enemyId
                    }], scene, playerPos);
                } else {
                    console.warn('Scene not available, using fallback combat');
                    startFallbackCombat(enemy);
                }
            } else {
                console.warn('Real3DCombat not available, using fallback');
                startFallbackCombat(enemy);
            }
        };
    };

    function startFallbackCombat(enemy) {
        console.warn('Real3DCombat nicht verfügbar!');
    }

    // Initialize on load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            console.log('✅ Simple Arena System loaded');
        });
    } else {
        console.log('✅ Simple Arena System loaded');
    }

})();
