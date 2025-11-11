/**
 * NAJIKA WORLD - CRAFTING SYSTEM
 * ================================
 *
 * Crafting-System mit:
 * - Rezepte für Waffen + Rüstungen
 * - Material-Anforderungen
 * - Crafting-UI
 * - Integration mit Schmied-NPCs
 */

class Recipe {
    constructor(data) {
        this.id = data.id;
        this.name = data.name;
        this.type = data.type; // 'weapon', 'armor', 'accessory'
        this.description = data.description;
        this.icon = data.icon || '⚔️';

        // Materials required
        this.materials = data.materials || []; // [{item: 'crystal_shard', count: 5}, ...]

        // Result item
        this.result = data.result; // Item ID

        // Requirements
        this.requiredLevel = data.requiredLevel || 1;
        this.requiredGold = data.requiredGold || 0;

        // Rarity
        this.rarity = data.rarity || 'common'; // 'common', 'uncommon', 'rare', 'legendary'
    }

    canCraft(inventorySystem) {
        // Check gold
        if (this.requiredGold > 0 && !inventorySystem.hasGold(this.requiredGold)) {
            return { canCraft: false, reason: `Nicht genug Gold (${this.requiredGold}g benötigt)` };
        }

        // Check materials
        for (const material of this.materials) {
            const count = inventorySystem.getItemCount(material.item);
            if (count < material.count) {
                return {
                    canCraft: false,
                    reason: `Nicht genug ${material.item} (${material.count} benötigt, ${count} vorhanden)`
                };
            }
        }

        return { canCraft: true };
    }

    getMissingMaterials(inventorySystem) {
        const missing = [];

        for (const material of this.materials) {
            const count = inventorySystem.getItemCount(material.item);
            if (count < material.count) {
                missing.push({
                    item: material.item,
                    needed: material.count,
                    have: count,
                    missing: material.count - count
                });
            }
        }

        return missing;
    }
}

class CraftingSystem {
    constructor(inventorySystem = null) {
        this.inventorySystem = inventorySystem;

        // Recipe Database
        this.recipes = {};
        this.loadRecipeDatabase();

        console.log('🔨 Crafting-System initialisiert');
    }

    loadRecipeDatabase() {
        const recipes = [
            // ===== LEGENDARY WEAPONS (Funken-Siedlung) =====
            {
                id: 'legendary_fire_blade',
                name: 'Legendäre Feuerklinge',
                type: 'weapon',
                description: 'Eine mächtige Klinge, geschmiedet aus den Flammen des Vulkans',
                icon: '🔥⚔️',
                materials: [
                    { item: 'crystal_shard', count: 10 },
                    { item: 'fire_sword', count: 1 },
                    { item: 'champion_keule', count: 1 } // Legendary ingredient!
                ],
                result: 'legendary_fire_blade',
                requiredGold: 1000,
                requiredLevel: 10,
                rarity: 'legendary'
            },
            {
                id: 'legendary_ice_spear',
                name: 'Legendärer Eisspeer',
                type: 'weapon',
                description: 'Ein gefrorener Speer, der niemals schmilzt',
                icon: '❄️🔱',
                materials: [
                    { item: 'crystal_shard', count: 15 },
                    { item: 'ice_dagger', count: 2 },
                    { item: 'salted_fish', count: 5 } // Ironie: Fisch für Eis-Waffe
                ],
                result: 'legendary_ice_spear',
                requiredGold: 1200,
                requiredLevel: 12,
                rarity: 'legendary'
            },
            {
                id: 'legendary_lightning_hammer',
                name: 'Legendärer Blitzhammer',
                type: 'weapon',
                description: 'Ein Hammer der Blitze entfesselt',
                icon: '⚡🔨',
                materials: [
                    { item: 'crystal_shard', count: 20 },
                    { item: 'lightning_staff', count: 1 },
                    { item: 'iron_helmet', count: 2 } // Metall für Leitfähigkeit
                ],
                result: 'legendary_lightning_hammer',
                requiredGold: 1500,
                requiredLevel: 15,
                rarity: 'legendary'
            },

            // ===== LEGENDARY ARMOR (Funken-Siedlung) =====
            {
                id: 'legendary_dragon_armor',
                name: 'Legendäre Drachenrüstung',
                type: 'armor',
                description: 'Rüstung aus Drachenschuppen, unzerstörbar',
                icon: '🐉🛡️',
                materials: [
                    { item: 'crystal_shard', count: 25 },
                    { item: 'steel_chestplate', count: 1 },
                    { item: 'leather_armor', count: 2 }
                ],
                result: 'legendary_dragon_armor',
                requiredGold: 2000,
                requiredLevel: 18,
                rarity: 'legendary'
            },
            {
                id: 'legendary_mage_robe',
                name: 'Legendäre Magie-Robe',
                type: 'armor',
                description: 'Eine Robe die Magie verstärkt',
                icon: '🔮👘',
                materials: [
                    { item: 'crystal_shard', count: 30 },
                    { item: 'vitality_amulet', count: 2 },
                    { item: 'baozi', count: 10 } // Magisches Essen
                ],
                result: 'legendary_mage_robe',
                requiredGold: 1800,
                requiredLevel: 16,
                rarity: 'legendary'
            },

            // ===== RARE WEAPONS =====
            {
                id: 'steel_sword',
                name: 'Stahlschwert',
                type: 'weapon',
                description: 'Ein solides Schwert aus Stahl',
                icon: '⚔️',
                materials: [
                    { item: 'crystal_shard', count: 5 },
                    { item: 'iron_helmet', count: 1 } // Schmelzen für Metall
                ],
                result: 'steel_sword',
                requiredGold: 200,
                requiredLevel: 5,
                rarity: 'rare'
            },
            {
                id: 'iron_axe',
                name: 'Eisenaxt',
                type: 'weapon',
                description: 'Eine schwere Axt für mächtige Schläge',
                icon: '🪓',
                materials: [
                    { item: 'crystal_shard', count: 3 },
                    { item: 'fire_sword', count: 1 }
                ],
                result: 'iron_axe',
                requiredGold: 150,
                requiredLevel: 4,
                rarity: 'uncommon'
            },

            // ===== ACCESSORIES =====
            {
                id: 'power_ring',
                name: 'Ring der Macht',
                type: 'accessory',
                description: 'Ein Ring der große Kraft verleiht',
                icon: '💍',
                materials: [
                    { item: 'crystal_shard', count: 8 },
                    { item: 'strength_ring', count: 1 }
                ],
                result: 'power_ring',
                requiredGold: 500,
                requiredLevel: 8,
                rarity: 'rare'
            }
        ];

        recipes.forEach(recipeData => {
            this.recipes[recipeData.id] = new Recipe(recipeData);
        });

        console.log(`🔨 ${recipes.length} Rezepte geladen`);
    }

    // ===== CRAFT ITEM =====

    craftItem(recipeId) {
        const recipe = this.recipes[recipeId];
        if (!recipe) {
            console.error(`❌ Rezept nicht gefunden: ${recipeId}`);
            return false;
        }

        if (!this.inventorySystem) {
            console.error('❌ Inventory System nicht verfügbar');
            return false;
        }

        // Check if can craft
        const check = recipe.canCraft(this.inventorySystem);
        if (!check.canCraft) {
            console.warn(`⚠️ Kann nicht craften: ${check.reason}`);
            return false;
        }

        // Remove materials
        for (const material of recipe.materials) {
            this.inventorySystem.removeItem(material.item, material.count);
        }

        // Remove gold
        if (recipe.requiredGold > 0) {
            this.inventorySystem.removeGold(recipe.requiredGold);
        }

        // Add result item
        this.inventorySystem.addItem(recipe.result, 1);

        console.log(`🔨 Crafting erfolgreich: ${recipe.icon} ${recipe.name} erstellt!`);
        return true;
    }

    // ===== GETTERS =====

    getAllRecipes() {
        return Object.values(this.recipes);
    }

    getRecipesByType(type) {
        return Object.values(this.recipes).filter(recipe => recipe.type === type);
    }

    getRecipesByRarity(rarity) {
        return Object.values(this.recipes).filter(recipe => recipe.rarity === rarity);
    }

    getCraftableRecipes() {
        if (!this.inventorySystem) return [];

        return Object.values(this.recipes).filter(recipe => {
            return recipe.canCraft(this.inventorySystem).canCraft;
        });
    }
}

// Export für globale Nutzung
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { Recipe, CraftingSystem };
}
