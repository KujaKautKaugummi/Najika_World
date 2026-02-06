/**
 * RPG BATTLE UI
 * Turn-Based Combat System UI für najika_battle.py Backend
 * Verbindet mit BattleAPI (battle_api.js)
 */

class RPGBattleUI {
    constructor() {
        this.battleAPI = window.battleAPI;
        this.currentStatus = null;
        this.isOpen = false;
        this.overlay = null;
        this.selectedTarget = 0;
        this.animating = false;
        this.battleLog = [];
    }

    /**
     * Öffne Battle UI und starte neuen Kampf
     */
    async open() {
        if (this.isOpen) return;

        console.log('⚔️ Öffne RPG Battle UI...');

        // Starte Battle im Backend
        const status = await this.battleAPI.startBattle();
        if (!status || !status.active) {
            console.error('❌ Konnte Battle nicht starten');
            this.showError('Konnte Battle nicht starten!');
            return;
        }

        this.currentStatus = status;
        this.isOpen = true;
        this.battleLog = status.log || [];
        this.selectedTarget = 0;

        // Erstelle UI
        this.createUI();
        this.updateUI();

        console.log('✅ RPG Battle UI geöffnet');
    }

    /**
     * Erstelle Battle UI DOM
     */
    createUI() {
        // Erstelle Overlay
        this.overlay = document.createElement('div');
        this.overlay.id = 'rpg-battle-overlay';
        this.overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.95);
            z-index: 10000;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            font-family: 'Courier New', monospace;
            color: #fff;
        `;

        // Battle Container
        const container = document.createElement('div');
        container.id = 'rpg-battle-container';
        container.style.cssText = `
            width: 90%;
            max-width: 1200px;
            height: 80%;
            display: flex;
            flex-direction: column;
            gap: 20px;
        `;

        container.innerHTML = `
            <!-- Header -->
            <div id="battle-header" style="
                background: linear-gradient(135deg, #ff0000 0%, #880000 100%);
                padding: 15px;
                border-radius: 10px;
                text-align: center;
                box-shadow: 0 4px 10px rgba(255, 0, 0, 0.5);
            ">
                <h2 style="margin: 0; font-size: 28px;">⚔️ RPG BATTLE ⚔️</h2>
                <div id="wave-info" style="font-size: 14px; margin-top: 5px; color: #ffcccc;">Wave 1</div>
            </div>

            <!-- Main Battle Area -->
            <div style="display: flex; gap: 20px; flex: 1; overflow: hidden;">
                <!-- Left: Player Stats + Actions -->
                <div style="flex: 1; display: flex; flex-direction: column; gap: 15px;">
                    <!-- Player Stats -->
                    <div id="player-stats" style="
                        background: rgba(76, 175, 80, 0.2);
                        border: 2px solid #4CAF50;
                        border-radius: 10px;
                        padding: 15px;
                    ">
                        <div style="font-size: 18px; font-weight: bold; margin-bottom: 10px; color: #4CAF50;">
                            🧙 NAJIKA
                        </div>
                        <div id="player-hp-bar" style="margin-bottom: 10px;"></div>
                        <div id="player-mp-bar" style="margin-bottom: 10px;"></div>
                        <div id="player-stats-details" style="font-size: 12px; color: #aaa;"></div>
                    </div>

                    <!-- Action Buttons -->
                    <div id="action-buttons" style="
                        background: rgba(255, 255, 255, 0.1);
                        border: 2px solid #666;
                        border-radius: 10px;
                        padding: 15px;
                        flex: 1;
                    ">
                        <div style="font-size: 14px; font-weight: bold; margin-bottom: 10px; color: #FFD700;">
                            AKTIONEN
                        </div>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                            <button id="action-attack" class="battle-action-btn" style="
                                background: #f44336;
                                border: none;
                                padding: 15px;
                                border-radius: 8px;
                                color: white;
                                font-size: 16px;
                                font-weight: bold;
                                cursor: pointer;
                                transition: all 0.2s;
                            ">⚔️ Angriff</button>
                            <button id="action-skill" class="battle-action-btn" style="
                                background: #2196F3;
                                border: none;
                                padding: 15px;
                                border-radius: 8px;
                                color: white;
                                font-size: 16px;
                                font-weight: bold;
                                cursor: pointer;
                                transition: all 0.2s;
                            ">✨ Skill</button>
                            <button id="action-defend" class="battle-action-btn" style="
                                background: #4CAF50;
                                border: none;
                                padding: 15px;
                                border-radius: 8px;
                                color: white;
                                font-size: 16px;
                                font-weight: bold;
                                cursor: pointer;
                                transition: all 0.2s;
                            ">🛡️ Verteidigen</button>
                            <button id="action-item" class="battle-action-btn" style="
                                background: #FF9800;
                                border: none;
                                padding: 15px;
                                border-radius: 8px;
                                color: white;
                                font-size: 16px;
                                font-weight: bold;
                                cursor: pointer;
                                transition: all 0.2s;
                            ">🎒 Item</button>
                        </div>
                        <button id="action-flee" class="battle-action-btn" style="
                            background: #9E9E9E;
                            border: none;
                            padding: 12px;
                            border-radius: 8px;
                            color: white;
                            font-size: 14px;
                            font-weight: bold;
                            cursor: pointer;
                            margin-top: 10px;
                            width: 100%;
                            transition: all 0.2s;
                        ">🏃 Fliehen</button>
                    </div>
                </div>

                <!-- Right: Enemies + Battle Log -->
                <div style="flex: 1; display: flex; flex-direction: column; gap: 15px;">
                    <!-- Enemies -->
                    <div id="enemies-container" style="
                        background: rgba(255, 68, 68, 0.2);
                        border: 2px solid #f44336;
                        border-radius: 10px;
                        padding: 15px;
                        min-height: 200px;
                    ">
                        <div style="font-size: 18px; font-weight: bold; margin-bottom: 10px; color: #f44336;">
                            👾 GEGNER
                        </div>
                        <div id="enemies-list"></div>
                    </div>

                    <!-- Battle Log -->
                    <div id="battle-log" style="
                        background: rgba(0, 0, 0, 0.5);
                        border: 2px solid #444;
                        border-radius: 10px;
                        padding: 15px;
                        flex: 1;
                        overflow-y: auto;
                        font-size: 13px;
                        line-height: 1.6;
                    ">
                        <div style="font-size: 14px; font-weight: bold; margin-bottom: 10px; color: #FFD700;">
                            📜 KAMPFLOG
                        </div>
                        <div id="log-entries"></div>
                    </div>
                </div>
            </div>
        `;

        this.overlay.appendChild(container);
        document.body.appendChild(this.overlay);

        // Event Listeners
        this.setupEventListeners();

        // Hover Effekte für Buttons
        const style = document.createElement('style');
        style.textContent = `
            .battle-action-btn:hover {
                transform: scale(1.05);
                box-shadow: 0 4px 12px rgba(255, 255, 255, 0.3);
            }
            .battle-action-btn:active {
                transform: scale(0.98);
            }
            .battle-action-btn:disabled {
                opacity: 0.5;
                cursor: not-allowed;
            }
            .enemy-card {
                background: rgba(255, 255, 255, 0.1);
                padding: 12px;
                border-radius: 8px;
                margin-bottom: 10px;
                cursor: pointer;
                transition: all 0.2s;
                border: 2px solid transparent;
            }
            .enemy-card:hover {
                background: rgba(255, 255, 255, 0.2);
                border-color: #FFD700;
            }
            .enemy-card.selected {
                border-color: #FFD700;
                box-shadow: 0 0 15px rgba(255, 215, 0, 0.5);
            }
            #log-entries::-webkit-scrollbar {
                width: 8px;
            }
            #log-entries::-webkit-scrollbar-track {
                background: rgba(0, 0, 0, 0.3);
                border-radius: 4px;
            }
            #log-entries::-webkit-scrollbar-thumb {
                background: #666;
                border-radius: 4px;
            }
            #log-entries::-webkit-scrollbar-thumb:hover {
                background: #888;
            }
        `;
        document.head.appendChild(style);
    }

    /**
     * Event Listeners setup
     */
    setupEventListeners() {
        // Action Buttons
        document.getElementById('action-attack').addEventListener('click', () => this.doAction('attack'));
        document.getElementById('action-skill').addEventListener('click', () => this.openSkillMenu());
        document.getElementById('action-defend').addEventListener('click', () => this.doAction('defend'));
        document.getElementById('action-item').addEventListener('click', () => this.openItemMenu());
        document.getElementById('action-flee').addEventListener('click', () => this.doAction('flee'));

        // ESC zum Schließen (nur wenn Battle vorbei)
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.currentStatus && !this.currentStatus.active) {
                this.close();
            }
        });
    }

    /**
     * Update gesamte UI basierend auf currentStatus
     */
    updateUI() {
        if (!this.currentStatus) return;

        // Wave Info
        const waveInfo = document.getElementById('wave-info');
        if (waveInfo) {
            waveInfo.textContent = `Wave ${this.currentStatus.wave || 1} | Turn ${this.currentStatus.turn || 1}`;
        }

        // Player Stats
        this.updatePlayerStats();

        // Enemies
        this.updateEnemies();

        // Battle Log
        this.updateBattleLog();

        // Check Battle End
        if (!this.currentStatus.active) {
            this.showBattleEnd();
        }
    }

    /**
     * Update Player Stats Display
     */
    updatePlayerStats() {
        const player = this.currentStatus.player;
        if (!player) return;

        const hpPercent = (player.hp / player.max_hp) * 100;
        const mpPercent = (player.mp / player.max_mp) * 100;

        const hpColor = hpPercent > 60 ? '#4CAF50' : hpPercent > 30 ? '#FFC107' : '#f44336';
        const mpColor = '#2196F3';

        // HP Bar
        document.getElementById('player-hp-bar').innerHTML = `
            <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 3px;">
                <span>❤️ HP</span>
                <span>${player.hp} / ${player.max_hp}</span>
            </div>
            <div style="background: #222; height: 20px; border-radius: 10px; overflow: hidden;">
                <div style="background: ${hpColor}; height: 100%; width: ${hpPercent}%; transition: width 0.5s;"></div>
            </div>
        `;

        // MP Bar
        document.getElementById('player-mp-bar').innerHTML = `
            <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 3px;">
                <span>💙 MP</span>
                <span>${player.mp} / ${player.max_mp}</span>
            </div>
            <div style="background: #222; height: 16px; border-radius: 8px; overflow: hidden;">
                <div style="background: ${mpColor}; height: 100%; width: ${mpPercent}%; transition: width 0.5s;"></div>
            </div>
        `;

        // Details
        document.getElementById('player-stats-details').innerHTML = `
            ATK: ${player.atk} | DEF: ${player.def} | Level: ${player.level || 1}
            ${player.buffs && player.buffs.length > 0 ? `<br>Buffs: ${player.buffs.join(', ')}` : ''}
        `;
    }

    /**
     * Update Enemies Display
     */
    updateEnemies() {
        const enemies = this.currentStatus.enemies || [];
        const listContainer = document.getElementById('enemies-list');

        if (enemies.length === 0) {
            listContainer.innerHTML = '<div style="color: #666; font-style: italic;">Keine Gegner</div>';
            return;
        }

        listContainer.innerHTML = enemies.map((enemy, index) => {
            const hpPercent = (enemy.hp / enemy.max_hp) * 100;
            const hpColor = hpPercent > 60 ? '#4CAF50' : hpPercent > 30 ? '#FFC107' : '#f44336';
            const isSelected = index === this.selectedTarget;

            return `
                <div class="enemy-card ${isSelected ? 'selected' : ''}" data-index="${index}">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                        <span style="font-weight: bold; font-size: 16px;">${enemy.name}</span>
                        <span style="color: #FFD700;">${enemy.boss ? '👑 BOSS' : ''}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 3px;">
                        <span>❤️ HP</span>
                        <span>${enemy.hp} / ${enemy.max_hp}</span>
                    </div>
                    <div style="background: #222; height: 14px; border-radius: 7px; overflow: hidden;">
                        <div style="background: ${hpColor}; height: 100%; width: ${hpPercent}%; transition: width 0.5s;"></div>
                    </div>
                    <div style="font-size: 11px; color: #aaa; margin-top: 5px;">
                        ATK: ${enemy.atk} | DEF: ${enemy.def}
                    </div>
                </div>
            `;
        }).join('');

        // Click Listener für Enemy Selection
        listContainer.querySelectorAll('.enemy-card').forEach(card => {
            card.addEventListener('click', (e) => {
                const index = parseInt(e.currentTarget.dataset.index);
                this.selectedTarget = index;
                this.updateEnemies(); // Re-render to update selection
            });
        });
    }

    /**
     * Update Battle Log
     */
    updateBattleLog() {
        const logContainer = document.getElementById('log-entries');
        const logMessages = this.currentStatus.log || [];

        // Zeige die letzten 20 Nachrichten
        const recentLogs = logMessages.slice(-20);

        logContainer.innerHTML = recentLogs.map(msg => {
            let color = '#fff';
            if (msg.includes('Schaden') || msg.includes('Damage') || msg.includes('HP')) {
                color = '#ff6b6b';
            } else if (msg.includes('heilt') || msg.includes('heal')) {
                color = '#4CAF50';
            } else if (msg.includes('Wave') || msg.includes('Sieg') || msg.includes('Victory')) {
                color = '#FFD700';
            }

            return `<div style="color: ${color}; margin-bottom: 4px;">▸ ${msg}</div>`;
        }).join('');

        // Auto-scroll to bottom
        logContainer.scrollTop = logContainer.scrollHeight;
    }

    /**
     * Führe Action aus
     */
    async doAction(action, options = {}) {
        if (this.animating) return;

        this.animating = true;
        this.disableButtons();

        // Target Index hinzufügen
        options.targetIndex = this.selectedTarget;

        console.log(`⚔️ Aktion: ${action}`, options);

        // API Call
        const status = await this.battleAPI.executeAction(action, options);

        if (status.error) {
            this.showError(status.error);
            this.animating = false;
            this.enableButtons();
            return;
        }

        this.currentStatus = status;
        this.updateUI();

        this.animating = false;
        this.enableButtons();
    }

    /**
     * Öffne Skill Menu
     */
    async openSkillMenu() {
        const skills = await this.battleAPI.getAvailableSkills();

        if (!skills || skills.length === 0) {
            this.showError('Keine Skills verfügbar!');
            return;
        }

        // Erstelle Skill-Auswahlmenü
        const skillMenu = document.createElement('div');
        skillMenu.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0, 0, 0, 0.95);
            padding: 30px;
            border-radius: 15px;
            z-index: 11000;
            border: 3px solid #2196F3;
            box-shadow: 0 0 30px rgba(33, 150, 243, 0.6);
            max-width: 500px;
        `;

        skillMenu.innerHTML = `
            <h3 style="margin: 0 0 20px 0; color: #2196F3; text-align: center;">✨ SKILLS WÄHLEN</h3>
            <div id="skill-list" style="max-height: 400px; overflow-y: auto; margin-bottom: 20px;">
                ${skills.map(skill => `
                    <div class="skill-item" data-skill="${skill.name}" style="
                        background: rgba(33, 150, 243, 0.2);
                        padding: 15px;
                        border-radius: 8px;
                        margin-bottom: 10px;
                        cursor: pointer;
                        border: 2px solid transparent;
                        transition: all 0.2s;
                    ">
                        <div style="font-weight: bold; font-size: 16px; margin-bottom: 5px;">${skill.name}</div>
                        <div style="font-size: 12px; color: #aaa; margin-bottom: 8px;">${skill.description || 'Kein Skill Effekt'}</div>
                        <div style="font-size: 11px; color: #FFD700;">
                            ${skill.cost ? `💙 MP: ${skill.cost}` : ''}
                            ${skill.damage ? `⚔️ DMG: ${skill.damage}` : ''}
                            ${skill.cooldown ? `⏱️ CD: ${skill.cooldown}` : ''}
                        </div>
                    </div>
                `).join('')}
            </div>
            <button id="skill-cancel" style="
                width: 100%;
                padding: 12px;
                background: #666;
                border: none;
                border-radius: 8px;
                color: white;
                font-size: 14px;
                cursor: pointer;
            ">Abbrechen</button>
        `;

        document.body.appendChild(skillMenu);

        // Hover Effekt
        skillMenu.querySelectorAll('.skill-item').forEach(item => {
            item.addEventListener('mouseenter', (e) => {
                e.target.style.borderColor = '#2196F3';
                e.target.style.background = 'rgba(33, 150, 243, 0.4)';
            });
            item.addEventListener('mouseleave', (e) => {
                e.target.style.borderColor = 'transparent';
                e.target.style.background = 'rgba(33, 150, 243, 0.2)';
            });

            item.addEventListener('click', async (e) => {
                const skillName = e.currentTarget.dataset.skill;
                skillMenu.remove();
                await this.doAction('skill', { skillName });
            });
        });

        document.getElementById('skill-cancel').addEventListener('click', () => {
            skillMenu.remove();
        });
    }

    /**
     * Öffne Item Menu (Placeholder)
     */
    openItemMenu() {
        this.showError('Item-System wird noch implementiert!');
    }

    /**
     * Zeige Battle End Screen
     */
    showBattleEnd() {
        const result = this.currentStatus.result;
        const isVictory = result === 'victory' || result === 'win';

        const endScreen = document.createElement('div');
        endScreen.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: ${isVictory ? 'rgba(76, 175, 80, 0.95)' : 'rgba(244, 67, 54, 0.95)'};
            padding: 50px;
            border-radius: 20px;
            z-index: 11000;
            text-align: center;
            border: 4px solid ${isVictory ? '#4CAF50' : '#f44336'};
            box-shadow: 0 0 40px ${isVictory ? 'rgba(76, 175, 80, 0.8)' : 'rgba(244, 67, 54, 0.8)'};
        `;

        endScreen.innerHTML = `
            <h2 style="margin: 0 0 20px 0; font-size: 36px;">
                ${isVictory ? '🎉 SIEG!' : '💀 NIEDERLAGE'}
            </h2>
            <div style="font-size: 18px; margin-bottom: 30px;">
                ${isVictory
                    ? `Du hast Wave ${this.currentStatus.wave} überlebt!<br>+${this.currentStatus.rewards?.xp || 0} XP | +${this.currentStatus.rewards?.gold || 0} Gold`
                    : 'Du wurdest besiegt...'}
            </div>
            <button id="battle-close-btn" style="
                padding: 15px 40px;
                background: white;
                border: none;
                border-radius: 10px;
                color: #333;
                font-size: 18px;
                font-weight: bold;
                cursor: pointer;
            ">Schließen</button>
        `;

        this.overlay.appendChild(endScreen);

        document.getElementById('battle-close-btn').addEventListener('click', () => {
            this.close();
        });
    }

    /**
     * Deaktiviere alle Action Buttons
     */
    disableButtons() {
        document.querySelectorAll('.battle-action-btn').forEach(btn => {
            btn.disabled = true;
        });
    }

    /**
     * Aktiviere alle Action Buttons
     */
    enableButtons() {
        document.querySelectorAll('.battle-action-btn').forEach(btn => {
            btn.disabled = false;
        });
    }

    /**
     * Zeige Error Message
     */
    showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.style.cssText = `
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: #f44336;
            color: white;
            padding: 15px 30px;
            border-radius: 8px;
            z-index: 12000;
            font-size: 16px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
        `;
        errorDiv.textContent = `⚠️ ${message}`;

        document.body.appendChild(errorDiv);

        setTimeout(() => {
            errorDiv.remove();
        }, 3000);
    }

    /**
     * Schließe Battle UI
     */
    async close() {
        if (!this.isOpen) return;

        console.log('🛑 Schließe RPG Battle UI...');

        // Reset Battle im Backend
        await this.battleAPI.resetBattle();

        // Entferne UI
        if (this.overlay) {
            this.overlay.remove();
            this.overlay = null;
        }

        this.isOpen = false;
        this.currentStatus = null;
        this.battleLog = [];

        console.log('✅ RPG Battle UI geschlossen');
    }
}

// Global Instance
window.rpgBattleUI = new RPGBattleUI();
