/**
 * UNIFIED COMBAT SYSTEM - Najika World
 * =====================================
 *
 * Ein einheitliches Kampfsystem für:
 * - Overworld Encounters
 * - Dungeon Combat
 * - Arena (Nemesis + Slime)
 * - Boss Fights
 *
 * 3 COMBAT MODI (jederzeit wechselbar):
 * 1. AUTO (KI) - KI steuert deinen Charakter
 * 2. MANUAL - Du wählst jede Aktion selbst
 * 3. CHEER - Feuere an für Buffs, KI kämpft
 *
 * MAGIE-SYSTEM (9 Schulen + Explosion):
 * - Feuer, Wasser, Eis, Blitz, Erde, Wind, Natur, Licht, Dunkel
 * - Explosion: Eigene Schule (NIEMALS mit anderen kombinieren!)
 * - Learning by Doing (Skyrim-Style)
 * - Element-Verweben (ESO-Style) - NICHT mit Explosion!
 *
 * FINISHER-SYSTEM:
 * - Alle Spieler können Finisher nutzen
 * - Najika's Explosion-Finisher (1x/Tag): Kann Overworld beschädigen!
 * - Happy Tree Friends Style Brutalität + Niedlichkeit
 */

const UnifiedCombat = (function() {
    'use strict';

    // ==========================================
    // S.P.E.C.I.A.L. STATS (Fallout-Style)
    // ==========================================

    const SPECIAL = {
        POW: 5,  // Power - Nahkampf +2% pro Punkt
        INT: 5,  // Intellect - Spell +3%, +10 Mana pro Punkt
        AGI: 5,  // Agility - Dodge +1%, Speed +1%
        VIT: 5,  // Vitality - +15 HP pro Punkt
        WIL: 5,  // Willpower - Mana Regen +1%
        LUK: 5,  // Luck - Crit +1%, Crit DMG +5%
        PER: 5   // Perception - Hit Chance +2%
    };

    // ==========================================
    // MAGIE-SCHULEN (9 + Explosion)
    // ==========================================

    const MAGIC_SCHOOLS = {
        feuer: { name: 'Feuer', type: 'destruction', color: '#ff4400', icon: '🔥' },
        wasser: { name: 'Wasser', type: 'alteration', color: '#0066ff', icon: '💧' },
        eis: { name: 'Eis', type: 'destruction', color: '#88ddff', icon: '❄️' },
        blitz: { name: 'Blitz', type: 'destruction', color: '#ffff00', icon: '⚡' },
        erde: { name: 'Erde', type: 'alteration', color: '#8b4513', icon: '🪨' },
        wind: { name: 'Wind', type: 'alteration', color: '#aaffaa', icon: '🌪️' },
        natur: { name: 'Natur', type: 'conjuration', color: '#00aa00', icon: '🌿' },
        licht: { name: 'Licht', type: 'restoration', color: '#ffffaa', icon: '✨' },
        dunkel: { name: 'Dunkel', type: 'illusion', color: '#330066', icon: '🌑' },
        explosion: { name: 'Explosion', type: 'SPECIAL', color: '#ff0000', icon: '💥', noWeave: true }
    };

    // ==========================================
    // ZAUBER-DATENBANK
    // ==========================================

    const SPELLS = {
        // FEUER
        flammen: { school: 'feuer', tier: 1, mana: 15, damage: 25, cast: 0.5, name: 'Flammen' },
        feuerball: { school: 'feuer', tier: 2, mana: 30, damage: 50, cast: 1.0, name: 'Feuerball' },
        feuerwand: { school: 'feuer', tier: 3, mana: 50, damage: 40, cast: 1.5, name: 'Feuerwand', aoe: true },

        // WASSER
        heilung: { school: 'wasser', tier: 1, mana: 20, heal: 30, cast: 1.0, name: 'Heilung' },
        wasserschild: { school: 'wasser', tier: 2, mana: 35, defense: 20, duration: 10, name: 'Wasserschild' },

        // EIS
        eiszapfen: { school: 'eis', tier: 1, mana: 18, damage: 28, cast: 0.6, name: 'Eiszapfen', slow: 0.2 },
        einfrieren: { school: 'eis', tier: 2, mana: 40, damage: 35, stun: 2, name: 'Einfrieren' },

        // BLITZ
        blitzschlag: { school: 'blitz', tier: 1, mana: 20, damage: 35, cast: 0.3, name: 'Blitzschlag' },
        kettenblitz: { school: 'blitz', tier: 2, mana: 45, damage: 30, chain: 3, name: 'Kettenblitz' },

        // ERDE
        steinpanzer: { school: 'erde', tier: 1, mana: 25, defense: 30, duration: 15, name: 'Steinpanzer' },
        erdbeben: { school: 'erde', tier: 2, mana: 50, damage: 45, knockdown: true, aoe: true, name: 'Erdbeben' },

        // WIND
        eile: { school: 'wind', tier: 1, mana: 15, speedBuff: 0.3, duration: 10, name: 'Eile' },
        windklinge: { school: 'wind', tier: 2, mana: 25, damage: 40, cast: 0.4, name: 'Windklinge' },

        // NATUR
        verstricken: { school: 'natur', tier: 1, mana: 22, root: 3, name: 'Verstricken' },
        wolf_beschwören: { school: 'natur', tier: 2, mana: 60, summon: 'wolf', duration: 30, name: 'Wolf beschwören' },

        // LICHT
        segen: { school: 'licht', tier: 1, mana: 18, heal: 20, buff: 'blessed', name: 'Segen' },
        heiliges_licht: { school: 'licht', tier: 2, mana: 40, damage: 50, vsUndead: 2.0, name: 'Heiliges Licht' },

        // DUNKEL
        leben_entziehen: { school: 'dunkel', tier: 1, mana: 25, damage: 30, lifesteal: 0.5, name: 'Leben entziehen' },
        fluch: { school: 'dunkel', tier: 2, mana: 35, debuff: 'cursed', duration: 15, name: 'Fluch' },

        // EXPLOSION (Megumin's Spezialität!)
        kleine_explosion: {
            school: 'explosion', tier: 1, mana: 80, stamina: 50, damage: 200,
            cast: 2.0, exhaustion: 30, name: 'Kleine Explosion', icon: '💥'
        },
        exploooosion: {
            school: 'explosion', tier: 2, mana: 110, stamina: 70, damage: 300,
            cast: 3.0, exhaustion: 45, name: 'EXPLOOOOSION!!!', icon: '💥💥'
        },
        omega_detonation: {
            school: 'explosion', tier: 3, mana: 140, stamina: 90, damage: 400,
            cast: 5.0, exhaustion: 60, name: 'OMEGA-DETONATION!!!', icon: '💥💥💥',
            najikaOnly: true  // NUR Najika kann diesen Zauber!
        }
    };

    // ==========================================
    // ELEMENT VERWEBEN (ESO-Style)
    // WICHTIG: Explosion kann NICHT verwoben werden!
    // ==========================================

    const ELEMENT_WEAVES = {
        'feuer+wasser': { name: 'Dampf', effect: 'blind', bonusDmg: 1.3 },
        'feuer+wind': { name: 'Feuersturm', effect: 'aoe', bonusDmg: 1.4 },
        'feuer+erde': { name: 'Magma', effect: 'dot+slow', bonusDmg: 1.35 },
        'wasser+wind': { name: 'Blizzard', effect: 'freeze', bonusDmg: 1.3 },
        'wasser+erde': { name: 'Schlamm', effect: 'root+slow', bonusDmg: 1.25 },
        'blitz+wasser': { name: 'Schock', effect: 'chain', bonusDmg: 1.5 },
        'blitz+wind': { name: 'Gewitter', effect: 'random_strikes', bonusDmg: 1.4 },
        'erde+wind': { name: 'Sandsturm', effect: 'blind+dot', bonusDmg: 1.3 },
        'eis+feuer': { name: 'Thermal', effect: 'armor_pierce', bonusDmg: 1.35 },
        'dunkel+licht': { name: 'Leere', effect: 'true_damage', bonusDmg: 1.5 }
    };

    // ==========================================
    // FINISHER SYSTEM
    // ==========================================

    const FINISHER_CONFIG = {
        meterMax: 100,
        meterGain: {
            perfectDodge: 30,
            combo5: 25,
            parryRiposte: 20,
            chargedAttack: 15,
            normalAttack: 5
        },
        cooldown: 24 * 60 * 60 * 1000,  // 24 Stunden in ms

        // Najika's spezielle Explosion-Finisher Effekte
        najikaExplosionFinisher: {
            tier1Multiplier: 3,   // 3x Schaden
            tier2Multiplier: 5,   // 5x Schaden
            tier3Multiplier: 10,  // 10x Schaden (OMEGA!)
            overworldDamage: true, // Kann Overworld beschädigen!
            exhaustionTime: 60000  // 60 Sekunden Movement Lock
        }
    };

    // ==========================================
    // COMBAT STATE
    // ==========================================

    const state = {
        active: false,
        mode: 'manual',  // 'auto', 'manual', 'cheer'

        // Spieler Stats
        player: {
            hp: 100,
            maxHp: 100,
            mana: 100,
            maxMana: 100,
            stamina: 100,
            maxStamina: 100,
            manaRegen: 3,
            staminaRegen: 5,

            // S.P.E.C.I.A.L.
            special: { ...SPECIAL },

            // Basis-Werte (berechnet aus SPECIAL)
            attackPower: 20,
            spellPower: 25,
            defense: 10,
            speed: 1.0,
            critChance: 0.05,
            critMultiplier: 1.5,

            // Magie-Fortschritt (Learning by Doing)
            schoolMastery: {
                feuer: 1, wasser: 1, eis: 1, blitz: 1, erde: 1,
                wind: 1, natur: 1, licht: 1, dunkel: 1, explosion: 1
            },
            schoolXP: {
                feuer: 0, wasser: 0, eis: 0, blitz: 0, erde: 0,
                wind: 0, natur: 0, licht: 0, dunkel: 0, explosion: 0
            },
            knownSpells: ['flammen', 'heilung', 'kleine_explosion'],

            // Finisher
            finisherMeter: 0,
            lastFinisherTime: 0,
            isNajika: true,  // Für Najika's exklusive Skills

            // Aktive Buffs/Debuffs
            buffs: {},
            debuffs: {},

            // Cooldowns (ms)
            cooldowns: {
                lightAttack: 0,
                heavyAttack: 0,
                dodge: 0,
                parry: 0
            },
            spellCooldowns: {},

            // Combo
            comboCount: 0,
            comboTimer: null,

            // Exhaustion (nach Explosion)
            isExhausted: false,
            exhaustionEndTime: 0
        },

        // Gegner
        enemy: null,
        enemies: [],

        // Kampf-Kontext
        context: {
            type: null,
            location: null,
            waveNumber: 0,
            isHardcore: false
        },

        // Cheer Buffs
        cheerBuffs: {
            attack: 0,
            defend: 0,
            combo: 0,
            focus: 0
        },

        // Battle Log
        log: [],
        uiContainer: null,

        // ==========================================
        // WEAPON INFUSE SYSTEM
        // Zauber auf Waffe = temporaerer Buff (NICHT Combo!)
        // ==========================================
        infuse: {
            leftHand: {
                type: null,  // 'weapon' oder 'spell'
                item: null   // weapon_id oder spell_id
            },
            rightHand: {
                type: null,
                item: null
            },
            activeInfuses: {}  // weapon_id -> { element, bonus, endTime }
        }
    };

    // ==========================================
    // WEAPON INFUSE FUNKTIONEN
    // Zauber auf Waffe wirken = temporaerer Element-Buff
    // NICHT das Gleiche wie ein Combo-Angriff!
    // ==========================================

    const INFUSE_BONUSES = {
        feuer: { damageBonus: 0.25, element: 'fire', color: '#ff4400', name: 'Flammen' },
        eis: { damageBonus: 0.20, element: 'ice', color: '#88ddff', name: 'Frost', effect: 'slow' },
        blitz: { damageBonus: 0.30, element: 'lightning', color: '#ffff00', name: 'Blitz', effect: 'stun_chance' },
        licht: { damageBonus: 0.25, element: 'light', color: '#ffffaa', name: 'Licht', effect: 'undead_bonus' },
        dunkel: { damageBonus: 0.20, element: 'dark', color: '#330066', name: 'Schatten', effect: 'lifesteal' },
        natur: { damageBonus: 0.15, element: 'nature', color: '#00aa00', name: 'Natur', effect: 'poison' },
        erde: { damageBonus: 0.15, element: 'earth', color: '#8b4513', name: 'Stein', effect: 'armor_pierce' },
        wind: { damageBonus: 0.15, element: 'wind', color: '#aaffaa', name: 'Wind', effect: 'speed_boost' },
        wasser: { damageBonus: 0.10, element: 'water', color: '#0066ff', name: 'Wasser', effect: 'heal_on_hit' }
        // EXPLOSION: NIEMALS auf Waffen! (8 Gebote!)
    };

    /**
     * Zauber auf Waffe wirken = temporaerer Buff
     *
     * Beispiel: Links Feuerball, Rechts Schwert
     * -> infuseWeapon('left', 'right')
     * -> Flammenschwert fuer 30 Sekunden!
     *
     * WICHTIG: EXPLOSION kann NIEMALS auf Waffen angewendet werden!
     */
    function infuseWeapon(spellHand, weaponHand) {
        const spellSlot = spellHand === 'left' ? state.infuse.leftHand : state.infuse.rightHand;
        const weaponSlot = weaponHand === 'left' ? state.infuse.leftHand : state.infuse.rightHand;

        // Pruefen ob Zauber vorhanden
        if (spellSlot.type !== 'spell' || !spellSlot.item) {
            addLog(`❌ Kein Zauber in ${spellHand === 'left' ? 'linker' : 'rechter'} Hand!`);
            return false;
        }

        // Pruefen ob Waffe vorhanden
        if (weaponSlot.type !== 'weapon' || !weaponSlot.item) {
            addLog(`❌ Keine Waffe in ${weaponHand === 'left' ? 'linker' : 'rechter'} Hand!`);
            return false;
        }

        const spell = SPELLS[spellSlot.item];
        if (!spell) {
            addLog('❌ Zauber nicht gefunden!');
            return false;
        }

        // EXPLOSION kann NIEMALS auf Waffen angewendet werden!
        if (spell.school === 'explosion') {
            addLog('💥 EXPLOSION kann NIEMALS auf Waffen angewendet werden! (8 Gebote!)');
            return false;
        }

        const infuseData = INFUSE_BONUSES[spell.school];
        if (!infuseData) {
            addLog(`❌ ${spell.name} kann nicht auf Waffen angewendet werden!`);
            return false;
        }

        // Mana-Kosten (50% des Zauber-Mana)
        const manaCost = Math.ceil(spell.mana * 0.5);
        if (state.player.mana < manaCost) {
            addLog(`❌ Nicht genug Mana! (${state.player.mana}/${manaCost})`);
            return false;
        }

        // Mana abziehen
        state.player.mana -= manaCost;

        // Infuse aktivieren (30 Sekunden)
        const duration = 30000;  // 30 Sekunden in ms
        const weaponId = weaponSlot.item;

        state.infuse.activeInfuses[weaponId] = {
            element: spell.school,
            bonus: infuseData.damageBonus,
            effect: infuseData.effect,
            color: infuseData.color,
            endTime: Date.now() + duration
        };

        // XP fuer Magie-Schule (Learning by Doing!)
        gainMagicXP(spell.school, 15);

        addLog(`✨ ${infuseData.name}-${weaponId}! +${Math.round(infuseData.damageBonus * 100)}% ${infuseData.name}-Schaden fuer 30s!`);

        // UI Update
        updateUI();
        return true;
    }

    /**
     * Prueft ob eine Waffe infust ist und gibt Bonus zurueck
     */
    function getInfuseBonus(weaponId) {
        const infuse = state.infuse.activeInfuses[weaponId];
        if (!infuse) return null;

        // Abgelaufen?
        if (Date.now() > infuse.endTime) {
            delete state.infuse.activeInfuses[weaponId];
            addLog(`⏱️ ${weaponId} Infuse abgelaufen!`);
            return null;
        }

        return infuse;
    }

    /**
     * Zauber oder Waffe in Hand ausruesten
     */
    function equipToHand(hand, type, itemId) {
        const slot = hand === 'left' ? state.infuse.leftHand : state.infuse.rightHand;
        slot.type = type;
        slot.item = itemId;
        addLog(`${hand === 'left' ? '⬅️' : '➡️'} ${type === 'spell' ? '🔮' : '⚔️'} ${itemId} ausgeruestet!`);
        updateUI();
    }

    /**
     * Aktive Infuses anzeigen
     */
    function getActiveInfuses() {
        const now = Date.now();
        const active = [];

        for (const [weaponId, infuse] of Object.entries(state.infuse.activeInfuses)) {
            if (now < infuse.endTime) {
                const remaining = Math.ceil((infuse.endTime - now) / 1000);
                active.push({
                    weapon: weaponId,
                    element: infuse.element,
                    bonus: infuse.bonus,
                    remaining: remaining,
                    color: infuse.color
                });
            }
        }

        return active;
    }

    // ==========================================
    // COOLDOWNS & STAMINA/MANA KOSTEN
    // ==========================================

    const COOLDOWNS = {
        lightAttack: 400,
        heavyAttack: 1200,
        dodge: 800,
        parry: 500
    };

    const COSTS = {
        lightAttack: { stamina: 10 },
        heavyAttack: { stamina: 25 },
        dodge: { stamina: 20 },
        parry: { stamina: 15 }
    };

    const DAMAGE = {
        light: 1.0,
        heavy: 2.0,
        combo_3: 1.5,
        combo_5: 2.0,
        combo_10: 3.0,
        parryCounter: 2.5
    };

    // ==========================================
    // INITIALIZATION
    // ==========================================

    function init() {
        console.log('⚔️ Unified Combat System v2 initializing...');
        console.log('   📚 9 Magieschulen + Explosion');
        console.log('   💥 Finisher System aktiv');

        calculateDerivedStats();
        createCombatUI();
        setupKeyBindings();
        startRegenLoop();

        console.log('✅ Unified Combat System ready!');
    }

    function calculateDerivedStats() {
        const s = state.player.special;

        // Berechne Stats aus S.P.E.C.I.A.L.
        state.player.maxHp = 100 + s.VIT * 15;
        state.player.maxMana = 100 + s.INT * 10;
        state.player.attackPower = 15 + s.POW * 2;
        state.player.spellPower = 20 + s.INT * 3;
        state.player.defense = 5 + Math.floor(s.VIT * 0.5);
        state.player.speed = 1.0 + s.AGI * 0.01;
        state.player.critChance = 0.05 + s.LUK * 0.01;
        state.player.critMultiplier = 1.5 + s.LUK * 0.05;
        state.player.manaRegen = 2 + s.WIL * 0.5;
    }

    // ==========================================
    // START COMBAT
    // ==========================================

    function startCombat(options) {
        console.log('⚔️ Starting combat:', options.type);

        state.active = true;
        state.context.type = options.type || 'overworld';
        state.context.location = options.location || 'Unknown';
        state.context.isHardcore = options.isHardcore || false;
        state.context.waveNumber = options.waveNumber || 0;

        // Reset Player
        state.player.hp = state.player.maxHp;
        state.player.mana = state.player.maxMana;
        state.player.stamina = state.player.maxStamina;
        state.player.comboCount = 0;
        state.player.buffs = {};
        state.player.debuffs = {};

        // Setup Enemies
        if (options.enemies && options.enemies.length > 0) {
            state.enemies = options.enemies.map(e => createEnemy(e));
            state.enemy = state.enemies[0];
        } else if (options.enemy) {
            state.enemy = createEnemy(options.enemy);
            state.enemies = [state.enemy];
        }

        state.log = [];
        addLog(`Kampf beginnt! ${state.context.isHardcore ? '⚠️ HARDCORE!' : ''}`);

        showCombatUI();
        updateUI();

        if (state.mode === 'auto') {
            startAutoMode();
        }

        startEnemyAI();
        return true;
    }

    function createEnemy(data) {
        return {
            id: data.id || 'enemy_' + Date.now(),
            name: data.name || 'Gegner',
            hp: data.hp || 50,
            maxHp: data.maxHp || data.hp || 50,
            attack: data.attack || data.damage || 10,
            defense: data.defense || 5,
            speed: data.speed || 1.0,
            type: data.type || 'normal',
            element: data.element || null,
            xp: data.xp || 10,
            loot: data.loot || [],
            traits: data.traits || [],
            isStunned: false,
            stunDuration: 0,
            nextAttackTime: Date.now() + 1000 + Math.random() * 1000
        };
    }

    // ==========================================
    // PHYSISCHE ANGRIFFE
    // ==========================================

    function lightAttack(hand = 'right') {
        if (!canPerformAction('lightAttack')) return false;
        if (!useStamina(COSTS.lightAttack.stamina * (hand === 'both' ? 1.5 : 1))) return false;

        setCooldown('lightAttack');

        let damage = calculatePhysicalDamage('light', hand);
        incrementCombo();
        applyDamageToEnemy(damage);
        gainFinisherMeter('normalAttack');

        addLog(`${hand === 'both' ? 'Doppel-' : ''}Angriff! ${damage} Schaden`);
        updateUI();
        return true;
    }

    function heavyAttack(hand = 'right') {
        if (!canPerformAction('heavyAttack')) return false;
        if (!useStamina(COSTS.heavyAttack.stamina * (hand === 'both' ? 1.5 : 1))) return false;

        setCooldown('heavyAttack');

        let damage = calculatePhysicalDamage('heavy', hand);

        // Chance auf Stun
        if (Math.random() < 0.3 && state.enemy) {
            state.enemy.isStunned = true;
            state.enemy.stunDuration = 2000;
            addLog('💫 Gegner betäubt!');
        }

        incrementCombo();
        applyDamageToEnemy(damage);
        gainFinisherMeter('chargedAttack');

        addLog(`${hand === 'both' ? 'Doppel-' : ''}SCHWERER Angriff! ${damage} Schaden`);
        updateUI();
        return true;
    }

    function dodge() {
        if (!canPerformAction('dodge')) return false;
        if (!useStamina(COSTS.dodge.stamina)) return false;

        setCooldown('dodge');
        state.player.buffs.invincible = Date.now() + 300;

        addLog('🏃 Ausgewichen!');
        updateUI();
        return true;
    }

    function parry() {
        if (!canPerformAction('parry')) return false;
        if (!useStamina(COSTS.parry.stamina)) return false;

        setCooldown('parry');
        state.player.buffs.parrying = Date.now() + 200;

        addLog('🛡️ Parieren!');
        updateUI();
        return true;
    }

    // ==========================================
    // MAGIE-SYSTEM
    // ==========================================

    /**
     * Zaubert einen Spell
     * @param {string} spellId - ID des Zaubers
     * @param {Object} target - Ziel (optional)
     */
    function castSpell(spellId, target = null) {
        const spell = SPELLS[spellId];
        if (!spell) {
            addLog(`❌ Unbekannter Zauber: ${spellId}`);
            return false;
        }

        // Prüfe ob Spieler den Spell kennt
        if (!state.player.knownSpells.includes(spellId)) {
            addLog(`❌ Du kennst diesen Zauber nicht!`);
            return false;
        }

        // Najika-Only Check für Tier 3 Explosion
        if (spell.najikaOnly && !state.player.isNajika) {
            addLog(`❌ Nur Najika kann OMEGA-DETONATION wirken!`);
            return false;
        }

        // Mana Check
        if (state.player.mana < spell.mana) {
            addLog(`❌ Nicht genug Mana! (${state.player.mana}/${spell.mana})`);
            return false;
        }

        // Stamina Check (für Explosion)
        if (spell.stamina && state.player.stamina < spell.stamina) {
            addLog(`❌ Nicht genug Stamina für ${spell.name}!`);
            return false;
        }

        // Exhaustion Check
        if (state.player.isExhausted) {
            addLog(`❌ Du bist noch erschöpft! *liegt am Boden*`);
            return false;
        }

        // Cooldown Check
        if (state.player.spellCooldowns[spellId] && Date.now() < state.player.spellCooldowns[spellId]) {
            addLog(`⏳ ${spell.name} ist noch auf Cooldown!`);
            return false;
        }

        // Kosten abziehen
        state.player.mana -= spell.mana;
        if (spell.stamina) {
            state.player.stamina -= spell.stamina;
        }

        // Casting Animation (für Explosion länger!)
        const castTime = spell.cast || 0.5;
        addLog(`🔮 Wirke ${spell.name}... (${castTime}s)`);

        // Explosion spezielle Behandlung
        if (spell.school === 'explosion') {
            handleExplosionCast(spell);
        } else {
            handleNormalSpellCast(spell, target);
        }

        // Learning by Doing: XP für Schule
        gainSchoolXP(spell.school, 5 + spell.tier * 5);

        // Cooldown setzen
        const cooldownTime = (spell.tier || 1) * 3000;
        state.player.spellCooldowns[spellId] = Date.now() + cooldownTime;

        updateUI();
        return true;
    }

    function handleExplosionCast(spell) {
        const school = MAGIC_SCHOOLS.explosion;

        // Berechne Schaden (INT skaliert extra für Explosion!)
        let damage = spell.damage;
        damage *= (1 + state.player.special.INT * 0.05);
        damage *= (1 + state.player.schoolMastery.explosion * 0.02);

        // Luck-Bonus für Explosion
        damage *= (1 + state.player.special.LUK * 0.02);

        setTimeout(() => {
            addLog(`💥💥💥 ${spell.name}!!! 💥💥💥`);
            addLog(`${Math.floor(damage)} SCHADEN!`);

            // Trifft alle Gegner
            state.enemies.forEach(enemy => {
                if (enemy.hp > 0) {
                    enemy.hp = Math.max(0, enemy.hp - damage);
                }
            });

            // Erschöpfung nach Explosion!
            state.player.isExhausted = true;
            state.player.exhaustionEndTime = Date.now() + (spell.exhaustion * 1000);
            addLog(`*Najika fällt um* "...so... müde..." 😵`);

            setTimeout(() => {
                state.player.isExhausted = false;
                addLog(`*Najika steht wieder auf* "...ich kann weitermachen!" 💪`);
            }, spell.exhaustion * 1000);

            checkEnemyDefeated();
            updateUI();
        }, spell.cast * 1000);
    }

    function handleNormalSpellCast(spell, target) {
        setTimeout(() => {
            let damage = 0;
            const school = MAGIC_SCHOOLS[spell.school];

            // Schadenzauber
            if (spell.damage) {
                damage = spell.damage;
                damage *= (1 + state.player.special.INT * 0.03);
                damage *= (1 + state.player.schoolMastery[spell.school] * 0.02);

                // Element-Bonus/Malus
                if (state.enemy && state.enemy.element) {
                    // TODO: Element-Schwächen-Tabelle
                }

                addLog(`${school.icon} ${spell.name}: ${Math.floor(damage)} Schaden!`);
                applyDamageToEnemy(damage);
            }

            // Heilzauber
            if (spell.heal) {
                const healAmount = spell.heal * (1 + state.player.special.WIL * 0.02);
                state.player.hp = Math.min(state.player.maxHp, state.player.hp + healAmount);
                addLog(`${school.icon} ${spell.name}: +${Math.floor(healAmount)} HP!`);
            }

            // Buffs
            if (spell.defense) {
                state.player.buffs.magicShield = {
                    value: spell.defense,
                    duration: spell.duration * 1000,
                    endTime: Date.now() + spell.duration * 1000
                };
                addLog(`${school.icon} ${spell.name}: +${spell.defense} Verteidigung!`);
            }

            // Stun/Freeze
            if (spell.stun && state.enemy) {
                state.enemy.isStunned = true;
                state.enemy.stunDuration = spell.stun * 1000;
                addLog(`${school.icon} Gegner eingefroren für ${spell.stun}s!`);
            }

            checkEnemyDefeated();
            updateUI();
        }, (spell.cast || 0.5) * 1000);
    }

    /**
     * Verwebt zwei Elemente (ESO-Style)
     * NICHT mit Explosion möglich!
     */
    function weaveElements(school1, school2) {
        if (school1 === 'explosion' || school2 === 'explosion') {
            addLog(`❌ Explosion kann NICHT mit anderen Elementen verwoben werden!`);
            return false;
        }

        const key1 = `${school1}+${school2}`;
        const key2 = `${school2}+${school1}`;
        const weave = ELEMENT_WEAVES[key1] || ELEMENT_WEAVES[key2];

        if (!weave) {
            addLog(`❌ ${school1} und ${school2} können nicht verwoben werden.`);
            return false;
        }

        // Prüfe Mastery Level (mindestens 20 in beiden Schulen)
        if (state.player.schoolMastery[school1] < 20 || state.player.schoolMastery[school2] < 20) {
            addLog(`❌ Benötigt Mastery 20+ in beiden Schulen!`);
            return false;
        }

        addLog(`✨ ${weave.name} verwoben! (${school1} + ${school2})`);
        // TODO: Weave-Effekt anwenden

        return true;
    }

    function gainSchoolXP(school, amount) {
        state.player.schoolXP[school] = (state.player.schoolXP[school] || 0) + amount;

        // Level-up Check
        const xpNeeded = state.player.schoolMastery[school] * 100 * 1.15;
        if (state.player.schoolXP[school] >= xpNeeded) {
            state.player.schoolXP[school] -= xpNeeded;
            state.player.schoolMastery[school]++;
            addLog(`📈 ${MAGIC_SCHOOLS[school].name} Level ${state.player.schoolMastery[school]}!`);
        }
    }

    // ==========================================
    // FINISHER SYSTEM
    // ==========================================

    function gainFinisherMeter(action) {
        const gain = FINISHER_CONFIG.meterGain[action] || 5;
        state.player.finisherMeter = Math.min(FINISHER_CONFIG.meterMax, state.player.finisherMeter + gain);
    }

    function canUseFinisher() {
        if (state.player.finisherMeter < FINISHER_CONFIG.meterMax) return false;
        if (!state.enemy || state.enemy.hp > state.enemy.maxHp * 0.2) return false;

        // 24h Cooldown Check
        const timeSinceLast = Date.now() - state.player.lastFinisherTime;
        if (timeSinceLast < FINISHER_CONFIG.cooldown) return false;

        return true;
    }

    function executeFinisher(finisherId = 'explosion') {
        if (!canUseFinisher()) {
            addLog(`❌ Finisher nicht verfügbar!`);
            return false;
        }

        state.player.finisherMeter = 0;
        state.player.lastFinisherTime = Date.now();

        // Najika's Explosion Finisher
        if (state.player.isNajika && finisherId === 'explosion') {
            executeExplosionFinisher();
        } else {
            executeGenericFinisher(finisherId);
        }

        return true;
    }

    function executeExplosionFinisher() {
        const tier = state.player.schoolMastery.explosion >= 50 ? 3 :
                     state.player.schoolMastery.explosion >= 25 ? 2 : 1;

        const config = FINISHER_CONFIG.najikaExplosionFinisher;
        const multiplier = tier === 3 ? config.tier3Multiplier :
                          tier === 2 ? config.tier2Multiplier : config.tier1Multiplier;

        const tierNames = {
            1: 'Kleine Explosion',
            2: 'EXPLOOOOSION!!!',
            3: 'OMEGA-DETONATION!!!'
        };

        // Animation
        addLog(`🔮 Magischer Kreis erscheint...`);
        addLog(`⚡ Energie sammelt sich...`);

        setTimeout(() => {
            const baseDamage = SPELLS[tier === 3 ? 'omega_detonation' : tier === 2 ? 'exploooosion' : 'kleine_explosion'].damage;
            const finalDamage = baseDamage * multiplier;

            addLog(`💥💥💥 FINISHER: ${tierNames[tier]} 💥💥💥`);
            addLog(`${finalDamage} MASSIVER SCHADEN!!!`);

            // Alle Gegner eliminieren
            state.enemies.forEach(enemy => {
                enemy.hp = 0;
            });

            // Tier 3: Overworld beschädigen (1x pro Tag!)
            if (tier === 3 && config.overworldDamage) {
                addLog(`🌍 Die Landschaft ist bis zur nächsten Regenerierung zerstört!`);
                // TODO: Overworld Damage Event triggern
                if (typeof window.triggerOverworldDamage === 'function') {
                    window.triggerOverworldDamage();
                }
            }

            // Erschöpfung
            state.player.isExhausted = true;
            state.player.exhaustionEndTime = Date.now() + config.exhaustionTime;
            addLog(`*Najika kollabiert* "...hat sich... gelohnt..." 😵`);

            checkEnemyDefeated();
            updateUI();
        }, 3000);
    }

    function executeGenericFinisher(finisherId) {
        addLog(`💀 FINISHER: ${finisherId}!`);

        const damage = state.player.attackPower * 5;
        state.enemies.forEach(enemy => {
            if (enemy.hp > 0) {
                enemy.hp = Math.max(0, enemy.hp - damage);
            }
        });

        checkEnemyDefeated();
        updateUI();
    }

    // ==========================================
    // DAMAGE CALCULATION
    // ==========================================

    function calculatePhysicalDamage(type, hand) {
        let baseDamage = state.player.attackPower;
        let multiplier = DAMAGE[type] || 1.0;
        let elementDamage = null;  // Fuer Infuse

        if (hand === 'both') multiplier *= 1.5;

        // ========== WEAPON INFUSE BONUS ==========
        // Pruefe ob Waffe mit einem Element infust ist
        const weaponSlot = hand === 'left' ? state.infuse.leftHand : state.infuse.rightHand;
        if (weaponSlot?.type === 'weapon' && weaponSlot.item) {
            const infuse = getInfuseBonus(weaponSlot.item);
            if (infuse) {
                multiplier *= (1 + infuse.bonus);
                elementDamage = infuse.element;

                // Spezial-Effekte basierend auf Element
                if (infuse.effect === 'slow' && state.enemy && Math.random() < 0.3) {
                    state.enemy.speedMod = 0.7;
                    addLog(`❄️ Gegner verlangsamt!`);
                }
                if (infuse.effect === 'stun_chance' && state.enemy && Math.random() < 0.1) {
                    state.enemy.isStunned = true;
                    state.enemy.stunDuration = 1000;
                    addLog(`⚡ Gegner paralysiert!`);
                }
                if (infuse.effect === 'lifesteal') {
                    const heal = Math.floor(baseDamage * 0.1);
                    state.player.hp = Math.min(state.player.maxHp, state.player.hp + heal);
                    addLog(`🩸 +${heal} HP durch Lebensraub!`);
                }
            }
        }

        // Combo Bonus
        if (state.player.comboCount >= 10) {
            multiplier *= DAMAGE.combo_10;
        } else if (state.player.comboCount >= 5) {
            multiplier *= DAMAGE.combo_5;
            gainFinisherMeter('combo5');
        } else if (state.player.comboCount >= 3) {
            multiplier *= DAMAGE.combo_3;
        }

        // Cheer Buffs
        if (state.cheerBuffs.attack > 0) multiplier *= 1.1;
        if (state.cheerBuffs.combo > 0) {
            multiplier *= 1.3;
            state.cheerBuffs.combo--;
        }

        // Crit
        if (Math.random() < state.player.critChance) {
            multiplier *= state.player.critMultiplier;
            addLog('💥 KRITISCH!');
        }

        // Defense (Element-Schaden ignoriert teilweise Ruestung)
        let enemyDef = state.enemy?.defense || 0;
        if (state.enemy?.isStunned) enemyDef = 0;
        if (elementDamage) enemyDef *= 0.7;  // Element durchdringt 30% Ruestung

        return Math.max(1, Math.floor(baseDamage * multiplier - enemyDef));
    }

    function applyDamageToEnemy(damage) {
        if (!state.enemy || state.enemy.hp <= 0) {
            state.enemy = state.enemies.find(e => e.hp > 0);
            if (!state.enemy) return;
        }

        state.enemy.hp = Math.max(0, state.enemy.hp - damage);
        checkEnemyDefeated();
    }

    // ==========================================
    // COMBO SYSTEM
    // ==========================================

    function incrementCombo() {
        state.player.comboCount++;

        if (state.player.comboTimer) clearTimeout(state.player.comboTimer);

        state.player.comboTimer = setTimeout(() => {
            if (state.player.comboCount > 0) {
                addLog(`Combo beendet: ${state.player.comboCount} Hits`);
                state.player.comboCount = 0;
                updateUI();
            }
        }, 2000);

        if (state.player.comboCount === 3) addLog('🔥 3-Hit Combo!');
        else if (state.player.comboCount === 5) addLog('🔥🔥 5-Hit Combo!');
        else if (state.player.comboCount === 10) addLog('🔥🔥🔥 10-HIT COMBO!');
    }

    // ==========================================
    // RESOURCE MANAGEMENT
    // ==========================================

    function useStamina(amount) {
        if (state.player.stamina < amount) {
            addLog('❌ Nicht genug Stamina!');
            return false;
        }
        state.player.stamina -= amount;
        return true;
    }

    function startRegenLoop() {
        setInterval(() => {
            if (!state.active) return;

            // Stamina Regen
            if (state.player.stamina < state.player.maxStamina) {
                state.player.stamina = Math.min(
                    state.player.maxStamina,
                    state.player.stamina + state.player.staminaRegen / 10
                );
            }

            // Mana Regen
            if (state.player.mana < state.player.maxMana) {
                state.player.mana = Math.min(
                    state.player.maxMana,
                    state.player.mana + state.player.manaRegen / 10
                );
            }

            updateUI();
        }, 100);
    }

    // ==========================================
    // COOLDOWN SYSTEM
    // ==========================================

    function canPerformAction(action) {
        if (!state.active) return false;
        if (state.player.isExhausted) {
            addLog('❌ Noch erschöpft!');
            return false;
        }
        return Date.now() >= state.player.cooldowns[action];
    }

    function setCooldown(action) {
        state.player.cooldowns[action] = Date.now() + COOLDOWNS[action];
    }

    // ==========================================
    // ENEMY AI
    // ==========================================

    function startEnemyAI() {
        const aiLoop = setInterval(() => {
            if (!state.active) {
                clearInterval(aiLoop);
                return;
            }

            state.enemies.forEach(enemy => {
                if (enemy.hp > 0 && Date.now() >= enemy.nextAttackTime) {
                    state.enemy = enemy;
                    enemyTurn();
                    enemy.nextAttackTime = Date.now() + (1000 / enemy.speed) + Math.random() * 500;
                }
            });
        }, 100);
    }

    function enemyTurn() {
        if (!state.active || !state.enemy || state.enemy.hp <= 0) return;

        if (state.enemy.isStunned) {
            state.enemy.stunDuration -= 500;
            if (state.enemy.stunDuration <= 0) {
                state.enemy.isStunned = false;
                addLog(`${state.enemy.name} erholt sich!`);
            }
            return;
        }

        // Dodge Check
        if (state.player.buffs.invincible && Date.now() < state.player.buffs.invincible) {
            addLog(`${state.enemy.name} verpasst! (Ausgewichen)`);
            gainFinisherMeter('perfectDodge');
            return;
        }

        // Parry Check
        if (state.player.buffs.parrying && Date.now() < state.player.buffs.parrying) {
            let counterDamage = calculatePhysicalDamage('light', 'right') * DAMAGE.parryCounter;
            state.enemy.hp = Math.max(0, state.enemy.hp - counterDamage);
            addLog(`🛡️ PARIERT! Konter: ${counterDamage}!`);
            gainFinisherMeter('parryRiposte');
            checkEnemyDefeated();
            return;
        }

        // Enemy Attack
        let damage = state.enemy.attack;
        let defense = state.player.defense;

        if (state.cheerBuffs.defend > 0) defense *= 1.2;
        if (state.player.buffs.magicShield) {
            defense += state.player.buffs.magicShield.value;
        }

        damage = Math.max(1, damage - defense);
        state.player.hp = Math.max(0, state.player.hp - damage);

        addLog(`${state.enemy.name} greift an! -${damage} HP`);

        if (state.player.hp <= 0) {
            handleDefeat();
        }

        updateUI();
    }

    // ==========================================
    // AUTO / CHEER MODE
    // ==========================================

    let autoModeInterval = null;

    function startAutoMode() {
        if (autoModeInterval) clearInterval(autoModeInterval);

        autoModeInterval = setInterval(() => {
            if (!state.active || state.mode !== 'auto') {
                clearInterval(autoModeInterval);
                autoModeInterval = null;
                return;
            }

            if (state.player.stamina > 30 && canPerformAction('lightAttack')) {
                lightAttack('right');
            }
            if (state.player.stamina > 50 && Math.random() < 0.2 && canPerformAction('heavyAttack')) {
                heavyAttack('right');
            }
        }, 500);
    }

    function setMode(newMode) {
        if (!['auto', 'manual', 'cheer'].includes(newMode)) return;

        state.mode = newMode;
        addLog(`Modus: ${getModeDisplayName(newMode)}`);

        if (newMode === 'auto' && state.active) startAutoMode();
        else if (autoModeInterval) {
            clearInterval(autoModeInterval);
            autoModeInterval = null;
        }

        updateUI();
    }

    function getModeDisplayName(mode) {
        return { auto: '🤖 KI', manual: '🎮 Manuell', cheer: '📣 Anfeuern' }[mode] || mode;
    }

    function cheer(type) {
        if (state.mode !== 'cheer') return false;

        const effects = {
            attack: { buff: 'attack', rounds: 3, msg: '💪 "LOS!" - Angriff +10%!' },
            defend: { buff: 'defend', rounds: 3, msg: '🛡️ "DEFEND!" - Verteidigung +20%!' },
            combo: { buff: 'combo', rounds: 1, msg: '💥 "COMBO!" - Nächster = Combo!' },
            focus: { buff: 'focus', rounds: 3, msg: '🎯 "FOCUS!" - Crit +15%!' }
        };

        const effect = effects[type];
        if (!effect || state.cheerBuffs[effect.buff] > 0) return false;

        state.cheerBuffs[effect.buff] = effect.rounds;
        addLog(effect.msg);

        setTimeout(() => {
            if (state.mode === 'cheer' && state.active) lightAttack('right');
        }, 500);

        updateUI();
        return true;
    }

    // ==========================================
    // VICTORY / DEFEAT
    // ==========================================

    function checkEnemyDefeated() {
        if (!state.enemy) return;

        if (state.enemy.hp <= 0) {
            addLog(`💀 ${state.enemy.name} besiegt! +${state.enemy.xp} XP`);

            if (typeof window.onEnemyKilled === 'function') {
                window.onEnemyKilled(state.enemy.xp, state.enemy.loot, null);
            }

            state.enemy = state.enemies.find(e => e.hp > 0);
            if (!state.enemy) handleVictory();
        }
    }

    function handleVictory() {
        addLog('🎉 SIEG!!!');

        const totalXP = state.enemies.reduce((sum, e) => sum + e.xp, 0);
        const allLoot = state.enemies.flatMap(e => e.loot);

        addLog(`${totalXP} XP | Loot: ${allLoot.join(', ') || 'nichts'}`);

        if (typeof window.onCombatVictory === 'function') {
            window.onCombatVictory({
                type: state.context.type,
                xp: totalXP,
                loot: allLoot,
                waveNumber: state.context.waveNumber
            });
        }

        setTimeout(() => endCombat(), 2000);
    }

    function handleDefeat() {
        addLog('💀 NIEDERLAGE...');

        if (state.context.isHardcore) {
            addLog('⚠️ HARDCORE: Echte Konsequenzen!');
        }

        if (typeof window.onCombatDefeat === 'function') {
            window.onCombatDefeat({
                type: state.context.type,
                isHardcore: state.context.isHardcore,
                waveNumber: state.context.waveNumber
            });
        }

        setTimeout(() => endCombat(), 2000);
    }

    function endCombat() {
        state.active = false;
        state.enemy = null;
        state.enemies = [];

        if (autoModeInterval) {
            clearInterval(autoModeInterval);
            autoModeInterval = null;
        }

        hideCombatUI();
    }

    // ==========================================
    // UI
    // ==========================================

    function createCombatUI() {
        if (document.getElementById('unified-combat-ui')) return;

        const ui = document.createElement('div');
        ui.id = 'unified-combat-ui';
        ui.className = 'unified-combat-ui hidden';
        ui.innerHTML = `
            <div class="combat-header">
                <div class="player-info">
                    <div class="player-name">KUJA</div>
                    <div class="bar-container hp">
                        <div class="bar-fill" id="player-hp-bar"></div>
                        <span class="bar-text" id="player-hp-text">100/100 HP</span>
                    </div>
                    <div class="bar-container mana">
                        <div class="bar-fill" id="player-mana-bar"></div>
                        <span class="bar-text" id="player-mana-text">100/100 MP</span>
                    </div>
                    <div class="bar-container stamina">
                        <div class="bar-fill" id="player-stamina-bar"></div>
                        <span class="bar-text" id="player-stamina-text">100/100 SP</span>
                    </div>
                    <div class="combat-meters">
                        <span class="combo" id="combo-display">Combo: 0</span>
                        <span class="finisher" id="finisher-display">Finisher: 0%</span>
                    </div>
                </div>

                <div class="mode-switcher">
                    <button class="mode-btn" data-mode="auto">🤖 Auto</button>
                    <button class="mode-btn active" data-mode="manual">🎮 Manual</button>
                    <button class="mode-btn" data-mode="cheer">📣 Cheer</button>
                </div>

                <div class="enemy-info" id="enemy-info">
                    <div class="enemy-name" id="enemy-name">Gegner</div>
                    <div class="bar-container hp enemy">
                        <div class="bar-fill" id="enemy-hp-bar"></div>
                        <span class="bar-text" id="enemy-hp-text">50/50</span>
                    </div>
                </div>
            </div>

            <div class="combat-actions" id="combat-actions">
                <div class="manual-actions" id="manual-actions">
                    <div class="action-row">
                        <button class="action-btn light" data-action="light-left">👊 L-Leicht</button>
                        <button class="action-btn light" data-action="light-right">Leicht-R 👊</button>
                        <button class="action-btn light dual" data-action="light-both">⚔️ Beide</button>
                    </div>
                    <div class="action-row">
                        <button class="action-btn heavy" data-action="heavy-left">💪 L-Schwer</button>
                        <button class="action-btn heavy" data-action="heavy-right">Schwer-R 💪</button>
                        <button class="action-btn heavy dual" data-action="heavy-both">⚔️ Beide</button>
                    </div>
                    <div class="action-row">
                        <button class="action-btn dodge" data-action="dodge">🏃 Dodge</button>
                        <button class="action-btn parry" data-action="parry">🛡️ Parry</button>
                        <button class="action-btn finisher" data-action="finisher" id="finisher-btn" disabled>💀 FINISHER</button>
                    </div>
                    <div class="action-row magic-row">
                        <button class="action-btn magic fire" data-spell="flammen">🔥 Feuer</button>
                        <button class="action-btn magic ice" data-spell="eiszapfen">❄️ Eis</button>
                        <button class="action-btn magic heal" data-spell="heilung">💧 Heilung</button>
                        <button class="action-btn magic explosion" data-spell="kleine_explosion">💥 EXPLOSION!</button>
                    </div>
                </div>

                <div class="cheer-actions hidden" id="cheer-actions">
                    <button class="cheer-btn" data-cheer="attack">💪 LOS!</button>
                    <button class="cheer-btn" data-cheer="defend">🛡️ DEFEND!</button>
                    <button class="cheer-btn" data-cheer="combo">💥 COMBO!</button>
                    <button class="cheer-btn" data-cheer="focus">🎯 FOCUS!</button>
                </div>

                <div class="auto-info hidden" id="auto-info">
                    <p>🤖 KI kämpft für dich...</p>
                </div>
            </div>

            <div class="combat-log" id="combat-log">
                <div class="log-entries" id="log-entries"></div>
            </div>
        `;

        document.body.appendChild(ui);
        state.uiContainer = ui;
        addCombatStyles();
        attachUIEvents();
    }

    function addCombatStyles() {
        if (document.getElementById('unified-combat-styles')) return;

        const styles = document.createElement('style');
        styles.id = 'unified-combat-styles';
        styles.textContent = `
            .unified-combat-ui {
                position: fixed; bottom: 0; left: 0; right: 0;
                background: linear-gradient(180deg, rgba(0,0,0,0.9), rgba(20,20,40,0.95));
                border-top: 3px solid #667eea; padding: 15px; z-index: 15000;
                font-family: 'Segoe UI', sans-serif; color: white;
            }
            .unified-combat-ui.hidden { display: none; }
            .combat-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
            .player-info, .enemy-info { flex: 1; }
            .enemy-info { text-align: right; }
            .player-name, .enemy-name { font-weight: bold; font-size: 1.2em; margin-bottom: 5px; }
            .enemy-name { color: #ff6b6b; }

            .bar-container { background: #333; border-radius: 5px; height: 18px; position: relative; margin: 3px 0; overflow: hidden; }
            .bar-container.hp .bar-fill { background: linear-gradient(90deg, #4CAF50, #8BC34A); }
            .bar-container.hp.enemy .bar-fill { background: linear-gradient(90deg, #ff4444, #ff6b6b); }
            .bar-container.mana .bar-fill { background: linear-gradient(90deg, #2196F3, #03A9F4); }
            .bar-container.stamina .bar-fill { background: linear-gradient(90deg, #FF9800, #FFC107); }
            .bar-fill { height: 100%; transition: width 0.2s; }
            .bar-text { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 11px; font-weight: bold; text-shadow: 1px 1px 2px black; }

            .combat-meters { display: flex; gap: 15px; margin-top: 5px; }
            .combo { color: #FFD700; }
            .finisher { color: #ff4444; }

            .mode-switcher { display: flex; gap: 10px; }
            .mode-btn { padding: 10px 20px; border: 2px solid #444; background: #222; color: #aaa; border-radius: 8px; cursor: pointer; transition: all 0.2s; }
            .mode-btn:hover { border-color: #667eea; color: white; }
            .mode-btn.active { background: linear-gradient(135deg, #667eea, #764ba2); border-color: #667eea; color: white; }

            .action-row { display: flex; gap: 10px; margin: 8px 0; justify-content: center; flex-wrap: wrap; }
            .action-btn, .cheer-btn { padding: 12px 18px; border: none; border-radius: 8px; cursor: pointer; font-size: 13px; font-weight: bold; transition: all 0.2s; min-width: 100px; }
            .action-btn.light { background: linear-gradient(135deg, #4CAF50, #45a049); color: white; }
            .action-btn.heavy { background: linear-gradient(135deg, #ff9800, #f57c00); color: white; }
            .action-btn.dodge { background: linear-gradient(135deg, #2196F3, #1976D2); color: white; }
            .action-btn.parry { background: linear-gradient(135deg, #9C27B0, #7B1FA2); color: white; }
            .action-btn.finisher { background: linear-gradient(135deg, #ff4444, #cc0000); color: white; }
            .action-btn.magic { min-width: 110px; }
            .action-btn.magic.fire { background: linear-gradient(135deg, #ff4400, #cc3300); }
            .action-btn.magic.ice { background: linear-gradient(135deg, #00bcd4, #0097a7); }
            .action-btn.magic.heal { background: linear-gradient(135deg, #4CAF50, #388E3C); }
            .action-btn.magic.explosion { background: linear-gradient(135deg, #ff0000, #aa0000); animation: pulse-explosion 1s infinite; }
            @keyframes pulse-explosion { 0%, 100% { box-shadow: 0 0 5px #ff0000; } 50% { box-shadow: 0 0 20px #ff4444; } }
            .action-btn:hover { transform: scale(1.05); }
            .action-btn:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }
            .cheer-btn { background: linear-gradient(135deg, #FFD700, #FFA500); color: #333; font-size: 16px; padding: 15px 25px; }
            .cheer-actions, .auto-info { text-align: center; }
            .cheer-actions.hidden, .auto-info.hidden, .manual-actions.hidden { display: none; }

            .combat-log { max-height: 80px; overflow-y: auto; background: rgba(0,0,0,0.5); border-radius: 5px; padding: 8px; margin-top: 10px; }
            .log-entries { font-size: 11px; }
            .log-entry { padding: 2px 0; border-bottom: 1px solid rgba(255,255,255,0.1); }
        `;
        document.head.appendChild(styles);
    }

    function attachUIEvents() {
        const ui = state.uiContainer;
        if (!ui) return;

        // Mode switching
        ui.querySelectorAll('.mode-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                setMode(btn.dataset.mode);
                ui.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                const manual = ui.querySelector('#manual-actions');
                const cheer = ui.querySelector('#cheer-actions');
                const auto = ui.querySelector('#auto-info');

                manual.classList.toggle('hidden', btn.dataset.mode !== 'manual');
                cheer.classList.toggle('hidden', btn.dataset.mode !== 'cheer');
                auto.classList.toggle('hidden', btn.dataset.mode !== 'auto');
            });
        });

        // Physical actions
        ui.querySelectorAll('.action-btn[data-action]').forEach(btn => {
            btn.addEventListener('click', () => {
                const action = btn.dataset.action;
                switch(action) {
                    case 'light-left': lightAttack('left'); break;
                    case 'light-right': lightAttack('right'); break;
                    case 'light-both': lightAttack('both'); break;
                    case 'heavy-left': heavyAttack('left'); break;
                    case 'heavy-right': heavyAttack('right'); break;
                    case 'heavy-both': heavyAttack('both'); break;
                    case 'dodge': dodge(); break;
                    case 'parry': parry(); break;
                    case 'finisher': executeFinisher(); break;
                }
            });
        });

        // Magic actions
        ui.querySelectorAll('.action-btn[data-spell]').forEach(btn => {
            btn.addEventListener('click', () => {
                castSpell(btn.dataset.spell);
            });
        });

        // Cheer actions
        ui.querySelectorAll('.cheer-btn').forEach(btn => {
            btn.addEventListener('click', () => cheer(btn.dataset.cheer));
        });
    }

    function setupKeyBindings() {
        document.addEventListener('keydown', (e) => {
            if (!state.active || state.mode !== 'manual') return;

            switch(e.code) {
                case 'KeyQ': lightAttack('left'); break;
                case 'KeyE': lightAttack('right'); break;
                case 'KeyR': lightAttack('both'); break;
                case 'KeyA': heavyAttack('left'); break;
                case 'KeyD': heavyAttack('right'); break;
                case 'KeyF': heavyAttack('both'); break;
                case 'Space': dodge(); e.preventDefault(); break;
                case 'ShiftLeft': case 'ShiftRight': parry(); break;
                case 'Digit1': castSpell('flammen'); break;
                case 'Digit2': castSpell('eiszapfen'); break;
                case 'Digit3': castSpell('heilung'); break;
                case 'Digit4': castSpell('kleine_explosion'); break;
                case 'KeyX': if (canUseFinisher()) executeFinisher(); break;
            }
        });
    }

    function updateUI() {
        if (!state.uiContainer) return;

        // Player bars
        const hpBar = document.getElementById('player-hp-bar');
        const hpText = document.getElementById('player-hp-text');
        const manaBar = document.getElementById('player-mana-bar');
        const manaText = document.getElementById('player-mana-text');
        const staminaBar = document.getElementById('player-stamina-bar');
        const staminaText = document.getElementById('player-stamina-text');

        if (hpBar) hpBar.style.width = `${(state.player.hp / state.player.maxHp) * 100}%`;
        if (hpText) hpText.textContent = `${Math.floor(state.player.hp)}/${state.player.maxHp} HP`;
        if (manaBar) manaBar.style.width = `${(state.player.mana / state.player.maxMana) * 100}%`;
        if (manaText) manaText.textContent = `${Math.floor(state.player.mana)}/${state.player.maxMana} MP`;
        if (staminaBar) staminaBar.style.width = `${(state.player.stamina / state.player.maxStamina) * 100}%`;
        if (staminaText) staminaText.textContent = `${Math.floor(state.player.stamina)}/${state.player.maxStamina} SP`;

        // Combo & Finisher
        const comboDisplay = document.getElementById('combo-display');
        const finisherDisplay = document.getElementById('finisher-display');
        const finisherBtn = document.getElementById('finisher-btn');

        if (comboDisplay) {
            comboDisplay.textContent = `Combo: ${state.player.comboCount}`;
            comboDisplay.style.color = state.player.comboCount >= 5 ? '#ff4444' : '#FFD700';
        }
        if (finisherDisplay) {
            finisherDisplay.textContent = `Finisher: ${state.player.finisherMeter}%`;
        }
        if (finisherBtn) {
            finisherBtn.disabled = !canUseFinisher();
        }

        // Enemy
        if (state.enemy) {
            const enemyName = document.getElementById('enemy-name');
            const enemyHpBar = document.getElementById('enemy-hp-bar');
            const enemyHpText = document.getElementById('enemy-hp-text');

            if (enemyName) enemyName.textContent = state.enemy.name;
            if (enemyHpBar) enemyHpBar.style.width = `${(state.enemy.hp / state.enemy.maxHp) * 100}%`;
            if (enemyHpText) enemyHpText.textContent = `${Math.floor(state.enemy.hp)}/${state.enemy.maxHp}`;
        }
    }

    function showCombatUI() {
        if (state.uiContainer) state.uiContainer.classList.remove('hidden');
    }

    function hideCombatUI() {
        if (state.uiContainer) state.uiContainer.classList.add('hidden');
    }

    function addLog(message) {
        state.log.push({ time: Date.now(), message });
        if (state.log.length > 50) state.log.shift();

        const logEntries = document.getElementById('log-entries');
        if (logEntries) {
            const entry = document.createElement('div');
            entry.className = 'log-entry';
            entry.textContent = message;
            logEntries.appendChild(entry);
            logEntries.scrollTop = logEntries.scrollHeight;
        }
        console.log(`⚔️ ${message}`);
    }

    // ==========================================
    // INIT
    // ==========================================

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // ==========================================
    // PUBLIC API
    // ==========================================

    return {
        startCombat,
        endCombat,
        lightAttack,
        heavyAttack,
        dodge,
        parry,
        castSpell,
        weaveElements,
        executeFinisher,
        cheer,
        setMode,
        getMode: () => state.mode,
        isActive: () => state.active,
        getState: () => state,
        getPlayer: () => state.player,
        canUseFinisher,
        showUI: showCombatUI,
        hideUI: hideCombatUI,

        // ========== WEAPON INFUSE API ==========
        infuseWeapon,           // Zauber auf Waffe = temporaerer Buff
        equipToHand,            // Zauber/Waffe in Hand ausruesten
        getActiveInfuses,       // Aktive Infuses anzeigen
        getInfuseBonus,         // Bonus fuer infuste Waffe
        getInfuse: () => state.infuse  // Komplettes Infuse-State
    };
})();

window.UnifiedCombat = UnifiedCombat;

console.log('⚔️ Unified Combat System v3 loaded!');
console.log('   🎮 Controls: Q/E/R (Light), A/D/F (Heavy), Space (Dodge), Shift (Parry)');
console.log('   ✨ WEAPON INFUSE: Zauber auf Waffe = temporaerer Buff!');
console.log('   🔮 Magic: 1 (Feuer), 2 (Eis), 3 (Heilung), 4 (EXPLOSION!)');
console.log('   💀 Finisher: X (wenn verfügbar)');
