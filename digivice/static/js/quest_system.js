/**
 * NAJIKA WORLD - QUEST SYSTEM
 * ============================
 *
 * Komplettes Quest-System mit:
 * - Quest-Typen: Kill, Collect, Talk, Explore
 * - Quest-Tracking
 * - Quest-Log UI
 * - Rewards (Gold, Items, XP)
 */

class Quest {
    constructor(data) {
        this.id = data.id;
        this.name = data.name;
        this.description = data.description;
        this.type = data.type; // 'kill', 'collect', 'talk', 'explore'
        this.giver = data.giver; // NPC who gives quest
        this.objectives = data.objectives || []; // Array of objectives
        this.rewards = data.rewards || { gold: 0, items: [], xp: 0 };
        this.status = 'available'; // 'available', 'active', 'completed', 'failed'
        this.tracked = false; // Show in quest tracker
        this.progress = {}; // Track progress for each objective

        // Initialize progress
        this.objectives.forEach((obj, index) => {
            this.progress[index] = 0;
        });
    }

    // Update objective progress
    updateObjective(objectiveIndex, amount = 1) {
        if (this.status !== 'active') return false;

        const objective = this.objectives[objectiveIndex];
        if (!objective) return false;

        this.progress[objectiveIndex] = Math.min(
            this.progress[objectiveIndex] + amount,
            objective.required
        );

        console.log(`📝 Quest "${this.name}": ${this.progress[objectiveIndex]}/${objective.required} ${objective.target}`);

        // Check if quest is complete
        if (this.isComplete()) {
            console.log(`✅ Quest "${this.name}" ist abgeschlossen!`);
        }

        return true;
    }

    // Check if all objectives are complete
    isComplete() {
        return this.objectives.every((obj, index) => {
            return this.progress[index] >= obj.required;
        });
    }

    // Get quest completion percentage
    getCompletionPercent() {
        if (this.objectives.length === 0) return 0;

        let totalRequired = 0;
        let totalProgress = 0;

        this.objectives.forEach((obj, index) => {
            totalRequired += obj.required;
            totalProgress += this.progress[index];
        });

        return Math.floor((totalProgress / totalRequired) * 100);
    }

    // Get formatted objectives for display
    getFormattedObjectives() {
        return this.objectives.map((obj, index) => {
            const current = this.progress[index];
            const required = obj.required;
            const complete = current >= required;

            return {
                text: obj.description,
                progress: `${current}/${required}`,
                complete: complete,
                icon: complete ? '✅' : '⏳'
            };
        });
    }
}

class QuestManager {
    constructor() {
        this.quests = {}; // All quests by ID
        this.activeQuests = []; // Currently active quest IDs
        this.completedQuests = []; // Completed quest IDs
        this.trackedQuest = null; // Quest to show in tracker

        // Load quest database
        this.loadQuestDatabase();

        console.log('📋 Quest-System initialisiert');
    }

    loadQuestDatabase() {
        const quests = [
            // ===== DAMPF-HAIN QUESTS =====
            {
                id: 'forest_secrets',
                name: 'Geheimnisse des Waldes',
                description: 'Der Druide Kaito spürt, dass die Magie des Waldes schwindet. Sammle Kristallscherben um die alten Bäume zu heilen.',
                type: 'collect',
                giver: 'dampf_hain_druid',
                objectives: [
                    {
                        type: 'collect',
                        target: 'crystal_shard',
                        required: 5,
                        description: 'Sammle 5 Kristallscherben'
                    }
                ],
                rewards: {
                    gold: 200,
                    items: ['vitality_amulet'],
                    xp: 500
                }
            },
            {
                id: 'nature_magic',
                name: 'Naturmagie lernen',
                description: 'Lerne die Grundlagen der Naturmagie vom Druiden.',
                type: 'talk',
                giver: 'dampf_hain_druid',
                objectives: [
                    {
                        type: 'talk',
                        target: 'dampf_hain_druid',
                        required: 1,
                        description: 'Sprich mit dem Druiden über Naturmagie'
                    },
                    {
                        type: 'explore',
                        target: 'dampf_hain',
                        required: 1,
                        description: 'Erkunde den Wald'
                    }
                ],
                rewards: {
                    gold: 100,
                    items: [],
                    xp: 300
                }
            },

            // ===== HANDELSFESTUNG QUESTS =====
            {
                id: 'arena_trial',
                name: 'Arena-Prüfung',
                description: 'Der Arena-Meister fordert dich heraus. Besiege 10 Gegner in der Arena!',
                type: 'kill',
                giver: 'handelsfestung_arena_master',
                objectives: [
                    {
                        type: 'kill',
                        target: 'any',
                        required: 10,
                        description: 'Besiege 10 Gegner'
                    }
                ],
                rewards: {
                    gold: 500,
                    items: ['fire_sword', 'strength_ring'],
                    xp: 1000
                }
            },
            {
                id: 'weapon_collector',
                name: 'Waffensammler',
                description: 'Der Waffenhändler sucht seltene Waffen. Bringe ihm 3 verschiedene Waffen.',
                type: 'collect',
                giver: 'handelsfestung_weapon_vendor',
                objectives: [
                    {
                        type: 'collect',
                        target: 'fire_sword',
                        required: 1,
                        description: 'Finde ein Feuerschwert'
                    },
                    {
                        type: 'collect',
                        target: 'ice_dagger',
                        required: 1,
                        description: 'Finde einen Eisdolch'
                    },
                    {
                        type: 'collect',
                        target: 'lightning_staff',
                        required: 1,
                        description: 'Finde einen Blitzstab'
                    }
                ],
                rewards: {
                    gold: 300,
                    items: [],
                    xp: 400
                }
            },

            // ===== SALZIGE BUCHT QUESTS =====
            {
                id: 'ocean_treasure',
                name: 'Schatz des Ozeans',
                description: 'Kapitän Akira hat seinen Schatz im Meer verloren. Finde den uralten Schlüssel!',
                type: 'collect',
                giver: 'salzige_bucht_captain',
                objectives: [
                    {
                        type: 'collect',
                        target: 'ancient_key',
                        required: 1,
                        description: 'Finde den uralten Schlüssel'
                    },
                    {
                        type: 'explore',
                        target: 'salzige_bucht',
                        required: 1,
                        description: 'Erkunde die Küste'
                    }
                ],
                rewards: {
                    gold: 400,
                    items: ['water_bow'],
                    xp: 600
                }
            },
            {
                id: 'fishing_master',
                name: 'Meister-Fischer',
                description: 'Fischer Ryuu will dir das Fischen beibringen. Fange 20 Fische!',
                type: 'collect',
                giver: 'salzige_bucht_fish_vendor',
                objectives: [
                    {
                        type: 'collect',
                        target: 'salted_fish',
                        required: 20,
                        description: 'Fange 20 Fische'
                    }
                ],
                rewards: {
                    gold: 250,
                    items: ['premium_salted_fish'],
                    xp: 350
                }
            },

            // ===== RUNENHEIM QUESTS =====
            {
                id: 'magic_training',
                name: 'Magische Ausbildung',
                description: 'Lerne die drei Grundzauber von Magier-Lehrerin Luna.',
                type: 'talk',
                giver: 'runenheim_mage_teacher',
                objectives: [
                    {
                        type: 'talk',
                        target: 'runenheim_mage_teacher',
                        required: 3,
                        description: 'Absolviere 3 Zauber-Lektionen'
                    }
                ],
                rewards: {
                    gold: 150,
                    items: ['lightning_staff'],
                    xp: 450
                }
            },

            // ===== FUNKEN-SIEDLUNG QUESTS =====
            {
                id: 'smithing_apprentice',
                name: 'Schmied-Lehrling',
                description: 'Meister-Schmied Tetsu sucht einen Lehrling. Bringe ihm 10 Kristallscherben!',
                type: 'collect',
                giver: 'funken_siedlung_master_smith',
                objectives: [
                    {
                        type: 'collect',
                        target: 'crystal_shard',
                        required: 10,
                        description: 'Sammle 10 Kristallscherben'
                    }
                ],
                rewards: {
                    gold: 300,
                    items: ['steel_chestplate'],
                    xp: 500
                }
            },

            // ===== STARTER QUESTS (Götterfels / Overworld) =====
            {
                id: 'wolfsjagd',
                name: 'Wolfsjagd',
                description: 'Die Wölfe im Samtmoos-Wald greifen Reisende an. Besiege 3 Wölfe!',
                type: 'kill',
                giver: 'wanderer_krieger',
                objectives: [
                    { type: 'kill', target: 'wolf', required: 3, description: 'Besiege 3 Wölfe' }
                ],
                rewards: { gold: 50, items: ['wolf_pelt'], xp: 100 }
            },
            {
                id: 'sammler',
                name: 'Kristall-Sammler',
                description: 'Sammle Kristallscherben von besiegten Gegnern oder in Dungeons.',
                type: 'collect',
                giver: 'wanderer_schatzjaeger',
                objectives: [
                    { type: 'collect', target: 'crystal_shard', required: 5, description: 'Sammle 5 Kristallscherben' }
                ],
                rewards: { gold: 100, items: ['health_potion', 'mana_potion'], xp: 150 }
            },
            {
                id: 'erste_schritte',
                name: 'Erste Schritte',
                description: 'Sprich mit dem Händler am Götterfels um die Welt kennenzulernen.',
                type: 'talk',
                giver: 'goetterfels_questgeber',
                objectives: [
                    { type: 'talk', target: 'goetterfels_haendler', required: 1, description: 'Sprich mit dem Reisenden Händler' }
                ],
                rewards: { gold: 25, items: ['bread'], xp: 50 }
            },
            {
                id: 'erkunder',
                name: 'Erkunder der Welt',
                description: 'Erkunde 3 verschiedene Regionen der Welt.',
                type: 'explore',
                giver: 'goetterfels_questgeber',
                objectives: [
                    { type: 'explore', target: 'samtmoos', required: 1, description: 'Besuche den Samtmoos-Tiefwald' },
                    { type: 'explore', target: 'heisse_duenen', required: 1, description: 'Besuche die Heißen Dünen' },
                    { type: 'explore', target: 'salzwind', required: 1, description: 'Besuche die Salzwind-Küste' }
                ],
                rewards: { gold: 150, items: [], xp: 300 }
            },
            {
                id: 'monster_jaeger',
                name: 'Monster-Jäger',
                description: 'Besiege 10 beliebige Gegner um deine Kampffähigkeiten zu beweisen.',
                type: 'kill',
                giver: null,
                objectives: [
                    { type: 'kill', target: 'any', required: 10, description: 'Besiege 10 Gegner' }
                ],
                rewards: { gold: 200, items: ['steel_sword'], xp: 500 }
            },

            // ===== WORLD EXPLORATION QUEST =====
            {
                id: 'world_explorer',
                name: 'Welt-Entdecker',
                description: 'Erkunde alle 9 Regionen der Welt!',
                type: 'explore',
                giver: null, // Auto-available
                objectives: [
                    {
                        type: 'explore',
                        target: 'ice',
                        required: 1,
                        description: 'Erkunde die Eisregion'
                    },
                    {
                        type: 'explore',
                        target: 'highland',
                        required: 1,
                        description: 'Erkunde das Hochland'
                    },
                    {
                        type: 'explore',
                        target: 'desert',
                        required: 1,
                        description: 'Erkunde die Wüste'
                    },
                    {
                        type: 'explore',
                        target: 'forest',
                        required: 1,
                        description: 'Erkunde den Wald'
                    },
                    {
                        type: 'explore',
                        target: 'coast',
                        required: 1,
                        description: 'Erkunde die Küste'
                    },
                    {
                        type: 'explore',
                        target: 'volcano',
                        required: 1,
                        description: 'Erkunde den Vulkan'
                    },
                    {
                        type: 'explore',
                        target: 'swamp',
                        required: 1,
                        description: 'Erkunde den Sumpf'
                    },
                    {
                        type: 'explore',
                        target: 'mountain',
                        required: 1,
                        description: 'Erkunde die Berge'
                    },
                    {
                        type: 'explore',
                        target: 'plains',
                        required: 1,
                        description: 'Erkunde die Ebene'
                    }
                ],
                rewards: {
                    gold: 1000,
                    items: ['champion_keule'],
                    xp: 2000
                }
            }
        ];

        // Add quests to database
        quests.forEach(questData => {
            this.quests[questData.id] = new Quest(questData);
        });

        console.log(`📋 ${quests.length} Quests geladen`);
    }

    // Accept a quest
    acceptQuest(questId) {
        const quest = this.quests[questId];
        if (!quest) {
            console.error(`❌ Quest nicht gefunden: ${questId}`);
            return false;
        }

        if (quest.status !== 'available') {
            console.warn(`⚠️ Quest "${quest.name}" ist nicht verfügbar (Status: ${quest.status})`);
            return false;
        }

        quest.status = 'active';
        this.activeQuests.push(questId);

        // Auto-track first quest
        if (!this.trackedQuest) {
            this.trackQuest(questId);
        }

        console.log(`✅ Quest angenommen: "${quest.name}"`);
        return true;
    }

    // Update quest progress
    updateQuest(questId, objectiveIndex, amount = 1) {
        const quest = this.quests[questId];
        if (!quest || quest.status !== 'active') return false;

        quest.updateObjective(objectiveIndex, amount);

        // Check if quest is complete
        if (quest.isComplete()) {
            this.showQuestCompleteNotification(questId);
        }

        return true;
    }

    // Update quests by trigger (automatic)
    updateQuestsByTrigger(triggerType, triggerTarget, amount = 1) {
        let updated = false;

        this.activeQuests.forEach(questId => {
            const quest = this.quests[questId];
            if (!quest || quest.status !== 'active') return;

            quest.objectives.forEach((obj, index) => {
                if (obj.type === triggerType) {
                    // Check if target matches (or 'any')
                    if (obj.target === triggerTarget || obj.target === 'any') {
                        quest.updateObjective(index, amount);
                        updated = true;
                    }
                }
            });
        });

        return updated;
    }

    // Complete a quest + REWARDS VERGEBEN
    completeQuest(questId) {
        const quest = this.quests[questId];
        if (!quest) return false;

        if (!quest.isComplete()) {
            console.warn(`⚠️ Quest "${quest.name}" ist noch nicht abgeschlossen!`);
            return false;
        }

        quest.status = 'completed';
        this.activeQuests = this.activeQuests.filter(id => id !== questId);
        this.completedQuests.push(questId);

        // Untrack if this was tracked
        if (this.trackedQuest === questId) {
            this.trackedQuest = null;
        }

        // ===== REWARDS VERGEBEN =====
        const rewards = quest.rewards || {};

        // Gold
        if (rewards.gold > 0 && window.inventorySystem && window.inventorySystem.addGold) {
            window.inventorySystem.addGold(rewards.gold);
            console.log(`💰 +${rewards.gold} Gold`);
        }

        // Items
        if (rewards.items && rewards.items.length > 0 && window.inventorySystem) {
            rewards.items.forEach(itemId => {
                window.inventorySystem.addItem(itemId, 1);
                console.log(`📦 +1 ${itemId}`);
            });
        }

        // XP (via GameEvents)
        if (rewards.xp > 0 && window.GameEvents) {
            window.GameEvents.emit('xpGained', { amount: rewards.xp, source: 'quest', questId });
        }

        // Quest-Complete Event
        if (window.GameEvents) {
            window.GameEvents.emit('questCompleted', { questId, questName: quest.name, rewards });
        }

        // Notification
        this.showQuestRewardNotification(quest);

        console.log(`🎉 Quest abgeschlossen: "${quest.name}"`);
        return true;
    }

    showQuestRewardNotification(quest) {
        const rewards = quest.rewards || {};
        let rewardText = [];
        if (rewards.gold) rewardText.push(`💰 ${rewards.gold} Gold`);
        if (rewards.xp) rewardText.push(`⭐ ${rewards.xp} XP`);
        if (rewards.items?.length) rewardText.push(`📦 ${rewards.items.length} Items`);

        const notif = document.createElement('div');
        notif.style.cssText = `
            position: fixed; top: 80px; left: 50%; transform: translateX(-50%);
            background: linear-gradient(135deg, rgba(0,100,0,0.95), rgba(0,60,0,0.95));
            color: #fff; padding: 15px 30px; border-radius: 12px; z-index: 5000;
            border: 2px solid #FFD700; font-family: Arial; text-align: center;
            animation: fadeInDown 0.5s ease;
        `;
        notif.innerHTML = `
            <div style="font-size:18px; font-weight:bold; color:#FFD700;">🎉 Quest Abgeschlossen!</div>
            <div style="font-size:14px; margin:5px 0;">${quest.name}</div>
            <div style="font-size:13px; color:#aaffaa;">${rewardText.join(' | ')}</div>
        `;
        document.body.appendChild(notif);
        setTimeout(() => notif.remove(), 4000);
    }

    // ===== GAME EVENT LISTENERS =====
    // Verbindet Quest-System mit dem globalen Event-Bus

    connectToGameEvents() {
        if (!window.GameEvents) {
            console.warn('⚠️ GameEvents nicht verfügbar, Quest-Events deaktiviert');
            return;
        }

        // Kill-Events → Quest-Progress
        window.GameEvents.on('enemyKilled', (data) => {
            const updated = this.updateQuestsByTrigger('kill', data.enemyType || data.enemyId, 1);
            if (updated) this.autoCompleteQuests();
        });

        // Item-Collect → Quest-Progress
        window.GameEvents.on('itemCollected', (data) => {
            const updated = this.updateQuestsByTrigger('collect', data.itemId, data.quantity || 1);
            if (updated) this.autoCompleteQuests();
        });

        // NPC-Talk → Quest-Progress
        window.GameEvents.on('npcTalked', (data) => {
            const updated = this.updateQuestsByTrigger('talk', data.npcId, 1);
            if (updated) this.autoCompleteQuests();
        });

        // Region-Enter → Quest-Progress
        window.GameEvents.on('regionEntered', (data) => {
            const updated = this.updateQuestsByTrigger('explore', data.biome || data.regionId, 1);
            if (updated) this.autoCompleteQuests();
        });

        console.log('🔗 Quest-System mit GameEvents verbunden');
    }

    autoCompleteQuests() {
        // Prüfe ob aktive Quests fertig sind und schließe sie automatisch ab
        [...this.activeQuests].forEach(questId => {
            const quest = this.quests[questId];
            if (quest && quest.isComplete()) {
                this.completeQuest(questId);
            }
        });
    }

    // Track a quest (show in tracker)
    trackQuest(questId) {
        const quest = this.quests[questId];
        if (!quest || quest.status !== 'active') {
            console.warn(`⚠️ Quest kann nicht getrackt werden: ${questId}`);
            return false;
        }

        this.trackedQuest = questId;
        console.log(`📍 Tracking Quest: "${quest.name}"`);
        return true;
    }

    // Get quests available from NPC
    getQuestsFromNPC(npcId) {
        const available = [];

        for (const questId in this.quests) {
            const quest = this.quests[questId];
            if (quest.giver === npcId && quest.status === 'available') {
                available.push(quest);
            }
        }

        return available;
    }

    // Show quest complete notification
    showQuestCompleteNotification(questId) {
        const quest = this.quests[questId];
        if (!quest) return;

        // This will be shown in UI (handled in HTML)
        console.log(`🎉 QUEST COMPLETE: ${quest.name}`);

        // Dispatch custom event for UI
        if (typeof window !== 'undefined') {
            window.dispatchEvent(new CustomEvent('quest-complete', {
                detail: { questId, quest }
            }));
        }
    }

    // Get active quests
    getActiveQuests() {
        return this.activeQuests.map(id => this.quests[id]);
    }

    // Get completed quests
    getCompletedQuests() {
        return this.completedQuests.map(id => this.quests[id]);
    }

    // Get tracked quest
    getTrackedQuest() {
        return this.trackedQuest ? this.quests[this.trackedQuest] : null;
    }
}

// Export for global use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { Quest, QuestManager };
}
