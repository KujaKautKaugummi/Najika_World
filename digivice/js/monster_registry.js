/**
 * NAJIKA WORLD - MONSTER REGISTRY
 * ================================
 * Zentrale Monster-Datenbank für alle Biome
 *
 * 2 KREATUR-KATEGORIEN:
 *   category: 'lebend'  → Anime-NPCs mit Verstand, sprechen, Persönlichkeit
 *                         Können angeworben oder versklavt werden
 *                         Droppen SELTENE Ressourcen beim Töten
 *   category: 'vieh'    → Minecraft-Tiere ohne Verstand
 *                         Können GEZÄHMT werden (Füttern, Geduld)
 *                         Standard-Ressourcen (Fleisch, Milch, Eier)
 *
 * Starter Map (Götterfels): 8 Wesen + 3 Vieh pro Biom + Exklusive
 * Später (eigene Biom-Maps): 64 Wesen + 20 Vieh pro Biom
 *
 * Zeitstadt: Versteckt in der Spitze des Götterfels!
 */

(function() {
    'use strict';

    // ==========================================
    // MONSTER BASE STATS (Level-Skalierung)
    // ==========================================

    function calcStats(base, level) {
        const scale = 1 + (level - 1) * 0.15;
        return {
            hp: Math.floor(base.hp * scale),
            attack: Math.floor(base.attack * scale),
            defense: Math.floor(base.defense * scale),
            speed: base.speed,
            xpReward: Math.floor(base.xpReward * scale),
            goldDrop: Math.floor(base.goldDrop * scale),
        };
    }

    // ==========================================
    // MONSTER DATABASE
    // ==========================================

    const MONSTERS = {

        // ===== SAMTMOOS - Sanfte Hügel, Pilzwälder =====
        // -- Lebende (Anime-NPCs) --
        pilzling:          { name: 'Pilzling',          biome: 'samtmoos',     category: 'lebend', clan: 'pilz_volk',      tier: 1, hp: 30,  attack: 8,  defense: 3,  speed: 0.8, xpReward: 15,  goldDrop: 5,  icon: '🍄', lootTable: ['spore_dust', 'mushroom_cap'], rareDrop: 'leuchtspore' },
        mooswolf:          { name: 'Mooswolf',          biome: 'samtmoos',     category: 'lebend', clan: 'waldrudel',      tier: 2, hp: 55,  attack: 14, defense: 6,  speed: 1.3, xpReward: 30,  goldDrop: 12, icon: '🐺', lootTable: ['wolf_pelt', 'moss_clump'], rareDrop: 'mondstein_fang' },
        sporengeist:       { name: 'Sporengeist',       biome: 'samtmoos',     category: 'lebend', clan: 'pilz_volk',      tier: 2, hp: 40,  attack: 18, defense: 2,  speed: 1.0, xpReward: 35,  goldDrop: 15, icon: '👻', lootTable: ['ghost_essence', 'spore_dust'], rareDrop: 'geist_kristall' },
        wurzelkriecher:    { name: 'Wurzelkriecher',    biome: 'samtmoos',     category: 'lebend', clan: 'baumgeister',    tier: 1, hp: 45,  attack: 10, defense: 8,  speed: 0.5, xpReward: 20,  goldDrop: 8,  icon: '🌿', lootTable: ['root_fiber', 'earth_crystal'], rareDrop: 'uralte_wurzel' },
        schleimkroete:     { name: 'Schleimkröte',      biome: 'samtmoos',     category: 'lebend', clan: 'sumpfchor',      tier: 1, hp: 35,  attack: 12, defense: 4,  speed: 0.6, xpReward: 18,  goldDrop: 6,  icon: '🐸', lootTable: ['slime_glob', 'toad_skin'], rareDrop: 'goldene_zunge' },
        nachtmotte:        { name: 'Nachtmotte',        biome: 'samtmoos',     category: 'lebend', clan: 'nachtschwaermer', tier: 2, hp: 25,  attack: 16, defense: 2,  speed: 1.5, xpReward: 25,  goldDrop: 10, icon: '🦋', lootTable: ['moth_wing', 'night_dust'], rareDrop: 'mondstaub' },
        pilzgolem:         { name: 'Pilzgolem',         biome: 'samtmoos',     category: 'lebend', clan: 'pilz_volk',      tier: 3, hp: 120, attack: 20, defense: 15, speed: 0.4, xpReward: 60,  goldDrop: 30, icon: '🗿', lootTable: ['golem_core', 'mushroom_cap', 'earth_crystal'], rareDrop: 'lebender_stein' },
        faulige_ranke:     { name: 'Faulige Ranke',     biome: 'samtmoos',     category: 'lebend', clan: 'baumgeister',    tier: 2, hp: 50,  attack: 15, defense: 5,  speed: 0.3, xpReward: 28,  goldDrop: 11, icon: '🌱', lootTable: ['vine_whip', 'rot_essence'], rareDrop: 'faul_essenz' },
        // -- Vieh (Minecraft-Tiere, kein Verstand) --
        moos_kuh:          { name: 'Moos-Kuh',          biome: 'samtmoos',     category: 'vieh',   tier: 0, hp: 40,  attack: 2,  defense: 3,  speed: 0.4, xpReward: 5,   goldDrop: 2,  icon: '🐄', lootTable: ['fleisch', 'leder'], tameFood: 'gras', product: { type: 'milch', interval: 'daily' } },
        pilz_huhn:         { name: 'Pilz-Huhn',         biome: 'samtmoos',     category: 'vieh',   tier: 0, hp: 15,  attack: 1,  defense: 1,  speed: 0.6, xpReward: 3,   goldDrop: 1,  icon: '🐔', lootTable: ['fleisch', 'feder'], tameFood: 'pilz_koerner', product: { type: 'ei', interval: 'daily' } },
        wald_ziege:        { name: 'Wald-Ziege',        biome: 'samtmoos',     category: 'vieh',   tier: 0, hp: 30,  attack: 4,  defense: 2,  speed: 0.8, xpReward: 4,   goldDrop: 2,  icon: '🐐', lootTable: ['fleisch', 'leder', 'wolle'], tameFood: 'krauter', product: { type: 'wolle', interval: '3days' } },

        // ===== REICH DER DREI - Zivilisiert, Städte =====
        // -- Lebende (NPCs) --
        bandit:            { name: 'Bandit',            biome: 'reich_der_drei', category: 'lebend', clan: 'strassenbande',  tier: 1, hp: 40,  attack: 12, defense: 5,  speed: 1.1, xpReward: 20,  goldDrop: 15, icon: '🗡️', lootTable: ['stolen_goods', 'leather_scrap'], rareDrop: 'geheime_karte' },
        deserteur:         { name: 'Deserteur',         biome: 'reich_der_drei', category: 'lebend', clan: 'gesetzlose',     tier: 2, hp: 65,  attack: 16, defense: 10, speed: 1.0, xpReward: 40,  goldDrop: 25, icon: '⚔️', lootTable: ['military_badge', 'iron_scrap'], rareDrop: 'offizierssiegel' },
        rattenfaenger:     { name: 'Rattenfänger',      biome: 'reich_der_drei', category: 'lebend', clan: 'rattenfaenger',  tier: 2, hp: 35,  attack: 10, defense: 3,  speed: 0.9, xpReward: 25,  goldDrop: 18, icon: '🐀', lootTable: ['rat_tail', 'poison_vial'], rareDrop: 'gift_rezept' },
        kellerspinne:      { name: 'Kellerspinne',      biome: 'reich_der_drei', category: 'lebend', clan: 'netzweber',      tier: 1, hp: 30,  attack: 14, defense: 3,  speed: 1.2, xpReward: 18,  goldDrop: 8,  icon: '🕷️', lootTable: ['spider_silk', 'venom_sac'], rareDrop: 'goldene_seide' },
        strassenhund:      { name: 'Straßenhund',       biome: 'reich_der_drei', category: 'lebend', clan: 'strassenbande',  tier: 1, hp: 25,  attack: 10, defense: 2,  speed: 1.4, xpReward: 12,  goldDrop: 5,  icon: '🐕', lootTable: ['fur_scrap', 'bone'], rareDrop: 'treue_pfote' },
        schatten_dieb:     { name: 'Schatten-Dieb',     biome: 'reich_der_drei', category: 'lebend', clan: 'schattenkaeufer', tier: 3, hp: 45,  attack: 22, defense: 4,  speed: 1.6, xpReward: 55,  goldDrop: 40, icon: '🥷', lootTable: ['shadow_cloak', 'lockpick', 'stolen_goods'], rareDrop: 'meisterdieb_ring' },
        soeldner:          { name: 'Söldner',           biome: 'reich_der_drei', category: 'lebend', clan: 'soeldner_gilde', tier: 2, hp: 70,  attack: 18, defense: 12, speed: 0.9, xpReward: 45,  goldDrop: 30, icon: '🛡️', lootTable: ['mercenary_contract', 'iron_scrap'], rareDrop: 'soeldner_ehre' },
        gang_anfuehrer:    { name: 'Gang-Anführer',     biome: 'reich_der_drei', category: 'lebend', clan: 'strassenbande',  tier: 3, hp: 100, attack: 22, defense: 14, speed: 1.0, xpReward: 70,  goldDrop: 50, icon: '👑', lootTable: ['gang_signet', 'gold_tooth', 'stolen_goods'], rareDrop: 'gang_krone' },
        // -- Vieh --
        stadtkatze:        { name: 'Stadtkatze',        biome: 'reich_der_drei', category: 'vieh',   tier: 0, hp: 10,  attack: 2,  defense: 1,  speed: 1.3, xpReward: 2,   goldDrop: 1,  icon: '🐱', lootTable: ['fell'], tameFood: 'fisch', product: { type: 'gesellschaft', interval: 'passive' } },
        hofhund:           { name: 'Hofhund',           biome: 'reich_der_drei', category: 'vieh',   tier: 0, hp: 30,  attack: 8,  defense: 3,  speed: 1.2, xpReward: 3,   goldDrop: 1,  icon: '🐕', lootTable: ['fell', 'knochen'], tameFood: 'fleisch', product: { type: 'wache', interval: 'passive' } },
        stadt_huhn:        { name: 'Hofhuhn',           biome: 'reich_der_drei', category: 'vieh',   tier: 0, hp: 12,  attack: 1,  defense: 1,  speed: 0.5, xpReward: 2,   goldDrop: 1,  icon: '🐔', lootTable: ['fleisch', 'feder'], tameFood: 'koerner', product: { type: 'ei', interval: 'daily' } },

        // ===== HEISSE DÜNEN - Wüste, Sand =====
        // -- Lebende --
        sandwurm:          { name: 'Sandwurm',          biome: 'heisse_duenen', category: 'lebend', clan: 'wuermervolk',    tier: 3, hp: 110, attack: 24, defense: 12, speed: 0.7, xpReward: 65,  goldDrop: 35, icon: '🪱', lootTable: ['wurm_scale', 'sand_crystal'], rareDrop: 'wuermerkoenig_zahn' },
        wuestenskorpion:   { name: 'Wüstenskorpion',    biome: 'heisse_duenen', category: 'lebend', clan: 'skorpion_nest',  tier: 2, hp: 50,  attack: 18, defense: 10, speed: 1.0, xpReward: 35,  goldDrop: 15, icon: '🦂', lootTable: ['scorpion_tail', 'venom_sac'], rareDrop: 'gift_juwel' },
        sandsturm_geist:   { name: 'Sandsturm-Geist',   biome: 'heisse_duenen', category: 'lebend', clan: 'wuestengeister', tier: 2, hp: 40,  attack: 20, defense: 3,  speed: 1.4, xpReward: 40,  goldDrop: 20, icon: '🌪️', lootTable: ['sand_essence', 'wind_crystal'], rareDrop: 'sturm_herz' },
        duenenlaufer:      { name: 'Dünenläufer',       biome: 'heisse_duenen', category: 'lebend', clan: 'nomaden_bund',   tier: 2, hp: 55,  attack: 16, defense: 6,  speed: 1.5, xpReward: 35,  goldDrop: 18, icon: '🏃', lootTable: ['dune_leather', 'swift_dust'], rareDrop: 'windlaeufer_stiefel' },
        oasen_sirene:      { name: 'Oasen-Sirene',      biome: 'heisse_duenen', category: 'lebend', clan: 'oasen_wesen',    tier: 3, hp: 60,  attack: 22, defense: 5,  speed: 0.8, xpReward: 55,  goldDrop: 30, icon: '🧜', lootTable: ['siren_tear', 'mirage_crystal'], rareDrop: 'ewige_traene' },
        kaktus_golem:      { name: 'Kaktus-Golem',      biome: 'heisse_duenen', category: 'lebend', clan: 'wuestenwaechter', tier: 2, hp: 80,  attack: 14, defense: 18, speed: 0.3, xpReward: 40,  goldDrop: 20, icon: '🌵', lootTable: ['cactus_spine', 'golem_core'], rareDrop: 'lebender_kaktus' },
        hitze_phantom:     { name: 'Hitze-Phantom',     biome: 'heisse_duenen', category: 'lebend', clan: 'wuestengeister', tier: 2, hp: 35,  attack: 20, defense: 1,  speed: 1.3, xpReward: 30,  goldDrop: 15, icon: '🔥', lootTable: ['mirage_crystal', 'heat_essence'], rareDrop: 'fata_morgana' },
        sandraeuber:       { name: 'Sandräuber',        biome: 'heisse_duenen', category: 'lebend', clan: 'nomaden_bund',   tier: 1, hp: 45,  attack: 14, defense: 7,  speed: 1.1, xpReward: 22,  goldDrop: 20, icon: '🏴', lootTable: ['stolen_goods', 'dune_leather'], rareDrop: 'wuesten_kompass' },
        // -- Vieh --
        sand_kamel:        { name: 'Sandkamel',         biome: 'heisse_duenen', category: 'vieh',   tier: 0, hp: 60,  attack: 3,  defense: 5,  speed: 0.7, xpReward: 5,   goldDrop: 3,  icon: '🐫', lootTable: ['leder', 'fleisch'], tameFood: 'dattel', product: { type: 'reittier', interval: 'passive' } },
        duenen_echse:      { name: 'Dünen-Echse',       biome: 'heisse_duenen', category: 'vieh',   tier: 0, hp: 20,  attack: 3,  defense: 4,  speed: 1.0, xpReward: 3,   goldDrop: 2,  icon: '🦎', lootTable: ['leder', 'echsen_schuppe'], tameFood: 'insekt', product: { type: 'eier', interval: '3days' } },
        wuesten_hase:      { name: 'Wüstenhase',        biome: 'heisse_duenen', category: 'vieh',   tier: 0, hp: 10,  attack: 1,  defense: 1,  speed: 1.6, xpReward: 2,   goldDrop: 1,  icon: '🐰', lootTable: ['fleisch', 'fell'], tameFood: 'kaktus_frucht', product: { type: 'fell', interval: '3days' } },

        // ===== SALZWIND - Küste, Meer =====
        // -- Lebende --
        seemoeven_schwarm: { name: 'Seemöwen-Schwarm',  biome: 'salzwind',     category: 'lebend', clan: 'kuestenschwarm', tier: 1, hp: 20,  attack: 12, defense: 1,  speed: 1.6, xpReward: 15,  goldDrop: 5,  icon: '🐦', lootTable: ['feather', 'fish_bone'], rareDrop: 'sturmfeder' },
        strandkrabbe:      { name: 'Strandkrabbe',      biome: 'salzwind',     category: 'lebend', clan: 'krabbenvolk',   tier: 1, hp: 50,  attack: 15, defense: 14, speed: 0.6, xpReward: 22,  goldDrop: 10, icon: '🦀', lootTable: ['crab_shell', 'claw_piece'], rareDrop: 'perlen_panzer' },
        wellenschlag:      { name: 'Wellenschlag',      biome: 'salzwind',     category: 'lebend', clan: 'meeresgeister', tier: 2, hp: 60,  attack: 18, defense: 5,  speed: 1.0, xpReward: 38,  goldDrop: 18, icon: '🌊', lootTable: ['water_essence', 'sea_crystal'], rareDrop: 'gezeiten_stein' },
        piraten_geist:     { name: 'Piraten-Geist',     biome: 'salzwind',     category: 'lebend', clan: 'geisterflotte', tier: 3, hp: 75,  attack: 22, defense: 8,  speed: 1.1, xpReward: 55,  goldDrop: 40, icon: '☠️', lootTable: ['ghost_essence', 'pirate_coin', 'treasure_map'], rareDrop: 'kapitaens_kompass' },
        salzgolem:         { name: 'Salzgolem',         biome: 'salzwind',     category: 'lebend', clan: 'salzwaechter',  tier: 3, hp: 100, attack: 16, defense: 20, speed: 0.3, xpReward: 50,  goldDrop: 25, icon: '🧂', lootTable: ['salt_crystal', 'golem_core'], rareDrop: 'ewiges_salz' },
        nebelsirene:       { name: 'Nebelsirene',       biome: 'salzwind',     category: 'lebend', clan: 'meeresgeister', tier: 2, hp: 45,  attack: 20, defense: 3,  speed: 0.9, xpReward: 35,  goldDrop: 20, icon: '🌫️', lootTable: ['siren_tear', 'fog_essence'], rareDrop: 'sirenen_lied' },
        anker_revenant:    { name: 'Anker-Revenant',    biome: 'salzwind',     category: 'lebend', clan: 'geisterflotte', tier: 3, hp: 90,  attack: 25, defense: 12, speed: 0.5, xpReward: 60,  goldDrop: 35, icon: '⚓', lootTable: ['anchor_chain', 'revenant_soul'], rareDrop: 'geisterschiff_splitter' },
        gezeiten_schlange: { name: 'Gezeiten-Schlange', biome: 'salzwind',     category: 'lebend', clan: 'schlangennest', tier: 2, hp: 55,  attack: 17, defense: 6,  speed: 1.2, xpReward: 30,  goldDrop: 15, icon: '🐍', lootTable: ['snake_scale', 'sea_venom'], rareDrop: 'tide_fang' },
        // -- Vieh --
        strand_schaf:      { name: 'Strand-Schaf',      biome: 'salzwind',     category: 'vieh',   tier: 0, hp: 25,  attack: 2,  defense: 2,  speed: 0.5, xpReward: 3,   goldDrop: 2,  icon: '🐑', lootTable: ['fleisch', 'wolle'], tameFood: 'seetang', product: { type: 'salzwolle', interval: '3days' } },
        fisch_reiher:      { name: 'Fisch-Reiher',      biome: 'salzwind',     category: 'vieh',   tier: 0, hp: 15,  attack: 3,  defense: 1,  speed: 1.2, xpReward: 2,   goldDrop: 1,  icon: '🦩', lootTable: ['feder', 'fisch'], tameFood: 'fisch', product: { type: 'feder', interval: 'daily' } },
        muschel_schnecke:  { name: 'Muschel-Schnecke',  biome: 'salzwind',     category: 'vieh',   tier: 0, hp: 20,  attack: 0,  defense: 12, speed: 0.1, xpReward: 2,   goldDrop: 3,  icon: '🐌', lootTable: ['muschelschale', 'perle'], tameFood: 'algen', product: { type: 'perle', interval: '7days' } },

        // ===== MAGMASTRÖME - Vulkan, Feuer =====
        // -- Lebende --
        lava_schleim:      { name: 'Lava-Schleim',      biome: 'magmastroeme', category: 'lebend', clan: 'feuer_brut',     tier: 1, hp: 35,  attack: 16, defense: 5,  speed: 0.5, xpReward: 22,  goldDrop: 10, icon: '🟠', lootTable: ['lava_glob', 'fire_essence'], rareDrop: 'flammenherz' },
        feuerkaefer:       { name: 'Feuerkäfer',        biome: 'magmastroeme', category: 'lebend', clan: 'feuer_brut',     tier: 1, hp: 20,  attack: 20, defense: 2,  speed: 1.3, xpReward: 18,  goldDrop: 8,  icon: '🪲', lootTable: ['beetle_shell', 'fire_dust'], rareDrop: 'glut_panzer' },
        asche_golem:       { name: 'Asche-Golem',       biome: 'magmastroeme', category: 'lebend', clan: 'vulkan_waechter', tier: 3, hp: 120, attack: 20, defense: 18, speed: 0.3, xpReward: 65,  goldDrop: 30, icon: '🗿', lootTable: ['ash_core', 'golem_core', 'obsidian_shard'], rareDrop: 'ewige_glut' },
        magma_wurm:        { name: 'Magma-Wurm',        biome: 'magmastroeme', category: 'lebend', clan: 'magma_brut',     tier: 3, hp: 100, attack: 26, defense: 10, speed: 0.6, xpReward: 60,  goldDrop: 35, icon: '🐛', lootTable: ['magma_scale', 'fire_crystal'], rareDrop: 'vulkan_kern' },
        funken_elementar:  { name: 'Funken-Elementar',  biome: 'magmastroeme', category: 'lebend', clan: 'elementar_zirkel', tier: 2, hp: 50,  attack: 22, defense: 4,  speed: 1.2, xpReward: 40,  goldDrop: 20, icon: '✨', lootTable: ['spark_essence', 'fire_crystal'], rareDrop: 'reine_flamme' },
        obsidian_ritter:   { name: 'Obsidian-Ritter',   biome: 'magmastroeme', category: 'lebend', clan: 'vulkan_waechter', tier: 3, hp: 130, attack: 24, defense: 22, speed: 0.4, xpReward: 75,  goldDrop: 45, icon: '🗡️', lootTable: ['obsidian_shard', 'knight_sigil', 'fire_crystal'], rareDrop: 'ritter_ehre' },
        flammen_imp:       { name: 'Flammen-Imp',       biome: 'magmastroeme', category: 'lebend', clan: 'feuer_brut',     tier: 1, hp: 25,  attack: 14, defense: 2,  speed: 1.5, xpReward: 15,  goldDrop: 8,  icon: '😈', lootTable: ['imp_horn', 'fire_dust'], rareDrop: 'teufelszunge' },
        vulkan_drake:      { name: 'Vulkan-Drake',      biome: 'magmastroeme', category: 'lebend', clan: 'drachen_hort',   tier: 3, hp: 150, attack: 28, defense: 15, speed: 1.0, xpReward: 85,  goldDrop: 50, icon: '🐉', lootTable: ['drake_scale', 'fire_crystal', 'dragon_tooth'], rareDrop: 'drachen_traene' },
        // -- Vieh --
        vulkan_bock:       { name: 'Vulkan-Bock',       biome: 'magmastroeme', category: 'vieh',   tier: 0, hp: 40,  attack: 5,  defense: 6,  speed: 0.6, xpReward: 4,   goldDrop: 2,  icon: '🐏', lootTable: ['fleisch', 'feuer_wolle'], tameFood: 'obsidian_gras', product: { type: 'feuer_wolle', interval: '3days' } },
        asche_huhn:        { name: 'Asche-Huhn',        biome: 'magmastroeme', category: 'vieh',   tier: 0, hp: 15,  attack: 2,  defense: 2,  speed: 0.7, xpReward: 3,   goldDrop: 1,  icon: '🐔', lootTable: ['fleisch', 'feder'], tameFood: 'feuer_koerner', product: { type: 'hitze_ei', interval: 'daily' } },
        magma_salamander:  { name: 'Magma-Salamander',  biome: 'magmastroeme', category: 'vieh',   tier: 0, hp: 25,  attack: 4,  defense: 8,  speed: 0.4, xpReward: 3,   goldDrop: 2,  icon: '🦎', lootTable: ['feuer_schuppe', 'leder'], tameFood: 'schwefel', product: { type: 'feuer_schuppe', interval: '3days' } },

        // ===== GRÜNSCHLAMM - Sumpf, Gift =====
        // -- Lebende --
        sumpfkroete:       { name: 'Sumpfkröte',        biome: 'gruenschlamm', category: 'lebend', clan: 'sumpfchor',      tier: 2, hp: 55,  attack: 14, defense: 8,  speed: 0.6, xpReward: 28,  goldDrop: 12, icon: '🐸', lootTable: ['toad_skin', 'poison_vial'], rareDrop: 'gift_druese' },
        faeulnis_zombie:   { name: 'Fäulnis-Zombie',    biome: 'gruenschlamm', category: 'lebend', clan: 'untote',         tier: 2, hp: 70,  attack: 16, defense: 6,  speed: 0.4, xpReward: 35,  goldDrop: 15, icon: '🧟', lootTable: ['rot_essence', 'zombie_tooth'], rareDrop: 'untoten_herz' },
        giftranke:         { name: 'Giftranke',         biome: 'gruenschlamm', category: 'lebend', clan: 'sumpfpflanzen',  tier: 1, hp: 30,  attack: 18, defense: 2,  speed: 0.2, xpReward: 20,  goldDrop: 8,  icon: '🌿', lootTable: ['poison_vine', 'toxic_pollen'], rareDrop: 'gift_blume' },
        irrlichter:        { name: 'Irrlichter',        biome: 'gruenschlamm', category: 'lebend', clan: 'sumpflichter',   tier: 2, hp: 20,  attack: 15, defense: 1,  speed: 1.4, xpReward: 25,  goldDrop: 15, icon: '💡', lootTable: ['wisp_light', 'swamp_gas'], rareDrop: 'ewiges_licht' },
        schlamm_golem:     { name: 'Schlamm-Golem',     biome: 'gruenschlamm', category: 'lebend', clan: 'sumpfwaechter',  tier: 3, hp: 110, attack: 18, defense: 16, speed: 0.3, xpReward: 55,  goldDrop: 25, icon: '🗿', lootTable: ['mud_core', 'golem_core'], rareDrop: 'lebender_schlamm' },
        blutegel_schwarm:  { name: 'Blutegel-Schwarm',  biome: 'gruenschlamm', category: 'lebend', clan: 'sumpfparasiten', tier: 1, hp: 15,  attack: 10, defense: 0,  speed: 0.8, xpReward: 12,  goldDrop: 5,  icon: '🩸', lootTable: ['leech_blood', 'swamp_herb'], rareDrop: 'heilblut' },
        moor_hexe:         { name: 'Moor-Hexe',         biome: 'gruenschlamm', category: 'lebend', clan: 'hexenzirkel',    tier: 3, hp: 65,  attack: 25, defense: 5,  speed: 0.8, xpReward: 70,  goldDrop: 40, icon: '🧙', lootTable: ['hex_scroll', 'poison_vial', 'witch_hat'], rareDrop: 'hexen_amulett' },
        faulgas_blase:     { name: 'Faulgas-Blase',     biome: 'gruenschlamm', category: 'lebend', clan: 'sumpfparasiten', tier: 1, hp: 10,  attack: 30, defense: 0,  speed: 0.3, xpReward: 20,  goldDrop: 5,  icon: '💨', lootTable: ['swamp_gas', 'toxic_pollen'], rareDrop: 'explosives_gas' },
        // -- Vieh --
        sumpf_schwein:     { name: 'Sumpf-Schwein',     biome: 'gruenschlamm', category: 'vieh',   tier: 0, hp: 35,  attack: 4,  defense: 3,  speed: 0.5, xpReward: 4,   goldDrop: 2,  icon: '🐖', lootTable: ['fleisch', 'fett'], tameFood: 'trueffel', product: { type: 'fett', interval: 'daily' } },
        moor_ente:         { name: 'Moor-Ente',         biome: 'gruenschlamm', category: 'vieh',   tier: 0, hp: 12,  attack: 1,  defense: 1,  speed: 0.8, xpReward: 2,   goldDrop: 1,  icon: '🦆', lootTable: ['fleisch', 'feder'], tameFood: 'wuermer', product: { type: 'moor_ei', interval: 'daily' } },
        gift_frosch:       { name: 'Gift-Frosch',       biome: 'gruenschlamm', category: 'vieh',   tier: 0, hp: 8,   attack: 6,  defense: 1,  speed: 0.7, xpReward: 3,   goldDrop: 2,  icon: '🐸', lootTable: ['gift_sekret'], tameFood: 'fliegen', product: { type: 'gift_sekret', interval: '3days' } },

        // ===== BLITZEBENE - Steppe, Gewitter =====
        // -- Lebende --
        blitz_wolf:        { name: 'Blitz-Wolf',        biome: 'blitzebene',   category: 'lebend', clan: 'blitzrudel',     tier: 2, hp: 60,  attack: 18, defense: 7,  speed: 1.5, xpReward: 38,  goldDrop: 18, icon: '⚡', lootTable: ['charged_pelt', 'lightning_fang'], rareDrop: 'donnerfell' },
        donner_bueffel:    { name: 'Donner-Büffel',     biome: 'blitzebene',   category: 'lebend', clan: 'donnerherde',    tier: 3, hp: 130, attack: 22, defense: 16, speed: 0.8, xpReward: 60,  goldDrop: 30, icon: '🦬', lootTable: ['thunder_horn', 'tough_hide'], rareDrop: 'blitz_horn' },
        sturm_harpy:       { name: 'Sturm-Harpy',       biome: 'blitzebene',   category: 'lebend', clan: 'sturmvoegel',    tier: 2, hp: 40,  attack: 20, defense: 3,  speed: 1.6, xpReward: 35,  goldDrop: 20, icon: '🦅', lootTable: ['harpy_feather', 'wind_crystal'], rareDrop: 'sturm_krone' },
        plasma_schlange:   { name: 'Plasma-Schlange',   biome: 'blitzebene',   category: 'lebend', clan: 'blitzschlangen', tier: 2, hp: 45,  attack: 22, defense: 4,  speed: 1.3, xpReward: 40,  goldDrop: 20, icon: '🐍', lootTable: ['plasma_fang', 'lightning_scale'], rareDrop: 'plasma_gift' },
        blitz_elementar:   { name: 'Blitz-Elementar',   biome: 'blitzebene',   category: 'lebend', clan: 'elementar_zirkel', tier: 3, hp: 70,  attack: 28, defense: 5,  speed: 1.8, xpReward: 65,  goldDrop: 35, icon: '⚡', lootTable: ['pure_lightning', 'storm_crystal'], rareDrop: 'reiner_blitz' },
        sturmjaeger:       { name: 'Sturmjäger',        biome: 'blitzebene',   category: 'lebend', clan: 'sturmjaeger',    tier: 2, hp: 55,  attack: 17, defense: 8,  speed: 1.4, xpReward: 35,  goldDrop: 22, icon: '🏹', lootTable: ['storm_arrow', 'hunter_cloak'], rareDrop: 'jaeger_auge' },
        kupfer_golem:      { name: 'Kupfer-Golem',      biome: 'blitzebene',   category: 'lebend', clan: 'metall_waechter', tier: 3, hp: 140, attack: 20, defense: 20, speed: 0.3, xpReward: 70,  goldDrop: 40, icon: '🗿', lootTable: ['copper_plate', 'golem_core', 'storm_crystal'], rareDrop: 'kupfer_herz' },
        gewittergeist:     { name: 'Gewittergeist',     biome: 'blitzebene',   category: 'lebend', clan: 'sturmvoegel',    tier: 2, hp: 35,  attack: 24, defense: 2,  speed: 1.2, xpReward: 40,  goldDrop: 18, icon: '👻', lootTable: ['storm_essence', 'ghost_essence'], rareDrop: 'gewitter_seele' },
        // -- Vieh --
        donner_pferd:      { name: 'Donner-Pferd',      biome: 'blitzebene',   category: 'vieh',   tier: 0, hp: 50,  attack: 6,  defense: 4,  speed: 1.8, xpReward: 5,   goldDrop: 3,  icon: '🐴', lootTable: ['leder', 'fleisch'], tameFood: 'blitz_gras', product: { type: 'reittier', interval: 'passive' } },
        steppen_hase:      { name: 'Steppen-Hase',      biome: 'blitzebene',   category: 'vieh',   tier: 0, hp: 10,  attack: 1,  defense: 1,  speed: 2.0, xpReward: 2,   goldDrop: 1,  icon: '🐰', lootTable: ['fleisch', 'fell'], tameFood: 'klee', product: { type: 'fell', interval: '3days' } },
        sturm_falke:       { name: 'Sturm-Falke',       biome: 'blitzebene',   category: 'vieh',   tier: 0, hp: 18,  attack: 5,  defense: 1,  speed: 2.2, xpReward: 3,   goldDrop: 2,  icon: '🦅', lootTable: ['feder'], tameFood: 'maus', product: { type: 'feder', interval: 'daily' } },

        // ===== TIEFENHÖHLEN - Unterirdisch, Dunkel =====
        // -- Lebende --
        hoehlen_troll:     { name: 'Höhlen-Troll',      biome: 'tiefenhoehlen', category: 'lebend', clan: 'troll_sippe',    tier: 3, hp: 140, attack: 25, defense: 14, speed: 0.5, xpReward: 65,  goldDrop: 35, icon: '👹', lootTable: ['troll_bone', 'cave_moss', 'troll_blood'], rareDrop: 'troll_herz' },
        kristall_fledermaus:{ name: 'Kristall-Fledermaus',biome: 'tiefenhoehlen', category: 'lebend', clan: 'kristall_schwarm', tier: 1, hp: 20,  attack: 12, defense: 2,  speed: 1.6, xpReward: 15,  goldDrop: 8,  icon: '🦇', lootTable: ['bat_wing', 'crystal_dust'], rareDrop: 'kristall_echo' },
        tiefenwurm:        { name: 'Tiefenwurm',        biome: 'tiefenhoehlen', category: 'lebend', clan: 'tiefen_brut',    tier: 3, hp: 100, attack: 22, defense: 10, speed: 0.6, xpReward: 55,  goldDrop: 30, icon: '🪱', lootTable: ['deep_scale', 'earth_crystal'], rareDrop: 'tiefen_juwel' },
        dunkel_schleicher: { name: 'Dunkel-Schleicher', biome: 'tiefenhoehlen', category: 'lebend', clan: 'schattenjaeger', tier: 2, hp: 35,  attack: 20, defense: 3,  speed: 1.5, xpReward: 35,  goldDrop: 20, icon: '🌑', lootTable: ['shadow_cloth', 'dark_essence'], rareDrop: 'nacht_auge' },
        stalaktit_spinne:  { name: 'Stalaktit-Spinne',  biome: 'tiefenhoehlen', category: 'lebend', clan: 'netzweber',      tier: 2, hp: 45,  attack: 18, defense: 8,  speed: 1.0, xpReward: 30,  goldDrop: 15, icon: '🕷️', lootTable: ['spider_silk', 'stalactite_shard'], rareDrop: 'diamant_seide' },
        echo_geist:        { name: 'Echo-Geist',        biome: 'tiefenhoehlen', category: 'lebend', clan: 'tiefen_geister', tier: 2, hp: 30,  attack: 22, defense: 1,  speed: 1.2, xpReward: 35,  goldDrop: 18, icon: '🔊', lootTable: ['echo_crystal', 'ghost_essence'], rareDrop: 'ewiges_echo' },
        minen_kobold:      { name: 'Minen-Kobold',      biome: 'tiefenhoehlen', category: 'lebend', clan: 'kobold_stamm',   tier: 1, hp: 25,  attack: 15, defense: 4,  speed: 1.3, xpReward: 18,  goldDrop: 15, icon: '💣', lootTable: ['kobold_bomb', 'iron_nugget'], rareDrop: 'kobold_gold' },
        steinbrecher:      { name: 'Steinbrecher',      biome: 'tiefenhoehlen', category: 'lebend', clan: 'stein_riesen',   tier: 3, hp: 160, attack: 28, defense: 22, speed: 0.2, xpReward: 75,  goldDrop: 40, icon: '🗿', lootTable: ['boulder_core', 'golem_core', 'earth_crystal'], rareDrop: 'urkern' },
        // -- Vieh --
        kristall_kaefer:   { name: 'Kristall-Käfer',    biome: 'tiefenhoehlen', category: 'vieh',   tier: 0, hp: 20,  attack: 2,  defense: 10, speed: 0.3, xpReward: 3,   goldDrop: 3,  icon: '🪲', lootTable: ['kristall_staub', 'erz'], tameFood: 'leuchtmoos', product: { type: 'erz', interval: '3days' } },
        hoehlen_fledermaus:{ name: 'Höhlen-Fledermaus', biome: 'tiefenhoehlen', category: 'vieh',   tier: 0, hp: 10,  attack: 3,  defense: 1,  speed: 1.4, xpReward: 2,   goldDrop: 1,  icon: '🦇', lootTable: ['fledermaus_fluegel'], tameFood: 'insekt', product: { type: 'guano', interval: 'daily' } },
        hoehlen_pilz:      { name: 'Leucht-Pilz',       biome: 'tiefenhoehlen', category: 'vieh',   tier: 0, hp: 5,   attack: 0,  defense: 0,  speed: 0.0, xpReward: 1,   goldDrop: 1,  icon: '🍄', lootTable: ['leuchtspore', 'pilz'], tameFood: 'wasser', product: { type: 'leuchtspore', interval: 'daily' } },

        // ===== GÖTTERFELS - Heilig, Mächtig, EXKLUSIV =====
        // -- Lebende (alle Götterfels = lebend, keine Vieh-Tiere hier) --
        himmels_waechter:  { name: 'Himmels-Wächter',   biome: 'goetterfels',  category: 'lebend', clan: 'himmelsorden',   tier: 3, hp: 180, attack: 30, defense: 20, speed: 1.0, xpReward: 100, goldDrop: 60, icon: '👼', lootTable: ['divine_feather', 'holy_crystal', 'guardian_sigil'], rareDrop: 'engelsflügel' },
        zeitriss_phantom:  { name: 'Zeitriss-Phantom',  biome: 'goetterfels',  category: 'lebend', clan: 'zeitwanderer',   tier: 3, hp: 80,  attack: 35, defense: 5,  speed: 2.0, xpReward: 120, goldDrop: 50, icon: '⏰', lootTable: ['time_shard', 'phantom_echo', 'zeitstadt_hinweis'], rareDrop: 'zeitfragment' },
        aether_wolf:       { name: 'Äther-Wolf',        biome: 'goetterfels',  category: 'lebend', clan: 'aether_rudel',   tier: 2, hp: 70,  attack: 22, defense: 10, speed: 1.6, xpReward: 50,  goldDrop: 25, icon: '🐺', lootTable: ['aether_pelt', 'spirit_fang'], rareDrop: 'geist_fang' },
        goetterfels_drake: { name: 'Götterfels-Drake',  biome: 'goetterfels',  category: 'lebend', clan: 'drachen_hort',   tier: 3, hp: 200, attack: 32, defense: 18, speed: 1.2, xpReward: 130, goldDrop: 70, icon: '🐉', lootTable: ['divine_scale', 'drake_heart', 'holy_crystal'], rareDrop: 'goetterschuppe' },
        kristall_seraph:   { name: 'Kristall-Seraph',   biome: 'goetterfels',  category: 'lebend', clan: 'himmelsorden',   tier: 3, hp: 100, attack: 28, defense: 12, speed: 1.4, xpReward: 90,  goldDrop: 45, icon: '💎', lootTable: ['seraph_crystal', 'divine_light'], rareDrop: 'seraph_traene' },
        runen_golem:       { name: 'Runen-Golem',       biome: 'goetterfels',  category: 'lebend', clan: 'runenwaechter',  tier: 3, hp: 250, attack: 25, defense: 30, speed: 0.2, xpReward: 110, goldDrop: 55, icon: '🗿', lootTable: ['rune_stone', 'golem_core', 'ancient_glyph'], rareDrop: 'uralte_rune' },
        schicksals_spinner:{ name: 'Schicksals-Spinner', biome: 'goetterfels',  category: 'lebend', clan: 'schicksalsweber', tier: 3, hp: 90,  attack: 30, defense: 8,  speed: 1.0, xpReward: 95,  goldDrop: 50, icon: '🕸️', lootTable: ['fate_thread', 'destiny_crystal'], rareDrop: 'schicksals_faden' },
        nebel_titan:       { name: 'Nebel-Titan',       biome: 'goetterfels',  category: 'lebend', clan: 'titanen',        tier: 4, hp: 400, attack: 40, defense: 25, speed: 0.6, xpReward: 200, goldDrop: 100,icon: '🌫️', lootTable: ['titan_essence', 'fog_crystal', 'divine_feather', 'zeitstadt_hinweis'], rareDrop: 'titan_seele' },

        // 🔒 GÖTTERFELS EXKLUSIV - Nur hier, nirgendwo sonst!
        zeitwandler:       { name: 'Zeitwandler',       biome: 'goetterfels',  category: 'lebend', clan: 'zeitwanderer',   tier: 4, hp: 150, attack: 35, defense: 15, speed: 2.5, xpReward: 180, goldDrop: 80, icon: '⏳', lootTable: ['time_shard', 'temporal_dust', 'zeitstadt_schluessel'], exclusive: true, hint: 'Flüstert von einer verborgenen Stadt in der Zeit...', rareDrop: 'zeit_essenz' },
        goetterbote:       { name: 'Götterbote',        biome: 'goetterfels',  category: 'lebend', clan: 'himmelsorden',   tier: 4, hp: 120, attack: 20, defense: 25, speed: 1.8, xpReward: 150, goldDrop: 100,icon: '📜', lootTable: ['divine_message', 'holy_crystal', 'zeitstadt_schluessel'], exclusive: true, hint: 'Überbringt Nachrichten zwischen den Göttern und der Zeitstadt.', rareDrop: 'goettliche_botschaft' },
    };

    // ==========================================
    // API
    // ==========================================

    function getMonster(id, level) {
        const base = MONSTERS[id];
        if (!base) return null;

        const stats = calcStats(base, level || 1);
        return {
            ...base,
            id: id,
            ...stats,
            level: level || 1,
        };
    }

    function getMonstersByBiome(biome) {
        return Object.entries(MONSTERS)
            .filter(([, m]) => m.biome === biome)
            .map(([id, m]) => ({ id, ...m }));
    }

    function getRandomEnemy(biome, level) {
        const biomeMonsters = getMonstersByBiome(biome || 'samtmoos');
        if (biomeMonsters.length === 0) return null;

        const idx = Math.floor(Math.random() * biomeMonsters.length);
        return getMonster(biomeMonsters[idx].id, level || 1);
    }

    function getExclusiveMonsters() {
        return Object.entries(MONSTERS)
            .filter(([, m]) => m.exclusive)
            .map(([id, m]) => ({ id, ...m }));
    }

    function getAllBiomes() {
        const biomes = new Set();
        Object.values(MONSTERS).forEach(m => biomes.add(m.biome));
        return [...biomes];
    }

    function getMonsterCount() {
        return Object.keys(MONSTERS).length;
    }

    // ==========================================
    // KATEGORIE & CLAN API
    // ==========================================

    function getByCategory(cat) {
        return Object.entries(MONSTERS)
            .filter(([, m]) => m.category === cat)
            .map(([id, m]) => ({ id, ...m }));
    }

    function getLebende(biome) {
        const list = getByCategory('lebend');
        return biome ? list.filter(m => m.biome === biome) : list;
    }

    function getVieh(biome) {
        const list = getByCategory('vieh');
        return biome ? list.filter(m => m.biome === biome) : list;
    }

    function getClanMembers(clanName) {
        return Object.entries(MONSTERS)
            .filter(([, m]) => m.clan === clanName)
            .map(([id, m]) => ({ id, ...m }));
    }

    function getAllClans() {
        const clans = new Set();
        Object.values(MONSTERS).forEach(m => { if (m.clan) clans.add(m.clan); });
        return [...clans];
    }

    function getViehByTameFood(food) {
        return getByCategory('vieh').filter(m => m.tameFood === food);
    }

    function getRandomVieh(biome) {
        const vieh = getVieh(biome);
        return vieh.length > 0 ? vieh[Math.floor(Math.random() * vieh.length)] : null;
    }

    function getRandomLebende(biome, minTier, maxTier) {
        let pool = getLebende(biome);
        if (minTier !== undefined) pool = pool.filter(m => m.tier >= minTier);
        if (maxTier !== undefined) pool = pool.filter(m => m.tier <= maxTier);
        return pool.length > 0 ? pool[Math.floor(Math.random() * pool.length)] : null;
    }

    // ==========================================
    // ZEITSTADT HINT SYSTEM
    // ==========================================

    function checkZeitstadtHint(lootItem) {
        if (lootItem === 'zeitstadt_hinweis') {
            console.log('⏰ ZEITSTADT-HINWEIS gefunden! Die Zeitstadt versteckt sich in der Spitze des Götterfels...');
            if (typeof notify === 'function') {
                notify('⏰ Ein mysteriöser Hinweis... Die Zeit scheint an der Spitze des Götterfels anders zu fließen.', 'info');
            }
            return true;
        }
        if (lootItem === 'zeitstadt_schluessel') {
            console.log('🔑 ZEITSTADT-SCHLÜSSEL! Der Zugang zur verborgenen Stadt öffnet sich...');
            if (typeof notify === 'function') {
                notify('🔑 Ein Schlüssel zur Zeitstadt! Suche den Eingang an der Spitze des Götterfels!', 'warning');
            }
            // Speichere Fortschritt
            localStorage.setItem('najika_zeitstadt_key', 'true');
            return true;
        }
        return false;
    }

    // ==========================================
    // EXPORT
    // ==========================================

    window.MonsterRegistry = {
        MONSTERS,
        getMonster,
        getMonstersByBiome,
        getRandomEnemy,
        getExclusiveMonsters,
        getAllBiomes,
        getMonsterCount,
        calcStats,
        checkZeitstadtHint,
        // Kategorie & Clan API
        getByCategory,
        getLebende,
        getVieh,
        getClanMembers,
        getAllClans,
        getViehByTameFood,
        getRandomVieh,
        getRandomLebende,
    };

    const lebCount = getLebende().length;
    const viehCount = getVieh().length;
    const clanCount = getAllClans().length;
    console.log(`👹 Monster-Registry: ${getMonsterCount()} Wesen (${lebCount} Lebende + ${viehCount} Vieh) in ${getAllBiomes().length} Biomen`);
    console.log(`🏰 ${clanCount} Kreatur-Clans registriert`);
    console.log(`🔒 Exklusive Götterfels-Wesen: ${getExclusiveMonsters().length}`);
    console.log(`⏰ Zeitstadt versteckt in der Spitze des Götterfels...`);

})();
