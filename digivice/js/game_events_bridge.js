/**
 * NAJIKA WORLD - GAME EVENTS BRIDGE
 * ===================================
 * Verbindet ALLE Systeme über den GameEvents Bus.
 * Wird NACH allen anderen Systemen geladen.
 *
 * Reihenfolge in index.html:
 *   1. game_events.js (EventBus)
 *   2. Alle Systeme (Faction, Economy, Survival, Career, Creature, Combat, NPC)
 *   3. game_events_bridge.js (DIESES FILE - verdrahtet alles)
 */

(function() {
    'use strict';

    const GE = window.GameEvents;
    if (!GE) {
        console.error('❌ GameEvents nicht gefunden! Bridge kann nicht starten.');
        return;
    }

    // ==========================================
    // ZENTRALES PLAYER-OBJEKT
    // ==========================================
    // Erstellt window.player falls noch nicht vorhanden.
    // Alle Systeme die player.gold, player.id etc. brauchen
    // greifen hierüber zu.

    if (!window.player) {
        const savedPlayer = (() => {
            try { return JSON.parse(localStorage.getItem('najika_player') || 'null'); }
            catch { return null; }
        })();

        window.player = {
            id: savedPlayer?.id || 'kuja_' + Date.now().toString(36),
            name: savedPlayer?.name || 'Kuja',
            gold: savedPlayer?.gold ?? 500,
            level: savedPlayer?.level ?? 1,
            xp: savedPlayer?.xp ?? 0,
            mesh: null,  // Wird von 3d_scene.js gesetzt
        };

        // Auto-Save alle 30 Sekunden
        setInterval(() => {
            const { id, name, gold, level, xp } = window.player;
            localStorage.setItem('najika_player', JSON.stringify({ id, name, gold, level, xp }));
        }, 30000);

        console.log(`👤 Player initialisiert: ${window.player.name} (${window.player.gold}G, Lvl ${window.player.level})`);
    }

    // Hilfsfunktion: Player-ID für API-Aufrufe
    window.getPlayerId = () => window.player?.id || 'kuja_default';

    // ==========================================
    // XP & LEVEL-UP SYSTEM
    // ==========================================
    // XP-Kurve: Jedes Level braucht mehr XP
    // Level 2: 150, Level 5: 750, Level 10: 2500, Level 20: 8000

    function xpForLevel(level) {
        return Math.floor(level * level * 25 + level * 100);
    }

    function xpToNextLevel() {
        return xpForLevel(window.player.level + 1);
    }

    /**
     * Zentrale XP-Vergabe + automatischer Level-Up Check.
     * @param {number} amount - XP-Menge
     * @param {string} source - Quelle ('combat', 'quest', 'craft', etc.)
     */
    window.addPlayerXP = function(amount, source) {
        if (!window.player || amount <= 0) return;
        window.player.xp += amount;

        // Level-Up prüfen (kann mehrere Level auf einmal springen)
        let leveledUp = false;
        while (window.player.xp >= xpToNextLevel()) {
            window.player.xp -= xpToNextLevel();
            window.player.level++;
            leveledUp = true;
            console.log(`⬆️ LEVEL UP! Jetzt Level ${window.player.level}!`);
        }

        if (leveledUp) {
            // Notification
            if (typeof notify === 'function') {
                notify(`⬆️ LEVEL UP! Du bist jetzt Level ${window.player.level}!`, 'success');
            }

            // Event für andere Systeme
            GE.emit('playerLeveledUp', {
                level: window.player.level,
                xp: window.player.xp,
                xpNeeded: xpToNextLevel()
            });

            // Survival Mood-Buff
            if (window.SurvivalSystem) {
                SurvivalSystem.addMoodlet('leveled_up', '⬆️ Level Up!', +15, 600000);
            }
        }

        return { xp: window.player.xp, level: window.player.level, needed: xpToNextLevel(), leveledUp };
    };

    // XP-Info für UI
    window.getPlayerXPInfo = function() {
        return {
            xp: window.player?.xp || 0,
            level: window.player?.level || 1,
            needed: xpToNextLevel(),
            percent: Math.floor(((window.player?.xp || 0) / xpToNextLevel()) * 100)
        };
    };

    // ==========================================
    // COMBAT → Faction, Career, Survival, Economy
    // ==========================================

    GE.on('enemyKilled', (data) => {
        // Player XP: 5-30 XP pro Kill basierend auf Feind-Level
        const enemyLevel = data.enemyLevel || data.level || 1;
        const killXP = Math.floor(5 + enemyLevel * 2.5);
        window.addPlayerXP(killXP, 'combat');

        // Gold-Drop: Gegner lassen Gold fallen
        const goldDrop = Math.floor(3 + enemyLevel * 2 + Math.random() * enemyLevel * 3);
        if (window.player) {
            window.player.gold += goldDrop;
            if (typeof notify === 'function') notify(`+${killXP} XP, +${goldDrop}G`, 'success');
        }

        // Faction: Kampf-Aktionen ändern Ruf
        if (window.FactionSystem) {
            FactionSystem.performAction('kampf', { intensity: 2 });
            // Banditen töten = gut bei Ordnungsfraktionen
            if (data.enemyType === 'bandit' || data.enemyType === 'desperado') {
                FactionSystem.performAction('banditen_jagen', { intensity: 3 });
            }
        }

        // Career: Kampf-Berufe bekommen XP
        if (window.CareerSystem) {
            const cd = CareerSystem.getState();
            if (cd.activeCareers.includes('soeldner')) CareerSystem.addCareerXP('soeldner', 8);
            if (cd.activeCareers.includes('jaeger'))   CareerSystem.addCareerXP('jaeger', 5);
            if (cd.activeCareers.includes('henker'))    CareerSystem.addCareerXP('henker', 3);
        }

        // Creature: Clan-Reputation bei Kreaturen
        if (window.CreatureRecruit && data.creatureClan) {
            CreatureRecruit.changeReputation(data.creatureClan, -15);
        }
    });

    GE.on('combatStarted', (data) => {
        // Survival: Kampf in Safe-Zone = Verbrechen!
        if (window.SurvivalSystem && data.region === 'goetterfels') {
            SurvivalSystem.commitCrime('kampf', 'goetterfels');
        }
    });

    GE.on('combatEnded', (data) => {
        const won = data.won || data.result === 'victory';

        if (won) {
            // Career: Kampf-XP
            if (window.CareerSystem) {
                const cd = CareerSystem.getState();
                if (cd.activeCareers.includes('soeldner')) CareerSystem.addCareerXP('soeldner', 12);
                if (cd.activeCareers.includes('eskorte'))  CareerSystem.addCareerXP('eskorte', 5);
            }
            // Mood: Sieg-Buff
            if (window.SurvivalSystem) {
                SurvivalSystem.addMoodlet('victory', '⚔️ Kampf gewonnen!', +5, 300000);
            }

            // Creature Capture: Wenn Feind tambar/rekrutierbar → Dialog zeigen
            const enemyData = data.enemyData || (data.enemies && data.enemies[0]);
            if (enemyData) {
                const enemy = enemyData;
                const isTamable = enemy.tamable || enemy.category === 'vieh' || enemy.category === 'tier';
                const isRecruitable = enemy.recruitable || enemy.category === 'lebende' || enemy.clan;
                if (isTamable || isRecruitable) {
                    setTimeout(() => showCreatureCaptureUI(enemy, isTamable, isRecruitable), 1500);
                }
            }
        } else {
            // Mood: Niederlage
            if (window.SurvivalSystem) {
                SurvivalSystem.addMoodlet('defeat', '😤 Kampf verloren', -5, 300000);
            }
        }
    });

    GE.on('xpGained', (data) => {
        // Zentrale XP-Vergabe an Player-Objekt
        if (data.amount > 0) {
            window.addPlayerXP(data.amount, data.source || 'unknown');
        }

        // Career: Kampf-Berufe profitieren von allgemeinem XP
        if (window.CareerSystem && data.source === 'combat') {
            const cd = CareerSystem.getState();
            if (cd.activeCareers.includes('soeldner')) CareerSystem.addCareerXP('soeldner', Math.floor(data.amount * 0.3));
        }
    });

    // ==========================================
    // NPC INTERACTION → Faction, Career, Economy
    // ==========================================

    GE.on('npcTalked', (data) => {
        // Career: Soziale Berufe
        if (window.CareerSystem) {
            const cd = CareerSystem.getState();
            if (cd.activeCareers.includes('diplomat')) CareerSystem.addCareerXP('diplomat', 3);
            if (cd.activeCareers.includes('barde'))    CareerSystem.addCareerXP('barde', 2);
            if (cd.activeCareers.includes('spion'))     CareerSystem.addCareerXP('spion', 2);
            if (cd.activeCareers.includes('haendler'))  CareerSystem.addCareerXP('haendler', 1);
            if (cd.activeCareers.includes('gastwirt'))   CareerSystem.addCareerXP('gastwirt', 1);
        }

        // Faction: NPC-Fraktion Ruf steigt leicht
        if (window.FactionSystem && data.npcFaction) {
            FactionSystem.changeFame(data.npcFaction, 1);
        }

        // Survival: Soziale Interaktion = Mood-Buff
        if (window.SurvivalSystem) {
            SurvivalSystem.moralAction('freund_getroffen');
        }
    });

    // ==========================================
    // TRADE → Economy, Faction, Career
    // ==========================================

    GE.on('itemPurchased', (data) => {
        if (window.CareerSystem) {
            const cd = CareerSystem.getState();
            if (cd.activeCareers.includes('haendler')) CareerSystem.addCareerXP('haendler', 5);
        }
    });

    GE.on('itemCrafted', (data) => {
        // Career: Handwerks-Berufe
        if (window.CareerSystem) {
            const cd = CareerSystem.getState();
            const craftType = data.craftType || '';
            if (craftType === 'weapon' || craftType === 'armor') {
                if (cd.activeCareers.includes('schmied')) CareerSystem.addCareerXP('schmied', 10);
            }
            if (craftType === 'potion' || craftType === 'elixir') {
                if (cd.activeCareers.includes('alchemist')) CareerSystem.addCareerXP('alchemist', 10);
                if (cd.activeCareers.includes('heiler'))    CareerSystem.addCareerXP('heiler', 5);
            }
            if (craftType === 'food' || craftType === 'meal') {
                if (cd.activeCareers.includes('koch')) CareerSystem.addCareerXP('koch', 10);
            }
            if (craftType === 'cloth' || craftType === 'armor_padding') {
                if (cd.activeCareers.includes('schneider')) CareerSystem.addCareerXP('schneider', 10);
            }
            if (craftType === 'leather') {
                if (cd.activeCareers.includes('lederer')) CareerSystem.addCareerXP('lederer', 10);
            }
            if (craftType === 'beer' || craftType === 'wine') {
                if (cd.activeCareers.includes('brauer')) CareerSystem.addCareerXP('brauer', 10);
            }
            if (craftType === 'wood' || craftType === 'furniture') {
                if (cd.activeCareers.includes('zimmermann')) CareerSystem.addCareerXP('zimmermann', 10);
            }
        }
    });

    // ==========================================
    // REGION & EXPLORATION → Survival, Career, Economy
    // ==========================================

    GE.on('regionEntered', (data) => {
        // Survival: Biom-basierte Hazards starten
        if (window.SurvivalSystem) {
            const biome = data.biome || data.regionId;
            const env = SurvivalSystem.BIOME_ENVIRONMENT[biome];
            if (env) {
                console.log(`🌍 Biom betreten: ${env.description}`);
            }
        }

        // Career: Kartograph-XP
        if (window.CareerSystem) {
            const cd = CareerSystem.getState();
            if (cd.activeCareers.includes('kartograph')) CareerSystem.addCareerXP('kartograph', 5);
            if (cd.activeCareers.includes('navigator'))  CareerSystem.addCareerXP('navigator', 3);
        }

        // Mood: Schöne Gegenden
        if (window.SurvivalSystem) {
            const prettyBiomes = ['goetterfels', 'samtmoos', 'salzwind'];
            if (prettyBiomes.includes(data.regionId)) {
                SurvivalSystem.moralAction('schoene_aussicht');
            }
        }
    });

    // ==========================================
    // QUEST → Faction, Career, Economy
    // ==========================================

    GE.on('questCompleted', (data) => {
        if (window.FactionSystem && data.factionId) {
            FactionSystem.changeFame(data.factionId, 10);
        }

        // Player XP: Quests geben 25-100 XP je nach Schwierigkeit
        const questXP = data.xpReward || (25 + (data.difficulty || 1) * 15);
        window.addPlayerXP(questXP, 'quest');

        // Career: Quest-Completion gibt breit XP
        if (window.CareerSystem) {
            const cd = CareerSystem.getState();
            cd.activeCareers.forEach(careerId => {
                CareerSystem.addCareerXP(careerId, 5);
            });
        }

        // Mood: Quest geschafft
        if (window.SurvivalSystem) {
            SurvivalSystem.addMoodlet('quest_done', '📜 Quest abgeschlossen!', +8, 600000);
        }
    });

    GE.on('questAccepted', (data) => {
        if (window.FactionSystem && data.factionId) {
            FactionSystem.changeFame(data.factionId, 2);
        }
    });

    // ==========================================
    // ITEM EVENTS → Career, Survival
    // ==========================================

    GE.on('itemCollected', (data) => {
        if (window.CareerSystem) {
            const cd = CareerSystem.getState();
            const source = data.source || '';
            if (source === 'herb' || source === 'plant') {
                if (cd.activeCareers.includes('sammler'))  CareerSystem.addCareerXP('sammler', 5);
                if (cd.activeCareers.includes('gaertner')) CareerSystem.addCareerXP('gaertner', 3);
            }
            if (source === 'ore' || source === 'crystal') {
                if (cd.activeCareers.includes('minenarbeiter')) CareerSystem.addCareerXP('minenarbeiter', 5);
            }
            if (source === 'wood') {
                if (cd.activeCareers.includes('holzfaeller')) CareerSystem.addCareerXP('holzfaeller', 5);
            }
            if (source === 'fish') {
                if (cd.activeCareers.includes('fischer')) CareerSystem.addCareerXP('fischer', 5);
            }
            if (source === 'hunt' || source === 'hide') {
                if (cd.activeCareers.includes('jaeger')) CareerSystem.addCareerXP('jaeger', 5);
            }
        }
    });

    // ==========================================
    // PLAYER EVENTS → Survival
    // ==========================================

    GE.on('playerDamaged', (data) => {
        if (window.SurvivalSystem) {
            SurvivalSystem.applyDamage(data.amount, data.source || 'unknown');
        }
    });

    GE.on('playerDied', (data) => {
        // Career: Sterben reduziert XP leicht
        if (window.CareerSystem) {
            const cd = CareerSystem.getState();
            cd.activeCareers.forEach(careerId => {
                // Lose 5% of current career XP (soft penalty)
                const career = CareerSystem.getCareerInfo?.(careerId);
                if (career && career.xp > 0) {
                    CareerSystem.addCareerXP(careerId, -Math.floor(career.xp * 0.05));
                }
            });
        }

        // Faction: Tod senkt etwas Ruf (man wird als schwach angesehen)
        if (window.FactionSystem) {
            FactionSystem.performAction('niederlage', { intensity: 1 });
        }
    });

    GE.on('playerRespawned', (data) => {
        console.log(`🔄 Player respawned at: ${data.location || 'unknown'}`);
    });

    GE.on('playerRested', (data) => {
        // Guter Schlaf in Inn → Mood
        if (window.SurvivalSystem && data.type === 'inn') {
            SurvivalSystem.addMoodlet('well_rested', '🛏️ Gut geschlafen!', +8, 1800000);
        }
    });

    GE.on('playerAte', (data) => {
        if (window.CareerSystem) {
            const cd = CareerSystem.getState();
            if (cd.activeCareers.includes('koch')) CareerSystem.addCareerXP('koch', 2);
        }
    });

    // ==========================================
    // FORGE/WEAPON EVENTS → Career, Economy
    // ==========================================

    GE.on('weaponUpgraded', (data) => {
        if (window.CareerSystem) {
            const cd = CareerSystem.getState();
            if (cd.activeCareers.includes('schmied')) CareerSystem.addCareerXP('schmied', 15);
        }
    });

    GE.on('weaponRepaired', (data) => {
        if (window.CareerSystem) {
            const cd = CareerSystem.getState();
            if (cd.activeCareers.includes('schmied')) CareerSystem.addCareerXP('schmied', 8);
        }
    });

    GE.on('weaponInfused', (data) => {
        if (window.CareerSystem) {
            const cd = CareerSystem.getState();
            if (cd.activeCareers.includes('schmied'))    CareerSystem.addCareerXP('schmied', 20);
            if (cd.activeCareers.includes('alchemist'))  CareerSystem.addCareerXP('alchemist', 10);
        }
    });

    // ==========================================
    // CREATURE CAPTURE UI - Zähmen/Anwerben Dialog
    // ==========================================

    function showCreatureCaptureUI(enemy, canTame, canRecruit) {
        let overlay = document.getElementById('creature-capture-overlay');
        if (overlay) overlay.remove();

        overlay = document.createElement('div');
        overlay.id = 'creature-capture-overlay';
        overlay.style.cssText = `
            position:fixed; top:0; left:0; width:100%; height:100%;
            background:rgba(0,0,0,0.85); z-index:16000;
            display:flex; align-items:center; justify-content:center;
        `;

        const name = enemy.name || enemy.id;
        let buttons = '';

        if (canTame && window.CreatureTaming) {
            buttons += `
                <button onclick="
                    window.CreatureTaming.startTaming('${enemy.id}', '${enemy.tameFood || 'brot'}');
                    document.getElementById('creature-capture-overlay').remove();
                    if(window.GameEvents) GameEvents.emit('creatureTamed', {creatureId:'${enemy.id}'});
                " style="background:linear-gradient(135deg,#27ae60,#2ecc71);color:#fff;border:none;
                    padding:15px;border-radius:10px;cursor:pointer;font-size:15px;text-align:left;">
                    🐾 <strong>Zähmen</strong> - Füttern und Geduld zeigen
                    <br><small style="color:#aaffaa">Wird ein Farmtier / Reittier</small>
                </button>`;
        }

        if (canRecruit && window.CreatureRecruit) {
            buttons += `
                <button onclick="
                    window.CreatureRecruit.recruitCreature('${enemy.id}', {method:'after_combat'});
                    document.getElementById('creature-capture-overlay').remove();
                    if(window.GameEvents) GameEvents.emit('creatureRecruited', {creatureId:'${enemy.id}'});
                " style="background:linear-gradient(135deg,#2980b9,#3498db);color:#fff;border:none;
                    padding:15px;border-radius:10px;cursor:pointer;font-size:15px;text-align:left;">
                    🤝 <strong>Anwerben</strong> - In deinen Dienst stellen
                    <br><small style="color:#aaddff">Wird ein Arbeiter / Kämpfer</small>
                </button>`;
        }

        buttons += `
            <button onclick="document.getElementById('creature-capture-overlay').remove()" style="
                background:#555;color:#fff;border:none;padding:12px;border-radius:10px;
                cursor:pointer;font-size:14px;">
                Gehen lassen
            </button>`;

        overlay.innerHTML = `
            <div style="background:linear-gradient(135deg,#1a1a2e,#1e2a3e);
                border:3px solid #00E676;border-radius:15px;padding:25px;
                max-width:400px;width:90%;color:#fff;font-family:'Segoe UI',Arial,sans-serif;">
                <h2 style="color:#00E676;margin:0 0 15px;text-align:center">🐾 ${name} besiegt!</h2>
                <p style="color:#ccc;text-align:center;margin-bottom:20px">Die Kreatur liegt am Boden. Was tust du?</p>
                <div style="display:grid;gap:10px;">${buttons}</div>
            </div>`;

        overlay.addEventListener('click', (e) => { if (e.target === overlay) overlay.remove(); });
        document.body.appendChild(overlay);
    }

    // ==========================================
    // CREATURE EVENTS → Faction, Career, Survival
    // ==========================================

    GE.on('creatureTamed', (data) => {
        if (window.CareerSystem) {
            const cd = CareerSystem.getState();
            if (cd.activeCareers.includes('tiermeister')) CareerSystem.addCareerXP('tiermeister', 20);
        }
        if (window.SurvivalSystem) {
            SurvivalSystem.addMoodlet('tamed', '🐾 Tier gezähmt!', +10, 600000);
        }
    });

    GE.on('creatureRecruited', (data) => {
        if (window.CareerSystem) {
            const cd = CareerSystem.getState();
            if (cd.activeCareers.includes('tiermeister')) CareerSystem.addCareerXP('tiermeister', 15);
            if (cd.activeCareers.includes('diplomat'))    CareerSystem.addCareerXP('diplomat', 10);
        }
    });

    // ==========================================
    // LEVEL UP → Global Notification
    // ==========================================

    GE.on('levelUp', (data) => {
        if (window.SurvivalSystem) {
            SurvivalSystem.addMoodlet('leveled_up', '⬆️ Level Up!', +15, 600000);
        }
    });

    // ==========================================
    // TAGES-ZYKLUS (alle Systeme synchron updaten)
    // ==========================================

    GE.on('newDay', (data) => {
        console.log(`🌅 Neuer Tag: ${data.day || '?'}`);

        if (window.FactionSystem)  FactionSystem.dailyUpdate();
        if (window.EconomySystem)  EconomySystem.dailyEconomyUpdate();
        if (window.SurvivalSystem) SurvivalSystem.dailyLawUpdate();
        if (window.CreatureTaming) CreatureTaming.dailyUpdate();
        if (window.CreatureRecruit) CreatureRecruit.dailyUpdate();

        // NPC Schedule aktualisieren
        if (window.NPCScheduleSystem) {
            NPCScheduleSystem.advanceTime(1440); // 1 Tag = 1440 Minuten
        }
    });

    // ==========================================
    // ECONOMY BRIDGE: Shop-Interaktionen emittieren
    // ==========================================

    // Wenn ein Shop-Kauf passiert, emit itemPurchased
    const origBuyGood = window.EconomySystem?.buyGood;
    if (origBuyGood && window.EconomySystem) {
        window.EconomySystem.buyGood = function(goodId, region, quantity) {
            const result = origBuyGood.call(this, goodId, region, quantity);
            if (result.success) {
                GE.emit('itemPurchased', {
                    itemId: goodId,
                    price: result.totalCost,
                    region,
                    quantity,
                });
            }
            return result;
        };
    }

    // ==========================================
    // TAGES-TIMER: Automatisch newDay emittieren
    // ==========================================
    // Ein Spieltag = 20 Minuten Echtzeit

    let lastDayCheck = Date.now();
    const DAY_LENGTH_MS = 20 * 60 * 1000; // 20 Minuten

    setInterval(() => {
        const now = Date.now();
        if (now - lastDayCheck >= DAY_LENGTH_MS) {
            lastDayCheck = now;
            const day = window.NPCScheduleSystem?.getGameTime?.()?.day || Math.floor(Date.now() / DAY_LENGTH_MS);
            GE.emit('newDay', { day });
        }
    }, 60000); // Check jede Minute

    // ==========================================
    // INITIALIZE NPC SYSTEMS
    // ==========================================

    // Schedule + Personality must init AFTER OverworldNPCs is available
    if (window.NPCScheduleSystem && window.NPCScheduleSystem.init) {
        try {
            window.NPCScheduleSystem.init();
            console.log('🕐 NPC Schedule System initialized via bridge');
        } catch(e) { console.warn('⚠️ NPC Schedule init error:', e); }
    }

    if (window.NPCPersonalitySystem && window.NPCPersonalitySystem.init) {
        try {
            window.NPCPersonalitySystem.init();
            console.log('🧠 NPC Personality System initialized via bridge');
        } catch(e) { console.warn('⚠️ NPC Personality init error:', e); }
    }

    // ==========================================
    // STARTUP LOG
    // ==========================================

    const systems = [];
    if (window.FactionSystem)       systems.push('Factions');
    if (window.EconomySystem)       systems.push('Economy');
    if (window.SurvivalSystem)      systems.push('Survival');
    if (window.CareerSystem)        systems.push('Career');
    if (window.CreatureTaming)      systems.push('Taming');
    if (window.CreatureRecruit)     systems.push('Recruit');
    if (window.NPCScheduleSystem)   systems.push('NPC-Schedule');
    if (window.NPCPersonalitySystem) systems.push('NPC-Personality');

    console.log(`🔗 GameEvents Bridge geladen! ${systems.length} Systeme verdrahtet: ${systems.join(', ')}`);

    // ==========================================
    // GLOBALER INPUT-DIALOG (prompt()-Ersatz)
    // ==========================================

    window.showInputDialog = function(title, defaultVal, callback) {
        const overlay = document.createElement('div');
        overlay.id = 'input-dialog-overlay';
        overlay.style.cssText = `
            position:fixed;inset:0;background:rgba(0,0,0,0.7);
            display:flex;align-items:center;justify-content:center;
            z-index:10002;font-family:'Segoe UI',Arial,sans-serif;
        `;

        const box = document.createElement('div');
        box.style.cssText = `
            background:#1a1a2e;border:2px solid #d4af37;border-radius:12px;
            padding:20px;max-width:380px;width:90%;color:#fff;
        `;
        box.innerHTML = `
            <h3 style="color:#ffd700;margin:0 0 12px;font-size:16px;">${title}</h3>
            <input id="input-dialog-field" type="text" value="${(defaultVal || '').replace(/"/g, '&quot;')}"
                style="width:100%;padding:10px;border:1px solid #555;border-radius:6px;
                background:#0a0a1a;color:#fff;font-size:14px;box-sizing:border-box;outline:none;"
                autocomplete="off">
            <div style="display:flex;gap:10px;margin-top:12px;justify-content:flex-end;">
                <button id="input-dialog-cancel" style="padding:8px 18px;background:#555;border:none;
                    border-radius:6px;color:#fff;cursor:pointer;">Abbrechen</button>
                <button id="input-dialog-ok" style="padding:8px 18px;background:#228b22;border:none;
                    border-radius:6px;color:#fff;cursor:pointer;font-weight:bold;">OK</button>
            </div>
        `;
        overlay.appendChild(box);
        document.body.appendChild(overlay);

        const input = document.getElementById('input-dialog-field');
        input.focus();
        input.select();

        function close(val) {
            if (overlay.parentNode) overlay.remove();
            if (callback) callback(val);
        }

        document.getElementById('input-dialog-ok').onclick = () => close(input.value);
        document.getElementById('input-dialog-cancel').onclick = () => close(null);
        input.onkeydown = (e) => {
            if (e.key === 'Enter') close(input.value);
            if (e.key === 'Escape') close(null);
        };
        overlay.onclick = (e) => { if (e.target === overlay) close(null); };
    };

})();
