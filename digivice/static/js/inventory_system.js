/**
 * NAJIKA WORLD - INVENTAR-SYSTEM
 * ================================
 *
 * Komplettes Item-Management System mit:
 * - 50 Item-Slots
 * - Equipment-Slots (Weapon L/R, Armor, Accessories)
 * - Item-Typen: Food, Weapons, Armor, Quest Items, Materials
 * - Drag & Drop
 * - Integration mit Food-System und Combat-System
 */

class InventorySystem {
    constructor(foodSystem = null, combatSystem = null) {
        // Dependencies
        this.foodSystem = foodSystem;
        this.combatSystem = combatSystem;

        // Inventory Storage
        this.items = []; // Max 50 items
        this.maxSlots = 50;

        // Equipment Slots
        this.equipment = {
            weapon_left: null,
            weapon_right: null,
            armor_head: null,
            armor_chest: null,
            armor_legs: null,
            accessory_1: null,
            accessory_2: null
        };

        // ===== HOTBAR SYSTEM (8 Quick-Slots) =====
        this.hotbar = [null, null, null, null, null, null, null, null]; // 8 slots (Tasten 1-8)
        this.hotbarCooldowns = [0, 0, 0, 0, 0, 0, 0, 0]; // Cooldowns pro Slot
        this.selectedHotbarSlot = 0; // Aktuell ausgewählter Slot

        // Player Stats (Gold, etc.)
        this.gold = 100; // Starting gold

        // Item Database
        this.itemDatabase = this.loadItemDatabase();

        // Initialize Hotbar UI + Keyboard Events
        this.initHotbarUI();
        this.initHotbarKeyboard();

        console.log('📦 Inventar-System initialisiert');
        console.log('🎮 Hotbar-System aktiviert (Tasten 1-8)');
    }

    // ===== HOTBAR UI INITIALIZATION =====
    initHotbarUI() {
        // Create Hotbar Container if it doesn't exist
        if (!document.getElementById('hotbar-container')) {
            const hotbarHTML = `
                <div id="hotbar-container">
                    <div id="hotbar">
                        ${[1,2,3,4,5,6,7,8].map(i => `
                            <div class="hotbar-slot" id="hotbar-slot-${i-1}" data-slot="${i-1}">
                                <div class="hotbar-icon"></div>
                                <div class="hotbar-quantity"></div>
                                <div class="hotbar-cooldown"></div>
                                <div class="hotbar-key">${i}</div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;

            const hotbarStyle = `
                <style id="hotbar-styles">
                    #hotbar-container {
                        position: fixed;
                        bottom: 20px;
                        left: 50%;
                        transform: translateX(-50%);
                        z-index: 500;
                        pointer-events: auto;
                    }
                    #hotbar {
                        display: flex;
                        gap: 4px;
                        background: rgba(0, 0, 0, 0.85);
                        padding: 8px;
                        border-radius: 12px;
                        border: 2px solid #4CAF50;
                        box-shadow: 0 0 20px rgba(76, 175, 80, 0.3);
                    }
                    .hotbar-slot {
                        width: 56px;
                        height: 56px;
                        background: rgba(40, 40, 60, 0.9);
                        border: 2px solid #555;
                        border-radius: 8px;
                        position: relative;
                        cursor: pointer;
                        transition: all 0.15s ease;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                    }
                    .hotbar-slot:hover {
                        border-color: #4CAF50;
                        transform: translateY(-3px);
                        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.4);
                    }
                    .hotbar-slot.selected {
                        border-color: #FFD700;
                        box-shadow: 0 0 15px rgba(255, 215, 0, 0.5);
                        background: rgba(60, 60, 80, 0.9);
                    }
                    .hotbar-slot.on-cooldown {
                        opacity: 0.6;
                    }
                    .hotbar-icon {
                        font-size: 28px;
                        text-align: center;
                        line-height: 1;
                    }
                    .hotbar-quantity {
                        position: absolute;
                        bottom: 2px;
                        right: 4px;
                        font-size: 11px;
                        font-weight: bold;
                        color: #fff;
                        text-shadow: 1px 1px 2px #000;
                    }
                    .hotbar-cooldown {
                        position: absolute;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 0%;
                        background: rgba(0, 0, 0, 0.7);
                        border-radius: 6px;
                        transition: height 0.1s linear;
                        pointer-events: none;
                    }
                    .hotbar-key {
                        position: absolute;
                        top: 2px;
                        left: 4px;
                        font-size: 10px;
                        color: #888;
                        font-weight: bold;
                    }
                    .hotbar-slot.empty .hotbar-icon {
                        color: #444;
                    }
                    /* Rarity colors */
                    .hotbar-slot.rarity-common { border-color: #888; }
                    .hotbar-slot.rarity-uncommon { border-color: #2ecc71; }
                    .hotbar-slot.rarity-rare { border-color: #3498db; }
                    .hotbar-slot.rarity-epic { border-color: #9b59b6; }
                    .hotbar-slot.rarity-legendary { border-color: #f39c12; }
                    .hotbar-slot.rarity-quest { border-color: #e74c3c; }
                </style>
            `;

            // Insert styles
            document.head.insertAdjacentHTML('beforeend', hotbarStyle);
            // Insert hotbar
            document.body.insertAdjacentHTML('beforeend', hotbarHTML);

            // Add click handlers
            document.querySelectorAll('.hotbar-slot').forEach(slot => {
                slot.addEventListener('click', (e) => {
                    const slotIndex = parseInt(slot.dataset.slot);
                    this.useHotbarSlot(slotIndex);
                });
                slot.addEventListener('contextmenu', (e) => {
                    e.preventDefault();
                    const slotIndex = parseInt(slot.dataset.slot);
                    this.clearHotbarSlot(slotIndex);
                });
            });
        }
    }

    // ===== HOTBAR KEYBOARD EVENTS =====
    initHotbarKeyboard() {
        window.addEventListener('keydown', (e) => {
            // Skip if typing in input/textarea
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

            // Number keys 1-8 for hotbar
            const key = parseInt(e.key);
            if (key >= 1 && key <= 8) {
                e.preventDefault();
                this.useHotbarSlot(key - 1);
            }
        });
    }

    // ===== HOTBAR SLOT MANAGEMENT =====
    assignToHotbar(slotIndex, itemId) {
        if (slotIndex < 0 || slotIndex >= 8) {
            console.error('❌ Ungültiger Hotbar-Slot:', slotIndex);
            return false;
        }

        const item = this.items.find(i => i.id === itemId);
        if (!item) {
            console.error('❌ Item nicht im Inventar:', itemId);
            return false;
        }

        this.hotbar[slotIndex] = {
            id: itemId,
            data: item.data
        };

        console.log(`🎮 Hotbar Slot ${slotIndex + 1}: ${item.data.icon} ${item.data.name}`);
        this.updateHotbarUI();
        return true;
    }

    clearHotbarSlot(slotIndex) {
        if (slotIndex < 0 || slotIndex >= 8) return false;

        if (this.hotbar[slotIndex]) {
            console.log(`🎮 Hotbar Slot ${slotIndex + 1} geleert`);
            this.hotbar[slotIndex] = null;
            this.updateHotbarUI();
        }
        return true;
    }

    useHotbarSlot(slotIndex) {
        if (slotIndex < 0 || slotIndex >= 8) return false;

        // Update selected slot
        this.selectedHotbarSlot = slotIndex;
        this.updateHotbarUI();

        const hotbarItem = this.hotbar[slotIndex];
        if (!hotbarItem) {
            console.log(`🎮 Hotbar Slot ${slotIndex + 1} ist leer`);
            return false;
        }

        // Check cooldown
        if (this.hotbarCooldowns[slotIndex] > 0) {
            console.log(`⏳ Cooldown: ${(this.hotbarCooldowns[slotIndex] / 1000).toFixed(1)}s`);
            return false;
        }

        // Check if item still in inventory
        const inventoryItem = this.items.find(i => i.id === hotbarItem.id);
        if (!inventoryItem && hotbarItem.data.type !== 'skill') {
            console.log(`❌ ${hotbarItem.data.name} nicht mehr im Inventar!`);
            this.clearHotbarSlot(slotIndex);
            return false;
        }

        console.log(`🎮 Benutze Hotbar Slot ${slotIndex + 1}: ${hotbarItem.data.icon} ${hotbarItem.data.name}`);

        // Use the item
        const success = this.useItem(hotbarItem.id);

        if (success) {
            // Apply cooldown based on item type
            let cooldownTime = 0;
            if (hotbarItem.data.type === 'food') {
                cooldownTime = 1000; // 1 second for food
            } else if (hotbarItem.data.type === 'skill') {
                cooldownTime = hotbarItem.data.cooldown || 3000;
            }

            if (cooldownTime > 0) {
                this.startHotbarCooldown(slotIndex, cooldownTime);
            }

            // Update UI after use
            this.updateHotbarUI();
        }

        return success;
    }

    startHotbarCooldown(slotIndex, duration) {
        this.hotbarCooldowns[slotIndex] = duration;
        const startTime = Date.now();

        const updateCooldown = () => {
            const elapsed = Date.now() - startTime;
            const remaining = duration - elapsed;

            if (remaining <= 0) {
                this.hotbarCooldowns[slotIndex] = 0;
                this.updateHotbarSlotCooldown(slotIndex, 0);
            } else {
                this.hotbarCooldowns[slotIndex] = remaining;
                this.updateHotbarSlotCooldown(slotIndex, remaining / duration);
                requestAnimationFrame(updateCooldown);
            }
        };

        requestAnimationFrame(updateCooldown);
    }

    updateHotbarSlotCooldown(slotIndex, percentage) {
        const slot = document.getElementById(`hotbar-slot-${slotIndex}`);
        if (!slot) return;

        const cooldownOverlay = slot.querySelector('.hotbar-cooldown');
        if (cooldownOverlay) {
            cooldownOverlay.style.height = `${percentage * 100}%`;
        }

        slot.classList.toggle('on-cooldown', percentage > 0);
    }

    updateHotbarUI() {
        for (let i = 0; i < 8; i++) {
            const slot = document.getElementById(`hotbar-slot-${i}`);
            if (!slot) continue;

            const hotbarItem = this.hotbar[i];
            const iconEl = slot.querySelector('.hotbar-icon');
            const quantityEl = slot.querySelector('.hotbar-quantity');

            // Clear old rarity classes
            slot.classList.remove('rarity-common', 'rarity-uncommon', 'rarity-rare', 'rarity-epic', 'rarity-legendary', 'rarity-quest', 'empty');

            if (hotbarItem) {
                // Check inventory for quantity
                const inventoryItem = this.items.find(item => item.id === hotbarItem.id);
                const quantity = inventoryItem ? inventoryItem.quantity : 0;

                iconEl.textContent = hotbarItem.data.icon || '?';
                quantityEl.textContent = quantity > 1 ? quantity : '';

                // Add rarity class
                if (hotbarItem.data.rarity) {
                    slot.classList.add(`rarity-${hotbarItem.data.rarity}`);
                }

                // Gray out if no quantity
                if (quantity <= 0 && hotbarItem.data.type !== 'skill') {
                    slot.style.opacity = '0.4';
                } else {
                    slot.style.opacity = '1';
                }
            } else {
                iconEl.textContent = '';
                quantityEl.textContent = '';
                slot.classList.add('empty');
                slot.style.opacity = '1';
            }

            // Update selected state
            slot.classList.toggle('selected', i === this.selectedHotbarSlot);
        }
    }

    // Get hotbar for save/load
    getHotbarData() {
        return this.hotbar.map(item => item ? item.id : null);
    }

    // Load hotbar from saved data
    loadHotbarData(savedHotbar) {
        if (!savedHotbar || !Array.isArray(savedHotbar)) return;

        for (let i = 0; i < Math.min(savedHotbar.length, 8); i++) {
            const itemId = savedHotbar[i];
            if (itemId) {
                const itemData = this.itemDatabase[itemId];
                if (itemData) {
                    this.hotbar[i] = { id: itemId, data: itemData };
                }
            }
        }
        this.updateHotbarUI();
    }

    // ===== ITEM DATABASE =====

    loadItemDatabase() {
        return {
            // ===== WEAPONS =====
            'fire_sword': {
                id: 'fire_sword',
                name: 'Feuerschwert',
                type: 'weapon',
                slot: 'weapon_left',
                icon: '🔥⚔️',
                description: 'Schwert mit Feuer-Magie',
                stats: {
                    damage: 25,
                    element: 'fire',
                    speed: 1.0
                },
                rarity: 'rare',
                value: 500
            },
            'ice_dagger': {
                id: 'ice_dagger',
                name: 'Eisdolch',
                type: 'weapon',
                slot: 'weapon_right',
                icon: '❄️🗡️',
                description: 'Schneller Dolch mit Eis-Magie',
                stats: {
                    damage: 18,
                    element: 'ice',
                    speed: 1.5
                },
                rarity: 'uncommon',
                value: 300
            },
            'lightning_staff': {
                id: 'lightning_staff',
                name: 'Blitzstab',
                type: 'weapon',
                slot: 'weapon_left',
                icon: '⚡🪄',
                description: 'Magischer Stab mit Blitz-Zauber',
                stats: {
                    damage: 35,
                    element: 'lightning',
                    speed: 0.8,
                    mana_cost: 10
                },
                rarity: 'rare',
                value: 800
            },
            'water_bow': {
                id: 'water_bow',
                name: 'Wasserbogen',
                type: 'weapon',
                slot: 'weapon_left',
                icon: '🌊🏹',
                description: 'Bogen mit Wasser-Pfeilen',
                stats: {
                    damage: 22,
                    element: 'water',
                    speed: 1.2,
                    range: 20
                },
                rarity: 'uncommon',
                value: 400
            },

            // ===== ARMOR =====
            'iron_helmet': {
                id: 'iron_helmet',
                name: 'Eisenhelm',
                type: 'armor',
                slot: 'armor_head',
                icon: '⛑️',
                description: 'Stabiler Helm aus Eisen',
                stats: {
                    defense: 10,
                    weight: 5
                },
                rarity: 'common',
                value: 100
            },
            'leather_armor': {
                id: 'leather_armor',
                name: 'Lederrüstung',
                type: 'armor',
                slot: 'armor_chest',
                icon: '🧥',
                description: 'Leichte Lederrüstung',
                stats: {
                    defense: 15,
                    weight: 3,
                    speed_bonus: 0.1
                },
                rarity: 'common',
                value: 150
            },
            'steel_chestplate': {
                id: 'steel_chestplate',
                name: 'Stahlbrustpanzer',
                type: 'armor',
                slot: 'armor_chest',
                icon: '🛡️',
                description: 'Schwerer Stahlpanzer',
                stats: {
                    defense: 35,
                    weight: 15,
                    speed_penalty: -0.2
                },
                rarity: 'rare',
                value: 600
            },

            // ===== ACCESSORIES =====
            'strength_ring': {
                id: 'strength_ring',
                name: 'Ring der Stärke',
                type: 'accessory',
                slot: 'accessory_1',
                icon: '💍',
                description: 'Ring der Stärke verleiht',
                stats: {
                    strength: 15, // +15% Damage
                    combat_power: 5
                },
                rarity: 'rare',
                value: 800
            },
            'vitality_amulet': {
                id: 'vitality_amulet',
                name: 'Amulett der Vitalität',
                type: 'accessory',
                slot: 'accessory_1',
                icon: '📿',
                description: 'Erhöht maximale HP',
                stats: {
                    max_hp: 50,
                    hp_regen: 2
                },
                rarity: 'uncommon',
                value: 400
            },

            // ===== QUEST ITEMS =====
            'ancient_key': {
                id: 'ancient_key',
                name: 'Uralter Schlüssel',
                type: 'quest',
                icon: '🗝️',
                description: 'Öffnet alte Ruinen',
                rarity: 'quest',
                value: 0, // Quest items can't be sold
                stackable: false
            },
            'crystal_shard': {
                id: 'crystal_shard',
                name: 'Kristallscherbe',
                type: 'material',
                icon: '💎',
                description: 'Magische Kristallscherbe',
                rarity: 'uncommon',
                value: 50,
                stackable: true
            },

            // ===== FOOD ITEMS =====
            'baozi': {
                id: 'baozi',
                name: 'Gedämpftes Brötchen (Baozi)',
                type: 'food',
                icon: '🥟',
                description: 'Dampf-Hain Special - Spirited Away Style',
                effects: {
                    hunger: 30,
                    health: 15,
                    stamina: 20
                },
                rarity: 'uncommon',
                value: 25,
                stackable: true
            },
            'arena_happen': {
                id: 'arena_happen',
                name: 'Arena-Happen Burger',
                type: 'food',
                icon: '🍔',
                description: 'Legendärer Burger aus der Handelsfestung Arena',
                effects: {
                    hunger: 50,
                    health: 25,
                    damage_boost: 10,
                    duration: 300
                },
                rarity: 'rare',
                value: 100,
                stackable: true
            },
            'salted_fish': {
                id: 'salted_fish',
                name: 'Salzfisch',
                type: 'food',
                icon: '🐟',
                description: 'Getrockneter Fisch von der Salzigen Bucht',
                effects: {
                    hunger: 25,
                    health: 10,
                    stamina_regen: 5,
                    duration: 180
                },
                rarity: 'common',
                value: 15,
                stackable: true
            },
            'champion_keule': {
                id: 'champion_keule',
                name: 'Champion-Keule',
                type: 'food',
                icon: '🍖',
                description: 'Legendäres Fleisch - Two-handed eating!',
                effects: {
                    hunger: 80,
                    health: 50,
                    damage_boost: 20,
                    crit_chance: 15,
                    duration: 600
                },
                rarity: 'legendary',
                value: 250,
                stackable: true
            }
        };
    }

    // ===== INVENTORY MANAGEMENT =====

    addItem(itemId, quantity = 1) {
        const itemData = this.itemDatabase[itemId];
        if (!itemData) {
            console.error(`❌ Item nicht gefunden: ${itemId}`);
            return false;
        }

        // Check if inventory full
        if (this.items.length >= this.maxSlots && !this.hasItem(itemId)) {
            console.error('❌ Inventar voll!');
            return false;
        }

        // Check if stackable
        if (itemData.stackable || itemData.type === 'food') {
            const existing = this.items.find(item => item.id === itemId);
            if (existing) {
                existing.quantity += quantity;
                console.log(`📦 +${quantity}x ${itemData.name} (Total: ${existing.quantity})`);
                return true;
            }
        }

        // Add new item
        const newItem = {
            id: itemId,
            data: itemData,
            quantity: quantity
        };

        this.items.push(newItem);
        console.log(`📦 +${quantity}x ${itemData.name} erhalten!`);
        return true;
    }

    removeItem(itemId, quantity = 1) {
        const item = this.items.find(i => i.id === itemId);
        if (!item) {
            console.error(`❌ Item nicht im Inventar: ${itemId}`);
            return false;
        }

        item.quantity -= quantity;
        console.log(`📦 -${quantity}x ${item.data.name}`);

        if (item.quantity <= 0) {
            this.items = this.items.filter(i => i.id !== itemId);
            console.log(`📦 ${item.data.name} aufgebraucht`);
        }

        return true;
    }

    useItem(itemId) {
        const item = this.items.find(i => i.id === itemId);
        if (!item) {
            console.error(`❌ Item nicht im Inventar: ${itemId}`);
            return false;
        }

        console.log(`🔧 Nutze: ${item.data.icon} ${item.data.name}`);

        // Handle different item types
        switch (item.data.type) {
            case 'food':
                // Use Food System
                if (this.foodSystem) {
                    const success = this.foodSystem.eatFood(itemId, {
                        health: this.combatSystem?.playerHealth || 100,
                        maxHealth: this.combatSystem?.playerMaxHealth || 100,
                        mana: this.combatSystem?.playerMana || 50,
                        maxMana: this.combatSystem?.playerMaxMana || 50,
                        stamina: this.combatSystem?.playerStamina || 100,
                        maxStamina: this.combatSystem?.playerMaxStamina || 100
                    });

                    if (success) {
                        this.removeItem(itemId, 1);
                        return true;
                    }
                }
                break;

            case 'weapon':
                // Equip weapon
                return this.equipItem(itemId);

            case 'armor':
                // Equip armor
                return this.equipItem(itemId);

            case 'accessory':
                // Equip accessory
                return this.equipItem(itemId);

            case 'quest':
                console.log('ℹ️ Quest-Items können nicht benutzt werden');
                return false;

            case 'material':
                console.log('ℹ️ Materialien werden für Crafting benötigt');
                return false;

            default:
                console.warn(`⚠️ Unbekannter Item-Typ: ${item.data.type}`);
                return false;
        }

        return false;
    }

    hasItem(itemId) {
        return this.items.some(item => item.id === itemId);
    }

    getItemCount(itemId) {
        const item = this.items.find(i => i.id === itemId);
        return item ? item.quantity : 0;
    }

    getItemsByType(type) {
        return this.items.filter(item => item.data.type === type);
    }

    // ===== EQUIPMENT SYSTEM =====

    equipItem(itemId) {
        const item = this.items.find(i => i.id === itemId);
        if (!item) {
            console.error(`❌ Item nicht im Inventar: ${itemId}`);
            return false;
        }

        const slot = item.data.slot;
        if (!slot) {
            console.error(`❌ Item kann nicht ausgerüstet werden: ${itemId}`);
            return false;
        }

        // Special handling for accessories (2 slots)
        if (item.data.type === 'accessory') {
            if (this.equipment.accessory_1 === null) {
                this.equipment.accessory_1 = item;
            } else if (this.equipment.accessory_2 === null) {
                this.equipment.accessory_2 = item;
            } else {
                console.log('⚠️ Beide Accessory-Slots belegt! Ersetze Slot 1');
                this.unequipItem('accessory_1');
                this.equipment.accessory_1 = item;
            }
        } else {
            // Unequip previous item in slot
            if (this.equipment[slot] !== null) {
                this.unequipItem(slot);
            }

            this.equipment[slot] = item;
        }

        console.log(`⚔️ ${item.data.icon} ${item.data.name} ausgerüstet!`);

        // Update Combat System
        if (this.combatSystem && item.data.type === 'weapon') {
            const hand = slot === 'weapon_left' ? 'left' : 'right';
            this.combatSystem.equipWeapon(hand, {
                type: itemId,
                element: item.data.stats.element,
                damage: item.data.stats.damage,
                speed: item.data.stats.speed
            });
        }

        // Remove from inventory (but keep in equipment)
        this.removeItem(itemId, 1);

        return true;
    }

    unequipItem(slot) {
        const item = this.equipment[slot];
        if (!item) {
            console.warn(`⚠️ Kein Item im Slot: ${slot}`);
            return false;
        }

        console.log(`🔓 ${item.data.icon} ${item.data.name} abgelegt`);

        // Add back to inventory
        this.addItem(item.id, 1);

        // Clear slot
        this.equipment[slot] = null;

        // Update Combat System
        if (this.combatSystem && item.data.type === 'weapon') {
            const hand = slot === 'weapon_left' ? 'left' : 'right';
            this.combatSystem.equipWeapon(hand, null);
        }

        return true;
    }

    getEquippedItem(slot) {
        return this.equipment[slot];
    }

    getAllEquipment() {
        return this.equipment;
    }

    // ===== STATS CALCULATION =====

    getTotalStats() {
        const stats = {
            damage: 0,
            defense: 0,
            strength: 0,
            combat_power: 0,
            max_hp: 0,
            hp_regen: 0,
            speed_modifier: 1.0,
            weight: 0
        };

        // Equipment stats
        for (const slot in this.equipment) {
            const item = this.equipment[slot];
            if (item && item.data.stats) {
                const itemStats = item.data.stats;

                stats.damage += itemStats.damage || 0;
                stats.defense += itemStats.defense || 0;
                stats.strength += itemStats.strength || 0;
                stats.combat_power += itemStats.combat_power || 0;
                stats.max_hp += itemStats.max_hp || 0;
                stats.hp_regen += itemStats.hp_regen || 0;
                stats.weight += itemStats.weight || 0;

                // Speed modifiers
                if (itemStats.speed_bonus) {
                    stats.speed_modifier += itemStats.speed_bonus;
                }
                if (itemStats.speed_penalty) {
                    stats.speed_modifier += itemStats.speed_penalty; // Negative value
                }
            }
        }

        return stats;
    }

    // ===== GOLD SYSTEM =====

    addGold(amount) {
        this.gold += amount;
        console.log(`💰 +${amount} Gold (Total: ${this.gold})`);
    }

    removeGold(amount) {
        if (this.gold < amount) {
            console.error(`❌ Nicht genug Gold! (Hast: ${this.gold}, Brauchst: ${amount})`);
            return false;
        }

        this.gold -= amount;
        console.log(`💰 -${amount} Gold (Verbleibend: ${this.gold})`);
        return true;
    }

    hasGold(amount) {
        return this.gold >= amount;
    }

    // ===== SHOP SYSTEM =====

    buyItem(itemId, quantity = 1) {
        const itemData = this.itemDatabase[itemId];
        if (!itemData) {
            console.error(`❌ Item nicht gefunden: ${itemId}`);
            return false;
        }

        const totalCost = itemData.value * quantity;

        if (!this.hasGold(totalCost)) {
            console.error(`❌ Nicht genug Gold! Brauchst: ${totalCost}, Hast: ${this.gold}`);
            return false;
        }

        if (this.removeGold(totalCost)) {
            this.addItem(itemId, quantity);
            console.log(`🛒 ${quantity}x ${itemData.icon} ${itemData.name} gekauft!`);
            return true;
        }

        return false;
    }

    sellItem(itemId, quantity = 1) {
        const item = this.items.find(i => i.id === itemId);
        if (!item) {
            console.error(`❌ Item nicht im Inventar: ${itemId}`);
            return false;
        }

        if (item.data.value === 0) {
            console.error('❌ Quest-Items können nicht verkauft werden!');
            return false;
        }

        if (item.quantity < quantity) {
            console.error(`❌ Nicht genug Items! (Hast: ${item.quantity}, Verkaufen: ${quantity})`);
            return false;
        }

        const sellPrice = Math.floor(item.data.value * 0.5 * quantity); // 50% des Kaufpreises

        if (this.removeItem(itemId, quantity)) {
            this.addGold(sellPrice);
            console.log(`💰 ${quantity}x ${item.data.icon} ${item.data.name} verkauft für ${sellPrice} Gold!`);
            return true;
        }

        return false;
    }

    // ===== FOOD INTEGRATION =====

    addFoodFromFoodSystem(foodId, quantity = 1) {
        if (!this.foodSystem) {
            console.error('❌ Food System nicht verfügbar');
            return false;
        }

        const foodInfo = this.foodSystem.getFoodInfo(foodId);
        if (!foodInfo) {
            console.error(`❌ Food nicht gefunden: ${foodId}`);
            return false;
        }

        // Add as inventory item
        return this.addItem(foodId, quantity);
    }

    // ===== UI HELPERS =====

    getInventoryDisplay() {
        return this.items.map(item => ({
            id: item.id,
            name: item.data.name,
            icon: item.data.icon,
            type: item.data.type,
            quantity: item.quantity,
            rarity: item.data.rarity,
            value: item.data.value,
            description: item.data.description
        }));
    }

    getEquipmentDisplay() {
        const display = {};
        for (const slot in this.equipment) {
            const item = this.equipment[slot];
            display[slot] = item ? {
                id: item.id,
                name: item.data.name,
                icon: item.data.icon,
                stats: item.data.stats,
                rarity: item.data.rarity
            } : null;
        }
        return display;
    }

    // ===== SAVE/LOAD =====

    saveToLocalStorage() {
        const saveData = {
            items: this.items,
            equipment: this.equipment,
            gold: this.gold,
            hotbar: this.getHotbarData() // Save hotbar assignments
        };

        localStorage.setItem('najika_inventory', JSON.stringify(saveData));
        console.log('💾 Inventar + Hotbar gespeichert');
    }

    loadFromLocalStorage() {
        const saveData = localStorage.getItem('najika_inventory');
        if (saveData) {
            const data = JSON.parse(saveData);
            this.items = data.items || [];
            this.equipment = data.equipment || {};
            this.gold = data.gold || 0;

            // Load hotbar after items are loaded
            if (data.hotbar) {
                this.loadHotbarData(data.hotbar);
            }

            console.log('💾 Inventar + Hotbar geladen');
            return true;
        }
        return false;
    }
}

// Export for global use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = InventorySystem;
}
