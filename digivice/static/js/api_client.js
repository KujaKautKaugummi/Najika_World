/**
 * Najika API Client v3.0
 * Frontend-Backend Bridge for all game systems
 *
 * Kommuniziert mit FastAPI Backend (backend/api/server.py)
 * Unterstützt: Combat, Food, Inventory, Quests, Skills, Crafting, NPCs, Save/Load
 */

class NajikaAPIClient {
    constructor(baseURL = 'http://127.0.0.1:5000') {
        this.baseURL = baseURL;
        this.isOnline = false;
        this.useFallback = true; // Use local fallback if offline

        // Check backend connectivity
        this.checkConnection();
    }

    // ═══════════════════════════════════════════════════════════════
    // CONNECTION MANAGEMENT
    // ═══════════════════════════════════════════════════════════════

    async checkConnection() {
        try {
            const response = await fetch(`${this.baseURL}/health`, {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' }
            });

            if (response.ok) {
                this.isOnline = true;
                console.log('✅ Najika Backend connected!');
                return true;
            }
        } catch (error) {
            console.warn('⚠️ Backend offline, using local fallback');
            this.isOnline = false;
        }
        return false;
    }

    async request(endpoint, method = 'GET', data = null) {
        const url = `${this.baseURL}${endpoint}`;

        const options = {
            method,
            headers: { 'Content-Type': 'application/json' }
        };

        if (data && method !== 'GET') {
            options.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(url, options);
            const result = await response.json();
            return result;
        } catch (error) {
            console.error(`API Error (${endpoint}):`, error);
            return { success: false, error: error.message };
        }
    }

    // ═══════════════════════════════════════════════════════════════
    // GAME STATE API
    // ═══════════════════════════════════════════════════════════════

    async getGameState() {
        if (!this.isOnline && this.useFallback) {
            return this.localGetGameState();
        }
        return await this.request('/game/state');
    }

    async getPlayerState() {
        if (!this.isOnline && this.useFallback) {
            return this.localGetPlayerState();
        }
        return await this.request('/game/player');
    }

    async updatePlayerState(updates) {
        if (!this.isOnline && this.useFallback) {
            return this.localUpdatePlayerState(updates);
        }
        return await this.request('/game/player/update', 'POST', updates);
    }

    // ═══════════════════════════════════════════════════════════════
    // COMBAT API
    // ═══════════════════════════════════════════════════════════════

    async executeCombatAction(action, enemyId = null, hand = null) {
        if (!this.isOnline && this.useFallback) {
            return this.localCombatAction(action, enemyId, hand);
        }

        return await this.request('/combat/action', 'POST', {
            action,
            enemy_id: enemyId,
            hand
        });
    }

    async getCombatHistory(limit = 10) {
        if (!this.isOnline && this.useFallback) {
            return this.localGetCombatHistory(limit);
        }
        return await this.request(`/combat/history?limit=${limit}`);
    }

    // ═══════════════════════════════════════════════════════════════
    // INVENTORY API
    // ═══════════════════════════════════════════════════════════════

    async getInventory() {
        if (!this.isOnline && this.useFallback) {
            return this.localGetInventory();
        }
        return await this.request('/inventory');
    }

    async inventoryAction(action, itemId = null, itemData = null, slot = null) {
        if (!this.isOnline && this.useFallback) {
            return this.localInventoryAction(action, itemId, itemData, slot);
        }

        return await this.request('/inventory/action', 'POST', {
            action,
            item_id: itemId,
            item_data: itemData,
            slot
        });
    }

    async getEquipment() {
        if (!this.isOnline && this.useFallback) {
            return this.localGetEquipment();
        }
        return await this.request('/inventory/equipment');
    }

    // ═══════════════════════════════════════════════════════════════
    // FOOD/BUFF API
    // ═══════════════════════════════════════════════════════════════

    async consumeFood(foodId, playerStats) {
        if (!this.isOnline && this.useFallback) {
            return this.localConsumeFood(foodId, playerStats);
        }

        return await this.request('/food/consume', 'POST', {
            food_id: foodId,
            player_stats: playerStats
        });
    }

    async getActiveBuffs() {
        if (!this.isOnline && this.useFallback) {
            return this.localGetActiveBuffs();
        }
        return await this.request('/food/buffs');
    }

    // ═══════════════════════════════════════════════════════════════
    // QUEST API
    // ═══════════════════════════════════════════════════════════════

    async getQuests() {
        if (!this.isOnline && this.useFallback) {
            return this.localGetQuests();
        }
        return await this.request('/quests');
    }

    async updateQuest(questId, objectiveIndex, amount = 1) {
        if (!this.isOnline && this.useFallback) {
            return this.localUpdateQuest(questId, objectiveIndex, amount);
        }

        return await this.request('/quests/update', 'POST', {
            quest_id: questId,
            objective_index: objectiveIndex,
            amount
        });
    }

    async completeQuest(questId) {
        if (!this.isOnline && this.useFallback) {
            return this.localCompleteQuest(questId);
        }

        return await this.request('/quests/complete', 'POST', {
            quest_id: questId
        });
    }

    async startQuest(questData) {
        if (!this.isOnline && this.useFallback) {
            return this.localStartQuest(questData);
        }
        return await this.request('/quests/start', 'POST', questData);
    }

    // ═══════════════════════════════════════════════════════════════
    // SKILL API
    // ═══════════════════════════════════════════════════════════════

    async getSkills() {
        if (!this.isOnline && this.useFallback) {
            return this.localGetSkills();
        }
        return await this.request('/skills');
    }

    async useSkill(skillId, targetId = null) {
        if (!this.isOnline && this.useFallback) {
            return this.localUseSkill(skillId, targetId);
        }

        return await this.request('/skills/use', 'POST', {
            skill_id: skillId,
            target_id: targetId
        });
    }

    async skillLevelUp(skillId, xpGained) {
        if (!this.isOnline && this.useFallback) {
            return this.localSkillLevelUp(skillId, xpGained);
        }

        return await this.request('/skills/levelup', 'POST', {
            skill_id: skillId,
            xp_gained: xpGained
        });
    }

    async learnSkill(skillData) {
        if (!this.isOnline && this.useFallback) {
            return this.localLearnSkill(skillData);
        }
        return await this.request('/skills/learn', 'POST', skillData);
    }

    // ═══════════════════════════════════════════════════════════════
    // CRAFTING API
    // ═══════════════════════════════════════════════════════════════

    async craftItem(recipeId, materials) {
        if (!this.isOnline && this.useFallback) {
            return this.localCraftItem(recipeId, materials);
        }

        return await this.request('/crafting/craft', 'POST', {
            recipe_id: recipeId,
            materials
        });
    }

    // ═══════════════════════════════════════════════════════════════
    // SAVE/LOAD API
    // ═══════════════════════════════════════════════════════════════

    async saveGame(saveData) {
        if (!this.isOnline && this.useFallback) {
            return this.localSaveGame(saveData);
        }
        return await this.request('/save', 'POST', saveData);
    }

    async loadGame(saveId = 'latest') {
        if (!this.isOnline && this.useFallback) {
            return this.localLoadGame(saveId);
        }

        return await this.request('/load', 'POST', {
            save_id: saveId
        });
    }

    async listSaves() {
        if (!this.isOnline && this.useFallback) {
            return this.localListSaves();
        }
        return await this.request('/saves');
    }

    // ═══════════════════════════════════════════════════════════════
    // NPC API
    // ═══════════════════════════════════════════════════════════════

    async getNPCs() {
        if (!this.isOnline && this.useFallback) {
            return this.localGetNPCs();
        }
        return await this.request('/npcs');
    }

    async interactNPC(npcId, action = 'talk') {
        if (!this.isOnline && this.useFallback) {
            return this.localInteractNPC(npcId, action);
        }

        return await this.request('/npcs/interact', 'POST', {
            npc_id: npcId,
            action
        });
    }

    // ═══════════════════════════════════════════════════════════════
    // LOCAL FALLBACK METHODS (if backend is offline)
    // ═══════════════════════════════════════════════════════════════

    localGetGameState() {
        const state = localStorage.getItem('najika_game_state');
        return state ? JSON.parse(state) : this.getDefaultGameState();
    }

    localGetPlayerState() {
        const state = this.localGetGameState();
        return state.player || {};
    }

    localUpdatePlayerState(updates) {
        const state = this.localGetGameState();
        state.player = { ...state.player, ...updates };
        localStorage.setItem('najika_game_state', JSON.stringify(state));
        return { success: true, player: state.player };
    }

    localCombatAction(action, enemyId, hand) {
        // Simple offline combat simulation
        const damage = Math.floor(Math.random() * 30) + 10;
        return {
            success: true,
            damage,
            player_health: 100,
            enemy_health: 100 - damage,
            message: `Offline Combat: ${damage} Schaden!`
        };
    }

    localGetCombatHistory(limit) {
        return [];
    }

    localGetInventory() {
        const state = this.localGetGameState();
        return state.inventory || { items: [], equipment: {} };
    }

    localInventoryAction(action, itemId, itemData, slot) {
        const state = this.localGetGameState();

        if (action === 'add') {
            state.inventory.items.push(itemData);
        } else if (action === 'equip') {
            state.inventory.equipment[slot] = itemData;
        }

        localStorage.setItem('najika_game_state', JSON.stringify(state));
        return { success: true, message: `${action} successful` };
    }

    localGetEquipment() {
        const state = this.localGetGameState();
        return state.inventory?.equipment || {};
    }

    localConsumeFood(foodId, playerStats) {
        return {
            success: true,
            message: `Food ${foodId} consumed (offline)`,
            active_buffs: 0
        };
    }

    localGetActiveBuffs() {
        return [];
    }

    localGetQuests() {
        const state = this.localGetGameState();
        return state.quests || { active: [], completed: [] };
    }

    localUpdateQuest(questId, objectiveIndex, amount) {
        return { success: true, message: 'Quest updated (offline)' };
    }

    localCompleteQuest(questId) {
        return { success: true, message: 'Quest completed (offline)' };
    }

    localStartQuest(questData) {
        return { success: true, message: 'Quest started (offline)' };
    }

    localGetSkills() {
        const state = this.localGetGameState();
        return state.skills || {};
    }

    localUseSkill(skillId, targetId) {
        return { success: true, message: `Skill ${skillId} used (offline)`, damage: 50 };
    }

    localSkillLevelUp(skillId, xpGained) {
        return { success: true, message: `XP gained: ${xpGained} (offline)` };
    }

    localLearnSkill(skillData) {
        return { success: true, message: `Skill learned (offline)` };
    }

    localCraftItem(recipeId, materials) {
        return {
            success: true,
            message: `Item crafted (offline)`,
            result: { id: recipeId, name: 'Crafted Item' }
        };
    }

    localSaveGame(saveData) {
        localStorage.setItem('najika_game_state', JSON.stringify(saveData));
        localStorage.setItem('najika_last_save', Date.now().toString());
        return { success: true, message: 'Game saved locally!' };
    }

    localLoadGame(saveId) {
        const state = localStorage.getItem('najika_game_state');
        if (state) {
            return {
                success: true,
                message: 'Game loaded from local storage',
                data: JSON.parse(state)
            };
        }
        return { success: false, message: 'No local save found' };
    }

    localListSaves() {
        const lastSave = localStorage.getItem('najika_last_save');
        if (lastSave) {
            return { saves: [`local_save_${lastSave}`] };
        }
        return { saves: [] };
    }

    localGetNPCs() {
        return {};
    }

    localInteractNPC(npcId, action) {
        return {
            success: true,
            message: `Interacting with NPC ${npcId} (offline)`,
            dialogue: 'Hallo! (Backend offline)',
            options: ['OK']
        };
    }

    getDefaultGameState() {
        return {
            player: {
                health: 100,
                maxHealth: 100,
                mana: 100,
                maxMana: 100,
                stamina: 100,
                maxStamina: 100,
                gold: 100,
                level: 1,
                xp: 0,
                position: { x: 0, y: 0, z: 0 }
            },
            inventory: {
                items: [],
                equipment: {
                    weapon_left: null,
                    weapon_right: null,
                    armor_head: null,
                    armor_chest: null,
                    armor_legs: null,
                    accessory_1: null,
                    accessory_2: null
                }
            },
            quests: {
                active: [],
                completed: []
            },
            skills: {},
            buffs: [],
            npcs: {}
        };
    }
}

// Create global API client instance
window.najikaAPI = new NajikaAPIClient();

console.log('✨ Najika API Client v3.0 initialized');
