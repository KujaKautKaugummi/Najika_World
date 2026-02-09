/**
 * NAJIKA WORLD - UNIFIED WORLD EVENT GENERATOR
 * ==============================================
 * DER KERN DES SPIELS.
 *
 * Die Welt IST das Spiel. Nicht Quests. Die Welt LEBT.
 * - NPCs tauchen auf, bewegen sich, handeln, sterben
 * - Events passieren ob der Spieler da ist oder nicht
 * - Konsequenzen: Ignorierst du den Jungen → sein Onkel (Händler) stirbt
 * - Oregon Trail / Konosuba Events während der Reise
 * - Postman-Ranger kreuzen die Welt
 * - Banditen, Händler, Karawanen, Abenteurer
 *
 * Außenwelt-Generator + Dungeon-Generator = SELBER KERN, andere Parameter
 * Einmal perfektioniert = endloser Content drinnen UND draußen
 *
 * "Es fühlt sich an wie eine echte Welt. Sachen geschehen.
 *  Menschen erscheinen. Ultimative Lebenssimulation." - Der User
 */

(function() {
    'use strict';

    // ==========================================
    // WORLD STATE (Persistente lebendige Welt)
    // ==========================================

    let worldState = loadWorldState();

    function loadWorldState() {
        try {
            return JSON.parse(localStorage.getItem('najika_world_state') || 'null') || createFreshWorldState();
        } catch { return createFreshWorldState(); }
    }

    function createFreshWorldState() {
        return {
            day: 1,
            timeOfDay: 'morning', // morning, afternoon, evening, night
            activeNPCs: [],       // NPCs gerade in der Welt
            deadNPCs: [],         // Tote NPCs (Konsequenzen!)
            activeEvents: [],     // Laufende Events
            eventHistory: [],     // Was passiert ist (max 100)
            worldReputation: {},  // Ruf pro Biom/Stadt
            consequences: [],     // Konsequenz-Ketten
            economyState: {},     // Händlerpreise, Verfügbarkeit
            lastGeneration: 0,    // Timestamp
        };
    }

    function saveWorldState() {
        // Limitiere History
        if (worldState.eventHistory.length > 100) {
            worldState.eventHistory = worldState.eventHistory.slice(-100);
        }
        if (worldState.consequences.length > 50) {
            worldState.consequences = worldState.consequences.slice(-50);
        }
        localStorage.setItem('najika_world_state', JSON.stringify(worldState));
    }

    // ==========================================
    // NPC TEMPLATES (Lebendige Welt-Bewohner)
    // ==========================================

    const NPC_TEMPLATES = {
        // Reisende die man unterwegs trifft
        wanderer: [
            { name: 'Alter Wanderer',     icon: '🧓', type: 'friendly',  dialogue: 'Vorsicht auf dem Weg, Fremder. Ich habe Banditen gesehen.', canTrade: false, canQuest: true },
            { name: 'Junge Abenteurerin', icon: '⚔️', type: 'friendly',  dialogue: 'Hey! Willst du zusammen reisen? Alleine ists gefährlich.', canTrade: false, canQuest: true },
            { name: 'Verwundeter Reiter', icon: '🤕', type: 'helpable',  dialogue: 'Hilfe... Banditen haben mich überfallen...', canTrade: false, canQuest: true },
            { name: 'Pilgerin',           icon: '🙏', type: 'friendly',  dialogue: 'Ich bin auf dem Weg zum Götterfels. Mögen die Götter dich beschützen.', canTrade: false, canQuest: false },
        ],

        // Händler unterwegs (KÖNNEN STERBEN → Konsequenzen!)
        haendler: [
            { name: 'Kräuterhändler',     icon: '🌿', type: 'trader',    dialogue: 'Frische Kräuter! Direkt aus dem Samtmoos!', canTrade: true, shopType: 'herbs',   goldRange: [50, 200] },
            { name: 'Waffenschmied',      icon: '⚒️', type: 'trader',    dialogue: 'Feinste Klingen für mutige Krieger!', canTrade: true, shopType: 'weapons', goldRange: [100, 500] },
            { name: 'Mysteriöser Händler', icon: '🎭', type: 'trader',    dialogue: '...Ich habe was du brauchst. Frag nicht woher.', canTrade: true, shopType: 'rare',    goldRange: [200, 1000] },
            { name: 'Reisender Koch',     icon: '🍳', type: 'trader',    dialogue: 'Hunger? Mein Eintopf ist der beste von hier bis Salzwind!', canTrade: true, shopType: 'food',    goldRange: [20, 100] },
        ],

        // Postman-Ranger unterwegs (andere Postman!)
        postman: [
            { name: 'Ranger-Veteranin',   icon: '📮', type: 'postman',   dialogue: 'Schönen Tag noch, Kollege. Die Straße war heute ruhig.', canTrade: false, canQuest: false },
            { name: 'Novize-Bote',        icon: '📬', type: 'postman',   dialogue: 'W-weißt du wo Grünschlamm ist? Ich hab mich verlaufen...', canTrade: false, canQuest: true },
        ],

        // Gefahren
        banditen: [
            { name: 'Straßenräuber',      icon: '🗡️', type: 'hostile',   dialogue: 'Geld oder Leben!', canTrade: false, canQuest: false, level: 3 },
            { name: 'Banditen-Anführer',   icon: '💀', type: 'hostile',   dialogue: 'Hübsche Ausrüstung. Die nehm ich.', canTrade: false, canQuest: false, level: 8 },
            { name: 'Desperado',           icon: '🤠', type: 'hostile',   dialogue: 'Nichts Persönliches, Partner.', canTrade: false, canQuest: false, level: 5 },
        ],

        // Hilfsbedürftige (IGNORIEREN = KONSEQUENZEN!)
        hilflose: [
            { name: 'Verlorener Junge',   icon: '👦', type: 'helpable',  dialogue: 'Bitte hilf mir! Ich finde meinen Onkel nicht!', canTrade: false, canQuest: true,
              consequence: { type: 'npc_death', target: 'random_trader', delay: 600000, description: 'Der Onkel ging ihn suchen und wurde unterwegs getötet.' }},
            { name: 'Verletzte Händlerin', icon: '🩹', type: 'helpable',  dialogue: 'Mein Bein... ich kann nicht weiterlaufen...', canTrade: false, canQuest: true,
              consequence: { type: 'price_increase', biome: 'current', amount: 1.3, delay: 300000, description: 'Ohne die Händlerin stiegen die Preise in der Region.' }},
            { name: 'Kranker Bauer',      icon: '🤒', type: 'helpable',  dialogue: 'Ich brauche Kräuter... sonst schaffe ich es nicht zur Stadt...', canTrade: false, canQuest: true,
              consequence: { type: 'quest_lost', questId: 'farmer_harvest', delay: 900000, description: 'Der Bauer starb. Seine Farm liegt brach. Kein Essen in der Stadt.' }},
            { name: 'Gefangener in Käfig', icon: '🔒', type: 'helpable',  dialogue: 'Die Banditen haben mich eingesperrt! Schlüssel liegt beim Lagerfeuer!', canTrade: false, canQuest: true,
              consequence: { type: 'reputation_loss', biome: 'current', amount: -10, delay: 0, description: 'Die Nachricht verbreitete sich: Du hast nicht geholfen.' }},
        ],

        // Besondere Begegnungen
        besonders: [
            { name: 'Zeitriss-Wanderer', icon: '⏰', type: 'mysterious', dialogue: 'Die Zeit... fließt hier anders. Spürst du es auch?', canTrade: false, canQuest: true,
              biomeOnly: 'goetterfels', hint: 'zeitstadt' },
            { name: 'Maskierter Krieger', icon: '🎭', type: 'challenge',  dialogue: 'Du siehst stark aus. Bist du bereit für eine Prüfung?', canTrade: false, canQuest: true },
            { name: 'Singende Reisende', icon: '🎵', type: 'friendly',   dialogue: '*singt* ...und der Wind trug ihn fort, über Berg und Meer...', canTrade: false, canQuest: false,
              buff: { morale: 1.1, duration: 300000 } },
        ],
    };

    // ==========================================
    // OREGON TRAIL / KONOSUBA EVENTS
    // ==========================================

    const WORLD_EVENTS = [
        // REISE-EVENTS (passieren unterwegs)
        {
            id: 'broken_bridge',
            name: '🌉 Brücke zerstört!',
            description: 'Eine Brücke auf dem Weg ist eingestürzt. Du musst einen anderen Weg finden oder sie reparieren.',
            biomes: ['samtmoos', 'reich_der_drei', 'blitzebene'],
            choices: [
                { text: 'Umweg nehmen (sicher, aber langsam)', effect: { time: +300, stamina: -10 } },
                { text: 'Durch den Fluss waten (riskant)', effect: { hp: -15, time: 0 }, risk: 0.3 },
                { text: 'Brücke reparieren (braucht Materialien)', effect: { time: +600, reputation: +5 }, requires: { item: 'root_fiber', count: 3 } },
            ],
        },
        {
            id: 'bandit_ambush',
            name: '⚔️ Hinterhalt!',
            description: 'Banditen springen aus dem Gebüsch! Sie wollen deine Sachen!',
            biomes: ['samtmoos', 'reich_der_drei', 'heisse_duenen', 'gruenschlamm'],
            choices: [
                { text: 'Kämpfen!', effect: { combat: true, enemies: ['bandit', 'bandit'] } },
                { text: 'Verhandeln (Gold anbieten)', effect: { gold: -50, time: 0 } },
                { text: 'Fliehen! (Stamina)', effect: { stamina: -25, time: -60 }, risk: 0.4 },
            ],
        },
        {
            id: 'mysterious_merchant',
            name: '🎭 Mysteriöser Händler',
            description: 'Ein maskierter Händler taucht aus dem Nichts auf. "Ich habe was du brauchst..."',
            biomes: ['*'],
            choices: [
                { text: 'Handeln', effect: { shop: true, shopType: 'rare' } },
                { text: 'Misstrauisch ablehnen', effect: {} },
                { text: 'Fragen woher er kommt', effect: { lore: true, hint: 'zeitstadt' }, chance: 0.2 },
            ],
        },
        {
            id: 'storm_approaching',
            name: '🌩️ Sturm zieht auf!',
            description: 'Dunkle Wolken am Horizont. Ein gewaltiger Sturm kommt!',
            biomes: ['blitzebene', 'salzwind', 'heisse_duenen'],
            choices: [
                { text: 'Unterschlupf suchen (Zeit verlieren)', effect: { time: +600, safe: true } },
                { text: 'Weiterlaufen (riskant!)', effect: { hp: -20, stamina: -15 }, risk: 0.5 },
                { text: 'Höhle suchen (Entdeckung möglich!)', effect: { time: +300, discovery: true }, chance: 0.4 },
            ],
        },
        {
            id: 'wounded_traveler',
            name: '🩹 Verwundeter Reisender',
            description: 'Ein verletzter Reisender liegt am Wegrand. Er stöhnt vor Schmerzen.',
            biomes: ['*'],
            choices: [
                { text: 'Helfen! (Kräuter/Zeit)', effect: { reputation: +10, time: +180, karma: +1 },
                  consequence_good: { type: 'npc_grateful', delay: 0, description: 'Er wird sich erinnern und dir einen Gefallen schulden.' } },
                { text: 'Ignorieren und weitergehen', effect: {},
                  consequence_bad: { type: 'npc_death', delay: 600000, description: 'Der Reisende starb am Wegrand. Die Nachricht verbreitet sich.' } },
                { text: 'Ausrauben (Evil!)', effect: { gold: +30, karma: -3, reputation: -15 },
                  consequence_bad: { type: 'wanted', bounty: 100, description: 'Du wirst als Räuber gesucht!' } },
            ],
        },
        {
            id: 'caravan_passing',
            name: '🐫 Karawane passiert',
            description: 'Eine Handelskarawane zieht an dir vorbei. Schwer bewacht.',
            biomes: ['heisse_duenen', 'reich_der_drei', 'blitzebene'],
            choices: [
                { text: 'Mitreisen (sicherer, langsamer)', effect: { safe: true, time: +300, social: true } },
                { text: 'Handeln mit den Kaufleuten', effect: { shop: true, shopType: 'exotic' } },
                { text: 'Eigenen Weg gehen', effect: {} },
            ],
        },
        {
            id: 'lost_child',
            name: '👦 Verlorenes Kind',
            description: 'Ein kleiner Junge weint am Wegrand. "Ich finde meinen Onkel nicht!"',
            biomes: ['*'],
            choices: [
                { text: 'Dem Kind helfen suchen', effect: { time: +600, reputation: +15, karma: +2 },
                  consequence_good: { type: 'npc_alive', npcType: 'cheap_trader', description: 'Der Onkel (bester Händler der Stadt) lebt! Günstige Preise für dich!' } },
                { text: 'Ignorieren', effect: {},
                  consequence_bad: { type: 'npc_death', target: 'cheap_trader', delay: 600000,
                    description: 'Der Onkel suchte allein und wurde von Banditen getötet. Preise in der Stadt steigen. Der günstigste Händler ist tot.' } },
            ],
        },
        {
            id: 'ancient_ruins',
            name: '🏛️ Antike Ruinen entdeckt!',
            description: 'Halb verborgen unter Ranken: Reste einer alten Zivilisation!',
            biomes: ['samtmoos', 'tiefenhoehlen', 'goetterfels'],
            choices: [
                { text: 'Erkunden (Loot + Gefahr)', effect: { dungeon: true, dungeonType: 'crawler', dungeonLevel: 3 } },
                { text: 'Vorsichtig umgehen', effect: { lore: true } },
                { text: 'Position merken für später', effect: { mapMarker: true } },
            ],
        },
        {
            id: 'konosuba_explosion',
            name: '💥 EXPLOSION!!! (Konosuba Style)',
            description: 'Eine gewaltige Explosion erschüttert den Horizont! *Megumin wäre stolz*',
            biomes: ['magmastroeme', 'blitzebene'],
            choices: [
                { text: 'Zum Explosionsort rennen!', effect: { discovery: true, combat: true, enemies: ['flammen_imp', 'flammen_imp', 'asche_golem'] } },
                { text: 'In Deckung gehen!', effect: { safe: true } },
                { text: '...Explosion ist NICHT Weave!', effect: { lore: true, funFact: true } },
            ],
        },
        {
            id: 'trader_dies_road',
            name: '💀 Toter Händler am Weg',
            description: 'Ein Händler liegt tot am Wegrand. Seine Waren sind verstreut. Banditen?',
            biomes: ['*'],
            choices: [
                { text: 'Waren einsammeln (gratis Loot!)', effect: { loot: true, karma: -1, reputation: -5 } },
                { text: 'Den Toten begraben (ehrenhaft)', effect: { time: +300, reputation: +10, karma: +2 } },
                { text: 'Spuren der Banditen folgen', effect: { combat: true, enemies: ['bandit', 'desperado'], lootBonus: true } },
            ],
            consequence_world: { type: 'trader_missing', description: 'Ein Händler fehlt in der nächsten Stadt. Preise steigen leicht.' },
        },
        {
            id: 'campfire_strangers',
            name: '🔥 Lagerfeuer in der Ferne',
            description: 'Rauch steigt auf. Jemand hat ein Lagerfeuer gemacht. Freund oder Feind?',
            biomes: ['*'],
            choices: [
                { text: 'Sich nähern und grüßen', effect: { social: true }, risk: 0.2 },
                { text: 'Beobachten aus der Ferne', effect: { perception: true } },
                { text: 'Umgehen', effect: {} },
            ],
        },
        {
            id: 'river_crossing',
            name: '🏞️ Flussdurchquerung',
            description: 'Ein breiter Fluss versperrt den Weg. Die Strömung ist stark.',
            biomes: ['samtmoos', 'gruenschlamm', 'reich_der_drei'],
            choices: [
                { text: 'Schwimmen (riskant)', effect: { stamina: -20, hp: -10 }, risk: 0.3 },
                { text: 'Flussabwärts Furt suchen', effect: { time: +300 } },
                { text: 'Floß bauen', effect: { time: +600, requires: { item: 'root_fiber', count: 5 } } },
            ],
        },
        {
            id: 'fellow_postman',
            name: '📮 Postman-Ranger gesichtet!',
            description: 'Ein anderer Postman-Ranger läuft die Straße entlang. Maske und Mantel wehen im Wind.',
            biomes: ['*'],
            choices: [
                { text: 'Grüßen und Informationen tauschen', effect: { info: true, postmanXP: +5 } },
                { text: 'Nicken und weitergehen', effect: {} },
                { text: 'Warnen: Banditen voraus!', effect: { karma: +1, postmanRep: +3 } },
            ],
        },
        {
            id: 'night_sounds',
            name: '🌙 Unheimliche Geräusche',
            description: 'In der Dunkelheit hörst du seltsame Geräusche. Etwas bewegt sich.',
            biomes: ['samtmoos', 'gruenschlamm', 'tiefenhoehlen'],
            timeOfDay: 'night',
            choices: [
                { text: 'Untersuchen (mutig!)', effect: { discovery: true, combat: true }, risk: 0.5 },
                { text: 'Feuer machen (Schutz)', effect: { safe: true, stamina: -5 } },
                { text: 'Still davonschleichen', effect: {} },
            ],
        },
        {
            id: 'singing_bard',
            name: '🎵 Wandernder Barde',
            description: 'Ein Barde spielt an einer Wegkreuzung. Seine Musik ist wunderschön.',
            biomes: ['reich_der_drei', 'samtmoos', 'goetterfels'],
            choices: [
                { text: 'Zuhören (Buff!)', effect: { buff: { morale: 1.15, stamina_regen: 1.1, duration: 300000 } } },
                { text: 'Münze werfen', effect: { gold: -5, reputation: +3, karma: +1 } },
                { text: 'Nach Neuigkeiten fragen', effect: { info: true, eventHint: true } },
            ],
        },
    ];

    // ==========================================
    // KONSEQUENZ-SYSTEM (Das Herz der lebendigen Welt!)
    // ==========================================

    function triggerConsequence(consequence) {
        if (!consequence) return;

        const entry = {
            ...consequence,
            triggeredAt: Date.now(),
            executesAt: Date.now() + (consequence.delay || 0),
            executed: false,
        };

        worldState.consequences.push(entry);
        saveWorldState();

        // Sofort ausführen wenn kein Delay
        if (!consequence.delay || consequence.delay === 0) {
            executeConsequence(entry);
        }

        console.log(`⚡ Konsequenz geplant: ${consequence.description} (in ${(consequence.delay || 0) / 1000}s)`);
    }

    function executeConsequence(consequence) {
        if (consequence.executed) return;
        consequence.executed = true;

        switch (consequence.type) {
            case 'npc_death':
                // Ein NPC stirbt! Weltauswirkung!
                worldState.deadNPCs.push({
                    type: consequence.target || 'unknown',
                    diedAt: Date.now(),
                    reason: consequence.description,
                });
                if (typeof notify === 'function') {
                    notify(`💀 ${consequence.description}`, 'warning');
                }
                worldState.eventHistory.push({
                    type: 'npc_death',
                    description: consequence.description,
                    timestamp: Date.now(),
                });
                break;

            case 'npc_alive':
                // NPC überlebt dank Spieler!
                if (typeof notify === 'function') {
                    notify(`✅ ${consequence.description}`, 'success');
                }
                worldState.eventHistory.push({
                    type: 'npc_saved',
                    description: consequence.description,
                    timestamp: Date.now(),
                });
                break;

            case 'price_increase':
                // Preise steigen in einer Region
                const biome = consequence.biome === 'current' ? getCurrentBiome() : consequence.biome;
                if (!worldState.economyState[biome]) worldState.economyState[biome] = {};
                worldState.economyState[biome].priceMultiplier = consequence.amount || 1.3;
                worldState.economyState[biome].reason = consequence.description;
                if (typeof notify === 'function') {
                    notify(`📈 Preise gestiegen: ${consequence.description}`, 'warning');
                }
                break;

            case 'reputation_loss':
                const repBiome = consequence.biome === 'current' ? getCurrentBiome() : consequence.biome;
                if (!worldState.worldReputation[repBiome]) worldState.worldReputation[repBiome] = 50;
                worldState.worldReputation[repBiome] += (consequence.amount || -10);
                worldState.worldReputation[repBiome] = Math.max(0, Math.min(100, worldState.worldReputation[repBiome]));
                break;

            case 'wanted':
                // Spieler wird gesucht!
                if (typeof notify === 'function') {
                    notify(`🚨 GESUCHT! Kopfgeld: ${consequence.bounty}g`, 'error');
                }
                worldState.eventHistory.push({
                    type: 'wanted',
                    bounty: consequence.bounty,
                    timestamp: Date.now(),
                });
                break;

            case 'trader_missing':
                // Händler fehlt in Stadt
                if (typeof notify === 'function') {
                    notify(`📦 ${consequence.description}`, 'info');
                }
                break;

            case 'npc_grateful':
                // NPC schuldet Spieler einen Gefallen
                worldState.eventHistory.push({
                    type: 'favor_owed',
                    description: consequence.description,
                    timestamp: Date.now(),
                });
                break;
        }

        saveWorldState();
    }

    // Prüfe ob verzögerte Konsequenzen fällig sind
    function checkPendingConsequences() {
        const now = Date.now();
        worldState.consequences.forEach(c => {
            if (!c.executed && c.executesAt <= now) {
                executeConsequence(c);
            }
        });
    }

    // ==========================================
    // WELT-GENERIERUNG (Kern-Engine)
    // ==========================================

    function generateWorldSlice(biome, playerX, playerZ, radius) {
        const result = {
            npcs: [],
            events: [],
            props: [], // Delegiert an OverworldProps
            enemies: [], // Delegiert an MonsterRegistry
        };

        // Seeded Random basierend auf Position + Tag
        const seed = hashPosition(playerX, playerZ, worldState.day);

        // 1. NPCs generieren
        result.npcs = generateNPCsForSlice(biome, seed, playerX, playerZ, radius);

        // 2. Events prüfen (basierend auf Distanz seit letztem Event)
        result.events = checkForEvents(biome);

        // 3. Konsequenzen anwenden (tote NPCs nicht spawnen etc.)
        applyConsequences(result);

        return result;
    }

    function generateNPCsForSlice(biome, seed, centerX, centerZ, radius) {
        const npcs = [];
        const rng = createRNG(seed);

        // Wie viele NPCs? Abhängig von Biom und Reputation
        const rep = worldState.worldReputation[biome] || 50;
        const baseDensity = getBiomeNPCDensity(biome);
        const density = baseDensity * (rep / 50); // Schlechte Rep = weniger NPCs

        const npcCount = Math.floor(2 + rng() * density * 4);

        for (let i = 0; i < npcCount; i++) {
            const r = rng();
            let template;

            // Gewichtete Auswahl
            if (r < 0.25) {
                template = pickRandom(NPC_TEMPLATES.wanderer, rng);
            } else if (r < 0.45) {
                template = pickRandom(NPC_TEMPLATES.haendler, rng);
            } else if (r < 0.55) {
                template = pickRandom(NPC_TEMPLATES.postman, rng);
            } else if (r < 0.70) {
                template = pickRandom(NPC_TEMPLATES.banditen, rng);
            } else if (r < 0.85) {
                template = pickRandom(NPC_TEMPLATES.hilflose, rng);
            } else {
                template = pickRandom(NPC_TEMPLATES.besonders, rng);
                // Biom-exklusive NPCs filtern
                if (template.biomeOnly && template.biomeOnly !== biome) {
                    template = pickRandom(NPC_TEMPLATES.wanderer, rng);
                }
            }

            // Tote NPCs nicht spawnen!
            if (isNPCTypeDead(template.name)) continue;

            // Position
            const angle = rng() * Math.PI * 2;
            const dist = 100 + rng() * (radius - 200);
            const x = centerX + Math.cos(angle) * dist;
            const z = centerZ + Math.sin(angle) * dist;

            npcs.push({
                ...template,
                id: `npc_${biome}_${i}_${worldState.day}`,
                worldX: x,
                worldZ: z,
                spawnedAt: Date.now(),
                interacted: false,
            });
        }

        return npcs;
    }

    function checkForEvents(biome) {
        const events = [];

        // Max 1 Event pro Weltgenerierung
        const chance = 0.35; // 35% Chance auf Event
        if (Math.random() > chance) return events;

        // Filtere Events für dieses Biom
        const possible = WORLD_EVENTS.filter(e =>
            e.biomes.includes('*') || e.biomes.includes(biome)
        );

        if (possible.length === 0) return events;

        // Vermeide kürzlich passierte Events
        const recentIds = worldState.eventHistory
            .filter(h => Date.now() - h.timestamp < 600000) // 10 min
            .map(h => h.eventId);

        const available = possible.filter(e => !recentIds.includes(e.id));
        if (available.length === 0) return events;

        // Zufälliges Event
        const event = available[Math.floor(Math.random() * available.length)];
        events.push(event);

        return events;
    }

    function applyConsequences(worldSlice) {
        // Entferne NPCs deren Typ tot ist
        worldSlice.npcs = worldSlice.npcs.filter(npc => {
            return !isNPCTypeDead(npc.type);
        });

        // Preis-Modifikationen auf Händler anwenden
        worldSlice.npcs.forEach(npc => {
            if (npc.canTrade && npc.shopType) {
                const biome = getCurrentBiome();
                const eco = worldState.economyState[biome];
                if (eco && eco.priceMultiplier) {
                    npc.priceMultiplier = eco.priceMultiplier;
                }
            }
        });
    }

    function isNPCTypeDead(npcType) {
        return worldState.deadNPCs.some(d =>
            d.type === npcType && (Date.now() - d.diedAt) < 86400000 // 24h tot bleiben
        );
    }

    // ==========================================
    // EVENT EXECUTION
    // ==========================================

    function executeEventChoice(event, choiceIndex) {
        const choice = event.choices[choiceIndex];
        if (!choice) return null;

        const result = {
            eventId: event.id,
            eventName: event.name,
            choiceText: choice.text,
            effects: {},
        };

        const effect = choice.effect;

        // Risiko-Check
        if (choice.risk && Math.random() < choice.risk) {
            result.effects.riskFailed = true;
            result.effects.extraDamage = Math.floor(effect.hp ? Math.abs(effect.hp) * 0.5 : 10);
        }

        // Effekte anwenden
        if (effect.hp) result.effects.hp = effect.hp;
        if (effect.stamina) result.effects.stamina = effect.stamina;
        if (effect.gold) result.effects.gold = effect.gold;
        if (effect.reputation) result.effects.reputation = effect.reputation;
        if (effect.karma) result.effects.karma = effect.karma;
        if (effect.combat) result.effects.combat = { enemies: effect.enemies || ['bandit'] };
        if (effect.shop) result.effects.shop = { type: effect.shopType || 'general' };
        if (effect.dungeon) result.effects.dungeon = { type: effect.dungeonType, level: effect.dungeonLevel };
        if (effect.loot) result.effects.loot = true;
        if (effect.lore) result.effects.lore = true;
        if (effect.buff) result.effects.buff = effect.buff;
        if (effect.discovery) result.effects.discovery = true;

        // Konsequenzen
        if (choice.consequence_good) triggerConsequence(choice.consequence_good);
        if (choice.consequence_bad) triggerConsequence(choice.consequence_bad);
        if (event.consequence_world) triggerConsequence(event.consequence_world);

        // In History speichern
        worldState.eventHistory.push({
            eventId: event.id,
            eventName: event.name,
            choice: choice.text,
            timestamp: Date.now(),
        });

        saveWorldState();

        console.log(`📖 Event: ${event.name} → "${choice.text}"`);
        if (typeof notify === 'function') {
            notify(`${event.name}: ${choice.text}`, 'info');
        }

        return result;
    }

    // ==========================================
    // HELPER
    // ==========================================

    function hashPosition(x, z, day) {
        return Math.abs(((x * 73856093) ^ (z * 19349669) ^ (day * 83492791)) % 2147483647);
    }

    function createRNG(seed) {
        let s = seed;
        return function() {
            s = (s * 1103515245 + 12345) & 0x7fffffff;
            return s / 0x7fffffff;
        };
    }

    function pickRandom(arr, rng) {
        const idx = Math.floor((rng ? rng() : Math.random()) * arr.length);
        return { ...arr[idx] };
    }

    function getCurrentBiome() {
        if (window.OverworldProps && typeof OverworldProps.getBiomeAtPosition === 'function') {
            const charGroup = window.Scene3D?.characterGroup;
            if (charGroup) {
                return OverworldProps.getBiomeAtPosition(charGroup.position.x, charGroup.position.z);
            }
        }
        return 'samtmoos';
    }

    function getBiomeNPCDensity(biome) {
        const densities = {
            samtmoos: 1.0,
            reich_der_drei: 1.5,  // Mehr NPCs in zivilisierten Gebieten
            heisse_duenen: 0.5,   // Weniger in der Wüste
            salzwind: 0.8,
            magmastroeme: 0.3,    // Sehr wenige in der Hölle
            gruenschlamm: 0.6,
            blitzebene: 0.7,
            tiefenhoehlen: 0.4,
            goetterfels: 1.2,     // Heiliger Ort = mehr Pilger
        };
        return densities[biome] || 0.8;
    }

    // ==========================================
    // TAGES-ZYKLUS
    // ==========================================

    function advanceDay() {
        worldState.day++;

        // Tote NPCs die >24h tot sind: manche kehren zurück (Ersatz)
        worldState.deadNPCs = worldState.deadNPCs.filter(d =>
            (Date.now() - d.diedAt) < 86400000
        );

        // Wirtschaft erholt sich langsam
        Object.keys(worldState.economyState).forEach(biome => {
            const eco = worldState.economyState[biome];
            if (eco.priceMultiplier && eco.priceMultiplier > 1.0) {
                eco.priceMultiplier = Math.max(1.0, eco.priceMultiplier - 0.05);
            }
        });

        saveWorldState();
        console.log(`🌅 Tag ${worldState.day} beginnt!`);
    }

    // ==========================================
    // AUTO-CHECK (Konsequenzen + Tageszeit)
    // ==========================================

    setInterval(() => {
        checkPendingConsequences();
    }, 30000); // Alle 30 Sekunden prüfen

    // ==========================================
    // EXPORT
    // ==========================================

    window.WorldEventGenerator = {
        // Kern-Generation
        generateWorldSlice,
        generateNPCsForSlice,
        checkForEvents,

        // Event-System
        executeEventChoice,
        WORLD_EVENTS,

        // Konsequenzen
        triggerConsequence,
        checkPendingConsequences,

        // NPC Templates
        NPC_TEMPLATES,

        // Welt-State
        getWorldState: () => ({ ...worldState }),
        advanceDay,
        getCurrentBiome,
        saveWorldState,

        // Helfer
        isNPCTypeDead,
        getBiomeNPCDensity,
    };

    console.log(`🌍 World Event Generator geladen! Tag ${worldState.day}`);
    console.log(`📖 ${WORLD_EVENTS.length} Events | ${worldState.eventHistory.length} History | ${worldState.deadNPCs.length} tote NPCs`);
    console.log(`⚡ ${worldState.consequences.filter(c => !c.executed).length} ausstehende Konsequenzen`);

})();
