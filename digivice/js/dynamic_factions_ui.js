/**
 * NAJIKA WORLD - DYNAMISCHE VOELKER UI
 * =====================================
 * Wild-Monster bilden spontan Voelker (1-5 pro Region).
 * Voelker wachsen, fuehren Kriege, kollabieren.
 * GETRENNT von statischen Fraktionen (faction_system.js)!
 *
 * Integration: Nutzt FactionSystem fuer Reputation-Mechaniken.
 * Backend: OPUS-1 (najika_dynamic_factions.py) - hier nur Frontend/UI.
 */
(function() {
    'use strict';

    // ==========================================
    // REGIONEN & VOELKER-TYPEN
    // ==========================================

    const REGIONS = {
        heisse_duenen:      { name: 'Heisse Duenen',       icon: '\u{1F3DC}', color: '#DAA520', maxVolker: 4 },
        samtmoos_tiefwald:  { name: 'Samtmoos-Tiefwald',   icon: '\u{1F332}', color: '#228B22', maxVolker: 3 },
        gruenschlamm_sumpf: { name: 'Gruenschlamm-Sumpf',  icon: '\u{1FAB9}', color: '#556B2F', maxVolker: 3 },
        magmastroeme:       { name: 'Magmastroeme',        icon: '\u{1F30B}', color: '#FF4500', maxVolker: 3 },
        reich_der_drei:     { name: 'Reich der Drei',       icon: '\u2744',    color: '#87CEEB', maxVolker: 5 },
        blitzebene:         { name: 'Blitzebene',          icon: '\u26A1',    color: '#FFD700', maxVolker: 4 },
        salzwind_kueste:    { name: 'Salzwind-Kueste',     icon: '\u{1F30A}', color: '#4682B4', maxVolker: 4 },
        tiefenhoehlen:      { name: 'Tiefenhoehlen',       icon: '\u{1F573}', color: '#8B4513', maxVolker: 5 },
    };

    // Voelker-Template-Namen pro Region (zufaellig kombiniert)
    const VOELKER_PREFIXES = {
        heisse_duenen:      ['Wuesten', 'Sand', 'Duenen', 'Oasen', 'Glut'],
        samtmoos_tiefwald:  ['Wald', 'Moos', 'Wurzel', 'Schatten', 'Blatt'],
        gruenschlamm_sumpf: ['Sumpf', 'Morast', 'Gift', 'Nebel', 'Schlamm'],
        magmastroeme:       ['Vulkan', 'Magma', 'Asche', 'Glut', 'Flammen'],
        reich_der_drei:     ['Eis', 'Frost', 'Schnee', 'Kristall', 'Nord'],
        blitzebene:         ['Blitz', 'Sturm', 'Donner', 'Wind', 'Strom'],
        salzwind_kueste:    ['Wellen', 'Salz', 'Flut', 'Korallen', 'Tide'],
        tiefenhoehlen:      ['Tiefen', 'Schatten', 'Kristall', 'Hoehlen', 'Dunkel'],
    };

    const VOELKER_SUFFIXES = [
        'Raeuber', 'Druiden', 'Jaeger', 'Krieger', 'Kult',
        'Zirkel', 'Klan', 'Bande', 'Horde', 'Gilde',
        'Stamm', 'Pakt', 'Orden', 'Meute', 'Schwarm',
    ];

    // AI-Level der Voelker
    const AI_LEVELS = {
        1: { name: 'Wilde',       color: '#888',    desc: 'Lose Gruppe, kaum Organisation' },
        2: { name: 'Stamm',       color: '#DAA520', desc: 'Einfache Hierarchie, teilen Beute' },
        3: { name: 'Clan',        color: '#2ecc71', desc: 'Fester Anspruch auf Territorium' },
        4: { name: 'Koenigreich', color: '#3498db', desc: 'Staerke Struktur, Handel moeglich' },
        5: { name: 'Imperium',    color: '#9b59b6', desc: 'Dominante Macht in der Region' },
    };

    // ==========================================
    // DYNAMISCHE VOELKER STATE
    // ==========================================

    let dynamicState = loadDynamicState();

    function loadDynamicState() {
        try {
            return JSON.parse(localStorage.getItem('najika_dynamic_factions') || 'null') || createFreshState();
        } catch { return createFreshState(); }
    }

    function createFreshState() {
        return {
            voelker: [],            // Array of Volk objects
            wars: [],               // Active wars between Voelker
            events: [],             // History log (last 50)
            playerRep: {},          // { volkId: reputation (-100 to 100) }
            lastUpdate: Date.now(),
            dayCounter: 0,
        };
    }

    function saveDynamicState() {
        // Keep events capped at 50
        if (dynamicState.events.length > 50) {
            dynamicState.events = dynamicState.events.slice(-50);
        }
        localStorage.setItem('najika_dynamic_factions', JSON.stringify(dynamicState));
    }

    // ==========================================
    // VOLK GENERIERUNG
    // ==========================================

    function generateVolkName(regionId) {
        const prefixes = VOELKER_PREFIXES[regionId] || ['Unbekannt'];
        const prefix = prefixes[Math.floor(Math.random() * prefixes.length)];
        const suffix = VOELKER_SUFFIXES[Math.floor(Math.random() * VOELKER_SUFFIXES.length)];
        return `${prefix}-${suffix}`;
    }

    function generateVolkId() {
        return 'volk_' + Date.now().toString(36) + '_' + Math.random().toString(36).substr(2, 4);
    }

    function spawnVolk(regionId) {
        const region = REGIONS[regionId];
        if (!region) return null;

        const volkInRegion = dynamicState.voelker.filter(v => v.region === regionId && v.alive);
        if (volkInRegion.length >= region.maxVolker) return null;

        const volk = {
            id: generateVolkId(),
            name: generateVolkName(regionId),
            region: regionId,
            aiLevel: 1,
            members: 3 + Math.floor(Math.random() * 5), // 3-7 initial
            maxMembers: 20,
            strength: 10 + Math.floor(Math.random() * 20),
            territory: 1, // 1-5 Gebiete
            resources: Math.floor(Math.random() * 50),
            aggression: 0.2 + Math.random() * 0.6, // 0.2-0.8
            alive: true,
            formedDay: dynamicState.dayCounter,
            traits: pickTraits(),
        };

        dynamicState.voelker.push(volk);
        dynamicState.playerRep[volk.id] = 0;

        addEvent('volk_formed', `${volk.name} hat sich in ${region.name} gebildet!`, volk.id);
        saveDynamicState();
        return volk;
    }

    function pickTraits() {
        const allTraits = [
            'aggressiv', 'friedlich', 'handelnd', 'territorial',
            'nomadisch', 'rituell', 'kriegerisch', 'scheu',
            'sammler', 'jaeger', 'plunderer', 'verteidiger',
        ];
        const count = 1 + Math.floor(Math.random() * 2);
        const shuffled = allTraits.sort(() => Math.random() - 0.5);
        return shuffled.slice(0, count);
    }

    // ==========================================
    // DAILY UPDATE (aufgerufen von Game-Loop)
    // ==========================================

    function dailyUpdate() {
        dynamicState.dayCounter++;

        // 1. Neue Voelker entstehen (Chance pro leere Region)
        Object.keys(REGIONS).forEach(regionId => {
            const volkCount = dynamicState.voelker.filter(v => v.region === regionId && v.alive).length;
            if (volkCount === 0 && Math.random() < 0.15) {
                spawnVolk(regionId);
            } else if (volkCount < 2 && Math.random() < 0.05) {
                spawnVolk(regionId);
            }
        });

        // 2. Voelker wachsen/schrumpfen
        dynamicState.voelker.filter(v => v.alive).forEach(volk => {
            growVolk(volk);
        });

        // 3. Kriege
        checkNewWars();
        advanceWars();

        // 4. Voelker kollabieren
        dynamicState.voelker.filter(v => v.alive).forEach(volk => {
            if (volk.members <= 0 || volk.strength <= 0) {
                collapseVolk(volk);
            }
        });

        saveDynamicState();
    }

    function growVolk(volk) {
        // Wachstum basiert auf Ressourcen und AI-Level
        if (volk.resources > 20 && volk.members < volk.maxMembers) {
            volk.members += Math.random() < 0.3 ? 1 : 0;
            volk.resources -= 5;
        }

        // Ressourcen sammeln
        volk.resources += volk.members * (0.5 + volk.aiLevel * 0.3);
        volk.resources = Math.min(200, volk.resources);

        // Staerke passt sich an
        volk.strength = Math.floor(volk.members * (2 + volk.aiLevel) + volk.resources * 0.1);

        // AI-Level steigt bei genug Mitgliedern und Ressourcen
        if (volk.members >= 8 && volk.aiLevel < 2 && volk.resources > 30) {
            volk.aiLevel = 2;
            addEvent('volk_evolved', `${volk.name} ist zu einem Stamm gewachsen!`, volk.id);
        } else if (volk.members >= 12 && volk.aiLevel < 3 && volk.resources > 60) {
            volk.aiLevel = 3;
            volk.territory = Math.min(3, volk.territory + 1);
            addEvent('volk_evolved', `${volk.name} beansprucht Territorium als Clan!`, volk.id);
        } else if (volk.members >= 16 && volk.aiLevel < 4 && volk.resources > 100) {
            volk.aiLevel = 4;
            volk.territory = Math.min(4, volk.territory + 1);
            addEvent('volk_evolved', `${volk.name} ist jetzt ein Koenigreich!`, volk.id);
        } else if (volk.members >= 20 && volk.aiLevel < 5 && volk.resources > 150) {
            volk.aiLevel = 5;
            volk.territory = 5;
            addEvent('volk_evolved', `${volk.name} hat Imperium-Status erreicht!`, volk.id);
        }

        // Natuerlicher Verfall - schwache Voelker schrumpfen
        if (volk.resources < 5 && Math.random() < 0.2) {
            volk.members = Math.max(0, volk.members - 1);
        }
    }

    function checkNewWars() {
        const alive = dynamicState.voelker.filter(v => v.alive);

        // Voelker in derselben Region koennen sich bekriegen
        Object.keys(REGIONS).forEach(regionId => {
            const regional = alive.filter(v => v.region === regionId);
            if (regional.length < 2) return;

            for (let i = 0; i < regional.length; i++) {
                for (let j = i + 1; j < regional.length; j++) {
                    const a = regional[i];
                    const b = regional[j];

                    // Existiert schon ein Krieg?
                    const existing = dynamicState.wars.find(w =>
                        !w.winner && ((w.attacker === a.id && w.defender === b.id) ||
                        (w.attacker === b.id && w.defender === a.id))
                    );
                    if (existing) continue;

                    // Kriegs-Chance basiert auf Aggression und Territory-Overlap
                    const warChance = (a.aggression + b.aggression) * 0.03;
                    if (regional.length > 3) {
                        // Mehr Voelker = mehr Konflikte
                        if (Math.random() < warChance * 1.5) {
                            startWar(a, b);
                        }
                    } else if (Math.random() < warChance) {
                        startWar(a, b);
                    }
                }
            }
        });
    }

    function startWar(attacker, defender) {
        const war = {
            id: 'war_' + Date.now().toString(36),
            attacker: attacker.id,
            defender: defender.id,
            attackerName: attacker.name,
            defenderName: defender.name,
            region: attacker.region,
            startDay: dynamicState.dayCounter,
            battles: 0,
            attackerWins: 0,
            defenderWins: 0,
            winner: null,
        };

        dynamicState.wars.push(war);
        const region = REGIONS[attacker.region];
        addEvent('war_started', `KRIEG in ${region?.name || '?'}! ${attacker.name} vs ${defender.name}!`, null, 'war');

        showWarNotification(attacker.name, defender.name, region?.name || '?');
    }

    function advanceWars() {
        dynamicState.wars.filter(w => !w.winner).forEach(war => {
            const attacker = dynamicState.voelker.find(v => v.id === war.attacker);
            const defender = dynamicState.voelker.find(v => v.id === war.defender);

            if (!attacker?.alive || !defender?.alive) {
                war.winner = attacker?.alive ? war.attacker : war.defender;
                return;
            }

            // Battle!
            if (Math.random() < 0.4) {
                war.battles++;
                const attackPower = attacker.strength * (0.7 + Math.random() * 0.6);
                const defendPower = defender.strength * (0.7 + Math.random() * 0.6);

                if (attackPower > defendPower) {
                    war.attackerWins++;
                    defender.members = Math.max(0, defender.members - (1 + Math.floor(Math.random() * 2)));
                    defender.resources = Math.max(0, defender.resources - 10);
                    attacker.resources += 5; // Plunder
                } else {
                    war.defenderWins++;
                    attacker.members = Math.max(0, attacker.members - (1 + Math.floor(Math.random() * 2)));
                    attacker.resources = Math.max(0, attacker.resources - 10);
                    defender.resources += 5;
                }
            }

            // Krieg endet?
            if (war.battles >= 5 || attacker.members <= 1 || defender.members <= 1) {
                war.winner = war.attackerWins >= war.defenderWins ? war.attacker : war.defender;
                const winnerVolk = dynamicState.voelker.find(v => v.id === war.winner);
                const loserVolk = dynamicState.voelker.find(v => v.id === (war.winner === war.attacker ? war.defender : war.attacker));

                if (winnerVolk) {
                    winnerVolk.territory = Math.min(5, winnerVolk.territory + 1);
                    addEvent('war_won', `${winnerVolk.name} hat den Krieg gegen ${loserVolk?.name || '?'} gewonnen!`, winnerVolk.id);
                }
            }
        });

        // Alte beendete Kriege aufraeumen (nach 10 Tagen)
        dynamicState.wars = dynamicState.wars.filter(w =>
            !w.winner || (dynamicState.dayCounter - w.startDay) < 10
        );
    }

    function collapseVolk(volk) {
        volk.alive = false;
        const region = REGIONS[volk.region];
        addEvent('volk_collapsed', `${volk.name} in ${region?.name || '?'} ist zerfallen!`, volk.id);
    }

    // ==========================================
    // SPIELER-INTERAKTION
    // ==========================================

    function changePlayerRep(volkId, amount) {
        if (!dynamicState.playerRep[volkId] && dynamicState.playerRep[volkId] !== 0) return;
        dynamicState.playerRep[volkId] = Math.max(-100, Math.min(100, (dynamicState.playerRep[volkId] || 0) + amount));
        saveDynamicState();
    }

    function getPlayerRep(volkId) {
        return dynamicState.playerRep[volkId] || 0;
    }

    function getRepLabel(rep) {
        if (rep >= 80)  return { name: 'Verbuendeter', color: '#2ecc71', icon: '\u2764' };
        if (rep >= 40)  return { name: 'Freund',       color: '#3498db', icon: '\u{1F91D}' };
        if (rep >= 10)  return { name: 'Bekannt',      color: '#f39c12', icon: '\u{1F44B}' };
        if (rep > -10)  return { name: 'Neutral',      color: '#888',    icon: '\u2796' };
        if (rep > -40)  return { name: 'Misstrauisch', color: '#e67e22', icon: '\u{1F440}' };
        if (rep > -80)  return { name: 'Feindlich',    color: '#e74c3c', icon: '\u2694' };
        return               { name: 'Erzfeind',     color: '#c0392b', icon: '\u2620' };
    }

    // ==========================================
    // EVENT LOG
    // ==========================================

    function addEvent(type, description, volkId, category) {
        dynamicState.events.push({
            type,
            description,
            volkId,
            category: category || 'info',
            day: dynamicState.dayCounter,
            timestamp: Date.now(),
        });
    }

    // ==========================================
    // NOTIFICATIONS
    // ==========================================

    function showWarNotification(attackerName, defenderName, regionName) {
        const el = document.createElement('div');
        el.style.cssText = `
            position: fixed; top: 80px; left: 50%; transform: translateX(-50%);
            background: linear-gradient(135deg, rgba(231,76,60,0.95), rgba(192,57,43,0.95));
            border: 2px solid #e74c3c; border-radius: 10px; padding: 15px 25px;
            color: white; font-family: 'Courier New', monospace; z-index: 10001;
            text-align: center; animation: fadeInDown 0.3s ease;
            box-shadow: 0 4px 20px rgba(231,76,60,0.5);
        `;
        el.innerHTML = `
            <div style="font-size: 18px; font-weight: bold; margin-bottom: 5px;">KRIEG!</div>
            <div style="font-size: 13px;">${attackerName} vs ${defenderName}</div>
            <div style="font-size: 11px; color: rgba(255,255,255,0.7); margin-top: 3px;">${regionName}</div>
        `;
        document.body.appendChild(el);
        setTimeout(() => {
            el.style.opacity = '0';
            el.style.transition = 'opacity 0.5s';
            setTimeout(() => el.remove(), 500);
        }, 4000);
    }

    function showEventNotification(text, type) {
        const colors = {
            info: { bg: 'rgba(52,152,219,0.9)', border: '#3498db' },
            war: { bg: 'rgba(231,76,60,0.9)', border: '#e74c3c' },
            growth: { bg: 'rgba(46,204,113,0.9)', border: '#2ecc71' },
            collapse: { bg: 'rgba(149,165,166,0.9)', border: '#95a5a6' },
        };
        const c = colors[type] || colors.info;

        const el = document.createElement('div');
        el.style.cssText = `
            position: fixed; top: 80px; right: 20px;
            background: ${c.bg}; border: 1px solid ${c.border};
            border-radius: 8px; padding: 10px 15px; color: white;
            font-family: 'Courier New', monospace; font-size: 12px;
            z-index: 10001; max-width: 300px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        `;
        el.textContent = text;
        document.body.appendChild(el);
        setTimeout(() => {
            el.style.opacity = '0';
            el.style.transition = 'opacity 0.5s';
            setTimeout(() => el.remove(), 500);
        }, 3000);
    }

    // ==========================================
    // UI CLASS
    // ==========================================

    class DynamicFactionsUI {
        constructor() {
            this.isOpen = false;
            this.overlay = null;
            this.selectedVolk = null;
            this.activeTab = 'overview'; // overview, wars, events
        }

        open() {
            if (this.isOpen) return;
            this.isOpen = true;
            this.overlay = document.createElement('div');
            this.overlay.id = 'dynamic-factions-overlay';
            this.overlay.style.cssText = `
                position: fixed; top: 0; left: 0; right: 0; bottom: 0;
                background: rgba(0, 0, 0, 0.95);
                z-index: 10000; display: flex; flex-direction: column;
                font-family: 'Courier New', monospace; color: #e0e0e0; overflow-y: auto;
            `;
            this.render();
            document.body.appendChild(this.overlay);
            this._keyHandler = (e) => { if (e.key === 'Escape') this.close(); };
            document.addEventListener('keydown', this._keyHandler);
        }

        close() {
            if (!this.isOpen) return;
            this.isOpen = false;
            if (this.overlay) { this.overlay.remove(); this.overlay = null; }
            document.removeEventListener('keydown', this._keyHandler);
        }

        toggle() { this.isOpen ? this.close() : this.open(); }

        setTab(tab) {
            this.activeTab = tab;
            this.render();
        }

        selectVolk(id) {
            this.selectedVolk = this.selectedVolk === id ? null : id;
            this.render();
        }

        render() {
            if (!this.overlay) return;

            const aliveVolker = dynamicState.voelker.filter(v => v.alive);
            const activeWars = dynamicState.wars.filter(w => !w.winner);

            this.overlay.innerHTML = `
                <div style="max-width: 1000px; margin: 0 auto; padding: 20px; width: 100%;">
                    <!-- Header -->
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; border-bottom: 2px solid #e67e22; padding-bottom: 10px;">
                        <h1 style="margin: 0; color: #e67e22; font-size: 22px;">DYNAMISCHE VOELKER</h1>
                        <div style="display: flex; gap: 8px; align-items: center;">
                            <span style="font-size: 11px; color: #888;">Tag ${dynamicState.dayCounter} | ${aliveVolker.length} Voelker | ${activeWars.length} Kriege</span>
                            <button onclick="window.dynamicFactionsUI.close()" style="background: #c0392b; border: none; color: white; padding: 6px 14px; border-radius: 5px; cursor: pointer; font-size: 14px; font-family: inherit;">ESC</button>
                        </div>
                    </div>

                    <!-- Tabs -->
                    <div style="display: flex; gap: 4px; margin-bottom: 15px;">
                        ${this._renderTab('overview', 'Regionen')}
                        ${this._renderTab('wars', `Kriege (${activeWars.length})`)}
                        ${this._renderTab('events', 'Chronik')}
                    </div>

                    <!-- Content -->
                    ${this.activeTab === 'overview' ? this._renderOverview(aliveVolker) : ''}
                    ${this.activeTab === 'wars' ? this._renderWars(activeWars) : ''}
                    ${this.activeTab === 'events' ? this._renderEvents() : ''}
                </div>
            `;
        }

        _renderTab(id, label) {
            const active = this.activeTab === id;
            return `<button onclick="window.dynamicFactionsUI.setTab('${id}')" style="
                background: ${active ? '#e67e22' : 'rgba(30,30,50,0.9)'};
                border: 1px solid ${active ? '#e67e22' : '#555'};
                color: ${active ? '#000' : '#ccc'};
                padding: 6px 14px; border-radius: 5px; cursor: pointer;
                font-family: inherit; font-size: 12px; font-weight: ${active ? 'bold' : 'normal'};
            ">${label}</button>`;
        }

        // ---- OVERVIEW TAB ----
        _renderOverview(aliveVolker) {
            const grouped = {};
            Object.keys(REGIONS).forEach(rid => { grouped[rid] = []; });
            aliveVolker.forEach(v => {
                if (grouped[v.region]) grouped[v.region].push(v);
            });

            return `
                <div style="display: grid; grid-template-columns: 1fr ${this.selectedVolk ? '1fr' : ''}; gap: 15px;">
                    <div>
                        ${Object.entries(REGIONS).map(([rid, r]) => {
                            const voelker = grouped[rid] || [];
                            return `
                            <div style="background: rgba(30,30,50,0.9); border: 1px solid ${r.color}33; border-left: 3px solid ${r.color}; border-radius: 6px; padding: 10px; margin-bottom: 8px;">
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                                    <span style="font-size: 13px; color: ${r.color}; font-weight: bold;">${r.icon} ${r.name}</span>
                                    <span style="font-size: 10px; color: #666;">${voelker.length}/${r.maxVolker} Voelker</span>
                                </div>
                                ${voelker.length === 0 ? '<div style="font-size: 11px; color: #444; font-style: italic;">Keine Voelker - nur wilde Monster</div>' : ''}
                                ${voelker.map(v => this._renderVolkRow(v, r)).join('')}
                            </div>`;
                        }).join('')}
                    </div>
                    ${this.selectedVolk ? this._renderVolkDetail() : ''}
                </div>
            `;
        }

        _renderVolkRow(volk, region) {
            const ai = AI_LEVELS[volk.aiLevel] || AI_LEVELS[1];
            const rep = getPlayerRep(volk.id);
            const repLabel = getRepLabel(rep);
            const selected = this.selectedVolk === volk.id;
            const atWar = dynamicState.wars.some(w => !w.winner && (w.attacker === volk.id || w.defender === volk.id));

            return `
                <div onclick="window.dynamicFactionsUI.selectVolk('${volk.id}')" style="
                    background: ${selected ? 'rgba(230,126,34,0.15)' : 'rgba(0,0,0,0.2)'};
                    border: 1px solid ${selected ? '#e67e22' : 'transparent'};
                    border-radius: 4px; padding: 6px 8px; margin-top: 4px; cursor: pointer;
                    display: flex; justify-content: space-between; align-items: center;
                ">
                    <div>
                        <span style="font-size: 12px; color: #ccc; font-weight: bold;">${volk.name}</span>
                        ${atWar ? '<span style="font-size: 10px; color: #e74c3c; margin-left: 5px;">IM KRIEG</span>' : ''}
                        <div style="font-size: 10px; color: ${ai.color};">${ai.name} (Lv.${volk.aiLevel}) | ${volk.members} Mitglieder</div>
                    </div>
                    <div style="text-align: right;">
                        <span style="font-size: 10px; color: ${repLabel.color};">${repLabel.icon} ${repLabel.name}</span>
                        <div style="background: #1a1a2e; border-radius: 2px; height: 3px; width: 60px; margin-top: 2px;">
                            <div style="background: ${ai.color}; height: 100%; width: ${Math.min(100, volk.strength)}%; border-radius: 2px;"></div>
                        </div>
                    </div>
                </div>
            `;
        }

        _renderVolkDetail() {
            const volk = dynamicState.voelker.find(v => v.id === this.selectedVolk);
            if (!volk) return '';

            const ai = AI_LEVELS[volk.aiLevel] || AI_LEVELS[1];
            const region = REGIONS[volk.region];
            const rep = getPlayerRep(volk.id);
            const repLabel = getRepLabel(rep);
            const activeWar = dynamicState.wars.find(w => !w.winner && (w.attacker === volk.id || w.defender === volk.id));
            const age = dynamicState.dayCounter - volk.formedDay;

            return `
                <div>
                    <div style="background: rgba(30,30,50,0.95); border: 1px solid #e67e22; border-radius: 8px; padding: 15px;">
                        <h2 style="color: #e67e22; margin: 0 0 10px; font-size: 18px;">${volk.name}</h2>
                        <div style="font-size: 11px; color: #888; margin-bottom: 10px;">${region?.icon || ''} ${region?.name || '?'} | Alter: ${age} Tage</div>

                        <!-- Stats Grid -->
                        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-bottom: 12px;">
                            <div style="background: rgba(0,0,0,0.3); padding: 8px; border-radius: 6px; text-align: center;">
                                <div style="font-size: 9px; color: #888;">AI-LEVEL</div>
                                <div style="font-size: 16px; color: ${ai.color}; font-weight: bold;">${volk.aiLevel}</div>
                                <div style="font-size: 10px; color: ${ai.color};">${ai.name}</div>
                            </div>
                            <div style="background: rgba(0,0,0,0.3); padding: 8px; border-radius: 6px; text-align: center;">
                                <div style="font-size: 9px; color: #888;">MITGLIEDER</div>
                                <div style="font-size: 16px; color: #ccc; font-weight: bold;">${volk.members}</div>
                                <div style="font-size: 10px; color: #666;">Max: ${volk.maxMembers}</div>
                            </div>
                            <div style="background: rgba(0,0,0,0.3); padding: 8px; border-radius: 6px; text-align: center;">
                                <div style="font-size: 9px; color: #888;">STAERKE</div>
                                <div style="font-size: 16px; color: #e74c3c; font-weight: bold;">${volk.strength}</div>
                                <div style="font-size: 10px; color: #666;">Territorium: ${volk.territory}</div>
                            </div>
                        </div>

                        <!-- Reputation -->
                        <div style="background: rgba(0,0,0,0.3); padding: 8px; border-radius: 6px; margin-bottom: 10px;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span style="font-size: 11px; color: #888;">Dein Ruf:</span>
                                <span style="font-size: 12px; color: ${repLabel.color}; font-weight: bold;">${repLabel.icon} ${repLabel.name} (${rep})</span>
                            </div>
                            <div style="background: #1a1a2e; border-radius: 3px; height: 6px; margin-top: 5px; overflow: hidden; position: relative;">
                                <div style="position: absolute; left: 50%; top: 0; width: 1px; height: 100%; background: #555;"></div>
                                <div style="background: ${rep >= 0 ? '#2ecc71' : '#e74c3c'}; height: 100%; width: ${Math.abs(rep) / 2}%; ${rep >= 0 ? 'margin-left: 50%' : 'margin-left: ' + (50 - Math.abs(rep) / 2) + '%'};"></div>
                            </div>
                        </div>

                        <!-- Traits -->
                        <div style="margin-bottom: 10px;">
                            <span style="font-size: 10px; color: #888;">Eigenschaften:</span>
                            <div style="display: flex; gap: 4px; flex-wrap: wrap; margin-top: 3px;">
                                ${(volk.traits || []).map(t => `<span style="font-size: 10px; background: rgba(230,126,34,0.2); border: 1px solid #e67e2244; border-radius: 3px; padding: 2px 6px; color: #e67e22;">${t}</span>`).join('')}
                            </div>
                        </div>

                        <!-- AI Level Description -->
                        <div style="font-size: 11px; color: #888; font-style: italic;">${ai.desc}</div>

                        <!-- Active War -->
                        ${activeWar ? `
                        <div style="background: rgba(231,76,60,0.15); border: 1px solid #e74c3c; border-radius: 6px; padding: 8px; margin-top: 10px;">
                            <div style="font-size: 11px; color: #e74c3c; font-weight: bold;">IM KRIEG</div>
                            <div style="font-size: 11px; color: #ccc;">
                                vs ${activeWar.attacker === volk.id ? activeWar.defenderName : activeWar.attackerName}
                                | Schlachten: ${activeWar.battles} | ${activeWar.attackerWins}:${activeWar.defenderWins}
                            </div>
                        </div>` : ''}

                        <!-- Resources -->
                        <div style="margin-top: 10px;">
                            <div style="font-size: 10px; color: #888; margin-bottom: 3px;">Ressourcen: ${Math.floor(volk.resources)}/200</div>
                            <div style="background: #1a1a2e; border-radius: 3px; height: 5px; overflow: hidden;">
                                <div style="background: #f39c12; height: 100%; width: ${volk.resources / 2}%;"></div>
                            </div>
                            <div style="font-size: 10px; color: #888; margin-top: 3px;">Aggression: ${Math.floor(volk.aggression * 100)}%</div>
                        </div>
                    </div>
                </div>
            `;
        }

        // ---- WARS TAB ----
        _renderWars(activeWars) {
            const finishedWars = dynamicState.wars.filter(w => w.winner);

            return `
                <div>
                    ${activeWars.length === 0 && finishedWars.length === 0 ?
                        '<div style="text-align: center; color: #555; padding: 40px; font-style: italic;">Kein Konflikt in der Welt... vorerst.</div>' : ''}

                    ${activeWars.length > 0 ? `
                    <div style="margin-bottom: 15px;">
                        <div style="font-size: 13px; color: #e74c3c; font-weight: bold; margin-bottom: 8px;">AKTIVE KRIEGE</div>
                        ${activeWars.map(w => this._renderWarCard(w, false)).join('')}
                    </div>` : ''}

                    ${finishedWars.length > 0 ? `
                    <div>
                        <div style="font-size: 13px; color: #888; font-weight: bold; margin-bottom: 8px;">VERGANGENE KRIEGE</div>
                        ${finishedWars.map(w => this._renderWarCard(w, true)).join('')}
                    </div>` : ''}
                </div>
            `;
        }

        _renderWarCard(war, finished) {
            const region = REGIONS[war.region];
            const winnerName = war.winner ? (dynamicState.voelker.find(v => v.id === war.winner)?.name || '?') : null;

            return `
                <div style="
                    background: rgba(30,30,50,0.9);
                    border: 1px solid ${finished ? '#555' : '#e74c3c'};
                    border-radius: 6px; padding: 10px; margin-bottom: 6px;
                    opacity: ${finished ? '0.7' : '1'};
                ">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="font-size: 13px; color: ${finished ? '#888' : '#e74c3c'}; font-weight: bold;">
                                ${war.attackerName} vs ${war.defenderName}
                            </span>
                            <div style="font-size: 10px; color: #666;">${region?.icon || ''} ${region?.name || '?'} | Tag ${war.startDay}</div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 12px; color: #ccc;">${war.attackerWins} : ${war.defenderWins}</div>
                            <div style="font-size: 10px; color: #666;">${war.battles} Schlachten</div>
                        </div>
                    </div>
                    ${winnerName ? `<div style="font-size: 11px; color: #2ecc71; margin-top: 4px;">Sieger: ${winnerName}</div>` : ''}
                </div>
            `;
        }

        // ---- EVENTS TAB ----
        _renderEvents() {
            const events = [...dynamicState.events].reverse().slice(0, 30);

            if (events.length === 0) {
                return '<div style="text-align: center; color: #555; padding: 40px; font-style: italic;">Keine Ereignisse bisher.</div>';
            }

            const typeColors = {
                volk_formed: '#2ecc71',
                volk_evolved: '#3498db',
                volk_collapsed: '#95a5a6',
                war_started: '#e74c3c',
                war_won: '#f39c12',
            };

            const typeIcons = {
                volk_formed: '\u{1F331}',
                volk_evolved: '\u2B06',
                volk_collapsed: '\u{1F480}',
                war_started: '\u2694',
                war_won: '\u{1F3C6}',
            };

            return `
                <div>
                    ${events.map(e => `
                        <div style="
                            background: rgba(30,30,50,0.9);
                            border-left: 3px solid ${typeColors[e.type] || '#555'};
                            border-radius: 4px; padding: 8px 10px; margin-bottom: 4px;
                            display: flex; justify-content: space-between; align-items: center;
                        ">
                            <div>
                                <span style="font-size: 12px;">${typeIcons[e.type] || '\u2022'}</span>
                                <span style="font-size: 11px; color: #ccc; margin-left: 5px;">${e.description}</span>
                            </div>
                            <span style="font-size: 10px; color: #555;">Tag ${e.day}</span>
                        </div>
                    `).join('')}
                </div>
            `;
        }
    }

    // ==========================================
    // EXPORT
    // ==========================================

    const ui = new DynamicFactionsUI();

    window.DynamicFactions = {
        // State
        getState: () => ({ ...dynamicState }),
        getAliveVolker: () => dynamicState.voelker.filter(v => v.alive),
        getVolkerInRegion: (regionId) => dynamicState.voelker.filter(v => v.alive && v.region === regionId),
        getActiveWars: () => dynamicState.wars.filter(w => !w.winner),

        // Actions
        spawnVolk,
        dailyUpdate,
        changePlayerRep,
        getPlayerRep,

        // Constants
        REGIONS,
        AI_LEVELS,

        // Save/Load
        save: saveDynamicState,
        load: () => { dynamicState = loadDynamicState(); },
        reset: () => { dynamicState = createFreshState(); saveDynamicState(); },
    };

    window.dynamicFactionsUI = ui;

    // Auf Seeder reagieren: Wenn WorldEventGenerator dailyUpdate macht, machen wir auch
    const origDailyUpdate = window.FactionSystem?.dailyUpdate;
    if (origDailyUpdate) {
        window.FactionSystem.dailyUpdate = function() {
            origDailyUpdate();
            dailyUpdate();
        };
    }

    const volkCount = dynamicState.voelker.filter(v => v.alive).length;
    const warCount = dynamicState.wars.filter(w => !w.winner).length;
    console.log(`\u{1F30D} Dynamische Voelker geladen! ${volkCount} Voelker aktiv | ${warCount} Kriege`);

})();
