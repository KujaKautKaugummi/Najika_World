// ============================================================
// BESTIARY UI - Monster-Kompendium
// Trackt alle begegneten Gegner, zeigt Stats & Loot
// ============================================================
(function() {
    'use strict';

    // Monster-Datenbank aus allen Quellen zusammengeführt
    const BESTIARY_DB = {
        // SAMTMOOS-TIEFWALD
        wolf: { name: 'Wolf', biome: 'Samtmoos-Tiefwald', tier: 1, rarity: 'common', hp: 40, attack: 8, defense: 3, speed: 1.3, xp: 15, element: null, loot: ['wolf_pelt', 'wolf_fang'], desc: 'Jagd in Rudeln im dichten Tiefwald. Schnell und gefährlich in Gruppen.' },
        forest_spider: { name: 'Waldspinne', biome: 'Samtmoos-Tiefwald', tier: 1, rarity: 'common', hp: 25, attack: 12, defense: 2, speed: 1.5, xp: 12, element: 'poison', loot: ['spider_silk', 'venom_sac'], desc: 'Lauert in Netzen zwischen den Bäumen. Gift schwächt Angriffskraft.' },
        boar: { name: 'Wildschwein', biome: 'Samtmoos-Tiefwald', tier: 1, rarity: 'common', hp: 50, attack: 10, defense: 5, speed: 0.8, xp: 18, element: null, loot: ['boar_tusk', 'meat'], desc: 'Robust und territorial. Angriff ist die beste Verteidigung.' },
        bear: { name: 'Bär', biome: 'Samtmoos-Tiefwald', tier: 2, rarity: 'rare', hp: 120, attack: 20, defense: 10, speed: 0.9, xp: 50, element: null, loot: ['bear_pelt', 'bear_claw', 'honey'], desc: 'König des Waldes. Massig und kraftvoll - besser nicht provozieren.' },
        treant: { name: 'Baumwächter', biome: 'Samtmoos-Tiefwald', tier: 3, rarity: 'rare', hp: 150, attack: 15, defense: 20, speed: 0.4, xp: 75, element: 'earth', loot: ['ancient_bark', 'life_sap'], desc: 'Uralter Hüter des Waldes. Langsam aber fast unzerstörbar.' },
        sporax: { name: 'Sporax der Pilzfürst', biome: 'Samtmoos-Tiefwald', tier: 4, rarity: 'boss', hp: 500, attack: 35, defense: 15, speed: 0.6, xp: 300, element: 'poison', loot: ['sporax_spore', 'fungal_crown', 'rare_mushroom'], desc: 'Boss des Tiefwalds. Verbreitet tödliche Sporenwolken.', traits: ['Giftwolke', 'Sporenexplosion'] },

        // REICH DER DREI
        ice_wolf: { name: 'Eiswolf', biome: 'Reich der Drei', tier: 1, rarity: 'common', hp: 45, attack: 10, defense: 4, speed: 1.4, xp: 18, element: 'ice', loot: ['frost_pelt', 'ice_fang'], desc: 'Geisterhafter Jäger der Schneelande. Frostbisse verlangsamen.' },
        snow_hare: { name: 'Schneehase', biome: 'Reich der Drei', tier: 1, rarity: 'common', hp: 20, attack: 5, defense: 1, speed: 2.0, xp: 8, element: null, loot: ['soft_fur', 'rabbit_foot'], desc: 'Flink und schwer zu fangen. Bringt angeblich Glück.' },
        frost_giant: { name: 'Frostriese', biome: 'Reich der Drei', tier: 3, rarity: 'rare', hp: 200, attack: 30, defense: 15, speed: 0.5, xp: 100, element: 'ice', loot: ['giant_ice', 'frozen_heart'], desc: 'Turmhoch und mit eisiger Macht. Ein Schlag kann tödlich sein.' },
        yeti: { name: 'Yeti', biome: 'Reich der Drei', tier: 3, rarity: 'rare', hp: 180, attack: 25, defense: 12, speed: 0.7, xp: 90, element: null, loot: ['yeti_fur', 'yeti_tooth'], desc: 'Legendäres Schneewesen. Extrem selten und extrem gefährlich.' },
        ice_queen: { name: 'Eiskönigin Crystalia', biome: 'Reich der Drei', tier: 5, rarity: 'boss', hp: 600, attack: 40, defense: 20, speed: 0.8, xp: 400, element: 'ice', loot: ['eternal_ice', 'frost_crown', 'diamond_dust'], desc: 'Herrscherin des Eises. Kontrolliert Blizzards und Frostschilde.', traits: ['Frostschild', 'Blizzard', 'Eissplitter'] },

        // HEISSE DÜNEN
        sand_scorpion: { name: 'Sandskorpion', biome: 'Heiße Dünen', tier: 1, rarity: 'common', hp: 35, attack: 15, defense: 8, speed: 1.2, xp: 15, element: null, loot: ['scorpion_tail', 'venom'], desc: 'Versteckt sich im Sand. Giftiger Stachel am Schwanz.' },
        desert_snake: { name: 'Wüstenschlange', biome: 'Heiße Dünen', tier: 1, rarity: 'common', hp: 30, attack: 12, defense: 2, speed: 1.6, xp: 12, element: null, loot: ['snake_skin', 'snake_venom'], desc: 'Blitzschnell und tödlich. Ihr Gift lähmt die Muskeln.' },
        sand_beetle: { name: 'Sandkäfer', biome: 'Heiße Dünen', tier: 1, rarity: 'common', hp: 40, attack: 8, defense: 12, speed: 0.8, xp: 14, element: null, loot: ['chitin_shell', 'beetle_horn'], desc: 'Gepanzert wie ein Panzer. Schwach aber kaum zu durchdringen.' },
        sand_wurm: { name: 'Sandwurm', biome: 'Heiße Dünen', tier: 3, rarity: 'rare', hp: 180, attack: 35, defense: 5, speed: 1.0, xp: 120, element: null, loot: ['wurm_scale', 'wurm_tooth', 'sand_crystal'], desc: 'Riesiges Wesen unter dem Sand. Erdbeben kündigen sein Kommen an.' },
        fire_lord: { name: 'Feuerfürst Ignis', biome: 'Heiße Dünen', tier: 4, rarity: 'boss', hp: 550, attack: 45, defense: 18, speed: 0.9, xp: 350, element: 'fire', loot: ['flame_essence', 'fire_crown', 'molten_core'], desc: 'Flammengeborener Herrscher der Dünen.', traits: ['Flammenaura', 'Meteorregen', 'Feueratem'] },

        // SALZWIND-KÜSTE
        crab: { name: 'Riesenkrabbe', biome: 'Salzwind-Küste', tier: 1, rarity: 'common', hp: 45, attack: 10, defense: 15, speed: 0.6, xp: 14, element: 'water', loot: ['crab_shell', 'crab_meat'], desc: 'Massig gepanzert. Ihre Scheren können Knochen brechen.' },
        seagull: { name: 'Aggressiver Seevogel', biome: 'Salzwind-Küste', tier: 1, rarity: 'common', hp: 20, attack: 8, defense: 1, speed: 2.0, xp: 8, element: null, loot: ['feather', 'beak'], desc: 'Nervige Plagegeister. Greifen in Schwärmen an.' },
        sea_serpent: { name: 'Seeschlange', biome: 'Salzwind-Küste', tier: 3, rarity: 'rare', hp: 160, attack: 28, defense: 10, speed: 1.2, xp: 85, element: 'water', loot: ['sea_scale', 'serpent_fang', 'pearl'], desc: 'Schimmernde Meeresbewohnerin. Selten aber tödlich.' },
        kraken: { name: 'Kraken Tidelord', biome: 'Salzwind-Küste', tier: 5, rarity: 'boss', hp: 700, attack: 50, defense: 25, speed: 0.5, xp: 500, element: 'water', loot: ['kraken_ink', 'tentacle', 'sea_crown'], desc: 'Schrecken der Meere. Tentakel so groß wie Bäume.', traits: ['Tentakelschlag', 'Tintenwolke', 'Gezeitenruf'] },

        // MAGMASTRÖME
        fire_imp: { name: 'Feuerteufel', biome: 'Magmaströme', tier: 1, rarity: 'common', hp: 30, attack: 18, defense: 3, speed: 1.4, xp: 16, element: 'fire', loot: ['fire_essence', 'imp_horn'], desc: 'Kleiner feuriger Plagegeist. Brennend heißes Temperament.' },
        lava_slug: { name: 'Lavaschnecke', biome: 'Magmaströme', tier: 1, rarity: 'common', hp: 50, attack: 12, defense: 8, speed: 0.3, xp: 15, element: 'fire', loot: ['molten_slime', 'obsidian_shard'], desc: 'Kriecht durch Lavaströme. Berührung verbrennt alles.' },
        magma_golem: { name: 'Magmagolem', biome: 'Magmaströme', tier: 3, rarity: 'rare', hp: 220, attack: 35, defense: 25, speed: 0.4, xp: 130, element: 'fire', loot: ['golem_core', 'living_stone', 'lava_crystal'], desc: 'Lebender Fels aus Magma. Fast unverwundbar gegen physische Angriffe.' },
        fire_drake: { name: 'Feuerdrache', biome: 'Magmaströme', tier: 4, rarity: 'rare', hp: 250, attack: 40, defense: 20, speed: 1.0, xp: 150, element: 'fire', loot: ['drake_scale', 'dragon_fang', 'fire_gem'], desc: 'Junger Drache der Vulkanregion. Feurig und flink.' },
        volcano_titan: { name: 'Vulkantitan Pyroclast', biome: 'Magmaströme', tier: 5, rarity: 'boss', hp: 800, attack: 60, defense: 30, speed: 0.3, xp: 600, element: 'fire', loot: ['titan_core', 'volcanic_crown', 'primordial_flame'], desc: 'Urkraft des Vulkans selbst. Kann Erdbeben und Lavawellen auslösen.', traits: ['Erdbeben', 'Lavawelle', 'Vulkanausbruch'] },

        // GRÜNSCHLAMM-SUMPF
        swamp_slime: { name: 'Sumpfschleim', biome: 'Grünschlamm-Sumpf', tier: 1, rarity: 'common', hp: 35, attack: 8, defense: 5, speed: 0.6, xp: 10, element: null, loot: ['slime_gel', 'swamp_moss'], desc: 'Glibberiges Wesen im Sumpf. Absorbiert Schaden.' },
        poison_frog: { name: 'Giftfrosch', biome: 'Grünschlamm-Sumpf', tier: 1, rarity: 'common', hp: 25, attack: 15, defense: 2, speed: 1.3, xp: 12, element: 'poison', loot: ['frog_skin', 'poison_gland'], desc: 'Klein aber tödlich. Hautsekret ist pures Gift.' },
        swamp_leech: { name: 'Riesenegel', biome: 'Grünschlamm-Sumpf', tier: 1, rarity: 'common', hp: 40, attack: 10, defense: 3, speed: 0.8, xp: 11, element: null, loot: ['leech_blood', 'anticoagulant'], desc: 'Saugt Lebensenergie. Je länger der Kampf, desto stärker wird er.' },
        bog_horror: { name: 'Sumpfschrecken', biome: 'Grünschlamm-Sumpf', tier: 3, rarity: 'rare', hp: 170, attack: 28, defense: 12, speed: 0.7, xp: 95, element: null, loot: ['horror_essence', 'swamp_heart'], desc: 'Amalgam aus Schlamm und Dunkelheit. Furcht einflößend.' },
        swamp_queen: { name: 'Sumpfkönigin Morbia', biome: 'Grünschlamm-Sumpf', tier: 4, rarity: 'boss', hp: 550, attack: 38, defense: 16, speed: 0.6, xp: 380, element: 'poison', loot: ['miasma_orb', 'bog_crown', 'essence_of_decay'], desc: 'Herrscherin über Fäulnis und Verfall.', traits: ['Giftnebel', 'Parasitenschwarm', 'Fäulnisaura'] },

        // BLITZEBENE
        lightning_hawk: { name: 'Blitzfalke', biome: 'Blitzebene', tier: 1, rarity: 'common', hp: 30, attack: 14, defense: 2, speed: 2.0, xp: 14, element: 'lightning', loot: ['charged_feather', 'hawk_talon'], desc: 'So schnell wie der Blitz. Sturzflug-Angriffe sind tödlich.' },
        plains_runner: { name: 'Steppenläufer', biome: 'Blitzebene', tier: 1, rarity: 'common', hp: 45, attack: 10, defense: 4, speed: 1.8, xp: 15, element: null, loot: ['swift_hide', 'horn'], desc: 'Flinkes Steppenraubtier. Jagt in Rudeln über die Ebene.' },
        storm_elemental: { name: 'Sturmelementar', biome: 'Blitzebene', tier: 3, rarity: 'rare', hp: 150, attack: 32, defense: 8, speed: 1.5, xp: 100, element: 'lightning', loot: ['storm_essence', 'lightning_crystal'], desc: 'Aus reiner Blitz-Energie geformt. Berührung = Schock.' },
        thunder_lord: { name: 'Donnerfürst Voltaris', biome: 'Blitzebene', tier: 4, rarity: 'boss', hp: 580, attack: 48, defense: 15, speed: 1.2, xp: 420, element: 'lightning', loot: ['thunder_core', 'storm_crown', 'bolt_essence'], desc: 'Lord des Donners. Blitze gehorchen seinem Willen.', traits: ['Kettenblitz', 'Donnerschlag', 'Sturmruf'] },

        // TIEFENHÖHLEN
        cave_bat: { name: 'Höhlenfledermaus', biome: 'Tiefenhöhlen', tier: 1, rarity: 'common', hp: 20, attack: 8, defense: 1, speed: 1.8, xp: 8, element: null, loot: ['bat_wing', 'echo_crystal'], desc: 'Schwärme in der Dunkelheit. Echolot-Schreie verwirren.' },
        rock_golem: { name: 'Steingolem', biome: 'Tiefenhöhlen', tier: 2, rarity: 'common', hp: 80, attack: 15, defense: 20, speed: 0.3, xp: 25, element: 'earth', loot: ['stone_core', 'ore_vein'], desc: 'Erwacht wenn man zu nahe kommt. Harte Schale, langsamer Kern.' },
        mushroom_creature: { name: 'Pilzwesen', biome: 'Tiefenhöhlen', tier: 1, rarity: 'common', hp: 35, attack: 10, defense: 5, speed: 0.7, xp: 12, element: null, loot: ['glowing_spore', 'cave_mushroom'], desc: 'Leuchtende Pilzkreatur. Sporen können halluzinogen wirken.' },
        crystal_dragon: { name: 'Kristalldrache', biome: 'Tiefenhöhlen', tier: 4, rarity: 'rare', hp: 280, attack: 42, defense: 28, speed: 0.8, xp: 180, element: 'earth', loot: ['dragon_crystal', 'prismatic_scale', 'gem_heart'], desc: 'Majestätischer Drache aus lebenden Kristallen. Extrem selten.' },
        deep_king: { name: 'Tiefenkönig Abyssal', biome: 'Tiefenhöhlen', tier: 5, rarity: 'boss', hp: 750, attack: 55, defense: 35, speed: 0.5, xp: 550, element: 'dark', loot: ['abyss_core', 'deep_crown', 'void_essence'], desc: 'Herrscher der Tiefe. Schattenmacht und Erdgewalt.', traits: ['Schattenruf', 'Erderschütterung', 'Abgrundblick'] },

        // REAL 3D COMBAT ENEMIES (Dungeon-basiert)
        bat: { name: 'Höhlenfledermaus', biome: 'Dungeon', tier: 1, rarity: 'common', hp: 15, attack: 3, defense: 0, speed: 2.0, xp: 5, element: null, loot: ['bat_wing'], desc: 'Schwache aber schnelle Dungeon-Fledermaus.' },
        slime: { name: 'Schleim', biome: 'Dungeon', tier: 1, rarity: 'common', hp: 20, attack: 2, defense: 0, speed: 0.5, xp: 8, element: null, loot: ['slime_goo'], desc: 'Klassischer Dungeon-Schleim. Langsam und schwach.' },
        skeleton_warrior: { name: 'Skelett-Krieger', biome: 'Dungeon', tier: 1, rarity: 'common', hp: 30, attack: 8, defense: 0, speed: 1.2, xp: 15, element: null, loot: ['bone', 'sword_rusty'], desc: 'Untotes Skelett mit rostigem Schwert.' },
        skeleton_archer: { name: 'Skelett-Bogenschütze', biome: 'Dungeon', tier: 1, rarity: 'common', hp: 20, attack: 10, defense: 0, speed: 1.0, xp: 18, element: null, loot: ['bone', 'arrow'], desc: 'Fernkämpfer-Skelett. Hält Distanz und schießt Pfeile.' },
        goblin: { name: 'Goblin', biome: 'Dungeon', tier: 2, rarity: 'common', hp: 35, attack: 10, defense: 0, speed: 1.8, xp: 22, element: null, loot: ['gold_coin', 'dagger_crude'], desc: 'Flinker kleiner Plagegeist. Stiehlt gern Items.' },
        skeleton_mage: { name: 'Skelett-Magier', biome: 'Dungeon', tier: 2, rarity: 'rare', hp: 25, attack: 18, defense: 0, speed: 0.8, xp: 30, element: 'arcane', loot: ['bone', 'magic_crystal'], desc: 'Magisch begabtes Skelett. Gefährliche Fernkampf-Zauber.' },
        corrupted_knight: { name: 'Verfluchter Ritter', biome: 'Dungeon', tier: 3, rarity: 'rare', hp: 80, attack: 20, defense: 0, speed: 1.0, xp: 60, element: 'dark', loot: ['cursed_sword', 'plate_armor_broken'], desc: 'Von dunkler Macht korrumpiert. Schwer und mächtig.' },
        witch: { name: 'Hexe', biome: 'Dungeon', tier: 3, rarity: 'rare', hp: 60, attack: 25, defense: 0, speed: 0.9, xp: 70, element: 'arcane', loot: ['witch_hat', 'potion_empty', 'spell_scroll'], desc: 'Dunkle Magierin. Hinterlistig und gefährlich.' },
        barbarian_boss: { name: 'Berserker-Untoter', biome: 'Dungeon', tier: 4, rarity: 'boss', hp: 200, attack: 35, defense: 0, speed: 0.7, xp: 150, element: null, loot: ['great_axe', 'berserker_helm', 'rare_gem'], desc: 'Dungeon-Boss. Wilder Berserker mit kolossaler Axt.' }
    };

    // Biome-Reihenfolge für Darstellung
    const BIOME_ORDER = [
        'Samtmoos-Tiefwald', 'Reich der Drei', 'Heiße Dünen', 'Salzwind-Küste',
        'Magmaströme', 'Grünschlamm-Sumpf', 'Blitzebene', 'Tiefenhöhlen', 'Dungeon'
    ];

    const BIOME_ICONS = {
        'Samtmoos-Tiefwald': '🌲', 'Reich der Drei': '❄️', 'Heiße Dünen': '🏜️',
        'Salzwind-Küste': '🌊', 'Magmaströme': '🌋', 'Grünschlamm-Sumpf': '🐸',
        'Blitzebene': '⚡', 'Tiefenhöhlen': '🕳️', 'Dungeon': '💀'
    };

    const RARITY_COLORS = {
        common: '#aaa', rare: '#3498db', boss: '#FFD700'
    };

    const ELEMENT_ICONS = {
        fire: '🔥', ice: '❄️', lightning: '⚡', water: '💧',
        poison: '☠️', earth: '🪨', dark: '🌑', arcane: '✨', null: ''
    };

    class BestiaryUI {
        constructor() {
            this.isOpen = false;
            this.overlay = null;
            this.encountered = this.loadEncountered();
            this.killed = this.loadKilled();
            this.filterBiome = 'all';

            // Hook into combat systems to track encounters
            this.hookCombatSystems();
        }

        loadEncountered() {
            try {
                return JSON.parse(localStorage.getItem('najika_bestiary_encountered') || '{}');
            } catch { return {}; }
        }

        loadKilled() {
            try {
                return JSON.parse(localStorage.getItem('najika_bestiary_killed') || '{}');
            } catch { return {}; }
        }

        save() {
            localStorage.setItem('najika_bestiary_encountered', JSON.stringify(this.encountered));
            localStorage.setItem('najika_bestiary_killed', JSON.stringify(this.killed));
        }

        trackEncounter(monsterId) {
            if (!BESTIARY_DB[monsterId]) return;
            if (!this.encountered[monsterId]) {
                this.encountered[monsterId] = { firstSeen: Date.now(), count: 0 };
            }
            this.encountered[monsterId].count++;
            this.save();
        }

        trackKill(monsterId) {
            if (!BESTIARY_DB[monsterId]) return;
            this.trackEncounter(monsterId);
            if (!this.killed[monsterId]) {
                this.killed[monsterId] = 0;
            }
            this.killed[monsterId]++;
            this.save();
        }

        hookCombatSystems() {
            // Periodically check if new enemies spawned in Real3DCombat
            setInterval(() => {
                if (window.Real3DCombat?.isActive?.()) {
                    const enemies = window.Real3DCombat?.getEnemies?.() || [];
                    enemies.forEach(e => {
                        if (e.type) this.trackEncounter(e.type);
                    });
                }
            }, 5000);
        }

        getStats() {
            const total = Object.keys(BESTIARY_DB).length;
            const discovered = Object.keys(this.encountered).length;
            const totalKills = Object.values(this.killed).reduce((a, b) => a + b, 0);
            return { total, discovered, totalKills };
        }

        open() {
            if (this.isOpen) return;
            this.isOpen = true;

            this.overlay = document.createElement('div');
            this.overlay.id = 'bestiary-overlay';
            this.overlay.style.cssText = `
                position: fixed; top: 0; left: 0; right: 0; bottom: 0;
                background: rgba(0, 0, 0, 0.95);
                z-index: 10000;
                display: flex;
                flex-direction: column;
                font-family: 'Courier New', monospace;
                color: #e0e0e0;
                overflow-y: auto;
            `;

            this.render();
            document.body.appendChild(this.overlay);

            this._keyHandler = (e) => {
                if (e.key === 'Escape') this.close();
            };
            document.addEventListener('keydown', this._keyHandler);
        }

        close() {
            if (!this.isOpen) return;
            this.isOpen = false;
            if (this.overlay) {
                this.overlay.remove();
                this.overlay = null;
            }
            document.removeEventListener('keydown', this._keyHandler);
        }

        toggle() {
            if (this.isOpen) this.close();
            else this.open();
        }

        setFilter(biome) {
            this.filterBiome = biome;
            this.render();
        }

        render() {
            const stats = this.getStats();
            const completionPercent = stats.total > 0 ? Math.floor((stats.discovered / stats.total) * 100) : 0;

            let monstersToShow = Object.entries(BESTIARY_DB);
            if (this.filterBiome !== 'all') {
                monstersToShow = monstersToShow.filter(([_, m]) => m.biome === this.filterBiome);
            }

            // Sort: discovered first, then by tier, then by name
            monstersToShow.sort((a, b) => {
                const aDiscovered = this.encountered[a[0]] ? 1 : 0;
                const bDiscovered = this.encountered[b[0]] ? 1 : 0;
                if (aDiscovered !== bDiscovered) return bDiscovered - aDiscovered;
                if (a[1].tier !== b[1].tier) return a[1].tier - b[1].tier;
                return a[1].name.localeCompare(b[1].name);
            });

            this.overlay.innerHTML = `
                <div style="max-width: 950px; margin: 0 auto; padding: 20px; width: 100%;">
                    <!-- Header -->
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; border-bottom: 2px solid #e74c3c; padding-bottom: 10px;">
                        <div>
                            <h1 style="margin: 0; color: #e74c3c; font-size: 24px;">📖 BESTIARY</h1>
                            <div style="font-size: 12px; color: #888; margin-top: 4px;">
                                Entdeckt: <span style="color: #FFD700;">${stats.discovered}/${stats.total}</span> (${completionPercent}%)
                                | Kills: <span style="color: #e74c3c;">${stats.totalKills}</span>
                            </div>
                        </div>
                        <button onclick="window.bestiaryUI.close()" style="background: #c0392b; border: none; color: white; padding: 8px 16px; border-radius: 5px; cursor: pointer; font-size: 16px; font-family: inherit;">
                            ✕ [ESC]
                        </button>
                    </div>

                    <!-- Completion Bar -->
                    <div style="background: #1a1a2e; border-radius: 6px; height: 20px; overflow: hidden; margin-bottom: 15px; border: 1px solid #333;">
                        <div style="background: linear-gradient(90deg, #e74c3c, #FFD700); height: 100%; width: ${completionPercent}%; transition: width 0.5s;"></div>
                    </div>

                    <!-- Biome Filter -->
                    <div style="display: flex; flex-wrap: wrap; gap: 5px; margin-bottom: 20px;">
                        <button onclick="window.bestiaryUI.setFilter('all')" style="
                            padding: 5px 12px; border: 1px solid ${this.filterBiome === 'all' ? '#FFD700' : '#555'};
                            background: ${this.filterBiome === 'all' ? 'rgba(255,215,0,0.15)' : 'rgba(0,0,0,0.3)'};
                            color: ${this.filterBiome === 'all' ? '#FFD700' : '#aaa'};
                            border-radius: 5px; cursor: pointer; font-family: inherit; font-size: 12px;
                        ">Alle</button>
                        ${BIOME_ORDER.map(biome => `
                            <button onclick="window.bestiaryUI.setFilter('${biome}')" style="
                                padding: 5px 12px; border: 1px solid ${this.filterBiome === biome ? '#FFD700' : '#555'};
                                background: ${this.filterBiome === biome ? 'rgba(255,215,0,0.15)' : 'rgba(0,0,0,0.3)'};
                                color: ${this.filterBiome === biome ? '#FFD700' : '#aaa'};
                                border-radius: 5px; cursor: pointer; font-family: inherit; font-size: 11px;
                            ">${BIOME_ICONS[biome] || ''} ${biome}</button>
                        `).join('')}
                    </div>

                    <!-- Monster Grid -->
                    <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 12px;">
                        ${monstersToShow.map(([id, m]) => this.renderMonsterCard(id, m)).join('')}
                    </div>
                </div>
            `;
        }

        renderMonsterCard(id, monster) {
            const isDiscovered = !!this.encountered[id];
            const kills = this.killed[id] || 0;
            const encounters = this.encountered[id]?.count || 0;
            const rarityColor = RARITY_COLORS[monster.rarity] || '#aaa';
            const elementIcon = ELEMENT_ICONS[monster.element] || '';
            const biomeIcon = BIOME_ICONS[monster.biome] || '';

            if (!isDiscovered) {
                return `
                <div style="background: rgba(30,30,30,0.8); border: 1px solid #333; border-radius: 8px; padding: 12px; opacity: 0.5;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #555; font-size: 16px;">???</span>
                        <span style="font-size: 10px; color: #444;">${biomeIcon} ${monster.biome}</span>
                    </div>
                    <div style="color: #333; font-size: 11px; margin-top: 8px; font-style: italic;">Noch nicht entdeckt...</div>
                </div>`;
            }

            const tierStars = '★'.repeat(monster.tier) + '☆'.repeat(Math.max(0, 5 - monster.tier));

            return `
            <div style="background: rgba(30,30,50,0.9); border: 1px solid ${rarityColor}; border-radius: 8px; padding: 12px; border-left: 3px solid ${rarityColor};">
                <!-- Name & Rarity -->
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 6px;">
                    <div>
                        <span style="color: ${rarityColor}; font-size: 15px; font-weight: bold;">${elementIcon} ${monster.name}</span>
                        <div style="font-size: 10px; color: #888; margin-top: 2px;">
                            ${biomeIcon} ${monster.biome} | <span style="color: #FFD700;">${tierStars}</span>
                        </div>
                    </div>
                    <span style="font-size: 10px; padding: 2px 6px; border-radius: 3px; background: ${rarityColor}22; color: ${rarityColor}; border: 1px solid ${rarityColor}44;">
                        ${monster.rarity.toUpperCase()}
                    </span>
                </div>

                <!-- Description -->
                <div style="font-size: 11px; color: #999; margin-bottom: 8px; font-style: italic;">${monster.desc}</div>

                <!-- Stats Grid -->
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 4px; font-size: 11px; margin-bottom: 8px;">
                    <span>❤️ ${monster.hp}</span>
                    <span>⚔️ ${monster.attack}</span>
                    <span>🛡️ ${monster.defense}</span>
                    <span>💨 ${monster.speed}</span>
                    <span>⭐ ${monster.xp} XP</span>
                    <span>${monster.element ? `${elementIcon} ${monster.element}` : ''}</span>
                </div>

                ${monster.traits ? `
                <div style="font-size: 10px; color: #9b59b6; margin-bottom: 6px;">
                    Fähigkeiten: ${monster.traits.join(', ')}
                </div>` : ''}

                <!-- Loot -->
                <div style="font-size: 10px; color: #2ecc71; margin-bottom: 6px;">
                    Loot: ${monster.loot.map(l => l.replace(/_/g, ' ')).join(', ')}
                </div>

                <!-- Kill Counter -->
                <div style="display: flex; justify-content: space-between; font-size: 10px; color: #666; border-top: 1px solid #333; padding-top: 5px; margin-top: 4px;">
                    <span>Begegnungen: ${encounters}</span>
                    <span>Besiegt: <span style="color: #e74c3c;">${kills}</span></span>
                </div>
            </div>`;
        }
    }

    // Global instance
    window.bestiaryUI = new BestiaryUI();

    // Expose trackKill for combat systems to call
    window.bestiaryTrackKill = (id) => window.bestiaryUI.trackKill(id);
    window.bestiaryTrackEncounter = (id) => window.bestiaryUI.trackEncounter(id);

    console.log('📖 BestiaryUI geladen - ' + Object.keys(BESTIARY_DB).length + ' Monster registriert');
})();
