/**
 * DUNGEON DICE MONSTERS - Vollständiges Gameplay System
 * =====================================================
 *
 * Yu-Gi-Oh! DDM inspiriertes Würfel-Kampfsystem
 *
 * Spielregeln:
 * - Jeder Spieler hat 3000 LP (Life Points)
 * - 12er Dice Pool (auswählen vor Match)
 * - 13x19 Dungeon Grid (vereinfacht: 7x7)
 * - Würfeln + Monster beschwören + Bewegen + Angreifen
 * - Wer den gegnerischen Monster Lord besiegt oder 0 LP = verliert
 *
 * Erstellt: 2025-12-18
 */

const DungeonDiceGame = (function() {
    'use strict';

    // ============================================
    // KONSTANTEN
    // ============================================

    const GRID_SIZE = 7;  // 7x7 Spielfeld
    const STARTING_LP = 3000;
    const DICE_POOL_SIZE = 12;
    const MAX_MONSTERS_ON_FIELD = 5;
    const CREST_TYPES = ['attack', 'defense', 'movement', 'magic', 'trap', 'summon'];

    // Element Stärken/Schwächen
    const ELEMENT_CHART = {
        fire: { strong: ['wind', 'earth'], weak: ['water'] },
        water: { strong: ['fire'], weak: ['wind', 'earth'] },
        wind: { strong: ['water'], weak: ['fire', 'earth'] },
        earth: { strong: ['wind', 'water'], weak: ['fire'] },
        light: { strong: ['dark'], weak: ['dark'] },
        dark: { strong: ['light'], weak: ['light'] },
        explosion: { strong: ['fire', 'water', 'wind', 'earth', 'light', 'dark'], weak: [] }
    };

    // ============================================
    // WÜRFEL MONSTER DATENBANK (von Shop importieren + erweitern)
    // ============================================

    const DICE_MONSTERS = {
        // Starter
        1: { id: 1, name: "Krieger-Würfel", atk: 15, def: 10, hp: 25, element: null, rarity: 'common', summonCost: 1, movement: 2 },
        2: { id: 2, name: "Schild-Würfel", atk: 5, def: 20, hp: 30, element: null, rarity: 'common', summonCost: 1, movement: 1 },
        3: { id: 3, name: "Bogenschütze", atk: 18, def: 5, hp: 20, element: null, rarity: 'common', summonCost: 1, movement: 2, ranged: true },

        // Fire
        4: { id: 4, name: "Feuer-Imp", atk: 12, def: 8, hp: 22, element: 'fire', rarity: 'common', summonCost: 1, movement: 3 },
        5: { id: 5, name: "Flammen-Ritter", atk: 25, def: 15, hp: 35, element: 'fire', rarity: 'uncommon', summonCost: 2, movement: 2 },
        6: { id: 6, name: "Lava-Golem", atk: 35, def: 30, hp: 50, element: 'fire', rarity: 'rare', summonCost: 3, movement: 1 },
        7: { id: 7, name: "Vulkan-Lord", atk: 45, def: 35, hp: 60, element: 'fire', rarity: 'epic', summonCost: 4, movement: 2, special: 'Verbrennt angrenzende Gegner' },

        // Water
        8: { id: 8, name: "Wasser-Sprite", atk: 10, def: 12, hp: 25, element: 'water', rarity: 'common', summonCost: 1, movement: 3 },
        9: { id: 9, name: "See-Schlange", atk: 22, def: 18, hp: 38, element: 'water', rarity: 'uncommon', summonCost: 2, movement: 3 },
        10: { id: 10, name: "Kraken", atk: 38, def: 25, hp: 55, element: 'water', rarity: 'rare', summonCost: 3, movement: 2, special: 'Greift 2 Ziele an' },
        11: { id: 11, name: "Leviathan", atk: 50, def: 40, hp: 70, element: 'water', rarity: 'epic', summonCost: 4, movement: 2, special: 'Tsunami: Schiebt alle Gegner' },

        // Earth
        12: { id: 12, name: "Erd-Wurm", atk: 14, def: 6, hp: 20, element: 'earth', rarity: 'common', summonCost: 1, movement: 2 },
        13: { id: 13, name: "Stein-Golem", atk: 20, def: 35, hp: 45, element: 'earth', rarity: 'uncommon', summonCost: 2, movement: 1 },
        14: { id: 14, name: "Kristall-Titan", atk: 32, def: 45, hp: 60, element: 'earth', rarity: 'rare', summonCost: 3, movement: 1, special: '+10 DEF pro Runde' },
        15: { id: 15, name: "Erdbeben-Behemoth", atk: 55, def: 50, hp: 80, element: 'earth', rarity: 'epic', summonCost: 4, movement: 1, special: 'Erdbeben: AoE Schaden' },

        // Wind
        16: { id: 16, name: "Wind-Fae", atk: 12, def: 6, hp: 18, element: 'wind', rarity: 'common', summonCost: 1, movement: 4 },
        17: { id: 17, name: "Sturm-Falke", atk: 28, def: 12, hp: 30, element: 'wind', rarity: 'uncommon', summonCost: 2, movement: 4, flying: true },
        18: { id: 18, name: "Tornado-Elemental", atk: 38, def: 18, hp: 42, element: 'wind', rarity: 'rare', summonCost: 3, movement: 3, flying: true },
        19: { id: 19, name: "Sturmgott", atk: 48, def: 25, hp: 55, element: 'wind', rarity: 'epic', summonCost: 4, movement: 4, special: 'Blitz: 2x Angriff', flying: true },

        // Light
        20: { id: 20, name: "Licht-Wisp", atk: 10, def: 10, hp: 22, element: 'light', rarity: 'common', summonCost: 1, movement: 3 },
        21: { id: 21, name: "Engel-Wächter", atk: 22, def: 28, hp: 40, element: 'light', rarity: 'uncommon', summonCost: 2, movement: 2, special: 'Heilt Verbündete' },
        22: { id: 22, name: "Seraph", atk: 35, def: 35, hp: 55, element: 'light', rarity: 'rare', summonCost: 3, movement: 3, flying: true },
        23: { id: 23, name: "Erzengel", atk: 45, def: 45, hp: 70, element: 'light', rarity: 'epic', summonCost: 4, movement: 3, special: 'Heiligenschein: +20 HP allen', flying: true },

        // Dark
        24: { id: 24, name: "Schatten-Sprite", atk: 15, def: 5, hp: 18, element: 'dark', rarity: 'common', summonCost: 1, movement: 3 },
        25: { id: 25, name: "Vampir", atk: 28, def: 15, hp: 35, element: 'dark', rarity: 'uncommon', summonCost: 2, movement: 2, special: 'Lebensraub' },
        26: { id: 26, name: "Lich", atk: 40, def: 20, hp: 48, element: 'dark', rarity: 'rare', summonCost: 3, movement: 2, special: 'Beschwört Skelett' },
        27: { id: 27, name: "Dunkler Lord", atk: 52, def: 38, hp: 65, element: 'dark', rarity: 'epic', summonCost: 4, movement: 2, special: 'Lebensraub 50%' },

        // Legendary / Special
        28: { id: 28, name: "Gold-Drache", atk: 60, def: 50, hp: 85, element: 'fire', rarity: 'legendary', summonCost: 5, movement: 3, flying: true, special: 'Feueratem: AoE' },
        29: { id: 29, name: "Götter-Würfel", atk: 70, def: 70, hp: 100, element: null, rarity: 'legendary', summonCost: 6, movement: 2, special: 'Göttlicher Schutz' },
        30: { id: 30, name: "Najika Explosion", atk: 99, def: 1, hp: 30, element: 'explosion', rarity: 'legendary', summonCost: 5, movement: 1, special: 'EXPLOSION: Zerstört ALLES!' }
    };

    // ============================================
    // NPC GEGNER
    // ============================================

    const NPC_OPPONENTS = {
        'roldan': {
            name: 'Meister Roldan',
            city: 'Handelsfestung',
            difficulty: 'hard',
            dicePool: [28, 7, 6, 5, 4, 4, 1, 2, 3, 5, 6, 7],  // Hat Gold-Drache!
            portrait: '🎲',
            dialogue: {
                start: "Du wagst es, mich herauszufordern? Ich bin Champion der Handelsfestung!",
                win: "Haha! Niemand besiegt Meister Roldan!",
                lose: "Unmöglich! Du... du hast gewonnen?!"
            }
        },
        'yuki': {
            name: 'Alte Meisterin Yuki',
            city: 'Dampf-Hain',
            difficulty: 'medium',
            dicePool: [13, 14, 12, 12, 13, 21, 20, 8, 9, 2, 2, 3],
            portrait: '🧓',
            dialogue: {
                start: "Setze dich, junger Reisender. Lass uns die Würfel sprechen...",
                win: "Die Weisheit der Jahre überwiegt.",
                lose: "Du hast ein gutes Herz. Nimm diesen Preis."
            }
        },
        'wurfbein': {
            name: "Käpt'n Wurfbein",
            city: 'Salzige Bucht',
            difficulty: 'medium',
            dicePool: [11, 10, 9, 8, 8, 9, 10, 3, 3, 1, 2, 16],
            portrait: '🏴‍☠️',
            dialogue: {
                start: "Yarr! Ein Landratten-Duell! Meine Würfel sind vom Meer gehärtet!",
                win: "Das Meer ist auf meiner Seite, Landratten!",
                lose: "Arrr... du hast mich besiegt! Hier, nimm die Beute!"
            }
        },
        'hexus': {
            name: 'Magister Hexus',
            city: 'Runenheim',
            difficulty: 'hard',
            dicePool: [19, 18, 17, 16, 22, 23, 20, 21, 16, 17, 4, 5],
            portrait: '🧙‍♂️',
            dialogue: {
                start: "Ein intellektuelles Duell. Möge der klügere Stratege gewinnen.",
                win: "Wie erwartet. Strategie besiegt Glück.",
                lose: "Faszinierend... Deine Taktik war überlegen."
            }
        },
        'ignis': {
            name: 'Schmied Ignis',
            city: 'Funken-Siedlung',
            difficulty: 'medium',
            dicePool: [7, 6, 5, 4, 4, 5, 6, 7, 28, 1, 2, 3],
            portrait: '🔥',
            dialogue: {
                start: "Meine Würfel sind im Vulkanfeuer gehärtet! Bereit für die Hitze?",
                win: "Heißer als die Lava selbst!",
                lose: "Du hast mein Feuer gelöscht... Respekt!"
            }
        },
        'najika_dice': {
            name: 'Najika (Würfel-Meisterin)',
            city: 'Schwarze Mühle',
            difficulty: 'legendary',
            dicePool: [30, 28, 29, 7, 11, 15, 19, 23, 27, 6, 10, 14],  // Hat NAJIKA EXPLOSION!
            portrait: '💥',
            dialogue: {
                start: "EXPLOSION-WÜRFEL! Das wird EPISCH, Mr. K!",
                win: "HAHA! Explosion gewinnt IMMER! 💥",
                lose: "W-WAS?! Das zählt nicht! Meine Würfel waren... ähm... müde!"
            }
        }
    };

    // ============================================
    // SPIELER DATEN
    // ============================================

    let playerData = {
        dicePool: [1, 2, 3, 4, 5, 8, 12, 16, 20, 24, 1, 2],  // Default Pool
        collection: [1, 2, 3, 4, 5, 8, 12, 16, 20, 24],
        wins: 0,
        losses: 0,
        gold: 500
    };

    function loadPlayerData() {
        const saved = localStorage.getItem('dungeonDiceGame_player');
        if (saved) {
            try {
                playerData = JSON.parse(saved);
            } catch(e) {
                console.error('DDM: Fehler beim Laden');
            }
        }
    }

    function savePlayerData() {
        localStorage.setItem('dungeonDiceGame_player', JSON.stringify(playerData));
    }

    // ============================================
    // SPIEL-ZUSTAND
    // ============================================

    let gameState = null;

    function createGame(opponentId) {
        const opponent = NPC_OPPONENTS[opponentId];
        if (!opponent) return null;

        gameState = {
            phase: 'roll',  // roll, summon, move, attack, end
            turn: 1,
            playerTurn: Math.random() < 0.5,

            // Spieler
            player: {
                lp: STARTING_LP,
                dicePool: [...playerData.dicePool],
                usedDice: [],
                crests: { attack: 0, defense: 0, movement: 0, magic: 0, summon: 0 },
                monsters: [],
                monsterLordPos: { x: 3, y: 0 }  // Mitte unten
            },

            // Gegner
            opponent: {
                name: opponent.name,
                portrait: opponent.portrait,
                difficulty: opponent.difficulty,
                lp: STARTING_LP,
                dicePool: [...opponent.dicePool],
                usedDice: [],
                crests: { attack: 0, defense: 0, movement: 0, magic: 0, summon: 0 },
                monsters: [],
                monsterLordPos: { x: 3, y: 6 }  // Mitte oben
            },

            // Spielfeld
            grid: createEmptyGrid(),

            // Aktuelle Aktion
            selectedMonster: null,
            selectedDice: null,
            lastRoll: null,

            // Status
            gameOver: false,
            winner: null,
            log: []
        };

        addLog(`Duell gegen ${opponent.name} beginnt!`);
        addLog(gameState.playerTurn ? 'Du fängst an!' : `${opponent.name} fängt an!`);

        return gameState;
    }

    function createEmptyGrid() {
        const grid = [];
        for (let y = 0; y < GRID_SIZE; y++) {
            const row = [];
            for (let x = 0; x < GRID_SIZE; x++) {
                row.push({
                    type: 'empty',
                    monster: null,
                    owner: null,
                    terrain: null
                });
            }
            grid.push(row);
        }
        // Monster Lords platzieren
        grid[0][3] = { type: 'monster_lord', monster: null, owner: 'player', terrain: 'base' };
        grid[6][3] = { type: 'monster_lord', monster: null, owner: 'opponent', terrain: 'base' };
        return grid;
    }

    function addLog(message) {
        if (gameState) {
            gameState.log.push({
                turn: gameState.turn,
                message: message,
                time: Date.now()
            });
        }
    }

    // ============================================
    // WÜRFEL MECHANIK
    // ============================================

    function rollDice(diceId) {
        const dice = DICE_MONSTERS[diceId];
        if (!dice) return null;

        // Würfel-Gesichter basierend auf Seltenheit
        const faces = generateDiceFaces(dice);
        const result = faces[Math.floor(Math.random() * 6)];

        return {
            diceId: diceId,
            diceName: dice.name,
            result: result,
            canSummon: result === 'summon',
            element: dice.element
        };
    }

    function generateDiceFaces(dice) {
        // Basis: 1 Summon, 5 Crests
        const summonChance = {
            'common': 2,      // 2/6 = 33%
            'uncommon': 2,    // 33%
            'rare': 1,        // 17%
            'epic': 1,        // 17%
            'legendary': 1    // 17%
        };

        const faces = [];
        const summons = summonChance[dice.rarity] || 1;

        for (let i = 0; i < summons; i++) {
            faces.push('summon');
        }

        // Rest mit Crests füllen
        const crests = ['attack', 'defense', 'movement', 'magic', 'trap'];
        while (faces.length < 6) {
            faces.push(crests[Math.floor(Math.random() * crests.length)]);
        }

        return shuffleArray(faces);
    }

    function shuffleArray(array) {
        const arr = [...array];
        for (let i = arr.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [arr[i], arr[j]] = [arr[j], arr[i]];
        }
        return arr;
    }

    // ============================================
    // SPIELZUG AKTIONEN
    // ============================================

    function playerRollDice(diceIndex) {
        if (!gameState || !gameState.playerTurn || gameState.phase !== 'roll') return null;
        if (gameState.gameOver) return null;

        const pool = gameState.player.dicePool;
        if (diceIndex >= pool.length) return null;

        const diceId = pool[diceIndex];
        const result = rollDice(diceId);

        // Würfel aus Pool entfernen und zu used hinzufügen
        pool.splice(diceIndex, 1);
        gameState.player.usedDice.push(diceId);

        gameState.lastRoll = result;

        if (result.canSummon) {
            gameState.phase = 'summon';
            addLog(`Du würfelst ${result.diceName}: BESCHWÖRUNG!`);
        } else {
            // Crest hinzufügen
            gameState.player.crests[result.result]++;
            addLog(`Du würfelst ${result.diceName}: ${getCrestEmoji(result.result)} ${result.result}`);
            gameState.phase = 'action';
        }

        return result;
    }

    function getCrestEmoji(crest) {
        const emojis = {
            attack: '⚔️',
            defense: '🛡️',
            movement: '👟',
            magic: '✨',
            trap: '🪤',
            summon: '🎯'
        };
        return emojis[crest] || '❓';
    }

    function summonMonster(x, y) {
        if (!gameState || !gameState.playerTurn || gameState.phase !== 'summon') return false;
        if (!gameState.lastRoll || !gameState.lastRoll.canSummon) return false;

        const cell = gameState.grid[y]?.[x];
        if (!cell || cell.type !== 'empty') return false;

        // Prüfe ob Beschwörung möglich (neben eigenem Monster oder Monster Lord)
        if (!canSummonAt(x, y, 'player')) {
            addLog('Kann dort nicht beschwören! Muss neben eigenem Monster/Lord sein.');
            return false;
        }

        const diceId = gameState.lastRoll.diceId;
        const dice = DICE_MONSTERS[diceId];

        // Monster auf Feld setzen
        const monster = {
            id: Date.now(),
            diceId: diceId,
            name: dice.name,
            atk: dice.atk,
            def: dice.def,
            hp: dice.hp,
            maxHp: dice.hp,
            element: dice.element,
            movement: dice.movement,
            movesLeft: dice.movement,
            hasAttacked: false,
            special: dice.special,
            ranged: dice.ranged || false,
            flying: dice.flying || false,
            owner: 'player',
            position: { x, y }
        };

        gameState.grid[y][x] = {
            type: 'monster',
            monster: monster,
            owner: 'player',
            terrain: null
        };
        gameState.player.monsters.push(monster);

        addLog(`${dice.name} beschworen auf (${x}, ${y})!`);
        gameState.phase = 'action';
        gameState.lastRoll = null;

        return true;
    }

    function canSummonAt(x, y, owner) {
        // Neben Monster Lord?
        const lord = owner === 'player' ? gameState.player.monsterLordPos : gameState.opponent.monsterLordPos;
        if (Math.abs(x - lord.x) <= 1 && Math.abs(y - lord.y) <= 1) {
            return true;
        }

        // Neben eigenem Monster?
        const directions = [[0,1], [0,-1], [1,0], [-1,0]];
        for (const [dx, dy] of directions) {
            const nx = x + dx;
            const ny = y + dy;
            const cell = gameState.grid[ny]?.[nx];
            if (cell && cell.owner === owner && cell.type === 'monster') {
                return true;
            }
        }

        return false;
    }

    function moveMonster(monsterId, targetX, targetY) {
        if (!gameState || !gameState.playerTurn || gameState.phase !== 'action') return false;

        const monster = gameState.player.monsters.find(m => m.id === monsterId);
        if (!monster || monster.movesLeft <= 0) return false;

        const { x: startX, y: startY } = monster.position;
        const distance = Math.abs(targetX - startX) + Math.abs(targetY - startY);

        if (distance > monster.movesLeft) {
            addLog('Zu weit! Nicht genug Bewegung.');
            return false;
        }

        const targetCell = gameState.grid[targetY]?.[targetX];
        if (!targetCell || targetCell.type !== 'empty') {
            addLog('Zielfeld besetzt!');
            return false;
        }

        // Bewegen
        gameState.grid[startY][startX] = { type: 'empty', monster: null, owner: null, terrain: null };
        gameState.grid[targetY][targetX] = { type: 'monster', monster: monster, owner: 'player', terrain: null };
        monster.position = { x: targetX, y: targetY };
        monster.movesLeft -= distance;

        addLog(`${monster.name} bewegt sich nach (${targetX}, ${targetY})`);
        return true;
    }

    function attackWithMonster(attackerId, targetX, targetY) {
        if (!gameState || !gameState.playerTurn || gameState.phase !== 'action') return null;

        const attacker = gameState.player.monsters.find(m => m.id === attackerId);
        if (!attacker || attacker.hasAttacked) {
            addLog('Dieses Monster hat bereits angegriffen!');
            return null;
        }

        // Prüfe Reichweite
        const { x: ax, y: ay } = attacker.position;
        const distance = Math.abs(targetX - ax) + Math.abs(targetY - ay);
        const maxRange = attacker.ranged ? 3 : 1;

        if (distance > maxRange) {
            addLog('Ziel außer Reichweite!');
            return null;
        }

        const targetCell = gameState.grid[targetY]?.[targetX];
        if (!targetCell) return null;

        // Angriff auf Monster Lord?
        if (targetCell.type === 'monster_lord' && targetCell.owner === 'opponent') {
            const damage = calculateDamage(attacker, null);
            gameState.opponent.lp -= damage;
            addLog(`${attacker.name} greift Monster Lord an! ${damage} Schaden! (LP: ${gameState.opponent.lp})`);
            attacker.hasAttacked = true;

            if (gameState.opponent.lp <= 0) {
                endGame('player');
            }
            return { damage, target: 'monster_lord' };
        }

        // Angriff auf Monster?
        if (targetCell.type === 'monster' && targetCell.owner === 'opponent') {
            const defender = targetCell.monster;
            const damage = calculateDamage(attacker, defender);

            defender.hp -= damage;
            addLog(`${attacker.name} greift ${defender.name} an! ${damage} Schaden!`);

            // Gegenangriff wenn Nahkampf
            if (distance === 1 && !attacker.ranged) {
                const counterDamage = Math.floor(defender.atk * 0.5);
                attacker.hp -= counterDamage;
                addLog(`${defender.name} kontert! ${counterDamage} Schaden!`);

                if (attacker.hp <= 0) {
                    destroyMonster(attacker, 'player');
                }
            }

            if (defender.hp <= 0) {
                destroyMonster(defender, 'opponent');
            }

            attacker.hasAttacked = true;
            return { damage, target: defender.name };
        }

        return null;
    }

    function calculateDamage(attacker, defender) {
        let baseDamage = attacker.atk;

        // Element-Bonus
        if (defender && attacker.element && defender.element) {
            const chart = ELEMENT_CHART[attacker.element];
            if (chart) {
                if (chart.strong.includes(defender.element)) {
                    baseDamage = Math.floor(baseDamage * 1.5);
                } else if (chart.weak.includes(defender.element)) {
                    baseDamage = Math.floor(baseDamage * 0.7);
                }
            }
        }

        // Defense abziehen wenn Verteidiger vorhanden
        if (defender) {
            baseDamage = Math.max(1, baseDamage - defender.def);
        }

        return baseDamage;
    }

    function destroyMonster(monster, owner) {
        const list = owner === 'player' ? gameState.player.monsters : gameState.opponent.monsters;
        const index = list.indexOf(monster);
        if (index > -1) {
            list.splice(index, 1);
        }

        const { x, y } = monster.position;
        gameState.grid[y][x] = { type: 'empty', monster: null, owner: null, terrain: null };

        addLog(`${monster.name} wurde zerstört!`);
    }

    function endPlayerTurn() {
        if (!gameState || !gameState.playerTurn) return;

        // Reset Monster-Status
        gameState.player.monsters.forEach(m => {
            m.movesLeft = m.movement;
            m.hasAttacked = false;
        });

        gameState.playerTurn = false;
        gameState.phase = 'roll';
        addLog(`--- ${gameState.opponent.name} ist dran ---`);

        // AI Zug nach kurzer Verzögerung
        setTimeout(() => opponentTurn(), 1000);
    }

    // ============================================
    // GEGNER AI
    // ============================================

    function opponentTurn() {
        if (!gameState || gameState.playerTurn || gameState.gameOver) return;

        const opponent = gameState.opponent;

        // 1. Würfeln
        if (opponent.dicePool.length > 0) {
            const diceIndex = Math.floor(Math.random() * opponent.dicePool.length);
            const diceId = opponent.dicePool[diceIndex];
            const result = rollDice(diceId);

            opponent.dicePool.splice(diceIndex, 1);
            opponent.usedDice.push(diceId);

            if (result.canSummon) {
                addLog(`${opponent.name} würfelt ${result.diceName}: BESCHWÖRUNG!`);
                // Finde Beschwörungsort
                const summonPos = findAISummonPosition();
                if (summonPos) {
                    aiSummonMonster(diceId, summonPos.x, summonPos.y);
                }
            } else {
                opponent.crests[result.result]++;
                addLog(`${opponent.name} würfelt: ${getCrestEmoji(result.result)} ${result.result}`);
            }
        }

        // 2. Monster bewegen und angreifen
        setTimeout(() => {
            opponent.monsters.forEach(monster => {
                // Finde Ziel
                const target = findAITarget(monster);
                if (target) {
                    // Bewege zum Ziel
                    const path = findPathTo(monster.position, target.position, monster.movesLeft);
                    if (path.length > 1) {
                        const newPos = path[path.length - 1];
                        gameState.grid[monster.position.y][monster.position.x] = { type: 'empty', monster: null, owner: null, terrain: null };
                        monster.position = newPos;
                        gameState.grid[newPos.y][newPos.x] = { type: 'monster', monster: monster, owner: 'opponent', terrain: null };
                        addLog(`${monster.name} bewegt sich`);
                    }

                    // Angreifen wenn in Reichweite
                    const distance = Math.abs(monster.position.x - target.position.x) + Math.abs(monster.position.y - target.position.y);
                    const maxRange = monster.ranged ? 3 : 1;

                    if (distance <= maxRange && !monster.hasAttacked) {
                        aiAttack(monster, target);
                    }
                }
            });

            // Zug beenden
            setTimeout(() => {
                opponent.monsters.forEach(m => {
                    m.movesLeft = m.movement;
                    m.hasAttacked = false;
                });

                gameState.playerTurn = true;
                gameState.phase = 'roll';
                gameState.turn++;
                addLog(`--- Runde ${gameState.turn}: Du bist dran ---`);
            }, 500);
        }, 800);
    }

    function findAISummonPosition() {
        const lord = gameState.opponent.monsterLordPos;
        const directions = [[0,1], [0,-1], [1,0], [-1,0], [1,1], [1,-1], [-1,1], [-1,-1]];

        for (const [dx, dy] of directions) {
            const x = lord.x + dx;
            const y = lord.y + dy;
            if (x >= 0 && x < GRID_SIZE && y >= 0 && y < GRID_SIZE) {
                const cell = gameState.grid[y][x];
                if (cell.type === 'empty') {
                    return { x, y };
                }
            }
        }
        return null;
    }

    function aiSummonMonster(diceId, x, y) {
        const dice = DICE_MONSTERS[diceId];
        if (!dice) return;

        const monster = {
            id: Date.now() + Math.random(),
            diceId: diceId,
            name: dice.name,
            atk: dice.atk,
            def: dice.def,
            hp: dice.hp,
            maxHp: dice.hp,
            element: dice.element,
            movement: dice.movement,
            movesLeft: dice.movement,
            hasAttacked: false,
            special: dice.special,
            ranged: dice.ranged || false,
            flying: dice.flying || false,
            owner: 'opponent',
            position: { x, y }
        };

        gameState.grid[y][x] = { type: 'monster', monster: monster, owner: 'opponent', terrain: null };
        gameState.opponent.monsters.push(monster);
        addLog(`${gameState.opponent.name} beschwört ${dice.name}!`);
    }

    function findAITarget(monster) {
        // Priorität: Monster Lord > Schwache Monster > Starke Monster
        const playerLord = gameState.player.monsterLordPos;
        const playerMonsters = gameState.player.monsters;

        // Monster Lord als Ziel wenn erreichbar
        const lordTarget = {
            position: playerLord,
            priority: 100,
            type: 'lord'
        };

        // Spieler-Monster als Ziele
        const targets = playerMonsters.map(m => ({
            position: m.position,
            monster: m,
            priority: 50 - m.hp,  // Schwächere Monster bevorzugen
            type: 'monster'
        }));

        targets.push(lordTarget);
        targets.sort((a, b) => b.priority - a.priority);

        return targets[0] || null;
    }

    function findPathTo(from, to, maxSteps) {
        // Vereinfachte Pfadfindung
        const path = [from];
        let current = { ...from };
        let steps = 0;

        while (steps < maxSteps) {
            const dx = Math.sign(to.x - current.x);
            const dy = Math.sign(to.y - current.y);

            if (dx === 0 && dy === 0) break;

            // Bevorzuge horizontale/vertikale Bewegung
            let nextX = current.x + dx;
            let nextY = current.y;

            if (dx === 0 || (dy !== 0 && Math.random() < 0.5)) {
                nextX = current.x;
                nextY = current.y + dy;
            }

            const cell = gameState.grid[nextY]?.[nextX];
            if (cell && cell.type === 'empty') {
                current = { x: nextX, y: nextY };
                path.push(current);
                steps++;
            } else {
                break;
            }
        }

        return path;
    }

    function aiAttack(attacker, target) {
        if (target.type === 'lord') {
            const damage = attacker.atk;
            gameState.player.lp -= damage;
            addLog(`${attacker.name} greift deinen Monster Lord an! ${damage} Schaden! (LP: ${gameState.player.lp})`);
            attacker.hasAttacked = true;

            if (gameState.player.lp <= 0) {
                endGame('opponent');
            }
        } else if (target.monster) {
            const damage = calculateDamage(attacker, target.monster);
            target.monster.hp -= damage;
            addLog(`${attacker.name} greift ${target.monster.name} an! ${damage} Schaden!`);

            if (target.monster.hp <= 0) {
                destroyMonster(target.monster, 'player');
            }
            attacker.hasAttacked = true;
        }
    }

    // ============================================
    // SPIELENDE
    // ============================================

    function endGame(winner) {
        gameState.gameOver = true;
        gameState.winner = winner;

        if (winner === 'player') {
            playerData.wins++;
            playerData.gold += 100;
            addLog('🎉 DU HAST GEWONNEN! +100 Gold');
        } else {
            playerData.losses++;
            addLog(`😢 ${gameState.opponent.name} hat gewonnen!`);
        }

        savePlayerData();
        syncToServer(winner);
    }

    async function syncToServer(winner) {
        try {
            await fetch('/api/dice-duel/end', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    match_id: Date.now(),
                    winner_id: winner === 'player' ? 'player1' : 'npc',
                    player1_hp: gameState.player.lp,
                    player2_hp: gameState.opponent.lp,
                    turns_played: gameState.turn,
                    gold_earned: winner === 'player' ? 100 : 0,
                    xp_earned: winner === 'player' ? 50 : 10
                })
            });
        } catch(e) {
            console.warn('DDM: Server sync fehlgeschlagen');
        }
    }

    // ============================================
    // UI RENDERING
    // ============================================

    function renderGameUI(container) {
        if (!gameState) {
            container.innerHTML = '<p style="color:#fff">Kein Spiel aktiv!</p>';
            return;
        }

        const html = `
            <div class="ddm-game-container">
                <!-- Header mit LP -->
                <div class="ddm-header">
                    <div class="ddm-player-info">
                        <span class="ddm-portrait">🧑</span>
                        <span class="ddm-name">Du</span>
                        <div class="ddm-lp">
                            <span class="ddm-lp-bar" style="width: ${(gameState.player.lp / STARTING_LP) * 100}%"></span>
                            <span class="ddm-lp-text">${gameState.player.lp} LP</span>
                        </div>
                    </div>
                    <div class="ddm-turn-info">
                        <span>Runde ${gameState.turn}</span>
                        <span class="ddm-phase">${getPhaseText()}</span>
                    </div>
                    <div class="ddm-opponent-info">
                        <span class="ddm-portrait">${gameState.opponent.portrait}</span>
                        <span class="ddm-name">${gameState.opponent.name}</span>
                        <div class="ddm-lp opponent">
                            <span class="ddm-lp-bar" style="width: ${(gameState.opponent.lp / STARTING_LP) * 100}%"></span>
                            <span class="ddm-lp-text">${gameState.opponent.lp} LP</span>
                        </div>
                    </div>
                </div>

                <!-- Spielfeld -->
                <div class="ddm-board" id="ddmBoard"></div>

                <!-- Würfel Pool -->
                <div class="ddm-dice-pool" id="ddmDicePool">
                    <h4>Dein Würfel-Pool (${gameState.player.dicePool.length} übrig)</h4>
                    <div class="ddm-dice-list" id="ddmDiceList"></div>
                </div>

                <!-- Crests -->
                <div class="ddm-crests">
                    <span title="Angriff">⚔️ ${gameState.player.crests.attack}</span>
                    <span title="Verteidigung">🛡️ ${gameState.player.crests.defense}</span>
                    <span title="Bewegung">👟 ${gameState.player.crests.movement}</span>
                    <span title="Magie">✨ ${gameState.player.crests.magic}</span>
                </div>

                <!-- Aktionen -->
                <div class="ddm-actions" id="ddmActions">
                    ${gameState.playerTurn && !gameState.gameOver ? `
                        ${gameState.phase === 'roll' ? '<button class="ddm-btn roll" onclick="DungeonDiceGame.promptRoll()">🎲 Würfeln</button>' : ''}
                        ${gameState.phase === 'action' ? '<button class="ddm-btn end-turn" onclick="DungeonDiceGame.endTurn()">⏭️ Zug beenden</button>' : ''}
                    ` : ''}
                    ${gameState.gameOver ? `
                        <div class="ddm-game-over">
                            <h2>${gameState.winner === 'player' ? '🎉 GEWONNEN!' : '😢 VERLOREN'}</h2>
                            <button class="ddm-btn" onclick="DungeonDiceGame.close()">Schließen</button>
                        </div>
                    ` : ''}
                </div>

                <!-- Log -->
                <div class="ddm-log" id="ddmLog"></div>
            </div>
        `;

        container.innerHTML = html;

        renderBoard();
        renderDicePool();
        renderLog();

        // Styles
        if (!document.getElementById('ddm-game-styles')) {
            const style = document.createElement('style');
            style.id = 'ddm-game-styles';
            style.textContent = getGameStyles();
            document.head.appendChild(style);
        }
    }

    function getPhaseText() {
        if (gameState.gameOver) return 'Spiel beendet';
        if (!gameState.playerTurn) return 'Gegner am Zug...';
        switch (gameState.phase) {
            case 'roll': return 'Würfeln!';
            case 'summon': return 'Beschwören!';
            case 'action': return 'Bewegen/Angreifen';
            default: return '';
        }
    }

    function renderBoard() {
        const board = document.getElementById('ddmBoard');
        if (!board) return;

        board.innerHTML = '';

        for (let y = GRID_SIZE - 1; y >= 0; y--) {  // Von oben nach unten
            for (let x = 0; x < GRID_SIZE; x++) {
                const cell = gameState.grid[y][x];
                const cellEl = document.createElement('div');
                cellEl.className = `ddm-cell ${cell.type} ${cell.owner || ''}`;
                cellEl.dataset.x = x;
                cellEl.dataset.y = y;

                if (cell.type === 'monster_lord') {
                    cellEl.innerHTML = cell.owner === 'player' ? '👑' : '💀';
                } else if (cell.type === 'monster' && cell.monster) {
                    const m = cell.monster;
                    const hpPercent = (m.hp / m.maxHp) * 100;
                    cellEl.innerHTML = `
                        <div class="ddm-monster ${m.owner}">
                            <span class="monster-icon">${getMonsterIcon(m)}</span>
                            <div class="monster-hp" style="width: ${hpPercent}%"></div>
                        </div>
                    `;
                    cellEl.title = `${m.name}\nATK: ${m.atk} DEF: ${m.def}\nHP: ${m.hp}/${m.maxHp}`;

                    if (m.owner === 'player' && gameState.playerTurn && gameState.phase === 'action') {
                        cellEl.onclick = () => selectMonster(m.id);
                    }
                } else if (cell.type === 'empty') {
                    // Klickbar für Beschwörung oder Bewegung
                    if (gameState.playerTurn) {
                        if (gameState.phase === 'summon' && canSummonAt(x, y, 'player')) {
                            cellEl.classList.add('summonable');
                            cellEl.onclick = () => summonMonster(x, y) && renderGameUI(document.getElementById('ddm-game-container')?.parentElement);
                        } else if (gameState.phase === 'action' && gameState.selectedMonster) {
                            cellEl.classList.add('moveable');
                            cellEl.onclick = () => {
                                moveMonster(gameState.selectedMonster, x, y);
                                renderGameUI(document.getElementById('ddm-game-container')?.parentElement);
                            };
                        }
                    }
                }

                // Attack target
                if (gameState.playerTurn && gameState.phase === 'action' && gameState.selectedMonster) {
                    if (cell.owner === 'opponent') {
                        cellEl.classList.add('attackable');
                        cellEl.onclick = () => {
                            attackWithMonster(gameState.selectedMonster, x, y);
                            gameState.selectedMonster = null;
                            renderGameUI(document.getElementById('ddm-game-container')?.parentElement);
                        };
                    }
                }

                board.appendChild(cellEl);
            }
        }
    }

    function getMonsterIcon(monster) {
        const element = monster.element;
        const icons = {
            fire: '🔥',
            water: '💧',
            earth: '🪨',
            wind: '🌪️',
            light: '✨',
            dark: '🌑',
            explosion: '💥'
        };
        return icons[element] || '⚔️';
    }

    function selectMonster(monsterId) {
        if (gameState.selectedMonster === monsterId) {
            gameState.selectedMonster = null;
        } else {
            gameState.selectedMonster = monsterId;
        }
        renderBoard();
    }

    function renderDicePool() {
        const list = document.getElementById('ddmDiceList');
        if (!list) return;

        list.innerHTML = '';
        gameState.player.dicePool.forEach((diceId, index) => {
            const dice = DICE_MONSTERS[diceId];
            if (!dice) return;

            const el = document.createElement('div');
            el.className = `ddm-dice-item rarity-${dice.rarity}`;
            el.innerHTML = `
                <span class="dice-icon">🎲</span>
                <span class="dice-name">${dice.name}</span>
            `;
            el.title = `${dice.name}\nATK: ${dice.atk} DEF: ${dice.def} HP: ${dice.hp}`;

            if (gameState.playerTurn && gameState.phase === 'roll') {
                el.classList.add('rollable');
                el.onclick = () => {
                    playerRollDice(index);
                    renderGameUI(document.getElementById('ddm-game-container')?.parentElement);
                };
            }

            list.appendChild(el);
        });
    }

    function renderLog() {
        const logEl = document.getElementById('ddmLog');
        if (!logEl) return;

        const recentLogs = gameState.log.slice(-8);
        logEl.innerHTML = recentLogs.map(l => `<div class="log-entry">${l.message}</div>`).join('');
        logEl.scrollTop = logEl.scrollHeight;
    }

    function promptRoll() {
        if (typeof showNotification === 'function') {
            showNotification('Klicke auf einen Würfel zum Werfen!');
        }
    }

    function endTurn() {
        endPlayerTurn();
        setTimeout(() => {
            const container = document.getElementById('ddm-game-container')?.parentElement;
            if (container) renderGameUI(container);
        }, 2000);
    }

    function getGameStyles() {
        return `
            .ddm-game-container {
                display: flex;
                flex-direction: column;
                gap: 10px;
                padding: 15px;
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                border-radius: 10px;
                color: #fff;
                max-width: 500px;
                margin: 0 auto;
            }
            .ddm-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 10px;
                background: rgba(0,0,0,0.3);
                border-radius: 8px;
            }
            .ddm-player-info, .ddm-opponent-info {
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 5px;
            }
            .ddm-portrait { font-size: 24px; }
            .ddm-name { font-size: 12px; color: #aaa; }
            .ddm-lp {
                width: 80px;
                height: 12px;
                background: #333;
                border-radius: 6px;
                position: relative;
                overflow: hidden;
            }
            .ddm-lp-bar {
                position: absolute;
                height: 100%;
                background: linear-gradient(90deg, #4CAF50, #8BC34A);
                transition: width 0.3s;
            }
            .ddm-lp.opponent .ddm-lp-bar {
                background: linear-gradient(90deg, #f44336, #FF5722);
            }
            .ddm-lp-text {
                position: absolute;
                width: 100%;
                text-align: center;
                font-size: 10px;
                line-height: 12px;
                color: #fff;
                text-shadow: 0 0 2px #000;
            }
            .ddm-turn-info {
                text-align: center;
            }
            .ddm-phase {
                display: block;
                font-size: 14px;
                color: #4CAF50;
                font-weight: bold;
            }
            .ddm-board {
                display: grid;
                grid-template-columns: repeat(${GRID_SIZE}, 1fr);
                gap: 3px;
                background: #0a0a0a;
                padding: 8px;
                border-radius: 8px;
                border: 2px solid #333;
            }
            .ddm-cell {
                aspect-ratio: 1;
                background: #1a1a1a;
                border: 1px solid #333;
                border-radius: 4px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 18px;
                transition: all 0.2s;
            }
            .ddm-cell.monster_lord {
                background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
                font-size: 22px;
            }
            .ddm-cell.monster_lord.player { border-color: #4169e1; }
            .ddm-cell.monster_lord.opponent { border-color: #ff69b4; }
            .ddm-cell.summonable {
                background: rgba(76,175,80,0.3);
                border-color: #4CAF50;
                cursor: pointer;
            }
            .ddm-cell.summonable:hover { background: rgba(76,175,80,0.5); }
            .ddm-cell.moveable {
                background: rgba(33,150,243,0.2);
                border-color: #2196F3;
                cursor: pointer;
            }
            .ddm-cell.moveable:hover { background: rgba(33,150,243,0.4); }
            .ddm-cell.attackable {
                background: rgba(244,67,54,0.3);
                border-color: #f44336;
                cursor: pointer;
            }
            .ddm-cell.attackable:hover { background: rgba(244,67,54,0.5); }
            .ddm-monster {
                width: 100%;
                height: 100%;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                position: relative;
                border-radius: 4px;
            }
            .ddm-monster.player { background: rgba(65,105,225,0.3); }
            .ddm-monster.opponent { background: rgba(255,105,180,0.3); }
            .monster-icon { font-size: 20px; }
            .monster-hp {
                position: absolute;
                bottom: 0;
                left: 0;
                height: 3px;
                background: #4CAF50;
                border-radius: 0 0 4px 4px;
            }
            .ddm-dice-pool {
                background: rgba(0,0,0,0.3);
                padding: 10px;
                border-radius: 8px;
            }
            .ddm-dice-pool h4 { margin: 0 0 10px 0; font-size: 12px; color: #aaa; }
            .ddm-dice-list {
                display: flex;
                flex-wrap: wrap;
                gap: 5px;
            }
            .ddm-dice-item {
                padding: 5px 8px;
                background: #2a2a2a;
                border: 2px solid #444;
                border-radius: 5px;
                font-size: 11px;
                display: flex;
                align-items: center;
                gap: 5px;
            }
            .ddm-dice-item.rollable {
                cursor: pointer;
                border-color: #4CAF50;
            }
            .ddm-dice-item.rollable:hover {
                background: rgba(76,175,80,0.3);
            }
            .ddm-dice-item.rarity-common { border-color: #888; }
            .ddm-dice-item.rarity-uncommon { border-color: #4CAF50; }
            .ddm-dice-item.rarity-rare { border-color: #2196F3; }
            .ddm-dice-item.rarity-epic { border-color: #9C27B0; }
            .ddm-dice-item.rarity-legendary { border-color: #FFD700; background: rgba(255,215,0,0.1); }
            .ddm-crests {
                display: flex;
                justify-content: center;
                gap: 15px;
                padding: 8px;
                background: rgba(0,0,0,0.2);
                border-radius: 5px;
            }
            .ddm-crests span {
                font-size: 14px;
            }
            .ddm-actions {
                display: flex;
                justify-content: center;
                gap: 10px;
                padding: 10px;
            }
            .ddm-btn {
                padding: 10px 20px;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-size: 14px;
                font-weight: bold;
                transition: all 0.2s;
            }
            .ddm-btn:hover { transform: scale(1.05); }
            .ddm-btn.roll { background: #4CAF50; color: white; }
            .ddm-btn.end-turn { background: #FF9800; color: white; }
            .ddm-game-over {
                text-align: center;
            }
            .ddm-game-over h2 {
                margin: 0 0 15px 0;
            }
            .ddm-log {
                max-height: 80px;
                overflow-y: auto;
                padding: 8px;
                background: rgba(0,0,0,0.4);
                border-radius: 5px;
                font-size: 11px;
                color: #aaa;
            }
            .log-entry {
                padding: 2px 0;
                border-bottom: 1px solid rgba(255,255,255,0.1);
            }
        `;
    }

    // ============================================
    // UI DIALOG
    // ============================================

    let dialogContainer = null;

    function openGame(opponentId) {
        const game = createGame(opponentId);
        if (!game) {
            if (typeof showNotification === 'function') {
                showNotification('Gegner nicht gefunden!');
            }
            return;
        }

        // Dialog erstellen
        const overlay = document.createElement('div');
        overlay.id = 'ddm-game-overlay';
        overlay.style.cssText = `
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0,0,0,0.9);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10001;
        `;

        const dialog = document.createElement('div');
        dialog.id = 'ddm-game-dialog';
        dialog.style.cssText = `
            position: relative;
            max-height: 90vh;
            overflow-y: auto;
        `;

        const closeBtn = document.createElement('button');
        closeBtn.textContent = '✕';
        closeBtn.style.cssText = `
            position: absolute;
            top: 10px;
            right: 10px;
            background: #f44336;
            border: none;
            color: white;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            cursor: pointer;
            z-index: 10;
            font-size: 16px;
        `;
        closeBtn.onclick = close;

        dialog.appendChild(closeBtn);
        overlay.appendChild(dialog);
        document.body.appendChild(overlay);

        dialogContainer = dialog;
        renderGameUI(dialog);
    }

    function close() {
        const overlay = document.getElementById('ddm-game-overlay');
        if (overlay) {
            overlay.remove();
        }
        gameState = null;
        dialogContainer = null;
    }

    // ============================================
    // INITIALISIERUNG
    // ============================================

    loadPlayerData();

    return {
        // Spiel starten
        startGame: openGame,
        close: close,

        // Aktionen
        promptRoll: promptRoll,
        endTurn: endTurn,

        // Daten
        getState: () => gameState,
        getPlayerData: () => playerData,
        getDiceMonsters: () => DICE_MONSTERS,
        getNPCs: () => NPC_OPPONENTS,

        // UI
        render: renderGameUI
    };
})();

window.DungeonDiceGame = DungeonDiceGame;

console.log('🎲 Dungeon Dice Monsters Gameplay System geladen');
