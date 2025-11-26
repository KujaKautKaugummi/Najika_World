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

        // Player Stats (Gold, etc.)
        this.gold = 100; // Starting gold

        // Item Database
        this.itemDatabase = this.loadItemDatabase();

        console.log('📦 Inventar-System initialisiert');
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
            gold: this.gold
        };

        localStorage.setItem('najika_inventory', JSON.stringify(saveData));
        console.log('💾 Inventar gespeichert');
    }

    loadFromLocalStorage() {
        const saveData = localStorage.getItem('najika_inventory');
        if (saveData) {
            const data = JSON.parse(saveData);
            this.items = data.items || [];
            this.equipment = data.equipment || {};
            this.gold = data.gold || 0;
            console.log('💾 Inventar geladen');
            return true;
        }
        return false;
    }
}

// Export for global use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = InventorySystem;
}
