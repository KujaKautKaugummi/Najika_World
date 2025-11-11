/**
 * NAJIKA WORLD - SKILL SYSTEM
 * ============================
 *
 * Skill-System mit:
 * - Skill lernen bei Trainern
 * - Skill-Leveling (1-10)
 * - XP-System
 * - Skill-UI (Character Menu)
 */

class Skill {
    constructor(data) {
        this.id = data.id;
        this.name = data.name;
        this.type = data.type; // 'rune_magic', 'lightning_magic', 'nature_magic', etc.
        this.description = data.description;
        this.level = data.level || 1;
        this.xp = data.xp || 0;
        this.xpRequired = this.calculateXPRequired(this.level);
        this.icon = data.icon || '⚡';

        // Requirements
        this.requiredLevel = data.requiredLevel || 1;
        this.cost = data.cost || 0; // Gold cost to learn

        // Stats
        this.power = data.power || 10; // Base power
        this.manaCost = data.manaCost || 10; // Mana per use
        this.cooldown = data.cooldown || 5; // Seconds

        // Trainer
        this.trainer = data.trainer || null; // NPC ID who teaches this
    }

    calculateXPRequired(level) {
        // XP benötigt für nächstes Level: 100 * level^1.5
        return Math.floor(100 * Math.pow(level, 1.5));
    }

    addXP(amount) {
        this.xp += amount;

        // Level up?
        while (this.xp >= this.xpRequired && this.level < 10) {
            this.xp -= this.xpRequired;
            this.level++;
            this.xpRequired = this.calculateXPRequired(this.level);

            // Increase stats on level up
            this.power += 5;

            console.log(`✨ ${this.name} Level UP! Level ${this.level}`);
        }
    }

    getPowerAtLevel() {
        // Power increases with level
        return this.power + (this.level - 1) * 5;
    }

    getManaCostAtLevel() {
        // Mana cost decreases slightly with level
        return Math.max(5, this.manaCost - Math.floor((this.level - 1) * 0.5));
    }

    getCooldownAtLevel() {
        // Cooldown decreases with level
        return Math.max(1, this.cooldown - (this.level - 1) * 0.2);
    }
}

class SkillSystem {
    constructor(inventorySystem = null) {
        this.inventorySystem = inventorySystem;

        // Player skills
        this.learnedSkills = {}; // skill_id => Skill
        this.equippedSkills = []; // Max 4 equipped skills
        this.maxEquippedSkills = 4;

        // Skill Database
        this.skillDatabase = this.loadSkillDatabase();

        console.log('📚 Skill-System initialisiert');
    }

    loadSkillDatabase() {
        return {
            // ===== RUNE MAGIC (Runenheim) =====
            'rune_fireball': {
                id: 'rune_fireball',
                name: 'Runen-Feuerball',
                type: 'rune_magic',
                description: 'Feuert einen mächtigen Feuerball ab',
                icon: '🔥',
                power: 30,
                manaCost: 20,
                cooldown: 5,
                requiredLevel: 1,
                cost: 100,
                trainer: 'runenheim_mage_teacher'
            },
            'rune_ice_lance': {
                id: 'rune_ice_lance',
                name: 'Runen-Eislanze',
                type: 'rune_magic',
                description: 'Schießt eine gefrorene Lanze',
                icon: '❄️',
                power: 35,
                manaCost: 25,
                cooldown: 6,
                requiredLevel: 3,
                cost: 200,
                trainer: 'runenheim_mage_teacher'
            },
            'rune_lightning': {
                id: 'rune_lightning',
                name: 'Runen-Blitz',
                type: 'rune_magic',
                description: 'Ruft einen Blitz vom Himmel',
                icon: '⚡',
                power: 50,
                manaCost: 40,
                cooldown: 8,
                requiredLevel: 5,
                cost: 500,
                trainer: 'runenheim_mage_teacher'
            },

            // ===== LIGHTNING MAGIC (Runenheim) =====
            'lightning_bolt': {
                id: 'lightning_bolt',
                name: 'Blitzschlag',
                type: 'lightning_magic',
                description: 'Schneller Blitzangriff',
                icon: '⚡',
                power: 25,
                manaCost: 15,
                cooldown: 3,
                requiredLevel: 1,
                cost: 150,
                trainer: 'runenheim_mage_teacher'
            },
            'chain_lightning': {
                id: 'chain_lightning',
                name: 'Kettenblitz',
                type: 'lightning_magic',
                description: 'Blitz springt zwischen Gegnern',
                icon: '⚡⚡',
                power: 40,
                manaCost: 30,
                cooldown: 7,
                requiredLevel: 4,
                cost: 400,
                trainer: 'runenheim_mage_teacher'
            },

            // ===== NATURE MAGIC (Dampf-Hain, Quest) =====
            'nature_heal': {
                id: 'nature_heal',
                name: 'Naturheilung',
                type: 'nature_magic',
                description: 'Heilt HP über Zeit',
                icon: '🌿',
                power: 20, // Healing power
                manaCost: 25,
                cooldown: 10,
                requiredLevel: 2,
                cost: 0, // Quest reward
                trainer: 'dampf_hain_druid'
            },
            'nature_roots': {
                id: 'nature_roots',
                name: 'Wurzel-Fesseln',
                type: 'nature_magic',
                description: 'Fesselt Gegner für 5 Sekunden',
                icon: '🌳',
                power: 15,
                manaCost: 20,
                cooldown: 12,
                requiredLevel: 3,
                cost: 0, // Quest reward
                trainer: 'dampf_hain_druid'
            },

            // ===== SMITHING (Funken-Siedlung) =====
            'weapon_repair': {
                id: 'weapon_repair',
                name: 'Waffen-Reparatur',
                type: 'smithing',
                description: 'Repariert beschädigte Waffen',
                icon: '🔨',
                power: 0, // Utility skill
                manaCost: 0,
                cooldown: 60,
                requiredLevel: 1,
                cost: 100,
                trainer: 'funken_siedlung_forge_worker'
            },
            'weapon_enchant': {
                id: 'weapon_enchant',
                name: 'Waffen-Verzauberung',
                type: 'smithing',
                description: 'Verzaubert Waffen (+10% Damage)',
                icon: '✨',
                power: 10, // Bonus %
                manaCost: 0,
                cooldown: 120,
                requiredLevel: 5,
                cost: 500,
                trainer: 'funken_siedlung_master_smith'
            }
        };
    }

    // ===== LEARN SKILL =====

    canLearnSkill(skillId) {
        const skillData = this.skillDatabase[skillId];
        if (!skillData) return { canLearn: false, reason: 'Skill nicht gefunden' };

        // Already learned?
        if (this.learnedSkills[skillId]) {
            return { canLearn: false, reason: 'Skill bereits gelernt' };
        }

        // Enough gold?
        if (this.inventorySystem && !this.inventorySystem.hasGold(skillData.cost)) {
            return { canLearn: false, reason: `Nicht genug Gold (${skillData.cost}g benötigt)` };
        }

        // Level requirement?
        // (Player-Level-System noch nicht implementiert, daher übersprungen)

        return { canLearn: true };
    }

    learnSkill(skillId) {
        const check = this.canLearnSkill(skillId);
        if (!check.canLearn) {
            console.warn(`⚠️ Kann Skill nicht lernen: ${check.reason}`);
            return false;
        }

        const skillData = this.skillDatabase[skillId];
        const skill = new Skill(skillData);

        // Pay cost
        if (this.inventorySystem && skillData.cost > 0) {
            this.inventorySystem.removeGold(skillData.cost);
        }

        // Learn skill
        this.learnedSkills[skillId] = skill;

        // Auto-equip if space available
        if (this.equippedSkills.length < this.maxEquippedSkills) {
            this.equipSkill(skillId);
        }

        console.log(`📚 Skill gelernt: ${skill.icon} ${skill.name}`);
        return true;
    }

    // ===== EQUIP SKILL =====

    equipSkill(skillId) {
        const skill = this.learnedSkills[skillId];
        if (!skill) {
            console.warn(`⚠️ Skill nicht gelernt: ${skillId}`);
            return false;
        }

        if (this.equippedSkills.length >= this.maxEquippedSkills) {
            console.warn(`⚠️ Alle Skill-Slots belegt! (Max ${this.maxEquippedSkills})`);
            return false;
        }

        if (this.equippedSkills.includes(skillId)) {
            console.warn(`⚠️ Skill bereits ausgerüstet: ${skillId}`);
            return false;
        }

        this.equippedSkills.push(skillId);
        console.log(`⚔️ Skill ausgerüstet: ${skill.name} (Slot ${this.equippedSkills.length})`);
        return true;
    }

    unequipSkill(skillId) {
        const index = this.equippedSkills.indexOf(skillId);
        if (index === -1) {
            console.warn(`⚠️ Skill nicht ausgerüstet: ${skillId}`);
            return false;
        }

        this.equippedSkills.splice(index, 1);
        console.log(`🔓 Skill abgelegt: ${skillId}`);
        return true;
    }

    // ===== USE SKILL =====

    useSkill(skillId, target = null) {
        const skill = this.learnedSkills[skillId];
        if (!skill) {
            console.warn(`⚠️ Skill nicht gelernt: ${skillId}`);
            return false;
        }

        if (!this.equippedSkills.includes(skillId)) {
            console.warn(`⚠️ Skill nicht ausgerüstet: ${skillId}`);
            return false;
        }

        // Check mana
        // (Mana-System noch nicht vollständig implementiert)

        // Use skill
        console.log(`✨ ${skill.icon} ${skill.name} benutzt! (Power: ${skill.getPowerAtLevel()})`);

        // Add XP
        skill.addXP(10); // +10 XP per use

        return true;
    }

    // ===== GETTERS =====

    getLearnedSkills() {
        return Object.values(this.learnedSkills);
    }

    getEquippedSkills() {
        return this.equippedSkills.map(id => this.learnedSkills[id]);
    }

    getSkillsFromTrainer(trainerId) {
        const skills = [];
        for (const skillId in this.skillDatabase) {
            const skillData = this.skillDatabase[skillId];
            if (skillData.trainer === trainerId && !this.learnedSkills[skillId]) {
                skills.push(skillData);
            }
        }
        return skills;
    }

    // ===== SAVE/LOAD =====

    saveToLocalStorage() {
        const saveData = {
            learnedSkills: {},
            equippedSkills: this.equippedSkills
        };

        // Save learned skills
        for (const skillId in this.learnedSkills) {
            const skill = this.learnedSkills[skillId];
            saveData.learnedSkills[skillId] = {
                id: skill.id,
                level: skill.level,
                xp: skill.xp
            };
        }

        localStorage.setItem('najika_skills', JSON.stringify(saveData));
        console.log('💾 Skills gespeichert');
    }

    loadFromLocalStorage() {
        const saveData = localStorage.getItem('najika_skills');
        if (!saveData) return false;

        const data = JSON.parse(saveData);

        // Load learned skills
        for (const skillId in data.learnedSkills) {
            const savedSkill = data.learnedSkills[skillId];
            const skillData = this.skillDatabase[skillId];
            if (skillData) {
                const skill = new Skill(skillData);
                skill.level = savedSkill.level;
                skill.xp = savedSkill.xp;
                this.learnedSkills[skillId] = skill;
            }
        }

        // Load equipped skills
        this.equippedSkills = data.equippedSkills || [];

        console.log('💾 Skills geladen');
        return true;
    }
}

// Export für globale Nutzung
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { Skill, SkillSystem };
}
