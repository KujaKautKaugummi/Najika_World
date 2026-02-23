// =============================================================================
// VÖLLEREI (GLUTTONY/DEVOUR) SYSTEM V2 - SURVIVAL FOCUSED
// =============================================================================
// Integration mit ECHTEN Systemen:
// - survival_system.js (Hunger/Mood/Traits)
// - food_system.js (Buffs)
// - building.py (HUNT als Basis)
//
// DESIGN-PHILOSOPHIE (User-Feedback):
// ✅ Survival-Fokus: Hauptsächlich Nahrungsquelle, keine Power-Ups
// ✅ Fair & Balanced: Kein "one correct path"
// ✅ Fallout-Style: Erst tote Körper, dann mit Level Progression 1 HP Finisher
// ✅ Snacks: Teile mitnehmen für später
// ✅ Graue Moral: Gesellschaft urteilt (Moodlets), nicht der Charakter
// ✅ Kannibalismus: Eigene Spezies essen = soziale Konsequenzen
// =============================================================================

(function() {
    'use strict';

    // ===== CONFIG =====
    const VOELLEREI_CONFIG = {
        // Progression: Level bestimmt was man fressen kann
        progressionThresholds: {
            deadOnly: { maxLevel: 25, hpThreshold: 0, description: 'Nur tote Körper' },
            finisher1HP: { minLevel: 26, maxLevel: 50, hpThreshold: 1, description: 'Finisher bei 1 HP' },
            finisher5HP: { minLevel: 51, hpThreshold: 5, description: 'Finisher bei 5 HP' }
        },

        cooldownMs: 5000,
        devourKey: 'KeyV',
        animDuration: 1200,

        // Learning by Doing XP
        baseXP: 15,
        tierXPMultiplier: [1, 1.5, 2, 3, 5], // Common, Uncommon, Rare, Elite, Boss

        // Snack-System
        meatDropChance: 0.6, // 60% Chance auf Fleisch-Drop

        // Kannibalismus-Detektion
        cannibalismSpecies: ['human', 'slime', 'elf', 'dwarf', 'orc'] // Intelligente Spezies
    };

    // ===== STATE =====
    const voellereiState = {
        lastDevourTime: 0,
        totalDevoured: 0,
        cannibalismCount: 0,
        isDevourActive: false,
        currentTarget: null,
        witnesses: []
    };

    // ===== FLEISCH-TYPEN (Integration mit food_system.js) =====
    // Minimale Buffs, Fokus auf Hunger-Sättigung
    const MEAT_TYPES = {
        default: {
            name: 'Rohes Fleisch',
            icon: '🍖',
            hungerRestore: 25,
            effects: { hp_instant: 10 }, // Minimal!
            duration: 120, // 2 Minuten
            rarity: 'common',
            description: 'Einfaches Fleisch von einem Tier'
        },
        beast: {
            name: 'Wildfleisch',
            icon: '🥩',
            hungerRestore: 30,
            effects: { hp_instant: 15, stamina_regen: 2 },
            duration: 180,
            rarity: 'common',
            description: 'Fleisch von wilden Tieren'
        },
        fire_creature: {
            name: 'Magma-Fleisch',
            icon: '🔥',
            hungerRestore: 20,
            effects: { hp_instant: 12, warmth: 5 }, // Wärme-Resist (survival_system)
            duration: 240,
            rarity: 'uncommon',
            description: 'Heißes Fleisch von Feuerkreaturen - warm!'
        },
        ice_creature: {
            name: 'Frost-Fleisch',
            icon: '❄️',
            hungerRestore: 20,
            effects: { hp_instant: 12, cold_resistance: 5 },
            duration: 240,
            rarity: 'uncommon',
            description: 'Kühles Fleisch - erfrischt in heißen Biomen'
        },
        undead: {
            name: 'Verdorbenes Fleisch',
            icon: '☠️',
            hungerRestore: 10, // Weniger!
            effects: { hp_instant: 5 },
            duration: 60,
            rarity: 'poor',
            description: 'Kaum genießbar... aber Nahrung ist Nahrung',
            disease_risk: 0.15 // 15% Krankheitsrisiko (survival_system)
        },
        boss: {
            name: 'Erlesenes Fleisch',
            icon: '🍗',
            hungerRestore: 50,
            effects: { hp_instant: 30, strength: 3, hp_regen: 5 }, // Etwas mehr bei Boss
            duration: 600, // 10 Minuten
            rarity: 'rare',
            description: 'Hochwertiges Fleisch von einem mächtigen Gegner'
        },
        // KANNIBALISMUS (selbe Spezies)
        cannibalism: {
            name: 'Menschenfleisch', // Wird dynamisch angepasst
            icon: '😱',
            hungerRestore: 30,
            effects: { hp_instant: 20 },
            duration: 180,
            rarity: 'forbidden',
            description: 'Das... das fühlt sich falsch an.',
            isCannibalism: true
        }
    };

    // ===== CORE FUNCTIONS =====

    function getVoellereiLevel() {
        if (window.EquipmentCombat?.getSkills) {
            const skills = window.EquipmentCombat.getSkills();
            return skills.voellerei?.level || 1;
        }
        return 1;
    }

    function getProgressionRule(level) {
        const rules = VOELLEREI_CONFIG.progressionThresholds;
        if (level <= rules.deadOnly.maxLevel) return rules.deadOnly;
        if (level <= rules.finisher5HP.minLevel - 1) return rules.finisher1HP;
        return rules.finisher5HP;
    }

    function canDevour(enemy) {
        if (!enemy || voellereiState.isDevourActive) return false;

        // Cooldown
        if (Date.now() - voellereiState.lastDevourTime < VOELLEREI_CONFIG.cooldownMs) return false;

        // Progression: Was kann ich auf meinem Level fressen?
        const level = getVoellereiLevel();
        const rule = getProgressionRule(level);

        if (enemy.hp > rule.hpThreshold) return false;

        return true;
    }

    function determineSpecies(enemy) {
        const data = enemy.data || enemy;
        const name = (data.name || '').toLowerCase();
        const id = (data.id || '').toLowerCase();
        const type = (data.type || '').toLowerCase();

        // Check für intelligente Spezies
        for (const species of VOELLEREI_CONFIG.cannibalismSpecies) {
            if (name.includes(species) || id.includes(species) || type.includes(species)) {
                return species;
            }
        }

        return null; // Tier/Monster
    }

    function getPlayerSpecies() {
        // TODO: Aus Player-State holen wenn implementiert
        // Für jetzt: slime (da Najika ein Slime-Companion hat)
        if (window.player?.species) return window.player.species;
        return 'slime';
    }

    function isCannibalism(enemy) {
        const playerSpecies = getPlayerSpecies();
        const enemySpecies = determineSpecies(enemy);

        return enemySpecies && playerSpecies === enemySpecies;
    }

    function determineMeatType(enemy) {
        const data = enemy.data || enemy;
        const name = (data.name || '').toLowerCase();
        const tier = data.tier || 1;

        // Kannibalismus?
        if (isCannibalism(enemy)) {
            return 'cannibalism';
        }

        // Boss?
        if (tier >= 4) return 'boss';

        // Element-basiert
        if (name.includes('feuer') || name.includes('magma') || name.includes('vulkan')) return 'fire_creature';
        if (name.includes('eis') || name.includes('frost') || name.includes('schnee')) return 'ice_creature';
        if (name.includes('skelett') || name.includes('zombie') || name.includes('untot')) return 'undead';
        if (name.includes('wolf') || name.includes('bär') || name.includes('büffel')) return 'beast';

        return 'default';
    }

    function getMeatItem(meatType, enemy) {
        const template = MEAT_TYPES[meatType] || MEAT_TYPES.default;
        const level = getVoellereiLevel();
        const bonus = 1 + (level - 1) * 0.02; // +2% pro Level (MINIMAL!)

        // Kannibalismus: Name anpassen
        let name = template.name;
        if (meatType === 'cannibalism') {
            const species = determineSpecies(enemy);
            name = `${species.charAt(0).toUpperCase() + species.slice(1)}-Fleisch`;
        }

        return {
            ...template,
            name,
            hungerRestore: Math.floor(template.hungerRestore * bonus),
            quality: bonus
        };
    }

    // ===== DEVOUR EXECUTION =====

    function devourEnemy(enemy) {
        if (!canDevour(enemy)) return false;

        voellereiState.isDevourActive = true;
        voellereiState.currentTarget = enemy;

        showDevourAnimation(enemy);

        setTimeout(() => {
            executeDevour(enemy);
        }, VOELLEREI_CONFIG.animDuration);

        return true;
    }

    function executeDevour(enemy) {
        const level = getVoellereiLevel();
        const meatType = determineMeatType(enemy);
        const meatItem = getMeatItem(meatType, enemy);
        const isCannib = meatType === 'cannibalism';

        // 1. Gegner töten (falls noch nicht tot)
        if (enemy.hp > 0) {
            if (typeof enemy.die === 'function') {
                enemy.die();
            } else {
                enemy.hp = 0;
                enemy.isDead = true;
            }
        }

        // 2. ESSEN via survival_system.js eat() - ECHTE INTEGRATION!
        if (window.SurvivalSystem?.eat) {
            window.SurvivalSystem.eat(meatItem);
        } else {
            console.warn('⚠️ survival_system.js nicht gefunden - Fallback');
            // Fallback: Manuell Hunger wiederherstellen
            if (window.player) {
                window.player.hunger = Math.min(100, (window.player.hunger || 50) + meatItem.hungerRestore);
            }
        }

        // 3. Kannibalismus-Konsequenzen (GRAUE MORAL!)
        if (isCannib) {
            handleCannibalismConsequences(enemy);
        }

        // 4. Snack-System: Chance auf extra Fleisch als Item
        if (Math.random() < VOELLEREI_CONFIG.meatDropChance) {
            addMeatToInventory(meatItem, enemy);
        }

        // 5. Learning by Doing XP
        const tier = (enemy.data?.tier || enemy.tier || 1) - 1;
        const xpMultiplier = VOELLEREI_CONFIG.tierXPMultiplier[tier] || 1;
        const xpAmount = Math.floor(VOELLEREI_CONFIG.baseXP * xpMultiplier);
        gainVoellereiXP(xpAmount);

        // 6. State Update
        voellereiState.lastDevourTime = Date.now();
        voellereiState.totalDevoured++;
        if (isCannib) voellereiState.cannibalismCount++;
        voellereiState.isDevourActive = false;
        voellereiState.currentTarget = null;

        // 7. Notification
        showDevourNotification(enemy, meatItem, xpAmount, isCannib);

        // 8. GameEvents
        if (window.GameEvents) {
            window.GameEvents.emit('enemyDevoured', {
                enemyId: enemy.data?.id || enemy.type || 'unknown',
                enemyName: enemy.data?.name || enemy.name || 'Gegner',
                meatType,
                isCannibalism: isCannib,
                hungerRestored: meatItem.hungerRestore,
                xpGained: xpAmount,
                voellereiLevel: level
            });
        }

        console.log(`🍖 VÖLLEREI: ${enemy.data?.name || 'Gegner'} gefressen! Typ: ${meatType}, +${meatItem.hungerRestore} Hunger, +${xpAmount} XP${isCannib ? ' [KANNIBALISMUS!]' : ''}`);

        saveState();
        return true;
    }

    // ===== KANNIBALISMUS-KONSEQUENZEN (GRAUE MORAL) =====
    function handleCannibalismConsequences(enemy) {
        voellereiState.cannibalismCount++;

        // WICHTIG: Keine automatischen Gewissensbisse!
        // "Die GESELLSCHAFT urteilt, nicht der Charakter selbst"

        // 1. Moodlet NUR wenn Zeugen da sind (soziale Scham, nicht moralisch!)
        const witnessCount = getWitnessCount();
        if (witnessCount > 0) {
            if (window.SurvivalSystem?.addMoodlet) {
                // Nur soziale Reaktion, keine Moral!
                window.SurvivalSystem.addMoodlet(
                    'cannibalism_witnessed',
                    '😨 Du wurdest beim Kannibalismus gesehen!',
                    -15, // Mood-Penalty durch soziale Ächtung
                    1800000 // 30 Minuten
                );
            }

            // 2. Reputation-Verlust in der Region
            const currentRegion = getCurrentRegion();
            if (window.FactionSystem?.modifyReputation) {
                // Nur in zivilisierten Regionen (nicht in Wildnis!)
                if (currentRegion && currentRegion !== 'wildnis') {
                    window.FactionSystem.modifyReputation(currentRegion, -10);
                    console.log(`⚖️ Reputation in ${currentRegion}: -10 (Kannibalismus gesehen)`);
                }
            }

            // 3. Chance auf Kopfgeld (nur in strengen Regionen)
            if (currentRegion === 'goetterfels' || currentRegion === 'reich_der_drei') {
                if (Math.random() < 0.3) { // 30% Chance
                    if (window.SurvivalSystem?.addBounty) {
                        window.SurvivalSystem.addBounty(currentRegion, 50); // 50 Gold Kopfgeld
                        console.log('⚖️ Kopfgeld: +50 Gold (Kannibalismus in zivilisierter Region)');
                    }
                }
            }
        } else {
            // Keine Zeugen = keine Konsequenzen (graue Moral!)
            console.log('👁️ Kein Zeuge... niemand wird es erfahren.');
        }

        // 4. Achievement (statistisch, keine Wertung!)
        if (voellereiState.cannibalismCount === 1) {
            console.log('📊 Erstes Mal Kannibalismus (Statistik)');
        }
    }

    function getWitnessCount() {
        // TODO: Echte NPC-Detektion wenn implementiert
        // Für jetzt: Random basierend auf Biome
        const biome = getCurrentBiome();
        const civilizedBiomes = ['goetterfels', 'reich_der_drei', 'salzwind'];

        if (civilizedBiomes.includes(biome)) {
            return Math.random() < 0.5 ? Math.floor(Math.random() * 3) + 1 : 0;
        }

        return 0; // Wildnis = keine Zeugen
    }

    function getCurrentRegion() {
        // TODO: Aus World-State holen
        if (window.player?.region) return window.player.region;
        return 'wildnis';
    }

    function getCurrentBiome() {
        // TODO: Aus World-State holen
        if (window.player?.biome) return window.player.biome;
        return 'samtmoos';
    }

    // ===== SNACK-SYSTEM =====
    function addMeatToInventory(meatItem, enemy) {
        // Integration mit InventorySystem
        if (window.InventorySystem?.addItem) {
            const item = {
                id: `meat_${Date.now()}`,
                name: meatItem.name,
                icon: meatItem.icon,
                type: 'food',
                rarity: meatItem.rarity,
                description: meatItem.description,
                effect: () => {
                    if (window.SurvivalSystem?.eat) {
                        window.SurvivalSystem.eat(meatItem);
                    }
                },
                stackable: true,
                maxStack: 20
            };

            window.InventorySystem.addItem(item);
            console.log(`📦 +1 ${meatItem.name} zum Inventar hinzugefügt`);

            if (typeof notify === 'function') {
                notify(`📦 Snack gesammelt: ${meatItem.name}`, 'success');
            }
        } else {
            // Fallback: LocalStorage
            try {
                const inventory = JSON.parse(localStorage.getItem('najika_inventory') || '[]');
                inventory.push({
                    name: meatItem.name,
                    icon: meatItem.icon,
                    hungerRestore: meatItem.hungerRestore,
                    timestamp: Date.now()
                });
                localStorage.setItem('najika_inventory', JSON.stringify(inventory));
                console.log(`📦 Fallback: ${meatItem.name} in localStorage gespeichert`);
            } catch (e) {
                console.warn('Snack-Speicherung fehlgeschlagen:', e);
            }
        }
    }

    // ===== SKILL XP =====
    function gainVoellereiXP(amount) {
        if (window.EquipmentCombat?._gainSkillXP) {
            window.EquipmentCombat._gainSkillXP('voellerei', amount);
        } else {
            // Fallback
            try {
                const saved = localStorage.getItem('najika_combat_skills');
                if (saved) {
                    const skills = JSON.parse(saved);
                    if (!skills.voellerei) {
                        skills.voellerei = { level: 1, xp: 0, xpNeeded: 150 };
                    }
                    skills.voellerei.xp += amount;

                    while (skills.voellerei.xp >= skills.voellerei.xpNeeded) {
                        skills.voellerei.xp -= skills.voellerei.xpNeeded;
                        skills.voellerei.level++;
                        skills.voellerei.xpNeeded = Math.floor(skills.voellerei.xpNeeded * 1.5);

                        const rule = getProgressionRule(skills.voellerei.level);
                        console.log(`🎉 VÖLLEREI LEVEL UP! → Level ${skills.voellerei.level} (${rule.description})`);

                        if (typeof notify === 'function') {
                            notify(`🍖 Völlerei Level ${skills.voellerei.level}! ${rule.description}`, 'success');
                        }
                    }

                    localStorage.setItem('najika_combat_skills', JSON.stringify(skills));
                }
            } catch (e) {
                console.warn('Völlerei XP save error:', e);
            }
        }
    }

    // ===== UI: DEVOUR PROMPT =====
    function showDevourPrompt(enemy) {
        if (document.getElementById('devour-prompt')) return;

        const level = getVoellereiLevel();
        const rule = getProgressionRule(level);
        const isCannib = isCannibalism(enemy);

        const prompt = document.createElement('div');
        prompt.id = 'devour-prompt';
        prompt.style.cssText = `
            position: fixed; top: 48%; left: 50%; transform: translateX(-50%);
            background: ${isCannib ? 'rgba(100, 0, 0, 0.95)' : 'rgba(80, 40, 0, 0.92)'};
            color: ${isCannib ? '#ff6666' : '#ff8844'};
            padding: 12px 24px; border-radius: 10px; font-size: 17px; font-weight: bold;
            font-family: monospace; z-index: 9999;
            border: 2px solid ${isCannib ? '#ff0000' : '#ff6600'};
            text-shadow: 0 0 8px ${isCannib ? '#ff0000' : '#ff4400'};
            box-shadow: 0 0 20px ${isCannib ? 'rgba(255, 0, 0, 0.6)' : 'rgba(255, 100, 0, 0.5)'};
            animation: devourPulse 0.6s infinite alternate;
        `;

        const text = isCannib
            ? `😱 Drücke <span style="color:#ffcc00;font-size:20px">V</span> zum FRESSEN... (Kannibalismus!)`
            : `🍖 Drücke <span style="color:#ffcc00;font-size:20px">V</span> zum FRESSEN!`;

        prompt.innerHTML = text;
        document.body.appendChild(prompt);

        // Style injection
        if (!document.getElementById('devour-pulse-style')) {
            const style = document.createElement('style');
            style.id = 'devour-pulse-style';
            style.textContent = `
                @keyframes devourPulse {
                    from { transform: translateX(-50%) scale(1); opacity: 0.9; }
                    to { transform: translateX(-50%) scale(1.08); opacity: 1; }
                }
                @keyframes devourChomp {
                    0%, 100% { transform: scale(1) rotate(0deg); }
                    25% { transform: scale(1.3) rotate(-5deg); }
                    50% { transform: scale(0.8) rotate(5deg); }
                    75% { transform: scale(1.2) rotate(-3deg); }
                }
            `;
            document.body.appendChild(style);
        }

        setTimeout(() => hideDevourPrompt(), 5000);
    }

    function hideDevourPrompt() {
        const prompt = document.getElementById('devour-prompt');
        if (prompt) prompt.remove();
    }

    // ===== UI: ANIMATION =====
    function showDevourAnimation(enemy) {
        const overlay = document.createElement('div');
        overlay.id = 'devour-animation';
        overlay.style.cssText = `
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: radial-gradient(circle, rgba(100,30,0,0.3) 0%, rgba(0,0,0,0.6) 100%);
            z-index: 10000; display: flex; align-items: center; justify-content: center;
            pointer-events: none;
        `;

        const enemyName = enemy.data?.name || enemy.name || 'Gegner';
        const level = getVoellereiLevel();
        const isCannib = isCannibalism(enemy);

        overlay.innerHTML = `
            <div style="text-align:center; animation: devourChomp ${VOELLEREI_CONFIG.animDuration}ms ease-in-out;">
                <div style="font-size: 80px;">
                    ${isCannib ? '😈' : (level >= 10 ? '😋' : '😤')}
                </div>
                <div style="font-size: 24px; color: ${isCannib ? '#ff6666' : '#ff8844'};
                     font-weight: bold; font-family: monospace;
                     text-shadow: 0 0 10px ${isCannib ? '#ff0000' : '#ff4400'}; margin-top: 10px;">
                    *FRISST ${enemyName.toUpperCase()}*
                </div>
                <div style="font-size: 16px; color: #ffaa66; font-family: monospace; margin-top: 5px;">
                    ${getDevourFlavorText(level, isCannib)}
                </div>
            </div>
        `;

        document.body.appendChild(overlay);

        setTimeout(() => {
            overlay.style.transition = 'opacity 0.3s';
            overlay.style.opacity = '0';
            setTimeout(() => overlay.remove(), 300);
        }, VOELLEREI_CONFIG.animDuration - 300);
    }

    function getDevourFlavorText(level, isCannibalism) {
        if (isCannibalism) {
            return [
                'Das... fühlt sich falsch an.',
                'Was tue ich hier...?',
                'Survival of the fittest...'
            ][Math.floor(Math.random() * 3)];
        }

        const texts = [
            'NOM NOM NOM...',
            '*MAMPF* *SCHLUCK*',
            'Hunger gestillt!',
            'Nahrung ist Nahrung.',
            'Survival-Mode: Aktiviert'
        ];

        if (level >= 10) {
            texts.push('Erfahrener Jäger!');
            texts.push('Effizient und schnell!');
        }

        return texts[Math.floor(Math.random() * texts.length)];
    }

    // ===== UI: NOTIFICATION =====
    function showDevourNotification(enemy, meatItem, xp, isCannibalism) {
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed; bottom: 120px; left: 50%; transform: translateX(-50%);
            background: ${isCannibalism ? 'rgba(80, 0, 0, 0.95)' : 'rgba(60, 20, 0, 0.95)'};
            color: #ffaa44; padding: 15px 25px; border-radius: 12px;
            font-family: monospace; z-index: 9999;
            border: 2px solid ${isCannibalism ? '#ff0000' : '#ff6600'};
            min-width: 300px; text-align: center;
            box-shadow: 0 0 25px ${isCannibalism ? 'rgba(255, 0, 0, 0.5)' : 'rgba(255, 100, 0, 0.4)'};
        `;

        const enemyName = enemy.data?.name || enemy.name || 'Gegner';
        const cannibalismWarning = isCannibalism ? '<br><span style="color:#ff4444;">⚠️ KANNIBALISMUS</span>' : '';

        notification.innerHTML = `
            <div style="font-size: 18px; font-weight: bold; color: #ff8844; margin-bottom: 8px;">
                🍖 ${enemyName} GEFRESSEN!${cannibalismWarning}
            </div>
            <div style="font-size: 13px; color: #ffcc88; line-height: 1.6;">
                ${meatItem.icon} +${meatItem.hungerRestore} Hunger<br>
                ${Object.keys(meatItem.effects).length > 0 ?
                    Object.entries(meatItem.effects).map(([k, v]) => `+${v} ${k.replace(/_/g, ' ')}`).join(' | ') + '<br>'
                    : ''}
                <span style="color: #88ff88;">+${xp} Völlerei-XP</span>
            </div>
        `;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.style.transition = 'opacity 0.5s, transform 0.5s';
            notification.style.opacity = '0';
            notification.style.transform = 'translateX(-50%) translateY(20px)';
            setTimeout(() => notification.remove(), 500);
        }, 4000);
    }

    // ===== COMBAT INTEGRATION =====
    function hookIntoCombat() {
        setInterval(() => {
            if (voellereiState.isDevourActive) return;

            let enemies = null;
            if (window.Real3DCombat?.getEnemies) {
                enemies = window.Real3DCombat.getEnemies();
            }

            if (enemies) {
                const devourableEnemies = enemies.filter(e => canDevour(e));
                if (devourableEnemies.length > 0) {
                    const target = devourableEnemies.sort((a, b) => a.hp - b.hp)[0];
                    voellereiState.currentTarget = target;
                    showDevourPrompt(target);
                } else {
                    if (document.getElementById('devour-prompt')) {
                        hideDevourPrompt();
                        voellereiState.currentTarget = null;
                    }
                }
            }
        }, 200);
    }

    // ===== INPUT =====
    function setupInput() {
        document.addEventListener('keydown', (e) => {
            if (e.code === VOELLEREI_CONFIG.devourKey && voellereiState.currentTarget) {
                e.preventDefault();
                hideDevourPrompt();
                devourEnemy(voellereiState.currentTarget);
            }
        });
    }

    // ===== SAVE/LOAD =====
    function saveState() {
        const data = {
            totalDevoured: voellereiState.totalDevoured,
            cannibalismCount: voellereiState.cannibalismCount,
            lastSave: Date.now()
        };
        localStorage.setItem('najika_voellerei_v2', JSON.stringify(data));
    }

    function loadState() {
        try {
            const saved = localStorage.getItem('najika_voellerei_v2');
            if (saved) {
                const data = JSON.parse(saved);
                voellereiState.totalDevoured = data.totalDevoured || 0;
                voellereiState.cannibalismCount = data.cannibalismCount || 0;
            }
        } catch (e) {
            console.warn('Völlerei load error:', e);
        }
    }

    // ===== INIT =====
    function init() {
        loadState();
        hookIntoCombat();
        setupInput();

        const level = getVoellereiLevel();
        const rule = getProgressionRule(level);
        console.log(`🍖 Völlerei-System V2 initialisiert! Level ${level} (${rule.description})`);
        console.log(`📊 Stats: ${voellereiState.totalDevoured} gefressen, ${voellereiState.cannibalismCount} Kannibalismus`);
    }

    // ===== PUBLIC API =====
    window.VoellereiSystem = {
        init,
        canDevour,
        devourEnemy,
        getLevel: getVoellereiLevel,
        getProgressionRule: () => getProgressionRule(getVoellereiLevel()),
        getState: () => ({ ...voellereiState }),
        getMeatTypes: () => ({ ...MEAT_TYPES }),
        isCannibalism,
        saveState
    };

    // Auto-init
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
