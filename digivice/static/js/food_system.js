/**
 * NAJIKA WORLD - FOOD & COOKING SYSTEM
 * =====================================
 *
 * Basierend auf NAJIKA_WORLD_COMPLETE_MASTER_DOCUMENTATION.md
 *
 * 3 STADT-SPEZIALITÄTEN:
 * 1. Salzfisch (Salzige Bucht) - Swimming, Water Resistance
 * 2. Gedämpfte Brötchen (Dampf-Hain) - HP Regen, Comfort
 * 3. Fleisch (Handelsfestung) - Strength, Stamina, Combat Power
 *
 * ANIME-CLASSIC: Champion-Keule! 🍖
 */

class FoodSystem {
    constructor() {
        // Player Buffs
        this.activeBuffs = [];

        // Food Database
        this.foodDatabase = this.loadFoodDatabase();

        // Player Inventory
        this.inventory = [];
    }

    loadFoodDatabase() {
        return {
            // ===== SALZFISCH (Salzige Bucht) 🐟 =====
            'salted_fish': {
                name: 'Salzfisch',
                description: 'Getrockneter Fisch aus der Salzigen Bucht',
                icon: '🐟',
                category: 'salzige_bucht',
                effects: {
                    hp_regen: 5, // HP/s für 30s
                    swimming: 20, // +20% Swimming Speed
                    water_resistance: 15 // +15% Water Resistance
                },
                duration: 300, // 5 Minuten
                rarity: 'common'
            },
            'premium_salted_fish': {
                name: 'Premium Salzfisch',
                description: 'Perfekt gewürzter Salzfisch',
                icon: '🐠',
                category: 'salzige_bucht',
                effects: {
                    hp_regen: 10,
                    swimming: 35,
                    water_resistance: 25
                },
                duration: 600,
                rarity: 'rare'
            },

            // ===== GEDÄMPFTE BRÖTCHEN (Dampf-Hain) 🥟 =====
            'baozi': {
                name: 'Baozi',
                description: 'Gedämpftes Brötchen mit Füllung',
                icon: '🥟',
                category: 'dampf_hain',
                effects: {
                    hp_regen: 8,
                    comfort: 10, // +10% XP Gain
                    warmth: 15 // +15% Cold Resistance
                },
                duration: 300,
                rarity: 'common'
            },
            'manju': {
                name: 'Manju',
                description: 'Süßes gedämpftes Brötchen',
                icon: '🍡',
                category: 'dampf_hain',
                effects: {
                    hp_regen: 6,
                    mana_regen: 5, // Mana/s für 30s
                    comfort: 15,
                    warmth: 10
                },
                duration: 300,
                rarity: 'common'
            },
            'dampfnudel': {
                name: 'Dampfnudel',
                description: 'Große fluffige Dampfnudel',
                icon: '🍞',
                category: 'dampf_hain',
                effects: {
                    hp_regen: 12,
                    stamina_regen: 10, // Stamina/s
                    comfort: 20
                },
                duration: 600,
                rarity: 'rare'
            },

            // ===== FLEISCH (Handelsfestung) 🍖 =====

            // Street Food
            'arena_happen': {
                name: 'Arena-Happen',
                description: 'Saftiger Burger (Straßenessen)',
                icon: '🍔',
                category: 'handelsfestung',
                effects: {
                    hp_instant: 30, // Sofort-Heilung
                    strength: 10, // +10% Damage
                    stamina_max: 15 // +15 Max Stamina
                },
                duration: 300,
                rarity: 'common'
            },
            'gold_staebchen': {
                name: 'Gold-Stäbchen',
                description: 'Knusprige Pommes',
                icon: '🍟',
                category: 'handelsfestung',
                effects: {
                    hp_instant: 15,
                    speed: 10 // +10% Movement Speed
                },
                duration: 180,
                rarity: 'common'
            },
            'haendler_wurst': {
                name: 'Händler-Wurst',
                description: 'Heiße Wurst im Brötchen',
                icon: '🌭',
                category: 'handelsfestung',
                effects: {
                    hp_instant: 25,
                    strength: 8,
                    combat_power: 5 // +5% All Combat Stats
                },
                duration: 240,
                rarity: 'common'
            },
            'dreh_braten': {
                name: 'Dreh-Braten',
                description: 'Döner (rotierendes Fleisch)',
                icon: '🥙',
                category: 'handelsfestung',
                effects: {
                    hp_instant: 40,
                    hp_regen: 5,
                    strength: 12,
                    stamina_regen: 8
                },
                duration: 300,
                rarity: 'uncommon'
            },
            'haendler_fladen': {
                name: 'Händler-Fladen',
                description: 'Türkische Pizza (Lahmacun)',
                icon: '🍕',
                category: 'handelsfestung',
                effects: {
                    hp_instant: 35,
                    strength: 10,
                    defense: 8 // +8% Defense
                },
                duration: 300,
                rarity: 'uncommon'
            },

            // Western BBQ
            'rauch_rippchen': {
                name: 'Rauch-Rippchen',
                description: 'BBQ Ribs (saftig geräuchert)',
                icon: '🍖',
                category: 'handelsfestung',
                effects: {
                    hp_instant: 50,
                    strength: 18,
                    combat_power: 10,
                    stamina_max: 20
                },
                duration: 600,
                rarity: 'rare'
            },
            'glut_steak': {
                name: 'Glut-Steak',
                description: 'Perfekt gegrilltes Steak',
                icon: '🥩',
                category: 'handelsfestung',
                effects: {
                    hp_instant: 60,
                    strength: 20,
                    combat_power: 12,
                    crit_chance: 5 // +5% Crit Chance
                },
                duration: 600,
                rarity: 'rare'
            },
            'wuesten_doerrfleisch': {
                name: 'Wüsten-Dörrfleisch',
                description: 'Jerky (lange haltbar)',
                icon: '🥓',
                category: 'handelsfestung',
                effects: {
                    hp_regen: 3,
                    strength: 15,
                    stamina_regen: 15,
                    heat_resistance: 20 // +20% Heat Resistance
                },
                duration: 1800, // 30 Minuten!
                rarity: 'uncommon'
            },

            // ANIME-CLASSIC: CHAMPION-KEULE! ⭐
            'champion_keule': {
                name: 'CHAMPION-KEULE',
                description: '🍖 Die legendäre große Fleischkeule am Knochen! Mit beiden Händen essen!',
                icon: '🍖',
                category: 'handelsfestung',
                effects: {
                    hp_instant: 100, // Massive Heilung!
                    hp_regen: 15,
                    strength: 30, // +30% Damage!
                    stamina_max: 40,
                    stamina_regen: 20,
                    combat_power: 20,
                    speed: -5 // -5% Speed (zu voll!)
                },
                duration: 900, // 15 Minuten!
                rarity: 'legendary',
                special: 'anime_classic',
                eatAnimation: 'both_hands' // Spezielle Animation
            }
        };
    }

    // ===== FOOD CONSUMPTION =====

    eatFood(foodID, player) {
        const food = this.foodDatabase[foodID];
        if (!food) {
            console.error(`❌ Food nicht gefunden: ${foodID}`);
            return false;
        }

        console.log(`🍴 Esse: ${food.icon} ${food.name}`);

        // Instant Effects (sofortige Heilung)
        if (food.effects.hp_instant) {
            player.health = Math.min(player.maxHealth, player.health + food.effects.hp_instant);
            console.log(`❤️ +${food.effects.hp_instant} HP (sofort)`);
        }

        // Apply Buffs (zeitbasiert)
        this.applyBuffs(food, player);

        // Special: Champion-Keule Animation
        if (food.special === 'anime_classic') {
            console.log('🍖 NAJIKA BEISST REIN WIE IN JEDEM GUTEN ANIME! 😂');
            // TODO: Trigger special eating animation
        }

        return true;
    }

    applyBuffs(food, player) {
        const buffID = `buff_${Date.now()}`;

        const buff = {
            id: buffID,
            name: food.name,
            icon: food.icon,
            effects: food.effects,
            startTime: Date.now(),
            duration: food.duration * 1000, // Convert to ms
            rarity: food.rarity
        };

        this.activeBuffs.push(buff);

        console.log(`✨ Buff aktiviert: ${food.icon} ${food.name} (${food.duration}s)`);

        // Remove buff after duration
        setTimeout(() => {
            this.removeBuff(buffID);
        }, buff.duration);
    }

    removeBuff(buffID) {
        const index = this.activeBuffs.findIndex(b => b.id === buffID);
        if (index !== -1) {
            const buff = this.activeBuffs[index];
            console.log(`⏱️ Buff abgelaufen: ${buff.icon} ${buff.name}`);
            this.activeBuffs.splice(index, 1);
        }
    }

    // ===== BUFF CALCULATION =====

    calculateBuffedStats(baseStats) {
        const buffed = { ...baseStats };

        for (const buff of this.activeBuffs) {
            const effects = buff.effects;

            // Damage Buffs
            if (effects.strength) {
                buffed.damage *= (1 + effects.strength / 100);
            }
            if (effects.combat_power) {
                buffed.damage *= (1 + effects.combat_power / 100);
                buffed.defense *= (1 + effects.combat_power / 100);
            }

            // Defense Buffs
            if (effects.defense) {
                buffed.defense *= (1 + effects.defense / 100);
            }

            // Speed Buffs
            if (effects.speed) {
                buffed.speed *= (1 + effects.speed / 100);
            }

            // Stamina Buffs
            if (effects.stamina_max) {
                buffed.maxStamina += effects.stamina_max;
            }

            // Resistance Buffs
            if (effects.water_resistance) {
                buffed.waterResistance = (buffed.waterResistance || 0) + effects.water_resistance;
            }
            if (effects.heat_resistance) {
                buffed.heatResistance = (buffed.heatResistance || 0) + effects.heat_resistance;
            }
            if (effects.warmth) {
                buffed.coldResistance = (buffed.coldResistance || 0) + effects.warmth;
            }

            // Crit Buffs
            if (effects.crit_chance) {
                buffed.critChance = (buffed.critChance || 0) + effects.crit_chance;
            }

            // XP Buffs
            if (effects.comfort) {
                buffed.xpGain = (buffed.xpGain || 100) + effects.comfort;
            }
        }

        return buffed;
    }

    // ===== REGEN TICK =====

    updateRegens(delta, player) {
        for (const buff of this.activeBuffs) {
            const effects = buff.effects;

            // HP Regen
            if (effects.hp_regen) {
                player.health = Math.min(player.maxHealth, player.health + effects.hp_regen * delta);
            }

            // Mana Regen
            if (effects.mana_regen) {
                player.mana = Math.min(player.maxMana, player.mana + effects.mana_regen * delta);
            }

            // Stamina Regen
            if (effects.stamina_regen) {
                player.stamina = Math.min(player.maxStamina, player.stamina + effects.stamina_regen * delta);
            }
        }

        return player;
    }

    // ===== UI HELPERS =====

    getActiveBuffs() {
        return this.activeBuffs.map(buff => {
            const remaining = (buff.startTime + buff.duration - Date.now()) / 1000;
            return {
                ...buff,
                remaining: Math.max(0, remaining)
            };
        });
    }

    getBuffSummary() {
        const summary = {
            damage: 0,
            defense: 0,
            speed: 0,
            hp_regen: 0,
            stamina_regen: 0
        };

        for (const buff of this.activeBuffs) {
            if (buff.effects.strength) summary.damage += buff.effects.strength;
            if (buff.effects.combat_power) summary.damage += buff.effects.combat_power;
            if (buff.effects.defense) summary.defense += buff.effects.defense;
            if (buff.effects.speed) summary.speed += buff.effects.speed;
            if (buff.effects.hp_regen) summary.hp_regen += buff.effects.hp_regen;
            if (buff.effects.stamina_regen) summary.stamina_regen += buff.effects.stamina_regen;
        }

        return summary;
    }

    // ===== INVENTORY =====

    addFood(foodID, quantity = 1) {
        const existing = this.inventory.find(item => item.id === foodID);
        if (existing) {
            existing.quantity += quantity;
        } else {
            this.inventory.push({
                id: foodID,
                quantity: quantity
            });
        }
        console.log(`📦 +${quantity}x ${this.foodDatabase[foodID].name}`);
    }

    removeFood(foodID, quantity = 1) {
        const existing = this.inventory.find(item => item.id === foodID);
        if (existing) {
            existing.quantity -= quantity;
            if (existing.quantity <= 0) {
                this.inventory = this.inventory.filter(item => item.id !== foodID);
            }
            return true;
        }
        return false;
    }

    hasFood(foodID) {
        const item = this.inventory.find(item => item.id === foodID);
        return item && item.quantity > 0;
    }

    // ===== PUBLIC API =====

    getFoodInfo(foodID) {
        return this.foodDatabase[foodID];
    }

    getAllFood() {
        return this.foodDatabase;
    }

    getInventory() {
        return this.inventory.map(item => ({
            ...item,
            info: this.foodDatabase[item.id]
        }));
    }
}

// Export for global use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = FoodSystem;
}
