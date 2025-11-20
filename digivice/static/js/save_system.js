/**
 * NAJIKA WORLD - SAVE/LOAD SYSTEM
 * =================================
 *
 * Speichersystem mit Auto-Save:
 * - LocalStorage-basiert
 * - Auto-Save alle 60 Sekunden
 * - Speichert: Position, Inventar, Quests, Skills, Gold, etc.
 */

class SaveSystem {
    constructor(gameState) {
        this.gameState = gameState; // Reference to all game systems

        // Auto-Save Settings
        this.autoSaveEnabled = true;
        this.autoSaveInterval = 60000; // 60 seconds
        this.autoSaveTimer = null;

        // Last save time
        this.lastSaveTime = null;

        // Start auto-save
        this.startAutoSave();

        console.log('💾 Save/Load System initialisiert');
    }

    // ===== SAVE =====

    saveGame() {
        const saveData = {
            version: '1.0',
            timestamp: Date.now(),
            player: this.savePlayerData(),
            inventory: this.saveInventoryData(),
            quests: this.saveQuestData(),
            skills: this.saveSkillData(),
            world: this.saveWorldData()
        };

        try {
            localStorage.setItem('najika_save', JSON.stringify(saveData));
            this.lastSaveTime = Date.now();
            console.log('💾 Spiel gespeichert!');
            this.showSaveNotification();
            return true;
        } catch (e) {
            console.error('❌ Fehler beim Speichern:', e);
            return false;
        }
    }

    savePlayerData() {
        // Check if gameState and character exist
        if (!this.gameState || !this.gameState.character) {
            console.warn('⚠️ Character not initialized yet, using defaults');
            return {
                position: { x: 4800, y: 0, z: 4800 }, // Default Götterfels
                health: 100,
                mana: 50,
                stamina: 100
            };
        }

        const { character } = this.gameState;
        return {
            position: {
                x: character.position.x,
                y: character.position.y,
                z: character.position.z
            },
            health: this.gameState.realtimeCombat?.playerHealth || 100,
            mana: this.gameState.realtimeCombat?.playerMana || 50,
            stamina: this.gameState.realtimeCombat?.playerStamina || 100
        };
    }

    saveInventoryData() {
        if (!this.gameState || !this.gameState.inventorySystem) {
            console.warn('⚠️ Inventory not initialized yet, using defaults');
            return { items: {}, equipment: {}, gold: 0 };
        }

        const { inventorySystem } = this.gameState;
        return {
            items: inventorySystem.items,
            equipment: inventorySystem.equipment,
            gold: inventorySystem.gold
        };
    }

    saveQuestData() {
        if (!this.gameState || !this.gameState.questManager) {
            console.warn('⚠️ Quest Manager not initialized yet, using defaults');
            return { activeQuests: [], completedQuests: [], trackedQuest: null };
        }

        const { questManager } = this.gameState;
        return {
            activeQuests: questManager.activeQuests,
            completedQuests: questManager.completedQuests,
            trackedQuest: questManager.trackedQuest
        };
    }

    saveSkillData() {
        if (!this.gameState || !this.gameState.skillSystem) {
            console.warn('⚠️ Skill System not initialized yet, using defaults');
            return { learnedSkills: {}, equippedSkills: [] };
        }

        const { skillSystem } = this.gameState;
        const learnedSkills = {};

        for (const skillId in skillSystem.learnedSkills) {
            const skill = skillSystem.learnedSkills[skillId];
            learnedSkills[skillId] = {
                id: skill.id,
                level: skill.level,
                xp: skill.xp
            };
        }

        return {
            learnedSkills: learnedSkills,
            equippedSkills: skillSystem.equippedSkills
        };
    }

    saveWorldData() {
        if (!this.gameState || !this.gameState.specialLocations) {
            console.warn('⚠️ Special Locations not initialized yet, using defaults');
            return { openedChests: [], exploredRegions: [] };
        }

        const { specialLocations } = this.gameState;
        return {
            openedChests: Array.from(specialLocations.openedChests || []),
            exploredRegions: Array.from(window.exploredRegions || [])
        };
    }

    // ===== LOAD =====

    loadGame() {
        const saveData = localStorage.getItem('najika_save');

        if (!saveData) {
            console.log('💾 Kein Spielstand gefunden');
            return false;
        }

        try {
            const data = JSON.parse(saveData);

            // Load player data
            this.loadPlayerData(data.player);

            // Load inventory
            this.loadInventoryData(data.inventory);

            // Load quests
            this.loadQuestData(data.quests);

            // Load skills
            this.loadSkillData(data.skills);

            // Load world
            this.loadWorldData(data.world);

            console.log('💾 Spielstand geladen!');
            this.showLoadNotification();
            return true;
        } catch (e) {
            console.error('❌ Fehler beim Laden:', e);
            return false;
        }
    }

    loadPlayerData(data) {
        const { character, realtimeCombat } = this.gameState;

        // Set position
        character.position.set(data.position.x, data.position.y, data.position.z);

        // Set stats
        if (realtimeCombat) {
            realtimeCombat.playerHealth = data.health;
            realtimeCombat.playerMana = data.mana;
            realtimeCombat.playerStamina = data.stamina;
        }
    }

    loadInventoryData(data) {
        const { inventorySystem } = this.gameState;

        inventorySystem.items = data.items || [];
        inventorySystem.equipment = data.equipment || {};
        inventorySystem.gold = data.gold || 0;
    }

    loadQuestData(data) {
        const { questManager } = this.gameState;

        // Reconstruct quests
        questManager.activeQuests = data.activeQuests || [];
        questManager.completedQuests = data.completedQuests || [];
        questManager.trackedQuest = data.trackedQuest || null;
    }

    loadSkillData(data) {
        const { skillSystem } = this.gameState;

        // Reconstruct skills
        for (const skillId in data.learnedSkills) {
            const savedSkill = data.learnedSkills[skillId];
            const skillData = skillSystem.skillDatabase[skillId];

            if (skillData) {
                const skill = new Skill(skillData);
                skill.level = savedSkill.level;
                skill.xp = savedSkill.xp;
                skillSystem.learnedSkills[skillId] = skill;
            }
        }

        skillSystem.equippedSkills = data.equippedSkills || [];
    }

    loadWorldData(data) {
        const { specialLocations } = this.gameState;

        // Restore opened chests
        if (data.openedChests) {
            specialLocations.openedChests = new Set(data.openedChests);
        }

        // Restore explored regions
        if (data.exploredRegions) {
            window.exploredRegions = new Set(data.exploredRegions);
        }
    }

    // ===== AUTO-SAVE =====

    startAutoSave() {
        if (!this.autoSaveEnabled) return;

        this.autoSaveTimer = setInterval(() => {
            this.saveGame();
        }, this.autoSaveInterval);

        console.log(`💾 Auto-Save aktiviert (alle ${this.autoSaveInterval / 1000}s)`);
    }

    stopAutoSave() {
        if (this.autoSaveTimer) {
            clearInterval(this.autoSaveTimer);
            this.autoSaveTimer = null;
        }
    }

    // ===== NOTIFICATIONS =====

    showSaveNotification() {
        this.showNotification('💾 Spiel gespeichert!', '#4CAF50');
    }

    showLoadNotification() {
        this.showNotification('💾 Spielstand geladen!', '#00aaff');
    }

    showNotification(text, color) {
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 80px;
            right: 20px;
            background: rgba(0, 0, 0, 0.9);
            padding: 15px 25px;
            border-radius: 8px;
            border: 2px solid ${color};
            color: white;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            z-index: 10000;
            animation: slideIn 0.3s ease-out;
        `;
        notification.textContent = text;

        document.body.appendChild(notification);

        // Remove after 3 seconds
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease-out';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }

    // ===== DELETE SAVE =====

    deleteSave() {
        if (confirm('⚠️ Spielstand wirklich löschen?')) {
            localStorage.removeItem('najika_save');
            console.log('💾 Spielstand gelöscht');
            alert('Spielstand gelöscht! Seite wird neu geladen...');
            location.reload();
        }
    }
}

// Export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SaveSystem;
}
