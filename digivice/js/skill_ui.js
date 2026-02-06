/**
 * NAJIKA WORLD - SKILL UI (K-Taste)
 * ===================================
 *
 * Skill-Übersicht UI System
 *
 * Features:
 * - K-Taste öffnet Skill-Übersicht
 * - Kategorien nach Zauberschulen (type)
 * - 1-Weg-Skills markiert (permanent, trade-offs)
 * - Equip/Unequip Skills
 * - Level/XP Progress
 * - Skill Details
 *
 * Integration: skill_system.js
 */

class SkillUI {
    constructor(skillSystem) {
        this.skillSystem = skillSystem;

        // UI State
        this.uiVisible = false;
        this.selectedCategory = 'all';

        // Categories (Zauberschulen)
        this.categories = {
            'all': { name: 'Alle Skills', icon: '📚' },
            'rune_magic': { name: 'Runen-Magie', icon: '📜' },
            'lightning_magic': { name: 'Blitz-Magie', icon: '⚡' },
            'nature_magic': { name: 'Natur-Magie', icon: '🌿' },
            'smithing': { name: 'Schmiedekunst', icon: '🔨' },
            'explosion': { name: 'Explosion (1-Weg)', icon: '💥' }
        };

        // Bind K-Key
        this.bindKeyboardShortcut();

        console.log('[SkillUI] Initialized');
    }

    // ===== KEYBOARD SHORTCUT =====

    bindKeyboardShortcut() {
        document.addEventListener('keydown', (e) => {
            // K-Taste öffnet Skill-Übersicht
            if (e.key === 'k' || e.key === 'K') {
                // Nicht in Chat/Input Feldern
                if (document.activeElement.tagName === 'INPUT' ||
                    document.activeElement.tagName === 'TEXTAREA') {
                    return;
                }

                e.preventDefault();
                this.toggleUI();
            }
        });

        console.log('[SkillUI] K-Taste bound to toggle UI');
    }

    // ===== UI CREATION =====

    createUI() {
        // Check if already exists
        if (document.getElementById('skill-ui')) {
            return document.getElementById('skill-ui');
        }

        // Create main container
        const container = document.createElement('div');
        container.id = 'skill-ui';
        container.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 800px;
            max-height: 85vh;
            background: rgba(20, 20, 30, 0.98);
            border: 3px solid #00aaff;
            border-radius: 12px;
            padding: 0;
            color: white;
            font-family: 'Courier New', monospace;
            z-index: 10000;
            display: none;
            overflow: hidden;
            box-shadow: 0 10px 50px rgba(0, 170, 255, 0.5);
        `;

        container.innerHTML = `
            <!-- Header -->
            <div style="background: linear-gradient(135deg, #00aaff, #0066cc); padding: 20px; display: flex; justify-content: space-between; align-items: center;">
                <h2 style="margin: 0; color: white; font-size: 22px;">📚 Skill-Übersicht</h2>
                <div style="display: flex; gap: 15px; align-items: center;">
                    <span style="font-size: 12px; color: rgba(255,255,255,0.8);">Taste [K] zum Schließen</span>
                    <button id="skill-ui-close" style="background: rgba(255,255,255,0.2); border: 2px solid white; color: white; font-size: 20px; cursor: pointer; padding: 5px 12px; border-radius: 6px;">×</button>
                </div>
            </div>

            <!-- Category Tabs -->
            <div id="skill-categories" style="display: flex; background: rgba(0, 0, 0, 0.3); border-bottom: 2px solid #00aaff; overflow-x: auto;">
                <!-- Categories will be inserted here -->
            </div>

            <!-- Main Content Area -->
            <div style="display: flex; height: calc(85vh - 140px); overflow: hidden;">
                <!-- Skill List (Left) -->
                <div id="skill-list" style="flex: 1; overflow-y: auto; padding: 20px; border-right: 2px solid rgba(0, 170, 255, 0.3);">
                    <!-- Skills will be listed here -->
                </div>

                <!-- Skill Detail (Right) -->
                <div id="skill-detail" style="width: 320px; overflow-y: auto; padding: 20px; background: rgba(0, 0, 0, 0.2);">
                    <div style="text-align: center; color: #888; padding-top: 50px;">
                        <div style="font-size: 48px;">📚</div>
                        <p>Wähle einen Skill aus, um Details zu sehen</p>
                    </div>
                </div>
            </div>

            <!-- Footer Stats -->
            <div style="background: rgba(0, 0, 0, 0.3); padding: 12px 20px; border-top: 2px solid #00aaff; display: flex; justify-content: space-between; font-size: 12px;">
                <div>📚 Gelernte Skills: <span id="stat-learned-skills">0</span></div>
                <div>⚔️ Ausgerüstete Skills: <span id="stat-equipped-skills">0</span> / 4</div>
            </div>
        `;

        document.body.appendChild(container);

        // Bind Events
        this.bindEvents();

        // Initialize Categories
        this.renderCategories();

        // Render Skills
        this.renderSkills();

        return container;
    }

    bindEvents() {
        // Close Button
        document.getElementById('skill-ui-close').addEventListener('click', () => {
            this.hideUI();
        });

        // ESC key closes UI
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.uiVisible) {
                this.hideUI();
            }
        });
    }

    // ===== UI VISIBILITY =====

    showUI() {
        if (!document.getElementById('skill-ui')) {
            this.createUI();
        }

        document.getElementById('skill-ui').style.display = 'block';
        this.uiVisible = true;

        // Refresh content
        this.renderSkills();
        this.updateStats();
    }

    hideUI() {
        const ui = document.getElementById('skill-ui');
        if (ui) {
            ui.style.display = 'none';
        }
        this.uiVisible = false;
    }

    toggleUI() {
        if (this.uiVisible) {
            this.hideUI();
        } else {
            this.showUI();
        }
    }

    // ===== CATEGORY RENDERING =====

    renderCategories() {
        const container = document.getElementById('skill-categories');
        if (!container) return;

        container.innerHTML = '';

        for (const [catId, catData] of Object.entries(this.categories)) {
            const tab = document.createElement('button');
            tab.style.cssText = `
                background: ${this.selectedCategory === catId ? 'rgba(0, 170, 255, 0.3)' : 'transparent'};
                border: none;
                border-bottom: 3px solid ${this.selectedCategory === catId ? '#00aaff' : 'transparent'};
                color: ${this.selectedCategory === catId ? '#00aaff' : '#aaa'};
                padding: 12px 20px;
                cursor: pointer;
                font-size: 13px;
                font-family: 'Courier New', monospace;
                white-space: nowrap;
                transition: all 0.2s;
            `;
            tab.textContent = `${catData.icon} ${catData.name}`;

            tab.addEventListener('click', () => {
                this.selectedCategory = catId;
                this.renderCategories();
                this.renderSkills();
            });

            tab.addEventListener('mouseenter', () => {
                if (this.selectedCategory !== catId) {
                    tab.style.background = 'rgba(0, 170, 255, 0.1)';
                }
            });

            tab.addEventListener('mouseleave', () => {
                if (this.selectedCategory !== catId) {
                    tab.style.background = 'transparent';
                }
            });

            container.appendChild(tab);
        }
    }

    // ===== SKILL LIST RENDERING =====

    renderSkills() {
        const container = document.getElementById('skill-list');
        if (!container) return;

        container.innerHTML = '';

        // Get all skills from database
        const allSkills = Object.values(this.skillSystem.skillDatabase);

        // Filter by category
        const filteredSkills = this.selectedCategory === 'all'
            ? allSkills
            : allSkills.filter(skill => skill.type === this.selectedCategory);

        if (filteredSkills.length === 0) {
            container.innerHTML = '<div style="color: #888; text-align: center; padding: 50px 20px;">Keine Skills in dieser Kategorie</div>';
            return;
        }

        // Render each skill
        filteredSkills.forEach(skillData => {
            const isLearned = !!this.skillSystem.learnedSkills[skillData.id];
            const isEquipped = this.skillSystem.equippedSkills.includes(skillData.id);
            const skill = isLearned ? this.skillSystem.learnedSkills[skillData.id] : null;

            // Check if 1-Weg-Skill
            const isOneWay = skillData.one_way || skillData.type === 'explosion';

            const skillItem = document.createElement('div');
            skillItem.style.cssText = `
                background: ${isLearned ? 'rgba(0, 170, 255, 0.15)' : 'rgba(255, 255, 255, 0.05)'};
                border: 2px solid ${isEquipped ? '#00ff00' : (isLearned ? '#00aaff' : '#555')};
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 12px;
                cursor: pointer;
                transition: all 0.2s;
                position: relative;
            `;

            // 1-Weg Badge
            const oneWayBadge = isOneWay ? `
                <span style="position: absolute; top: 10px; right: 10px; background: #ff4444; color: white; padding: 3px 8px; border-radius: 4px; font-size: 9px; font-weight: bold;">
                    1-WEG ⚠️
                </span>
            ` : '';

            // Equipped Badge
            const equippedBadge = isEquipped ? `
                <span style="position: absolute; top: 10px; right: ${isOneWay ? '90px' : '10px'}; background: #00ff00; color: black; padding: 3px 8px; border-radius: 4px; font-size: 9px; font-weight: bold;">
                    ⚔️ EQUIPPED
                </span>
            ` : '';

            skillItem.innerHTML = `
                ${oneWayBadge}
                ${equippedBadge}
                <div style="display: flex; align-items: center; gap: 15px;">
                    <div style="font-size: 32px;">${skillData.icon}</div>
                    <div style="flex: 1;">
                        <div style="font-size: 16px; font-weight: bold; color: ${isLearned ? '#00aaff' : '#888'};">
                            ${skillData.name}
                            ${isLearned ? `<span style="font-size: 12px; color: #ffa500; margin-left: 8px;">Lv.${skill.level}</span>` : ''}
                        </div>
                        <div style="font-size: 11px; color: #aaa; margin-top: 4px;">
                            ${skillData.description}
                        </div>
                        ${isLearned && skill ? `
                            <div style="margin-top: 8px; background: rgba(0,0,0,0.3); border-radius: 4px; height: 8px; overflow: hidden;">
                                <div style="background: linear-gradient(90deg, #00aaff, #00ff88); height: 100%; width: ${(skill.xp / skill.xpRequired) * 100}%;"></div>
                            </div>
                            <div style="font-size: 9px; color: #888; margin-top: 2px;">
                                XP: ${skill.xp} / ${skill.xpRequired}
                            </div>
                        ` : ''}
                    </div>
                    <div style="display: flex; flex-direction: column; gap: 5px;">
                        ${!isLearned ? `
                            <div style="font-size: 11px; color: #ffa500;">
                                💰 ${skillData.cost}g
                            </div>
                        ` : ''}
                    </div>
                </div>
            `;

            skillItem.addEventListener('click', () => {
                this.showSkillDetail(skillData, skill);
            });

            skillItem.addEventListener('mouseenter', () => {
                skillItem.style.transform = 'translateX(5px)';
                if (!isLearned) {
                    skillItem.style.background = 'rgba(255, 255, 255, 0.08)';
                } else {
                    skillItem.style.background = 'rgba(0, 170, 255, 0.25)';
                }
            });

            skillItem.addEventListener('mouseleave', () => {
                skillItem.style.transform = 'translateX(0)';
                if (!isLearned) {
                    skillItem.style.background = 'rgba(255, 255, 255, 0.05)';
                } else {
                    skillItem.style.background = 'rgba(0, 170, 255, 0.15)';
                }
            });

            container.appendChild(skillItem);
        });

        this.updateStats();
    }

    // ===== SKILL DETAIL =====

    showSkillDetail(skillData, skill) {
        const container = document.getElementById('skill-detail');
        if (!container) return;

        const isLearned = !!skill;
        const isEquipped = this.skillSystem.equippedSkills.includes(skillData.id);
        const isOneWay = skillData.one_way || skillData.type === 'explosion';

        container.innerHTML = `
            <div style="text-align: center;">
                <div style="font-size: 64px; margin-bottom: 15px;">${skillData.icon}</div>
                <h3 style="margin: 0 0 10px 0; color: #00aaff; font-size: 18px;">${skillData.name}</h3>
                ${isOneWay ? `
                    <div style="background: rgba(255, 68, 68, 0.2); border: 2px solid #ff4444; border-radius: 8px; padding: 10px; margin-bottom: 15px;">
                        <div style="font-weight: bold; color: #ff4444; margin-bottom: 5px;">⚠️ 1-WEG-SKILL</div>
                        <div style="font-size: 10px; line-height: 1.5; color: #ffaaaa;">
                            Permanent! Kann nicht rückgängig gemacht werden.<br>
                            Trade-offs: +35% Power / -18% Mana Efficiency
                        </div>
                    </div>
                ` : ''}
                ${isLearned ? `
                    <div style="margin-bottom: 15px;">
                        <div style="font-size: 14px; color: #ffa500; margin-bottom: 5px;">Level ${skill.level} / 10</div>
                        <div style="background: rgba(0,0,0,0.5); border-radius: 6px; height: 12px; overflow: hidden; margin-bottom: 5px;">
                            <div style="background: linear-gradient(90deg, #00aaff, #00ff88); height: 100%; width: ${(skill.xp / skill.xpRequired) * 100}%;"></div>
                        </div>
                        <div style="font-size: 10px; color: #888;">XP: ${skill.xp} / ${skill.xpRequired}</div>
                    </div>
                ` : ''}
            </div>

            <!-- Description -->
            <div style="background: rgba(0, 170, 255, 0.1); border: 2px solid #00aaff; border-radius: 8px; padding: 12px; margin-bottom: 15px;">
                <div style="font-size: 12px; line-height: 1.6; color: #ccc;">${skillData.description}</div>
            </div>

            <!-- Stats -->
            <div style="font-size: 12px; line-height: 1.8; margin-bottom: 15px;">
                <div style="display: flex; justify-content: space-between; padding: 5px 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
                    <span style="color: #888;">⚡ Power:</span>
                    <span style="color: #00aaff;">${isLearned ? skill.getPowerAtLevel() : skillData.power}</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 5px 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
                    <span style="color: #888;">💧 Mana Cost:</span>
                    <span style="color: #00aaff;">${isLearned ? skill.getManaCostAtLevel() : skillData.manaCost}</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 5px 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
                    <span style="color: #888;">⏱️ Cooldown:</span>
                    <span style="color: #00aaff;">${isLearned ? skill.getCooldownAtLevel().toFixed(1) : skillData.cooldown}s</span>
                </div>
                ${!isLearned ? `
                    <div style="display: flex; justify-content: space-between; padding: 5px 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
                        <span style="color: #888;">💰 Cost:</span>
                        <span style="color: #ffa500;">${skillData.cost}g</span>
                    </div>
                ` : ''}
                <div style="display: flex; justify-content: space-between; padding: 5px 0;">
                    <span style="color: #888;">📚 Kategorie:</span>
                    <span style="color: #00aaff;">${this.categories[skillData.type]?.name || skillData.type}</span>
                </div>
            </div>

            <!-- Actions -->
            <div style="display: flex; flex-direction: column; gap: 10px;">
                ${isLearned ? `
                    ${isEquipped ? `
                        <button onclick="skillUI.unequipSkill('${skillData.id}')" style="background: #ff4444; border: none; color: white; padding: 12px; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 13px;">
                            🔓 Skill ablegen
                        </button>
                    ` : `
                        <button onclick="skillUI.equipSkill('${skillData.id}')" style="background: #00aaff; border: none; color: white; padding: 12px; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 13px;">
                            ⚔️ Skill ausrüsten
                        </button>
                    `}
                ` : `
                    <button onclick="skillUI.learnSkill('${skillData.id}')" style="background: #00ff88; border: none; color: black; padding: 12px; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 13px;">
                        📚 Skill lernen (${skillData.cost}g)
                    </button>
                `}
            </div>

            ${skillData.trainer ? `
                <div style="margin-top: 15px; padding-top: 15px; border-top: 2px solid rgba(255,255,255,0.1); font-size: 11px; color: #888;">
                    👨‍🏫 Trainer: ${skillData.trainer}
                </div>
            ` : ''}
        `;
    }

    // ===== SKILL ACTIONS =====

    learnSkill(skillId) {
        const success = this.skillSystem.learnSkill(skillId);
        if (success) {
            this.renderSkills();
            const skillData = this.skillSystem.skillDatabase[skillId];
            const skill = this.skillSystem.learnedSkills[skillId];
            this.showSkillDetail(skillData, skill);
        }
    }

    equipSkill(skillId) {
        const success = this.skillSystem.equipSkill(skillId);
        if (success) {
            this.renderSkills();
            const skillData = this.skillSystem.skillDatabase[skillId];
            const skill = this.skillSystem.learnedSkills[skillId];
            this.showSkillDetail(skillData, skill);
        } else {
            alert('⚠️ Alle Skill-Slots belegt! (Max 4)');
        }
    }

    unequipSkill(skillId) {
        const success = this.skillSystem.unequipSkill(skillId);
        if (success) {
            this.renderSkills();
            const skillData = this.skillSystem.skillDatabase[skillId];
            const skill = this.skillSystem.learnedSkills[skillId];
            this.showSkillDetail(skillData, skill);
        }
    }

    // ===== STATS UPDATE =====

    updateStats() {
        const learnedCount = Object.keys(this.skillSystem.learnedSkills).length;
        const equippedCount = this.skillSystem.equippedSkills.length;

        const learnedEl = document.getElementById('stat-learned-skills');
        const equippedEl = document.getElementById('stat-equipped-skills');

        if (learnedEl) learnedEl.textContent = learnedCount;
        if (equippedEl) equippedEl.textContent = equippedCount;
    }
}

// Global Instance (wird nach skillSystem initialisiert)
if (typeof window !== 'undefined') {
    window.skillUI = null; // Will be initialized after skillSystem
}

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SkillUI;
}
