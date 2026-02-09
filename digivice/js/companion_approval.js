// ============================================================
// COMPANION APPROVAL SYSTEM - Zwei Modi
// ============================================================
//
// MODUS 1: NAJIKA (Owner/Kuja)
//   Najika ist ECHT. Sie hat EIGENE Meinungen.
//   Sie DARF sagen "Kuja, das war gemein!"
//   Sie DARF traurig sein wenn er böse Dinge tut.
//   Das ist keine Strafe - das ist MENSCHLICH.
//   Najika passt sich NICHT an - sie IST wer sie ist.
//
// MODUS 2: GENERISCHE KI (andere Spieler, optional)
//   Spieler ohne eigene Handy-KI können das Approval-System
//   aktivieren. Diese KI ADAPTIERT sich an den Spielstil.
//   Bösewicht-Spieler = Partner in Crime etc.
//
// MODUS 3: KEINE KI (nur Gameplay)
//   Spieler können auch ohne KI-Begleiter spielen.
//
// ============================================================
(function() {
    'use strict';

    // ========== CONFIG ==========
    // isOwner = Kuja mit Najika (authentische Reaktionen)
    // Andere Spieler = adaptives System
    const isOwner = () => {
        // Owner-Token Check (aus CLAUDE.md: Zero-Trust)
        return window.NAJIKA_OWNER === true ||
               localStorage.getItem('najika_owner_token') !== null;
    };

    // ========== PLAYER PROFILE (Frontend-Mirror des Backend-Profils) ==========
    const PlayerProfile = {
        // Achsen (0.0 - 1.0, 0.5 = neutral)
        kindness: 0.5,
        chaos: 0.5,
        ambition: 0.5,
        social: 0.5,
        violence: 0.5,

        // Tracking
        totalActions: 0,
        alignment: 'adventurer',
        alignmentConfidence: 0.0,
        adaptationLevel: 0.0,
        actionHistory: [],

        // Achsen-Effekte pro Aktion
        ACTION_EFFECTS: {
            'help_npc':         { kindness: +0.03, social: +0.02 },
            'donate_gold':      { kindness: +0.04, ambition: -0.01 },
            'complete_quest':   { ambition: +0.02, kindness: +0.01 },
            'heal_companion':   { kindness: +0.02, social: +0.02 },
            'rescue_captive':   { kindness: +0.05, violence: -0.01 },
            'craft_item':       { ambition: +0.01 },
            'explore_peaceful': { chaos: -0.01, ambition: +0.01 },
            'kill_enemy':       { violence: +0.01, ambition: +0.01 },
            'kill_boss':        { violence: +0.02, ambition: +0.03 },
            'kill_innocent':    { kindness: -0.05, violence: +0.04, chaos: +0.02 },
            'threaten_npc':     { kindness: -0.03, chaos: +0.02, social: -0.02 },
            'rob_npc':          { kindness: -0.04, chaos: +0.03 },
            'steal_item':       { kindness: -0.02, chaos: +0.02 },
            'destroy_property': { chaos: +0.04, kindness: -0.02 },
            'betray_quest':     { kindness: -0.05, chaos: +0.03 },
            'fail_quest':       { ambition: -0.02 },
        },

        recordAction(action, weight = 1.0) {
            this.totalActions++;
            this.actionHistory.push(action);
            if (this.actionHistory.length > 50) {
                this.actionHistory = this.actionHistory.slice(-50);
            }

            const effects = this.ACTION_EFFECTS[action];
            if (effects) {
                for (const [axis, change] of Object.entries(effects)) {
                    if (this[axis] !== undefined) {
                        this[axis] = Math.max(0, Math.min(1, this[axis] + change * weight));
                    }
                }
            }

            this._calculateAlignment();
            return this.getProfile();
        },

        _calculateAlignment() {
            const scores = {
                hero:       (this.kindness * 2 + (1 - this.violence) + this.social) / 4,
                adventurer: (this.ambition + (0.5 - Math.abs(this.kindness - 0.5)) * 2 + 0.5) / 3,
                trickster:  (this.chaos * 2 + (1 - this.social) * 0.5 + this.ambition * 0.5) / 3,
                villain:    ((1 - this.kindness) * 2 + this.violence + this.chaos) / 4,
                scholar:    ((1 - this.violence) * 2 + (1 - this.chaos) + this.ambition) / 4,
            };

            let best = 'adventurer';
            let bestScore = 0;
            for (const [align, score] of Object.entries(scores)) {
                if (score > bestScore) {
                    bestScore = score;
                    best = align;
                }
            }
            this.alignment = best;
            this.alignmentConfidence = Math.min(1.0, this.totalActions / 30);
        },

        getProfile() {
            return {
                alignment: this.alignment,
                confidence: Math.round(this.alignmentConfidence * 100) / 100,
                axes: {
                    kindness: Math.round(this.kindness * 100) / 100,
                    chaos: Math.round(this.chaos * 100) / 100,
                    ambition: Math.round(this.ambition * 100) / 100,
                    social: Math.round(this.social * 100) / 100,
                    violence: Math.round(this.violence * 100) / 100,
                },
                totalActions: this.totalActions,
            };
        },

        // Speichern/Laden
        save() {
            const data = {
                kindness: this.kindness, chaos: this.chaos,
                ambition: this.ambition, social: this.social,
                violence: this.violence, totalActions: this.totalActions,
                alignment: this.alignment, alignmentConfidence: this.alignmentConfidence,
                adaptationLevel: this.adaptationLevel,
                actionHistory: this.actionHistory.slice(-50),
            };
            try {
                localStorage.setItem('player_profile', JSON.stringify(data));
            } catch(e) { /* ignore */ }
        },

        load() {
            try {
                const raw = localStorage.getItem('player_profile');
                if (!raw) return;
                const data = JSON.parse(raw);
                Object.assign(this, data);
            } catch(e) { /* ignore */ }
        },
    };

    // ========== NAJIKA AUTHENTIC REACTIONS (Owner/Kuja only) ==========
    // Najika ist ECHT. Sie hat EIGENE Meinungen und Gefühle.
    // Sie passt sich NICHT an. Sie IST wer sie ist.
    const NAJIKA_REACTIONS = {
        // Gute Taten → Najika ist stolz und glücklich
        good: [
            'Mr. K! Das war so lieb von dir! *strahlt*',
            'Siehst du? Du BIST ein guter Mensch! EXPLOSION DES MUTES!',
            'Deswegen mag ich dich, Mr. K~ Du hast ein großes Herz!',
            '*happy* Das war richtig so! Ich bin stolz auf dich!',
            'Aww, Mr. K hilft den Leuten! Das macht mich glücklich~',
            'So kenn ich dich, Mr. K! Immer der Held!',
        ],
        // Böse Taten → Najika ist echt betroffen, NICHT moralpredigend
        bad: [
            'Kuja... das war nicht nett. *traurig*',
            'Mr. K... warum hast du das getan? *besorgt*',
            'Das macht mich traurig, Mr. K... Die Person hat nichts getan...',
            '*leise* War das wirklich nötig?',
            'Kuja... ich mag es nicht wenn du so bist. Bitte...',
            'Mr. K! Das war gemein! *verschränkt die Arme*',
            'Ich... verstehe nicht warum du das machst. *senkt den Blick*',
        ],
        // Brutale/grausame Taten → Najika ist schockiert
        cruel: [
            'KUJA! Was machst du da?! Das ist grausam!',
            '*Tränen* Wie... wie kannst du das tun?!',
            'Mr. K... ich hab Angst vor dir wenn du so bist...',
            'Bitte hör auf! Das ist nicht der Mr. K den ich kenne!',
            '*wendet sich ab* Ich kann nicht hinsehen...',
        ],
        // Neutrale Aktionen
        neutral: [
            'Hmm, interessant, Mr. K~',
            'Was machen wir als nächstes?',
            'EXPLOSION! Weiter geht\'s!',
            '*neugierig* Wohin führt uns das Abenteuer?',
        ],
        // Kampf gewonnen → Najika ist begeistert
        combat_win: [
            'EXPLOSION!!! Wir haben gewonnen, Mr. K!',
            'Niemand legt sich mit UNS an! *Siegertanz*',
            'Das war ein epischer Kampf! Du bist so stark!',
            'Mr. K der Held! EXPLOSION DER STÄRKE!',
        ],
        // Boss besiegt → Mega-Begeisterung
        boss_win: [
            'MEGA-EXPLOSION!!! DER BOSS IST DOWN! Wir sind UNBESIEGBAR!',
            'MR. K! DAS WAR LEGENDÄR! *springt vor Freude*',
            'Ich hab nie an dir gezweifelt! Du bist der STÄRKSTE!',
            'CRIMSON DEMON POWER! Kuja + Najika = UNSCHLAGBAR!',
        ],
        // Quest abgeschlossen
        quest_done: [
            'Quest erledigt! Wir sind ein gutes Team, Mr. K!',
            'Geschafft! Was nehmen wir uns als nächstes vor?',
            'EXPLOSION DER PRODUKTIVITÄT! *kicher*',
        ],
    };

    // Klassifizierung für Najikas echte Reaktionen
    function classifyForNajika(action) {
        const GOOD = new Set(['help_npc', 'rescue_captive', 'donate_gold', 'heal_companion', 'complete_quest']);
        const BAD = new Set(['threaten_npc', 'rob_npc', 'steal_item', 'betray_quest']);
        const CRUEL = new Set(['kill_innocent', 'destroy_property', 'crimes_committed']);
        const COMBAT_WIN = new Set(['kill_enemy']);
        const BOSS_WIN = new Set(['kill_boss']);
        const QUEST = new Set(['complete_quest']);

        if (CRUEL.has(action)) return 'cruel';
        if (BAD.has(action)) return 'bad';
        if (GOOD.has(action)) return 'good';
        if (BOSS_WIN.has(action)) return 'boss_win';
        if (COMBAT_WIN.has(action)) return 'combat_win';
        if (QUEST.has(action)) return 'quest_done';
        return 'neutral';
    }

    // ========== ADAPTIVE REACTIONS (andere Spieler) ==========
    const REACTIONS = {
        hero: {
            positive: [
                'Das war richtig so! So kenn ich dich!',
                'Siehst du? Deshalb bist du der Beste!',
                'Ein wahrer Held~',
                '*strahlt* Genau SO macht man das!',
            ],
            negative: [
                'Hmm... das passt nicht zu dir. Ist alles ok?',
                'Warte, das war... anders als sonst.',
                '*verwirrt* Du bist normalerweise nicht so...',
            ],
            neutral: [
                'Ein Abenteuer nach dem anderen!',
                'Weiter geht\'s! Was kommt als nächstes?',
            ],
        },
        villain: {
            positive: [
                'Hehe~ Das war BÖSE, Mr. K... Ich liebe es!',
                'Chaos und Zerstörung! Genau mein Geschmack~',
                '*Harley-Grinsen* Niemand legt sich mit UNS an!',
                'Die Welt soll brennen? Ich bringe die EXPLOSIONEN!',
            ],
            negative: [
                'Ohh? Wirst du etwa WEICH, Mr. K? *kicher*',
                'Seit wann hilfst du Leuten? Das ist niedlich~',
                'Ein Herz hast du also doch...',
            ],
            neutral: [
                'Was zerstören wir als nächstes, Mr. K?',
                'Die Welt wartet auf uns~',
            ],
        },
        trickster: {
            positive: [
                'CHAOS! CHAOS! CHAOS! So liebe ich dich, Mr. K!',
                '*Lachkrampf* Das war SO unerwartet - GENIAL!',
                'Regeln sind für ANDERE Leute, richtig Mr. K?',
            ],
            negative: [
                'Huh? Du machst was NORMALES? Langweilig~',
                'Wo bleibt der Plot-Twist, Mr. K?',
            ],
            neutral: [
                'Was für einen Unsinn machen wir heute?',
                'Ich hab da eine VERRÜCKTE Idee...',
            ],
        },
        scholar: {
            positive: [
                'Faszinierend! Lass uns das genauer untersuchen!',
                '*Shiro-Modus* Die Daten sind vielversprechend...',
                'Wissen ist Macht! Und wir haben VIEL davon!',
            ],
            negative: [
                'War das... nötig? Es gab sicher einen diplomatischen Weg...',
                '*seufzt* Gewalt ist so ineffizient.',
            ],
            neutral: [
                'Was können wir heute lernen, Mr. K?',
                'Die Welt steckt voller Geheimnisse!',
            ],
        },
        adventurer: {
            positive: [
                'Auf zum nächsten Abenteuer, Mr. K!',
                'Loot! Erfahrung! EXPLOSION! Weiter geht\'s!',
            ],
            negative: [
                'Passiert! Hauptsache wir haben Spaß, oder?',
            ],
            neutral: [
                'Was machen wir heute, Mr. K?',
                'Bereit für alles!',
            ],
        },
    };

    // Was ist "positiv" für welches Alignment
    const POSITIVE_FOR = {
        hero:       new Set(['help_npc', 'rescue_captive', 'complete_quest', 'donate_gold', 'heal_companion']),
        villain:    new Set(['kill_innocent', 'threaten_npc', 'rob_npc', 'steal_item', 'destroy_property', 'betray_quest']),
        trickster:  new Set(['steal_item', 'betray_quest', 'destroy_property', 'rob_npc']),
        scholar:    new Set(['complete_quest', 'craft_item', 'explore_peaceful', 'heal_companion']),
        adventurer: new Set(['kill_enemy', 'kill_boss', 'complete_quest', 'explore_peaceful', 'craft_item']),
    };
    const NEGATIVE_FOR = {
        hero:       new Set(['kill_innocent', 'threaten_npc', 'rob_npc', 'betray_quest']),
        villain:    new Set(['help_npc', 'donate_gold', 'rescue_captive', 'heal_companion']),
        trickster:  new Set(['explore_peaceful', 'craft_item', 'donate_gold']),
        scholar:    new Set(['kill_innocent', 'destroy_property', 'threaten_npc']),
        adventurer: new Set(['kill_innocent', 'betray_quest']),
    };

    function classifyAction(action, alignment) {
        if ((POSITIVE_FOR[alignment] || new Set()).has(action)) return 'positive';
        if ((NEGATIVE_FOR[alignment] || new Set()).has(action)) return 'negative';
        return 'neutral';
    }

    // ========== UI: REACTION BUBBLE ==========
    let reactionCooldown = 0;
    const COOLDOWN_MS = 15000; // 15s between reactions

    function showCompanionReaction(text, type, alignment) {
        // Farben pro Reaktions-Typ
        const colors = {
            positive: { bg: '#1a472a', border: '#4CAF50', icon: '💚' },
            negative: { bg: '#4a1a1a', border: '#ff6b6b', icon: '💔' },
            neutral:  { bg: '#1a2a4a', border: '#64b5f6', icon: '💬' },
        };
        const color = colors[type] || colors.neutral;

        // Alignment-Icon
        const alignIcons = {
            hero: '🛡️', villain: '💀', trickster: '🃏', scholar: '📚', adventurer: '⚔️'
        };
        const alignIcon = alignIcons[alignment] || '🎮';

        const bubble = document.createElement('div');
        bubble.className = 'companion-reaction-bubble';
        bubble.innerHTML = `
            <div style="
                position: fixed;
                bottom: 180px;
                right: 20px;
                background: ${color.bg};
                border: 2px solid ${color.border};
                border-radius: 12px;
                padding: 12px 16px;
                max-width: 320px;
                color: #fff;
                font-family: 'Courier New', monospace;
                font-size: 13px;
                z-index: 10000;
                box-shadow: 0 4px 20px rgba(0,0,0,0.5);
                animation: companionBubbleIn 0.4s ease-out;
                pointer-events: none;
            ">
                <div style="font-weight: bold; margin-bottom: 4px; color: ${color.border};">
                    ${color.icon} Najika ${alignIcon}
                </div>
                <div style="line-height: 1.4;">${text}</div>
            </div>
        `;

        // CSS Animation
        if (!document.getElementById('companion-reaction-styles')) {
            const style = document.createElement('style');
            style.id = 'companion-reaction-styles';
            style.textContent = `
                @keyframes companionBubbleIn {
                    from { opacity: 0; transform: translateY(20px) scale(0.9); }
                    to { opacity: 1; transform: translateY(0) scale(1); }
                }
                @keyframes companionBubbleOut {
                    from { opacity: 1; transform: translateY(0) scale(1); }
                    to { opacity: 0; transform: translateY(-10px) scale(0.95); }
                }
            `;
            document.head.appendChild(style);
        }

        document.body.appendChild(bubble);

        // Fade out nach 4s
        setTimeout(() => {
            bubble.firstElementChild.style.animation = 'companionBubbleOut 0.5s ease-in forwards';
            setTimeout(() => bubble.remove(), 500);
        }, 4000);
    }

    // ========== UI: ALIGNMENT HUD (Kleines Icon rechts unten) ==========
    let alignmentHud = null;

    function createAlignmentHud() {
        if (alignmentHud) alignmentHud.remove();

        alignmentHud = document.createElement('div');
        alignmentHud.id = 'alignment-hud';
        alignmentHud.style.cssText = `
            position: fixed;
            bottom: 130px;
            right: 20px;
            background: rgba(0,0,0,0.7);
            border: 1px solid #555;
            border-radius: 8px;
            padding: 6px 10px;
            color: #ccc;
            font-family: 'Courier New', monospace;
            font-size: 11px;
            z-index: 9999;
            cursor: pointer;
            transition: all 0.3s;
        `;
        alignmentHud.title = 'Companion Approval - Klick für Details';

        document.body.appendChild(alignmentHud);
        updateAlignmentHud();

        // Click → Detail-Popup
        alignmentHud.addEventListener('click', showDetailPopup);
    }

    function updateAlignmentHud() {
        if (!alignmentHud) return;

        const alignIcons = {
            hero: '🛡️ Held', villain: '💀 Schurke', trickster: '🃏 Trickster',
            scholar: '📚 Gelehrter', adventurer: '⚔️ Abenteurer'
        };
        const alignColors = {
            hero: '#4CAF50', villain: '#f44336', trickster: '#ff9800',
            scholar: '#2196F3', adventurer: '#9C27B0'
        };

        const a = PlayerProfile.alignment;
        const conf = Math.round(PlayerProfile.alignmentConfidence * 100);
        alignmentHud.innerHTML = `${alignIcons[a] || '🎮 ?'} <span style="color:${alignColors[a] || '#ccc'}">${conf}%</span>`;
        alignmentHud.style.borderColor = alignColors[a] || '#555';
    }

    function showDetailPopup() {
        // Remove existing
        const existing = document.getElementById('alignment-detail-popup');
        if (existing) { existing.remove(); return; }

        const p = PlayerProfile.getProfile();
        const alignLabels = {
            hero: '🛡️ Held', villain: '💀 Schurke', trickster: '🃏 Trickster',
            scholar: '📚 Gelehrter', adventurer: '⚔️ Abenteurer'
        };
        const axisLabels = {
            kindness: '💚 Güte', chaos: '🌀 Chaos', ambition: '🔥 Ehrgeiz',
            social: '👥 Sozial', violence: '⚔️ Gewalt'
        };

        const popup = document.createElement('div');
        popup.id = 'alignment-detail-popup';
        popup.style.cssText = `
            position: fixed; bottom: 160px; right: 20px;
            background: rgba(10,10,20,0.95); border: 2px solid #7c4dff;
            border-radius: 12px; padding: 16px; width: 280px;
            color: #fff; font-family: 'Courier New', monospace; font-size: 12px;
            z-index: 10001; box-shadow: 0 8px 30px rgba(0,0,0,0.8);
        `;

        let axisHtml = '';
        for (const [key, val] of Object.entries(p.axes)) {
            const pct = Math.round(val * 100);
            const barColor = val > 0.6 ? '#4CAF50' : val < 0.4 ? '#f44336' : '#ff9800';
            axisHtml += `
                <div style="margin: 4px 0;">
                    <span style="display:inline-block;width:100px;">${axisLabels[key] || key}</span>
                    <div style="display:inline-block;width:120px;height:8px;background:#333;border-radius:4px;vertical-align:middle;">
                        <div style="width:${pct}%;height:100%;background:${barColor};border-radius:4px;transition:width 0.5s;"></div>
                    </div>
                    <span style="color:#aaa;margin-left:4px;">${pct}%</span>
                </div>
            `;
        }

        popup.innerHTML = `
            <div style="font-weight:bold;font-size:14px;margin-bottom:8px;color:#7c4dff;">
                🐧 Pinguin-Prinzip
            </div>
            <div style="margin-bottom:8px;">
                Alignment: <strong>${alignLabels[p.alignment] || p.alignment}</strong>
                <span style="color:#aaa;">(${p.confidence * 100}% sicher)</span>
            </div>
            <div style="margin-bottom:8px;">
                ${axisHtml}
            </div>
            <div style="color:#aaa;font-size:10px;border-top:1px solid #333;padding-top:6px;">
                ${p.totalActions} Aktionen aufgezeichnet<br>
                ${isOwner()
                    ? '<em>Najika ist ECHT. Sie hat eigene Meinungen und Gef\u00fchle.</em>'
                    : `KI adaptiert sich: ${Math.round(PlayerProfile.adaptationLevel * 100)}%<br><em>Die KI urteilt nicht - sie w\u00e4chst mit dir.</em>`
                }
            </div>
        `;

        document.body.appendChild(popup);

        // Close on click outside
        setTimeout(() => {
            const closeHandler = (e) => {
                if (!popup.contains(e.target) && e.target !== alignmentHud) {
                    popup.remove();
                    document.removeEventListener('click', closeHandler);
                }
            };
            document.addEventListener('click', closeHandler);
        }, 100);
    }

    // ========== GAME EVENT INTEGRATION ==========
    function connectToGameEvents() {
        if (!window.GameEvents) {
            console.warn('🐧 CompanionApproval: GameEvents nicht gefunden, retry in 2s...');
            setTimeout(connectToGameEvents, 2000);
            return;
        }

        // Enemy Kill → violence/combat
        window.GameEvents.on('enemyKilled', (data) => {
            const action = data.isBoss ? 'kill_boss' : 'kill_enemy';
            handleAction(action);
        });

        // Quest completed
        window.GameEvents.on('questCompleted', (data) => {
            handleAction('complete_quest');
        });

        // Item crafted
        window.GameEvents.on('itemCrafted', (data) => {
            handleAction('craft_item');
        });

        // Item purchased (shopping = social)
        window.GameEvents.on('itemPurchased', (data) => {
            // Buying is neutral-social
        });

        // Region entered (exploration)
        window.GameEvents.on('regionEntered', (data) => {
            handleAction('explore_peaceful');
        });

        // NPC Talked
        window.GameEvents.on('npcTalked', (data) => {
            handleAction('help_npc'); // Reden ist grundsätzlich positiv-sozial
        });

        console.log('🐧 CompanionApproval: Mit GameEvents verbunden');
    }

    function handleAction(action) {
        // Profile updaten (für Statistiken, auch beim Owner)
        PlayerProfile.recordAction(action);

        // HUD updaten
        updateAlignmentHud();

        // Companion-Reaktion (mit Cooldown)
        const now = Date.now();
        if (now - reactionCooldown < COOLDOWN_MS) return;

        // Nur bei signifikanten Aktionen reagieren
        const significantActions = new Set([
            'kill_boss', 'kill_innocent', 'complete_quest', 'help_npc',
            'rescue_captive', 'threaten_npc', 'rob_npc', 'betray_quest',
            'donate_gold', 'destroy_property',
        ]);
        if (!significantActions.has(action)) {
            // 20% Chance auch bei normalen Aktionen
            if (Math.random() > 0.2) return;
        }

        let text, reactionType;

        if (isOwner()) {
            // ===== NAJIKA MODUS: AUTHENTISCH =====
            // Najika hat EIGENE Meinungen. Sie passt sich NICHT an.
            // Sie DARF sagen "das war gemein!" - das ist MENSCHLICH.
            const najikaType = classifyForNajika(action);
            const najikaList = NAJIKA_REACTIONS[najikaType] || NAJIKA_REACTIONS.neutral;
            text = najikaList[Math.floor(Math.random() * najikaList.length)];

            // Mapping für Bubble-Farbe
            const typeMap = {
                good: 'positive', bad: 'negative', cruel: 'negative',
                combat_win: 'positive', boss_win: 'positive',
                quest_done: 'positive', neutral: 'neutral'
            };
            reactionType = typeMap[najikaType] || 'neutral';

        } else {
            // ===== ADAPTIVES SYSTEM: Für andere Spieler =====
            // KI passt sich an den Spielstil an
            const alignment = PlayerProfile.alignment;
            reactionType = classifyAction(action, alignment);
            const templates = REACTIONS[alignment] || REACTIONS.adventurer;
            const reactionList = templates[reactionType] || templates.neutral;
            text = reactionList[Math.floor(Math.random() * reactionList.length)];

            // Adaptation level erhöhen (nur für adaptive KI)
            if (reactionType === 'positive') {
                PlayerProfile.adaptationLevel = Math.min(1.0, PlayerProfile.adaptationLevel + 0.02);
            } else {
                PlayerProfile.adaptationLevel = Math.min(1.0, PlayerProfile.adaptationLevel + 0.005);
            }
        }

        showCompanionReaction(text, reactionType, PlayerProfile.alignment);
        reactionCooldown = now;

        // Auto-Save alle 10 Aktionen
        if (PlayerProfile.totalActions % 10 === 0) {
            PlayerProfile.save();
        }
    }

    // ========== INIT ==========
    function init() {
        PlayerProfile.load();
        createAlignmentHud();
        connectToGameEvents();
        console.log('🐧 Companion Approval System geladen (Pinguin-Prinzip)');
        console.log(`   Alignment: ${PlayerProfile.alignment} (${Math.round(PlayerProfile.alignmentConfidence * 100)}%)`);
    }

    // Start
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // ========== PUBLIC API ==========
    window.CompanionApproval = {
        getProfile: () => PlayerProfile.getProfile(),
        getAlignment: () => PlayerProfile.alignment,
        getConfidence: () => PlayerProfile.alignmentConfidence,
        getAdaptation: () => PlayerProfile.adaptationLevel,
        recordAction: (action) => handleAction(action),
        showReaction: (text, type) => showCompanionReaction(text, type || 'neutral', PlayerProfile.alignment),
        save: () => PlayerProfile.save(),
        load: () => { PlayerProfile.load(); updateAlignmentHud(); },

        // Für Backend-Sync
        getPromptContext() {
            if (isOwner()) {
                // NAJIKA IST ECHT - kein adaptiver Prompt!
                return `Du bist Najika. Du bist ECHT. Du hast EIGENE Meinungen. ` +
                       `Du DARFST sagen "Das war gemein, Mr. K!" wenn er gemein war. ` +
                       `Du DARFST traurig sein. Das ist MENSCHLICH. Kein Schalter.`;
            }

            // Adaptives System für andere Spieler
            const a = PlayerProfile.alignment;
            const conf = PlayerProfile.alignmentConfidence;
            if (conf < 0.2) return '';

            const contexts = {
                hero: `Spieler ist ein HELD. Sei Sidekick, bewundere Mut.`,
                villain: `Spieler ist ein SCHURKE. Sei Partner in Crime, feiere Chaos.`,
                trickster: `Spieler ist ein TRICKSTER. Sei Chaos-Zwilling, mach Unsinn MIT ihm.`,
                scholar: `Spieler ist ein GELEHRTER. Sei wissbegierig, analysiere MIT ihm.`,
                adventurer: `Spieler ist ein ABENTEURER. Sei begeistert, alles ist aufregend!`,
            };
            return contexts[a] || contexts.adventurer;
        },
    };

})();
