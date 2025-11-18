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
            dice: '/api/dice',
            duel: '/api/dice-duel'
        };

        this.playerId = 1; // TODO: Get from session
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
        alert(`Starting Dice Duel!\n\nFull game logic coming soon.\n\nFeatures:\n- Roll dice to summon monsters\n- Move and attack on dungeon board\n- Special abilities\n- 3000 HP Dungeon Master system\n\nFor now, check your dice collection and history!`);

        // TODO: Implement full duel logic with:
        // - Dice pool selection (12 dice)
        // - Dice rolling mechanics
        // - Board rendering (grid-based movement)
        // - Monster summoning
        // - Turn-based combat
        // - HP tracking
        // - Victory/defeat screens
    }
}

// Auto-initialize
if (typeof window !== 'undefined') {
    console.log('🎲 Dice Monsters UI loaded');
}
