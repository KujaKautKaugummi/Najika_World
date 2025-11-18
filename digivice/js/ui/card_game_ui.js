/**
 * Card Game UI - Najika World
 * Hybrid Triple Triad + Hearthstone System
 *
 * Uses Backend APIs:
 * - /api/cards - Card management
 * - /api/decks - Deck building
 * - /api/matches - Match system
 * - /api/rankings - ELO rankings
 */

class CardGameUI {
    constructor() {
        this.apiBase = {
            cards: '/api/cards',
            decks: '/api/decks',
            matches: '/api/matches',
            rankings: '/api/rankings'
        };

        this.playerId = 1; // TODO: Get from session
        this.currentMatch = null;
        this.selectedDeck = null;
        this.board = Array(9).fill(null); // 3x3 Triple Triad board

        this.createUI();
    }

    createUI() {
        this.modal = document.createElement('div');
        this.modal.id = 'card-game-modal';
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
                        🃏 Card Game
                        <span style="font-size: 14px; color: #888; margin-left: 10px;">Triple Triad + Hearthstone</span>
                    </h2>
                    <button onclick="window.cardGameUI.hide()" style="
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
                    <button onclick="window.cardGameUI.showTab('collection')" id="tab-collection" class="card-tab active" style="
                        background: linear-gradient(135deg, #667eea, #764ba2);
                        border: none;
                        color: #fff;
                        padding: 12px 24px;
                        border-radius: 8px;
                        cursor: pointer;
                        font-weight: bold;
                    ">📚 Collection</button>
                    <button onclick="window.cardGameUI.showTab('decks')" id="tab-decks" class="card-tab" style="
                        background: rgba(102, 126, 234, 0.3);
                        border: 2px solid #667eea;
                        color: #fff;
                        padding: 12px 24px;
                        border-radius: 8px;
                        cursor: pointer;
                        font-weight: bold;
                    ">🎴 Decks</button>
                    <button onclick="window.cardGameUI.showTab('play')" id="tab-play" class="card-tab" style="
                        background: rgba(102, 126, 234, 0.3);
                        border: 2px solid #667eea;
                        color: #fff;
                        padding: 12px 24px;
                        border-radius: 8px;
                        cursor: pointer;
                        font-weight: bold;
                    ">⚔️ Play</button>
                    <button onclick="window.cardGameUI.showTab('rankings')" id="tab-rankings" class="card-tab" style="
                        background: rgba(102, 126, 234, 0.3);
                        border: 2px solid #667eea;
                        color: #fff;
                        padding: 12px 24px;
                        border-radius: 8px;
                        cursor: pointer;
                        font-weight: bold;
                    ">🏆 Rankings</button>
                </div>

                <!-- Tab Contents -->
                <div id="card-tab-content" style="min-height: 600px;"></div>
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
        document.querySelectorAll('.card-tab').forEach(btn => {
            btn.style.background = 'rgba(102, 126, 234, 0.3)';
        });
        document.getElementById(`tab-${tabName}`).style.background = 'linear-gradient(135deg, #667eea, #764ba2)';

        // Load tab content
        const content = document.getElementById('card-tab-content');
        content.innerHTML = '<div style="color: #fff; text-align: center; padding: 40px;">Loading...</div>';

        switch(tabName) {
            case 'collection':
                await this.showCollection();
                break;
            case 'decks':
                await this.showDecks();
                break;
            case 'play':
                await this.showPlay();
                break;
            case 'rankings':
                await this.showRankings();
                break;
        }
    }

    async showCollection() {
        try {
            const response = await fetch(`${this.apiBase.cards}/collection/${this.playerId}`);
            const data = await response.json();

            const content = document.getElementById('card-tab-content');

            if (!data.collection || data.collection.length === 0) {
                content.innerHTML = `
                    <div style="text-align: center; color: #888; padding: 40px;">
                        <p style="font-size: 24px; margin-bottom: 20px;">📦 No cards yet!</p>
                        <p>Play matches to earn cards</p>
                    </div>
                `;
                return;
            }

            let html = '<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 15px;">';

            data.collection.forEach(entry => {
                const card = entry.card;
                const rarityColors = {
                    common: '#95a5a6',
                    uncommon: '#2ecc71',
                    rare: '#3498db',
                    epic: '#9b59b6',
                    legendary: '#f39c12'
                };

                html += `
                    <div style="
                        background: linear-gradient(135deg, rgba(0,0,0,0.8), rgba(0,0,0,0.6));
                        border: 2px solid ${rarityColors[card.rarity] || '#666'};
                        border-radius: 10px;
                        padding: 15px;
                        color: #fff;
                        position: relative;
                    ">
                        <!-- Card Name -->
                        <div style="font-weight: bold; font-size: 16px; margin-bottom: 10px; color: ${rarityColors[card.rarity]};">
                            ${card.name}
                        </div>

                        <!-- Triple Triad Values -->
                        <div style="position: relative; height: 100px; margin: 10px 0;">
                            <div style="position: absolute; top: 0; left: 50%; transform: translateX(-50%);
                                background: #2c3e50; padding: 3px 8px; border-radius: 5px; font-weight: bold;">
                                ${card.triad_values.top}
                            </div>
                            <div style="position: absolute; top: 50%; right: 0; transform: translateY(-50%);
                                background: #2c3e50; padding: 3px 8px; border-radius: 5px; font-weight: bold;">
                                ${card.triad_values.right}
                            </div>
                            <div style="position: absolute; bottom: 0; left: 50%; transform: translateX(-50%);
                                background: #2c3e50; padding: 3px 8px; border-radius: 5px; font-weight: bold;">
                                ${card.triad_values.bottom}
                            </div>
                            <div style="position: absolute; top: 50%; left: 0; transform: translateY(-50%);
                                background: #2c3e50; padding: 3px 8px; border-radius: 5px; font-weight: bold;">
                                ${card.triad_values.left}
                            </div>
                        </div>

                        <!-- Hearthstone Stats -->
                        <div style="display: flex; justify-content: space-around; margin: 10px 0; padding: 8px; background: rgba(102, 126, 234, 0.2); border-radius: 5px;">
                            <span title="Mana">💎 ${card.hearthstone_stats.mana}</span>
                            <span title="Attack">⚔️ ${card.hearthstone_stats.attack}</span>
                            <span title="Health">❤️ ${card.hearthstone_stats.health}</span>
                        </div>

                        <!-- Rarity & Copies -->
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px;">
                            <span style="font-size: 12px; color: ${rarityColors[card.rarity]}; text-transform: uppercase;">
                                ${card.rarity}
                            </span>
                            <span style="background: rgba(231, 76, 60, 0.3); padding: 3px 8px; border-radius: 5px; font-size: 12px;">
                                x${entry.collection.copies_owned}
                            </span>
                        </div>

                        <!-- Effect -->
                        ${card.effect && card.effect.description ? `
                            <div style="margin-top: 10px; padding: 8px; background: rgba(155, 89, 182, 0.2); border-radius: 5px; font-size: 12px; line-height: 1.4;">
                                <strong>${card.effect.type}:</strong> ${card.effect.description}
                            </div>
                        ` : ''}
                    </div>
                `;
            });

            html += '</div>';
            content.innerHTML = html;

        } catch (error) {
            console.error('Failed to load collection:', error);
            document.getElementById('card-tab-content').innerHTML = `
                <div style="color: #e74c3c; text-align: center; padding: 40px;">
                    ❌ Failed to load collection
                </div>
            `;
        }
    }

    async showDecks() {
        const content = document.getElementById('card-tab-content');
        content.innerHTML = `
            <div style="text-align: center; color: #888; padding: 40px;">
                <p style="font-size: 24px; margin-bottom: 20px;">🎴 Deck Builder</p>
                <p>Coming soon! Build your 30-card deck here.</p>
            </div>
        `;
    }

    async showPlay() {
        const content = document.getElementById('card-tab-content');
        content.innerHTML = `
            <div style="text-align: center; color: #fff; padding: 40px;">
                <h3 style="margin-bottom: 30px;">⚔️ Select Game Mode</h3>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; max-width: 900px; margin: 0 auto;">
                    <button onclick="window.cardGameUI.startMatch('triad')" style="
                        background: linear-gradient(135deg, #667eea, #764ba2);
                        border: none;
                        color: #fff;
                        padding: 40px 20px;
                        border-radius: 10px;
                        cursor: pointer;
                        font-size: 18px;
                        font-weight: bold;
                    ">
                        <div style="font-size: 48px; margin-bottom: 10px;">🎴</div>
                        Triple Triad<br/>
                        <span style="font-size: 12px; font-weight: normal;">Board Control</span>
                    </button>

                    <button onclick="window.cardGameUI.startMatch('hearthstone')" style="
                        background: linear-gradient(135deg, #f39c12, #e67e22);
                        border: none;
                        color: #fff;
                        padding: 40px 20px;
                        border-radius: 10px;
                        cursor: pointer;
                        font-size: 18px;
                        font-weight: bold;
                    ">
                        <div style="font-size: 48px; margin-bottom: 10px;">⚔️</div>
                        Hearthstone<br/>
                        <span style="font-size: 12px; font-weight: normal;">Hero Combat</span>
                    </button>

                    <button onclick="window.cardGameUI.startMatch('hybrid')" style="
                        background: linear-gradient(135deg, #e74c3c, #c0392b);
                        border: none;
                        color: #fff;
                        padding: 40px 20px;
                        border-radius: 10px;
                        cursor: pointer;
                        font-size: 18px;
                        font-weight: bold;
                    ">
                        <div style="font-size: 48px; margin-bottom: 10px;">🔥</div>
                        Hybrid Mode<br/>
                        <span style="font-size: 12px; font-weight: normal;">Ultimate Challenge</span>
                    </button>
                </div>
            </div>
        `;
    }

    async showRankings() {
        try {
            const response = await fetch(`${this.apiBase.rankings}/leaderboard?limit=50`);
            const data = await response.json();

            const content = document.getElementById('card-tab-content');

            if (!data.leaderboard || data.leaderboard.length === 0) {
                content.innerHTML = `
                    <div style="text-align: center; color: #888; padding: 40px;">
                        <p style="font-size: 24px; margin-bottom: 20px;">🏆 No rankings yet</p>
                        <p>Be the first to play ranked matches!</p>
                    </div>
                `;
                return;
            }

            const tierColors = {
                legend: '#f39c12',
                diamond: '#3498db',
                platinum: '#95a5a6',
                gold: '#f1c40f',
                silver: '#bdc3c7',
                bronze: '#cd7f32'
            };

            let html = '<div style="max-width: 800px; margin: 0 auto;">';
            html += '<h3 style="color: #fff; text-align: center; margin-bottom: 20px;">🏆 Top Players</h3>';

            data.leaderboard.forEach((player, index) => {
                html += `
                    <div style="
                        background: ${index < 3 ? 'linear-gradient(135deg, rgba(241, 196, 15, 0.2), rgba(243, 156, 18, 0.2))' : 'rgba(0,0,0,0.5)'};
                        border: 2px solid ${tierColors[player.rank_tier] || '#666'};
                        border-radius: 10px;
                        padding: 15px;
                        margin-bottom: 10px;
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        color: #fff;
                    ">
                        <div style="display: flex; align-items: center; gap: 15px;">
                            <div style="font-size: 24px; font-weight: bold; width: 40px; text-align: center;">
                                ${index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : `#${index + 1}`}
                            </div>
                            <div>
                                <div style="font-weight: bold;">Player ${player.player_id}</div>
                                <div style="font-size: 12px; color: #888;">ELO: ${player.elo_rating}</div>
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div style="
                                background: ${tierColors[player.rank_tier]};
                                color: #000;
                                padding: 5px 15px;
                                border-radius: 5px;
                                font-weight: bold;
                                text-transform: uppercase;
                                font-size: 14px;
                            ">${player.rank_tier}</div>
                            <div style="font-size: 12px; color: #888; margin-top: 5px;">
                                ${player.ranked_wins}W - ${player.ranked_losses}L
                            </div>
                        </div>
                    </div>
                `;
            });

            html += '</div>';
            content.innerHTML = html;

        } catch (error) {
            console.error('Failed to load rankings:', error);
            document.getElementById('card-tab-content').innerHTML = `
                <div style="color: #e74c3c; text-align: center; padding: 40px;">
                    ❌ Failed to load rankings
                </div>
            `;
        }
    }

    async startMatch(gameMode) {
        alert(`Starting ${gameMode} match!\n\nFull game logic coming soon.\n\nFor now, check your collection and rankings!`);

        // TODO: Implement full match logic with:
        // - Deck selection
        // - Board rendering (3x3 for Triple Triad)
        // - Turn-based gameplay
        // - Capture mechanics
        // - Victory/defeat screens
    }
}

// Auto-initialize
if (typeof window !== 'undefined') {
    console.log('🃏 Card Game UI loaded');
}
