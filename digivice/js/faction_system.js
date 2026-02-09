/**
 * NAJIKA WORLD - FACTION SYSTEM (Fallout NV / Kenshi Style)
 * ==========================================================
 * GRAUE MORAL. Keine Fraktion ist rein gut oder böse.
 * Jede hat nachvollziehbare Gründe. Jede hat dunkle Seiten.
 *
 * Inspiriert von:
 * - Fallout NV: NCR vs Legion vs House vs Yes Man - alle haben Recht UND Unrecht
 * - Kenshi: Holy Nation vs Shek vs UC - Sklaverei als Wirtschaftsfaktor
 * - Rimworld: Unmoralische Taten bringen echte Vorteile
 * - Mount & Blade 2: Fraktionen bekriegen sich ohne den Spieler
 *
 * "Keine guten oder bösen Seiten. Nur verschiedene Arten zu überleben." - Najika World
 */

(function() {
    'use strict';

    // ==========================================
    // FRAKTIONEN DER WELT
    // ==========================================
    // Jede Fraktion hat eine HELLE und eine DUNKLE Seite.
    // Der Spieler MUSS wählen - es gibt kein perfektes Ende.

    const FACTIONS = {
        // === REICH DER DREI (3 rivalisierende Familien) ===
        haus_silberdorn: {
            id: 'haus_silberdorn',
            name: 'Haus Silberdorn',
            icon: '🥈',
            region: 'reich_der_drei',
            category: 'adel',
            color: '#C0C0C0',
            // HELLE SEITE: Ordnung, Sicherheit, Wohlstand
            lightSide: 'Sicherheit durch Gesetze. Handelsrouten sind geschützt. Bürger leben komfortabel.',
            // DUNKLE SEITE: Klassengesellschaft, Unterdrückung der Armen
            darkSide: 'Strikte Klassenhierarchie. Arme werden ausgebeutet. Wer nicht zahlt, fliegt raus.',
            allies: [],
            enemies: ['haus_kupferklinge', 'schwarzmarkt_gilde'],
            neutral: ['haus_eiseneid', 'postman_orden'],
            values: ['ordnung', 'handel', 'tradition'],
            hatedActions: ['diebstahl', 'mord_in_stadt', 'schmuggel'],
            lovedActions: ['handel', 'gesetz_durchsetzen', 'banditen_jagen'],
        },
        haus_kupferklinge: {
            id: 'haus_kupferklinge',
            name: 'Haus Kupferklinge',
            icon: '⚔️',
            region: 'reich_der_drei',
            category: 'adel',
            color: '#B87333',
            lightSide: 'Militärische Stärke. Beschützen die Grenzen vor Monstern und Banditen.',
            darkSide: 'Expansionistisch. Annektieren kleinere Dörfer. Zwangsrekrutierung.',
            allies: [],
            enemies: ['haus_silberdorn', 'wuestenfreie'],
            neutral: ['haus_eiseneid', 'goetterfels_waechter'],
            values: ['staerke', 'ehre', 'expansion'],
            hatedActions: ['feigheit', 'verrat', 'desertion'],
            lovedActions: ['kampf', 'eroberung', 'heldentum'],
        },
        haus_eiseneid: {
            id: 'haus_eiseneid',
            name: 'Haus Eiseneid',
            icon: '🔨',
            region: 'reich_der_drei',
            category: 'adel',
            color: '#434343',
            lightSide: 'Meisterhandwerker. Stellen die besten Waffen und Rüstungen her. Fair zu Arbeitern.',
            darkSide: 'Monopolistisch. Kontrollieren Ressourcen. Konkurrenten werden "beseitigt".',
            allies: ['schmiede_gilde'],
            enemies: ['schwarzmarkt_gilde'],
            neutral: ['haus_silberdorn', 'haus_kupferklinge'],
            values: ['handwerk', 'qualitaet', 'monopol'],
            hatedActions: ['billigware', 'ressourcendiebstahl', 'pfusch'],
            lovedActions: ['schmieden', 'qualitaet', 'handelsabkommen'],
        },

        // === ÜBERREGIONALE FRAKTIONEN ===
        postman_orden: {
            id: 'postman_orden',
            name: 'Orden der Postman-Ranger',
            icon: '📮',
            region: '*', // Überall
            category: 'orden',
            color: '#8B4513',
            lightSide: 'Verbinden die Welt. Bringen Nachrichten, Medizin, Hoffnung. Respektiert von allen.',
            darkSide: 'Wissen ALLES. Lesen manchmal Briefe. Spielen Fraktionen gegeneinander aus.',
            allies: ['goetterfels_waechter'],
            enemies: ['banditen_bund'],
            neutral: ['haus_silberdorn', 'haus_kupferklinge', 'haus_eiseneid'],
            values: ['verbindung', 'pflicht', 'neutralitaet'],
            hatedActions: ['postman_angriff', 'lieferung_stehlen', 'luegen'],
            lovedActions: ['postman_beruf', 'lieferung_abschliessen', 'nachrichten_ueberbringen'],
        },
        goetterfels_waechter: {
            id: 'goetterfels_waechter',
            name: 'Wächter des Götterfels',
            icon: '⛰️',
            region: 'goetterfels',
            category: 'orden',
            color: '#FFD700',
            lightSide: 'Hüten uraltes Wissen. Beschützen die Zeitstadt. Neutral in Konflikten.',
            darkSide: 'Elitär. Halten Wissen zurück. Opfern Einzelne für "das große Ganze".',
            allies: ['postman_orden'],
            enemies: ['schatten_kult'],
            neutral: ['haus_silberdorn', 'wuestenfreie'],
            values: ['wissen', 'balance', 'zeitstadt'],
            hatedActions: ['zeitstadt_missbrauch', 'goetterfels_entweihen'],
            lovedActions: ['wissen_suchen', 'goetterfels_beschuetzen', 'zeitwandler_jagen'],
        },

        // === UNTERWELT ===
        schwarzmarkt_gilde: {
            id: 'schwarzmarkt_gilde',
            name: 'Schwarzmarkt-Gilde',
            icon: '🎭',
            region: '*',
            category: 'unterwelt',
            color: '#4A0080',
            lightSide: 'Bieten verbotene Waren die Leben retten. Helfen Flüchtlingen über Grenzen.',
            darkSide: 'Drogenhandel. Erpressung. Organhandel. Alles hat seinen Preis.',
            allies: ['banditen_bund'],
            enemies: ['haus_silberdorn', 'haus_eiseneid'],
            neutral: ['wuestenfreie', 'sumpfhexen'],
            values: ['profit', 'freiheit', 'geheimhaltung'],
            hatedActions: ['verrat_an_gilde', 'mit_wachen_reden'],
            lovedActions: ['schmuggel', 'hehlerei', 'bestechung', 'organhandel'],
        },
        banditen_bund: {
            id: 'banditen_bund',
            name: 'Bund der Freien Klingen',
            icon: '🗡️',
            region: '*',
            category: 'unterwelt',
            color: '#8B0000',
            lightSide: 'Freiheitskämpfer! Gegen Unterdrückung. Robin Hood unter den Banditen.',
            darkSide: 'Brutal. Überfallen Unschuldige. Schutzgeld-Erpressung. Morden für Gold.',
            allies: ['schwarzmarkt_gilde'],
            enemies: ['postman_orden', 'haus_kupferklinge'],
            neutral: [],
            values: ['freiheit', 'staerke', 'eigennutz'],
            hatedActions: ['mit_adel_verbunden', 'schwach_sein', 'gesetze_befolgen'],
            lovedActions: ['raubueberfall', 'flucht', 'banditen_helfen'],
        },

        // === REGIONALE FRAKTIONEN ===
        wuestenfreie: {
            id: 'wuestenfreie',
            name: 'Freies Volk der Dünen',
            icon: '🏜️',
            region: 'heisse_duenen',
            category: 'regional',
            color: '#DAA520',
            lightSide: 'Leben im Einklang mit der Wüste. Gastfreundlich. Teilen mit Reisenden.',
            darkSide: 'Hassen Außenseiter die bleiben wollen. Ritualmorde bei Vollmond.',
            allies: [],
            enemies: ['haus_kupferklinge'],
            neutral: ['postman_orden', 'sumpfhexen'],
            values: ['wueste', 'tradition', 'freiheit'],
            hatedActions: ['wueste_verschmutzen', 'oase_stehlen', 'kulturlosigkeit'],
            lovedActions: ['wuestenhandel', 'rituale_ehren', 'sandwurm_zaehmen'],
        },
        sumpfhexen: {
            id: 'sumpfhexen',
            name: 'Hexenzirkel des Grünschlamms',
            icon: '🧙',
            region: 'gruenschlamm',
            category: 'regional',
            color: '#228B22',
            lightSide: 'Heilerinnen. Bewahren altes Kräuterwissen. Retten Todkranke.',
            darkSide: 'Experimente an Lebenden. Gift-Handel. Flüche gegen Feinde.',
            allies: [],
            enemies: [],
            neutral: ['goetterfels_waechter', 'schwarzmarkt_gilde'],
            values: ['natur', 'wissen', 'gift_und_heilung'],
            hatedActions: ['natur_zerstoeren', 'hexen_jagen'],
            lovedActions: ['kraeuter_sammeln', 'gift_brauen', 'heilen', 'alchemie'],
        },
        schatten_kult: {
            id: 'schatten_kult',
            name: 'Kult der Tiefenschatten',
            icon: '🕳️',
            region: 'tiefenhoehlen',
            category: 'geheim',
            color: '#1a1a2e',
            lightSide: 'Suchen die Wahrheit hinter der Realität. Philosophen des Abgrunds.',
            darkSide: 'Wollen die Zeitstadt öffnen um "die Welt zu erneuern" (= zerstören).',
            allies: [],
            enemies: ['goetterfels_waechter'],
            neutral: ['schwarzmarkt_gilde'],
            values: ['chaos', 'wahrheit', 'zerstoerung_als_erneuerung'],
            hatedActions: ['ordnung', 'goetterfels_schuetzen'],
            lovedActions: ['chaos_saeen', 'zeitstadt_oeffnen', 'rituale'],
        },
        schmiede_gilde: {
            id: 'schmiede_gilde',
            name: 'Gilde der Meisterschmiede',
            icon: '🔥',
            region: 'magmastroeme',
            category: 'handwerk',
            color: '#FF4500',
            lightSide: 'Legendäre Waffen. Ehrenvolles Handwerk. Feuer reinigt und formt.',
            darkSide: 'Waffenlieferanten für ALLE Seiten. Profitieren vom Krieg.',
            allies: ['haus_eiseneid'],
            enemies: [],
            neutral: ['haus_kupferklinge', 'banditen_bund'],
            values: ['feuer', 'handwerk', 'neutralitaet_im_handel'],
            hatedActions: ['billigwaffen', 'pfusch'],
            lovedActions: ['schmieden', 'magma_ernten', 'meisterwerk_schaffen'],
        },
    };

    // ==========================================
    // FRAKTIONS-REPUTATION (Fallout NV Style!)
    // ==========================================
    // Jede Fraktion hat FAME (Bekanntheit) und INFAMY (Berüchtigung)
    // BEIDES steigt unabhängig! Man kann berühmt UND berüchtigt sein.

    const REP_LEVELS = [
        { threshold: 0,   name: 'Unbekannt',      icon: '❓', effect: 'Keine Reaktion' },
        { threshold: 10,  name: 'Akzeptiert',      icon: '👋', effect: 'Grundhandel möglich' },
        { threshold: 25,  name: 'Geschätzt',       icon: '😊', effect: '-10% Preise, mehr Quests' },
        { threshold: 50,  name: 'Bewundert',       icon: '⭐', effect: '-20% Preise, exklusive Quests' },
        { threshold: 75,  name: 'Verehrt',         icon: '🏆', effect: '-30% Preise, Fraktion hilft im Kampf' },
        { threshold: 100, name: 'Vergöttert',      icon: '👑', effect: 'Führungsposition, beste Preise, NPC-Begleiter' },
    ];

    const INFAMY_LEVELS = [
        { threshold: 0,   name: 'Neutral',         icon: '➖', effect: 'Keine negative Reaktion' },
        { threshold: 10,  name: 'Verdächtig',       icon: '👀', effect: 'Wachen beobachten dich' },
        { threshold: 25,  name: 'Unerwünscht',      icon: '🚫', effect: '+20% Preise, kein Zutritt zu Bereichen' },
        { threshold: 50,  name: 'Feind',            icon: '⚔️', effect: 'Angriff bei Sichtkontakt!' },
        { threshold: 75,  name: 'Erzfeind',         icon: '💀', effect: 'Kopfgeld, Assassinen werden geschickt' },
        { threshold: 100, name: 'Nemesis',          icon: '☠️', effect: 'Kill on Sight, Alliierte helfen Fraktion' },
    ];

    // ==========================================
    // SPIELER-RUF MANAGEMENT
    // ==========================================

    let factionState = loadFactionState();

    function loadFactionState() {
        try {
            return JSON.parse(localStorage.getItem('najika_faction_state') || 'null') || createFreshFactionState();
        } catch { return createFreshFactionState(); }
    }

    function createFreshFactionState() {
        const state = {
            playerReputation: {},  // { factionId: { fame: 0, infamy: 0 } }
            factionRelations: {},  // Dynamische Beziehungen (können sich ändern!)
            factionWars: [],       // Aktive Kriege zwischen Fraktionen
            factionEvents: [],     // Was ist zwischen Fraktionen passiert
            completedQuests: {},   // { factionId: [questIds] }
            playerAlliance: null,  // Wenn Spieler sich entschieden hat
        };

        // Initialisiere Reputation für alle Fraktionen
        Object.keys(FACTIONS).forEach(id => {
            state.playerReputation[id] = { fame: 0, infamy: 0 };
        });

        return state;
    }

    function saveFactionState() {
        localStorage.setItem('najika_faction_state', JSON.stringify(factionState));
    }

    // ==========================================
    // REPUTATION ÄNDERN
    // ==========================================

    function changeFame(factionId, amount) {
        if (!factionState.playerReputation[factionId]) return;
        const rep = factionState.playerReputation[factionId];
        rep.fame = Math.max(0, Math.min(100, rep.fame + amount));

        // RIPPLE EFFECT: Feinde der Fraktion mögen dich weniger!
        const faction = FACTIONS[factionId];
        if (faction && amount > 0) {
            faction.enemies.forEach(enemyId => {
                if (factionState.playerReputation[enemyId]) {
                    factionState.playerReputation[enemyId].infamy += Math.floor(amount * 0.3);
                    factionState.playerReputation[enemyId].infamy = Math.min(100, factionState.playerReputation[enemyId].infamy);
                }
            });
            // Alliierte mögen dich mehr
            faction.allies.forEach(allyId => {
                if (factionState.playerReputation[allyId]) {
                    factionState.playerReputation[allyId].fame += Math.floor(amount * 0.2);
                    factionState.playerReputation[allyId].fame = Math.min(100, factionState.playerReputation[allyId].fame);
                }
            });
        }

        saveFactionState();
        checkReputationThresholds(factionId);
    }

    function changeInfamy(factionId, amount) {
        if (!factionState.playerReputation[factionId]) return;
        const rep = factionState.playerReputation[factionId];
        rep.infamy = Math.max(0, Math.min(100, rep.infamy + amount));

        // RIPPLE: Feinde der Fraktion finden dich gut wenn du deren Feind bist!
        const faction = FACTIONS[factionId];
        if (faction && amount > 0) {
            faction.enemies.forEach(enemyId => {
                if (factionState.playerReputation[enemyId]) {
                    factionState.playerReputation[enemyId].fame += Math.floor(amount * 0.15);
                    factionState.playerReputation[enemyId].fame = Math.min(100, factionState.playerReputation[enemyId].fame);
                }
            });
        }

        saveFactionState();
        checkReputationThresholds(factionId);
    }

    // Aktion ändert Ruf bei ALLEN relevanten Fraktionen
    function performAction(actionType, context) {
        Object.keys(FACTIONS).forEach(fid => {
            const f = FACTIONS[fid];
            if (f.lovedActions.includes(actionType)) {
                changeFame(fid, context?.intensity || 5);
            }
            if (f.hatedActions.includes(actionType)) {
                changeInfamy(fid, context?.intensity || 5);
            }
        });
    }

    function checkReputationThresholds(factionId) {
        const rep = factionState.playerReputation[factionId];
        const faction = FACTIONS[factionId];
        if (!rep || !faction) return;

        const fameLevel = getRepLevel(rep.fame, REP_LEVELS);
        const infamyLevel = getRepLevel(rep.infamy, INFAMY_LEVELS);

        // Notifications bei wichtigen Schwellen
        if (rep.fame >= 50 && !rep._notified50fame) {
            rep._notified50fame = true;
            if (typeof notify === 'function') {
                notify(`⭐ ${faction.name} bewundert dich! Exklusive Quests verfügbar.`, 'success');
            }
        }
        if (rep.infamy >= 50 && !rep._notified50infamy) {
            rep._notified50infamy = true;
            if (typeof notify === 'function') {
                notify(`⚔️ ${faction.name} betrachtet dich als FEIND! Vorsicht!`, 'error');
            }
        }
    }

    function getRepLevel(value, levels) {
        let result = levels[0];
        for (const level of levels) {
            if (value >= level.threshold) result = level;
        }
        return result;
    }

    // ==========================================
    // FRAKTIONSKRIEGE (passieren OHNE den Spieler!)
    // ==========================================

    function checkFactionConflicts() {
        // Einmal pro Spieltag: Fraktionen können in Konflikt geraten
        const possibleConflicts = [];

        Object.keys(FACTIONS).forEach(fid => {
            const faction = FACTIONS[fid];
            faction.enemies.forEach(enemyId => {
                // Existiert bereits ein Krieg?
                const existingWar = factionState.factionWars.find(w =>
                    (w.attacker === fid && w.defender === enemyId) ||
                    (w.attacker === enemyId && w.defender === fid)
                );
                if (!existingWar && Math.random() < 0.05) { // 5% pro Tag pro Feindpaar
                    possibleConflicts.push({ attacker: fid, defender: enemyId });
                }
            });
        });

        possibleConflicts.forEach(conflict => {
            startFactionWar(conflict.attacker, conflict.defender);
        });
    }

    function startFactionWar(attackerId, defenderId) {
        const war = {
            attacker: attackerId,
            defender: defenderId,
            startedDay: getWorldDay(),
            intensity: 1, // 1-5
            battles: [],
            winner: null,
        };

        factionState.factionWars.push(war);

        const attacker = FACTIONS[attackerId];
        const defender = FACTIONS[defenderId];

        if (typeof notify === 'function') {
            notify(`⚔️ KRIEG! ${attacker.name} greift ${defender.name} an!`, 'warning');
        }

        factionState.factionEvents.push({
            type: 'war_started',
            factions: [attackerId, defenderId],
            day: getWorldDay(),
            description: `${attacker.name} hat ${defender.name} den Krieg erklärt!`,
        });

        saveFactionState();
    }

    function advanceFactionWars() {
        factionState.factionWars.forEach(war => {
            if (war.winner) return;

            // Krieg eskaliert oder deeskaliert
            war.intensity += (Math.random() > 0.6 ? 0.5 : -0.3);
            war.intensity = Math.max(0, Math.min(5, war.intensity));

            // Zufällige Schlachten
            if (Math.random() < 0.3) {
                const attackerWins = Math.random() < 0.5;
                war.battles.push({
                    day: getWorldDay(),
                    winner: attackerWins ? war.attacker : war.defender,
                    location: getRandomWarLocation(war),
                });

                // Auswirkungen auf die Welt
                applyWarEffects(war, attackerWins);
            }

            // Krieg endet?
            if (war.intensity <= 0 || war.battles.length > 10) {
                const attackerWins = war.battles.filter(b => b.winner === war.attacker).length;
                const defenderWins = war.battles.filter(b => b.winner === war.defender).length;
                war.winner = attackerWins > defenderWins ? war.attacker : war.defender;

                const winnerFaction = FACTIONS[war.winner];
                if (typeof notify === 'function') {
                    notify(`🏳️ Krieg vorbei! ${winnerFaction.name} hat gewonnen!`, 'info');
                }

                factionState.factionEvents.push({
                    type: 'war_ended',
                    winner: war.winner,
                    day: getWorldDay(),
                });
            }
        });

        // Abgeschlossene Kriege aufräumen (nach 7 Tagen)
        factionState.factionWars = factionState.factionWars.filter(w =>
            !w.winner || (getWorldDay() - (w.battles[w.battles.length - 1]?.day || w.startedDay)) < 7
        );

        saveFactionState();
    }

    function applyWarEffects(war, attackerWins) {
        // Kriege beeinflussen die Welt!
        const loser = attackerWins ? war.defender : war.attacker;
        const loserFaction = FACTIONS[loser];

        // Preise steigen in der Region des Verlierers
        if (loserFaction.region !== '*' && window.WorldEventGenerator) {
            const wState = WorldEventGenerator.getWorldState();
            if (!wState.economyState) wState.economyState = {};
            if (!wState.economyState[loserFaction.region]) wState.economyState[loserFaction.region] = {};
            wState.economyState[loserFaction.region].priceMultiplier =
                (wState.economyState[loserFaction.region].priceMultiplier || 1.0) + 0.1;
            wState.economyState[loserFaction.region].reason = `Krieg zwischen Fraktionen treibt Preise hoch`;
            WorldEventGenerator.saveWorldState();
        }

        // Händler auf Straßen der Region sterben
        if (Math.random() < 0.2 && window.WorldEventGenerator) {
            WorldEventGenerator.triggerConsequence({
                type: 'trader_missing',
                delay: 0,
                description: `Ein Händler wurde im Krieg zwischen ${FACTIONS[war.attacker].name} und ${FACTIONS[war.defender].name} getötet.`,
            });
        }
    }

    function getRandomWarLocation(war) {
        const attacker = FACTIONS[war.attacker];
        const defender = FACTIONS[war.defender];
        const regions = [attacker.region, defender.region].filter(r => r !== '*');
        return regions[Math.floor(Math.random() * regions.length)] || 'grenzgebiet';
    }

    // ==========================================
    // GRAUE MORAL ENTSCHEIDUNGEN
    // ==========================================

    // Aktionen die bei verschiedenen Fraktionen UNTERSCHIEDLICH bewertet werden
    const MORAL_DILEMMAS = {
        organhandel: {
            description: 'Organe auf dem Schwarzmarkt verkaufen',
            reactions: {
                schwarzmarkt_gilde: { fame: +15, infamy: 0 },      // Geschäft ist Geschäft!
                haus_silberdorn:    { fame: 0, infamy: +20 },       // Barbarisch!
                sumpfhexen:         { fame: +5, infamy: 0 },        // Ingredienzien!
                goetterfels_waechter: { fame: 0, infamy: +15 },     // Gegen die Ordnung!
            },
            goldReward: 500,
            karmaHit: -5,
        },
        sklaverei_befreien: {
            description: 'Sklaven aus Haus Kupferklinge befreien',
            reactions: {
                haus_kupferklinge:  { fame: 0, infamy: +25 },       // VERRAT!
                banditen_bund:      { fame: +15, infamy: 0 },       // Freiheitsheld!
                wuestenfreie:       { fame: +10, infamy: 0 },       // Freiheit über alles!
                haus_silberdorn:    { fame: +5, infamy: +5 },       // Hmm, kompliziert...
            },
            goldReward: 0,
            karmaHit: +3,
        },
        bestechung: {
            description: 'Wachen bestechen um Zugang zu erhalten',
            reactions: {
                haus_silberdorn:    { fame: 0, infamy: +10 },
                schwarzmarkt_gilde: { fame: +5, infamy: 0 },
                postman_orden:      { fame: 0, infamy: +5 },
            },
            goldReward: 0,
            karmaHit: -1,
        },
        kriegspartei_waehlen: {
            description: 'Sich auf eine Seite in einem Fraktionskrieg stellen',
            // Wird dynamisch berechnet basierend auf dem aktuellen Krieg
            goldReward: 200,
            karmaHit: 0, // Keine Fraktion ist per se falsch
        },
        schmuggel: {
            description: 'Verbotene Waren über Grenzen schmuggeln',
            reactions: {
                schwarzmarkt_gilde: { fame: +10, infamy: 0 },
                haus_silberdorn:    { fame: 0, infamy: +15 },
                banditen_bund:      { fame: +5, infamy: 0 },
                postman_orden:      { fame: 0, infamy: +8 },
            },
            goldReward: 300,
            karmaHit: -2,
        },
        gift_verkaufen: {
            description: 'Gifte der Sumpfhexen an Meistbietende verkaufen',
            reactions: {
                sumpfhexen:         { fame: +8, infamy: 0 },        // Gutes Geschäft!
                haus_silberdorn:    { fame: 0, infamy: +10 },
                schwarzmarkt_gilde: { fame: +10, infamy: 0 },
                goetterfels_waechter: { fame: 0, infamy: +5 },
            },
            goldReward: 200,
            karmaHit: -2,
        },
        wissen_teilen: {
            description: 'Geheimes Zeitstadt-Wissen mit einer Fraktion teilen',
            reactions: {
                goetterfels_waechter: { fame: 0, infamy: +30 },     // VERRAT am Geheimnis!
                schatten_kult:      { fame: +25, infamy: 0 },       // Genau was wir wollen!
                haus_silberdorn:    { fame: +10, infamy: 0 },       // Wissen ist Macht!
            },
            goldReward: 0,
            karmaHit: -1, // Wissen gehört allen... oder?
        },
    };

    function executeMoralDilemma(dilemmaId) {
        const dilemma = MORAL_DILEMMAS[dilemmaId];
        if (!dilemma) return null;

        const results = [];

        // Reputation-Änderungen bei allen betroffenen Fraktionen
        if (dilemma.reactions) {
            Object.entries(dilemma.reactions).forEach(([fid, changes]) => {
                if (changes.fame > 0) changeFame(fid, changes.fame);
                if (changes.infamy > 0) changeInfamy(fid, changes.infamy);
                results.push({
                    faction: FACTIONS[fid]?.name || fid,
                    icon: FACTIONS[fid]?.icon || '?',
                    fame: changes.fame,
                    infamy: changes.infamy,
                });
            });
        }

        factionState.factionEvents.push({
            type: 'moral_dilemma',
            dilemma: dilemmaId,
            description: dilemma.description,
            day: getWorldDay(),
        });

        saveFactionState();

        return {
            dilemma: dilemma.description,
            results,
            goldReward: dilemma.goldReward,
            karmaHit: dilemma.karmaHit,
        };
    }

    // ==========================================
    // PREISMODIFIKATION DURCH REPUTATION
    // ==========================================

    function getPriceModifier(factionId) {
        const rep = factionState.playerReputation[factionId];
        if (!rep) return 1.0;

        const fameLevel = getRepLevel(rep.fame, REP_LEVELS);
        const infamyLevel = getRepLevel(rep.infamy, INFAMY_LEVELS);

        let modifier = 1.0;

        // Fame gibt Rabatt
        if (rep.fame >= 75)      modifier -= 0.30;
        else if (rep.fame >= 50) modifier -= 0.20;
        else if (rep.fame >= 25) modifier -= 0.10;

        // Infamy erhöht Preise (oder verweigert Handel)
        if (rep.infamy >= 50)     return Infinity; // KEIN HANDEL!
        else if (rep.infamy >= 25) modifier += 0.20;
        else if (rep.infamy >= 10) modifier += 0.10;

        return Math.max(0.5, modifier);
    }

    // ==========================================
    // NPC REAKTION BASIEREND AUF FRAKTION
    // ==========================================

    function getNPCReaction(npcFaction) {
        const rep = factionState.playerReputation[npcFaction];
        if (!rep) return { attitude: 'neutral', dialogue: 'Hmm...' };

        const fame = rep.fame;
        const infamy = rep.infamy;

        if (infamy >= 50) {
            return {
                attitude: 'hostile',
                dialogue: 'Du wagst es dich hier blicken zu lassen?! WACHEN!',
                willAttack: true,
            };
        }
        if (infamy >= 25) {
            return {
                attitude: 'suspicious',
                dialogue: 'Ich behalte dich im Auge, Fremder...',
                priceModifier: 1.2,
            };
        }
        if (fame >= 75) {
            return {
                attitude: 'adoring',
                dialogue: 'Es ist eine Ehre! Was kann ich für euch tun?',
                priceModifier: 0.7,
                offersExclusiveQuest: true,
            };
        }
        if (fame >= 50) {
            return {
                attitude: 'friendly',
                dialogue: 'Ah, ein Freund! Willkommen!',
                priceModifier: 0.8,
            };
        }
        if (fame >= 25) {
            return {
                attitude: 'welcoming',
                dialogue: 'Guten Tag! Du hast einen guten Ruf.',
                priceModifier: 0.9,
            };
        }

        return { attitude: 'neutral', dialogue: 'Kann ich dir helfen?' };
    }

    // ==========================================
    // HELPER
    // ==========================================

    function getWorldDay() {
        if (window.WorldEventGenerator) {
            return WorldEventGenerator.getWorldState().day || 1;
        }
        return 1;
    }

    function getPlayerReputation(factionId) {
        return factionState.playerReputation[factionId] || { fame: 0, infamy: 0 };
    }

    function getAllReputations() {
        const result = {};
        Object.keys(FACTIONS).forEach(fid => {
            const rep = factionState.playerReputation[fid] || { fame: 0, infamy: 0 };
            result[fid] = {
                ...rep,
                fameLevel: getRepLevel(rep.fame, REP_LEVELS),
                infamyLevel: getRepLevel(rep.infamy, INFAMY_LEVELS),
                faction: FACTIONS[fid],
            };
        });
        return result;
    }

    function getActiveWars() {
        return factionState.factionWars.filter(w => !w.winner);
    }

    // ==========================================
    // TAGES-UPDATE (von WorldEventGenerator aufgerufen)
    // ==========================================

    function dailyUpdate() {
        checkFactionConflicts();
        advanceFactionWars();

        // Infamy verfällt langsam (0.5 pro Tag)
        Object.keys(factionState.playerReputation).forEach(fid => {
            const rep = factionState.playerReputation[fid];
            if (rep.infamy > 0) {
                rep.infamy = Math.max(0, rep.infamy - 0.5);
            }
        });

        saveFactionState();
    }

    // ==========================================
    // EXPORT
    // ==========================================

    window.FactionSystem = {
        // Daten
        FACTIONS,
        MORAL_DILEMMAS,
        REP_LEVELS,
        INFAMY_LEVELS,

        // Reputation
        changeFame,
        changeInfamy,
        performAction,
        getPlayerReputation,
        getAllReputations,
        getPriceModifier,

        // NPC Reaktion
        getNPCReaction,

        // Moralische Entscheidungen
        executeMoralDilemma,

        // Kriege
        getActiveWars,
        startFactionWar,

        // Tages-Update
        dailyUpdate,

        // State
        getState: () => ({ ...factionState }),
        saveFactionState,
    };

    const factionCount = Object.keys(FACTIONS).length;
    const warCount = factionState.factionWars.filter(w => !w.winner).length;
    console.log(`🏛️ Fraktionssystem geladen! ${factionCount} Fraktionen | ${warCount} aktive Kriege`);
    console.log(`🎭 ${Object.keys(MORAL_DILEMMAS).length} moralische Dilemmata verfügbar`);

})();
