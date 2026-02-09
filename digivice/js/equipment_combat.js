/**
 * NAJIKA EQUIPMENT COMBAT SYSTEM
 * Souls-like Combat mit Equipment-basierten Angriffen
 *
 * Features:
 * - Linke/Rechte Hand Waffen
 * - Leichte/Schwere Angriffe
 * - Stamina-System
 * - Dodge Roll mit i-Frames
 * - Parry/Block
 * - Combo-System
 */

(function() {
    'use strict';

    // ===== EQUIPMENT DATABASE (30+ WAFFEN) =====
    const WEAPONS = {
        // ==================== SCHWERTER (8) ====================
        rusty_sword: {
            name: 'Rostiges Schwert', type: 'sword', hand: 'right',
            damage: { light: 15, heavy: 30 }, staminaCost: { light: 10, heavy: 25 },
            speed: { light: 0.4, heavy: 0.8 }, range: 2.5, element: null, special: null
        },
        iron_sword: {
            name: 'Eisenschwert', type: 'sword', hand: 'right',
            damage: { light: 22, heavy: 45 }, staminaCost: { light: 12, heavy: 28 },
            speed: { light: 0.4, heavy: 0.8 }, range: 2.8, element: null, special: null
        },
        steel_sword: {
            name: 'Stahlschwert', type: 'sword', hand: 'right',
            damage: { light: 28, heavy: 55 }, staminaCost: { light: 14, heavy: 30 },
            speed: { light: 0.38, heavy: 0.75 }, range: 3.0, element: null, special: null
        },
        flame_blade: {
            name: 'Flammenklinge', type: 'sword', hand: 'right',
            damage: { light: 18, heavy: 38 }, staminaCost: { light: 15, heavy: 32 },
            speed: { light: 0.45, heavy: 0.9 }, range: 2.5, element: 'fire', special: 'burn'
        },
        frost_edge: {
            name: 'Frostschneide', type: 'sword', hand: 'right',
            damage: { light: 20, heavy: 42 }, staminaCost: { light: 14, heavy: 30 },
            speed: { light: 0.45, heavy: 0.85 }, range: 2.6, element: 'ice', special: 'slow'
        },
        lightning_saber: {
            name: 'Blitzsäbel', type: 'sword', hand: 'right',
            damage: { light: 16, heavy: 35 }, staminaCost: { light: 12, heavy: 28 },
            speed: { light: 0.3, heavy: 0.6 }, range: 2.8, element: 'lightning', special: 'chain'
        },
        zweihander: {
            name: 'Zweihänder', type: 'sword', hand: 'both',
            damage: { light: 35, heavy: 80 }, staminaCost: { light: 25, heavy: 50 },
            speed: { light: 0.8, heavy: 1.5 }, range: 4.0, element: null, special: 'stagger'
        },
        katana: {
            name: 'Katana', type: 'sword', hand: 'right',
            damage: { light: 24, heavy: 48 }, staminaCost: { light: 10, heavy: 22 },
            speed: { light: 0.25, heavy: 0.5 }, range: 2.8, element: null, special: 'iai_slash', critChance: 0.2
        },

        // ==================== DOLCHE (4) ====================
        rusty_dagger: {
            name: 'Rostiger Dolch', type: 'dagger', hand: 'both',
            damage: { light: 8, heavy: 18 }, staminaCost: { light: 5, heavy: 12 },
            speed: { light: 0.2, heavy: 0.4 }, range: 1.5, element: null, special: 'bleed', critChance: 0.15
        },
        assassin_blade: {
            name: 'Assassinenklinge', type: 'dagger', hand: 'both',
            damage: { light: 12, heavy: 28 }, staminaCost: { light: 6, heavy: 14 },
            speed: { light: 0.18, heavy: 0.35 }, range: 1.8, element: 'shadow', special: 'backstab', critChance: 0.25
        },
        poison_dagger: {
            name: 'Giftdolch', type: 'dagger', hand: 'both',
            damage: { light: 10, heavy: 22 }, staminaCost: { light: 6, heavy: 14 },
            speed: { light: 0.2, heavy: 0.4 }, range: 1.6, element: 'poison', special: 'poison_stack', critChance: 0.18
        },
        soul_knife: {
            name: 'Seelenmesser', type: 'dagger', hand: 'both',
            damage: { light: 14, heavy: 32 }, staminaCost: { light: 8, heavy: 18 },
            speed: { light: 0.22, heavy: 0.45 }, range: 1.7, element: 'shadow', special: 'soul_drain', critChance: 0.22
        },

        // ==================== ÄXTE (4) ====================
        wood_axe: {
            name: 'Holzfälleraxt', type: 'axe', hand: 'right',
            damage: { light: 18, heavy: 40 }, staminaCost: { light: 15, heavy: 35 },
            speed: { light: 0.5, heavy: 1.0 }, range: 2.2, element: null, special: null
        },
        battle_axe: {
            name: 'Streitaxt', type: 'axe', hand: 'right',
            damage: { light: 28, heavy: 60 }, staminaCost: { light: 18, heavy: 40 },
            speed: { light: 0.55, heavy: 1.1 }, range: 2.5, element: null, special: 'armor_break'
        },
        executioner_axe: {
            name: 'Henkeraxt', type: 'axe', hand: 'both',
            damage: { light: 40, heavy: 95 }, staminaCost: { light: 30, heavy: 60 },
            speed: { light: 0.9, heavy: 1.8 }, range: 3.0, element: null, special: 'execute', critChance: 0.3
        },
        frost_axe: {
            name: 'Frostaxt', type: 'axe', hand: 'right',
            damage: { light: 25, heavy: 55 }, staminaCost: { light: 18, heavy: 38 },
            speed: { light: 0.55, heavy: 1.1 }, range: 2.5, element: 'ice', special: 'freeze'
        },

        // ==================== HÄMMER (3) ====================
        wooden_hammer: {
            name: 'Holzhammer', type: 'hammer', hand: 'right',
            damage: { light: 20, heavy: 50 }, staminaCost: { light: 18, heavy: 40 },
            speed: { light: 0.6, heavy: 1.2 }, range: 2.0, element: null, special: 'stun'
        },
        war_hammer: {
            name: 'Kriegshammer', type: 'hammer', hand: 'both',
            damage: { light: 35, heavy: 85 }, staminaCost: { light: 28, heavy: 55 },
            speed: { light: 0.8, heavy: 1.6 }, range: 2.8, element: null, special: 'crush'
        },
        thunder_hammer: {
            name: 'Donnerhammer', type: 'hammer', hand: 'both',
            damage: { light: 30, heavy: 75 }, staminaCost: { light: 25, heavy: 50 },
            speed: { light: 0.75, heavy: 1.5 }, range: 3.0, element: 'lightning', special: 'thunder_strike'
        },

        // ==================== SPEERE (3) ====================
        wooden_spear: {
            name: 'Holzspeer', type: 'spear', hand: 'both',
            damage: { light: 14, heavy: 35 }, staminaCost: { light: 10, heavy: 25 },
            speed: { light: 0.35, heavy: 0.7 }, range: 4.5, element: null, special: 'thrust'
        },
        iron_spear: {
            name: 'Eisenspeer', type: 'spear', hand: 'both',
            damage: { light: 22, heavy: 50 }, staminaCost: { light: 12, heavy: 28 },
            speed: { light: 0.35, heavy: 0.7 }, range: 5.0, element: null, special: 'thrust'
        },
        trident: {
            name: 'Dreizack', type: 'spear', hand: 'both',
            damage: { light: 26, heavy: 58 }, staminaCost: { light: 14, heavy: 32 },
            speed: { light: 0.4, heavy: 0.8 }, range: 4.8, element: 'water', special: 'triple_hit'
        },

        // ==================== STÄBE (6) ====================
        wooden_staff: {
            name: 'Holzstab', type: 'staff', hand: 'left',
            damage: { light: 12, heavy: 35 }, staminaCost: { light: 8, heavy: 20 },
            manaCost: { light: 10, heavy: 25 }, speed: { light: 0.5, heavy: 1.2 },
            range: 8, element: 'arcane', special: null
        },
        fire_staff: {
            name: 'Feuerstab', type: 'staff', hand: 'left',
            damage: { light: 18, heavy: 50 }, staminaCost: { light: 5, heavy: 15 },
            manaCost: { light: 15, heavy: 35 }, speed: { light: 0.6, heavy: 1.5 },
            range: 10, element: 'fire', special: 'fireball_aoe'
        },
        ice_staff: {
            name: 'Eisstab', type: 'staff', hand: 'left',
            damage: { light: 15, heavy: 45 }, staminaCost: { light: 5, heavy: 15 },
            manaCost: { light: 12, heavy: 30 }, speed: { light: 0.55, heavy: 1.3 },
            range: 9, element: 'ice', special: 'freeze'
        },
        lightning_staff: {
            name: 'Blitzstab', type: 'staff', hand: 'left',
            damage: { light: 16, heavy: 42 }, staminaCost: { light: 5, heavy: 15 },
            manaCost: { light: 14, heavy: 32 }, speed: { light: 0.5, heavy: 1.2 },
            range: 12, element: 'lightning', special: 'chain_lightning'
        },
        necro_staff: {
            name: 'Nekromantenstab', type: 'staff', hand: 'left',
            damage: { light: 14, heavy: 40 }, staminaCost: { light: 6, heavy: 18 },
            manaCost: { light: 20, heavy: 50 }, speed: { light: 0.7, heavy: 1.6 },
            range: 8, element: 'shadow', special: 'raise_undead'
        },
        megumin_staff: {
            name: 'Megumins Explosionsstab', type: 'staff', hand: 'left',
            damage: { light: 5, heavy: 999 }, staminaCost: { light: 5, heavy: 100 },
            manaCost: { light: 5, heavy: 100 }, speed: { light: 0.3, heavy: 3.0 },
            range: 15, element: 'explosion', special: 'EXPLOSION'
        },

        // ==================== SCHILDE (4) ====================
        wooden_shield: {
            name: 'Holzschild', type: 'shield', hand: 'left',
            blockReduction: 0.5, parryWindow: 0.2, staminaCostBlock: 15, staminaCostParry: 20, stability: 30
        },
        iron_shield: {
            name: 'Eisenschild', type: 'shield', hand: 'left',
            blockReduction: 0.7, parryWindow: 0.18, staminaCostBlock: 12, staminaCostParry: 18, stability: 50
        },
        tower_shield: {
            name: 'Turmschild', type: 'shield', hand: 'left',
            blockReduction: 0.9, parryWindow: 0.1, staminaCostBlock: 8, staminaCostParry: 25, stability: 80
        },
        magic_shield: {
            name: 'Magieschild', type: 'shield', hand: 'left',
            blockReduction: 0.6, parryWindow: 0.25, staminaCostBlock: 10, staminaCostParry: 15, stability: 40,
            special: 'spell_reflect'
        },

        // ==================== FÄUSTE/HANDSCHUHE (4) ====================
        bare_fists: {
            name: 'Bloße Fäuste', type: 'fist', hand: 'both',
            damage: { light: 5, heavy: 12 }, staminaCost: { light: 3, heavy: 8 },
            speed: { light: 0.15, heavy: 0.3 }, range: 1.2, element: null, special: null
        },
        brass_knuckles: {
            name: 'Schlagring', type: 'fist', hand: 'both',
            damage: { light: 10, heavy: 22 }, staminaCost: { light: 5, heavy: 12 },
            speed: { light: 0.18, heavy: 0.35 }, range: 1.3, element: null, special: 'stun_chance'
        },
        combat_gloves: {
            name: 'Kampfhandschuhe', type: 'fist', hand: 'both',
            damage: { light: 14, heavy: 30 }, staminaCost: { light: 6, heavy: 15 },
            speed: { light: 0.16, heavy: 0.32 }, range: 1.4, element: null, special: 'combo_master'
        },
        titan_gauntlets: {
            name: 'Titanfäuste', type: 'fist', hand: 'both',
            damage: { light: 20, heavy: 45 }, staminaCost: { light: 10, heavy: 22 },
            speed: { light: 0.22, heavy: 0.45 }, range: 1.5, element: null, special: 'ground_pound'
        },

        // ==================== WESTERN WAFFEN (10) ====================
        // Revolver
        rusty_revolver: {
            name: 'Rostiger Revolver', type: 'gun', hand: 'right',
            damage: { light: 25, heavy: 50 }, staminaCost: { light: 5, heavy: 10 },
            speed: { light: 0.3, heavy: 0.8 }, range: 15, ammo: 6, reloadTime: 2.0,
            element: null, special: null
        },
        colt_peacemaker: {
            name: 'Colt Friedensstifter', type: 'gun', hand: 'right',
            damage: { light: 35, heavy: 70 }, staminaCost: { light: 5, heavy: 10 },
            speed: { light: 0.25, heavy: 0.6 }, range: 18, ammo: 6, reloadTime: 1.8,
            element: null, special: 'fan_the_hammer', critChance: 0.15
        },
        dual_revolvers: {
            name: 'Doppelte Revolver', type: 'gun', hand: 'both',
            damage: { light: 28, heavy: 55 }, staminaCost: { light: 8, heavy: 15 },
            speed: { light: 0.2, heavy: 0.5 }, range: 14, ammo: 12, reloadTime: 3.0,
            element: null, special: 'akimbo'
        },
        // Gewehre
        winchester_rifle: {
            name: 'Winchester Gewehr', type: 'rifle', hand: 'both',
            damage: { light: 45, heavy: 90 }, staminaCost: { light: 10, heavy: 20 },
            speed: { light: 0.8, heavy: 1.5 }, range: 30, ammo: 15, reloadTime: 2.5,
            element: null, special: 'lever_action'
        },
        sawed_off_shotgun: {
            name: 'Abgesägte Schrotflinte', type: 'shotgun', hand: 'right',
            damage: { light: 60, heavy: 120 }, staminaCost: { light: 15, heavy: 30 },
            speed: { light: 0.6, heavy: 1.2 }, range: 5, ammo: 2, reloadTime: 2.0,
            element: null, special: 'spread_shot'
        },
        long_shotgun: {
            name: 'Lange Schrotflinte', type: 'shotgun', hand: 'both',
            damage: { light: 50, heavy: 100 }, staminaCost: { light: 12, heavy: 25 },
            speed: { light: 0.7, heavy: 1.4 }, range: 8, ammo: 2, reloadTime: 2.2,
            element: null, special: 'slug_shot'
        },
        minigun: {
            name: 'Minigun', type: 'minigun', hand: 'both',
            damage: { light: 8, heavy: 8 }, staminaCost: { light: 2, heavy: 2 },
            speed: { light: 0.05, heavy: 0.05 }, range: 20, ammo: 200, reloadTime: 5.0,
            element: null, special: 'suppression', // Nur Status, kein Kill-Damage
            statusOnly: true // Macht keinen echten Schaden, nur Suppression/Fear
        },
        // Peitsche & Lasso
        whip: {
            name: 'Peitsche', type: 'whip', hand: 'right',
            damage: { light: 12, heavy: 25 }, staminaCost: { light: 8, heavy: 18 },
            speed: { light: 0.4, heavy: 0.8 }, range: 6.0, element: null, special: 'disarm'
        },
        lasso: {
            name: 'Lasso', type: 'lasso', hand: 'right',
            damage: { light: 0, heavy: 0 }, staminaCost: { light: 15, heavy: 30 },
            speed: { light: 0.6, heavy: 1.2 }, range: 10, element: null, special: 'capture'
        },
        dynamite: {
            name: 'Dynamit', type: 'throwable', hand: 'right',
            damage: { light: 80, heavy: 150 }, staminaCost: { light: 10, heavy: 20 },
            speed: { light: 1.5, heavy: 2.5 }, range: 12, ammo: 3, element: 'fire', special: 'aoe_explosion'
        },

        // ==================== BÖGEN (3) ====================
        wooden_bow: {
            name: 'Holzbogen', type: 'bow', hand: 'both',
            damage: { light: 18, heavy: 45 }, staminaCost: { light: 8, heavy: 20 },
            speed: { light: 0.5, heavy: 1.2 }, range: 25, ammo: 30, element: null, special: null
        },
        longbow: {
            name: 'Langbogen', type: 'bow', hand: 'both',
            damage: { light: 28, heavy: 65 }, staminaCost: { light: 12, heavy: 28 },
            speed: { light: 0.7, heavy: 1.5 }, range: 40, ammo: 20, element: null, special: 'piercing'
        },
        crossbow: {
            name: 'Armbrust', type: 'bow', hand: 'both',
            damage: { light: 40, heavy: 85 }, staminaCost: { light: 5, heavy: 12 },
            speed: { light: 1.0, heavy: 2.0 }, range: 35, ammo: 15, element: null, special: 'armor_pierce'
        },

        // ==================== KNÜPPEL (2) ====================
        wooden_club: {
            name: 'Holzknüppel', type: 'club', hand: 'right',
            damage: { light: 12, heavy: 28 }, staminaCost: { light: 8, heavy: 20 },
            speed: { light: 0.35, heavy: 0.7 }, range: 1.8, element: null, special: 'stun_chance'
        },
        spiked_club: {
            name: 'Stachelkeule', type: 'club', hand: 'right',
            damage: { light: 18, heavy: 40 }, staminaCost: { light: 12, heavy: 28 },
            speed: { light: 0.4, heavy: 0.8 }, range: 2.0, element: null, special: 'bleed'
        }
    };

    // ===== ARMOR DATABASE =====
    const ARMOR = {
        // HEAD
        cloth_hood: { slot: 'head', defense: 2, weight: 1, resist: { fire: 0, ice: 0, lightning: 0 } },
        iron_helm: { slot: 'head', defense: 8, weight: 5, resist: { fire: 5, ice: 5, lightning: -5 } },
        mage_hat: { slot: 'head', defense: 3, weight: 1, resist: { fire: 10, ice: 10, lightning: 10 }, manaBonus: 20 },

        // BODY
        cloth_robe: { slot: 'body', defense: 5, weight: 2, resist: { fire: 0, ice: 0, lightning: 0 }, manaBonus: 10 },
        leather_armor: { slot: 'body', defense: 12, weight: 6, resist: { fire: 5, ice: 5, lightning: 0 } },
        iron_plate: { slot: 'body', defense: 25, weight: 15, resist: { fire: 10, ice: -5, lightning: -10 } },
        gothic_lolita_dress: { slot: 'body', defense: 8, weight: 3, resist: { fire: 15, ice: 15, lightning: 15 }, manaBonus: 30, special: 'najika_boost' },

        // LEGS
        cloth_pants: { slot: 'legs', defense: 3, weight: 1, resist: { fire: 0, ice: 0, lightning: 0 } },
        leather_boots: { slot: 'legs', defense: 6, weight: 3, resist: { fire: 0, ice: 5, lightning: 0 }, speedBonus: 0.05 },
        iron_greaves: { slot: 'legs', defense: 15, weight: 10, resist: { fire: 5, ice: -5, lightning: -5 } }
    };

    // ===== COMBAT STATE =====
    const state = {
        // Player Stats
        hp: 100,
        maxHp: 100,
        stamina: 100,
        maxStamina: 100,
        mana: 50,
        maxMana: 50,

        // Equipment
        rightHand: 'rusty_sword',
        leftHand: 'wooden_staff',
        head: null,
        body: 'cloth_robe',
        legs: 'cloth_pants',

        // Combat State
        isAttacking: false,
        isBlocking: false,
        isParrying: false,
        isDodging: false,
        iFrames: false,
        comboCount: 0,
        lastAttackTime: 0,
        comboWindow: 800, // ms für Combo

        // Status Effects
        effects: [], // { type, duration, strength, startTime }

        // Cooldowns
        dodgeCooldown: 0,
        parryCooldown: 0,
        explosionUsedToday: false
    };

    // ===== STAMINA REGENERATION =====
    let staminaRegenInterval = null;

    function startStaminaRegen() {
        if (staminaRegenInterval) return;
        staminaRegenInterval = setInterval(() => {
            if (!state.isAttacking && !state.isBlocking && !state.isDodging) {
                state.stamina = Math.min(state.maxStamina, state.stamina + 2);
                updateUI();
            }
        }, 100);
    }

    // ===== ATTACK FUNCTIONS =====

    function attackLight(hand = 'right') {
        const weaponId = hand === 'right' ? state.rightHand : state.leftHand;
        const weapon = WEAPONS[weaponId];

        if (!weapon || state.isAttacking || state.isDodging) return null;
        if (state.stamina < weapon.staminaCost.light) {
            console.log('⚠️ Nicht genug Stamina!');
            return null;
        }
        if (weapon.manaCost && state.mana < weapon.manaCost.light) {
            console.log('⚠️ Nicht genug Mana!');
            return null;
        }

        state.isAttacking = true;
        state.stamina -= weapon.staminaCost.light;
        if (weapon.manaCost) state.mana -= weapon.manaCost.light;

        // Combo Check
        const now = Date.now();
        if (now - state.lastAttackTime < state.comboWindow) {
            state.comboCount++;
        } else {
            state.comboCount = 1;
        }
        state.lastAttackTime = now;

        // Damage Calculation
        let damage = weapon.damage.light;
        damage *= (1 + state.comboCount * 0.1); // +10% pro Combo

        // Crit Check
        if (weapon.critChance && Math.random() < weapon.critChance) {
            damage *= 2;
            console.log('💥 KRITISCHER TREFFER!');
        }

        // Attack Duration
        setTimeout(() => {
            state.isAttacking = false;
        }, weapon.speed.light * 1000);

        updateUI();

        return {
            damage: Math.floor(damage),
            element: weapon.element,
            special: weapon.special,
            range: weapon.range,
            hand,
            type: 'light',
            combo: state.comboCount
        };
    }

    function attackHeavy(hand = 'right') {
        const weaponId = hand === 'right' ? state.rightHand : state.leftHand;
        const weapon = WEAPONS[weaponId];

        if (!weapon || state.isAttacking || state.isDodging) return null;
        if (state.stamina < weapon.staminaCost.heavy) {
            console.log('⚠️ Nicht genug Stamina für Heavy Attack!');
            return null;
        }
        if (weapon.manaCost && state.mana < weapon.manaCost.heavy) {
            console.log('⚠️ Nicht genug Mana für Heavy Attack!');
            return null;
        }

        // EXPLOSION Special Check
        if (weapon.special === 'EXPLOSION') {
            if (state.explosionUsedToday) {
                console.log('💥 EXPLOSION bereits heute verwendet! Megumin muss sich erholen...');
                return null;
            }
            state.explosionUsedToday = true;
            console.log('💥💥💥 EXPLOSION!!! 💥💥💥');
        }

        state.isAttacking = true;
        state.stamina -= weapon.staminaCost.heavy;
        if (weapon.manaCost) state.mana -= weapon.manaCost.heavy;
        state.comboCount = 0; // Heavy resets combo

        let damage = weapon.damage.heavy;

        setTimeout(() => {
            state.isAttacking = false;
        }, weapon.speed.heavy * 1000);

        updateUI();

        return {
            damage: Math.floor(damage),
            element: weapon.element,
            special: weapon.special,
            range: weapon.range,
            hand,
            type: 'heavy',
            isExplosion: weapon.special === 'EXPLOSION'
        };
    }

    // ===== DUAL ATTACK (BEIDE HÄNDE GLEICHZEITIG!) =====

    function attackDual(isHeavy = false) {
        const rightWeapon = WEAPONS[state.rightHand];
        const leftWeapon = WEAPONS[state.leftHand];

        if (!rightWeapon || !leftWeapon) {
            console.log('⚠️ Brauche Waffen in BEIDEN Händen für Dual-Attack!');
            return null;
        }
        if (state.isAttacking || state.isDodging) return null;

        // Dual-Attack kostet Stamina von BEIDEN Waffen + 20% Aufschlag
        const attackType = isHeavy ? 'heavy' : 'light';
        const staminaCost = Math.floor(
            (rightWeapon.staminaCost[attackType] + leftWeapon.staminaCost[attackType]) * 1.2
        );

        if (state.stamina < staminaCost) {
            console.log('⚠️ Nicht genug Stamina für Dual-Attack!');
            return null;
        }

        // Mana-Check für magische Waffen
        const manaCost = ((rightWeapon.manaCost?.[attackType]) || 0) + ((leftWeapon.manaCost?.[attackType]) || 0);
        if (manaCost > 0 && state.mana < manaCost) {
            console.log('⚠️ Nicht genug Mana für Dual-Attack!');
            return null;
        }

        // EXPLOSION Check - beide Hände!
        if (rightWeapon.special === 'EXPLOSION' || leftWeapon.special === 'EXPLOSION') {
            if (state.explosionUsedToday) {
                console.log('💥 EXPLOSION bereits heute verwendet!');
                return null;
            }
            state.explosionUsedToday = true;
            console.log('💥💥💥 DOPPEL-EXPLOSION!!! 💥💥💥');
        }

        state.isAttacking = true;
        state.stamina -= staminaCost;
        if (manaCost > 0) state.mana -= manaCost;

        // Combo Check - Dual-Attacks zählen als 2 Hits!
        const now = Date.now();
        if (now - state.lastAttackTime < state.comboWindow) {
            state.comboCount += 2;
        } else {
            state.comboCount = 2;
        }
        state.lastAttackTime = now;

        // Schaden = Beide Waffen addiert + 30% Dual-Bonus
        let rightDmg = rightWeapon.damage[attackType];
        let leftDmg = leftWeapon.damage[attackType];

        // Crit Check - höhere Crit-Chance der beiden Waffen zählt
        const maxCrit = Math.max(rightWeapon.critChance || 0, leftWeapon.critChance || 0);
        let isCrit = false;
        if (maxCrit > 0 && Math.random() < maxCrit * 1.15) { // +15% Crit-Bonus bei Dual
            isCrit = true;
            console.log('💥💥 DOPPEL-KRIT!!!');
        }

        let totalDamage = Math.floor((rightDmg + leftDmg) * 1.3); // +30% Dual-Bonus
        if (isCrit) totalDamage *= 2;
        if (isHeavy) state.comboCount = 0; // Heavy Dual resets combo

        // Combo-Bonus
        totalDamage = Math.floor(totalDamage * (1 + state.comboCount * 0.1));

        // Skill XP - Learning by Doing! Beide Waffen leveln!
        gainSkillXP(rightWeapon.type, isHeavy ? 3 : 2);
        gainSkillXP(leftWeapon.type, isHeavy ? 3 : 2);

        // Langsamere Recovery - beide Waffen Speed addiert × 0.7
        const recoveryTime = (rightWeapon.speed[attackType] + leftWeapon.speed[attackType]) * 0.7 * 1000;
        setTimeout(() => {
            state.isAttacking = false;
        }, recoveryTime);

        updateUI();

        // Elemente sammeln (für Multi-Element Hits)
        const elements = [];
        if (rightWeapon.element) elements.push(rightWeapon.element);
        if (leftWeapon.element) elements.push(leftWeapon.element);

        console.log(`⚔️⚔️ DUAL ${isHeavy ? 'HEAVY' : 'LIGHT'}! ${totalDamage} Schaden! (R:${rightWeapon.name} + L:${leftWeapon.name})`);

        return {
            damage: totalDamage,
            element: elements.length > 0 ? elements[0] : null,
            elements: elements,
            special: rightWeapon.special || leftWeapon.special,
            range: Math.max(rightWeapon.range, leftWeapon.range),
            hand: 'both',
            type: isHeavy ? 'dual_heavy' : 'dual_light',
            combo: state.comboCount,
            isCrit,
            isDual: true
        };
    }

    // ===== DEFENSE FUNCTIONS =====

    function block() {
        const shieldId = state.leftHand;
        const shield = WEAPONS[shieldId];

        if (!shield || shield.type !== 'shield') {
            console.log('⚠️ Kein Schild ausgerüstet!');
            return false;
        }
        if (state.stamina < shield.staminaCostBlock) return false;

        state.isBlocking = true;
        return true;
    }

    function releaseBlock() {
        state.isBlocking = false;
    }

    function parry() {
        const shieldId = state.leftHand;
        const shield = WEAPONS[shieldId];

        if (!shield || shield.type !== 'shield') return false;
        if (state.stamina < shield.staminaCostParry) return false;
        if (state.parryCooldown > Date.now()) return false;

        state.isParrying = true;
        state.stamina -= shield.staminaCostParry;
        state.parryCooldown = Date.now() + 1000; // 1s Cooldown

        // Parry Window
        setTimeout(() => {
            state.isParrying = false;
        }, shield.parryWindow * 1000);

        updateUI();
        return true;
    }

    function dodge(direction = 'back') {
        if (state.isDodging || state.stamina < 25) return false;
        if (state.dodgeCooldown > Date.now()) return false;

        state.isDodging = true;
        state.iFrames = true;
        state.stamina -= 25;
        state.dodgeCooldown = Date.now() + 800; // 800ms Cooldown

        // i-Frames Duration (300ms)
        setTimeout(() => {
            state.iFrames = false;
        }, 300);

        // Dodge Duration (500ms)
        setTimeout(() => {
            state.isDodging = false;
        }, 500);

        updateUI();

        return {
            direction,
            distance: 5, // Units to move
            iFrameDuration: 300
        };
    }

    // ===== DAMAGE CALCULATION =====

    function takeDamage(incomingDamage, element = null) {
        if (state.iFrames) {
            console.log('🌀 Dodge! Kein Schaden!');
            return 0;
        }

        let finalDamage = incomingDamage;

        // Block Reduction
        if (state.isBlocking) {
            const shield = WEAPONS[state.leftHand];
            if (shield && shield.type === 'shield') {
                finalDamage *= (1 - shield.blockReduction);
                state.stamina -= Math.floor(incomingDamage * 0.3);
                console.log(`🛡️ Block! Reduziert auf ${Math.floor(finalDamage)} Schaden`);
            }
        }

        // Parry (vollständige Negation + Riposte Window)
        if (state.isParrying) {
            console.log('⚔️ PARRY! Riposte möglich!');
            return -1; // -1 = Successful Parry
        }

        // Armor Reduction
        const totalDefense = calculateTotalDefense();
        const armorReduction = totalDefense / (totalDefense + 100);
        finalDamage *= (1 - armorReduction);

        // Elemental Resistance
        if (element) {
            const resist = calculateElementResist(element);
            finalDamage *= (1 - resist / 100);
        }

        finalDamage = Math.floor(finalDamage);
        state.hp = Math.max(0, state.hp - finalDamage);

        updateUI();

        if (state.hp <= 0) {
            onDeath();
        }

        return finalDamage;
    }

    function calculateTotalDefense() {
        let defense = 0;
        if (state.head && ARMOR[state.head]) defense += ARMOR[state.head].defense;
        if (state.body && ARMOR[state.body]) defense += ARMOR[state.body].defense;
        if (state.legs && ARMOR[state.legs]) defense += ARMOR[state.legs].defense;
        return defense;
    }

    function calculateElementResist(element) {
        let resist = 0;
        ['head', 'body', 'legs'].forEach(slot => {
            const armorId = state[slot];
            if (armorId && ARMOR[armorId] && ARMOR[armorId].resist[element]) {
                resist += ARMOR[armorId].resist[element];
            }
        });
        return resist;
    }

    // ===== EQUIPMENT MANAGEMENT =====

    function equipWeapon(weaponId, hand = 'right') {
        if (!WEAPONS[weaponId]) {
            console.log(`❌ Waffe ${weaponId} nicht gefunden!`);
            return false;
        }

        const weapon = WEAPONS[weaponId];
        if (weapon.hand !== 'both' && weapon.hand !== hand) {
            console.log(`❌ ${weapon.name} kann nicht in ${hand === 'right' ? 'rechter' : 'linker'} Hand getragen werden!`);
            return false;
        }

        if (hand === 'right') {
            state.rightHand = weaponId;
        } else {
            state.leftHand = weaponId;
        }

        console.log(`✅ ${weapon.name} in ${hand === 'right' ? 'rechter' : 'linker'} Hand ausgerüstet`);
        updateUI();
        return true;
    }

    function equipArmor(armorId) {
        if (!ARMOR[armorId]) {
            console.log(`❌ Rüstung ${armorId} nicht gefunden!`);
            return false;
        }

        const armor = ARMOR[armorId];
        state[armor.slot] = armorId;

        console.log(`✅ ${armorId} ausgerüstet (${armor.slot})`);
        updateUI();
        return true;
    }

    // ===== STATUS EFFECTS =====

    function applyEffect(type, duration, strength) {
        state.effects.push({
            type,
            duration,
            strength,
            startTime: Date.now()
        });
        console.log(`🔮 Effekt: ${type} (${duration}s)`);
    }

    function processEffects() {
        const now = Date.now();
        state.effects = state.effects.filter(effect => {
            const elapsed = (now - effect.startTime) / 1000;
            if (elapsed >= effect.duration) {
                console.log(`✨ Effekt ${effect.type} beendet`);
                return false;
            }

            // Apply Effect
            switch (effect.type) {
                case 'burn':
                    state.hp = Math.max(0, state.hp - effect.strength * 0.1);
                    break;
                case 'poison':
                    state.hp = Math.max(0, state.hp - effect.strength * 0.05);
                    break;
                case 'regen':
                    state.hp = Math.min(state.maxHp, state.hp + effect.strength * 0.1);
                    break;
            }
            return true;
        });
    }

    // ===== EVENT HANDLERS =====

    function onDeath() {
        console.log('💀 Du bist gestorben!');
        // Trigger death event for game system
        if (window.dispatchEvent) {
            window.dispatchEvent(new CustomEvent('playerDeath', { detail: state }));
        }
    }

    // ===== UI UPDATE =====

    function updateUI() {
        // Update HP Bar
        const hpBar = document.getElementById('combat-hp-bar');
        const hpText = document.getElementById('combat-hp-text');
        if (hpBar) hpBar.style.width = `${(state.hp / state.maxHp) * 100}%`;
        if (hpText) hpText.textContent = `${state.hp}/${state.maxHp}`;

        // Update Stamina Bar
        const staminaBar = document.getElementById('combat-stamina-bar');
        if (staminaBar) staminaBar.style.width = `${(state.stamina / state.maxStamina) * 100}%`;

        // Update Mana Bar
        const manaBar = document.getElementById('combat-mana-bar');
        if (manaBar) manaBar.style.width = `${(state.mana / state.maxMana) * 100}%`;

        // Update Combo Counter
        const comboEl = document.getElementById('combat-combo');
        if (comboEl) {
            if (state.comboCount > 1) {
                comboEl.textContent = `${state.comboCount}x COMBO!`;
                comboEl.style.display = 'block';
            } else {
                comboEl.style.display = 'none';
            }
        }
    }

    // ===== INITIALIZATION =====

    function init() {
        console.log('⚔️ Equipment Combat System initialized');
        startStaminaRegen();

        // Effect Processing Loop
        setInterval(processEffects, 100);

        // Create Combat UI if not exists
        createCombatUI();
    }

    function createCombatUI() {
        if (document.getElementById('combat-ui')) return;

        const ui = document.createElement('div');
        ui.id = 'combat-ui';
        ui.innerHTML = `
            <div class="combat-bars">
                <div class="combat-bar hp">
                    <div class="bar-fill" id="combat-hp-bar"></div>
                    <span class="bar-text" id="combat-hp-text">${state.hp}/${state.maxHp}</span>
                </div>
                <div class="combat-bar stamina">
                    <div class="bar-fill" id="combat-stamina-bar"></div>
                </div>
                <div class="combat-bar mana">
                    <div class="bar-fill" id="combat-mana-bar"></div>
                </div>
            </div>
            <div class="combat-combo" id="combat-combo" style="display:none;"></div>
        `;

        const style = document.createElement('style');
        style.textContent = `
            #combat-ui { position: fixed; top: 55px; left: 50%; transform: translateX(-50%); z-index: 999; }
            .combat-bars { display: flex; flex-direction: row; gap: 8px; background: rgba(0,0,0,0.7); padding: 6px 12px; border-radius: 8px; }
            .combat-bar { width: 150px; height: 18px; background: #222; border-radius: 3px; position: relative; overflow: hidden; border: 1px solid #444; }
            .combat-bar .bar-fill { height: 100%; transition: width 0.2s; }
            .combat-bar.hp .bar-fill { background: linear-gradient(90deg, #ff4444, #ff6666); }
            .combat-bar.stamina .bar-fill { background: linear-gradient(90deg, #44ff44, #66ff66); width: 100%; }
            .combat-bar.mana .bar-fill { background: linear-gradient(90deg, #4444ff, #6666ff); width: 100%; }
            .combat-bar .bar-text { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 11px; color: white; text-shadow: 1px 1px 2px black; font-weight: bold; }
            .combat-combo { position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 32px; color: #FFD700; text-shadow: 2px 2px 4px black; animation: comboPulse 0.3s ease-out; }
            @keyframes comboPulse { 0% { transform: translate(-50%, -50%) scale(1.5); } 100% { transform: translate(-50%, -50%) scale(1); } }
        `;
        document.head.appendChild(style);
        document.body.appendChild(ui);

        updateUI();
    }

    // ===== USE-BASED SKILL PROGRESSION =====
    const skillProgress = {
        // ========== WAFFEN-SKILLS (alle leveln durch Nutzung) ==========
        sword: { level: 1, xp: 0, xpNeeded: 100 },
        dagger: { level: 1, xp: 0, xpNeeded: 80 },
        axe: { level: 1, xp: 0, xpNeeded: 120 },
        hammer: { level: 1, xp: 0, xpNeeded: 130 },
        spear: { level: 1, xp: 0, xpNeeded: 110 },
        staff: { level: 1, xp: 0, xpNeeded: 100 },
        shield: { level: 1, xp: 0, xpNeeded: 90 },
        fist: { level: 1, xp: 0, xpNeeded: 70 },       // Brawler/Wrestling
        bow: { level: 1, xp: 0, xpNeeded: 100 },
        club: { level: 1, xp: 0, xpNeeded: 80 },
        // Western Waffen
        gun: { level: 1, xp: 0, xpNeeded: 120 },      // Revolver
        rifle: { level: 1, xp: 0, xpNeeded: 140 },
        shotgun: { level: 1, xp: 0, xpNeeded: 130 },
        whip: { level: 1, xp: 0, xpNeeded: 100 },
        lasso: { level: 1, xp: 0, xpNeeded: 90 },

        // ========== KAMPF-SKILLS ==========
        dodge: { level: 1, xp: 0, xpNeeded: 50 },
        parry: { level: 1, xp: 0, xpNeeded: 80 },
        block: { level: 1, xp: 0, xpNeeded: 60 },
        combo: { level: 1, xp: 0, xpNeeded: 120 },
        // Wrestling/Griffe (Brawler)
        grab: { level: 1, xp: 0, xpNeeded: 100 },     // Greifen
        throw: { level: 1, xp: 0, xpNeeded: 120 },    // Würfe
        suplex: { level: 1, xp: 0, xpNeeded: 200 },   // Wrestling-Moves
        environment: { level: 1, xp: 0, xpNeeded: 150 }, // Umgebungs-Nutzung

        // ========== MAGIESCHULEN (Skyrim-basiert + erweitert) ==========
        // Zerstörungsmagie
        fire: { level: 1, xp: 0, xpNeeded: 150 },
        ice: { level: 1, xp: 0, xpNeeded: 150 },
        lightning: { level: 1, xp: 0, xpNeeded: 150 },
        // Wiederherstellung
        restoration: { level: 1, xp: 0, xpNeeded: 180 },  // Heilung, Wards
        // Illusion
        illusion: { level: 1, xp: 0, xpNeeded: 200 },    // Unsichtbar, Angst, Charm
        // Beschwörung
        conjuration: { level: 1, xp: 0, xpNeeded: 220 }, // Dämonen, Waffen beschwören
        // Veränderung
        alteration: { level: 1, xp: 0, xpNeeded: 180 },  // Rüstungs-Zauber, Telekinese
        // Nekromantie (eigene Schule!)
        necromancy: { level: 1, xp: 0, xpNeeded: 250 },  // Untote erheben, Lebensraub
        // Gift (eigene Schule!)
        poison: { level: 1, xp: 0, xpNeeded: 160 },      // Gift-Magie, DoT, Debuffs
        // Natur/Wasser (Konosuba - Aqua)
        water: { level: 1, xp: 0, xpNeeded: 150 },       // Reinigung, Wasser-Magie
        // Schatten
        shadow: { level: 1, xp: 0, xpNeeded: 200 },      // Schatten-Magie
        // Arkane
        arcane: { level: 1, xp: 0, xpNeeded: 170 },      // Basis-Magie
        // EXPLOSION (STANDALONE - Megumin-Klasse!)
        explosion: { level: 1, xp: 0, xpNeeded: 500 }    // Nie mit anderen kombinieren!
    };

    // ========== 1-SKILL-WEG SYSTEM ==========
    // Wenn aktiviert: +300% in EINEM Skill, -90% in ALLEN anderen
    const oneSkillPath = {
        active: false,
        chosenSkill: null,
        confirmedPermanent: false  // Nach Quest ist es permanent!
    };

    function activateOneSkillPath(skillName) {
        if (oneSkillPath.confirmedPermanent) {
            console.log('❌ 1-Skill-Weg bereits permanent gewählt!');
            return false;
        }
        if (!skillProgress[skillName]) {
            console.log(`❌ Skill ${skillName} existiert nicht!`);
            return false;
        }
        oneSkillPath.active = true;
        oneSkillPath.chosenSkill = skillName;
        console.log(`⚠️ 1-SKILL-WEG AKTIVIERT: ${skillName.toUpperCase()}`);
        console.log('💥 +300% Bonus in diesem Skill, -90% in allen anderen!');
        saveOneSkillPath();
        return true;
    }

    function confirmOneSkillPathPermanent() {
        if (!oneSkillPath.active) return false;
        oneSkillPath.confirmedPermanent = true;
        console.log('🔒 1-SKILL-WEG IST JETZT PERMANENT!');
        console.log('⚠️ Kein Zurück möglich! Nur Charakter-Löschung!');
        saveOneSkillPath();
        return true;
    }

    function getOneSkillBonus(skillName) {
        if (!oneSkillPath.active) return 1.0;
        if (skillName === oneSkillPath.chosenSkill) {
            return 4.0; // +300% = 4x
        }
        return 0.1; // -90% = 0.1x
    }

    function saveOneSkillPath() {
        localStorage.setItem('najika_one_skill_path', JSON.stringify(oneSkillPath));
    }

    function loadOneSkillPath() {
        const saved = localStorage.getItem('najika_one_skill_path');
        if (saved) {
            const loaded = JSON.parse(saved);
            Object.assign(oneSkillPath, loaded);
            if (oneSkillPath.active) {
                console.log(`✅ 1-Skill-Weg geladen: ${oneSkillPath.chosenSkill}`);
            }
        }
    }

    // ========== GLÜCK & CHARM STATS ==========
    const playerStats = {
        luck: 10,       // Basis 10, beeinflusst Crit, Drops, Fischen, etc.
        charm: 10,      // Basis 10, beeinflusst NPCs, Preise, Dialog-Optionen
        strength: 10,   // Physischer Schaden
        intelligence: 10, // Magie-Schaden
        agility: 10,    // Bewegung, Dodge-Bonus
        endurance: 10   // Max Stamina, Regen
    };

    function getLuckBonus() {
        return 1 + (playerStats.luck - 10) * 0.02; // +2% pro Punkt über 10
    }

    function getCharmBonus() {
        return 1 + (playerStats.charm - 10) * 0.02;
    }

    // ========== TIDS (Tritt In Den Schritt) - GAG MOVE ==========
    const tidsState = {
        lastUsed: 0,
        cooldownMs: 24 * 60 * 60 * 1000 // 24 Stunden
    };

    function useTIDS(targetType = 'humanoid') {
        const now = Date.now();
        if (now - tidsState.lastUsed < tidsState.cooldownMs) {
            const remaining = Math.ceil((tidsState.cooldownMs - (now - tidsState.lastUsed)) / 3600000);
            console.log(`⏰ TIDS Cooldown! Noch ${remaining} Stunden.`);
            return null;
        }

        if (targetType !== 'humanoid') {
            console.log('🤷 TIDS funktioniert nur bei humanoiden Gegnern!');
            return null;
        }

        tidsState.lastUsed = now;
        localStorage.setItem('najika_tids_last', tidsState.lastUsed.toString());

        console.log('🦵 TIDS! Tritt in den Schritt! 🎯');
        console.log('💫 Gegner ist 3 Sekunden gestunnt!');
        console.log('🏃 +90% Flucht-Chance für 5 Sekunden!');

        // Broadcast für andere Spieler (PvP Gag)
        if (window.dispatchEvent) {
            window.dispatchEvent(new CustomEvent('tidsUsed', {
                detail: { attacker: 'player', effect: 'stun', duration: 3000 }
            }));
        }

        return {
            damage: 1, // Symbolisch
            stun: 3000, // 3 Sekunden
            fleeBonus: 0.9, // +90% Flucht
            fleeDuration: 5000, // 5 Sekunden
            isGag: true
        };
    }

    function loadTIDSState() {
        const saved = localStorage.getItem('najika_tids_last');
        if (saved) {
            tidsState.lastUsed = parseInt(saved);
        }
    }

    // ========== WRESTLING / GRIFF-SYSTEM ==========
    const grabState = {
        isGrabbing: false,
        grabbedTarget: null,
        grabStartTime: 0
    };

    function grab() {
        if (state.isAttacking || state.isDodging || grabState.isGrabbing) return null;
        if (state.stamina < 20) {
            console.log('⚠️ Nicht genug Stamina zum Greifen!');
            return null;
        }

        // Skill-Check basierend auf grab Level
        const grabSkill = skillProgress.grab?.level || 1;
        const successChance = 0.5 + grabSkill * 0.02; // 50% + 2% pro Level

        if (Math.random() > successChance) {
            console.log('❌ Griff verfehlt!');
            state.stamina -= 10;
            return null;
        }

        grabState.isGrabbing = true;
        grabState.grabStartTime = Date.now();
        state.stamina -= 20;

        gainSkillXP('grab', 15);
        gainSkillXP('fist', 5);

        console.log('🤼 Gegner gegriffen! Wähle Follow-Up:');
        console.log('  [1] Suplex (Shift+1)');
        console.log('  [2] Chokeslam (Shift+2)');
        console.log('  [3] In Objekt werfen (Shift+3)');
        console.log('  [4] Loslassen (Shift+4)');

        return { grabbed: true, options: ['suplex', 'chokeslam', 'throw_object', 'release'] };
    }

    function executeGrabMove(move) {
        if (!grabState.isGrabbing) return null;

        let result = null;
        const fistBonus = getSkillBonus('fist');
        const oneSkillMult = getOneSkillBonus('fist');

        switch (move) {
            case 'suplex':
                if (skillProgress.suplex?.level < 15) {
                    console.log('❌ Suplex benötigt Suplex-Skill Level 15!');
                    break;
                }
                result = {
                    damage: Math.floor(50 * fistBonus * oneSkillMult),
                    type: 'suplex',
                    stun: 2000
                };
                gainSkillXP('suplex', 25);
                gainSkillXP('throw', 15);
                console.log('💥 SUPLEX! Massiver Schaden!');
                break;

            case 'chokeslam':
                if (skillProgress.throw?.level < 10) {
                    console.log('❌ Chokeslam benötigt Wurf-Skill Level 10!');
                    break;
                }
                result = {
                    damage: Math.floor(40 * fistBonus * oneSkillMult),
                    type: 'chokeslam',
                    groundedDuration: 3000
                };
                gainSkillXP('throw', 20);
                console.log('💥 CHOKESLAM! Gegner am Boden!');
                break;

            case 'throw_object':
                // Wirft Gegner in nahes Objekt (Fass, Tisch, etc.)
                result = {
                    damage: Math.floor(30 * fistBonus * oneSkillMult),
                    type: 'environment_throw',
                    bonusDamage: 20, // Extra wenn Objekt trifft
                    critVulnerable: 3000 // 3s extra Crit-Anfälligkeit
                };
                gainSkillXP('throw', 15);
                gainSkillXP('environment', 20);
                console.log('💥 In Objekt geworfen! +Crit Verwundbarkeit!');
                break;

            case 'release':
                console.log('👋 Gegner losgelassen.');
                break;
        }

        grabState.isGrabbing = false;
        grabState.grabbedTarget = null;
        return result;
    }

    // ========== UMGEBUNGS-INTERAKTION (Wrestling-Style) ==========
    const environmentObjects = {
        barrel: { damage: 20, effect: 'stun', duration: 1500 },
        table: { damage: 35, effect: 'grounded', duration: 2000 },
        chair: { damage: 15, effect: null, uses: 3 },
        wall: { damage: 0, effect: 'wall_jump', speedBonus: 1.5 },
        fire: { damage: 10, effect: 'burn', duration: 5000 },
        chandelier: { damage: 25, effect: 'knockdown', aoe: true }
    };

    function useEnvironmentObject(objectType, action = 'throw') {
        const obj = environmentObjects[objectType];
        if (!obj) {
            console.log(`❌ Objekt-Typ ${objectType} nicht nutzbar!`);
            return null;
        }

        // Skill-Check
        const envSkill = skillProgress.environment?.level || 1;
        const agilityBonus = (playerStats.agility - 10) * 0.01;
        const successChance = 0.4 + envSkill * 0.03 + agilityBonus;

        if (Math.random() > successChance) {
            console.log(`❌ Umgebungs-Aktion fehlgeschlagen! (${Math.floor(successChance * 100)}% Chance)`);
            // Kann nach hinten losgehen!
            if (Math.random() < 0.3) {
                console.log('💥 Es ging nach hinten los! Du nimmst Schaden!');
                state.hp -= 10;
                updateUI();
            }
            return null;
        }

        gainSkillXP('environment', 20);

        let result = {
            objectType,
            action,
            damage: obj.damage,
            effect: obj.effect,
            duration: obj.duration
        };

        switch (action) {
            case 'wall_jump':
                console.log('🧱 Von Wand abgestoßen! +50% nächster Angriff!');
                result.nextAttackBonus = 1.5;
                break;
            case 'throw':
                console.log(`🪣 ${objectType} geworfen! ${obj.damage} Schaden!`);
                break;
            case 'slam':
                console.log(`🪑 Gegner in ${objectType} geschleudert!`);
                result.damage *= 1.5;
                break;
        }

        return result;
    }

    function wallJump() {
        // Prüfe ob Wand in der Nähe
        const envSkill = skillProgress.environment?.level || 1;
        if (envSkill < 5) {
            console.log('❌ Wand-Abstoß benötigt Environment-Skill Level 5!');
            return null;
        }

        if (state.stamina < 15) {
            console.log('⚠️ Nicht genug Stamina!');
            return null;
        }

        state.stamina -= 15;
        gainSkillXP('environment', 10);

        console.log('🧱 Von Wand abgestoßen! Nächster Angriff +50%!');
        return { wallJump: true, nextAttackBonus: 1.5, duration: 3000 };
    }

    function gainSkillXP(skillName, amount) {
        if (!skillProgress[skillName]) return;

        const skill = skillProgress[skillName];
        skill.xp += amount;

        // Level Up Check
        while (skill.xp >= skill.xpNeeded) {
            skill.xp -= skill.xpNeeded;
            skill.level++;
            skill.xpNeeded = Math.floor(skill.xpNeeded * 1.5); // Exponentiell

            console.log(`🎉 ${skillName.toUpperCase()} LEVEL UP! → Level ${skill.level}`);

            if (typeof showNotification === 'function') {
                showNotification(`🎉 ${skillName} Level ${skill.level}!`);
            }
        }

        // Save to localStorage
        saveSkillProgress();
    }

    function getSkillBonus(skillName) {
        if (!skillProgress[skillName]) return 1.0;
        // +5% Bonus pro Level
        return 1 + (skillProgress[skillName].level - 1) * 0.05;
    }

    function saveSkillProgress() {
        localStorage.setItem('najika_combat_skills', JSON.stringify(skillProgress));
    }

    function loadSkillProgress() {
        const saved = localStorage.getItem('najika_combat_skills');
        if (saved) {
            const loaded = JSON.parse(saved);
            Object.keys(loaded).forEach(key => {
                if (skillProgress[key]) {
                    skillProgress[key] = loaded[key];
                }
            });
            console.log('✅ Combat Skills geladen:', skillProgress);
        }
    }

    // Modify attackLight to gain XP
    const originalAttackLight = attackLight;
    attackLight = function(hand = 'right') {
        const result = originalAttackLight(hand);
        if (result) {
            const weapon = WEAPONS[hand === 'right' ? state.rightHand : state.leftHand];
            if (weapon) {
                gainSkillXP(weapon.type, 5); // +5 XP pro Light Attack
                if (weapon.element) gainSkillXP(weapon.element, 2);
            }
            if (result.combo > 2) gainSkillXP('combo', result.combo);

            // Apply skill bonus to damage
            result.damage = Math.floor(result.damage * getSkillBonus(weapon?.type || 'sword'));
        }
        return result;
    };

    // Modify attackHeavy to gain XP
    const originalAttackHeavy = attackHeavy;
    attackHeavy = function(hand = 'right') {
        const result = originalAttackHeavy(hand);
        if (result) {
            const weapon = WEAPONS[hand === 'right' ? state.rightHand : state.leftHand];
            if (weapon) {
                gainSkillXP(weapon.type, 15); // +15 XP pro Heavy Attack
                if (weapon.element) gainSkillXP(weapon.element, 8);
            }
            if (result.isExplosion) gainSkillXP('explosion', 50);

            // Apply skill bonus to damage
            result.damage = Math.floor(result.damage * getSkillBonus(weapon?.type || 'sword'));
        }
        return result;
    };

    // Modify dodge to gain XP
    const originalDodge = dodge;
    dodge = function(direction = 'back') {
        const result = originalDodge(direction);
        if (result) {
            gainSkillXP('dodge', 10);
        }
        return result;
    };

    // Modify parry to gain XP
    const originalParry = parry;
    parry = function() {
        const result = originalParry();
        if (result) {
            gainSkillXP('parry', 20); // Parry ist schwerer → mehr XP
        }
        return result;
    };

    // ===== KEYBOARD CONTROLS =====
    function setupKeyboardControls() {
        document.addEventListener('keydown', (e) => {
            // Ignoriere wenn Chat-Input oder andere Input-Felder fokussiert sind
            if (window.chatInputFocused) return;
            const active = document.activeElement;
            if (active && (active.tagName === 'INPUT' || active.tagName === 'TEXTAREA' || active.isContentEditable)) return;

            switch (e.code) {
                // Q = Linke Hand
                case 'KeyQ':
                    if (e.shiftKey) {
                        attackHeavy('left');
                        console.log('🔮 Heavy Attack (Linke Hand)');
                    } else {
                        attackLight('left');
                        console.log('🔮 Light Attack (Linke Hand)');
                    }
                    e.preventDefault();
                    break;

                // E = Rechte Hand (NUR wenn nicht in der Nähe eines Gebäudes!)
                case 'KeyE':
                    // WICHTIG: E wird auch für Gebäude-Interaktion verwendet
                    // Wenn nearBuilding existiert (aus 3d_scene.js), nicht attackieren
                    if (window.nearBuilding) {
                        // Lass 3d_scene.js die Interaktion übernehmen
                        return;
                    }
                    if (e.shiftKey) {
                        attackHeavy('right');
                        console.log('⚔️ Heavy Attack (Rechte Hand)');
                    } else {
                        attackLight('right');
                        console.log('⚔️ Light Attack (Rechte Hand)');
                    }
                    e.preventDefault();
                    break;

                // F = Parry
                case 'KeyF':
                    parry();
                    console.log('🛡️ Parry!');
                    e.preventDefault();
                    break;

                // Space = Dodge
                case 'Space':
                    if (!e.repeat) {
                        dodge('back');
                        console.log('🌀 Dodge!');
                        e.preventDefault();
                    }
                    break;

                // Shift = Block (Hold)
                case 'ShiftLeft':
                case 'ShiftRight':
                    if (!e.repeat) {
                        block();
                        console.log('🛡️ Block Start');
                    }
                    break;

                // G = Grab (Wrestling)
                case 'KeyG':
                    grab();
                    e.preventDefault();
                    break;

                // 1-4 = Grab Moves (wenn gegriffen)
                case 'Digit1':
                    if (grabState.isGrabbing) executeGrabMove('suplex');
                    e.preventDefault();
                    break;
                case 'Digit2':
                    if (grabState.isGrabbing) executeGrabMove('chokeslam');
                    e.preventDefault();
                    break;
                case 'Digit3':
                    if (grabState.isGrabbing) executeGrabMove('throw_object');
                    e.preventDefault();
                    break;
                case 'Digit4':
                    if (grabState.isGrabbing) executeGrabMove('release');
                    e.preventDefault();
                    break;

                // T = TIDS (Gag-Move)
                case 'KeyT':
                    useTIDS('humanoid');
                    e.preventDefault();
                    break;

                // V = Wall Jump
                case 'KeyV':
                    wallJump();
                    e.preventDefault();
                    break;

                // B = Throw Barrel/Object
                case 'KeyB':
                    useEnvironmentObject('barrel', 'throw');
                    e.preventDefault();
                    break;
            }
        });

        document.addEventListener('keyup', (e) => {
            // Block Release
            if (e.code === 'ShiftLeft' || e.code === 'ShiftRight') {
                releaseBlock();
                console.log('🛡️ Block End');
            }
        });

        console.log('⌨️ Keyboard Controls aktiv: Q/E=Attack, Shift+Q/E=Heavy, F=Parry, Space=Dodge, Shift(hold)=Block');
        console.log('🤼 G=Grab, 1-4=Grab-Moves | T=TIDS | V=Wand | B=Fass werfen');
    }

    // ===== PUBLIC API =====
    window.EquipmentCombat = {
        // Basis-Kampf
        init,
        attackLight,
        attackHeavy,
        attackDual,
        block,
        releaseBlock,
        parry,
        dodge,
        takeDamage,
        equipWeapon,
        equipArmor,
        applyEffect,

        // State & Data Getters
        getState: () => ({ ...state }),
        getWeapons: () => WEAPONS,
        getArmor: () => ARMOR,
        getSkills: () => ({ ...skillProgress }),
        getSkillBonus,
        getPlayerStats: () => ({ ...playerStats }),
        getLuckBonus,
        getCharmBonus,

        // Healing & Resources
        heal: (amount) => { state.hp = Math.min(state.maxHp, state.hp + amount); updateUI(); },
        restoreMana: (amount) => { state.mana = Math.min(state.maxMana, state.mana + amount); updateUI(); },
        resetExplosion: () => { state.explosionUsedToday = false; },

        // 1-Skill-Weg System
        activateOneSkillPath,
        confirmOneSkillPathPermanent,
        getOneSkillPath: () => ({ ...oneSkillPath }),
        getOneSkillBonus,

        // Wrestling / Griff-System
        grab,
        executeGrabMove,
        getGrabState: () => ({ ...grabState }),

        // Umgebungs-Interaktion
        useEnvironmentObject,
        wallJump,
        getEnvironmentObjects: () => environmentObjects,

        // TIDS (Gag-Move)
        useTIDS,
        getTIDSCooldown: () => {
            const remaining = tidsState.cooldownMs - (Date.now() - tidsState.lastUsed);
            return remaining > 0 ? remaining : 0;
        },

        // Stats modifizieren
        modifyPlayerStat: (stat, amount) => {
            if (playerStats[stat] !== undefined) {
                playerStats[stat] += amount;
                console.log(`📊 ${stat}: ${playerStats[stat]}`);
                localStorage.setItem('najika_player_stats', JSON.stringify(playerStats));
            }
        },
        loadPlayerStats: () => {
            const saved = localStorage.getItem('najika_player_stats');
            if (saved) Object.assign(playerStats, JSON.parse(saved));
        }
    };

    // Auto-init when DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            loadSkillProgress();
            loadOneSkillPath();
            loadTIDSState();
            window.EquipmentCombat.loadPlayerStats();
            init();
            setupKeyboardControls();
        });
    } else {
        loadSkillProgress();
        loadOneSkillPath();
        loadTIDSState();
        window.EquipmentCombat.loadPlayerStats();
        init();
        setupKeyboardControls();
    }

    console.log('✅ Equipment Combat System loaded (ERWEITERT)');
    console.log('⌨️ Controls: Q/E=Attack, Shift+Q/E=Heavy, Q+E=Dual, Shift+Q+E=Dual Heavy, F=Parry/Grab, Space=Dodge, Shift(hold)=Block');
    console.log('🤼 Wrestling: G=Grab, 1-4=Grab-Moves');
    console.log('🦵 TIDS: T (1x/24h, nur Humanoide)');
    console.log('🧱 Umgebung: V=Wand-Abstoß, B=Objekt werfen');
})();
