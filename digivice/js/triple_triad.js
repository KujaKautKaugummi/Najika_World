/**
 * TRIPLE TRIAD - Eigenständiges Kartenspiel (FF8/FF9 Style)
 *
 * NICHT ein Minigame! Man kann mit NPCs in der Welt spielen.
 * Monster-Karten werden durch Kampf gefangen (sehr geringe Chance)
 * oder durch speziellen "Card Capture" Skill.
 *
 * Erstellt: 2025-12-12
 */

const TripleTriad = (function() {
    'use strict';

    // ============================================
    // KARTEN-DATENBANK
    // ============================================

    // Basis-Karten (immer verfügbar)
    const BASE_CARDS = {
        // Starter-Karten
        'slime': { name: 'Schleim', values: [2, 3, 2, 1], emoji: '🟢', rarity: 'common', element: null },
        'goblin': { name: 'Goblin', values: [3, 2, 4, 3], emoji: '👺', rarity: 'common', element: null },
        'bat': { name: 'Fledermaus', values: [2, 4, 2, 3], emoji: '🦇', rarity: 'common', element: 'dark' },
        'rat': { name: 'Ratte', values: [1, 2, 3, 2], emoji: '🐀', rarity: 'common', element: null },
        'spider': { name: 'Spinne', values: [3, 3, 2, 2], emoji: '🕷️', rarity: 'common', element: null },

        // Uncommon Monster
        'skeleton': { name: 'Skelett', values: [4, 3, 3, 5], emoji: '💀', rarity: 'uncommon', element: 'dark' },
        'wolf': { name: 'Wolf', values: [5, 4, 3, 4], emoji: '🐺', rarity: 'uncommon', element: null },
        'ghost': { name: 'Geist', values: [4, 5, 3, 4], emoji: '👻', rarity: 'uncommon', element: 'dark' },
        'mushroom': { name: 'Pilzling', values: [3, 4, 5, 3], emoji: '🍄', rarity: 'uncommon', element: 'earth' },
        'beetle': { name: 'Käfer', values: [4, 3, 4, 4], emoji: '🪲', rarity: 'uncommon', element: 'earth' },

        // Rare Monster
        'golem': { name: 'Golem', values: [5, 5, 6, 6], emoji: '🗿', rarity: 'rare', element: 'earth' },
        'vampire': { name: 'Vampir', values: [6, 5, 4, 6], emoji: '🧛', rarity: 'rare', element: 'dark' },
        'werewolf': { name: 'Werwolf', values: [6, 6, 5, 5], emoji: '🐺', rarity: 'rare', element: null },
        'mage': { name: 'Magier', values: [5, 7, 4, 5], emoji: '🧙', rarity: 'rare', element: 'fire' },
        'knight': { name: 'Ritter', values: [6, 5, 6, 5], emoji: '🛡️', rarity: 'rare', element: null },

        // Epic Monster (Region Bosse)
        'sporax': { name: 'Sporax', values: [7, 6, 7, 6], emoji: '🍄', rarity: 'epic', element: 'poison' },
        'thornback': { name: 'Thornback', values: [7, 7, 6, 6], emoji: '🌳', rarity: 'epic', element: 'earth' },
        'ice_queen': { name: 'Eiskönigin', values: [6, 8, 6, 6], emoji: '❄️', rarity: 'epic', element: 'ice' },
        'fire_lord': { name: 'Feuerfürst', values: [8, 6, 6, 6], emoji: '🔥', rarity: 'epic', element: 'fire' },

        // Legendary (Spezielle NPCs)
        'najika': { name: 'Najika', values: [8, 7, 7, 8], emoji: '🧙‍♀️', rarity: 'legendary', element: 'fire' },
        'megumin': { name: 'Megumin', values: [9, 9, 1, 1], emoji: '💥', rarity: 'legendary', element: 'fire' },
        'harley': { name: 'Harley', values: [6, 6, 6, 6], emoji: '🃏', rarity: 'legendary', element: null },
        'dragon': { name: 'Drache', values: [9, 7, 8, 8], emoji: '🐉', rarity: 'legendary', element: 'fire' },
        'phoenix': { name: 'Phoenix', values: [7, 9, 6, 7], emoji: '🔥', rarity: 'legendary', element: 'fire' },
        'kuja': { name: 'Kuja', values: [7, 7, 7, 7], emoji: '⚔️', rarity: 'legendary', element: null }
    };

    // Karten-Fang-Chancen nach Rarität
    const CAPTURE_CHANCES = {
        'common': 0.05,      // 5%
        'uncommon': 0.02,    // 2%
        'rare': 0.008,       // 0.8%
        'epic': 0.003,       // 0.3%
        'legendary': 0.001   // 0.1%
    };

    // Element-Bonus (wenn Karte auf Element-Feld gespielt wird)
    const ELEMENT_BONUS = 1;

    // ============================================
    // SPIELER KARTEN-SAMMLUNG
    // ============================================

    let playerCollection = {
        cards: ['slime', 'goblin', 'bat'],  // Starter-Karten
        deck: ['slime', 'goblin', 'bat', 'slime', 'goblin'],  // 5 Karten Deck
        wins: 0,
        losses: 0
    };

    // Lade aus localStorage wenn vorhanden
    function loadCollection() {
        const saved = localStorage.getItem('tripleTriad_collection');
        if (saved) {
            try {
                playerCollection = JSON.parse(saved);
            } catch(e) {
                console.error('Triple Triad: Fehler beim Laden der Sammlung');
            }
        }
        // Versuche auch vom Server zu laden
        syncWithServer();
    }

    function saveCollection() {
        localStorage.setItem('tripleTriad_collection', JSON.stringify(playerCollection));
        // Sync zum Server
        syncToServer();
    }

    // ============================================
    // BACKEND API INTEGRATION
    // ============================================

    let serverCards = {};  // Karten vom Server
    let syncEnabled = true;

    async function syncWithServer() {
        if (!syncEnabled) return;
        try {
            // Lade Karten-Datenbank vom Server
            const cardsResponse = await fetch('http://localhost:8000/api/cards');
            if (cardsResponse.ok) {
                const data = await cardsResponse.json();
                if (data.cards) {
                    serverCards = {};
                    data.cards.forEach(card => {
                        serverCards[card.id] = card;
                    });
                    console.log('🃏 Triple Triad: ' + Object.keys(serverCards).length + ' Karten vom Server geladen');
                }
            }

            // Lade Spieler-Sammlung vom Server (wenn eingeloggt)
            const collectionResponse = await fetch('http://localhost:8000/api/cards/collection/player1');
            if (collectionResponse.ok) {
                const data = await collectionResponse.json();
                if (data.collection && data.collection.length > 0) {
                    // Merge mit lokaler Sammlung
                    data.collection.forEach(serverCard => {
                        const cardId = serverCard.card_id.toString();
                        if (!playerCollection.cards.includes(cardId)) {
                            playerCollection.cards.push(cardId);
                        }
                    });
                    console.log('🃏 Triple Triad: Sammlung synchronisiert');
                }
            }
        } catch(e) {
            console.warn('Triple Triad: Server-Sync fehlgeschlagen (offline?)', e);
        }
    }

    async function syncToServer() {
        if (!syncEnabled) return;
        try {
            // Sende Matches zum Server für Statistiken
            // Lokale Sammlung hat Priorität, Server ist Backup
        } catch(e) {
            console.warn('Triple Triad: Server-Sync fehlgeschlagen');
        }
    }

    // Server-Karte abrufen (mit Fallback zu lokaler Datenbank)
    function getServerCard(cardId) {
        if (serverCards[cardId]) {
            const sc = serverCards[cardId];
            return {
                name: sc.name,
                values: [sc.stats.top, sc.stats.right, sc.stats.bottom, sc.stats.left],
                emoji: getCardEmoji(sc.faction, sc.rarity),
                rarity: sc.rarity,
                element: sc.element
            };
        }
        return null;
    }

    function getCardEmoji(faction, rarity) {
        const emojis = {
            'fire_gunslingers': '🔥',
            'ice_mages': '❄️',
            'earth_warriors': '🗿',
            'wind_rangers': '🌪️',
            'shadow_outlaws': '🌑',
            'light_paladins': '✨',
            'beast_tamers': '🐺',
            'special': '⭐'
        };
        return emojis[faction] || '🃏';
    }

    // ============================================
    // KARTEN-FANG SYSTEM (wie FF8!)
    // ============================================

    /**
     * Versuche ein Monster als Karte zu fangen
     * Wird nach Kampf aufgerufen
     * @param {string} monsterId - ID des besiegten Monsters
     * @param {number} bonusChance - Extra Chance durch Skills/Items (0-1)
     * @returns {object|null} - Gefangene Karte oder null
     */
    function tryCapture(monsterId, bonusChance = 0) {
        const card = BASE_CARDS[monsterId];
        if (!card) return null;

        const baseChance = CAPTURE_CHANCES[card.rarity] || 0.01;
        const totalChance = Math.min(baseChance + bonusChance, 0.25); // Max 25%

        if (Math.random() < totalChance) {
            // Karte gefangen!
            if (!playerCollection.cards.includes(monsterId)) {
                playerCollection.cards.push(monsterId);
                saveCollection();
                return {
                    success: true,
                    isNew: true,
                    card: { id: monsterId, ...card }
                };
            } else {
                // Schon vorhanden - Duplikat!
                return {
                    success: true,
                    isNew: false,
                    card: { id: monsterId, ...card }
                };
            }
        }
        return null;
    }

    /**
     * Card Capture Skill - Erhöht Chance dramatisch
     * Kostet Mana, hat Cooldown
     */
    function useCardCaptureSkill(monsterId) {
        // Bonus von 10% durch Skill
        return tryCapture(monsterId, 0.10);
    }

    // ============================================
    // TRIPLE TRIAD SPIEL-LOGIK
    // ============================================

    let gameState = null;

    function createGame(opponentDeck, opponentName = 'NPC', rules = {}) {
        gameState = {
            board: Array(9).fill(null),  // 3x3 Board
            playerHand: [],
            opponentHand: [],
            playerTurn: Math.random() < 0.5,  // Zufällig wer anfängt
            selectedCard: null,
            playerScore: 5,
            opponentScore: 5,
            opponentName: opponentName,
            rules: {
                open: false,        // Gegner Karten sichtbar
                sameWall: false,    // Same-Wall Regel
                plus: false,        // Plus Regel
                elemental: false,   // Element-Felder
                ...rules
            },
            elementalBoard: rules.elemental ? generateElementBoard() : null,
            gameOver: false,
            winner: null
        };

        // Spieler-Deck laden
        const playerDeckCards = playerCollection.deck.map(id => ({
            id: id,
            ...BASE_CARDS[id],
            owner: 'player'
        }));
        gameState.playerHand = shuffleArray([...playerDeckCards]).slice(0, 5);

        // Gegner-Deck
        const opponentDeckCards = opponentDeck.map(id => ({
            id: id,
            ...BASE_CARDS[id],
            owner: 'opponent'
        }));
        gameState.opponentHand = shuffleArray([...opponentDeckCards]).slice(0, 5);

        return gameState;
    }

    function generateElementBoard() {
        const elements = ['fire', 'ice', 'earth', 'dark', 'wind', 'water', null, null, null];
        return shuffleArray(elements);
    }

    function shuffleArray(array) {
        const arr = [...array];
        for (let i = arr.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [arr[i], arr[j]] = [arr[j], arr[i]];
        }
        return arr;
    }

    function selectCard(index) {
        if (!gameState || !gameState.playerTurn || gameState.gameOver) return false;
        gameState.selectedCard = gameState.selectedCard === index ? null : index;
        return true;
    }

    function playCard(cellIndex) {
        if (!gameState || !gameState.playerTurn || gameState.selectedCard === null) return false;
        if (gameState.board[cellIndex] || gameState.gameOver) return false;

        const card = gameState.playerHand.splice(gameState.selectedCard, 1)[0];

        // Element-Bonus anwenden
        if (gameState.rules.elemental && gameState.elementalBoard[cellIndex]) {
            if (card.element === gameState.elementalBoard[cellIndex]) {
                card.values = card.values.map(v => Math.min(v + ELEMENT_BONUS, 10));
            } else if (card.element && card.element !== gameState.elementalBoard[cellIndex]) {
                card.values = card.values.map(v => Math.max(v - ELEMENT_BONUS, 1));
            }
        }

        gameState.board[cellIndex] = card;
        gameState.selectedCard = null;

        // Capture-Logik
        captureCards(cellIndex, card);
        updateScores();

        // Check Game End
        if (checkGameEnd()) return true;

        // Gegner ist dran
        gameState.playerTurn = false;
        return true;
    }

    function opponentTurn() {
        if (!gameState || gameState.playerTurn || gameState.gameOver) return false;
        if (gameState.opponentHand.length === 0) return false;

        // AI: Finde beste Position
        let bestMove = null;
        let bestScore = -Infinity;

        gameState.opponentHand.forEach((card, cardIdx) => {
            for (let cellIdx = 0; cellIdx < 9; cellIdx++) {
                if (gameState.board[cellIdx]) continue;

                let score = 0;
                const neighbors = getNeighbors(cellIdx);

                neighbors.forEach(n => {
                    const target = gameState.board[n.targetIdx];
                    if (target && target.owner === 'player') {
                        if (card.values[n.dir] > target.values[n.oppDir]) {
                            score += 10;  // Capture!
                        }
                    }
                    // Defensive: Vermeide schwache Seiten
                    if (!target && card.values[n.dir] < 4) {
                        score -= 2;
                    }
                });

                // Leichte Randomisierung
                score += Math.random() * 3;

                if (score > bestScore) {
                    bestScore = score;
                    bestMove = { cardIdx, cellIdx };
                }
            }
        });

        if (bestMove) {
            const card = gameState.opponentHand.splice(bestMove.cardIdx, 1)[0];

            // Element-Bonus
            if (gameState.rules.elemental && gameState.elementalBoard[bestMove.cellIdx]) {
                if (card.element === gameState.elementalBoard[bestMove.cellIdx]) {
                    card.values = card.values.map(v => Math.min(v + ELEMENT_BONUS, 10));
                }
            }

            gameState.board[bestMove.cellIdx] = card;
            captureCards(bestMove.cellIdx, card);
            updateScores();
        }

        checkGameEnd();
        gameState.playerTurn = true;
        return true;
    }

    function getNeighbors(cellIndex) {
        const row = Math.floor(cellIndex / 3);
        const col = cellIndex % 3;
        const neighbors = [];

        // Oben
        if (row > 0) neighbors.push({ dir: 0, targetIdx: cellIndex - 3, oppDir: 2 });
        // Rechts
        if (col < 2) neighbors.push({ dir: 1, targetIdx: cellIndex + 1, oppDir: 3 });
        // Unten
        if (row < 2) neighbors.push({ dir: 2, targetIdx: cellIndex + 3, oppDir: 0 });
        // Links
        if (col > 0) neighbors.push({ dir: 3, targetIdx: cellIndex - 1, oppDir: 1 });

        return neighbors;
    }

    function captureCards(cellIndex, card) {
        const neighbors = getNeighbors(cellIndex);

        neighbors.forEach(n => {
            const target = gameState.board[n.targetIdx];
            if (target && target.owner !== card.owner) {
                if (card.values[n.dir] > target.values[n.oppDir]) {
                    target.owner = card.owner;
                }
            }
        });
    }

    function updateScores() {
        gameState.playerScore = gameState.board.filter(c => c && c.owner === 'player').length
                               + gameState.playerHand.length;
        gameState.opponentScore = gameState.board.filter(c => c && c.owner === 'opponent').length
                                 + gameState.opponentHand.length;
    }

    function checkGameEnd() {
        const filledCells = gameState.board.filter(c => c).length;
        if (filledCells === 9) {
            gameState.gameOver = true;
            if (gameState.playerScore > gameState.opponentScore) {
                gameState.winner = 'player';
                playerCollection.wins++;
            } else if (gameState.playerScore < gameState.opponentScore) {
                gameState.winner = 'opponent';
                playerCollection.losses++;
            } else {
                gameState.winner = 'draw';
            }
            saveCollection();
            return true;
        }
        return false;
    }

    // ============================================
    // NPC GEGNER DEFINITIONEN
    // ============================================

    const NPC_OPPONENTS = {
        'dampf_hain_haendler': {
            name: 'Händler Bruno',
            deck: ['slime', 'goblin', 'rat', 'bat', 'spider'],
            difficulty: 'easy',
            dialogue: {
                start: "Ein Kartenspiel? Warum nicht, ich hab Zeit!",
                win: "Haha! Du schuldest mir jetzt was!",
                lose: "Naja, Karten waren nie meine Stärke...",
                draw: "Unentschieden! Nochmal?"
            }
        },
        'fee_luminara': {
            name: 'Fee Luminara',
            deck: ['ghost', 'spirit', 'bat', 'mushroom', 'skeleton'],
            difficulty: 'medium',
            rules: { elemental: true },
            dialogue: {
                start: "*kichert* Du willst gegen eine Fee spielen?",
                win: "Die Feen gewinnen immer!",
                lose: "Ohhh! Du bist gut! Hier, ein Geschenk!",
                draw: "Wie langweilig... nochmal!"
            }
        },
        'erzdruide_oakhart': {
            name: 'Erzdruide Oakhart',
            deck: ['golem', 'mushroom', 'thornback', 'beetle', 'wolf'],
            difficulty: 'hard',
            rules: { elemental: true, open: true },
            dialogue: {
                start: "Die Bäume sagen mir, du bist ein würdiger Gegner...",
                win: "Der Wald triumphiert immer.",
                lose: "Beeindruckend. Nimm diese seltene Karte.",
                draw: "Die Balance ist gewahrt."
            }
        },
        'najika': {
            name: 'Najika',
            deck: ['najika', 'megumin', 'harley', 'dragon', 'phoenix'],
            difficulty: 'legendary',
            rules: { elemental: true, plus: true },
            dialogue: {
                start: "EXPLOSION!!! ...äh, ich meine, lass uns spielen, Mr. K!",
                win: "Haha! Ich bin die Beste! 💥",
                lose: "W-WAS?! Das zählt nicht! Nochmal!",
                draw: "Hmph! Beim nächsten Mal gewinn ich!"
            }
        }
    };

    function challengeNPC(npcId) {
        const npc = NPC_OPPONENTS[npcId];
        if (!npc) return null;
        return createGame(npc.deck, npc.name, npc.rules || {});
    }

    // ============================================
    // DECK MANAGEMENT
    // ============================================

    function setDeck(cardIds) {
        if (cardIds.length !== 5) {
            console.error('Deck muss genau 5 Karten haben!');
            return false;
        }
        // Prüfe ob Spieler alle Karten besitzt
        for (const id of cardIds) {
            if (!playerCollection.cards.includes(id)) {
                console.error(`Karte ${id} nicht in Sammlung!`);
                return false;
            }
        }
        playerCollection.deck = cardIds;
        saveCollection();
        return true;
    }

    function getCollection() {
        return {
            cards: playerCollection.cards.map(id => ({
                id: id,
                ...BASE_CARDS[id]
            })),
            deck: playerCollection.deck,
            wins: playerCollection.wins,
            losses: playerCollection.losses
        };
    }

    function addCardToCollection(cardId) {
        if (BASE_CARDS[cardId] && !playerCollection.cards.includes(cardId)) {
            playerCollection.cards.push(cardId);
            saveCollection();
            return true;
        }
        return false;
    }

    // ============================================
    // UI RENDERING
    // ============================================

    function renderGameUI(container) {
        if (!gameState) {
            container.innerHTML = '<p>Kein Spiel aktiv!</p>';
            return;
        }

        const html = `
            <div class="triad-container">
                <div class="triad-header">
                    <span class="player-score">Du: <strong>${gameState.playerScore}</strong></span>
                    <span class="vs">VS</span>
                    <span class="opponent-score">${gameState.opponentName}: <strong>${gameState.opponentScore}</strong></span>
                </div>

                <div class="triad-main">
                    <div class="triad-hand player-hand" id="playerHandContainer"></div>
                    <div class="triad-board" id="triadBoardContainer"></div>
                    <div class="triad-hand opponent-hand" id="opponentHandContainer"></div>
                </div>

                <div class="triad-status" id="triadStatusText">
                    ${gameState.gameOver ? getEndGameText() : (gameState.playerTurn ? '🎯 Dein Zug!' : '⏳ Gegner denkt nach...')}
                </div>
            </div>
        `;

        container.innerHTML = html;

        // Player Hand rendern
        const playerHandEl = document.getElementById('playerHandContainer');
        gameState.playerHand.forEach((card, i) => {
            const cardEl = createCardElement(card, i, 'player');
            if (gameState.selectedCard === i) cardEl.classList.add('selected');
            if (gameState.playerTurn && !gameState.gameOver) {
                cardEl.onclick = () => {
                    selectCard(i);
                    renderGameUI(container);
                };
            }
            playerHandEl.appendChild(cardEl);
        });

        // Opponent Hand rendern
        const opponentHandEl = document.getElementById('opponentHandContainer');
        gameState.opponentHand.forEach((card, i) => {
            if (gameState.rules.open) {
                opponentHandEl.appendChild(createCardElement(card, i, 'opponent'));
            } else {
                const back = document.createElement('div');
                back.className = 'triad-card back';
                back.innerHTML = '🃏';
                opponentHandEl.appendChild(back);
            }
        });

        // Board rendern
        const boardEl = document.getElementById('triadBoardContainer');
        for (let i = 0; i < 9; i++) {
            const cell = document.createElement('div');
            cell.className = 'triad-cell';

            // Element-Feld anzeigen
            if (gameState.rules.elemental && gameState.elementalBoard[i]) {
                cell.classList.add('element-' + gameState.elementalBoard[i]);
                cell.setAttribute('data-element', getElementEmoji(gameState.elementalBoard[i]));
            }

            if (gameState.board[i]) {
                cell.appendChild(createCardElement(gameState.board[i], i, gameState.board[i].owner, true));
            } else if (gameState.playerTurn && gameState.selectedCard !== null && !gameState.gameOver) {
                cell.classList.add('playable');
                cell.onclick = () => {
                    if (playCard(i)) {
                        renderGameUI(container);
                        if (!gameState.gameOver && !gameState.playerTurn) {
                            setTimeout(() => {
                                opponentTurn();
                                renderGameUI(container);
                            }, 800);
                        }
                    }
                };
            }
            boardEl.appendChild(cell);
        }

        // Styles einfügen wenn nicht vorhanden
        if (!document.getElementById('triad-game-styles')) {
            const style = document.createElement('style');
            style.id = 'triad-game-styles';
            style.textContent = getStyles();
            document.head.appendChild(style);
        }
    }

    function createCardElement(card, index, owner, onBoard = false) {
        const el = document.createElement('div');
        el.className = `triad-card ${owner}`;
        if (onBoard) el.classList.add('on-board');

        const rarityColors = {
            'common': '#888',
            'uncommon': '#4CAF50',
            'rare': '#2196F3',
            'epic': '#9C27B0',
            'legendary': '#FFD700'
        };

        el.style.borderColor = rarityColors[card.rarity] || '#888';

        el.innerHTML = `
            <div class="card-value top">${card.values[0]}</div>
            <div class="card-row">
                <span class="card-value left">${card.values[3]}</span>
                <span class="card-emoji">${card.emoji}</span>
                <span class="card-value right">${card.values[1]}</span>
            </div>
            <div class="card-value bottom">${card.values[2]}</div>
            <div class="card-name">${card.name}</div>
        `;

        return el;
    }

    function getElementEmoji(element) {
        const emojis = {
            'fire': '🔥', 'ice': '❄️', 'earth': '🪨',
            'dark': '🌑', 'wind': '💨', 'water': '💧'
        };
        return emojis[element] || '';
    }

    function getEndGameText() {
        if (gameState.winner === 'player') {
            return '🎉 GEWONNEN!';
        } else if (gameState.winner === 'opponent') {
            return '😢 VERLOREN!';
        }
        return '🤝 UNENTSCHIEDEN!';
    }

    function getStyles() {
        return `
            .triad-container { display: flex; flex-direction: column; gap: 15px; padding: 15px; background: rgba(0,0,0,0.9); border-radius: 10px; max-width: 600px; margin: 0 auto; }
            .triad-header { display: flex; justify-content: space-between; align-items: center; font-size: 18px; }
            .player-score { color: #4169e1; }
            .opponent-score { color: #ff69b4; }
            .vs { color: #fff; font-weight: bold; }
            .triad-main { display: flex; justify-content: center; align-items: center; gap: 15px; }
            .triad-hand { display: flex; flex-direction: column; gap: 5px; }
            .triad-board { display: grid; grid-template-columns: repeat(3, 85px); gap: 4px; background: #1a1a1a; padding: 8px; border-radius: 8px; }
            .triad-cell { width: 85px; height: 100px; background: #222; border: 2px solid #333; border-radius: 4px; display: flex; align-items: center; justify-content: center; position: relative; }
            .triad-cell.playable { cursor: pointer; border-color: #4CAF50; background: rgba(76,175,80,0.2); }
            .triad-cell.playable:hover { background: rgba(76,175,80,0.4); }
            .triad-cell[data-element]::before { content: attr(data-element); position: absolute; top: 2px; right: 2px; font-size: 12px; opacity: 0.6; }
            .triad-cell.element-fire { background: rgba(255,100,0,0.15); }
            .triad-cell.element-ice { background: rgba(100,200,255,0.15); }
            .triad-cell.element-earth { background: rgba(139,69,19,0.15); }
            .triad-cell.element-dark { background: rgba(50,0,50,0.3); }
            .triad-card { width: 75px; height: 95px; background: #333; border: 3px solid #666; border-radius: 5px; display: flex; flex-direction: column; align-items: center; justify-content: center; cursor: pointer; transition: all 0.2s; font-size: 13px; }
            .triad-card:hover { transform: scale(1.05); }
            .triad-card.selected { transform: scale(1.1); box-shadow: 0 0 15px gold; }
            .triad-card.back { background: linear-gradient(135deg, #4a0e4e, #1a1a2e); font-size: 28px; cursor: default; }
            .triad-card.player { background: rgba(65,105,225,0.2); }
            .triad-card.player.on-board { background: rgba(65,105,225,0.4); }
            .triad-card.opponent { background: rgba(255,105,180,0.2); }
            .triad-card.opponent.on-board { background: rgba(255,105,180,0.4); }
            .card-value { font-weight: bold; font-size: 14px; }
            .card-row { display: flex; align-items: center; gap: 3px; }
            .card-emoji { font-size: 22px; }
            .card-name { font-size: 9px; color: #aaa; margin-top: 2px; }
            .triad-status { text-align: center; font-size: 16px; color: #fff; padding: 10px; background: rgba(255,255,255,0.1); border-radius: 5px; }
        `;
    }

    // ============================================
    // ÖFFENTLICHE API
    // ============================================

    // Initialisierung
    loadCollection();

    return {
        // Spiel starten
        challengeNPC: challengeNPC,
        createGame: createGame,

        // Spiel-Aktionen
        selectCard: selectCard,
        playCard: playCard,
        opponentTurn: opponentTurn,
        getState: () => gameState,

        // Karten-Sammlung
        tryCapture: tryCapture,
        useCardCaptureSkill: useCardCaptureSkill,
        getCollection: getCollection,
        addCard: addCardToCollection,
        setDeck: setDeck,

        // UI
        render: renderGameUI,

        // NPCs
        getNPCs: () => NPC_OPPONENTS,
        getCard: (id) => BASE_CARDS[id] ? { id, ...BASE_CARDS[id] } : null,
        getAllCards: () => BASE_CARDS,

        // Backend API
        syncWithServer: syncWithServer,
        getServerCards: () => serverCards,
        getServerCard: getServerCard,
        setSyncEnabled: (enabled) => { syncEnabled = enabled; }
    };
})();

// Global verfügbar machen
window.TripleTriad = TripleTriad;

// ============================================
// TRIPLE TRIAD NPC DIALOG SYSTEM
// ============================================

const TripleTriadUI = (function() {
    'use strict';

    let dialogOpen = false;
    let currentNpcId = null;
    let gameContainer = null;

    /**
     * Öffne Triple Triad Dialog mit NPC
     * @param {string} npcId - ID des NPCs (z.B. 'dampf_hain_haendler')
     */
    function openNPCChallenge(npcId) {
        const npcs = TripleTriad.getNPCs();
        const npc = npcs[npcId];

        if (!npc) {
            if (typeof showNotification === 'function') {
                showNotification('Dieser NPC spielt kein Triple Triad.');
            }
            return;
        }

        currentNpcId = npcId;
        dialogOpen = true;

        // Erstelle Dialog-Container
        const overlay = document.createElement('div');
        overlay.id = 'triad-npc-overlay';
        overlay.innerHTML = `
            <div class="triad-npc-dialog">
                <div class="triad-npc-header">
                    <h2>🃏 Triple Triad</h2>
                    <button class="triad-close-btn" onclick="TripleTriadUI.close()">✕</button>
                </div>
                <div class="triad-npc-content">
                    <div class="npc-portrait">🧑‍🌾</div>
                    <div class="npc-info">
                        <h3>${npc.name}</h3>
                        <p class="npc-dialogue">"${npc.dialogue.start}"</p>
                        <p class="difficulty">Schwierigkeit: <span class="diff-${npc.difficulty}">${npc.difficulty.toUpperCase()}</span></p>
                    </div>
                </div>
                <div class="triad-npc-actions">
                    <button class="triad-btn play" onclick="TripleTriadUI.startGame()">🎴 Spielen</button>
                    <button class="triad-btn deck" onclick="TripleTriadUI.showDeck()">📋 Deck</button>
                    <button class="triad-btn collection" onclick="TripleTriadUI.showCollection()">🗃️ Sammlung</button>
                    <button class="triad-btn cancel" onclick="TripleTriadUI.close()">Abbrechen</button>
                </div>
            </div>
        `;

        // Styles einfügen
        if (!document.getElementById('triad-ui-styles')) {
            const style = document.createElement('style');
            style.id = 'triad-ui-styles';
            style.textContent = getNPCDialogStyles();
            document.head.appendChild(style);
        }

        document.body.appendChild(overlay);
    }

    function startGame() {
        if (!currentNpcId) return;

        const npcs = TripleTriad.getNPCs();
        const npc = npcs[currentNpcId];

        // Spiel starten
        const game = TripleTriad.challengeNPC(currentNpcId);
        if (!game) {
            if (typeof showNotification === 'function') {
                showNotification('Fehler beim Starten des Spiels!');
            }
            return;
        }

        // Dialog zu Spiel-Ansicht wechseln
        const overlay = document.getElementById('triad-npc-overlay');
        if (overlay) {
            overlay.innerHTML = `
                <div class="triad-game-dialog">
                    <div class="triad-game-header">
                        <h2>🃏 ${npc.name}</h2>
                        <button class="triad-close-btn" onclick="TripleTriadUI.confirmQuit()">✕</button>
                    </div>
                    <div id="triad-game-container"></div>
                </div>
            `;

            gameContainer = document.getElementById('triad-game-container');
            TripleTriad.render(gameContainer);

            // Wenn Gegner anfängt
            const state = TripleTriad.getState();
            if (!state.playerTurn) {
                setTimeout(() => {
                    TripleTriad.opponentTurn();
                    TripleTriad.render(gameContainer);
                }, 1000);
            }
        }
    }

    function showDeck() {
        const collection = TripleTriad.getCollection();
        const overlay = document.getElementById('triad-npc-overlay');

        if (overlay) {
            const dialog = overlay.querySelector('.triad-npc-dialog');
            if (dialog) {
                dialog.innerHTML = `
                    <div class="triad-npc-header">
                        <h2>📋 Dein Deck</h2>
                        <button class="triad-close-btn" onclick="TripleTriadUI.backToNPC()">←</button>
                    </div>
                    <div class="triad-deck-content">
                        <p>Wähle 5 Karten für dein Deck:</p>
                        <div class="deck-slots" id="deckSlots"></div>
                        <hr>
                        <p>Deine Karten:</p>
                        <div class="collection-grid" id="deckCollectionGrid"></div>
                    </div>
                    <div class="triad-npc-actions">
                        <button class="triad-btn play" onclick="TripleTriadUI.saveDeck()">💾 Speichern</button>
                        <button class="triad-btn cancel" onclick="TripleTriadUI.backToNPC()">Zurück</button>
                    </div>
                `;

                renderDeckUI();
            }
        }
    }

    function renderDeckUI() {
        const collection = TripleTriad.getCollection();
        const deckSlots = document.getElementById('deckSlots');
        const collectionGrid = document.getElementById('deckCollectionGrid');

        if (!deckSlots || !collectionGrid) return;

        // Deck Slots
        deckSlots.innerHTML = '';
        for (let i = 0; i < 5; i++) {
            const slot = document.createElement('div');
            slot.className = 'deck-slot';
            slot.dataset.index = i;

            if (collection.deck[i]) {
                const card = TripleTriad.getCard(collection.deck[i]);
                if (card) {
                    slot.innerHTML = `
                        <div class="mini-card" data-id="${card.id}">
                            <span class="card-emoji">${card.emoji}</span>
                            <span class="card-name">${card.name}</span>
                        </div>
                    `;
                    slot.onclick = () => removeFromDeck(i);
                }
            } else {
                slot.innerHTML = '<span class="empty">Leer</span>';
            }

            deckSlots.appendChild(slot);
        }

        // Alle Karten in Sammlung
        collectionGrid.innerHTML = '';
        collection.cards.forEach(card => {
            const cardEl = document.createElement('div');
            cardEl.className = 'mini-card selectable';
            cardEl.dataset.id = card.id;
            cardEl.innerHTML = `
                <span class="card-emoji">${card.emoji}</span>
                <span class="card-name">${card.name}</span>
            `;
            cardEl.onclick = () => addToDeck(card.id);
            collectionGrid.appendChild(cardEl);
        });
    }

    let tempDeck = [];

    function addToDeck(cardId) {
        const collection = TripleTriad.getCollection();
        tempDeck = [...collection.deck];

        // Finde ersten leeren Slot
        const emptyIdx = tempDeck.findIndex(c => !c || c === null);
        if (emptyIdx !== -1 && tempDeck.length < 5) {
            tempDeck[emptyIdx] = cardId;
        } else if (tempDeck.length < 5) {
            tempDeck.push(cardId);
        } else {
            if (typeof showNotification === 'function') {
                showNotification('Deck ist voll! Entferne erst eine Karte.');
            }
            return;
        }

        // Temporär speichern
        TripleTriad.setDeck(tempDeck);
        renderDeckUI();
    }

    function removeFromDeck(index) {
        const collection = TripleTriad.getCollection();
        tempDeck = [...collection.deck];
        tempDeck[index] = null;
        tempDeck = tempDeck.filter(c => c !== null);

        // Pad auf 5
        while (tempDeck.length < 5) {
            // Fülle mit ersten verfügbaren Karten
            const available = collection.cards.find(c => !tempDeck.includes(c.id));
            if (available) tempDeck.push(available.id);
            else break;
        }

        if (tempDeck.length === 5) {
            TripleTriad.setDeck(tempDeck);
        }
        renderDeckUI();
    }

    function saveDeck() {
        if (typeof showNotification === 'function') {
            showNotification('Deck gespeichert!');
        }
        backToNPC();
    }

    function showCollection() {
        const collection = TripleTriad.getCollection();
        const allCards = TripleTriad.getAllCards();
        const overlay = document.getElementById('triad-npc-overlay');

        if (overlay) {
            const dialog = overlay.querySelector('.triad-npc-dialog');
            if (dialog) {
                const totalCards = Object.keys(allCards).length;
                const ownedCards = collection.cards.length;

                dialog.innerHTML = `
                    <div class="triad-npc-header">
                        <h2>🗃️ Kartensammlung</h2>
                        <button class="triad-close-btn" onclick="TripleTriadUI.backToNPC()">←</button>
                    </div>
                    <div class="triad-collection-content">
                        <p class="collection-stats">
                            Gesammelt: <strong>${ownedCards}/${totalCards}</strong> |
                            Siege: <strong>${collection.wins}</strong> |
                            Niederlagen: <strong>${collection.losses}</strong>
                        </p>
                        <div class="collection-full-grid" id="fullCollectionGrid"></div>
                    </div>
                    <div class="triad-npc-actions">
                        <button class="triad-btn cancel" onclick="TripleTriadUI.backToNPC()">Zurück</button>
                    </div>
                `;

                const grid = document.getElementById('fullCollectionGrid');
                Object.entries(allCards).forEach(([id, card]) => {
                    const owned = collection.cards.some(c => c.id === id || c === id);
                    const cardEl = document.createElement('div');
                    cardEl.className = `collection-card ${owned ? 'owned' : 'locked'}`;
                    cardEl.innerHTML = `
                        <div class="card-emoji">${owned ? card.emoji : '❓'}</div>
                        <div class="card-name">${owned ? card.name : '???'}</div>
                        <div class="card-rarity rarity-${card.rarity}">${card.rarity}</div>
                    `;
                    grid.appendChild(cardEl);
                });
            }
        }
    }

    function backToNPC() {
        if (currentNpcId) {
            close();
            openNPCChallenge(currentNpcId);
        }
    }

    function confirmQuit() {
        if (confirm('Spiel wirklich beenden? Du verlierst das aktuelle Spiel!')) {
            close();
        }
    }

    function close() {
        const overlay = document.getElementById('triad-npc-overlay');
        if (overlay) {
            overlay.remove();
        }
        dialogOpen = false;
        currentNpcId = null;
        gameContainer = null;
    }

    function getNPCDialogStyles() {
        return `
            #triad-npc-overlay {
                position: fixed;
                top: 0; left: 0; right: 0; bottom: 0;
                background: rgba(0,0,0,0.85);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 10000;
            }
            .triad-npc-dialog, .triad-game-dialog {
                background: linear-gradient(135deg, #1a1a2e, #16213e);
                border: 2px solid #4CAF50;
                border-radius: 15px;
                padding: 20px;
                min-width: 400px;
                max-width: 700px;
                color: #fff;
                box-shadow: 0 0 30px rgba(76,175,80,0.3);
            }
            .triad-npc-header, .triad-game-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 15px;
                border-bottom: 1px solid #4CAF50;
                padding-bottom: 10px;
            }
            .triad-npc-header h2, .triad-game-header h2 {
                margin: 0;
                color: #4CAF50;
            }
            .triad-close-btn {
                background: #ff4444;
                border: none;
                color: white;
                width: 30px; height: 30px;
                border-radius: 50%;
                cursor: pointer;
                font-size: 16px;
            }
            .triad-close-btn:hover { background: #ff6666; }
            .triad-npc-content {
                display: flex;
                gap: 20px;
                align-items: center;
                margin-bottom: 20px;
            }
            .npc-portrait {
                font-size: 60px;
                background: rgba(255,255,255,0.1);
                border-radius: 10px;
                padding: 15px;
            }
            .npc-info h3 { margin: 0 0 10px 0; color: #FFD700; }
            .npc-dialogue {
                font-style: italic;
                color: #aaa;
                margin: 10px 0;
            }
            .difficulty { font-size: 14px; }
            .diff-easy { color: #4CAF50; }
            .diff-medium { color: #FFC107; }
            .diff-hard { color: #FF9800; }
            .diff-legendary { color: #E91E63; }
            .triad-npc-actions {
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
            }
            .triad-btn {
                padding: 10px 20px;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-size: 14px;
                font-weight: bold;
                transition: all 0.2s;
            }
            .triad-btn:hover { transform: scale(1.05); }
            .triad-btn.play { background: #4CAF50; color: white; }
            .triad-btn.deck { background: #2196F3; color: white; }
            .triad-btn.collection { background: #9C27B0; color: white; }
            .triad-btn.cancel { background: #666; color: white; }
            .deck-slots {
                display: flex;
                gap: 10px;
                margin: 10px 0;
            }
            .deck-slot {
                width: 80px; height: 100px;
                border: 2px dashed #4CAF50;
                border-radius: 8px;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
            }
            .deck-slot .empty { color: #666; font-size: 12px; }
            .mini-card {
                display: flex;
                flex-direction: column;
                align-items: center;
                padding: 5px;
                background: rgba(255,255,255,0.1);
                border-radius: 5px;
            }
            .mini-card.selectable { cursor: pointer; }
            .mini-card.selectable:hover { background: rgba(76,175,80,0.3); }
            .mini-card .card-emoji { font-size: 24px; }
            .mini-card .card-name { font-size: 10px; color: #aaa; }
            .collection-grid, .collection-full-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(70px, 1fr));
                gap: 10px;
                max-height: 200px;
                overflow-y: auto;
                padding: 10px;
                background: rgba(0,0,0,0.3);
                border-radius: 8px;
            }
            .collection-full-grid { max-height: 300px; }
            .collection-card {
                padding: 10px;
                text-align: center;
                border-radius: 8px;
                background: rgba(255,255,255,0.05);
            }
            .collection-card.owned { border: 2px solid #4CAF50; }
            .collection-card.locked { opacity: 0.5; border: 2px solid #333; }
            .collection-card .card-emoji { font-size: 30px; display: block; }
            .collection-card .card-name { font-size: 11px; color: #fff; }
            .collection-card .card-rarity { font-size: 9px; text-transform: uppercase; margin-top: 3px; }
            .rarity-common { color: #888; }
            .rarity-uncommon { color: #4CAF50; }
            .rarity-rare { color: #2196F3; }
            .rarity-epic { color: #9C27B0; }
            .rarity-legendary { color: #FFD700; }
            .collection-stats { margin-bottom: 15px; color: #aaa; }
            .triad-deck-content, .triad-collection-content {
                margin-bottom: 20px;
            }
        `;
    }

    return {
        open: openNPCChallenge,
        close: close,
        startGame: startGame,
        showDeck: showDeck,
        showCollection: showCollection,
        saveDeck: saveDeck,
        backToNPC: backToNPC,
        confirmQuit: confirmQuit,
        isOpen: () => dialogOpen
    };
})();

window.TripleTriadUI = TripleTriadUI;

console.log('🃏 Triple Triad System geladen');
