/**
 * NAJIKA WORLD - SKILL TREE UI
 * =============================
 * Skyrim-Style Skill-Baum Visualisierung
 * - Skills in der Hand ausrüstbar (wie Waffen)
 * - Learning by Doing Progression
 * - Element-Weaving (außer EXPLOSION!)
 */

class SkillTreeUI {
    constructor() {
        this.isOpen = false;
        this.overlay = null;
        this.selectedCategory = 'fire';

        // Skill Trees (Skyrim-Style)
        this.skillTrees = {
            fire: {
                name: 'Feuer-Magie',
                icon: '🔥',
                color: '#ff4400',
                skills: [
                    { id: 'fire_1', name: 'Feuer', tier: 1, power: 10, mana: 8, learned: true, equipped: false },
                    { id: 'fire_2', name: 'Feura', tier: 2, power: 25, mana: 15, learned: false, requires: 'fire_1', xpNeeded: 100 },
                    { id: 'fire_3', name: 'Feuga', tier: 3, power: 50, mana: 30, learned: false, requires: 'fire_2', xpNeeded: 300 },
                    { id: 'fire_4', name: 'Feuraga', tier: 4, power: 100, mana: 60, learned: false, requires: 'fire_3', xpNeeded: 600 }
                ]
            },
            ice: {
                name: 'Eis-Magie',
                icon: '❄️',
                color: '#00aaff',
                skills: [
                    { id: 'ice_1', name: 'Eis', tier: 1, power: 8, mana: 10, learned: true, equipped: false, effect: 'slow' },
                    { id: 'ice_2', name: 'Eisra', tier: 2, power: 20, mana: 18, learned: false, requires: 'ice_1', xpNeeded: 100 },
                    { id: 'ice_3', name: 'Eisga', tier: 3, power: 45, mana: 35, learned: false, requires: 'ice_2', xpNeeded: 300 },
                    { id: 'ice_4', name: 'Eisraga', tier: 4, power: 90, mana: 70, learned: false, requires: 'ice_3', xpNeeded: 600 }
                ]
            },
            lightning: {
                name: 'Blitz-Magie',
                icon: '⚡',
                color: '#ffdd00',
                skills: [
                    { id: 'lightning_1', name: 'Blitz', tier: 1, power: 12, mana: 7, learned: true, equipped: false },
                    { id: 'lightning_2', name: 'Blitzra', tier: 2, power: 28, mana: 14, learned: false, requires: 'lightning_1', xpNeeded: 100 },
                    { id: 'lightning_3', name: 'Blitzga', tier: 3, power: 55, mana: 28, learned: false, requires: 'lightning_2', xpNeeded: 300 },
                    { id: 'lightning_4', name: 'Blitzraga', tier: 4, power: 110, mana: 55, learned: false, requires: 'lightning_3', xpNeeded: 600 }
                ]
            },
            nature: {
                name: 'Natur-Magie',
                icon: '🌿',
                color: '#22cc44',
                skills: [
                    { id: 'heal_1', name: 'Heilung', tier: 1, power: 15, mana: 12, learned: true, equipped: false, type: 'heal' },
                    { id: 'heal_2', name: 'Heilra', tier: 2, power: 35, mana: 25, learned: false, requires: 'heal_1', xpNeeded: 100 },
                    { id: 'roots', name: 'Wurzeln', tier: 2, power: 0, mana: 20, learned: false, requires: 'heal_1', xpNeeded: 150, effect: 'bind' },
                    { id: 'regen', name: 'Regeneration', tier: 3, power: 5, mana: 40, learned: false, requires: 'heal_2', xpNeeded: 400, type: 'hot' }
                ]
            },
            explosion: {
                name: 'EXPLOSION!!!',
                icon: '💥',
                color: '#ff0066',
                warning: 'KANN NICHT MIT ANDEREN ELEMENTEN KOMBINIERT WERDEN!',
                skills: [
                    { id: 'explosion', name: 'EXPLOSION', tier: 5, power: 999, mana: 100, learned: true, equipped: false,
                      exhaustion: 60, cooldown: 600, description: 'Ein Zauber pro Tag. Vernichtet alles.' }
                ]
            }
        };

        // Equipped Spells (Left/Right Hand - wie Skyrim)
        this.equippedSpells = {
            left: null,
            right: null
        };

        // Skill XP (Learning by Doing)
        this.skillXP = {};

        console.log('📚 Skill Tree UI initialisiert');
    }

    open() {
        if (this.isOpen) return;
        this.isOpen = true;

        this.overlay = document.createElement('div');
        this.overlay.id = 'skill-tree-overlay';
        this.overlay.style.cssText = `
            position: fixed; top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0, 0, 0, 0.95);
            z-index: 10000;
            display: flex;
            font-family: 'Courier New', monospace;
        `;

        this.overlay.innerHTML = this.renderUI();
        document.body.appendChild(this.overlay);

        // Event Listeners
        this.overlay.querySelector('.close-btn').onclick = () => this.close();
        this.overlay.querySelectorAll('.category-btn').forEach(btn => {
            btn.onclick = () => this.selectCategory(btn.dataset.category);
        });
    }

    renderUI() {
        return `
            <div style="width: 100%; display: flex;">
                <!-- Left Sidebar: Categories -->
                <div style="width: 200px; background: #111; padding: 20px; border-right: 2px solid #333;">
                    <h2 style="color: #FFD700; margin: 0 0 20px 0;">📚 MAGIE</h2>

                    ${Object.entries(this.skillTrees).map(([key, tree]) => `
                        <button class="category-btn ${this.selectedCategory === key ? 'active' : ''}"
                                data-category="${key}"
                                style="
                                    width: 100%;
                                    padding: 12px;
                                    margin-bottom: 8px;
                                    background: ${this.selectedCategory === key ? tree.color + '44' : '#222'};
                                    border: 2px solid ${this.selectedCategory === key ? tree.color : '#444'};
                                    border-radius: 8px;
                                    color: white;
                                    cursor: pointer;
                                    text-align: left;
                                    font-size: 14px;
                                ">
                            <span style="font-size: 20px; margin-right: 8px;">${tree.icon}</span>
                            ${tree.name}
                        </button>
                    `).join('')}

                    <hr style="border-color: #333; margin: 20px 0;">

                    <!-- Equipped Spells -->
                    <div style="color: #aaa; font-size: 12px; margin-bottom: 10px;">AUSGERÜSTET:</div>
                    <div style="display: flex; gap: 10px; margin-bottom: 10px;">
                        <div style="flex: 1; background: #222; border: 2px solid #666; border-radius: 8px; padding: 10px; text-align: center;">
                            <div style="font-size: 10px; color: #888;">LINKS [Q]</div>
                            <div style="font-size: 24px; margin: 5px 0;">
                                ${this.equippedSpells.left ? this.getSkillIcon(this.equippedSpells.left) : '—'}
                            </div>
                        </div>
                        <div style="flex: 1; background: #222; border: 2px solid #666; border-radius: 8px; padding: 10px; text-align: center;">
                            <div style="font-size: 10px; color: #888;">RECHTS [R]</div>
                            <div style="font-size: 24px; margin: 5px 0;">
                                ${this.equippedSpells.right ? this.getSkillIcon(this.equippedSpells.right) : '—'}
                            </div>
                        </div>
                    </div>

                    ${this.getWeavingInfo()}
                </div>

                <!-- Main Content: Skill Tree -->
                <div style="flex: 1; padding: 30px; overflow-y: auto;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                        <h1 style="color: ${this.skillTrees[this.selectedCategory].color}; margin: 0;">
                            ${this.skillTrees[this.selectedCategory].icon} ${this.skillTrees[this.selectedCategory].name}
                        </h1>
                        <button class="close-btn" style="
                            background: #ff4444;
                            border: none;
                            color: white;
                            padding: 10px 20px;
                            border-radius: 5px;
                            cursor: pointer;
                            font-size: 16px;
                        ">✕ Schließen [ESC]</button>
                    </div>

                    ${this.skillTrees[this.selectedCategory].warning ? `
                        <div style="background: rgba(255, 0, 100, 0.2); border: 2px solid #ff0066; padding: 15px; border-radius: 10px; margin-bottom: 20px; color: #ff6699;">
                            ⚠️ ${this.skillTrees[this.selectedCategory].warning}
                        </div>
                    ` : ''}

                    <!-- Skill Nodes -->
                    <div style="display: flex; flex-wrap: wrap; gap: 20px; justify-content: center;">
                        ${this.renderSkillNodes()}
                    </div>
                </div>
            </div>
        `;
    }

    renderSkillNodes() {
        const tree = this.skillTrees[this.selectedCategory];
        const color = tree.color;

        return tree.skills.map(skill => {
            const xp = this.skillXP[skill.id] || 0;
            const progress = skill.xpNeeded ? Math.min(100, (xp / skill.xpNeeded) * 100) : 100;
            const canLearn = !skill.requires || this.isSkillLearned(skill.requires);
            const isEquippedLeft = this.equippedSpells.left === skill.id;
            const isEquippedRight = this.equippedSpells.right === skill.id;

            return `
                <div class="skill-node" data-skill="${skill.id}" style="
                    width: 180px;
                    background: ${skill.learned ? color + '33' : '#1a1a1a'};
                    border: 3px solid ${skill.learned ? color : canLearn ? '#555' : '#333'};
                    border-radius: 15px;
                    padding: 15px;
                    text-align: center;
                    opacity: ${canLearn || skill.learned ? 1 : 0.5};
                    cursor: ${skill.learned ? 'pointer' : canLearn ? 'pointer' : 'not-allowed'};
                    transition: all 0.2s;
                ">
                    <!-- Tier Badge -->
                    <div style="
                        position: absolute;
                        top: -10px;
                        right: -10px;
                        background: ${color};
                        color: white;
                        width: 24px;
                        height: 24px;
                        border-radius: 12px;
                        font-size: 12px;
                        line-height: 24px;
                        font-weight: bold;
                    ">T${skill.tier}</div>

                    <div style="font-size: 32px; margin-bottom: 10px;">
                        ${tree.icon}
                    </div>

                    <div style="font-size: 16px; font-weight: bold; color: ${color}; margin-bottom: 5px;">
                        ${skill.name}
                    </div>

                    <div style="font-size: 11px; color: #888; margin-bottom: 10px;">
                        ⚔️ ${skill.power} | 💎 ${skill.mana}
                        ${skill.effect ? `| ✨ ${skill.effect}` : ''}
                    </div>

                    ${skill.learned ? `
                        <!-- Equip Buttons -->
                        <div style="display: flex; gap: 5px; justify-content: center;">
                            <button onclick="window.skillTreeUI.equipSpell('${skill.id}', 'left')"
                                    style="
                                        padding: 5px 10px;
                                        background: ${isEquippedLeft ? '#4CAF50' : '#333'};
                                        border: 1px solid ${isEquippedLeft ? '#4CAF50' : '#666'};
                                        color: white;
                                        border-radius: 5px;
                                        cursor: pointer;
                                        font-size: 11px;
                                    ">
                                ${isEquippedLeft ? '✓ L' : 'L [Q]'}
                            </button>
                            <button onclick="window.skillTreeUI.equipSpell('${skill.id}', 'right')"
                                    style="
                                        padding: 5px 10px;
                                        background: ${isEquippedRight ? '#4CAF50' : '#333'};
                                        border: 1px solid ${isEquippedRight ? '#4CAF50' : '#666'};
                                        color: white;
                                        border-radius: 5px;
                                        cursor: pointer;
                                        font-size: 11px;
                                    ">
                                ${isEquippedRight ? '✓ R' : 'R [R]'}
                            </button>
                        </div>
                    ` : `
                        <!-- Progress Bar -->
                        <div style="background: #222; height: 8px; border-radius: 4px; overflow: hidden; margin-bottom: 5px;">
                            <div style="background: ${color}; height: 100%; width: ${progress}%;"></div>
                        </div>
                        <div style="font-size: 10px; color: #666;">
                            ${xp}/${skill.xpNeeded || 0} XP
                        </div>
                    `}

                    ${skill.description ? `
                        <div style="font-size: 10px; color: #888; margin-top: 8px; font-style: italic;">
                            ${skill.description}
                        </div>
                    ` : ''}
                </div>
            `;
        }).join('');
    }

    getSkillIcon(skillId) {
        for (const tree of Object.values(this.skillTrees)) {
            const skill = tree.skills.find(s => s.id === skillId);
            if (skill) return tree.icon;
        }
        return '?';
    }

    getWeavingInfo() {
        const left = this.equippedSpells.left;
        const right = this.equippedSpells.right;

        if (!left || !right) return '';

        // Check for weaving combinations (NOT with explosion!)
        const leftTree = this.getTreeForSkill(left);
        const rightTree = this.getTreeForSkill(right);

        if (leftTree === 'explosion' || rightTree === 'explosion') {
            return `
                <div style="background: rgba(255, 0, 0, 0.2); border: 1px solid #ff0000; padding: 10px; border-radius: 5px; margin-top: 10px; font-size: 11px; color: #ff6666;">
                    ⚠️ EXPLOSION kann NICHT kombiniert werden!
                </div>
            `;
        }

        const combinations = {
            'fire+ice': { name: 'STEAM', effect: 'Blindheit', icon: '💨', color: '#aaddff' },
            'fire+lightning': { name: 'PLASMA', effect: 'DoT', icon: '🔮', color: '#ff66ff' },
            'ice+lightning': { name: 'SHATTER', effect: 'Stun', icon: '💎', color: '#66ffff' },
            'fire+nature': { name: 'WILDFIRE', effect: 'Spread', icon: '🔥🌿', color: '#ff8800' },
            'ice+nature': { name: 'FROST BLOOM', effect: 'Slow + Heal', icon: '❄️🌸', color: '#88ffaa' },
            'lightning+nature': { name: 'STORM', effect: 'Chain + Root', icon: '⛈️', color: '#88ff00' }
        };

        const key1 = `${leftTree}+${rightTree}`;
        const key2 = `${rightTree}+${leftTree}`;
        const combo = combinations[key1] || combinations[key2];

        if (combo) {
            return `
                <div style="background: ${combo.color}22; border: 2px solid ${combo.color}; padding: 12px; border-radius: 8px; margin-top: 15px;">
                    <div style="font-size: 18px; text-align: center; margin-bottom: 5px;">${combo.icon}</div>
                    <div style="font-size: 14px; color: ${combo.color}; text-align: center; font-weight: bold;">
                        WEAVE: ${combo.name}
                    </div>
                    <div style="font-size: 11px; color: #aaa; text-align: center;">
                        Effekt: ${combo.effect}
                    </div>
                    <div style="font-size: 10px; color: #666; text-align: center; margin-top: 5px;">
                        [Q+R gleichzeitig]
                    </div>
                </div>
            `;
        }

        return '';
    }

    getTreeForSkill(skillId) {
        for (const [key, tree] of Object.entries(this.skillTrees)) {
            if (tree.skills.find(s => s.id === skillId)) return key;
        }
        return null;
    }

    isSkillLearned(skillId) {
        for (const tree of Object.values(this.skillTrees)) {
            const skill = tree.skills.find(s => s.id === skillId);
            if (skill && skill.learned) return true;
        }
        return false;
    }

    equipSpell(skillId, hand) {
        // Check if explosion is already equipped
        const otherHand = hand === 'left' ? 'right' : 'left';
        const newTree = this.getTreeForSkill(skillId);
        const existingTree = this.equippedSpells[otherHand] ? this.getTreeForSkill(this.equippedSpells[otherHand]) : null;

        if (newTree === 'explosion' && existingTree) {
            alert('⚠️ EXPLOSION kann nicht mit anderen Zaubern kombiniert werden!\nEntferne zuerst den anderen Zauber.');
            return;
        }
        if (existingTree === 'explosion' && newTree !== 'explosion') {
            alert('⚠️ EXPLOSION ist ausgerüstet!\nSie kann nicht mit anderen Zaubern kombiniert werden.');
            return;
        }

        // Toggle equip
        if (this.equippedSpells[hand] === skillId) {
            this.equippedSpells[hand] = null;
        } else {
            this.equippedSpells[hand] = skillId;
        }

        // Re-render
        if (this.overlay) {
            this.overlay.innerHTML = this.renderUI();
            this.overlay.querySelector('.close-btn').onclick = () => this.close();
            this.overlay.querySelectorAll('.category-btn').forEach(btn => {
                btn.onclick = () => this.selectCategory(btn.dataset.category);
            });
        }

        // Notify combat system
        if (window.equipmentCombat) {
            window.equipmentCombat.setEquippedSpells(this.equippedSpells);
        }
    }

    selectCategory(category) {
        this.selectedCategory = category;
        if (this.overlay) {
            this.overlay.innerHTML = this.renderUI();
            this.overlay.querySelector('.close-btn').onclick = () => this.close();
            this.overlay.querySelectorAll('.category-btn').forEach(btn => {
                btn.onclick = () => this.selectCategory(btn.dataset.category);
            });
        }
    }

    // Learning by Doing: Add XP when using skill
    addSkillXP(skillId, amount) {
        if (!this.skillXP[skillId]) this.skillXP[skillId] = 0;
        this.skillXP[skillId] += amount;

        // Check if skill can be learned now
        for (const tree of Object.values(this.skillTrees)) {
            const skill = tree.skills.find(s => s.id === skillId);
            if (skill && !skill.learned && skill.xpNeeded) {
                if (this.skillXP[skillId] >= skill.xpNeeded) {
                    skill.learned = true;
                    console.log(`✨ SKILL GELERNT: ${skill.name}!`);
                    if (window.showNotification) {
                        window.showNotification(`✨ ${skill.name} gelernt!`, 3000);
                    }
                }
            }
        }
    }

    close() {
        if (this.overlay) {
            this.overlay.remove();
            this.overlay = null;
        }
        this.isOpen = false;
    }
}

// Global instance
window.skillTreeUI = new SkillTreeUI();

// Keyboard shortcut
document.addEventListener('keydown', (e) => {
    if (e.key === 'k' || e.key === 'K') {
        if (!e.target.matches('input, textarea')) {
            if (window.skillTreeUI.isOpen) {
                window.skillTreeUI.close();
            } else {
                window.skillTreeUI.open();
            }
        }
    }
    if (e.key === 'Escape' && window.skillTreeUI.isOpen) {
        window.skillTreeUI.close();
    }
});

console.log('📚 Skill Tree UI geladen - [K] zum Öffnen');
