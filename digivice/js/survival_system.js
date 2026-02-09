/**
 * NAJIKA WORLD - SURVIVAL + MOOD + LAW SYSTEM
 * =============================================
 * Kenshi / Rimworld / Elder Scrolls Hybrid.
 *
 * SURVIVAL: Hunger, Durst, Schlaf, Temperatur, Verletzungen
 * MOOD:     Rimworld-Style Stimmung basierend auf Aktionen
 * GESETZE:  Verschiedene Gesetze pro Region, Kopfgeld, Gefängnis
 *
 * ALLES greift ineinander:
 * - Hunger → Koch-Beruf wird wichtig
 * - Kälte → Schneider-Beruf wird wichtig
 * - Verletzungen → Heiler-Beruf wird wichtig
 * - Verbrechen → Konsequenzen, Flucht, Bestechung
 * - Stimmung → Unmoralische Taten drücken Mood, Psychopathen immun
 */

(function() {
    'use strict';

    // ==========================================
    // SURVIVAL STATE
    // ==========================================

    let survivalState = loadSurvivalState();

    function loadSurvivalState() {
        try {
            return JSON.parse(localStorage.getItem('najika_survival') || 'null') || createFreshState();
        } catch { return createFreshState(); }
    }

    function createFreshState() {
        return {
            // BASIC NEEDS (0-100, unter 20 = kritisch)
            hunger: 80,
            thirst: 80,
            energy: 100,      // Schlaf
            warmth: 50,       // Temperatur-Komfort (0=erfrierend, 100=überhitzend, 50=perfekt)

            // HEALTH
            hp: 100,
            maxHp: 100,
            injuries: [],      // Aktive Verletzungen
            diseases: [],      // Krankheiten

            // MOOD (Rimworld Style!) - Basis 50, modifiziert durch Moodlets
            baseMood: 50,
            moodlets: [],      // { id, name, icon, value, duration, expiresAt }

            // TRAITS (beeinflussen Mood-Reaktionen!)
            traits: [],        // z.B. 'psychopath', 'optimist', 'glutton'

            // KRIMINALITÄT
            bounties: {},      // { regionId: bountyAmount }
            crimesCommitted: [],
            jailTime: 0,       // Verbleibende Gefängnis-Minuten
            isWanted: false,

            // ZEITSTEMPEL
            lastUpdate: Date.now(),
            lastMeal: Date.now(),
            lastDrink: Date.now(),
            lastSleep: Date.now(),
        };
    }

    function saveSurvivalState() {
        localStorage.setItem('najika_survival', JSON.stringify(survivalState));
    }

    // ==========================================
    // BIOME-UMGEBUNGSEFFEKTE
    // ==========================================

    const BIOME_ENVIRONMENT = {
        samtmoos:       { temperature: 'mild',    hazard: null,           thirstRate: 1.0, description: 'Angenehm mild, feuchte Luft' },
        reich_der_drei: { temperature: 'mild',    hazard: null,           thirstRate: 1.0, description: 'Gemäßigtes Klima, gut bewohnt' },
        heisse_duenen:  { temperature: 'heiss',   hazard: 'hitzeschlag',  thirstRate: 2.5, description: '🌡️ Extreme Hitze! Durst ×2.5!' },
        salzwind:       { temperature: 'kuehl',   hazard: 'seekrankheit', thirstRate: 1.2, description: 'Salzige Meeresluft, kühl' },
        magmastroeme:   { temperature: 'extrem',  hazard: 'verbrennung',  thirstRate: 2.0, description: '🔥 Vulkanhitze! Permanenter Schaden ohne Schutz!' },
        gruenschlamm:   { temperature: 'feucht',  hazard: 'sumpffieber',  thirstRate: 0.8, description: '🤢 Giftige Dämpfe! Krankheitsrisiko!' },
        blitzebene:     { temperature: 'kalt',    hazard: 'blitzschlag',  thirstRate: 1.0, description: '⚡ Elektrische Stürme! Deckung suchen!' },
        tiefenhoehlen:  { temperature: 'kalt',    hazard: 'dunkelheit',   thirstRate: 0.7, description: '❄️ Kalt und dunkel. Wärme nötig!' },
        goetterfels:    { temperature: 'kalt',    hazard: null,           thirstRate: 1.0, description: '⛰️ Dünne Luft, heiliger Boden' },
    };

    // ==========================================
    // HUNGER & DURST SYSTEM
    // ==========================================

    function updateNeeds(deltaMinutes) {
        const biome = getCurrentBiome();
        const env = BIOME_ENVIRONMENT[biome] || BIOME_ENVIRONMENT.samtmoos;

        // Hunger: -1 pro 10 Minuten Spielzeit
        survivalState.hunger -= (deltaMinutes / 10) * 1.0;

        // Durst: Biom-abhängig!
        survivalState.thirst -= (deltaMinutes / 8) * env.thirstRate;

        // Energie: Sinkt langsam
        survivalState.energy -= (deltaMinutes / 30) * 1.0;

        // Clamp
        survivalState.hunger = Math.max(0, Math.min(100, survivalState.hunger));
        survivalState.thirst = Math.max(0, Math.min(100, survivalState.thirst));
        survivalState.energy = Math.max(0, Math.min(100, survivalState.energy));

        // Kritische Zustände
        if (survivalState.hunger <= 0) {
            applyDamage(1, 'Verhungern');
            addMoodlet('starving', '🍽️ Verhungere!', -15, 0); // permanent bis Essen
        }
        if (survivalState.thirst <= 0) {
            applyDamage(2, 'Verdursten');
            addMoodlet('dehydrated', '🏜️ Verdurste!', -20, 0);
        }
        if (survivalState.energy <= 10) {
            addMoodlet('exhausted', '😴 Todmüde!', -10, 0);
        }

        // Biom-Hazards
        checkBiomeHazards(biome, env, deltaMinutes);
    }

    function eat(foodItem) {
        const hungerRestore = foodItem.hungerRestore || 20;
        const quality = foodItem.quality || 1.0; // Koch-Skill beeinflusst das!
        const buffValue = foodItem.buff || null;

        survivalState.hunger = Math.min(100, survivalState.hunger + hungerRestore * quality);
        survivalState.lastMeal = Date.now();

        // Moodlets entfernen
        removeMoodlet('starving');

        // Gutes Essen = Mood-Buff!
        if (quality >= 2.0) {
            addMoodlet('great_meal', '🍖 Köstliches Mahl!', +10, 600000); // 10 Min
        } else if (quality <= 0.5) {
            addMoodlet('awful_meal', '🤮 Ekelhaftes Essen!', -5, 300000);
        }

        // Koch-Buff (vom Career System)
        if (buffValue && window.CareerSystem) {
            // Buff wird von Career System berechnet
        }

        saveSurvivalState();
        return { restored: hungerRestore * quality, currentHunger: survivalState.hunger };
    }

    function drink(waterItem) {
        const thirstRestore = waterItem.thirstRestore || 25;
        survivalState.thirst = Math.min(100, survivalState.thirst + thirstRestore);
        survivalState.lastDrink = Date.now();
        removeMoodlet('dehydrated');
        saveSurvivalState();
    }

    /**
     * SCHLAF-SYSTEM mit GEFAHR
     * Draußen schlafen = Überfall möglich! Wie im Wilden Westen.
     *
     * @param {number} hours - Stunden Schlaf
     * @param {object} options - {
     *   location: 'inn'|'tent_hidden'|'tent_fire'|'camp_open'|'caravan',
     *   hasGuard: false,   // Wache engagiert? (Eskorte-Beruf!)
     *   guardSkill: 0,     // Skill des Wächters
     * }
     */
    function sleep(hours, options = {}) {
        const location = options.location || 'camp_open';
        const hasGuard = options.hasGuard || false;
        const guardSkill = options.guardSkill || 0;

        // Überfall-Risiko basierend auf Schlafplatz
        const AMBUSH_RISK = {
            'inn':          0.00,  // Gasthof = 100% sicher
            'tent_hidden':  0.05,  // Verstecktes Zelt ohne Feuer = 5%
            'tent_fire':    0.25,  // Zelt MIT Feuer = sichtbar! 25%
            'camp_open':    0.40,  // Offenes Lager = 40% Überfall!
            'caravan':      0.15,  // Karawane mit Wachen = 15%
        };

        let ambushChance = AMBUSH_RISK[location] || 0.40;

        // Wache reduziert Risiko massiv
        if (hasGuard) {
            ambushChance *= Math.max(0.05, 1.0 - (guardSkill / 50)); // Skill 50 = fast 0%
        }

        // Biom-Modifikator
        const biome = getCurrentBiome();
        const dangerousBiomes = {
            'heisse_duenen': 1.3,
            'gruenschlamm': 1.5,
            'tiefenhoehlen': 1.8,
            'blitzebene': 1.2,
            'magmastroeme': 1.4,
        };
        ambushChance *= (dangerousBiomes[biome] || 1.0);

        // ÜBERFALL-CHECK für jede Schlafstunde!
        let wasAmbushed = false;
        let ambushHour = 0;
        for (let h = 0; h < hours; h++) {
            if (Math.random() < ambushChance) {
                wasAmbushed = true;
                ambushHour = h;
                break;
            }
        }

        if (wasAmbushed) {
            // Aufgewacht durch Überfall! Nur teilweise geschlafen
            const partialRestore = ambushHour * 12;
            survivalState.energy = Math.min(100, survivalState.energy + partialRestore);

            // Schaden und Diebstahl
            const ambushDamage = 10 + Math.floor(Math.random() * 20);
            applyDamage(ambushDamage, 'Überfall im Schlaf');
            addMoodlet('ambushed_sleep', '😱 Im Schlaf überfallen!', -15, 1800000);

            if (typeof notify === 'function') {
                notify(`⚔️ ÜBERFALL IM SCHLAF! ${ambushDamage} Schaden! Du wurdest beraubt!`, 'error');
            }

            // Wache hat den Spieler geweckt = weniger Schaden
            if (hasGuard) {
                if (typeof notify === 'function') {
                    notify(`🛡️ Deine Wache hat dich geweckt! Weniger Schaden genommen.`, 'info');
                }
            }

            saveSurvivalState();
            return {
                slept: ambushHour,
                ambushed: true,
                damage: ambushDamage,
                combat: true, // Trigger Kampf!
                enemies: ['bandit', 'desperado'],
            };
        }

        // Friedlicher Schlaf
        const restore = hours * 12; // 8h = volle Energie
        survivalState.energy = Math.min(100, survivalState.energy + restore);
        survivalState.lastSleep = Date.now();
        removeMoodlet('exhausted');

        // Schlaf heilt leichte Verletzungen
        survivalState.injuries = survivalState.injuries.filter(i => {
            if (i.severity === 'light') {
                i.healing -= hours * 10;
                return i.healing > 0;
            }
            return true;
        });

        // Mood basierend auf Schlafplatz
        if (location === 'inn') {
            addMoodlet('well_rested', '🛏️ Gemütliches Bett!', +8, 1800000);
        } else if (location === 'tent_hidden') {
            addMoodlet('well_rested', '⛺ Ruhiger Schlaf', +3, 1200000);
        } else {
            addMoodlet('rough_sleep', '😴 Unruhig geschlafen...', -2, 600000);
        }

        saveSurvivalState();
        return { slept: hours, ambushed: false };
    }

    // ==========================================
    // BIOME HAZARDS
    // ==========================================

    function checkBiomeHazards(biome, env, deltaMinutes) {
        if (!env.hazard) return;

        const chance = deltaMinutes * 0.005; // ~0.5% pro Minute

        switch (env.hazard) {
            case 'hitzeschlag':
                if (survivalState.warmth > 80 && Math.random() < chance) {
                    addInjury('hitzeschlag', '🌡️ Hitzeschlag!', 'medium', 60);
                    addMoodlet('overheating', '🥵 Überhitzt!', -8, 300000);
                }
                break;

            case 'verbrennung':
                if (Math.random() < chance * 2) {
                    applyDamage(3, 'Vulkanhitze');
                    if (Math.random() < 0.1) {
                        addInjury('verbrennung', '🔥 Verbrennung!', 'heavy', 120);
                    }
                }
                break;

            case 'sumpffieber':
                if (Math.random() < chance * 0.5) {
                    addDisease('sumpffieber', '🤢 Sumpffieber!', 60, { hp: -1, energy: -2 });
                    addMoodlet('sick', '🤮 Krank!', -12, 3600000);
                }
                break;

            case 'blitzschlag':
                if (Math.random() < chance * 0.3) {
                    applyDamage(25, 'Blitzschlag');
                    addInjury('blitzschlag', '⚡ Blitzschlag!', 'heavy', 90);
                    if (typeof notify === 'function') {
                        notify('⚡ BLITZSCHLAG! Du wurdest getroffen!', 'error');
                    }
                }
                break;

            case 'seekrankheit':
                if (survivalState.energy < 50 && Math.random() < chance) {
                    addMoodlet('seasick', '🤢 Seekrank!', -5, 600000);
                }
                break;

            case 'dunkelheit':
                if (!hasItem('fackel')) {
                    addMoodlet('darkness', '🕯️ Dunkelheit!', -8, 0);
                }
                break;
        }
    }

    // ==========================================
    // VERLETZUNGEN & KRANKHEITEN
    // ==========================================

    function addInjury(id, name, severity, healingTime) {
        if (survivalState.injuries.find(i => i.id === id)) return; // Kein Doppelt

        survivalState.injuries.push({
            id, name, severity, // 'light', 'medium', 'heavy', 'critical'
            healing: healingTime, // Minuten bis Heilung
            addedAt: Date.now(),
        });

        // Schwere Verletzungen = Bewegungs-Debuff
        if (severity === 'heavy' || severity === 'critical') {
            addMoodlet(`injury_${id}`, `🩹 ${name}`, -15, healingTime * 60000);
        }

        if (typeof notify === 'function') {
            notify(`🩹 Verletzung: ${name}`, 'warning');
        }

        saveSurvivalState();
    }

    function addDisease(id, name, duration, effects) {
        if (survivalState.diseases.find(d => d.id === id)) return;

        survivalState.diseases.push({
            id, name, duration,
            effects, // { hp: -1, energy: -2 } pro Minute
            addedAt: Date.now(),
            expiresAt: Date.now() + duration * 60000,
        });

        saveSurvivalState();
    }

    function applyDamage(amount, source) {
        survivalState.hp = Math.max(0, survivalState.hp - amount);
        if (survivalState.hp <= 0) {
            handleDeath(source);
        }
        saveSurvivalState();
    }

    function handleDeath(source) {
        if (typeof notify === 'function') {
            notify(`💀 Du bist gestorben! Ursache: ${source}`, 'error');
        }
        // TODO: Respawn-System, Loot-Drop, etc.
    }

    // ==========================================
    // MOOD SYSTEM (Rimworld Style!)
    // ==========================================
    // Mood = baseMood + Summe aller Moodlets
    // Unter 20 = Mental Break möglich!
    // Über 80 = Inspiration möglich!

    function getCurrentMood() {
        // Cleanup abgelaufene Moodlets
        const now = Date.now();
        survivalState.moodlets = survivalState.moodlets.filter(m =>
            m.expiresAt === 0 || m.expiresAt > now  // 0 = permanent
        );

        let mood = survivalState.baseMood;

        // Moodlets addieren
        survivalState.moodlets.forEach(m => {
            mood += m.value;
        });

        // Needs beeinflussen Mood
        if (survivalState.hunger < 20) mood -= 10;
        else if (survivalState.hunger > 80) mood += 3;

        if (survivalState.thirst < 20) mood -= 12;

        if (survivalState.energy < 20) mood -= 8;
        else if (survivalState.energy > 80) mood += 2;

        // Verletzungen
        survivalState.injuries.forEach(i => {
            if (i.severity === 'critical') mood -= 20;
            else if (i.severity === 'heavy') mood -= 12;
            else if (i.severity === 'medium') mood -= 6;
            else mood -= 2;
        });

        return Math.max(0, Math.min(100, Math.round(mood)));
    }

    function addMoodlet(id, name, value, duration) {
        // Traits modifizieren Moodlets!
        // HINWEIS: Keine 'psychopath'-Prüfung nötig weil es
        // keine automatischen Gewissensbisse gibt!
        // Wahre Freiheit = Jeder spielt wie er will.
        if (survivalState.traits.includes('optimist')) {
            if (value < 0) value = Math.ceil(value * 0.5); // Negative halbiert
            if (value > 0) value = Math.floor(value * 1.5); // Positive +50%
        }
        if (survivalState.traits.includes('pessimist')) {
            if (value < 0) value = Math.floor(value * 1.5);
            if (value > 0) value = Math.ceil(value * 0.5);
        }
        if (survivalState.traits.includes('glutton')) {
            if (id.includes('meal')) value = Math.floor(value * 1.5);
        }

        // Ersetze existierendes Moodlet gleicher ID
        survivalState.moodlets = survivalState.moodlets.filter(m => m.id !== id);

        survivalState.moodlets.push({
            id, name, value,
            duration,
            expiresAt: duration > 0 ? Date.now() + duration : 0,
        });

        saveSurvivalState();
    }

    function removeMoodlet(id) {
        survivalState.moodlets = survivalState.moodlets.filter(m => m.id !== id);
        saveSurvivalState();
    }

    // MOOD-KONSEQUENZEN
    function checkMoodBreaks() {
        const mood = getCurrentMood();

        if (mood <= 10 && Math.random() < 0.1) {
            // MENTAL BREAK!
            const breaks = [
                { name: '😱 Panikattacke!', effect: 'Kann 2 Minuten nicht kämpfen', duration: 120000 },
                { name: '😤 Wutausbruch!', effect: '+50% Schaden, -50% Verteidigung für 1 Minute', duration: 60000 },
                { name: '😢 Zusammenbruch!', effect: 'Bewegung verlangsamt, -30% auf alles', duration: 180000 },
                { name: '🏃 Fluchtinstinkt!', effect: 'Automatische Flucht aus nächstem Kampf', duration: 300000 },
            ];
            const mentalBreak = breaks[Math.floor(Math.random() * breaks.length)];

            if (typeof notify === 'function') {
                notify(`🧠 MENTAL BREAK: ${mentalBreak.name} - ${mentalBreak.effect}`, 'error');
            }

            return mentalBreak;
        }

        if (mood >= 90 && Math.random() < 0.05) {
            // INSPIRATION!
            const inspirations = [
                { name: '✨ Kampfgeist!', effect: '+30% Schaden für 5 Minuten', duration: 300000 },
                { name: '🎨 Kreativ-Schub!', effect: 'Nächstes Crafting = Meisterwerk', duration: 600000 },
                { name: '💪 Unaufhaltsam!', effect: 'Kein Stamina-Verbrauch für 3 Minuten', duration: 180000 },
                { name: '🧠 Geistesblitz!', effect: 'Doppelte XP für 10 Minuten', duration: 600000 },
            ];
            const inspiration = inspirations[Math.floor(Math.random() * inspirations.length)];

            if (typeof notify === 'function') {
                notify(`✨ INSPIRATION: ${inspiration.name} - ${inspiration.effect}`, 'success');
            }

            return inspiration;
        }

        return null;
    }

    // ==========================================
    // GRAUE MORAL - WAHRE FREIHEIT!
    // ==========================================
    // WICHTIG: Der Spielercharakter bekommt KEINE automatischen
    // Gewissensbisse! Er kann sein was er will - Organräuber,
    // Heiliger, Mörder, Retter. Das ist SEINE Entscheidung.
    //
    // Was sich ändert ist wie die WELT auf ihn reagiert:
    // - Fraktions-Reputation (FactionSystem)
    // - Kopfgeld (REGIONAL_LAWS)
    // - NPC-Reaktionen
    // - Preise
    //
    // Mood wird nur durch PHYSISCHES und UMGEBUNG beeinflusst:
    // - Gut geschlafen? Mood up
    // - Verletzt? Mood down
    // - Schöne Aussicht? Mood up
    // - Hunger? Mood down
    //
    // NICHT durch moralische Entscheidungen!
    // "Sei was du sein willst. Die Gesellschaft urteilt, nicht dein Kopf."

    function moralAction(actionType) {
        // GESELLSCHAFTLICHE REAKTIONEN (Fraktionen, Gesetze, Preise)
        // Mood bleibt UNBEEINFLUSST von moralischen Entscheidungen!

        switch (actionType) {
            case 'mord':
            case 'diebstahl':
            case 'organhandel':
            case 'verrat':
            case 'bestechung':
            case 'schmuggel':
                // KEINE Mood-Änderung! Dein Charakter ist frei!
                // Aber die Welt reagiert:
                if (window.FactionSystem) {
                    FactionSystem.performAction(actionType, { intensity: 8 });
                }
                break;

            // POSITIVES - Umgebungs-Mood (nicht moralisch!)
            case 'schoene_aussicht':
                addMoodlet('nice_view', '🌄 Schöne Aussicht!', +5, 600000);
                break;
            case 'musik_gehoert':
                addMoodlet('music', '🎵 Musik gehört!', +6, 600000);
                break;
            case 'freund_getroffen':
                addMoodlet('social', '👋 Nette Gesellschaft', +4, 900000);
                break;
            case 'hilfe':
            case 'rettung':
                // Gesellschaft reagiert positiv (Reputation steigt)
                if (window.FactionSystem) {
                    FactionSystem.performAction(actionType, { intensity: 5 });
                }
                break;
            case 'tod_gesehen':
                // Optional: Nur wenn Trait 'empathisch' vorhanden
                if (survivalState.traits.includes('empathisch')) {
                    addMoodlet('witnessed_death', '💀 Tod gesehen', -5, 900000);
                }
                break;
        }
    }

    // ==========================================
    // GESETZE & KRIMINALITÄT
    // ==========================================

    const REGIONAL_LAWS = {
        reich_der_drei: {
            name: 'Gesetze der Drei Häuser',
            strictness: 0.9,  // Sehr streng
            illegal: ['giftpilz', 'sumpfessenz', 'organprobe', 'schlafgift', 'verbotenes_buch', 'gefaelschte_papiere'],
            crimes: {
                diebstahl:    { bounty: 50,  jailTime: 30,  description: 'Diebstahl' },
                mord:         { bounty: 500, jailTime: 180, description: 'Mord' },
                schmuggel:    { bounty: 100, jailTime: 60,  description: 'Schmuggel verbotener Waren' },
                einbruch:     { bounty: 80,  jailTime: 45,  description: 'Einbruch' },
                angriff:      { bounty: 150, jailTime: 90,  description: 'Angriff auf Bürger' },
                bestechung:   { bounty: 75,  jailTime: 30,  description: 'Bestechung' },
                postman_angriff: { bounty: 1000, jailTime: 360, description: 'Angriff auf Postman-Ranger!' },
            },
            bribable: true,
            briberyCost: 2.0, // 200% der Strafe
        },
        heisse_duenen: {
            name: 'Wüstengesetz der Freien',
            strictness: 0.3,  // Locker
            illegal: ['organprobe'], // Nur das Schlimmste
            crimes: {
                diebstahl:    { bounty: 20,  jailTime: 10,  description: 'Diebstahl' },
                mord:         { bounty: 200, jailTime: 60,  description: 'Mord' },
                schmuggel:    { bounty: 0,   jailTime: 0,   description: 'Kein Vergehen hier!' },
                oase_stehlen: { bounty: 500, jailTime: 240, description: 'WASSER GESTOHLEN!' },
                postman_angriff: { bounty: 800, jailTime: 300, description: 'Angriff auf Postman-Ranger!' },
            },
            bribable: true,
            briberyCost: 1.0,
        },
        gruenschlamm: {
            name: 'Recht der Hexen',
            strictness: 0.2,  // Fast keine Gesetze
            illegal: [],       // Alles erlaubt!
            crimes: {
                mord:           { bounty: 50,  jailTime: 15, description: 'Mord' },
                hexen_jagen:    { bounty: 300, jailTime: 120, description: 'Hexenjagd!' },
                natur_zerstoeren: { bounty: 200, jailTime: 90, description: 'Naturzerstörung' },
                postman_angriff: { bounty: 600, jailTime: 180, description: 'Angriff auf Postman-Ranger!' },
            },
            bribable: false, // Hexen nehmen kein Gold
        },
        salzwind: {
            name: 'Hafengesetz',
            strictness: 0.5,
            illegal: ['organprobe', 'verbotenes_buch'],
            crimes: {
                diebstahl:    { bounty: 40,  jailTime: 20,  description: 'Diebstahl' },
                mord:         { bounty: 300, jailTime: 120, description: 'Mord' },
                schmuggel:    { bounty: 60,  jailTime: 30,  description: 'Schmuggel' },
                piraterie:    { bounty: 400, jailTime: 180, description: 'Piraterie!' },
                postman_angriff: { bounty: 800, jailTime: 300, description: 'Angriff auf Postman-Ranger!' },
            },
            bribable: true,
            briberyCost: 1.5,
        },
        magmastroeme: {
            name: 'Gesetz der Schmiede',
            strictness: 0.6,
            illegal: ['schlafgift', 'gefaelschte_papiere'],
            crimes: {
                diebstahl:    { bounty: 60,  jailTime: 30,  description: 'Diebstahl' },
                mord:         { bounty: 400, jailTime: 150, description: 'Mord' },
                pfusch:       { bounty: 200, jailTime: 90,  description: 'Pfuscharbeit verkauft!' },
                postman_angriff: { bounty: 800, jailTime: 300, description: 'Angriff auf Postman-Ranger!' },
            },
            bribable: true,
            briberyCost: 1.8,
        },
        goetterfels: {
            name: 'Heiliges Gesetz',
            strictness: 1.0,  // ABSOLUT STRENG
            illegal: ['giftpilz', 'sumpfessenz', 'organprobe', 'schlafgift', 'verbotenes_buch', 'gefaelschte_papiere'],
            crimes: {
                diebstahl:    { bounty: 100, jailTime: 60,  description: 'Diebstahl auf heiligem Boden' },
                mord:         { bounty: 1000, jailTime: 360, description: 'Mord auf heiligem Boden!' },
                kampf:        { bounty: 50,  jailTime: 30,  description: 'Kampf in der Safe Zone!' },
                goetterfels_entweihen: { bounty: 500, jailTime: 240, description: 'Entweihung!' },
                postman_angriff: { bounty: 1500, jailTime: 480, description: 'Angriff auf Postman-Ranger am Götterfels!' },
            },
            bribable: false, // Wächter sind NICHT bestechbar
        },
        // Biome ohne eigenes Rechtssystem = gesetzlos
        samtmoos:       null, // Wildnis, kein Gesetz
        blitzebene:     null, // Wildnis
        tiefenhoehlen:  null, // Gesetzlos
    };

    // ==========================================
    // VERBRECHEN BEGEHEN & KONSEQUENZEN
    // ==========================================

    function commitCrime(crimeType, region) {
        const law = REGIONAL_LAWS[region];
        if (!law) return { caught: false, reason: 'Gesetzlos hier! Keine Strafe.' };

        const crime = law.crimes[crimeType];
        if (!crime) return { caught: false, reason: 'Kein Vergehen in dieser Region.' };

        // Wurde man erwischt? Basierend auf Strictness + Tageszeit + Zeugen
        const catchChance = law.strictness * 0.7; // 70% der Strictness
        const caught = Math.random() < catchChance;

        // Mood-Effekt immer (Gewissen!)
        moralAction(crimeType);

        // Faction-Effekt
        if (window.FactionSystem) {
            FactionSystem.performAction(crimeType, { intensity: 8 });
        }

        if (!caught) {
            survivalState.crimesCommitted.push({
                type: crimeType,
                region,
                timestamp: Date.now(),
                caught: false,
            });
            saveSurvivalState();
            return { caught: false, reason: 'Niemand hat dich gesehen... diesmal.' };
        }

        // ERWISCHT!
        const bounty = crime.bounty;
        survivalState.bounties[region] = (survivalState.bounties[region] || 0) + bounty;
        survivalState.isWanted = true;

        survivalState.crimesCommitted.push({
            type: crimeType,
            region,
            timestamp: Date.now(),
            caught: true,
            bounty,
        });

        saveSurvivalState();

        if (typeof notify === 'function') {
            notify(`🚨 ERWISCHT! ${crime.description}! Kopfgeld: ${bounty}g`, 'error');
        }

        return {
            caught: true,
            crime: crime.description,
            bounty,
            jailTime: crime.jailTime,
            canBribe: law.bribable,
            bribeCost: law.bribable ? Math.floor(bounty * law.briberyCost) : 0,
        };
    }

    function payBounty(region) {
        const bounty = survivalState.bounties[region] || 0;
        if (bounty <= 0) return { success: true, reason: 'Kein Kopfgeld.' };

        // TODO: Gold vom Spieler abziehen
        survivalState.bounties[region] = 0;

        // Prüfe ob noch irgendwo Kopfgeld
        survivalState.isWanted = Object.values(survivalState.bounties).some(b => b > 0);

        saveSurvivalState();
        return { success: true, paid: bounty };
    }

    function bribeGuard(region) {
        const law = REGIONAL_LAWS[region];
        if (!law || !law.bribable) return { success: false, reason: 'Bestechung nicht möglich hier.' };

        const bounty = survivalState.bounties[region] || 0;
        const cost = Math.floor(bounty * law.briberyCost);

        // Mood-Effekt
        moralAction('bestechung');

        // Faction-Effekt
        if (window.FactionSystem) {
            FactionSystem.performAction('bestechung', { intensity: 3 });
        }

        survivalState.bounties[region] = 0;
        survivalState.isWanted = Object.values(survivalState.bounties).some(b => b > 0);

        saveSurvivalState();
        return { success: true, cost, reason: 'Die Wache schaut weg...' };
    }

    function goToJail(region, minutes) {
        survivalState.jailTime = minutes;

        // Im Gefängnis: Hunger/Durst sinkt langsamer
        addMoodlet('imprisoned', '🔒 Eingesperrt!', -20, minutes * 60000);

        // Kopfgeld in dieser Region gelöscht (Strafe abgesessen)
        survivalState.bounties[region] = 0;
        survivalState.isWanted = Object.values(survivalState.bounties).some(b => b > 0);

        saveSurvivalState();

        if (typeof notify === 'function') {
            notify(`🔒 Im Gefängnis für ${minutes} Minuten. Verbrechen in ${region} bezahlt.`, 'warning');
        }
    }

    function escapeJail() {
        if (survivalState.jailTime <= 0) return { success: false };

        // 30% Basis-Chance, +Skill
        const chance = 0.3;
        if (Math.random() < chance) {
            survivalState.jailTime = 0;
            removeMoodlet('imprisoned');
            addMoodlet('escaped', '🏃 Ausgebrochen!', +5, 300000);

            // Aber: Höheres Kopfgeld!
            const regions = Object.keys(survivalState.bounties);
            regions.forEach(r => {
                if (survivalState.bounties[r] > 0) {
                    survivalState.bounties[r] *= 2;
                }
            });

            saveSurvivalState();
            return { success: true, reason: 'Du bist ausgebrochen! Aber das Kopfgeld ist gestiegen!' };
        }

        addMoodlet('failed_escape', '😤 Fluchtversuch gescheitert', -10, 600000);
        survivalState.jailTime += 30; // Strafe erhöht

        saveSurvivalState();
        return { success: false, reason: 'Erwischt! Strafe erhöht um 30 Minuten.' };
    }

    // ==========================================
    // KOPFGELD VERFÄLLT LANGSAM
    // ==========================================

    function dailyLawUpdate() {
        // Kopfgeld verfällt (-5% pro Tag)
        Object.keys(survivalState.bounties).forEach(region => {
            if (survivalState.bounties[region] > 0) {
                survivalState.bounties[region] = Math.max(0,
                    Math.floor(survivalState.bounties[region] * 0.95));
            }
        });

        survivalState.isWanted = Object.values(survivalState.bounties).some(b => b > 0);

        // Gefängniszeit reduzieren (1 Tag = -60 Minuten)
        if (survivalState.jailTime > 0) {
            survivalState.jailTime = Math.max(0, survivalState.jailTime - 60);
            if (survivalState.jailTime <= 0) {
                removeMoodlet('imprisoned');
                if (typeof notify === 'function') {
                    notify('🔓 Freigelassen! Strafe abgesessen.', 'success');
                }
            }
        }

        // Krankheiten heilen
        const now = Date.now();
        survivalState.diseases = survivalState.diseases.filter(d => d.expiresAt > now);

        // Verletzungen heilen (1 Heilung pro Tag)
        survivalState.injuries.forEach(i => {
            i.healing = Math.max(0, i.healing - 60);
        });
        survivalState.injuries = survivalState.injuries.filter(i => i.healing > 0);

        saveSurvivalState();
    }

    // ==========================================
    // HELPER
    // ==========================================

    function getCurrentBiome() {
        if (window.WorldEventGenerator) {
            return WorldEventGenerator.getCurrentBiome();
        }
        return 'samtmoos';
    }

    function hasItem(itemId) {
        // TODO: Integration mit Inventar-System
        return false;
    }

    // Haupt-Update (alle 60 Sekunden aufrufen)
    function update() {
        const now = Date.now();
        const delta = (now - survivalState.lastUpdate) / 60000; // Minuten seit letztem Update
        survivalState.lastUpdate = now;

        if (delta > 0 && delta < 60) { // Max 60 Minuten auf einmal
            updateNeeds(delta);
        }

        // Krankheits-Effekte
        survivalState.diseases.forEach(d => {
            if (d.effects.hp) applyDamage(Math.abs(d.effects.hp) * 0.1, d.name);
            if (d.effects.energy) survivalState.energy = Math.max(0, survivalState.energy - Math.abs(d.effects.energy) * 0.1);
        });

        // Mood-Check
        checkMoodBreaks();

        saveSurvivalState();
    }

    // Auto-Update alle 60 Sekunden
    setInterval(update, 60000);

    // ==========================================
    // EXPORT
    // ==========================================

    window.SurvivalSystem = {
        // Needs
        eat,
        drink,
        sleep,
        getNeeds: () => ({
            hunger: survivalState.hunger,
            thirst: survivalState.thirst,
            energy: survivalState.energy,
            hp: survivalState.hp,
            maxHp: survivalState.maxHp,
        }),

        // Mood
        getCurrentMood,
        addMoodlet,
        removeMoodlet,
        moralAction,
        getMoodlets: () => [...survivalState.moodlets],

        // Traits
        addTrait: (trait) => { survivalState.traits.push(trait); saveSurvivalState(); },
        hasTrait: (trait) => survivalState.traits.includes(trait),
        getTraits: () => [...survivalState.traits],

        // Health
        addInjury,
        addDisease,
        applyDamage,
        getInjuries: () => [...survivalState.injuries],
        getDiseases: () => [...survivalState.diseases],

        // Law
        commitCrime,
        payBounty,
        bribeGuard,
        goToJail,
        escapeJail,
        getBounties: () => ({ ...survivalState.bounties }),
        isWanted: () => survivalState.isWanted,
        REGIONAL_LAWS,

        // Environment
        BIOME_ENVIRONMENT,

        // Updates
        update,
        dailyLawUpdate,

        // State
        getState: () => ({ ...survivalState }),
        saveSurvivalState,
    };

    const mood = getCurrentMood();
    const moodIcon = mood > 70 ? '😊' : mood > 40 ? '😐' : mood > 20 ? '😰' : '😱';
    console.log(`🏕️ Survival System geladen! Mood: ${moodIcon} ${mood}/100`);
    console.log(`🍞 Hunger: ${Math.round(survivalState.hunger)} | 💧 Durst: ${Math.round(survivalState.thirst)} | ⚡ Energie: ${Math.round(survivalState.energy)}`);
    console.log(`⚖️ ${Object.keys(REGIONAL_LAWS).filter(r => REGIONAL_LAWS[r]).length} Regionen mit Gesetzen | Gesucht: ${survivalState.isWanted ? 'JA!' : 'Nein'}`);

})();
