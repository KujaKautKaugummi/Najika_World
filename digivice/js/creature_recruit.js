/**
 * NAJIKA WORLD - CREATURE RECRUIT & CLAN SYSTEM
 * ===============================================
 * NUR für Kategorie 1 "Lebende" (Anime-NPCs mit Verstand)
 *
 * Lebende Kreaturen = wie NPCs, nur nicht in Menschenform
 * Selbe Interaktionsmöglichkeiten wie mit Menschen:
 *   - ANWERBEN (Gold, Ruf, Schutz) → arbeitet für dich
 *   - VERSKLAVEN (Gewalt, Kette) → schuftet, hasst dich, kann fliehen
 *   - TÖTEN → Seltene Drops, aber Clan-Konsequenzen!
 *   - HANDELN → Manche Clans haben Händler
 *   - IGNORIEREN → Friedliche Koexistenz
 *
 * CLAN-REPUTATION SYSTEM:
 *   Jede Kat.1 Spezies = ein Clan (Mini-Fraktion)
 *   Töte Goblins → Goblin-Clan hasst dich
 *   Gerüchte breiten sich zwischen Clans aus
 *   Überjagung → weniger Spawns → Ökosystem-Kettenreaktion
 *
 * MORALISCHES DILEMMA:
 *   Der süße sprechende Hase hat einen seltenen Edelstein...
 *   Töte ich ihn oder farme ich 2 Stunden länger?
 *   Deine Wahl. Keine automatische Schuld. Nur die WELT reagiert.
 */

(function() {
    'use strict';

    // ==========================================
    // CLAN REPUTATION CONFIG
    // ==========================================

    const CLAN_CONFIG = {
        // Reputation-Bereich
        minRep: -1000,
        maxRep: 1000,
        defaultRep: 0,

        // Reputation-Schwellen
        thresholds: {
            hated:    -500,   // Clan greift bei Sichtkontakt an
            hostile:  -200,   // Clan ist feindlich, warnt erst
            disliked: -50,    // Clan misstraut dir
            neutral:  0,      // Standard
            liked:    100,    // Clan ist freundlich
            friendly: 300,    // Clan bietet Quests/Handel
            allied:   600,    // Clan kämpft für dich
            revered:  900,    // Clan verehrt dich
        },

        // Reputation-Änderungen
        repChanges: {
            kill:        -80,    // Clanmitglied getötet
            enslave:     -120,   // Versklavt (schlimmer als töten!)
            recruit:     +20,    // Angeworben (freiwillig)
            trade:       +5,     // Gehandelt
            gift:        +15,    // Geschenk gegeben
            helpInCombat:+30,    // Im Kampf geholfen
            quest:       +50,    // Quest für Clan erledigt
            freeSlaves:  +40,    // Versklavte Clanmitglieder befreit
            betrayal:    -150,   // Verrat (angeworben dann getötet)
        },

        // Gerüchte-System
        rumorSpreadRate: 0.3,     // 30% der Rep-Änderung breitet sich aus
        rumorMaxDistance: 2,      // Wie viele Clans-Sprünge Gerüchte reisen
        rumorDecayPerHop: 0.5,    // Halbe Stärke pro Sprung

        // Ökologisches Gleichgewicht
        overhuntThreshold: 10,    // Kills bevor Überjagung einsetzt
        respawnPenalty: 0.2,      // 20% weniger Spawns pro Überjagung-Stufe
        ecosystemRecoveryDays: 7, // Tage bis Ökosystem sich erholt
    };

    // Clan-Verbindungen (welche Clans kommunizieren)
    // Gerüchte breiten sich über diese Verbindungen aus
    const CLAN_CONNECTIONS = {
        // Samtmoos
        pilz_volk:      ['baumgeister', 'wuermervolk', 'nachtjaeger'],
        waldrudel:      ['baumgeister', 'nachtjaeger'],
        baumgeister:    ['pilz_volk', 'waldrudel', 'gruen_druiden'],
        nachtjaeger:    ['waldrudel', 'pilz_volk', 'schattenwesen'],
        wuermervolk:    ['pilz_volk', 'kristall_volk', 'erdgeister'],

        // Heisse Dünen
        sandgeister:    ['duenen_nomaden', 'wuesten_bestien'],
        duenen_nomaden: ['sandgeister', 'karawanen_volk'],
        wuesten_bestien:['sandgeister', 'feuer_elementare'],
        karawanen_volk: ['duenen_nomaden', 'haendler_gilde'],

        // Salzwind
        meereswesen:    ['kuesten_geister', 'tiefsee_clan'],
        kuesten_geister:['meereswesen', 'fischer_volk'],
        tiefsee_clan:   ['meereswesen', 'kristall_volk'],
        fischer_volk:   ['kuesten_geister', 'haendler_gilde'],

        // Magmaströme
        feuer_elementare:['magma_schmiede', 'wuesten_bestien', 'vulkan_wesen'],
        magma_schmiede:  ['feuer_elementare', 'vulkan_wesen', 'kristall_volk'],
        vulkan_wesen:    ['feuer_elementare', 'magma_schmiede'],

        // Grünschlamm
        sumpf_wesen:    ['gift_brut', 'gruen_druiden'],
        gift_brut:      ['sumpf_wesen', 'pilz_volk'],
        gruen_druiden:  ['sumpf_wesen', 'baumgeister'],

        // Blitzebene
        donner_clan:    ['sturm_nomaden', 'blitz_geister'],
        sturm_nomaden:  ['donner_clan', 'duenen_nomaden'],
        blitz_geister:  ['donner_clan', 'erdgeister'],

        // Tiefenhöhlen
        kristall_volk:  ['erdgeister', 'tiefsee_clan', 'magma_schmiede', 'wuermervolk'],
        erdgeister:     ['kristall_volk', 'wuermervolk', 'blitz_geister'],
        schattenwesen:  ['kristall_volk', 'nachtjaeger'],

        // Reich der Drei
        frost_clan:     ['wolf_rudel', 'berg_riesen'],
        wolf_rudel:     ['frost_clan', 'waldrudel'],
        berg_riesen:    ['frost_clan', 'erdgeister'],

        // Götterfels
        goetter_diener: ['tempel_waechter'],
        tempel_waechter:['goetter_diener', 'haendler_gilde'],
        haendler_gilde: ['tempel_waechter', 'karawanen_volk', 'fischer_volk'],
    };

    // ==========================================
    // STATE
    // ==========================================

    // Clan-Reputation: { clanName: number }
    let clanReputation = {};

    // Kill-Counter für Ökosystem: { clanName: { kills: number, lastKillDay: number } }
    let killTracking = {};

    // Angeworbene Kreaturen: [ RecruitedCreature ]
    let recruitedCreatures = [];

    // Versklavte Kreaturen: [ EnslavedCreature ]
    let enslavedCreatures = [];

    // Gerüchte-Queue: [ { from, to, amount, day } ]
    let rumorQueue = [];

    // Combat-Help-Log: { clanName: timestamp } - wann zuletzt im Kampf geholfen
    let combatHelpLog = {};

    // Spieltag (wird extern gesetzt)
    let currentDay = 1;

    // ==========================================
    // RECRUITED CREATURE CLASS
    // ==========================================

    class RecruitedCreature {
        constructor(monsterId, monsterData, method) {
            this.id = `recruit_${Date.now()}_${Math.random().toString(36).substr(2, 6)}`;
            this.monsterId = monsterId;
            this.monsterData = monsterData;
            this.name = monsterData.name;
            this.method = method;         // 'gold', 'reputation', 'protection', 'quest'
            this.recruitedAt = Date.now();
            this.loyalty = 60;            // 0-100
            this.job = null;              // 'guard', 'worker', 'scout', 'merchant'
            this.mood = 70;               // 0-100
        }
    }

    class EnslavedCreature {
        constructor(monsterId, monsterData) {
            this.id = `slave_${Date.now()}_${Math.random().toString(36).substr(2, 6)}`;
            this.monsterId = monsterId;
            this.monsterData = monsterData;
            this.name = monsterData.name;
            this.enslavedAt = Date.now();
            this.obedience = 30;          // 0-100 (starts low)
            this.hatred = 80;             // 0-100 (starts high)
            this.escapeAttempts = 0;
            this.job = 'labor';
        }
    }

    // ==========================================
    // CLAN REPUTATION CORE
    // ==========================================

    function getReputation(clanName) {
        if (clanReputation[clanName] === undefined) {
            clanReputation[clanName] = CLAN_CONFIG.defaultRep;
        }
        return clanReputation[clanName];
    }

    function getReputationLevel(clanName) {
        const rep = getReputation(clanName);
        const t = CLAN_CONFIG.thresholds;
        if (rep >= t.revered)  return { level: 'revered',  label: 'Verehrt',     color: '#FFD700' };
        if (rep >= t.allied)   return { level: 'allied',   label: 'Verbündet',   color: '#00FF00' };
        if (rep >= t.friendly) return { level: 'friendly', label: 'Freundlich',  color: '#88FF88' };
        if (rep >= t.liked)    return { level: 'liked',    label: 'Wohlgesinnt', color: '#AAFFAA' };
        if (rep >= t.neutral)  return { level: 'neutral',  label: 'Neutral',     color: '#CCCCCC' };
        if (rep >= t.disliked) return { level: 'disliked', label: 'Misstrauisch',color: '#FFAA88' };
        if (rep >= t.hostile)  return { level: 'hostile',  label: 'Feindlich',   color: '#FF6644' };
        return                          { level: 'hated',    label: 'Verhasst',    color: '#FF0000' };
    }

    /**
     * Reputation ändern + Gerüchte verbreiten
     */
    function changeReputation(clanName, amount, reason) {
        const oldRep = getReputation(clanName);
        clanReputation[clanName] = Math.max(CLAN_CONFIG.minRep,
            Math.min(CLAN_CONFIG.maxRep, oldRep + amount));

        const newLevel = getReputationLevel(clanName);
        const oldLevel = _levelForRep(oldRep);

        console.log(`🏰 Clan ${clanName}: ${oldRep} → ${clanReputation[clanName]} (${reason})`);

        // Level-Wechsel melden
        if (newLevel.level !== oldLevel) {
            if (typeof notify === 'function') {
                const dir = amount > 0 ? '📈' : '📉';
                notify(`${dir} ${clanName}: ${newLevel.label}`, amount > 0 ? 'success' : 'warning');
            }
        }

        // Gerüchte verbreiten
        _spreadRumor(clanName, amount);

        _save();
        return { clan: clanName, rep: clanReputation[clanName], level: newLevel };
    }

    function _levelForRep(rep) {
        const t = CLAN_CONFIG.thresholds;
        if (rep >= t.revered)  return 'revered';
        if (rep >= t.allied)   return 'allied';
        if (rep >= t.friendly) return 'friendly';
        if (rep >= t.liked)    return 'liked';
        if (rep >= t.neutral)  return 'neutral';
        if (rep >= t.disliked) return 'disliked';
        if (rep >= t.hostile)  return 'hostile';
        return 'hated';
    }

    // ==========================================
    // GERÜCHTE-SYSTEM (RUMORS)
    // ==========================================

    /**
     * Gerüchte über Verbindungen verbreiten
     */
    function _spreadRumor(originClan, amount) {
        const connections = CLAN_CONNECTIONS[originClan] || [];
        const rumorAmount = Math.floor(amount * CLAN_CONFIG.rumorSpreadRate);

        if (Math.abs(rumorAmount) < 3) return; // Zu klein für Gerüchte

        connections.forEach(targetClan => {
            rumorQueue.push({
                from: originClan,
                to: targetClan,
                amount: rumorAmount,
                day: currentDay,
                hop: 1
            });
        });
    }

    /**
     * Gerüchte-Queue verarbeiten (wird täglich aufgerufen)
     */
    function processRumors() {
        const toProcess = [...rumorQueue];
        rumorQueue = [];

        toProcess.forEach(rumor => {
            // Nur Gerüchte vom Vortag oder älter verarbeiten
            if (rumor.day >= currentDay) {
                rumorQueue.push(rumor); // Zurücklegen
                return;
            }

            const decayedAmount = Math.floor(rumor.amount * (1 - (rumor.hop - 1) * CLAN_CONFIG.rumorDecayPerHop));
            if (Math.abs(decayedAmount) < 2) return; // Gerücht zu schwach

            const oldRep = getReputation(rumor.to);
            clanReputation[rumor.to] = Math.max(CLAN_CONFIG.minRep,
                Math.min(CLAN_CONFIG.maxRep, oldRep + decayedAmount));

            console.log(`👂 Gerücht: ${rumor.from} → ${rumor.to}: ${decayedAmount > 0 ? '+' : ''}${decayedAmount}`);

            // Weiterverbreiten?
            if (rumor.hop < CLAN_CONFIG.rumorMaxDistance) {
                const nextConnections = CLAN_CONNECTIONS[rumor.to] || [];
                nextConnections.forEach(nextClan => {
                    if (nextClan !== rumor.from) { // Nicht zurück zum Ursprung
                        rumorQueue.push({
                            from: rumor.to,
                            to: nextClan,
                            amount: decayedAmount,
                            day: currentDay,
                            hop: rumor.hop + 1
                        });
                    }
                });
            }
        });

        _save();
    }

    // ==========================================
    // ÖKOLOGISCHES GLEICHGEWICHT
    // ==========================================

    /**
     * Kill registrieren → Clan-Rep + Ökosystem
     */
    function registerKill(monsterId) {
        const registry = window.MonsterRegistry;
        if (!registry) return null;

        const monster = registry.getMonster(monsterId);
        if (!monster || monster.category !== 'lebend') return null;

        const clan = monster.clan;
        if (!clan) return null;

        // Kill-Tracking
        if (!killTracking[clan]) {
            killTracking[clan] = { kills: 0, lastKillDay: currentDay, totalKills: 0 };
        }
        killTracking[clan].kills++;
        killTracking[clan].totalKills++;
        killTracking[clan].lastKillDay = currentDay;

        // Reputation-Verlust
        const repChange = CLAN_CONFIG.repChanges.kill;
        const result = changeReputation(clan, repChange, `${monster.name} getötet`);

        // Überjagung prüfen
        const overhunt = _checkOverhunt(clan);

        // Rare Drop?
        let rareDrop = null;
        if (monster.rareDrop && Math.random() < 0.15) { // 15% Chance
            rareDrop = monster.rareDrop;
            console.log(`💎 Seltener Drop: ${rareDrop} von ${monster.name}!`);
        }

        return {
            kill: true,
            monster: monster.name,
            clan: clan,
            reputation: result,
            overhunt: overhunt,
            rareDrop: rareDrop,
            normalLoot: monster.lootTable
        };
    }

    function _checkOverhunt(clan) {
        const tracking = killTracking[clan];
        if (!tracking) return null;

        if (tracking.kills >= CLAN_CONFIG.overhuntThreshold) {
            const overhuntLevel = Math.floor(tracking.kills / CLAN_CONFIG.overhuntThreshold);
            const spawnReduction = Math.min(0.8, overhuntLevel * CLAN_CONFIG.respawnPenalty);

            console.log(`⚠️ Überjagung: ${clan} (Stufe ${overhuntLevel}, -${Math.floor(spawnReduction * 100)}% Spawns)`);

            if (typeof notify === 'function' && overhuntLevel === 1) {
                notify(`⚠️ Die ${clan} werden seltener gesichtet...`, 'warning');
            }

            return {
                active: true,
                level: overhuntLevel,
                spawnReduction: spawnReduction,
                message: `${clan} Population sinkt! -${Math.floor(spawnReduction * 100)}% Spawns`
            };
        }

        return { active: false };
    }

    /**
     * Spawn-Multiplikator für ein Monster (Ökosystem-basiert)
     */
    function getSpawnMultiplier(monsterId) {
        const registry = window.MonsterRegistry;
        if (!registry) return 1.0;

        const monster = registry.getMonster(monsterId);
        if (!monster || !monster.clan) return 1.0;

        const tracking = killTracking[monster.clan];
        if (!tracking) return 1.0;

        if (tracking.kills >= CLAN_CONFIG.overhuntThreshold) {
            const overhuntLevel = Math.floor(tracking.kills / CLAN_CONFIG.overhuntThreshold);
            return Math.max(0.2, 1.0 - overhuntLevel * CLAN_CONFIG.respawnPenalty);
        }

        return 1.0;
    }

    /**
     * Tägliche Ökosystem-Erholung
     */
    function dailyEcosystemRecovery() {
        Object.keys(killTracking).forEach(clan => {
            const tracking = killTracking[clan];
            const daysSinceKill = currentDay - tracking.lastKillDay;

            if (daysSinceKill >= CLAN_CONFIG.ecosystemRecoveryDays && tracking.kills > 0) {
                const recovery = Math.ceil(tracking.kills * 0.3);
                tracking.kills = Math.max(0, tracking.kills - recovery);
                console.log(`🌱 Ökosystem-Erholung: ${clan} -${recovery} Kills (noch ${tracking.kills})`);
            }
        });
        _save();
    }

    // ==========================================
    // ANWERBEN (RECRUIT)
    // ==========================================

    /**
     * Kreatur anwerben (freiwillig, mit Bedingungen)
     * @param {string} monsterId
     * @param {string} method - 'gold', 'reputation', 'protection', 'quest'
     * @param {object} offer - { gold: 100 } oder { questId: 'xyz' }
     */
    function recruitCreature(monsterId, method, offer) {
        const registry = window.MonsterRegistry;
        if (!registry) return { success: false, error: 'MonsterRegistry nicht geladen' };

        const monster = registry.getMonster(monsterId);
        if (!monster) return { success: false, error: `Unbekanntes Monster: ${monsterId}` };

        if (monster.category !== 'lebend') {
            return {
                success: false,
                error: `${monster.name} ist Vieh! Vieh wird GEZÄHMT, nicht angeworben.`,
                hint: 'Nutze creature_taming.js für Vieh'
            };
        }

        // Clan-Reputation prüfen
        const clanRep = getReputationLevel(monster.clan);
        const minRecruitRep = CLAN_CONFIG.thresholds.neutral; // Mindestens neutral

        if (getReputation(monster.clan) < minRecruitRep) {
            return {
                success: false,
                error: `Der ${monster.clan} vertraut dir nicht genug.`,
                currentRep: clanRep,
                needed: 'neutral',
                hint: `Verbessere deinen Ruf beim ${monster.clan} durch Geschenke oder Quests.`
            };
        }

        // Kosten je nach Methode
        let cost = {};
        let successChance = 0.5;

        switch (method) {
            case 'gold':
                cost = { gold: 50 + monster.tier * 30 };
                successChance = 0.7;
                break;
            case 'reputation':
                if (getReputation(monster.clan) < CLAN_CONFIG.thresholds.friendly) {
                    return { success: false, error: `Brauche mindestens "Freundlich" beim ${monster.clan}` };
                }
                cost = {};
                successChance = 0.6;
                break;
            case 'protection': {
                // Erfordert: Clan kürzlich im Kampf geholfen (letzte 30 Minuten Echtzeit)
                const lastHelp = combatHelpLog[monster.clan] || 0;
                const helpAge = Date.now() - lastHelp;
                const HELP_WINDOW = 30 * 60 * 1000; // 30 Minuten
                if (lastHelp === 0 || helpAge > HELP_WINDOW) {
                    return {
                        success: false,
                        error: `Du musst dem ${monster.clan} zuerst im Kampf helfen! Verteidige ihre Mitglieder gegen Angreifer.`
                    };
                }
                cost = {};
                successChance = 0.4 + Math.min(0.3, getReputation(monster.clan) / 1000);
                break;
            }
            case 'quest': {
                // Erfordert: Quest für diesen Clan abgeschlossen
                const questId = offer?.questId;
                const guildState = window.GildenhausUI?.getState?.();
                const completedIds = guildState?.completedQuestIds || [];
                if (questId && !completedIds.includes(questId)) {
                    return {
                        success: false,
                        error: `Schließe zuerst die Quest ab, bevor du ${monster.name} anwerben kannst.`
                    };
                }
                // Auch ohne spezifische Quest-ID: Rep-Check als Fallback
                if (!questId && getReputation(monster.clan) < CLAN_CONFIG.thresholds.liked) {
                    return {
                        success: false,
                        error: `Erledige Quests für den ${monster.clan} um genug Vertrauen aufzubauen.`
                    };
                }
                cost = {};
                successChance = 0.9;
                break;
            }
            default:
                return { success: false, error: `Unbekannte Methode: ${method}` };
        }

        // Würfeln
        if (Math.random() > successChance) {
            return {
                success: false,
                rejected: true,
                message: `${monster.name} lehnt dein Angebot ab. Vielleicht nächstes Mal.`,
                cost: cost // Gold wird trotzdem verbraucht (Verhandlung)
            };
        }

        // Angeworben!
        const recruit = new RecruitedCreature(monsterId, monster, method);
        recruitedCreatures.push(recruit);

        // Reputation-Bonus
        changeReputation(monster.clan, CLAN_CONFIG.repChanges.recruit, `${monster.name} angeworben`);

        _save();

        return {
            success: true,
            recruit: recruit,
            cost: cost,
            message: `${monster.name} schließt sich dir an!`,
            availableJobs: ['guard', 'worker', 'scout', 'merchant']
        };
    }

    // ==========================================
    // VERSKLAVEN (ENSLAVE)
    // ==========================================

    /**
     * Kreatur versklaven (Gewalt, schwere Konsequenzen)
     */
    function enslaveCreature(monsterId) {
        const registry = window.MonsterRegistry;
        if (!registry) return { success: false, error: 'MonsterRegistry nicht geladen' };

        const monster = registry.getMonster(monsterId);
        if (!monster) return { success: false, error: `Unbekanntes Monster: ${monsterId}` };

        if (monster.category !== 'lebend') {
            return { success: false, error: `${monster.name} ist Vieh. Vieh wird gezähmt, nicht versklavt.` };
        }

        const slave = new EnslavedCreature(monsterId, monster);
        enslavedCreatures.push(slave);

        // SCHWERER Reputation-Verlust
        changeReputation(monster.clan, CLAN_CONFIG.repChanges.enslave, `${monster.name} versklavt!`);

        _save();

        console.log(`⛓️ ${monster.name} versklavt! ${monster.clan} ist wütend.`);

        return {
            success: true,
            slave: slave,
            warning: `Der ${monster.clan} wird das nicht vergessen!`,
            message: `${monster.name} ist nun dein Sklave. Es hasst dich.`
        };
    }

    /**
     * Sklaven-Update (täglich) - Fluchtversuche, Gehorsam
     */
    function dailySlaveUpdate() {
        const escaped = [];
        const events = [];

        enslavedCreatures.forEach(slave => {
            // Gehorsam sinkt wenn Hass hoch
            if (slave.hatred > 50) {
                slave.obedience = Math.max(0, slave.obedience - 2);
            }

            // Fluchtversuch?
            const escapeChance = (100 - slave.obedience) / 200; // Max 50%
            if (Math.random() < escapeChance) {
                slave.escapeAttempts++;

                if (slave.escapeAttempts >= 3 || Math.random() < 0.3) {
                    // Flucht erfolgreich!
                    escaped.push(slave);
                    events.push({
                        type: 'escape',
                        message: `⛓️💨 ${slave.name} ist geflohen!`,
                        slave: slave
                    });
                } else {
                    events.push({
                        type: 'escape_failed',
                        message: `⛓️ ${slave.name} versuchte zu fliehen, wurde aber gefasst.`,
                        slave: slave
                    });
                    slave.hatred = Math.min(100, slave.hatred + 10);
                }
            }

            // Sabotage bei sehr niedrigem Gehorsam
            if (slave.obedience < 10 && Math.random() < 0.2) {
                events.push({
                    type: 'sabotage',
                    message: `⚠️ ${slave.name} hat Arbeit sabotiert!`,
                    slave: slave
                });
            }
        });

        // Geflohene entfernen
        if (escaped.length > 0) {
            const escapeIds = new Set(escaped.map(s => s.id));
            enslavedCreatures = enslavedCreatures.filter(s => !escapeIds.has(s.id));
        }

        _save();
        return { events, escaped: escaped.length };
    }

    /**
     * Sklaven befreien → Rep-Bonus bei dem Clan
     */
    function freeSlaves(slaveIds) {
        const freed = [];

        slaveIds.forEach(id => {
            const index = enslavedCreatures.findIndex(s => s.id === id);
            if (index === -1) return;

            const slave = enslavedCreatures[index];
            enslavedCreatures.splice(index, 1);
            freed.push(slave);

            // Reputation-Bonus
            changeReputation(slave.monsterData.clan, CLAN_CONFIG.repChanges.freeSlaves,
                `${slave.name} befreit`);
        });

        _save();

        return {
            success: true,
            freed: freed.length,
            message: `${freed.length} Kreatur(en) befreit. Ihre Clans werden es hören.`
        };
    }

    // ==========================================
    // RECRUITED CREATURE MANAGEMENT
    // ==========================================

    /**
     * Angeworbener Kreatur einen Job zuweisen
     */
    function assignJob(recruitId, job) {
        const recruit = recruitedCreatures.find(r => r.id === recruitId);
        if (!recruit) return { success: false, error: 'Kreatur nicht gefunden' };

        const validJobs = ['guard', 'worker', 'scout', 'merchant'];
        const workerJobs = window.WorkerSystem?.JOB_DEFINITIONS;
        if (!validJobs.includes(job) && !(workerJobs && workerJobs[job])) {
            return { success: false, error: `Ungültiger Job: ${job}` };
        }

        recruit.job = job;
        _save();

        const jobNames = {
            guard: 'Wächter', worker: 'Arbeiter',
            scout: 'Kundschafter', merchant: 'Händler'
        };

        return {
            success: true,
            message: `${recruit.name} ist jetzt ${jobNames[job]}.`,
            recruit: recruit
        };
    }

    /**
     * Angeworbene Kreatur entlassen
     */
    function dismissRecruit(recruitId) {
        const index = recruitedCreatures.findIndex(r => r.id === recruitId);
        if (index === -1) return { success: false, error: 'Kreatur nicht gefunden' };

        const recruit = recruitedCreatures[index];
        recruitedCreatures.splice(index, 1);
        _save();

        return {
            success: true,
            message: `${recruit.name} kehrt zu ${recruit.monsterData.clan} zurück.`
        };
    }

    /**
     * Tägliches Update für angeworbene Kreaturen
     */
    function dailyRecruitUpdate() {
        const events = [];

        recruitedCreatures.forEach(recruit => {
            // Loyalität basierend auf Clan-Rep
            const clanRep = getReputation(recruit.monsterData.clan);
            if (clanRep < CLAN_CONFIG.thresholds.hostile) {
                recruit.loyalty = Math.max(0, recruit.loyalty - 10);
                events.push({
                    type: 'loyalty_drop',
                    message: `${recruit.name} ist beunruhigt über deinen Ruf bei ${recruit.monsterData.clan}.`
                });
            }

            // Desertierung bei 0 Loyalität
            if (recruit.loyalty <= 0) {
                events.push({
                    type: 'desertion',
                    message: `${recruit.name} hat dich verlassen! Dein Ruf bei ${recruit.monsterData.clan} ist zu schlecht.`
                });
            }
        });

        // Deserteure entfernen
        recruitedCreatures = recruitedCreatures.filter(r => r.loyalty > 0);

        _save();
        return { events };
    }

    // ==========================================
    // INTERACTION (Geschenke, Handel)
    // ==========================================

    /**
     * Clan ein Geschenk geben
     */
    function giftToClan(clanName, item) {
        return changeReputation(clanName, CLAN_CONFIG.repChanges.gift, `Geschenk: ${item}`);
    }

    /**
     * Mit Clan handeln
     */
    function tradeWithClan(clanName) {
        return changeReputation(clanName, CLAN_CONFIG.repChanges.trade, 'Handel');
    }

    // ==========================================
    // QUERIES
    // ==========================================

    function getAllClanReputations() {
        const registry = window.MonsterRegistry;
        const clans = registry ? registry.getAllClans() : Object.keys(clanReputation);

        return clans.map(clan => ({
            clan: clan,
            reputation: getReputation(clan),
            level: getReputationLevel(clan),
            overhunt: killTracking[clan] ? _checkOverhunt(clan) : { active: false },
            connections: CLAN_CONNECTIONS[clan] || []
        }));
    }

    function getRecruitedCreatures() {
        return recruitedCreatures.map(r => ({
            id: r.id,
            monsterId: r.monsterId,
            name: r.name,
            icon: r.monsterData.icon,
            clan: r.monsterData.clan,
            loyalty: r.loyalty,
            mood: r.mood,
            job: r.job,
            method: r.method
        }));
    }

    function getEnslavedCreatures() {
        return enslavedCreatures.map(s => ({
            id: s.id,
            monsterId: s.monsterId,
            name: s.name,
            icon: s.monsterData.icon,
            clan: s.monsterData.clan,
            obedience: s.obedience,
            hatred: s.hatred,
            escapeAttempts: s.escapeAttempts,
            job: s.job
        }));
    }

    /**
     * NPC-Reaktion basierend auf Clan-Rep (für Dialog-System)
     */
    function getCreatureReaction(monsterId) {
        const registry = window.MonsterRegistry;
        if (!registry) return { reaction: 'neutral', dialog: '' };

        const monster = registry.getMonster(monsterId);
        if (!monster || !monster.clan) return { reaction: 'neutral', dialog: '' };

        const level = getReputationLevel(monster.clan);

        const dialogs = {
            hated:    [`Du wagst es hierher zu kommen?! Verschwinde!`, `Mörder! Der ${monster.clan} vergisst nicht!`],
            hostile:  [`Geh weg, Fremder. Hier bist du nicht willkommen.`, `Ich warne dich nur einmal...`],
            disliked: [`Was willst du?`, `Mach schnell...`],
            neutral:  [`Hallo, Reisender.`, `Was führt dich hierher?`],
            liked:    [`Willkommen! Kann ich dir helfen?`, `Schön dich zu sehen!`],
            friendly: [`Mein Freund! Komm, ich habe Angebote für dich.`, `Der ${monster.clan} grüßt dich!`],
            allied:   [`Verbündeter! Wir kämpfen an deiner Seite!`, `Ehre dem ${monster.clan} und dir!`],
            revered:  [`Der Große ist hier! Es ist uns eine Ehre!`, `Gebiete, und wir gehorchen!`],
        };

        const lines = dialogs[level.level] || dialogs.neutral;
        const dialog = lines[Math.floor(Math.random() * lines.length)];

        return {
            reaction: level.level,
            label: level.label,
            color: level.color,
            dialog: dialog,
            willAttack: level.level === 'hated',
            willTrade: ['friendly', 'allied', 'revered'].includes(level.level),
            willRecruit: ['liked', 'friendly', 'allied', 'revered'].includes(level.level),
        };
    }

    /**
     * Spieltag setzen (wird von game loop aufgerufen)
     */
    function setDay(day) {
        currentDay = day;
    }

    /**
     * Tägliches Komplett-Update
     */
    function dailyUpdate() {
        processRumors();
        dailyEcosystemRecovery();
        const recruitEvents = dailyRecruitUpdate();
        const slaveEvents = dailySlaveUpdate();
        return {
            rumors: 'processed',
            ecosystem: 'recovered',
            recruits: recruitEvents,
            slaves: slaveEvents
        };
    }

    // ==========================================
    // PERSISTENCE
    // ==========================================

    function _save() {
        try {
            const data = {
                clanReputation,
                killTracking,
                combatHelpLog,
                currentDay,
                recruitedCreatures: recruitedCreatures.map(r => ({
                    id: r.id, monsterId: r.monsterId, name: r.name,
                    method: r.method, recruitedAt: r.recruitedAt,
                    loyalty: r.loyalty, job: r.job, mood: r.mood,
                })),
                enslavedCreatures: enslavedCreatures.map(s => ({
                    id: s.id, monsterId: s.monsterId, name: s.name,
                    enslavedAt: s.enslavedAt, obedience: s.obedience,
                    hatred: s.hatred, escapeAttempts: s.escapeAttempts, job: s.job,
                })),
                rumorQueue,
            };
            localStorage.setItem('najika_clans', JSON.stringify(data));
        } catch (e) {
            console.error('Clan Save Error:', e);
        }
    }

    function _load() {
        try {
            const raw = localStorage.getItem('najika_clans');
            if (!raw) return;
            const data = JSON.parse(raw);
            const registry = window.MonsterRegistry;

            if (data.clanReputation) clanReputation = data.clanReputation;
            if (data.killTracking) killTracking = data.killTracking;
            if (data.combatHelpLog) combatHelpLog = data.combatHelpLog;
            if (data.currentDay) currentDay = data.currentDay;
            if (data.rumorQueue) rumorQueue = data.rumorQueue;

            // Angeworbene laden
            if (data.recruitedCreatures && registry) {
                recruitedCreatures = data.recruitedCreatures.map(saved => {
                    const monsterData = registry.getMonster(saved.monsterId);
                    if (!monsterData) return null;
                    const r = new RecruitedCreature(saved.monsterId, monsterData, saved.method);
                    r.id = saved.id; r.name = saved.name;
                    r.recruitedAt = saved.recruitedAt;
                    r.loyalty = saved.loyalty; r.job = saved.job; r.mood = saved.mood;
                    return r;
                }).filter(Boolean);
            }

            // Versklavte laden
            if (data.enslavedCreatures && registry) {
                enslavedCreatures = data.enslavedCreatures.map(saved => {
                    const monsterData = registry.getMonster(saved.monsterId);
                    if (!monsterData) return null;
                    const s = new EnslavedCreature(saved.monsterId, monsterData);
                    s.id = saved.id; s.name = saved.name;
                    s.enslavedAt = saved.enslavedAt;
                    s.obedience = saved.obedience; s.hatred = saved.hatred;
                    s.escapeAttempts = saved.escapeAttempts; s.job = saved.job;
                    return s;
                }).filter(Boolean);
            }

            console.log(`🏰 Clan-System geladen: ${Object.keys(clanReputation).length} Clans, ${recruitedCreatures.length} Angeworbene, ${enslavedCreatures.length} Sklaven`);
        } catch (e) {
            console.error('Clan Load Error:', e);
        }
    }

    // ==========================================
    // INIT
    // ==========================================

    /**
     * Kampfhilfe für Clan registrieren (für 'protection' Rekrutierungsmethode)
     */
    function logCombatHelp(clanName) {
        combatHelpLog[clanName] = Date.now();
        changeReputation(clanName, CLAN_CONFIG.repChanges.helpInCombat, `Im Kampf geholfen`);
        _save();
    }

    function init() {
        _load();

        // GameEvents: Kampf-Hilfe für Clans verknüpfen
        if (window.GameEvents) {
            window.GameEvents.on('combatEnded', (data) => {
                if ((data.won || data.result === 'victory') && data.allyClan) {
                    logCombatHelp(data.allyClan);
                }
            });
        }

        const clans = window.MonsterRegistry ? window.MonsterRegistry.getAllClans() : [];
        console.log(`🏰 Creature Recruit & Clan System bereit (${clans.length} Clans)`);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // ==========================================
    // EXPORT
    // ==========================================

    window.CreatureRecruit = {
        // Clan Reputation
        getReputation,
        getReputationLevel,
        changeReputation,
        getAllClanReputations,
        getCreatureReaction,

        // Kills & Ökosystem
        registerKill,
        getSpawnMultiplier,

        // Anwerben
        recruitCreature,
        assignJob,
        dismissRecruit,
        getRecruitedCreatures,

        // Versklaven
        enslaveCreature,
        freeSlaves,
        getEnslavedCreatures,

        // Interaktion
        giftToClan,
        tradeWithClan,
        logCombatHelp,

        // Daily Updates
        setDay,
        dailyUpdate,
        processRumors,

        // Death
        scatterOnDeath: () => {
            const stayed = [];
            const fled = [];
            recruitedCreatures.forEach(r => {
                if (r.loyalty > 70) { stayed.push(r.name); }
                else { fled.push(r.name); }
            });
            recruitedCreatures = recruitedCreatures.filter(r => r.loyalty > 70);

            const escaped = enslavedCreatures.map(s => s.name);
            enslavedCreatures = [];
            _save();
            return { stayed, fled, escaped };
        },

        // Config
        CLAN_CONFIG,
        CLAN_CONNECTIONS,
    };

})();
