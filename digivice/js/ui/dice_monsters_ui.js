/**
 * Dice Monsters UI - Najika World
 * Dungeon Dice Monsters (DDM) System
 * Inspired by Yu-Gi-Oh! Dungeon Dice Monsters
 *
 * Uses Backend APIs:
 * - /api/dice - Dice monster management
 * - /api/dice-duel - Duel system
 */

class DiceMonstersUI {
    constructor() {
        this.apiBase = {
            dice: 'http://localhost:8000/api/dice',
            duel: 'http://localhost:8000/api/dice-duel'
        };

        this.playerId = (typeof getPlayerId === 'function') ? getPlayerId() : 1;
        this.currentDuel = null;
        this.selectedDice = [];

        this.createUI();
    }

    createUI() {
        this.modal = document.createElement('div');
        this.modal.id = 'dice-monsters-modal';
        this.modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.9);
            z-index: 10000;
            display: none;
            overflow-y: auto;
        `;

        this.modal.innerHTML = `
            <div style="max-width: 1400px; margin: 20px auto; padding: 20px;">
                <!-- Header -->
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                    <h2 style="color: #fff; font-size: 32px; margin: 0;">
                        🎲 Dice Monsters
                        <span style="font-size: 14px; color: #888; margin-left: 10px;">Dungeon Dice Monsters</span>
                    </h2>
                    <button onclick="window.diceMonstersUI.hide()" style="
                        background: rgba(231, 76, 60, 0.3);
                        border: 2px solid #e74c3c;
                        color: #fff;
                        padding: 10px 20px;
                        border-radius: 5px;
                        cursor: pointer;
                        font-size: 18px;
                    ">✕ Close</button>
                </div>

                <!-- Tabs -->
                <div style="display: flex; gap: 10px; margin-bottom: 20px; border-bottom: 2px solid #333; padding-bottom: 10px;">
                    <button onclick="window.diceMonstersUI.showTab('collection')" id="dm-tab-collection" class="dm-tab active" style="
                        background: linear-gradient(135deg, #f39c12, #e67e22);
                        border: none;
                        color: #fff;
                        padding: 12px 24px;
                        border-radius: 8px;
                        cursor: pointer;
                        font-weight: bold;
                    ">📦 Collection</button>
                    <button onclick="window.diceMonstersUI.showTab('duel')" id="dm-tab-duel" class="dm-tab" style="
                        background: rgba(243, 156, 18, 0.3);
                        border: 2px solid #f39c12;
                        color: #fff;
                        padding: 12px 24px;
                        border-radius: 8px;
                        cursor: pointer;
                        font-weight: bold;
                    ">⚔️ Duel</button>
                    <button onclick="window.diceMonstersUI.showTab('history')" id="dm-tab-history" class="dm-tab" style="
                        background: rgba(243, 156, 18, 0.3);
                        border: 2px solid #f39c12;
                        color: #fff;
                        padding: 12px 24px;
                        border-radius: 8px;
                        cursor: pointer;
                        font-weight: bold;
                    ">📜 History</button>
                </div>

                <!-- Tab Contents -->
                <div id="dm-tab-content" style="min-height: 600px;"></div>
            </div>
        `;

        document.body.appendChild(this.modal);
    }

    async show() {
        this.modal.style.display = 'block';
        await this.showTab('collection');
    }

    hide() {
        this.modal.style.display = 'none';
    }

    async showTab(tabName) {
        // Update tab buttons
        document.querySelectorAll('.dm-tab').forEach(btn => {
            btn.style.background = 'rgba(243, 156, 18, 0.3)';
        });
        document.getElementById(`dm-tab-${tabName}`).style.background = 'linear-gradient(135deg, #f39c12, #e67e22)';

        // Load tab content
        const content = document.getElementById('dm-tab-content');
        content.innerHTML = '<div style="color: #fff; text-align: center; padding: 40px;">Loading...</div>';

        switch(tabName) {
            case 'collection':
                await this.showCollection();
                break;
            case 'duel':
                await this.showDuel();
                break;
            case 'history':
                await this.showHistory();
                break;
        }
    }

    async showCollection() {
        try {
            const response = await fetch(`${this.apiBase.dice}/collection/${this.playerId}`);
            const data = await response.json();

            const content = document.getElementById('dm-tab-content');

            if (!data.collection || data.collection.length === 0) {
                content.innerHTML = `
                    <div style="text-align: center; color: #888; padding: 40px;">
                        <p style="font-size: 24px; margin-bottom: 20px;">📦 No dice monsters yet!</p>
                        <p>Win duels to earn dice monsters</p>
                    </div>
                `;
                return;
            }

            const elementColors = {
                fire: '#e74c3c',
                water: '#3498db',
                earth: '#27ae60',
                wind: '#95a5a6',
                light: '#f1c40f',
                dark: '#8e44ad'
            };

            const rarityColors = {
                common: '#95a5a6',
                uncommon: '#2ecc71',
                rare: '#3498db',
                epic: '#9b59b6',
                legendary: '#f39c12'
            };

            let html = '<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 20px;">';

            data.collection.forEach(entry => {
                const dice = entry.dice_monster;

                html += `
                    <div style="
                        background: linear-gradient(135deg, rgba(0,0,0,0.8), rgba(0,0,0,0.6));
                        border: 3px solid ${elementColors[dice.element] || '#666'};
                        border-radius: 15px;
                        padding: 20px;
                        color: #fff;
                        position: relative;
                        box-shadow: 0 0 20px ${elementColors[dice.element]}40;
                    ">
                        <!-- Element Badge -->
                        <div style="
                            position: absolute;
                            top: 10px;
                            right: 10px;
                            background: ${elementColors[dice.element]};
                            color: #fff;
                            padding: 5px 12px;
                            border-radius: 20px;
                            font-size: 12px;
                            font-weight: bold;
                            text-transform: uppercase;
                        ">${dice.element}</div>

                        <!-- Dice Name -->
                        <div style="font-weight: bold; font-size: 18px; margin-bottom: 15px; padding-right: 80px; color: ${rarityColors[dice.rarity]};">
                            ${dice.name}
                        </div>

                        <!-- Monster Type -->
                        <div style="font-size: 12px; color: #888; margin-bottom: 15px; text-transform: uppercase;">
                            ${dice.type}
                        </div>

                        <!-- Stats Grid -->
                        <div style="
                            display: grid;
                            grid-template-columns: repeat(3, 1fr);
                            gap: 10px;
                            margin: 15px 0;
                            padding: 15px;
                            background: rgba(255,255,255,0.05);
                            border-radius: 10px;
                        ">
                            <div style="text-align: center;">
                                <div style="font-size: 12px; color: #888; margin-bottom: 5px;">ATK</div>
                                <div style="
                                    background: linear-gradient(135deg, #e74c3c, #c0392b);
                                    padding: 8px;
                                    border-radius: 8px;
                                    font-weight: bold;
                                    font-size: 18px;
                                ">⚔️ ${dice.stats.attack}</div>
                            </div>
                            <div style="text-align: center;">
                                <div style="font-size: 12px; color: #888; margin-bottom: 5px;">DEF</div>
                                <div style="
                                    background: linear-gradient(135deg, #3498db, #2980b9);
                                    padding: 8px;
                                    border-radius: 8px;
                                    font-weight: bold;
                                    font-size: 18px;
                                ">🛡️ ${dice.stats.defense}</div>
                            </div>
                            <div style="text-align: center;">
                                <div style="font-size: 12px; color: #888; margin-bottom: 5px;">MOV</div>
                                <div style="
                                    background: linear-gradient(135deg, #2ecc71, #27ae60);
                                    padding: 8px;
                                    border-radius: 8px;
                                    font-weight: bold;
                                    font-size: 18px;
                                ">🏃 ${dice.stats.movement}</div>
                            </div>
                        </div>

                        <!-- Dice Level & Summon Cost -->
                        <div style="display: flex; justify-content: space-between; margin: 10px 0; padding: 10px; background: rgba(243, 156, 18, 0.2); border-radius: 8px;">
                            <span style="font-size: 14px;">
                                <strong>Level:</strong> ${dice.dice_level}
                            </span>
                            <span style="font-size: 14px;">
                                <strong>Cost:</strong> ${dice.summon.cost} 💎
                            </span>
                        </div>

                        <!-- Ability -->
                        ${dice.ability && dice.ability.name ? `
                            <div style="
                                margin-top: 15px;
                                padding: 12px;
                                background: rgba(155, 89, 182, 0.3);
                                border-left: 4px solid #9b59b6;
                                border-radius: 5px;
                            ">
                                <div style="font-weight: bold; font-size: 14px; margin-bottom: 5px; color: #9b59b6;">
                                    ⚡ ${dice.ability.name}
                                </div>
                                <div style="font-size: 12px; line-height: 1.4; color: #ccc;">
                                    ${dice.ability.description}
                                </div>
                            </div>
                        ` : ''}

                        <!-- Rarity & Copies -->
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(255,255,255,0.1);">
                            <span style="font-size: 12px; color: ${rarityColors[dice.rarity]}; text-transform: uppercase; font-weight: bold;">
                                ⭐ ${dice.rarity}
                            </span>
                            <span style="background: rgba(231, 76, 60, 0.3); padding: 5px 12px; border-radius: 5px; font-size: 13px; font-weight: bold;">
                                x${entry.collection.copies_owned}
                            </span>
                        </div>

                        <!-- Stats -->
                        ${entry.collection.times_summoned > 0 ? `
                            <div style="margin-top: 10px; font-size: 11px; color: #666; text-align: center;">
                                Summoned: ${entry.collection.times_summoned} | Won: ${entry.collection.times_won_with}
                            </div>
                        ` : ''}
                    </div>
                `;
            });

            html += '</div>';
            content.innerHTML = html;

        } catch (error) {
            console.error('Failed to load dice collection:', error);
            document.getElementById('dm-tab-content').innerHTML = `
                <div style="color: #e74c3c; text-align: center; padding: 40px;">
                    ❌ Failed to load collection
                </div>
            `;
        }
    }

    async showDuel() {
        const content = document.getElementById('dm-tab-content');
        content.innerHTML = `
            <div style="text-align: center; color: #fff; padding: 40px;">
                <h3 style="margin-bottom: 30px;">⚔️ Start a Dice Duel</h3>

                <div style="max-width: 600px; margin: 0 auto; background: rgba(0,0,0,0.5); padding: 40px; border-radius: 15px; border: 2px solid #f39c12;">
                    <div style="font-size: 48px; margin-bottom: 20px;">🎲</div>
                    <h4 style="margin-bottom: 20px;">Dice Duel</h4>
                    <p style="color: #888; margin-bottom: 30px; line-height: 1.6;">
                        Roll your dice, summon monsters, and battle on the dungeon board!<br/>
                        Each player starts with 3000 LP (Dungeon Master HP).<br/>
                        Select 12 dice monsters for your pool.
                    </p>

                    <button onclick="window.diceMonstersUI.startDuel()" style="
                        background: linear-gradient(135deg, #f39c12, #e67e22);
                        border: none;
                        color: #fff;
                        padding: 15px 40px;
                        border-radius: 10px;
                        cursor: pointer;
                        font-size: 18px;
                        font-weight: bold;
                        margin-top: 20px;
                    ">🎲 Start Duel</button>
                </div>

                <div style="margin-top: 40px; padding: 20px; background: rgba(155, 89, 182, 0.2); border-radius: 10px; max-width: 800px; margin: 40px auto 0;">
                    <h4 style="margin-bottom: 15px;">📖 How to Play</h4>
                    <div style="text-align: left; color: #ccc; line-height: 1.8;">
                        <p><strong>1. Roll Dice:</strong> Roll your dice to summon monsters</p>
                        <p><strong>2. Move & Attack:</strong> Move monsters on the board and attack</p>
                        <p><strong>3. Use Abilities:</strong> Activate special monster abilities</p>
                        <p><strong>4. Win:</strong> Reduce opponent's Dungeon Master HP to 0</p>
                    </div>
                </div>
            </div>
        `;
    }

    async showHistory() {
        try {
            const response = await fetch(`${this.apiBase.duel}/history/${this.playerId}?limit=20`);
            const data = await response.json();

            const content = document.getElementById('dm-tab-content');

            if (!data.duels || data.duels.length === 0) {
                content.innerHTML = `
                    <div style="text-align: center; color: #888; padding: 40px;">
                        <p style="font-size: 24px; margin-bottom: 20px;">📜 No duel history</p>
                        <p>Start your first duel to see history!</p>
                    </div>
                `;
                return;
            }

            let html = '<div style="max-width: 900px; margin: 0 auto;">';
            html += '<h3 style="color: #fff; text-align: center; margin-bottom: 20px;">📜 Recent Duels</h3>';

            data.duels.forEach(duel => {
                const isWinner = duel.winner_id === this.playerId;
                const isPlayer1 = duel.player1_id === this.playerId;

                html += `
                    <div style="
                        background: ${isWinner ? 'linear-gradient(135deg, rgba(46, 204, 113, 0.2), rgba(39, 174, 96, 0.2))' : 'rgba(0,0,0,0.5)'};
                        border: 2px solid ${isWinner ? '#2ecc71' : '#e74c3c'};
                        border-radius: 10px;
                        padding: 20px;
                        margin-bottom: 15px;
                        color: #fff;
                    ">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                            <div style="font-weight: bold; font-size: 18px;">
                                ${isWinner ? '🏆 Victory' : '💀 Defeat'}
                            </div>
                            <div style="font-size: 14px; color: #888;">
                                ${new Date(duel.started_at).toLocaleDateString()}
                            </div>
                        </div>

                        <div style="display: grid; grid-template-columns: 1fr auto 1fr; gap: 20px; align-items: center;">
                            <div style="text-align: center;">
                                <div style="font-size: 14px; color: #888; margin-bottom: 5px;">You</div>
                                <div style="font-size: 24px; font-weight: bold;">
                                    ${isPlayer1 ? duel.hp.player1_final : duel.hp.player2_final} HP
                                </div>
                            </div>

                            <div style="font-size: 32px; color: #888;">vs</div>

                            <div style="text-align: center;">
                                <div style="font-size: 14px; color: #888; margin-bottom: 5px;">
                                    ${duel.is_vs_npc ? duel.npc_name : 'Opponent'}
                                </div>
                                <div style="font-size: 24px; font-weight: bold;">
                                    ${isPlayer1 ? duel.hp.player2_final : duel.hp.player1_final} HP
                                </div>
                            </div>
                        </div>

                        <div style="
                            margin-top: 15px;
                            padding-top: 15px;
                            border-top: 1px solid rgba(255,255,255,0.1);
                            display: flex;
                            justify-content: space-around;
                            font-size: 13px;
                            color: #888;
                        ">
                            <span>⏱️ ${Math.floor(duel.duration_seconds / 60)}m ${duel.duration_seconds % 60}s</span>
                            <span>🔄 ${duel.turns_played} turns</span>
                            <span>🎲 ${duel.stats.total_dice_rolled} dice rolled</span>
                            <span>👹 ${duel.stats.total_monsters_summoned} monsters</span>
                        </div>

                        ${duel.rewards && (duel.rewards.gold_earned > 0 || duel.rewards.xp_earned > 0) ? `
                            <div style="
                                margin-top: 15px;
                                padding: 10px;
                                background: rgba(241, 196, 15, 0.2);
                                border-radius: 5px;
                                text-align: center;
                                font-size: 14px;
                            ">
                                💰 ${duel.rewards.gold_earned} Gold | ⭐ ${duel.rewards.xp_earned} XP
                                ${duel.rewards.dice_won && duel.rewards.dice_won.length > 0 ? ` | 🎲 +${duel.rewards.dice_won.length} Dice` : ''}
                            </div>
                        ` : ''}
                    </div>
                `;
            });

            html += '</div>';
            content.innerHTML = html;

        } catch (error) {
            console.error('Failed to load duel history:', error);
            document.getElementById('dm-tab-content').innerHTML = `
                <div style="color: #e74c3c; text-align: center; padding: 40px;">
                    ❌ Failed to load duel history
                </div>
            `;
        }
    }

    async startDuel() {
        try {
            // Create duel
            const response = await fetch(`${this.apiBase.duel}/create`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    player_id: this.playerId,
                    is_vs_npc: true,
                    npc_name: 'Dice Master'
                })
            });

            const data = await response.json();
            this.currentDuel = data.duel;

            // Show duel board
            this.showDuelBoard();
        } catch (error) {
            console.error('Failed to start duel:', error);
            if (typeof notify === 'function') notify('❌ Duell konnte nicht gestartet werden', 'error');
        }
    }

    showDuelBoard() {
        const content = document.getElementById('dm-tab-content');

        // Initialize game state
        this.gameState = {
            board: this.createEmptyBoard(),
            player: {
                hp: 30,
                dicePool: 12,
                diceRolled: 0,
                crests: []
            },
            opponent: {
                hp: 30,
                dicePool: 12,
                diceRolled: 0,
                crests: []
            },
            turn: 'player',
            phase: 'roll', // roll, place, summon, move, attack
            selectedDice: null,
            pathPreview: [],
            placedMonsters: [],
            selectedMonster: null
        };

        content.innerHTML = `
            <div style="display: flex; gap: 20px; color: #fff;">
                <!-- Left Panel: Board -->
                <div style="flex: 1;">
                    <!-- HP Displays -->
                    <div style="display: flex; justify-content: space-between; margin-bottom: 15px;">
                        <div style="
                            background: linear-gradient(135deg, #3498db, #2980b9);
                            padding: 15px 30px;
                            border-radius: 10px;
                            border: 3px solid #2c3e50;
                            text-align: center;
                        ">
                            <div style="font-size: 14px; color: #ecf0f1; margin-bottom: 5px;">YOUR DICE LORD</div>
                            <div style="font-size: 32px; font-weight: bold;">
                                ❤️ <span id="player-hp">30</span> HP
                            </div>
                        </div>

                        <div style="
                            background: linear-gradient(135deg, #e74c3c, #c0392b);
                            padding: 15px 30px;
                            border-radius: 10px;
                            border: 3px solid #2c3e50;
                            text-align: center;
                        ">
                            <div style="font-size: 14px; color: #ecf0f1; margin-bottom: 5px;">OPPONENT DICE LORD</div>
                            <div style="font-size: 32px; font-weight: bold;">
                                ❤️ <span id="opponent-hp">30</span> HP
                            </div>
                        </div>
                    </div>

                    <!-- 15×15 Grid Board -->
                    <div style="
                        background: #0a0a0a;
                        padding: 20px;
                        border-radius: 15px;
                        border: 3px solid #f39c12;
                        box-shadow: 0 0 30px rgba(243, 156, 18, 0.5);
                    ">
                        <canvas id="ddm-board-canvas" width="600" height="600" style="
                            display: block;
                            cursor: crosshair;
                            background: #1a1a1a;
                            border: 2px solid #333;
                        "></canvas>
                    </div>

                    <!-- Phase Info -->
                    <div id="phase-info" style="
                        margin-top: 15px;
                        padding: 15px;
                        background: rgba(243, 156, 18, 0.3);
                        border-radius: 10px;
                        text-align: center;
                        font-size: 18px;
                        font-weight: bold;
                    ">
                        🎲 Roll Phase - Roll your dice!
                    </div>
                </div>

                <!-- Right Panel: Actions & Info -->
                <div style="width: 350px;">
                    <div style="
                        background: rgba(0,0,0,0.6);
                        padding: 20px;
                        border-radius: 15px;
                        border: 2px solid #f39c12;
                        max-height: 800px;
                        overflow-y: auto;
                    ">
                        <!-- Turn Info -->
                        <div style="text-align: center; margin-bottom: 20px; padding: 15px; background: rgba(243, 156, 18, 0.3); border-radius: 10px;">
                            <div style="font-size: 24px; font-weight: bold; color: #f39c12;" id="turn-display">
                                YOUR TURN
                            </div>
                            <div style="font-size: 14px; color: #ccc; margin-top: 5px;">
                                Dice Pool: <span id="dice-pool">12</span>
                            </div>
                        </div>

                        <!-- Action Buttons -->
                        <div id="action-buttons" style="display: flex; flex-direction: column; gap: 10px; margin-bottom: 20px;">
                            <button onclick="window.diceMonstersUI.rollDice()" style="
                                background: linear-gradient(135deg, #f39c12, #e67e22);
                                border: none;
                                color: white;
                                padding: 15px;
                                border-radius: 10px;
                                cursor: pointer;
                                font-size: 16px;
                                font-weight: bold;
                            ">🎲 Roll Dice</button>

                            <button onclick="window.diceMonstersUI.showSynergyMenu()" style="
                                background: linear-gradient(135deg, #9b59b6, #8e44ad);
                                border: none;
                                color: white;
                                padding: 15px;
                                border-radius: 10px;
                                cursor: pointer;
                                font-size: 16px;
                                font-weight: bold;
                            ">⚡ Synergy Combos</button>

                            <button onclick="window.diceMonstersUI.endTurn()" style="
                                background: linear-gradient(135deg, #95a5a6, #7f8c8d);
                                border: none;
                                color: white;
                                padding: 15px;
                                border-radius: 10px;
                                cursor: pointer;
                                font-size: 16px;
                                font-weight: bold;
                            ">⏭️ End Turn</button>
                        </div>

                        <!-- Synergy Info -->
                        <div style="
                            margin-top: 20px;
                            padding: 15px;
                            background: rgba(155, 89, 182, 0.3);
                            border-radius: 10px;
                            border-left: 4px solid #9b59b6;
                        ">
                            <h4 style="margin: 0 0 10px 0; color: #9b59b6;">⚡ Active Crests</h4>
                            <div id="active-crests" style="font-size: 14px; line-height: 1.6;">
                                No crests active
                            </div>
                        </div>

                        <!-- Monsters on Board -->
                        <div style="
                            margin-top: 20px;
                            padding: 15px;
                            background: rgba(46, 204, 113, 0.3);
                            border-radius: 10px;
                            border-left: 4px solid #2ecc71;
                        ">
                            <h4 style="margin: 0 0 10px 0; color: #2ecc71;">👹 Your Monsters</h4>
                            <div id="player-monsters" style="font-size: 13px; line-height: 1.6;">
                                No monsters summoned
                            </div>
                        </div>

                        <!-- Game Log -->
                        <div style="
                            margin-top: 20px;
                            padding: 15px;
                            background: rgba(0,0,0,0.5);
                            border-radius: 10px;
                            max-height: 200px;
                            overflow-y: auto;
                        ">
                            <h4 style="margin: 0 0 10px 0; color: #f39c12;">📜 Game Log</h4>
                            <div id="game-log" style="font-size: 12px; line-height: 1.6; color: #ccc;">
                                <div>🎮 Duel started!</div>
                                <div>🎲 Your turn - Roll dice to build path</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Initialize canvas
        this.canvas = document.getElementById('ddm-board-canvas');
        this.ctx = this.canvas.getContext('2d');

        // Add event listeners
        this.canvas.addEventListener('click', (e) => this.handleBoardClick(e));
        this.canvas.addEventListener('mousemove', (e) => this.handleBoardHover(e));

        // Initial render
        this.renderBoard();
    }

    createEmptyBoard() {
        const board = [];
        for (let y = 0; y < 15; y++) {
            board[y] = [];
            for (let x = 0; x < 15; x++) {
                board[y][x] = {
                    type: 'empty', // empty, path, monster, dice_lord
                    owner: null, // player, opponent
                    monster: null,
                    crest: null
                };
            }
        }

        // Place Dice Lords
        board[14][7] = { type: 'dice_lord', owner: 'player', monster: null, crest: null };
        board[0][7] = { type: 'dice_lord', owner: 'opponent', monster: null, crest: null };

        return board;
    }

    renderBoard() {
        const ctx = this.ctx;
        const cellSize = 40;

        // Clear canvas
        ctx.fillStyle = '#1a1a1a';
        ctx.fillRect(0, 0, 600, 600);

        // Draw grid
        for (let y = 0; y < 15; y++) {
            for (let x = 0; x < 15; x++) {
                const cell = this.gameState.board[y][x];
                const px = x * cellSize;
                const py = y * cellSize;

                // Cell background
                if (cell.type === 'dice_lord') {
                    ctx.fillStyle = cell.owner === 'player' ? '#3498db' : '#e74c3c';
                } else if (cell.type === 'path') {
                    ctx.fillStyle = cell.owner === 'player' ? '#2ecc71' : '#e67e22';
                } else if (cell.type === 'monster') {
                    ctx.fillStyle = cell.owner === 'player' ? '#27ae60' : '#d35400';
                } else {
                    ctx.fillStyle = '#2a2a2a';
                }

                ctx.fillRect(px, py, cellSize - 2, cellSize - 2);

                // Draw content
                ctx.fillStyle = '#fff';
                ctx.font = '20px Arial';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';

                if (cell.type === 'dice_lord') {
                    ctx.fillText('👑', px + cellSize/2, py + cellSize/2);
                } else if (cell.type === 'monster' && cell.monster) {
                    ctx.fillText('👹', px + cellSize/2, py + cellSize/2);
                } else if (cell.crest) {
                    ctx.font = '16px Arial';
                    ctx.fillText(this.getCrestIcon(cell.crest), px + cellSize/2, py + cellSize/2);
                }

                // Grid lines
                ctx.strokeStyle = '#444';
                ctx.lineWidth = 1;
                ctx.strokeRect(px, py, cellSize, cellSize);
            }
        }

        // Draw path preview
        if (this.gameState.pathPreview.length > 0) {
            ctx.fillStyle = 'rgba(241, 196, 15, 0.5)';
            this.gameState.pathPreview.forEach(pos => {
                const px = pos.x * cellSize;
                const py = pos.y * cellSize;
                ctx.fillRect(px + 5, py + 5, cellSize - 12, cellSize - 12);
            });
        }
    }

    getCrestIcon(crest) {
        const icons = {
            fire: '🔥',
            water: '💧',
            earth: '🌍',
            wind: '💨',
            light: '✨',
            dark: '🌑'
        };
        return icons[crest] || '◆';
    }

    handleBoardClick(e) {
        const rect = this.canvas.getBoundingClientRect();
        const x = Math.floor((e.clientX - rect.left) / 40);
        const y = Math.floor((e.clientY - rect.top) / 40);

        if (x < 0 || x >= 15 || y < 0 || y >= 15) return;

        console.log(`Clicked cell: ${x}, ${y}`);

        // Handle different phases
        if (this.gameState.phase === 'place' && this.gameState.pathPreview.length > 0) {
            this.placePath(x, y);
        } else if (this.gameState.phase === 'move' && this.gameState.selectedMonster) {
            this.moveMonster(x, y);
        }
    }

    handleBoardHover(e) {
        const rect = this.canvas.getBoundingClientRect();
        const x = Math.floor((e.clientX - rect.left) / 40);
        const y = Math.floor((e.clientY - rect.top) / 40);

        if (x < 0 || x >= 15 || y < 0 || y >= 15) return;

        // Show preview for path placement
        if (this.gameState.phase === 'place' && this.gameState.selectedDice) {
            this.updatePathPreview(x, y);
        }
    }

    async rollDice() {
        if (this.gameState.player.dicePool <= 0) {
            this.addLog('❌ No dice left in pool!');
            return;
        }

        // 🎲 3D Dice Animation (if available)
        let actualResults = [];
        if (window.diceSystem3D && window.characterGroup) {
            try {
                this.addLog('🎲 Rolling 3D dice...');
                // Roll 3 dice in 3D scene
                actualResults = await window.diceSystem3D.rollDice(3, window.characterGroup.position);
                this.addLog(`🎲 Rolled: ${actualResults.join(', ')}`);
            } catch (error) {
                console.error('3D Dice failed, using fallback:', error);
                // Fallback to random
                actualResults = [
                    Math.floor(Math.random() * 6) + 1,
                    Math.floor(Math.random() * 6) + 1,
                    Math.floor(Math.random() * 6) + 1
                ];
            }
        } else {
            // Fallback: No 3D dice available
            actualResults = [
                Math.floor(Math.random() * 6) + 1,
                Math.floor(Math.random() * 6) + 1,
                Math.floor(Math.random() * 6) + 1
            ];
        }

        // Roll dice (simulate)
        const diceResult = {
            faces: this.generateDiceFaces(),
            crest: this.getRandomCrest(),
            diceValues: actualResults // Store 3D dice results
        };

        this.gameState.selectedDice = diceResult;
        this.gameState.player.dicePool--;
        this.gameState.player.diceRolled++;
        this.gameState.player.crests.push(diceResult.crest);

        document.getElementById('dice-pool').textContent = this.gameState.player.dicePool;

        this.addLog(`🎲 Rolled dice! Crest: ${this.getCrestIcon(diceResult.crest)}`);
        this.addLog(`📦 Path: ${diceResult.faces.length} squares`);

        // Change to place phase
        this.gameState.phase = 'place';
        this.updatePhaseInfo('📍 Place Phase - Click on board to place path');
        this.updateActiveCrestsDisplay();
    }

    generateDiceFaces() {
        // Each dice unfolds into 6 squares
        return [
            { direction: 'up' },
            { direction: 'right' },
            { direction: 'down' },
            { direction: 'left' },
            { direction: 'up' },
            { direction: 'right' }
        ];
    }

    getRandomCrest() {
        const crests = ['fire', 'water', 'earth', 'wind', 'light', 'dark'];
        return crests[Math.floor(Math.random() * crests.length)];
    }

    updatePathPreview(startX, startY) {
        if (!this.gameState.selectedDice) return;

        const preview = [];
        let x = startX;
        let y = startY;

        // Build path from dice faces
        this.gameState.selectedDice.faces.forEach((face, i) => {
            if (x >= 0 && x < 15 && y >= 0 && y < 15) {
                preview.push({ x, y });

                // Move to next square based on direction
                switch (face.direction) {
                    case 'up': y--; break;
                    case 'down': y++; break;
                    case 'left': x--; break;
                    case 'right': x++; break;
                }
            }
        });

        this.gameState.pathPreview = preview;
        this.renderBoard();
    }

    placePath(startX, startY) {
        if (!this.gameState.selectedDice || this.gameState.pathPreview.length === 0) return;

        // Place path on board
        this.gameState.pathPreview.forEach(pos => {
            if (this.gameState.board[pos.y][pos.x].type === 'empty') {
                this.gameState.board[pos.y][pos.x] = {
                    type: 'path',
                    owner: 'player',
                    monster: null,
                    crest: this.gameState.selectedDice.crest
                };
            }
        });

        this.addLog(`✅ Path placed! (${this.gameState.pathPreview.length} squares)`);

        // Clear preview and dice
        this.gameState.pathPreview = [];
        this.gameState.selectedDice = null;
        this.gameState.phase = 'roll';
        this.updatePhaseInfo('🎲 Roll Phase - Roll your dice!');

        this.renderBoard();
    }

    showSynergyMenu() {
        const crests = this.gameState.player.crests;
        const crestCounts = {};
        crests.forEach(c => crestCounts[c] = (crestCounts[c] || 0) + 1);

        let html = `
            <div style="
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: linear-gradient(135deg, #2c3e50, #34495e);
                padding: 30px;
                border-radius: 15px;
                border: 3px solid #9b59b6;
                box-shadow: 0 0 50px rgba(155, 89, 182, 0.8);
                z-index: 20000;
                max-width: 600px;
                max-height: 80vh;
                overflow-y: auto;
                color: white;
            ">
                <h2 style="margin: 0 0 20px 0; color: #9b59b6; text-align: center;">⚡ Synergy Combos</h2>

                <div style="margin-bottom: 20px; padding: 15px; background: rgba(0,0,0,0.3); border-radius: 10px;">
                    <h4 style="margin: 0 0 10px 0;">🎲 Your Crests:</h4>
                    ${Object.entries(crestCounts).map(([crest, count]) =>
                        `<span style="display: inline-block; margin: 5px; padding: 8px 15px; background: rgba(243,156,18,0.3); border-radius: 20px;">
                            ${this.getCrestIcon(crest)} x${count}
                        </span>`
                    ).join('')}
                </div>

                <h4 style="margin: 20px 0 15px 0; border-bottom: 2px solid #9b59b6; padding-bottom: 10px;">
                    📖 Available Combos (2 Crests Required)
                </h4>

                ${this.renderSynergyCombos(crestCounts)}

                <button onclick="this.parentElement.remove()" style="
                    width: 100%;
                    margin-top: 20px;
                    background: linear-gradient(135deg, #95a5a6, #7f8c8d);
                    border: none;
                    color: white;
                    padding: 12px;
                    border-radius: 10px;
                    cursor: pointer;
                    font-size: 16px;
                    font-weight: bold;
                ">Close</button>
            </div>
        `;

        const overlay = document.createElement('div');
        overlay.innerHTML = html;
        document.body.appendChild(overlay);
    }

    renderSynergyCombos(crestCounts) {
        const combos = [
            { crests: ['fire', 'fire'], name: 'Rush Summon', effect: 'Summon monster instantly without movement cost', icon: '🔥🔥' },
            { crests: ['water', 'water'], name: 'Twin Summon', effect: 'Summon 2 copies of same monster', icon: '💧💧' },
            { crests: ['earth', 'earth'], name: 'Fortress', effect: 'Monster gains +2 DEF and cannot be moved', icon: '🌍🌍' },
            { crests: ['wind', 'wind'], name: 'Swift Strike', effect: 'Monster can attack twice this turn', icon: '💨💨' },
            { crests: ['light', 'light'], name: 'Holy Barrier', effect: 'Negate next attack against your Dice Lord', icon: '✨✨' },
            { crests: ['dark', 'dark'], name: 'Shadow Drain', effect: 'Heal 3 HP when monster destroys opponent monster', icon: '🌑🌑' },
            { crests: ['fire', 'water'], name: 'Steam Blast', effect: 'Deal 2 damage to all adjacent enemies', icon: '🔥💧' },
            { crests: ['fire', 'wind'], name: 'Inferno Storm', effect: 'Monster gains +3 ATK this turn', icon: '🔥💨' },
            { crests: ['water', 'earth'], name: 'Tidal Wave', effect: 'Push all enemy monsters 2 squares away', icon: '💧🌍' },
            { crests: ['earth', 'wind'], name: 'Earthquake', effect: 'Destroy 3 random opponent path squares', icon: '🌍💨' },
            { crests: ['light', 'dark'], name: 'Twilight Merge', effect: 'Sacrifice monster to deal damage = ATK to enemy Dice Lord', icon: '✨🌑' },
            { crests: ['light', 'fire'], name: 'Divine Flame', effect: 'Monster becomes immune to destruction this turn', icon: '✨🔥' }
        ];

        return combos.map(combo => {
            const canUse = combo.crests.every(c => (crestCounts[c] || 0) >= combo.crests.filter(x => x === c).length);

            return `
                <div style="
                    background: ${canUse ? 'rgba(155,89,182,0.3)' : 'rgba(50,50,50,0.3)'};
                    border: 2px solid ${canUse ? '#9b59b6' : '#555'};
                    border-radius: 10px;
                    padding: 15px;
                    margin-bottom: 12px;
                    ${canUse ? 'cursor: pointer;' : 'opacity: 0.5;'}
                " ${canUse ? `onclick="window.diceMonstersUI.useSynergy('${combo.name}')"` : ''}>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <div style="font-weight: bold; font-size: 16px;">${combo.icon} ${combo.name}</div>
                        ${canUse ? '<div style="color: #2ecc71; font-weight: bold;">✓ Available</div>' : '<div style="color: #e74c3c;">✗ Locked</div>'}
                    </div>
                    <div style="font-size: 13px; color: #ccc; line-height: 1.5;">
                        ${combo.effect}
                    </div>
                    <div style="font-size: 12px; color: #888; margin-top: 8px;">
                        Requires: ${combo.crests.map(c => this.getCrestIcon(c)).join(' ')}
                    </div>
                </div>
            `;
        }).join('');
    }

    useSynergy(comboName) {
        this.addLog(`⚡ Used ${comboName}!`);
        if (typeof notify === 'function') notify(`⚡ Synergie aktiviert: ${comboName}!`, 'success');

        // Remove the combo menu
        document.querySelectorAll('div').forEach(el => {
            if (el.textContent.includes('Synergy Combos') && el.style.position === 'fixed') {
                el.remove();
            }
        });
    }

    moveMonster(x, y) {
        if (!this.gameState || !this.gameState.board) return;

        // Finde das ausgewählte Monster auf dem Board
        const selectedMonster = this.gameState.selectedMonster;
        if (!selectedMonster) {
            this.addLog('⚠️ Kein Monster ausgewählt!');
            return;
        }

        // Prüfe ob Zielfeld frei ist
        if (this.gameState.board[y] && this.gameState.board[y][x]) {
            this.addLog('⚠️ Feld besetzt!');
            return;
        }

        // Prüfe Reichweite (max 2 Felder Manhattan-Distanz)
        const dist = Math.abs(x - selectedMonster.x) + Math.abs(y - selectedMonster.y);
        if (dist > 2) {
            this.addLog('⚠️ Zu weit! (Max 2 Felder)');
            return;
        }

        // Bewege Monster
        if (this.gameState.board[selectedMonster.y]) {
            this.gameState.board[selectedMonster.y][selectedMonster.x] = null;
        }
        if (!this.gameState.board[y]) this.gameState.board[y] = {};
        this.gameState.board[y][x] = selectedMonster.monster;
        selectedMonster.x = x;
        selectedMonster.y = y;

        this.addLog(`👹 ${selectedMonster.monster?.name || 'Monster'} → (${x}, ${y})`);
        this.gameState.selectedMonster = null;
    }

    endTurn() {
        this.addLog('⏭️ Turn ended');
        this.gameState.turn = 'opponent';
        document.getElementById('turn-display').textContent = 'OPPONENT TURN';

        // Simulate opponent turn
        setTimeout(() => {
            this.addLog('🤖 Opponent turn...');
            setTimeout(() => {
                this.gameState.turn = 'player';
                document.getElementById('turn-display').textContent = 'YOUR TURN';
                this.addLog('🎲 Your turn!');
            }, 2000);
        }, 1000);
    }

    updatePhaseInfo(text) {
        const phaseInfo = document.getElementById('phase-info');
        if (phaseInfo) {
            phaseInfo.textContent = text;
        }
    }

    updateActiveCrestsDisplay() {
        const crestsDiv = document.getElementById('active-crests');
        if (!crestsDiv) return;

        const crests = this.gameState.player.crests;
        if (crests.length === 0) {
            crestsDiv.textContent = 'No crests active';
            return;
        }

        const crestCounts = {};
        crests.forEach(c => crestCounts[c] = (crestCounts[c] || 0) + 1);

        crestsDiv.innerHTML = Object.entries(crestCounts)
            .map(([crest, count]) => `${this.getCrestIcon(crest)} ${crest}: x${count}`)
            .join('<br>');
    }

    addLog(message) {
        const log = document.getElementById('game-log');
        if (!log) return;

        const entry = document.createElement('div');
        entry.textContent = message;
        entry.style.marginBottom = '5px';
        log.insertBefore(entry, log.firstChild);

        // Keep only last 10 entries
        while (log.children.length > 10) {
            log.removeChild(log.lastChild);
        }
    }
}

// Auto-initialize
if (typeof window !== 'undefined') {
    console.log('🎲 Dice Monsters UI loaded');
}
