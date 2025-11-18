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
        this.gameMode = gameMode;

        try {
            // Create match
            const response = await fetch(`${this.apiBase.matches}/create`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    player_id: this.playerId,
                    game_mode: gameMode,
                    is_ranked: false
                })
            });

            const data = await response.json();
            this.currentMatch = data.match;

            // Load player's cards for hand
            await this.loadPlayerHand();

            // Show match board
            this.showMatchBoard();
        } catch (error) {
            console.error('Failed to start match:', error);
            alert('❌ Failed to start match');
        }
    }

    async loadPlayerHand() {
        try {
            const response = await fetch(`${this.apiBase.cards}/collection/${this.playerId}`);
            const data = await response.json();

            // Get 5 random cards for hand (Triple Triad style)
            const allCards = data.collection.map(entry => entry.card);
            this.playerHand = [];
            for (let i = 0; i < 5 && allCards.length > 0; i++) {
                const randomIndex = Math.floor(Math.random() * allCards.length);
                this.playerHand.push(allCards[randomIndex]);
            }

            // Generate opponent hand
            this.opponentHand = [];
            for (let i = 0; i < 5; i++) {
                this.opponentHand.push(this.generateOpponentCard());
            }
        } catch (error) {
            console.error('Failed to load cards:', error);
            this.playerHand = [this.generateSampleCard(), this.generateSampleCard(), this.generateSampleCard(), this.generateSampleCard(), this.generateSampleCard()];
            this.opponentHand = [this.generateOpponentCard(), this.generateOpponentCard(), this.generateOpponentCard(), this.generateOpponentCard(), this.generateOpponentCard()];
        }
    }

    generateSampleCard() {
        return {
            name: 'Sample Card',
            top_value: Math.floor(Math.random() * 10) + 1,
            right_value: Math.floor(Math.random() * 10) + 1,
            bottom_value: Math.floor(Math.random() * 10) + 1,
            left_value: Math.floor(Math.random() * 10) + 1,
            faction: 'Neutral',
            rarity: 'common'
        };
    }

    generateOpponentCard() {
        const names = ['Fire Dragon', 'Ice Wizard', 'Thunder Knight', 'Earth Golem', 'Wind Archer'];
        return {
            name: names[Math.floor(Math.random() * names.length)],
            top_value: Math.floor(Math.random() * 10) + 1,
            right_value: Math.floor(Math.random() * 10) + 1,
            bottom_value: Math.floor(Math.random() * 10) + 1,
            left_value: Math.floor(Math.random() * 10) + 1,
            faction: 'Enemy',
            rarity: 'common'
        };
    }

    showMatchBoard() {
        const content = document.getElementById('tab-content');

        // Initialize game state
        this.gameState = {
            board: Array(9).fill(null), // 3×3 grid (0-8)
            playerScore: 5, // Start with 5 cards
            opponentScore: 5,
            turn: 'player',
            selectedCard: null,
            selectedHandIndex: null,
            gameOver: false
        };

        content.innerHTML = `
            <div style="color: #fff;">
                <!-- Score Display -->
                <div style="display: flex; justify-content: space-between; margin-bottom: 20px; padding: 20px; background: rgba(0,0,0,0.5); border-radius: 15px;">
                    <div style="text-align: center; flex: 1;">
                        <div style="font-size: 18px; color: #3498db; margin-bottom: 10px; font-weight: bold;">YOUR SCORE</div>
                        <div style="font-size: 48px; font-weight: bold; color: #3498db;" id="player-score">5</div>
                    </div>

                    <div style="text-align: center; flex: 1;">
                        <div style="font-size: 16px; color: #888; margin-bottom: 10px;">
                            <span id="turn-indicator" style="color: #f39c12; font-weight: bold;">YOUR TURN</span>
                        </div>
                        <div style="font-size: 14px; color: #ccc;">
                            🃏 Triple Triad
                        </div>
                        <div id="game-status" style="margin-top: 10px; font-size: 14px; color: #f39c12;">
                            Select a card and place it on the board
                        </div>
                    </div>

                    <div style="text-align: center; flex: 1;">
                        <div style="font-size: 18px; color: #e74c3c; margin-bottom: 10px; font-weight: bold;">OPPONENT SCORE</div>
                        <div style="font-size: 48px; font-weight: bold; color: #e74c3c;" id="opponent-score">5</div>
                    </div>
                </div>

                <!-- Main Game Area -->
                <div style="display: flex; gap: 30px; justify-content: center;">
                    <!-- 3×3 Grid Board -->
                    <div style="flex-shrink: 0;">
                        <div style="
                            display: grid;
                            grid-template-columns: repeat(3, 150px);
                            grid-template-rows: repeat(3, 150px);
                            gap: 10px;
                            padding: 20px;
                            background: rgba(0,0,0,0.7);
                            border-radius: 15px;
                            border: 3px solid #667eea;
                            box-shadow: 0 0 30px rgba(102, 126, 234, 0.5);
                        " id="triad-board">
                            ${Array(9).fill(0).map((_, i) => `
                                <div
                                    id="cell-${i}"
                                    onclick="window.cardGameUI.placeCard(${i})"
                                    style="
                                        background: linear-gradient(135deg, rgba(44,62,80,0.8), rgba(52,73,94,0.8));
                                        border: 2px solid #555;
                                        border-radius: 10px;
                                        cursor: pointer;
                                        transition: all 0.3s;
                                        display: flex;
                                        align-items: center;
                                        justify-content: center;
                                        position: relative;
                                    "
                                    onmouseover="this.style.borderColor='#667eea'; this.style.transform='scale(1.05)'"
                                    onmouseout="this.style.borderColor='#555'; this.style.transform='scale(1)'"
                                >
                                    <div style="font-size: 12px; color: #666; position: absolute; top: 5px; left: 5px;">
                                        ${i + 1}
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    </div>

                    <!-- Side Panel -->
                    <div style="flex: 1; max-width: 400px;">
                        <!-- Player Hand -->
                        <div style="
                            background: rgba(0,0,0,0.6);
                            padding: 20px;
                            border-radius: 15px;
                            border: 2px solid #3498db;
                            margin-bottom: 20px;
                        ">
                            <h3 style="margin: 0 0 15px 0; color: #3498db; text-align: center;">🃏 Your Hand</h3>
                            <div id="player-hand" style="display: flex; flex-direction: column; gap: 10px;">
                                <!-- Populated dynamically -->
                            </div>
                        </div>

                        <!-- Game Info -->
                        <div style="
                            background: rgba(0,0,0,0.6);
                            padding: 20px;
                            border-radius: 15px;
                            border: 2px solid #9b59b6;
                        ">
                            <h4 style="margin: 0 0 15px 0; color: #9b59b6;">📖 Triple Triad Rules</h4>
                            <div style="font-size: 13px; line-height: 1.8; color: #ccc;">
                                <p><strong>1.</strong> Players take turns placing cards on the 3×3 board</p>
                                <p><strong>2.</strong> Each card has 4 values (Top, Right, Bottom, Left)</p>
                                <p><strong>3.</strong> When you place a card next to an opponent's card, compare adjacent values</p>
                                <p><strong>4.</strong> If your value is <strong>higher</strong>, you <strong>capture</strong> the opponent's card</p>
                                <p><strong>5.</strong> Captured cards change to your color and add to your score</p>
                                <p><strong>6.</strong> Player with most cards at the end <strong>wins</strong></p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Render initial state
        this.renderPlayerHand();
    }

    renderPlayerHand() {
        const handDiv = document.getElementById('player-hand');
        if (!handDiv) return;

        handDiv.innerHTML = this.playerHand.map((card, index) => `
            <div
                onclick="window.cardGameUI.selectCard(${index})"
                style="
                    background: linear-gradient(135deg, ${this.gameState.selectedHandIndex === index ? '#3498db' : 'rgba(52,73,94,0.8)'}, rgba(44,62,80,0.8));
                    border: 3px solid ${this.gameState.selectedHandIndex === index ? '#f39c12' : '#3498db'};
                    border-radius: 12px;
                    padding: 12px;
                    cursor: pointer;
                    transition: all 0.3s;
                    ${this.gameState.selectedHandIndex === index ? 'box-shadow: 0 0 20px rgba(243,156,18,0.8);' : ''}
                "
                onmouseover="if(${this.gameState.selectedHandIndex !== index}) this.style.borderColor='#5dade2'"
                onmouseout="if(${this.gameState.selectedHandIndex !== index}) this.style.borderColor='#3498db'"
            >
                <div style="font-weight: bold; margin-bottom: 8px; color: #fff; text-align: center;">
                    ${card.name}
                </div>

                <!-- Card Values in Cross Pattern -->
                <div style="position: relative; height: 60px; margin: 10px 0;">
                    <!-- Top -->
                    <div style="position: absolute; top: 0; left: 50%; transform: translateX(-50%);
                        background: #e74c3c; color: white; width: 30px; height: 30px;
                        border-radius: 50%; display: flex; align-items: center; justify-content: center;
                        font-weight: bold; font-size: 16px; border: 2px solid #c0392b;">
                        ${card.top_value}
                    </div>

                    <!-- Center Cross -->
                    <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
                        display: flex; align-items: center; gap: 10px;">
                        <!-- Left -->
                        <div style="background: #3498db; color: white; width: 30px; height: 30px;
                            border-radius: 50%; display: flex; align-items: center; justify-content: center;
                            font-weight: bold; font-size: 16px; border: 2px solid #2980b9;">
                            ${card.left_value}
                        </div>

                        <!-- Right -->
                        <div style="background: #3498db; color: white; width: 30px; height: 30px;
                            border-radius: 50%; display: flex; align-items: center; justify-content: center;
                            font-weight: bold; font-size: 16px; border: 2px solid #2980b9;">
                            ${card.right_value}
                        </div>
                    </div>

                    <!-- Bottom -->
                    <div style="position: absolute; bottom: 0; left: 50%; transform: translateX(-50%);
                        background: #e74c3c; color: white; width: 30px; height: 30px;
                        border-radius: 50%; display: flex; align-items: center; justify-content: center;
                        font-weight: bold; font-size: 16px; border: 2px solid #c0392b;">
                        ${card.bottom_value}
                    </div>
                </div>

                <div style="text-align: center; font-size: 11px; color: #888; margin-top: 5px;">
                    ${card.faction}
                </div>
            </div>
        `).join('');
    }

    selectCard(index) {
        if (this.gameState.turn !== 'player' || this.gameState.gameOver) return;

        this.gameState.selectedHandIndex = index;
        this.gameState.selectedCard = this.playerHand[index];
        this.renderPlayerHand();

        document.getElementById('game-status').textContent = `Selected: ${this.gameState.selectedCard.name} - Click on board to place`;
        document.getElementById('game-status').style.color = '#2ecc71';
    }

    async placeCard(cellIndex) {
        if (this.gameState.turn !== 'player' || this.gameState.gameOver) return;
        if (!this.gameState.selectedCard) {
            document.getElementById('game-status').textContent = 'Select a card from your hand first!';
            document.getElementById('game-status').style.color = '#e74c3c';
            return;
        }
        if (this.gameState.board[cellIndex] !== null) {
            document.getElementById('game-status').textContent = 'Cell already occupied!';
            document.getElementById('game-status').style.color = '#e74c3c';
            return;
        }

        // Place card on board
        this.gameState.board[cellIndex] = {
            card: this.gameState.selectedCard,
            owner: 'player'
        };

        // Remove card from hand
        this.playerHand.splice(this.gameState.selectedHandIndex, 1);
        this.gameState.selectedCard = null;
        this.gameState.selectedHandIndex = null;

        // Check for captures
        const captures = this.checkCaptures(cellIndex, 'player');

        // Render board
        this.renderBoard();
        this.renderPlayerHand();

        // Update scores
        this.updateScores();

        // Check for game end
        if (this.checkGameEnd()) {
            this.endGame();
            return;
        }

        // Opponent turn
        this.gameState.turn = 'opponent';
        document.getElementById('turn-indicator').textContent = 'OPPONENT TURN';
        document.getElementById('game-status').textContent = 'Opponent is thinking...';
        document.getElementById('game-status').style.color = '#e74c3c';

        setTimeout(() => this.opponentTurn(), 1500);
    }

    checkCaptures(cellIndex, player) {
        const captures = [];
        const placedCard = this.gameState.board[cellIndex];

        // Check adjacent cells (top, right, bottom, left)
        const adjacents = [
            { dir: 'top', cell: cellIndex - 3, compareOwn: 'top_value', compareOther: 'bottom_value' },
            { dir: 'right', cell: cellIndex + 1, compareOwn: 'right_value', compareOther: 'left_value' },
            { dir: 'bottom', cell: cellIndex + 3, compareOwn: 'bottom_value', compareOther: 'top_value' },
            { dir: 'left', cell: cellIndex - 1, compareOwn: 'left_value', compareOther: 'right_value' }
        ];

        adjacents.forEach(adj => {
            // Check if adjacent cell is valid and occupied by opponent
            if (adj.cell >= 0 && adj.cell < 9 && this.gameState.board[adj.cell]) {
                const adjCard = this.gameState.board[adj.cell];

                // Skip if same owner or if checking across rows (left/right)
                if (adjCard.owner === player) return;
                if ((adj.dir === 'left' && cellIndex % 3 === 0) || (adj.dir === 'right' && cellIndex % 3 === 2)) return;

                // Compare values
                const ownValue = placedCard.card[adj.compareOwn];
                const otherValue = adjCard.card[adj.compareOther];

                if (ownValue > otherValue) {
                    // Capture!
                    this.gameState.board[adj.cell].owner = player;
                    captures.push(adj.cell);
                }
            }
        });

        return captures;
    }

    renderBoard() {
        for (let i = 0; i < 9; i++) {
            const cell = document.getElementById(`cell-${i}`);
            if (!cell) continue;

            if (this.gameState.board[i]) {
                const { card, owner } = this.gameState.board[i];
                const bgColor = owner === 'player' ? 'linear-gradient(135deg, #3498db, #2980b9)' : 'linear-gradient(135deg, #e74c3c, #c0392b)';

                cell.innerHTML = `
                    <div style="width: 100%; height: 100%; padding: 10px; display: flex; flex-direction: column; align-items: center; justify-content: space-between;">
                        <div style="font-weight: bold; font-size: 14px; color: #fff; text-align: center;">
                            ${card.name}
                        </div>

                        <!-- Card Values -->
                        <div style="position: relative; width: 100%; height: 60px;">
                            <!-- Top -->
                            <div style="position: absolute; top: -5px; left: 50%; transform: translateX(-50%);
                                background: rgba(0,0,0,0.3); color: white; width: 25px; height: 25px;
                                border-radius: 50%; display: flex; align-items: center; justify-content: center;
                                font-weight: bold; font-size: 14px; border: 2px solid rgba(255,255,255,0.3);">
                                ${card.top_value}
                            </div>

                            <!-- Left & Right -->
                            <div style="position: absolute; top: 50%; left: 0; transform: translateY(-50%);
                                background: rgba(0,0,0,0.3); color: white; width: 25px; height: 25px;
                                border-radius: 50%; display: flex; align-items: center; justify-content: center;
                                font-weight: bold; font-size: 14px; border: 2px solid rgba(255,255,255,0.3);">
                                ${card.left_value}
                            </div>
                            <div style="position: absolute; top: 50%; right: 0; transform: translateY(-50%);
                                background: rgba(0,0,0,0.3); color: white; width: 25px; height: 25px;
                                border-radius: 50%; display: flex; align-items: center; justify-content: center;
                                font-weight: bold; font-size: 14px; border: 2px solid rgba(255,255,255,0.3);">
                                ${card.right_value}
                            </div>

                            <!-- Bottom -->
                            <div style="position: absolute; bottom: -5px; left: 50%; transform: translateX(-50%);
                                background: rgba(0,0,0,0.3); color: white; width: 25px; height: 25px;
                                border-radius: 50%; display: flex; align-items: center; justify-content: center;
                                font-weight: bold; font-size: 14px; border: 2px solid rgba(255,255,255,0.3);">
                                ${card.bottom_value}
                            </div>
                        </div>

                        <div style="font-size: 10px; color: rgba(255,255,255,0.7);">
                            ${owner === 'player' ? '🔵 You' : '🔴 Opp'}
                        </div>
                    </div>
                `;

                cell.style.background = bgColor;
                cell.style.cursor = 'default';
                cell.onclick = null;
            }
        }
    }

    updateScores() {
        // Count cards for each player
        let playerScore = 0;
        let opponentScore = 0;

        this.gameState.board.forEach(cell => {
            if (cell) {
                if (cell.owner === 'player') playerScore++;
                else opponentScore++;
            }
        });

        // Add cards still in hand
        playerScore += this.playerHand.length;
        opponentScore += this.opponentHand.length;

        this.gameState.playerScore = playerScore;
        this.gameState.opponentScore = opponentScore;

        document.getElementById('player-score').textContent = playerScore;
        document.getElementById('opponent-score').textContent = opponentScore;
    }

    async opponentTurn() {
        if (this.gameState.gameOver) return;

        // Find empty cells
        const emptyCells = [];
        for (let i = 0; i < 9; i++) {
            if (this.gameState.board[i] === null) {
                emptyCells.push(i);
            }
        }

        if (emptyCells.length === 0 || this.opponentHand.length === 0) {
            this.endGame();
            return;
        }

        // Simple AI: Pick random card and cell
        const randomCell = emptyCells[Math.floor(Math.random() * emptyCells.length)];
        const randomCardIndex = Math.floor(Math.random() * this.opponentHand.length);
        const opponentCard = this.opponentHand[randomCardIndex];

        // Place card
        this.gameState.board[randomCell] = {
            card: opponentCard,
            owner: 'opponent'
        };

        // Remove card from hand
        this.opponentHand.splice(randomCardIndex, 1);

        // Check for captures
        this.checkCaptures(randomCell, 'opponent');

        // Render
        this.renderBoard();
        this.updateScores();

        // Check for game end
        if (this.checkGameEnd()) {
            this.endGame();
            return;
        }

        // Back to player turn
        this.gameState.turn = 'player';
        document.getElementById('turn-indicator').textContent = 'YOUR TURN';
        document.getElementById('game-status').textContent = 'Your turn - Select a card and place it';
        document.getElementById('game-status').style.color = '#f39c12';
    }

    checkGameEnd() {
        // Game ends when all 9 cells are filled
        return this.gameState.board.every(cell => cell !== null);
    }

    endGame() {
        this.gameState.gameOver = true;

        const winner = this.gameState.playerScore > this.gameState.opponentScore ? 'player' :
                      this.gameState.playerScore < this.gameState.opponentScore ? 'opponent' : 'draw';

        let message = '';
        let color = '';

        if (winner === 'player') {
            message = `🏆 VICTORY!\n\nFinal Score: ${this.gameState.playerScore} - ${this.gameState.opponentScore}`;
            color = '#2ecc71';
        } else if (winner === 'opponent') {
            message = `💀 DEFEAT!\n\nFinal Score: ${this.gameState.playerScore} - ${this.gameState.opponentScore}`;
            color = '#e74c3c';
        } else {
            message = `🤝 DRAW!\n\nFinal Score: ${this.gameState.playerScore} - ${this.gameState.opponentScore}`;
            color = '#f39c12';
        }

        document.getElementById('game-status').textContent = message.replace(/\n/g, ' ');
        document.getElementById('game-status').style.color = color;
        document.getElementById('turn-indicator').textContent = 'GAME OVER';

        // Show play again button
        setTimeout(() => {
            if (confirm(message + '\n\nPlay again?')) {
                this.startMatch(this.gameMode);
            } else {
                this.showTab('play');
            }
        }, 1000);
    }
}

// Auto-initialize
if (typeof window !== 'undefined') {
    console.log('🃏 Card Game UI loaded');
}
