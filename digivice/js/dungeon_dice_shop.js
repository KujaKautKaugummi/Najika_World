/**
 * DUNGEON DICE MONSTERS - Stadt-Läden System (Yu-Gi-Oh! Inspired)
 *
 * Dungeon Dice ist NUR in Städten spielbar (zu komplex für überall)
 * Jede Stadt hat einen "Würfelmeister" Laden
 *
 * Erstellt: 2025-12-12
 */

const DungeonDiceShop = (function() {
    'use strict';

    // ============================================
    // SHOP STANDORTE (in Städten)
    // ============================================

    const SHOP_LOCATIONS = {
        'handelsfestung': {
            name: "Goldenes Würfelhaus",
            shopkeeper: "Meister Roldan",
            city: "Handelsfestung (Heiße Dünen)",
            specializes: "legendary",
            portrait: "🎲",
            dialogue: {
                welcome: "Willkommen im besten Würfelladen der Wüste! Ich bin Meister Roldan.",
                buy: "Ausgezeichnete Wahl! Die Würfel werden dir Glück bringen.",
                challenge: "Du willst gegen mich spielen? Mutig! Ich bin Champion der Handelsfestung!"
            }
        },
        'dampf_hain': {
            name: "Nebel-Spielhalle",
            shopkeeper: "Alte Meisterin Yuki",
            city: "Dampf-Hain (Samtmoos-Tiefwald)",
            specializes: "earth",
            portrait: "🧓",
            dialogue: {
                welcome: "Die Würfel der Druiden sind magisch... willkommen, junger Reisender.",
                buy: "Diese Würfel wurden im heißen Dampf gehärtet. Stark wie der Wald.",
                challenge: "Du möchtest die Weisheit der Würfel testen? Komm, setze dich."
            }
        },
        'salzige_bucht': {
            name: "Piraten-Würfelkajüte",
            shopkeeper: "Käpt'n Wurfbein",
            city: "Salzige Bucht (Salzwind-Küste)",
            specializes: "water",
            portrait: "🏴‍☠️",
            dialogue: {
                welcome: "Yarr! Willkommen in meiner Würfelkajüte! Ich bin Käpt'n Wurfbein!",
                buy: "Diese Würfel haben Schiffbrüche überlebt! Stark wie das Meer!",
                challenge: "Ein Würfelduell? Ich hab noch nie gegen einen Landratten verloren!"
            }
        },
        'runenheim': {
            name: "Runen-Akademie Spielzimmer",
            shopkeeper: "Magister Hexus",
            city: "Runenheim (Blitzebene)",
            specializes: "lightning",
            portrait: "🧙‍♂️",
            dialogue: {
                welcome: "Die Akademie begrüßt dich. Würfel sind auch eine Form der Magie.",
                buy: "Mit Runen verzierte Würfel... sie werden dich nicht enttäuschen.",
                challenge: "Ein intellektuelles Duell? Faszinierend. Möge der klügere gewinnen."
            }
        },
        'funken_siedlung': {
            name: "Glut & Würfel",
            shopkeeper: "Schmied Ignis",
            city: "Funken-Siedlung (Magmaströme)",
            specializes: "fire",
            portrait: "🔥",
            dialogue: {
                welcome: "Heiß hier, was? Aber meine Würfel sind noch heißer! Willkommen!",
                buy: "Im Vulkanfeuer geschmiedet! Diese Würfel sind unzerstörbar!",
                challenge: "Du willst spielen? Ich warne dich, ich bin so heiß wie meine Schmiede!"
            }
        }
    };

    // ============================================
    // WÜRFEL-MONSTER DATENBANK
    // ============================================

    const DICE_MONSTERS = {
        // Starter (jeder hat diese)
        'warrior_die': { name: "Krieger-Würfel", atk: 3, def: 2, summonCost: 1, element: null, rarity: 'common', price: 50 },
        'shield_die': { name: "Schild-Würfel", atk: 1, def: 4, summonCost: 1, element: null, rarity: 'common', price: 50 },
        'archer_die': { name: "Bogenschützen-Würfel", atk: 4, def: 1, summonCost: 1, element: null, rarity: 'common', price: 50 },

        // Uncommon
        'flame_knight': { name: "Flammen-Ritter", atk: 4, def: 3, summonCost: 2, element: 'fire', rarity: 'uncommon', price: 150 },
        'frost_golem': { name: "Frost-Golem", atk: 3, def: 5, summonCost: 2, element: 'ice', rarity: 'uncommon', price: 150 },
        'thunder_hawk': { name: "Donner-Falke", atk: 5, def: 2, summonCost: 2, element: 'lightning', rarity: 'uncommon', price: 150 },
        'earth_titan': { name: "Erd-Titan", atk: 2, def: 6, summonCost: 2, element: 'earth', rarity: 'uncommon', price: 150 },
        'sea_serpent': { name: "See-Schlange", atk: 4, def: 4, summonCost: 2, element: 'water', rarity: 'uncommon', price: 150 },

        // Rare
        'dark_magician': { name: "Dunkler Magier", atk: 6, def: 4, summonCost: 3, element: 'dark', rarity: 'rare', price: 400 },
        'angel_warrior': { name: "Engel-Krieger", atk: 5, def: 5, summonCost: 3, element: 'light', rarity: 'rare', price: 400 },
        'dragon_knight': { name: "Drachen-Ritter", atk: 7, def: 3, summonCost: 3, element: 'fire', rarity: 'rare', price: 400 },
        'crystal_beast': { name: "Kristall-Bestie", atk: 4, def: 7, summonCost: 3, element: 'earth', rarity: 'rare', price: 400 },

        // Epic (Shop-exklusiv pro Stadt)
        'volcano_lord': { name: "Vulkan-Lord", atk: 8, def: 5, summonCost: 4, element: 'fire', rarity: 'epic', price: 1000, shop: 'funken_siedlung' },
        'storm_emperor': { name: "Sturm-Kaiser", atk: 7, def: 6, summonCost: 4, element: 'lightning', rarity: 'epic', price: 1000, shop: 'runenheim' },
        'forest_ancient': { name: "Wald-Urvater", atk: 6, def: 8, summonCost: 4, element: 'earth', rarity: 'epic', price: 1000, shop: 'dampf_hain' },
        'leviathan': { name: "Leviathan", atk: 9, def: 4, summonCost: 4, element: 'water', rarity: 'epic', price: 1000, shop: 'salzige_bucht' },
        'gold_dragon': { name: "Gold-Drache", atk: 8, def: 7, summonCost: 5, element: null, rarity: 'epic', price: 1500, shop: 'handelsfestung' },

        // Legendary (sehr selten, Quest-Belohnungen)
        'najika_explosion': { name: "Najika Explosion", atk: 10, def: 1, summonCost: 5, element: 'fire', rarity: 'legendary', price: 5000 },
        'god_die': { name: "Götter-Würfel", atk: 9, def: 9, summonCost: 6, element: null, rarity: 'legendary', price: 10000 }
    };

    // ============================================
    // SPIELER INVENTAR
    // ============================================

    let playerInventory = {
        dice: ['warrior_die', 'shield_die', 'archer_die'],
        deck: ['warrior_die', 'shield_die', 'archer_die'],
        gold: 500,
        wins: 0,
        losses: 0
    };

    function loadInventory() {
        const saved = localStorage.getItem('dungeonDice_inventory');
        if (saved) {
            try {
                playerInventory = JSON.parse(saved);
            } catch(e) {
                console.error('Dungeon Dice: Fehler beim Laden');
            }
        }
    }

    function saveInventory() {
        localStorage.setItem('dungeonDice_inventory', JSON.stringify(playerInventory));
    }

    // ============================================
    // SHOP SYSTEM
    // ============================================

    let currentShop = null;
    let shopOpen = false;

    function openShop(shopId) {
        const shop = SHOP_LOCATIONS[shopId];
        if (!shop) {
            if (typeof showNotification === 'function') {
                showNotification('Kein Würfelladen hier!');
            }
            return;
        }

        currentShop = shopId;
        shopOpen = true;

        const overlay = document.createElement('div');
        overlay.id = 'dice-shop-overlay';
        overlay.innerHTML = `
            <div class="dice-shop-dialog">
                <div class="dice-shop-header">
                    <h2>🎲 ${shop.name}</h2>
                    <button class="dice-close-btn" onclick="DungeonDiceShop.close()">✕</button>
                </div>
                <div class="dice-shop-content">
                    <div class="shopkeeper-area">
                        <div class="shopkeeper-portrait">${shop.portrait}</div>
                        <div class="shopkeeper-info">
                            <h3>${shop.shopkeeper}</h3>
                            <p class="shopkeeper-dialogue">"${shop.dialogue.welcome}"</p>
                            <p class="shop-city">📍 ${shop.city}</p>
                        </div>
                    </div>
                    <div class="player-gold">
                        💰 Gold: <strong>${playerInventory.gold}</strong>
                    </div>
                </div>
                <div class="dice-shop-actions">
                    <button class="dice-btn buy" onclick="DungeonDiceShop.showBuyMenu()">🛒 Kaufen</button>
                    <button class="dice-btn play" onclick="DungeonDiceShop.challengeShopkeeper()">⚔️ Herausfordern</button>
                    <button class="dice-btn inventory" onclick="DungeonDiceShop.showInventory()">📦 Inventar</button>
                    <button class="dice-btn cancel" onclick="DungeonDiceShop.close()">Verlassen</button>
                </div>
            </div>
        `;

        if (!document.getElementById('dice-shop-styles')) {
            const style = document.createElement('style');
            style.id = 'dice-shop-styles';
            style.textContent = getShopStyles();
            document.head.appendChild(style);
        }

        document.body.appendChild(overlay);
    }

    function showBuyMenu() {
        const shop = SHOP_LOCATIONS[currentShop];
        const overlay = document.getElementById('dice-shop-overlay');
        if (!overlay) return;

        const dialog = overlay.querySelector('.dice-shop-dialog');
        if (!dialog) return;

        // Filtere Würfel nach Shop
        const availableDice = Object.entries(DICE_MONSTERS).filter(([id, die]) => {
            // Shop-exklusive Würfel
            if (die.shop && die.shop !== currentShop) return false;
            // Legendary nur in speziellen Shops
            if (die.rarity === 'legendary' && currentShop !== 'handelsfestung') return false;
            return true;
        });

        dialog.innerHTML = `
            <div class="dice-shop-header">
                <h2>🛒 Würfel kaufen</h2>
                <button class="dice-close-btn" onclick="DungeonDiceShop.backToMain()">←</button>
            </div>
            <div class="dice-buy-content">
                <p class="player-gold">💰 Gold: <strong>${playerInventory.gold}</strong></p>
                <div class="dice-grid" id="diceShopGrid"></div>
            </div>
        `;

        const grid = document.getElementById('diceShopGrid');
        availableDice.forEach(([id, die]) => {
            const owned = playerInventory.dice.includes(id);
            const canBuy = playerInventory.gold >= die.price && !owned;

            const dieEl = document.createElement('div');
            dieEl.className = `dice-item ${owned ? 'owned' : ''} ${canBuy ? 'buyable' : ''}`;
            dieEl.innerHTML = `
                <div class="die-icon rarity-${die.rarity}">🎲</div>
                <div class="die-name">${die.name}</div>
                <div class="die-stats">ATK:${die.atk} DEF:${die.def}</div>
                <div class="die-element">${die.element ? getElementEmoji(die.element) : '⚪'}</div>
                <div class="die-price">${owned ? '✓ Besitzt' : `💰 ${die.price}`}</div>
            `;

            if (canBuy) {
                dieEl.onclick = () => buyDie(id);
            }

            grid.appendChild(dieEl);
        });
    }

    function buyDie(dieId) {
        const die = DICE_MONSTERS[dieId];
        if (!die) return;

        if (playerInventory.gold < die.price) {
            if (typeof showNotification === 'function') {
                showNotification('Nicht genug Gold!');
            }
            return;
        }

        if (playerInventory.dice.includes(dieId)) {
            if (typeof showNotification === 'function') {
                showNotification('Du besitzt diesen Würfel bereits!');
            }
            return;
        }

        playerInventory.gold -= die.price;
        playerInventory.dice.push(dieId);
        saveInventory();

        // Gold auch im zentralen Player-Objekt aktualisieren
        if (window.player) {
            window.player.gold = playerInventory.gold;
        }

        // GameEvent emittieren
        if (window.GameEvents) {
            window.GameEvents.emit('itemPurchased', { itemId: dieId, price: die.price, type: 'dice' });
        }

        const shop = SHOP_LOCATIONS[currentShop];
        if (typeof showNotification === 'function') {
            showNotification(`${shop.shopkeeper}: "${shop.dialogue.buy}"`);
        }

        showBuyMenu(); // Refresh
    }

    function showInventory() {
        const overlay = document.getElementById('dice-shop-overlay');
        if (!overlay) return;

        const dialog = overlay.querySelector('.dice-shop-dialog');
        if (!dialog) return;

        dialog.innerHTML = `
            <div class="dice-shop-header">
                <h2>📦 Dein Würfel-Inventar</h2>
                <button class="dice-close-btn" onclick="DungeonDiceShop.backToMain()">←</button>
            </div>
            <div class="dice-inventory-content">
                <p>Siege: <strong>${playerInventory.wins}</strong> | Niederlagen: <strong>${playerInventory.losses}</strong></p>
                <h3>Dein Deck (${playerInventory.deck.length} Würfel):</h3>
                <div class="deck-display" id="deckDisplay"></div>
                <hr>
                <h3>Alle Würfel:</h3>
                <div class="dice-grid" id="inventoryGrid"></div>
            </div>
        `;

        // Deck anzeigen
        const deckDisplay = document.getElementById('deckDisplay');
        playerInventory.deck.forEach((id, idx) => {
            const die = DICE_MONSTERS[id];
            if (!die) return;
            const el = document.createElement('div');
            el.className = 'deck-die';
            el.innerHTML = `
                <span class="die-icon rarity-${die.rarity}">🎲</span>
                <span>${die.name}</span>
            `;
            el.onclick = () => removeFromDeck(idx);
            deckDisplay.appendChild(el);
        });

        // Inventar anzeigen
        const invGrid = document.getElementById('inventoryGrid');
        playerInventory.dice.forEach(id => {
            const die = DICE_MONSTERS[id];
            if (!die) return;
            const inDeck = playerInventory.deck.includes(id);
            const el = document.createElement('div');
            el.className = `dice-item ${inDeck ? 'in-deck' : ''}`;
            el.innerHTML = `
                <div class="die-icon rarity-${die.rarity}">🎲</div>
                <div class="die-name">${die.name}</div>
                <div class="die-stats">ATK:${die.atk} DEF:${die.def}</div>
            `;
            if (!inDeck) {
                el.onclick = () => addToDeck(id);
            }
            invGrid.appendChild(el);
        });
    }

    function addToDeck(dieId) {
        if (playerInventory.deck.length >= 10) {
            if (typeof showNotification === 'function') {
                showNotification('Deck ist voll! (Max 10 Würfel)');
            }
            return;
        }
        playerInventory.deck.push(dieId);
        saveInventory();
        showInventory();
    }

    function removeFromDeck(index) {
        if (playerInventory.deck.length <= 3) {
            if (typeof showNotification === 'function') {
                showNotification('Deck braucht mindestens 3 Würfel!');
            }
            return;
        }
        playerInventory.deck.splice(index, 1);
        saveInventory();
        showInventory();
    }

    function challengeShopkeeper() {
        const shop = SHOP_LOCATIONS[currentShop];
        if (typeof showNotification === 'function') {
            showNotification(`${shop.shopkeeper}: "${shop.dialogue.challenge}"`);
        }

        // Shop schließen und Spiel starten
        close();

        // NPC ID aus Shop-ID ableiten
        const npcMapping = {
            'handelsfestung': 'roldan',
            'dampf_hain': 'yuki',
            'salzige_bucht': 'wurfbein',
            'runenheim': 'hexus',
            'funken_siedlung': 'ignis'
        };

        const npcId = npcMapping[currentShop];

        if (npcId && window.DungeonDiceGame) {
            setTimeout(() => {
                window.DungeonDiceGame.startGame(npcId);
            }, 500);
        } else {
            if (typeof showNotification === 'function') {
                showNotification('Dungeon Dice Game wird geladen...');
            }
        }
    }

    function backToMain() {
        if (currentShop) {
            close();
            openShop(currentShop);
        }
    }

    function close() {
        const overlay = document.getElementById('dice-shop-overlay');
        if (overlay) overlay.remove();
        shopOpen = false;
    }

    function getElementEmoji(element) {
        const emojis = {
            'fire': '🔥', 'ice': '❄️', 'earth': '🪨',
            'dark': '🌑', 'light': '✨', 'lightning': '⚡', 'water': '💧'
        };
        return emojis[element] || '⚪';
    }

    function getShopStyles() {
        return `
            #dice-shop-overlay {
                position: fixed;
                top: 0; left: 0; right: 0; bottom: 0;
                background: rgba(0,0,0,0.9);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 10000;
            }
            .dice-shop-dialog {
                background: linear-gradient(135deg, #2d1b4e, #1a1a2e);
                border: 3px solid #9C27B0;
                border-radius: 15px;
                padding: 20px;
                min-width: 450px;
                max-width: 600px;
                max-height: 80vh;
                overflow-y: auto;
                color: #fff;
                box-shadow: 0 0 40px rgba(156,39,176,0.4);
            }
            .dice-shop-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 15px;
                border-bottom: 2px solid #9C27B0;
                padding-bottom: 10px;
            }
            .dice-shop-header h2 {
                margin: 0;
                color: #E1BEE7;
            }
            .dice-close-btn {
                background: #ff4444;
                border: none;
                color: white;
                width: 30px; height: 30px;
                border-radius: 50%;
                cursor: pointer;
                font-size: 16px;
            }
            .shopkeeper-area {
                display: flex;
                gap: 15px;
                align-items: center;
                margin-bottom: 15px;
            }
            .shopkeeper-portrait {
                font-size: 50px;
                background: rgba(255,255,255,0.1);
                padding: 15px;
                border-radius: 10px;
            }
            .shopkeeper-info h3 { margin: 0 0 5px 0; color: #FFD700; }
            .shopkeeper-dialogue { font-style: italic; color: #aaa; margin: 5px 0; }
            .shop-city { font-size: 12px; color: #888; }
            .player-gold {
                background: rgba(255,215,0,0.1);
                padding: 10px;
                border-radius: 5px;
                text-align: center;
            }
            .dice-shop-actions {
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
                margin-top: 15px;
            }
            .dice-btn {
                padding: 12px 20px;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-size: 14px;
                font-weight: bold;
                transition: all 0.2s;
            }
            .dice-btn:hover { transform: scale(1.05); }
            .dice-btn.buy { background: #4CAF50; color: white; }
            .dice-btn.play { background: #E91E63; color: white; }
            .dice-btn.inventory { background: #2196F3; color: white; }
            .dice-btn.cancel { background: #666; color: white; }
            .dice-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
                gap: 10px;
                max-height: 300px;
                overflow-y: auto;
                padding: 10px;
                background: rgba(0,0,0,0.3);
                border-radius: 8px;
            }
            .dice-item {
                padding: 10px;
                background: rgba(255,255,255,0.05);
                border: 2px solid #444;
                border-radius: 8px;
                text-align: center;
                transition: all 0.2s;
            }
            .dice-item.buyable { cursor: pointer; border-color: #4CAF50; }
            .dice-item.buyable:hover { background: rgba(76,175,80,0.2); }
            .dice-item.owned { opacity: 0.6; }
            .dice-item.in-deck { border-color: #2196F3; background: rgba(33,150,243,0.1); }
            .die-icon { font-size: 30px; display: block; }
            .die-icon.rarity-common { filter: grayscale(50%); }
            .die-icon.rarity-uncommon { filter: hue-rotate(120deg); }
            .die-icon.rarity-rare { filter: hue-rotate(200deg); }
            .die-icon.rarity-epic { filter: hue-rotate(280deg) brightness(1.2); }
            .die-icon.rarity-legendary { filter: hue-rotate(45deg) brightness(1.5) drop-shadow(0 0 5px gold); }
            .die-name { font-size: 11px; color: #fff; margin: 5px 0; }
            .die-stats { font-size: 10px; color: #aaa; }
            .die-element { font-size: 14px; }
            .die-price { font-size: 11px; color: #FFD700; margin-top: 5px; }
            .deck-display {
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
                padding: 10px;
                background: rgba(0,0,0,0.2);
                border-radius: 5px;
                margin: 10px 0;
            }
            .deck-die {
                display: flex;
                align-items: center;
                gap: 5px;
                padding: 5px 10px;
                background: rgba(33,150,243,0.2);
                border: 1px solid #2196F3;
                border-radius: 5px;
                cursor: pointer;
                font-size: 12px;
            }
            .deck-die:hover { background: rgba(244,67,54,0.2); border-color: #f44336; }
        `;
    }

    // Initialisierung
    loadInventory();

    return {
        openShop: openShop,
        close: close,
        showBuyMenu: showBuyMenu,
        showInventory: showInventory,
        challengeShopkeeper: challengeShopkeeper,
        backToMain: backToMain,
        getShops: () => SHOP_LOCATIONS,
        getInventory: () => playerInventory,
        isOpen: () => shopOpen
    };
})();

window.DungeonDiceShop = DungeonDiceShop;

console.log('🎲 Dungeon Dice Shop System geladen');
