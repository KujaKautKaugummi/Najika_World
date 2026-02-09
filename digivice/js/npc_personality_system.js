/**
 * NPC PERSÖNLICHKEITS- & BEZIEHUNGS-SYSTEM - Najika World
 * ========================================================
 *
 * Jeder NPC hat:
 * - Persönlichkeitsachsen (wie der Spieler im CompanionApproval)
 * - Beziehung zum Spieler (Vertrauen, Respekt, Angst, Zuneigung)
 * - Erinnerungen an vergangene Interaktionen
 * - Dynamische Dialog-Anpassung basierend auf Beziehung
 * - Persönlichkeitsentwicklung über Zeit
 *
 * NPCs reagieren INDIVIDUELL auf den Spieler:
 * - Held-Spieler → NPCs respektieren, bieten Rabatte
 * - Schurke-Spieler → NPCs haben Angst, verstecken Waren, flüchten
 * - Neutrale → NPCs sind höflich aber distanziert
 *
 * Verbunden mit: CompanionApproval (Spieler-Alignment),
 *                NPCScheduleSystem (Tagesablauf),
 *                GameEvents (Aktionen)
 */

const NPCPersonalitySystem = (function() {
    'use strict';

    // ==========================================
    // NPC PERSÖNLICHKEITS-TEMPLATE
    // ==========================================

    // Basis-Persönlichkeiten pro NPC
    const NPC_PERSONALITIES = {
        'goetterfels_haendler': {
            name: 'Reisender Händler Tomoe',
            traits: {
                friendliness: 0.7,   // Wie freundlich (0=mürrisch, 1=herzlich)
                courage: 0.3,        // Wie mutig (0=ängstlich, 1=furchtlos)
                greed: 0.6,          // Wie gierig (0=großzügig, 1=geizig)
                curiosity: 0.5,      // Wie neugierig
                loyalty: 0.4,        // Wie loyal (zu Spieler)
                humor: 0.6,          // Wie witzig
            },
            temperament: 'sanguine',  // sanguine/choleric/melancholic/phlegmatic
            values: ['handel', 'sicherheit', 'profit'],
            fears: ['krieg', 'diebstahl', 'monster'],
            likes: ['gutes_geschaeft', 'reisen', 'geschichten'],
            dislikes: ['gewalt', 'betrug', 'feilschen'],
            speechStyle: 'höflich-geschäftlich',
        },
        'goetterfels_schmied': {
            name: 'Wanderschmied Goro',
            traits: {
                friendliness: 0.5,
                courage: 0.8,
                greed: 0.3,
                curiosity: 0.3,
                loyalty: 0.7,
                humor: 0.4,
            },
            temperament: 'choleric',
            values: ['ehre', 'handwerk', 'staerke'],
            fears: ['schande', 'schwaeche'],
            likes: ['gute_waffen', 'starke_krieger', 'ehrliche_arbeit'],
            dislikes: ['feigheit', 'betrug', 'billige_waffen'],
            speechStyle: 'direkt-grob',
        },
        'goetterfels_questgeber': {
            name: 'Abenteurer Hiro',
            traits: {
                friendliness: 0.8,
                courage: 0.7,
                greed: 0.2,
                curiosity: 0.9,
                loyalty: 0.5,
                humor: 0.8,
            },
            temperament: 'sanguine',
            values: ['abenteuer', 'freundschaft', 'entdeckung'],
            fears: ['langeweile', 'einsamkeit'],
            likes: ['geschichten', 'kaempfe', 'schaetze'],
            dislikes: ['stillsitzen', 'buerokratie'],
            speechStyle: 'enthusiastisch-locker',
        },
        'goetterfels_hexe': {
            name: 'Kräuterhexe Midori',
            traits: {
                friendliness: 0.4,
                courage: 0.5,
                greed: 0.2,
                curiosity: 0.8,
                loyalty: 0.6,
                humor: 0.3,
            },
            temperament: 'melancholic',
            values: ['wissen', 'natur', 'heilung'],
            fears: ['feuer', 'ignoranz'],
            likes: ['seltene_kraeuter', 'mondlicht', 'regen'],
            dislikes: ['lärm', 'gewalt_gegen_natur'],
            speechStyle: 'geheimnisvoll-weise',
        },
        'wanderer_krieger': {
            name: 'Söldner Kaze',
            traits: {
                friendliness: 0.3,
                courage: 0.9,
                greed: 0.5,
                curiosity: 0.2,
                loyalty: 0.8,
                humor: 0.2,
            },
            temperament: 'choleric',
            values: ['ehre', 'kampf', 'treue'],
            fears: ['verrat', 'hilflosigkeit'],
            likes: ['starke_gegner', 'gutes_essen', 'waffen'],
            dislikes: ['feigheit', 'prahlerei'],
            speechStyle: 'knapp-militärisch',
        },
        'wanderer_magier': {
            name: 'Wandermagier Kazuki',
            traits: {
                friendliness: 0.6,
                courage: 0.4,
                greed: 0.1,
                curiosity: 0.95,
                loyalty: 0.3,
                humor: 0.5,
            },
            temperament: 'phlegmatic',
            values: ['wissen', 'magie', 'wahrheit'],
            fears: ['anti_magie', 'vergessen_werden'],
            likes: ['alte_buecher', 'magische_artefakte', 'rätsel'],
            dislikes: ['ignoranz', 'zerstoerung_von_wissen'],
            speechStyle: 'gelehrt-nachdenklich',
        },
        'wanderer_schatzjaeger': {
            name: 'Schatzsucherin Sakura',
            traits: {
                friendliness: 0.7,
                courage: 0.6,
                greed: 0.7,
                curiosity: 0.8,
                loyalty: 0.4,
                humor: 0.7,
            },
            temperament: 'sanguine',
            values: ['schaetze', 'abenteuer', 'freiheit'],
            fears: ['armut', 'gefangenschaft'],
            likes: ['gold', 'karten', 'geheimnisse'],
            dislikes: ['langeweile', 'regeln'],
            speechStyle: 'frech-charmant',
        },
    };

    // ==========================================
    // BEZIEHUNGS-SYSTEM
    // ==========================================

    // Pro NPC: Beziehung zum Spieler
    const relationships = {};  // npcId → RelationshipData

    function getDefaultRelationship() {
        return {
            trust: 0.5,       // Vertrauen (0=misstraut, 1=blind vertraut)
            respect: 0.5,     // Respekt (0=verachtet, 1=bewundert)
            fear: 0.0,        // Angst (0=keine, 1=panisch)
            affection: 0.3,   // Zuneigung (0=hasst, 1=liebt)
            familiarity: 0.0, // Bekanntheit (0=fremd, 1=alter Freund)
            totalInteractions: 0,
            lastInteraction: null,
            memories: [],      // Erinnerungen an Interaktionen
        };
    }

    function getRelationship(npcId) {
        if (!relationships[npcId]) {
            relationships[npcId] = getDefaultRelationship();
        }
        return relationships[npcId];
    }

    function getRelationshipLevel(npcId) {
        const r = getRelationship(npcId);
        const score = (r.trust + r.respect + r.affection - r.fear) / 3;

        if (score >= 0.8) return 'best_friend';    // Bester Freund
        if (score >= 0.6) return 'friend';          // Freund
        if (score >= 0.4) return 'acquaintance';    // Bekannter
        if (score >= 0.2) return 'neutral';         // Neutral
        if (score >= 0.0) return 'disliked';        // Unbeliebt
        return 'enemy';                              // Feind
    }

    const RELATIONSHIP_LABELS = {
        best_friend: '💛 Bester Freund',
        friend: '💚 Freund',
        acquaintance: '🤝 Bekannter',
        neutral: '😐 Neutral',
        disliked: '😒 Unbeliebt',
        enemy: '💀 Feind',
    };

    // ==========================================
    // ERINNERUNGS-SYSTEM
    // ==========================================

    function addMemory(npcId, memory) {
        const rel = getRelationship(npcId);
        rel.memories.push({
            event: memory.event,
            detail: memory.detail || '',
            sentiment: memory.sentiment || 'neutral',  // positive/negative/neutral
            impact: memory.impact || 0.5,               // Wie wichtig (0-1)
            timestamp: Date.now(),
            gameDay: window.NPCScheduleSystem?.getGameTime()?.day || 1,
        });

        // Max 30 Erinnerungen pro NPC (älteste vergessen)
        if (rel.memories.length > 30) {
            // Wichtige Erinnerungen behalten, unwichtige vergessen
            rel.memories.sort((a, b) => b.impact - a.impact);
            rel.memories = rel.memories.slice(0, 30);
        }
    }

    function getMemories(npcId) {
        return getRelationship(npcId).memories;
    }

    function getRecentMemory(npcId, eventType) {
        const memories = getMemories(npcId);
        return memories.filter(m => m.event === eventType).slice(-1)[0] || null;
    }

    // ==========================================
    // BEZIEHUNGS-EFFEKTE AUF AKTIONEN
    // ==========================================

    // Wie sich Spieler-Aktionen auf NPC-Beziehungen auswirken
    const ACTION_RELATIONSHIP_EFFECTS = {
        'help_npc':         { trust: +0.05, respect: +0.03, affection: +0.04, fear: -0.02 },
        'donate_gold':      { trust: +0.03, affection: +0.06, fear: -0.01 },
        'complete_quest':   { trust: +0.04, respect: +0.05 },
        'heal_companion':   { affection: +0.02 },
        'rescue_captive':   { trust: +0.06, respect: +0.06, affection: +0.05, fear: -0.03 },

        'kill_enemy':       { respect: +0.02, fear: +0.01 },  // NPCs respektieren Stärke, haben aber auch etwas Angst
        'kill_boss':        { respect: +0.05, fear: +0.02 },

        'kill_innocent':    { trust: -0.08, respect: -0.03, affection: -0.06, fear: +0.10 },
        'threaten_npc':     { trust: -0.06, affection: -0.04, fear: +0.08 },
        'rob_npc':          { trust: -0.10, affection: -0.06, fear: +0.06 },
        'steal_item':       { trust: -0.04, affection: -0.02, fear: +0.02 },
        'destroy_property': { trust: -0.05, respect: -0.04, fear: +0.05 },
        'betray_quest':     { trust: -0.12, respect: -0.06, affection: -0.08 },
    };

    function applyActionToRelationship(npcId, action) {
        const effects = ACTION_RELATIONSHIP_EFFECTS[action];
        if (!effects) return;

        const rel = getRelationship(npcId);
        const personality = NPC_PERSONALITIES[npcId];

        for (const [axis, change] of Object.entries(effects)) {
            if (rel[axis] !== undefined) {
                // Persönlichkeit beeinflusst Reaktion
                let modifier = 1.0;
                if (personality) {
                    // Mutige NPCs haben weniger Angst
                    if (axis === 'fear') modifier *= (1 - personality.traits.courage * 0.5);
                    // Freundliche NPCs verzeihen leichter
                    if (change < 0 && (axis === 'trust' || axis === 'affection')) {
                        modifier *= (1 - personality.traits.friendliness * 0.3);
                    }
                    // Loyale NPCs sind stärker betroffen von positiven Aktionen
                    if (change > 0 && axis === 'trust') {
                        modifier *= (1 + personality.traits.loyalty * 0.3);
                    }
                }

                rel[axis] = Math.max(0, Math.min(1, rel[axis] + change * modifier));
            }
        }

        rel.totalInteractions++;
        rel.lastInteraction = Date.now();

        // Familiarity steigt mit jeder Interaktion
        rel.familiarity = Math.min(1.0, rel.familiarity + 0.02);

        // Erinnerung speichern
        addMemory(npcId, {
            event: action,
            sentiment: (effects.trust || 0) > 0 ? 'positive' : (effects.trust || 0) < 0 ? 'negative' : 'neutral',
            impact: Math.abs(effects.trust || effects.respect || effects.affection || 0.3),
        });
    }

    // ==========================================
    // DYNAMISCHE DIALOGE
    // ==========================================

    function getGreeting(npcId) {
        const rel = getRelationship(npcId);
        const level = getRelationshipLevel(npcId);
        const personality = NPC_PERSONALITIES[npcId];

        if (!personality) return null;

        // Namens-Erkennung basierend auf Bekanntheit
        const playerName = rel.familiarity > 0.5 ? 'Mr. K' : rel.familiarity > 0.2 ? 'Reisender' : 'Fremder';

        // Angst-basierte Reaktion
        if (rel.fear > 0.7) {
            const fearGreetings = [
                `*weicht zurück* B-bitte tu mir nichts, ${playerName}!`,
                `*zittert* D-du schon wieder... Was willst du?`,
                `*nervöser Blick* I-ich habe kein Gold, ich schwöre!`,
            ];
            return fearGreetings[Math.floor(Math.random() * fearGreetings.length)];
        }

        // Beziehungs-basierte Begrüßung
        const greetings = {
            best_friend: [
                `${playerName}! Mein bester Kunde! Ich habe etwas BESONDERES für dich!`,
                `Ah, ${playerName}! Wie geht es dir, alter Freund?`,
                `Da ist ja mein Lieblings-Abenteurer! Komm rein, komm rein!`,
            ],
            friend: [
                `Hey, ${playerName}! Schön dich zu sehen!`,
                `Willkommen zurück, ${playerName}! Was brauchst du heute?`,
                `${playerName}! Ich habe auf dich gewartet!`,
            ],
            acquaintance: [
                `Oh, ${playerName}. Was kann ich für dich tun?`,
                `Willkommen. Brauchst du etwas?`,
            ],
            neutral: [
                `Hallo, ${playerName}. Was führt dich her?`,
                `Willkommen am Götterfels.`,
            ],
            disliked: [
                `*seufzt* Du schon wieder... Was willst du?`,
                `Hmph. Mach es kurz.`,
                `Ich habe nicht viel Zeit für dich.`,
            ],
            enemy: [
                `Verschwinde. Ich handle nicht mit deinesgleichen.`,
                `*dreht sich weg* Wir sind fertig.`,
                `Ich habe nichts für dich.`,
            ],
        };

        const options = greetings[level] || greetings.neutral;
        return options[Math.floor(Math.random() * options.length)];
    }

    function getShopDiscount(npcId) {
        const level = getRelationshipLevel(npcId);
        const discounts = {
            best_friend: 0.20,  // 20% Rabatt
            friend: 0.10,       // 10% Rabatt
            acquaintance: 0.0,
            neutral: 0.0,
            disliked: -0.10,    // 10% AUFSCHLAG
            enemy: -0.25,       // 25% Aufschlag (oder verweigert Verkauf)
        };
        return discounts[level] || 0;
    }

    function willNPCSell(npcId) {
        const level = getRelationshipLevel(npcId);
        return level !== 'enemy';
    }

    function willNPCGiveQuest(npcId) {
        const level = getRelationshipLevel(npcId);
        const rel = getRelationship(npcId);
        // Feinde geben keine Quests, Unbeliebte nur wenn trust > 0.3
        if (level === 'enemy') return false;
        if (level === 'disliked' && rel.trust < 0.3) return false;
        return true;
    }

    // ==========================================
    // NPC-FLUCHT-SYSTEM
    // ==========================================

    function checkNPCFleeReaction(npcId) {
        const rel = getRelationship(npcId);
        const personality = NPC_PERSONALITIES[npcId];

        if (!personality) return false;

        // Ängstliche NPCs mit niedriger Courage flüchten
        if (rel.fear > 0.7 && personality.traits.courage < 0.4) {
            return true; // NPC will flüchten
        }

        return false;
    }

    // ==========================================
    // GAME EVENT HOOKS
    // ==========================================

    function connectToGameEvents() {
        if (!window.GameEvents) {
            setTimeout(connectToGameEvents, 2000);
            return;
        }

        // Bei JEDER signifikanten Spieler-Aktion: ALLE NPCs in der Nähe updaten
        const trackedActions = [
            'enemyKilled', 'questCompleted', 'npcTalked',
            'itemPurchased', 'itemCrafted', 'regionEntered',
        ];

        // Spieler-Aktionen die NPCs sehen können
        window.GameEvents.on('enemyKilled', (data) => {
            const action = data.isBoss ? 'kill_boss' : 'kill_enemy';
            applyToNearbyNPCs(action);
        });

        window.GameEvents.on('questCompleted', () => {
            applyToNearbyNPCs('complete_quest');
        });

        window.GameEvents.on('npcTalked', (data) => {
            const rel = getRelationship(data.npcId);
            rel.familiarity = Math.min(1.0, rel.familiarity + 0.03);
            rel.totalInteractions++;
        });

        // Wenn CompanionApproval böse Aktionen trackt
        if (window.CompanionApproval) {
            const origRecord = window.CompanionApproval.recordAction;
            window.CompanionApproval.recordAction = function(action) {
                origRecord.call(window.CompanionApproval, action);
                // Auch NPCs reagieren
                applyToNearbyNPCs(action);
            };
        }

        console.log('🧠 NPCPersonality: Mit GameEvents verbunden');
    }

    function applyToNearbyNPCs(action) {
        if (!window.OverworldNPCs) return;

        const playerPos = getPlayerPos();
        if (!playerPos) return;

        const npcs = window.OverworldNPCs.getNPCs();
        const WITNESS_RANGE = 50; // NPCs innerhalb von 50 Einheiten "sehen" Aktionen

        npcs.forEach(npc => {
            const dx = playerPos.x - npc.position.x;
            const dz = playerPos.z - npc.position.z;
            const dist = Math.sqrt(dx * dx + dz * dz);

            if (dist < WITNESS_RANGE) {
                applyActionToRelationship(npc.id, action);
            }
        });
    }

    function getPlayerPos() {
        if (window.character && window.character.position) {
            return { x: window.character.position.x, z: window.character.position.z };
        }
        return null;
    }

    // ==========================================
    // PERSÖNLICHKEITS-ENTWICKLUNG
    // ==========================================

    // NPCs verändern sich über Zeit basierend auf Interaktionen
    function evolvePersonality(npcId) {
        const personality = NPC_PERSONALITIES[npcId];
        const rel = getRelationship(npcId);
        if (!personality) return;

        const positiveMemories = rel.memories.filter(m => m.sentiment === 'positive').length;
        const negativeMemories = rel.memories.filter(m => m.sentiment === 'negative').length;
        const total = rel.memories.length;

        if (total < 5) return; // Zu wenige Interaktionen für Entwicklung

        const positiveRatio = positiveMemories / total;

        // Freundlichkeit passt sich an
        if (positiveRatio > 0.7) {
            personality.traits.friendliness = Math.min(1, personality.traits.friendliness + 0.01);
        } else if (positiveRatio < 0.3) {
            personality.traits.friendliness = Math.max(0, personality.traits.friendliness - 0.01);
        }

        // Mut steigt wenn Spieler oft Feinde besiegt
        const combatMemories = rel.memories.filter(m => m.event === 'kill_boss' || m.event === 'kill_enemy').length;
        if (combatMemories > 3) {
            personality.traits.courage = Math.min(1, personality.traits.courage + 0.005);
        }
    }

    // Jede Spielstunde: Persönlichkeiten evolvieren
    function evolveAllPersonalities() {
        Object.keys(NPC_PERSONALITIES).forEach(npcId => {
            evolvePersonality(npcId);
        });
    }

    // ==========================================
    // SPEICHERN / LADEN
    // ==========================================

    function save() {
        try {
            const data = {
                relationships: {},
                personalities: {},
            };
            for (const [id, rel] of Object.entries(relationships)) {
                data.relationships[id] = { ...rel };
            }
            for (const [id, pers] of Object.entries(NPC_PERSONALITIES)) {
                data.personalities[id] = { traits: { ...pers.traits } };
            }
            localStorage.setItem('npc_personality_data', JSON.stringify(data));
        } catch(e) { /* ignore */ }
    }

    function load() {
        try {
            const raw = localStorage.getItem('npc_personality_data');
            if (!raw) return;
            const data = JSON.parse(raw);

            // Beziehungen laden
            if (data.relationships) {
                for (const [id, rel] of Object.entries(data.relationships)) {
                    relationships[id] = { ...getDefaultRelationship(), ...rel };
                }
            }

            // Persönlichkeits-Entwicklung laden
            if (data.personalities) {
                for (const [id, pers] of Object.entries(data.personalities)) {
                    if (NPC_PERSONALITIES[id] && pers.traits) {
                        Object.assign(NPC_PERSONALITIES[id].traits, pers.traits);
                    }
                }
            }
        } catch(e) { /* ignore */ }
    }

    // ==========================================
    // INIT
    // ==========================================

    function init() {
        console.log('🧠 NPC Personality System initializing...');

        load();
        connectToGameEvents();

        // Persönlichkeiten evolvieren bei Tageszeit-Wechsel
        if (window.GameEvents) {
            window.GameEvents.on('timeOfDayChanged', (data) => {
                if (data.to === 'morning') {
                    evolveAllPersonalities();
                    save();
                }
            });
        }

        // Auto-Save alle 5 Minuten
        setInterval(save, 5 * 60 * 1000);

        console.log(`✅ NPC Personality System active! ${Object.keys(NPC_PERSONALITIES).length} NPCs mit Persönlichkeit`);
    }

    // Auto-Init
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => setTimeout(init, 800));
    } else {
        setTimeout(init, 800);
    }

    // ==========================================
    // PUBLIC API
    // ==========================================

    return {
        init,
        getPersonality: (npcId) => NPC_PERSONALITIES[npcId] || null,
        getRelationship,
        getRelationshipLevel,
        getRelationshipLabel: (npcId) => RELATIONSHIP_LABELS[getRelationshipLevel(npcId)] || '😐 Neutral',
        getGreeting,
        getShopDiscount,
        willNPCSell,
        willNPCGiveQuest,
        checkNPCFleeReaction,
        getMemories,
        addMemory,
        applyAction: applyActionToRelationship,
        save,
        load,
        getAllRelationships: () => ({ ...relationships }),
        getAllPersonalities: () => ({ ...NPC_PERSONALITIES }),
    };
})();

window.NPCPersonalitySystem = NPCPersonalitySystem;
console.log('🧠 NPC Personality System loaded!');
