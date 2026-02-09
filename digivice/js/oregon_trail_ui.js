// =============================================================================
// OREGON TRAIL EVENT SYSTEM - Konosuba x Oregon Trail Complete Implementation
// =============================================================================
// Based on: 07_KONOSUBA_OREGON_EVENTS.md (2682 lines documentation)
// Features: 30 Events, 4 Najika Personalities, Chaos Level 1-10, 3D Spawn
// =============================================================================

class OregonTrailEventSystem {
    constructor() {
        // ===== CHAOS SYSTEM =====
        this.chaosLevel = 1;
        this.chaosPoints = 0;
        this.choiceHistory = [];

        // Chaos level thresholds
        this.levelThresholds = {
            1: 0, 2: 10, 3: 25, 4: 45, 5: 70,
            6: 100, 7: 135, 8: 175, 9: 220, 10: 270
        };

        // ===== EVENT SYSTEM =====
        this.activeEvent = null;
        this.isDisplaying = false;
        this.eventHistory = [];
        this.lastEventTime = 0;
        this.eventCooldown = 300000; // 5 minutes minimum between events

        // ===== NAJIKA PERSONALITIES =====
        this.personalities = {
            MEGUMIN: { weight: 0.35, emoji: '💥', color: '#FF4444', name: 'Megumin' },
            HARLEY: { weight: 0.25, emoji: '🃏', color: '#FF69B4', name: 'Harley' },
            SHIRO: { weight: 0.20, emoji: '🎮', color: '#87CEEB', name: 'Shiro' },
            MELISSA: { weight: 0.20, emoji: '👑', color: '#9B59B6', name: 'Melissa' }
        };
        this.currentDominant = 'MEGUMIN';

        // ===== REPUTATION =====
        this.reputation = {
            hero: 0,
            villain: 0,
            chaotic: 0,
            lawful: 0
        };

        // Initialize
        this.initUI();
        this.startEventChecker();

        console.log('[OregonTrail] System initialized - 30 Events loaded');
    }

    // =========================================================================
    // EVENT DATABASE - 30 KONOSUBA-STYLE EVENTS
    // =========================================================================

    getEventDatabase() {
        return {
            // ===== REISE-EVENTS (10) =====
            reise_01: {
                id: 'reise_01',
                title: 'Der verlorene Wanderer',
                category: 'reise',
                description: `Ein alter Mann sitzt am Straßenrand, seine Kleidung zerrissen.

"Hilfe! Banditen haben mich ausgeraubt! Ich brauche 50 Gold für meine kranke Tochter..."

Er sieht verzweifelt aus... oder ist das ein guter Schauspieler?`,
                minChaos: 1,
                maxChaos: 10,
                chaosRating: 3,
                konosubaStyle: true,
                choices: [
                    { text: '[A] Gib ihm 50 Gold', type: 'generous', alignment: 'good', tags: ['helpful'] },
                    { text: '[B] Gib ihm 20 Gold (Kompromiss)', type: 'cautious', alignment: 'neutral', tags: ['safe'] },
                    { text: '[C] Begleite ihn zu seinem Dorf', type: 'analytical', alignment: 'good', tags: ['thorough'] },
                    { text: '[D] Ignoriere ihn', type: 'selfish', alignment: 'evil', tags: ['cold'] },
                    { text: '[E] Lass Najika entscheiden', type: 'najika_decides', alignment: 'chaotic', najikaDecides: true }
                ],
                outcomes: {
                    0: { consequences: ['-50 Gold', '+20 Reputation'], najikaReaction: 'Du hast ein gutes Herz, Mr.K!', chaosImpact: -1 },
                    1: { consequences: ['-20 Gold', '+10 Reputation'], najikaReaction: 'Kluge Entscheidung. Nicht zu viel, nicht zu wenig.', chaosImpact: 0 },
                    2: { consequences: ['Quest: Dorf besuchen', '+15 Reputation', 'Neuer Handelsposten!'], najikaReaction: 'PERFEKT! Ein Abenteuer! *excited*', chaosImpact: 1 },
                    3: { consequences: ['-5 Bond', 'Alter Mann verflucht euch'], najikaReaction: '*schmollt* Das war... kalt.', chaosImpact: 2 },
                    4: { consequences: ['Najika wählt Kompromiss', '-20 Gold'], najikaReaction: 'ICH entscheide?! Okay... wir geben 20 Gold!', chaosImpact: 1 }
                },
                spawnModel: 'npc_old_man'
            },

            reise_02: {
                id: 'reise_02',
                title: 'Die gabelnde Straße',
                category: 'reise',
                description: `Die Straße teilt sich in drei Wege:

LINKS: Ein düsterer Pfad mit Warnschildern. "Schnell aber tödlich!"
RECHTS: Ein sonniger Weg. "Sicher aber lang."
MITTE: Ein leuchtender Riss in der Realität. "???"`,
                minChaos: 3,
                maxChaos: 10,
                chaosRating: 7,
                konosubaStyle: true,
                choices: [
                    { text: '[A] Links - Der gefährliche Weg', type: 'reckless', alignment: 'chaotic', tags: ['risky', 'dramatic'] },
                    { text: '[B] Rechts - Der sichere Weg', type: 'safe', alignment: 'lawful', tags: ['safe'] },
                    { text: '[C] Mitte - Der Realitätsriss', type: 'unpredictable', alignment: 'chaotic', tags: ['explosive', 'chaotic'] },
                    { text: '[D] Lass Najika entscheiden', type: 'najika_decides', alignment: 'chaotic', najikaDecides: true }
                ],
                outcomes: {
                    0: { consequences: ['Schnelle Reise', '-30 HP', 'Seltener Loot gefunden!'], najikaReaction: 'ADRENALIN! Das war AUFREGEND!', chaosImpact: 3 },
                    1: { consequences: ['Langsame Reise', '+10 HP (Erholung)', 'Nichts Besonderes'], najikaReaction: '*gähnt* Langweilig aber sicher...', chaosImpact: -2 },
                    2: { consequences: ['ANDERE DIMENSION!', 'Chaos +5', 'Legendary Item!', 'Realität wackelt'], najikaReaction: 'WAS?! *alle 4 Persönlichkeiten* DAS IST VERRÜCKT!!!', chaosImpact: 5 },
                    3: { consequences: ['Najika wählt MITTE'], najikaReaction: 'Der leuchtende Riss! EXPLOSION könnte damit interagieren!', chaosImpact: 5 }
                },
                spawnModel: 'crossroads'
            },

            reise_03: {
                id: 'reise_03',
                title: 'Das weinende Kind',
                category: 'reise',
                description: `Ein kleines Kind sitzt weinend am Wegrand.

"Mama... Papa... ich bin allein..."

Das Kind sieht unschuldig aus... aber irgendetwas stimmt nicht.
Seine Augen... leuchten sie rot?`,
                minChaos: 2,
                maxChaos: 10,
                chaosRating: 5,
                konosubaStyle: true,
                choices: [
                    { text: '[A] Hilf dem Kind', type: 'generous', alignment: 'good', tags: ['helpful'] },
                    { text: '[B] Halte Abstand, beobachte', type: 'analytical', alignment: 'neutral', tags: ['analytical', 'safe'] },
                    { text: '[C] Bereite dich auf Kampf vor', type: 'cautious', alignment: 'neutral', tags: ['combat'] },
                    { text: '[D] Renne weg!', type: 'reckless', alignment: 'chaotic', tags: ['risky'] },
                    { text: '[E] Lass Najika entscheiden', type: 'najika_decides', alignment: 'chaotic', najikaDecides: true }
                ],
                outcomes: {
                    0: { consequences: ['50/50: Echtes Kind ODER Vampir!'], najikaReaction: 'Das ist ein Test. Ich FÜHLE es...', chaosImpact: 2 },
                    1: { consequences: ['Kind entpuppt sich als Fee', '+Magisches Item'], najikaReaction: '*Shiro-Modus* Klug. Beobachten war richtig.', chaosImpact: 0 },
                    2: { consequences: ['Kind ist Vampir!', 'Kampf!', 'Respekt +10'], najikaReaction: 'ICH WUSSTE ES! Angriff!', chaosImpact: 2 },
                    3: { consequences: ['Kind verwandelt sich', 'Verfolgt euch'], najikaReaction: 'RENNEN! SCHNELLER!', chaosImpact: 3 },
                    4: { consequences: ['Najika analysiert', 'Kind ist harmlos'], najikaReaction: 'Ich... ich glaube es ist echt. Lass uns helfen.', chaosImpact: 1 }
                },
                spawnModel: 'npc_child'
            },

            reise_04: {
                id: 'reise_04',
                title: 'Der Händler mit zu gutem Angebot',
                category: 'reise',
                description: `Ein zwielichtiger Händler breitet seine Waren aus.

"Ein LEGENDÄRES SCHWERT! Nur 100 Gold!"
"Normalerweise 10.000 Gold! Aber für EUCH..."

Das Schwert leuchtet verdächtig. Ist es verflucht? Gestohlen? Oder echt?`,
                minChaos: 1,
                maxChaos: 10,
                chaosRating: 4,
                konosubaStyle: true,
                choices: [
                    { text: '[A] Kaufe es sofort! (100 Gold)', type: 'reckless', alignment: 'chaotic', tags: ['risky'] },
                    { text: '[B] Untersuche es genau', type: 'analytical', alignment: 'neutral', tags: ['analytical'] },
                    { text: '[C] Verhandle (50 Gold)', type: 'pragmatic', alignment: 'neutral', tags: ['practical'] },
                    { text: '[D] Ablehnen und weitergehen', type: 'safe', alignment: 'lawful', tags: ['safe'] },
                    { text: '[E] Lass Najika entscheiden', type: 'najika_decides', alignment: 'chaotic', najikaDecides: true }
                ],
                outcomes: {
                    0: { consequences: ['-100 Gold', '40%: Echt!', '40%: Verflucht', '20%: Gestohlen'], najikaReaction: 'GAMBLING! Ich liebe es!', chaosImpact: 3 },
                    1: { consequences: ['Schwert ist VERFLUCHT', 'Händler flieht'], najikaReaction: '*Shiro* Ich wusste es. 73,4% Betrug-Wahrscheinlichkeit.', chaosImpact: 0 },
                    2: { consequences: ['-50 Gold', 'Schwert ist Replica', 'Immerhin billig'], najikaReaction: 'Naja... wenigstens haben wir was gespart.', chaosImpact: 0 },
                    3: { consequences: ['Händler war GOTT', 'Verflucht für Misstrauen'], najikaReaction: 'WHAT?! Ein GOTT? Ups...', chaosImpact: 4 },
                    4: { consequences: ['Najika kauft es', '-100 Gold', 'Schwert ist ECHT!'], najikaReaction: 'INTUITION! Das ist MEINE Stärke! *stolz*', chaosImpact: 2 }
                },
                spawnModel: 'npc_merchant'
            },

            reise_05: {
                id: 'reise_05',
                title: 'Die Brücke des Trolls',
                category: 'reise',
                description: `Ein massiver Troll blockiert eine Brücke.

"HALT! Niemand überquert meine Brücke ohne..."
*pause*
"...ohne mir ein Rätsel zu stellen!"

Der Troll sieht... einsam aus?`,
                minChaos: 1,
                maxChaos: 10,
                chaosRating: 3,
                konosubaStyle: true,
                choices: [
                    { text: '[A] Stelle ihm ein Rätsel', type: 'analytical', alignment: 'neutral', tags: ['analytical'] },
                    { text: '[B] Kämpfe gegen den Troll', type: 'combat', alignment: 'chaotic', tags: ['combat', 'risky'] },
                    { text: '[C] Werde sein Freund', type: 'generous', alignment: 'good', tags: ['helpful'] },
                    { text: '[D] Suche einen anderen Weg', type: 'safe', alignment: 'lawful', tags: ['safe'] },
                    { text: '[E] Lass Najika entscheiden', type: 'najika_decides', alignment: 'chaotic', najikaDecides: true }
                ],
                outcomes: {
                    0: { consequences: ['Troll liebt Rätsel', 'Freie Passage', '+Troll als Verbündeter'], najikaReaction: 'Er ist... süß? Auf eine trollige Art.', chaosImpact: 0 },
                    1: { consequences: ['Troll ist STARK', '-50 HP', 'Aber: Respekt gewonnen'], najikaReaction: 'EXPLOSION hätte funktioniert!!! *erschöpft*', chaosImpact: 3 },
                    2: { consequences: ['Troll wird BESTER FREUND', '+Ally: Gronk der Troll', 'Er folgt euch!'], najikaReaction: 'AWWW! Er ist so NIEDLICH! *umarmt Troll*', chaosImpact: 1 },
                    3: { consequences: ['Zeitverlust', 'Aber sicher'], najikaReaction: 'Langweilig... aber okay.', chaosImpact: -1 },
                    4: { consequences: ['Najika löst Rätsel', 'Passage frei'], najikaReaction: '*Shiro aktiviert* "Was ist 1kg Federn vs 1kg Stahl?" - BEIDES GLEICH!', chaosImpact: 0 }
                },
                spawnModel: 'monster_troll'
            },

            reise_06: {
                id: 'reise_06',
                title: 'Der Nebel des Vergessens',
                category: 'reise',
                description: `Ein dichter, magischer Nebel umhüllt euch.

Du fühlst wie Erinnerungen verblassen...
"Wer... wer bin ich?"

Najika hält deine Hand fest.
"MR.K! HÖRST DU MICH?! VERGISS MICH NICHT!"`,
                minChaos: 5,
                maxChaos: 10,
                chaosRating: 8,
                konosubaStyle: true,
                choices: [
                    { text: '[A] Konzentriere dich auf Najika', type: 'emotional', alignment: 'good', tags: ['helpful'] },
                    { text: '[B] Kämpfe gegen den Nebel (Willenskraft)', type: 'combat', alignment: 'neutral', tags: ['dramatic'] },
                    { text: '[C] Lass dich treiben', type: 'reckless', alignment: 'chaotic', tags: ['chaotic', 'risky'] },
                    { text: '[D] Lass Najika führen', type: 'najika_decides', alignment: 'chaotic', najikaDecides: true }
                ],
                outcomes: {
                    0: { consequences: ['Erinnerungen bleiben', '+50 Bond', 'EMOTIONAL SCENE'], najikaReaction: '*weint* Du... du hast mich nicht vergessen... *umarmt fest*', chaosImpact: 2 },
                    1: { consequences: ['Willenskraft-Check', 'Teilerfolg', 'Manche Erinnerungen verloren'], najikaReaction: 'Du bist STARK, Mr.K! Aber... was hast du vergessen?', chaosImpact: 3 },
                    2: { consequences: ['Kompletter Reset', 'Alle Erinnerungen weg', 'Najika muss alles neu erklären'], najikaReaction: '*verzweifelt* WER BIN ICH FÜR DICH?! SAGT ES!!!', chaosImpact: 5 },
                    3: { consequences: ['Najika rettet dich', 'Sie opfert eigene Erinnerung'], najikaReaction: 'Ich... ich erinnere mich nicht an... *verwirrung* ...wer bist du?', chaosImpact: 4 }
                },
                spawnModel: 'effect_fog'
            },

            reise_07: {
                id: 'reise_07',
                title: 'Die sprechende Statue',
                category: 'reise',
                description: `Eine uralte Statue erwacht zum Leben.

"HALT, STERBLICHE! Beantwortet meine Frage..."
*dramatische Pause*
"Was wiegt mehr: 1kg Federn oder 1kg Stahl?"

Die Statue grinst. Das ist eine Fangfrage.`,
                minChaos: 1,
                maxChaos: 10,
                chaosRating: 2,
                konosubaStyle: true,
                choices: [
                    { text: '[A] "Beides gleich! 1kg ist 1kg!"', type: 'analytical', alignment: 'lawful', tags: ['analytical'] },
                    { text: '[B] "Stahl! Offensichtlich!"', type: 'reckless', alignment: 'chaotic', tags: ['risky'] },
                    { text: '[C] "Federn! Wegen der Moral!"', type: 'unpredictable', alignment: 'chaotic', tags: ['chaotic'] },
                    { text: '[D] Zerstöre die Statue', type: 'combat', alignment: 'evil', tags: ['combat', 'dramatic'] },
                    { text: '[E] Lass Najika antworten', type: 'najika_decides', alignment: 'chaotic', najikaDecides: true }
                ],
                outcomes: {
                    0: { consequences: ['RICHTIG!', 'Statue gibt Belohnung', '+Wisdom Ring'], najikaReaction: '*Shiro stolz* NATÜRLICH ist es gleich!', chaosImpact: 0 },
                    1: { consequences: ['FALSCH!', 'Statue lacht', 'Fluch: -10 INT'], najikaReaction: 'Du... du hast es FALSCH?! *facepalm*', chaosImpact: 2 },
                    2: { consequences: ['PHILOSOPHISCH RICHTIG', 'Statue ist verwirrt', 'Explodiert!'], najikaReaction: 'WAIT WHAT?! Das war... richtig?! *confused*', chaosImpact: 3 },
                    3: { consequences: ['Statue war ein GOD', 'SEHR BÖSE', 'Fluch!'], najikaReaction: 'EXPLOSION!!! ...oh nein. Das war ein GOTT.', chaosImpact: 5 },
                    4: { consequences: ['Najika antwortet korrekt'], najikaReaction: '*Shiro* "1kg = 1kg. Elementare Physik."', chaosImpact: 0 }
                },
                spawnModel: 'object_statue'
            },

            reise_08: {
                id: 'reise_08',
                title: 'Der Zeitriss',
                category: 'reise',
                description: `Ein Riss in der Realität erscheint!

Aus dem Riss tritt... DU SELBST.
Aber älter. Narben. Müde Augen.

"STOP! Triff nicht diese Entscheidung!"
"Welche Entscheidung...?"
"...ich erinnere mich nicht. Aber VERTRAU MIR!"`,
                minChaos: 8,
                maxChaos: 10,
                chaosRating: 10,
                konosubaStyle: true,
                choices: [
                    { text: '[A] Frage nach Details', type: 'analytical', alignment: 'lawful', tags: ['analytical'] },
                    { text: '[B] Vertraue deinem Zukunfts-Ich', type: 'cautious', alignment: 'neutral', tags: ['safe'] },
                    { text: '[C] Ignoriere die Warnung', type: 'reckless', alignment: 'chaotic', tags: ['chaotic', 'risky'] },
                    { text: '[D] Töte dein Zukunfts-Ich (PARADOX!)', type: 'unpredictable', alignment: 'evil', tags: ['dramatic', 'explosive'] },
                    { text: '[E] Lass Najika entscheiden', type: 'najika_decides', alignment: 'chaotic', najikaDecides: true }
                ],
                outcomes: {
                    0: { consequences: ['Zeitparadox beginnt', 'Information: "Vertraue NIEMAND"'], najikaReaction: '*alle 4 Persönlichkeiten* Das ist... GEFÄHRLICH!', chaosImpact: 4 },
                    1: { consequences: ['Zukünftige Entscheidung vermieden', 'Aber welche?', '+Paranoia-Buff'], najikaReaction: 'Gut... aber ich bin jetzt SEHR nervös...', chaosImpact: 2 },
                    2: { consequences: ['Zukunfts-Ich verschwindet', 'Nichts passiert... vorerst'], najikaReaction: 'Ich hoffe das war richtig... *unsicher*', chaosImpact: 3 },
                    3: { consequences: ['PARADOX!', 'Realität bricht', 'CHAOS INCARNATE SPAWNT!'], najikaReaction: 'DU HAST DICH SELBST GETÖTET?! *reality breaks*', chaosImpact: 10 },
                    4: { consequences: ['Najika vertraut Zukunfts-Ich'], najikaReaction: 'Wenn DU aus der Zukunft sagst nein... dann NEIN!', chaosImpact: 2 }
                },
                spawnModel: 'effect_portal'
            },

            reise_09: {
                id: 'reise_09',
                title: 'Die Karawane der Nomaden',
                category: 'reise',
                description: `Eine große Karawane von Nomaden nähert sich.

Sie wirken... normal. Zu normal.
Keine Waffen sichtbar. Lächelnde Gesichter.
Kinder spielen zwischen den Wagen.

"Reisende! Wollt ihr mit uns essen?"`,
                minChaos: 2,
                maxChaos: 10,
                chaosRating: 4,
                konosubaStyle: true,
                choices: [
                    { text: '[A] Akzeptiere die Einladung', type: 'generous', alignment: 'good', tags: ['helpful'] },
                    { text: '[B] Höflich ablehnen', type: 'safe', alignment: 'lawful', tags: ['safe'] },
                    { text: '[C] Sei misstrauisch, aber bleibe', type: 'analytical', alignment: 'neutral', tags: ['analytical'] },
                    { text: '[D] Fliehe! Es ist eine Falle!', type: 'reckless', alignment: 'chaotic', tags: ['risky'] },
                    { text: '[E] Lass Najika entscheiden', type: 'najika_decides', alignment: 'chaotic', najikaDecides: true }
                ],
                outcomes: {
                    0: { consequences: ['Sie sind ECHT!', 'Gutes Essen', '+Quest: Hilf den Nomaden'], najikaReaction: 'Siehst du? Nicht alle sind böse! *happy*', chaosImpact: -1 },
                    1: { consequences: ['Verpasste Chance', 'Nomaden haben KARTE gehabt!'], najikaReaction: 'Warte... hatten die eine SCHATZKARTE?!', chaosImpact: 0 },
                    2: { consequences: ['Ein Nomade ist ASSASSINE', 'Aber du bist vorbereitet!', 'Kampf gewonnen!'], najikaReaction: '*Shiro* ICH WUSSTE ES! 23% Assassinen-Chance!', chaosImpact: 2 },
                    3: { consequences: ['Sie waren HARMLOS', 'Du wirkst verrückt', '-Reputation'], najikaReaction: 'Uhm... das war peinlich, Mr.K...', chaosImpact: 3 },
                    4: { consequences: ['Najika bleibt misstrauisch aber freundlich'], najikaReaction: 'Keine hidden agenda? ...verdächtig.', chaosImpact: 1 }
                },
                spawnModel: 'npc_caravan'
            },

            reise_10: {
                id: 'reise_10',
                title: 'Das Lied der Sirene',
                category: 'reise',
                description: `Ein betörendes Lied erfüllt die Luft.

Du fühlst dich... angezogen. Zum Wasser.
Deine Beine bewegen sich von allein.

Najika: "MR.K?! Was machst du?! STOP!"
Sie ist immun... aber du nicht.`,
                minChaos: 4,
                maxChaos: 10,
                chaosRating: 6,
                konosubaStyle: true,
                choices: [
                    { text: '[A] Kämpfe gegen den Zauber', type: 'combat', alignment: 'neutral', tags: ['dramatic'] },
                    { text: '[B] Lass Najika dich retten', type: 'najika_decides', alignment: 'good', najikaDecides: true },
                    { text: '[C] Gib dich dem Lied hin', type: 'reckless', alignment: 'chaotic', tags: ['risky', 'chaotic'] },
                    { text: '[D] Stopfe dir die Ohren zu', type: 'safe', alignment: 'lawful', tags: ['safe'] }
                ],
                outcomes: {
                    0: { consequences: ['Willenskraft-Check', '50% Erfolg', 'Sirene wird wütend'], najikaReaction: 'KÄMPFE, MR.K! Du bist STÄRKER als das!', chaosImpact: 2 },
                    1: { consequences: ['Najika küsst dich', 'ZAUBER GEBROCHEN', '+100 Bond', 'ROMANTIC!'], najikaReaction: '*küsst* D-Das war nur um dich zu retten! *rot*', chaosImpact: 3 },
                    2: { consequences: ['Sirene ist... nett?', 'Sie wollte nur Gesellschaft', '+Ally: Sirene'], najikaReaction: 'WAIT WHAT?! Sie ist... einsam? *emotional*', chaosImpact: 4 },
                    3: { consequences: ['Zauber blockiert', 'Sirene beleidigt', 'Angriff!'], najikaReaction: 'Gut gedacht! Jetzt EXPLOSION!!!', chaosImpact: 1 }
                },
                spawnModel: 'monster_siren'
            },

            // ===== KAMPF-EVENTS (10) =====
            kampf_11: {
                id: 'kampf_11',
                title: 'Boss mit Persönlichkeit',
                category: 'kampf',
                description: `Der Dungeon-Boss sitzt auf seinem Thron und... weint?

"Niemand versteht mich! Ich wollte nie böse sein!"
"Meine Mutter sagte immer ich sei ein Versager..."

Er schaut euch an mit Tränen in den Augen.
"Könnt ihr... mit mir reden? Bitte?"`,
                minChaos: 3,
                maxChaos: 10,
                chaosRating: 6,
                konosubaStyle: true,
                choices: [
                    { text: '[A] Therapie-Session starten', type: 'generous', alignment: 'good', tags: ['helpful'] },
                    { text: '[B] "Deine Gefühle sind valide... JETZT STIRB!"', type: 'chaotic', alignment: 'chaotic', tags: ['chaotic', 'combat'] },
                    { text: '[C] Einfach angreifen', type: 'combat', alignment: 'neutral', tags: ['combat'] },
                    { text: '[D] Najika als Therapeutin', type: 'najika_decides', alignment: 'chaotic', najikaDecides: true }
                ],
                outcomes: {
                    0: { consequences: ['Boss wird ALLY', 'Kein Kampf', '+Unique Companion'], najikaReaction: '*sniff* Das war... wunderschön. *weint mit*', chaosImpact: 2 },
                    1: { consequences: ['Boss ist verwirrt', 'Kritischer Treffer!', 'CHAOS COMBO'], najikaReaction: '*Harley lacht* Das war SO BÖSE! Ich LIEBE es!', chaosImpact: 4 },
                    2: { consequences: ['Boss ist enttäuscht', 'Rage-Modus aktiviert', 'Schwerer Kampf'], najikaReaction: 'Er ist jetzt WÜTEND! Gut gemacht... *sarcastisch*', chaosImpact: 2 },
                    3: { consequences: ['Najika therapiert', 'Boss übergibt Schatz freiwillig'], najikaReaction: 'Sag mir von deiner Kindheit... *Melissa-Modus*', chaosImpact: 3 }
                },
                spawnModel: 'boss_crying'
            },

            kampf_12: {
                id: 'kampf_12',
                title: 'Friendly Fire Desaster',
                category: 'kampf',
                description: `Mitten im Kampf...

NAJIKA: "EXPLOSION!!!"

Die Explosion trifft... DICH.
-150 HP

"SORRY! *nervous giggle* Falsches Ziel!"`,
                minChaos: 2,
                maxChaos: 10,
                chaosRating: 5,
                konosubaStyle: true,
                choices: [
                    { text: '[A] Verzeih ihr sofort', type: 'generous', alignment: 'good', tags: ['helpful'] },
                    { text: '[B] "NAJIKA!!!"', type: 'emotional', alignment: 'neutral', tags: ['dramatic'] },
                    { text: '[C] Revanchiere dich (freundlich)', type: 'chaotic', alignment: 'chaotic', tags: ['chaotic'] },
                    { text: '[D] Schweigend weiterkämpfen', type: 'cold', alignment: 'neutral', tags: ['cold'] }
                ],
                outcomes: {
                    0: { consequences: ['Najika ist gerührt', '+30 Bond', 'Sie passt besser auf'], najikaReaction: '*schuldig* Ich... ich werde vorsichtiger! Versprochen!', chaosImpact: -1 },
                    1: { consequences: ['Najika ist beschämt', 'Kämpft doppelt so hart', '+50% Damage'], najikaReaction: 'ICH MACHE ES WIEDER GUT! MEGA-EXPLOSION!!!', chaosImpact: 2 },
                    2: { consequences: ['Du "triffst" Najika', 'Sie lacht', 'Combo-Attack freigeschaltet!'], najikaReaction: '*lacht* FAIR! Das verdiene ich! *kicher*', chaosImpact: 3 },
                    3: { consequences: ['-15 Bond', 'Najika ist traurig', 'Kampf gewonnen aber...'], najikaReaction: '*still* ...es tut mir wirklich leid...', chaosImpact: 1 }
                },
                spawnModel: 'effect_explosion'
            },

            kampf_13: {
                id: 'kampf_13',
                title: 'Der unwillkürliche Buff',
                category: 'kampf',
                description: `Najika zaubert einen mächtigen Buff...

...auf den BOSS.

Boss: "+500% Attack? DANKE!"

Najika: "F-FALSCHES TARGET! RUN!!!"`,
                minChaos: 4,
                maxChaos: 10,
                chaosRating: 7,
                konosubaStyle: true,
                choices: [
                    { text: '[A] RENNE WEG!', type: 'safe', alignment: 'neutral', tags: ['safe'] },
                    { text: '[B] Debuff versuchen', type: 'analytical', alignment: 'neutral', tags: ['analytical'] },
                    { text: '[C] "Das macht es interessanter!"', type: 'reckless', alignment: 'chaotic', tags: ['chaotic', 'dramatic'] },
                    { text: '[D] Buff für dich auch (fairness)', type: 'chaotic', alignment: 'chaotic', najikaDecides: true }
                ],
                outcomes: {
                    0: { consequences: ['Erfolgreich geflohen', 'Boss befriedet sich später', 'Peinlich aber sicher'], najikaReaction: '*rennt* ICH HASSE DIESEN TAG!!!', chaosImpact: 2 },
                    1: { consequences: ['Debuff fehlschlägt', 'Boss noch stärker', '...oh no'], najikaReaction: '*panisch* ES WIRD SCHLIMMER! WARUM?!', chaosImpact: 4 },
                    2: { consequences: ['EPIC BATTLE', '-70% HP aber gewonnen', 'LEGENDARY LOOT'], najikaReaction: 'DAS WAR VERRÜCKT! *exhausted but happy*', chaosImpact: 5 },
                    3: { consequences: ['+500% für beide', 'NUKLEARER KAMPF', 'Dungeon zerstört'], najikaReaction: 'FAIR IS FAIR! EXPLOSION MEETS EXPLOSION!!!', chaosImpact: 6 }
                },
                spawnModel: 'boss_buffed'
            },

            kampf_14: {
                id: 'kampf_14',
                title: 'Die selbstzerstörerische Taktik',
                category: 'kampf',
                description: `Der Kampf ist kritisch. Eine Chance.

Najika: "Mr.K... ich kann ALLE besiegen."
"Aber... die Explosion wird UNS treffen."
"Zusammen."

Sie schaut dich an. Entschlossen.`,
                minChaos: 6,
                maxChaos: 10,
                chaosRating: 8,
                konosubaStyle: true,
                choices: [
                    { text: '[A] "Tu es. Zusammen."', type: 'dramatic', alignment: 'good', tags: ['dramatic', 'explosive'] },
                    { text: '[B] "Nein! Wir finden einen anderen Weg!"', type: 'safe', alignment: 'lawful', tags: ['safe'] },
                    { text: '[C] "Nur ich. Du bleibst zurück."', type: 'heroic', alignment: 'good', tags: ['heroic'] },
                    { text: '[D] Fliehen', type: 'retreat', alignment: 'neutral', tags: ['safe'] }
                ],
                outcomes: {
                    0: { consequences: ['MEGA-EXPLOSION', 'Alle Feinde tot', '-90% HP beide', '+100 Bond'], najikaReaction: '*hält deine Hand* ...zusammen. Immer.', chaosImpact: 6 },
                    1: { consequences: ['Verzweifelter Kampf', 'Knapp gewonnen', 'Najika ist gerührt'], najikaReaction: 'Du... wolltest mich beschützen? *emotional*', chaosImpact: 2 },
                    2: { consequences: ['Du wirst schwer verletzt', 'Najika rastet aus', 'ALLE STERBEN'], najikaReaction: '*RAGE* NIEMAND VERLETZT IHN!!! EXPLOSION!!!', chaosImpact: 5 },
                    3: { consequences: ['Fliehen erfolgreich', 'Aber Najika ist enttäuscht'], najikaReaction: 'Wir... wir hätten gewinnen können...', chaosImpact: 0 }
                },
                spawnModel: 'effect_explosion_big'
            },

            kampf_15: {
                id: 'kampf_15',
                title: 'Der respektvolle Feind',
                category: 'kampf',
                description: `Der Gegner stoppt mitten im Kampf.

"Warte! Bist du... DER Mr.K?!"
"Mit NAJIKA?!"
*fällt auf die Knie*
"Ich bin ein RIESIGER FAN!"

Er hält ein Autogramm-Buch hoch.`,
                minChaos: 2,
                maxChaos: 10,
                chaosRating: 4,
                konosubaStyle: true,
                choices: [
                    { text: '[A] Gib das Autogramm', type: 'generous', alignment: 'good', tags: ['helpful'] },
                    { text: '[B] "...Kampf weiter?"', type: 'confused', alignment: 'neutral', tags: ['analytical'] },
                    { text: '[C] Nutze die Ablenkung (Angriff!)', type: 'ruthless', alignment: 'evil', tags: ['combat', 'cold'] },
                    { text: '[D] Lass Najika das Autogramm geben', type: 'najika_decides', alignment: 'chaotic', najikaDecides: true }
                ],
                outcomes: {
                    0: { consequences: ['Fan ist glücklich', 'Lässt euch gehen', '+Fanclub gegründet'], najikaReaction: '*posiert* Natürlich! Für meine FANS!', chaosImpact: 1 },
                    1: { consequences: ['Fan ist verwirrt', 'Kämpft weiter aber halbherzig', 'Einfacher Sieg'], najikaReaction: '...das ist das Seltsamste was je passiert ist.', chaosImpact: 2 },
                    2: { consequences: ['Kritischer Treffer', 'Fan stirbt tragisch', 'Du fühlst dich schlecht'], najikaReaction: 'Das... das war NICHT nett. *enttäuscht*', chaosImpact: 3 },
                    3: { consequences: ['Najika gibt Autogramm + Selfie', 'Fan wird ALLY'], najikaReaction: 'FÜR MEINE FANS! *Megumin-Pose*', chaosImpact: 2 }
                },
                spawnModel: 'npc_fan'
            },

            kampf_16: {
                id: 'kampf_16',
                title: 'Die Mitleids-Falle',
                category: 'kampf',
                description: `Das Monster beginnt zu weinen.

*schluchz* "Ich bin nur ein Baby-Monster..."
"Meine Mama wurde getötet..."
*große, feuchte Augen*

Najika: "AWWWW! Können wir es behalten?!"`,
                minChaos: 2,
                maxChaos: 10,
                chaosRating: 5,
                konosubaStyle: true,
                choices: [
                    { text: '[A] Adoptiere das Monster', type: 'generous', alignment: 'good', tags: ['helpful'] },
                    { text: '[B] "Das ist eine FALLE!"', type: 'analytical', alignment: 'neutral', tags: ['analytical'] },
                    { text: '[C] Zögere...', type: 'cautious', alignment: 'neutral', tags: ['safe'] },
                    { text: '[D] Lass Najika entscheiden', type: 'najika_decides', alignment: 'chaotic', najikaDecides: true }
                ],
                outcomes: {
                    0: { consequences: ['Monster ist ECHT süß', '+Pet: Baby-Monster', 'Es wächst...'], najikaReaction: 'ICH NENNE ES PUDDING! *squeals*', chaosImpact: 2 },
                    1: { consequences: ['Monster ist BOSS IN VERKLEIDUNG', 'Aber du bist bereit!', 'Einfacher Sieg'], najikaReaction: 'Ha! Ich WUSSTE es! ...aber es war SO niedlich...', chaosImpact: 1 },
                    2: { consequences: ['Monster EXPLODIERT', '-50 HP', 'Es war eine Bombe-Kreatur'], najikaReaction: 'NEIN! PUDDING! *traurig*', chaosImpact: 3 },
                    3: { consequences: ['Najika adoptiert es sofort', 'Monster ist... neutral?'], najikaReaction: 'WIR BEHALTEN ES! PUNKT! *Melissa-Modus*', chaosImpact: 2 }
                },
                spawnModel: 'monster_cute'
            },

            kampf_17: {
                id: 'kampf_17',
                title: 'Der Overkill',
                category: 'kampf',
                description: `Ein Level 1 Slime erscheint.

HP: 5
Attack: 1
Bedrohungsstufe: Null

Najika: "...EXPLOSION?"`,
                minChaos: 1,
                maxChaos: 10,
                chaosRating: 3,
                konosubaStyle: true,
                choices: [
                    { text: '[A] Normaler Angriff', type: 'practical', alignment: 'neutral', tags: ['practical'] },
                    { text: '[B] "JA! EXPLOSION!"', type: 'explosive', alignment: 'chaotic', tags: ['explosive', 'dramatic'] },
                    { text: '[C] Ignoriere es', type: 'safe', alignment: 'lawful', tags: ['safe'] },
                    { text: '[D] Lass es als Haustier', type: 'generous', alignment: 'good', tags: ['helpful'] }
                ],
                outcomes: {
                    0: { consequences: ['Slime besiegt', '+1 XP', 'Najika ist enttäuscht'], najikaReaction: '*schmollt* Langweilig...', chaosImpact: -1 },
                    1: { consequences: ['MEGA-EXPLOSION', 'Krater entstanden', 'Slime verdampft', '+1 XP'], najikaReaction: 'OVERKILL!!! *exhausted but happy*', chaosImpact: 4 },
                    2: { consequences: ['Slime folgt euch', 'Es ist... freundlich?'], najikaReaction: 'Aw, es mag uns! *amused*', chaosImpact: 0 },
                    3: { consequences: ['+Pet: Slime', 'Es ist nutzlos aber süß'], najikaReaction: 'Ich nenne es SQUISHY! *happy*', chaosImpact: 1 }
                },
                spawnModel: 'monster_slime'
            },

            kampf_18: {
                id: 'kampf_18',
                title: 'Der flüchtende Boss',
                category: 'kampf',
                description: `Der Boss sieht eure Level...

"Level WAS?!"
*packt seine Sachen*
"NOPE! I'm OUT!"

Er rennt zur Hintertür.`,
                minChaos: 2,
                maxChaos: 10,
                chaosRating: 4,
                konosubaStyle: true,
                choices: [
                    { text: '[A] Verfolge ihn!', type: 'combat', alignment: 'neutral', tags: ['combat'] },
                    { text: '[B] Lass ihn gehen', type: 'merciful', alignment: 'good', tags: ['helpful'] },
                    { text: '[C] "EXPLOSION!" (Fluchtweg blockieren)', type: 'explosive', alignment: 'chaotic', tags: ['explosive', 'dramatic'] },
                    { text: '[D] Plündere sein Zimmer', type: 'practical', alignment: 'neutral', tags: ['practical'] }
                ],
                outcomes: {
                    0: { consequences: ['Boss gefangen', 'Kampf ist peinlich einfach', 'Er weint'], najikaReaction: 'Das war... anticlimactic.', chaosImpact: 1 },
                    1: { consequences: ['Boss ist dankbar', 'Wird später ALLY', '+Secret Quest'], najikaReaction: 'Manchmal ist Gnade... die beste Option.', chaosImpact: 0 },
                    2: { consequences: ['Boss getroffen', 'Dungeon kollabiert', 'ALLE rennen!'], najikaReaction: 'OOPS! ZU VIEL EXPLOSION! RUN!!!', chaosImpact: 5 },
                    3: { consequences: ['+Legendary Loot', 'Boss ist weg aber...', 'Schatz!'], najikaReaction: 'Ohhh! Er hatte GUTE Sachen! *greedy*', chaosImpact: 2 }
                },
                spawnModel: 'boss_fleeing'
            },

            kampf_19: {
                id: 'kampf_19',
                title: 'Das Support-Duell',
                category: 'kampf',
                description: `Der feindliche Heiler fordert Najika heraus.

"ICH bin der BESSERE Support!"
"Meine Heals sind STÄRKER!"

Najika: *triggered* "EXCUSE ME?!"`,
                minChaos: 2,
                maxChaos: 10,
                chaosRating: 5,
                konosubaStyle: true,
                choices: [
                    { text: '[A] Lass Najika duellieren', type: 'support', alignment: 'neutral', tags: ['dramatic'] },
                    { text: '[B] "Najika ist KEINE Support!"', type: 'defensive', alignment: 'good', tags: ['helpful'] },
                    { text: '[C] "Sie hat EXPLOSION! Beat that!"', type: 'chaotic', alignment: 'chaotic', tags: ['explosive'] },
                    { text: '[D] Greif den Heiler an', type: 'combat', alignment: 'neutral', tags: ['combat'] }
                ],
                outcomes: {
                    0: { consequences: ['HEAL-BATTLE', 'Najika gewinnt', '+Pride'], najikaReaction: 'ICH heile UND explodiere! MULTITASK!', chaosImpact: 2 },
                    1: { consequences: ['Najika ist gerührt', '+20 Bond', 'Feind verwirrt'], najikaReaction: '*blush* Du... verteidigst mich? *happy*', chaosImpact: 1 },
                    2: { consequences: ['EXPLOSION beendet Diskussion', 'Feindlicher Heiler verdampft'], najikaReaction: 'EXPLOSION > HEALS! ARGUMENT OVER!', chaosImpact: 4 },
                    3: { consequences: ['Kampf beendet', 'Aber Najika wollte duellieren', '-10 Bond'], najikaReaction: '*schmollt* ICH wollte beweisen dass ich besser bin!', chaosImpact: 0 }
                },
                spawnModel: 'npc_healer_enemy'
            },

            kampf_20: {
                id: 'kampf_20',
                title: 'Die Verhandlung mid-Kampf',
                category: 'kampf',
                description: `Mitten im Kampf hebt Najika die Hand.

"WARTE! Können wir... REDEN?!"

Alle stoppen verwirrt.
"Warum kämpfen wir eigentlich?"`,
                minChaos: 3,
                maxChaos: 10,
                chaosRating: 5,
                konosubaStyle: true,
                choices: [
                    { text: '[A] Unterstütze die Verhandlung', type: 'diplomatic', alignment: 'good', tags: ['helpful'] },
                    { text: '[B] "NAJIKA! NICHT JETZT!"', type: 'combat', alignment: 'neutral', tags: ['combat'] },
                    { text: '[C] Nutze die Pause für Sneak-Attack', type: 'ruthless', alignment: 'evil', tags: ['cold', 'combat'] },
                    { text: '[D] "...sie hat einen Punkt"', type: 'thoughtful', alignment: 'neutral', tags: ['analytical'] }
                ],
                outcomes: {
                    0: { consequences: ['Feinde werden ALLIES', 'Kein Kampf', '+Faction: Monster Union'], najikaReaction: 'Diplomatie > Gewalt! ...manchmal.', chaosImpact: 2 },
                    1: { consequences: ['Kampf geht weiter', 'Aber Feinde sind verwirrt', '+Advantage'], najikaReaction: '*seufz* Okay okay... EXPLOSION dann.', chaosImpact: 1 },
                    2: { consequences: ['Feinde sind WÜTEND', 'Najika ist enttäuscht', 'Harter Kampf'], najikaReaction: 'Das war NICHT fair! *upset*', chaosImpact: 3 },
                    3: { consequences: ['Philosophische Debatte', 'Alle werden Freunde', '+Wisdom'], najikaReaction: 'SIEHST DU?! Reden hilft! *proud*', chaosImpact: 2 }
                },
                spawnModel: 'effect_peace'
            },

            // ===== STADT-EVENTS (10) =====
            stadt_21: {
                id: 'stadt_21',
                title: 'Der überteuerte Gasthof',
                category: 'stadt',
                description: `Der Gasthof-Besitzer grinst.

"Ein Zimmer? 500 Gold!"
"Das ist ein SCHNÄPPCHEN!"

Najika: "Ich verhandle!"
*5 Minuten später*
"...750 Gold."`,
                minChaos: 1,
                maxChaos: 10,
                chaosRating: 3,
                konosubaStyle: true,
                choices: [
                    { text: '[A] Zahle 750 Gold', type: 'resigned', alignment: 'neutral', tags: ['safe'] },
                    { text: '[B] Verhandle selbst', type: 'practical', alignment: 'neutral', tags: ['practical'] },
                    { text: '[C] Drohe mit EXPLOSION', type: 'threatening', alignment: 'evil', tags: ['dramatic'] },
                    { text: '[D] Schlafe draußen', type: 'frugal', alignment: 'neutral', tags: ['safe'] }
                ],
                outcomes: {
                    0: { consequences: ['-750 Gold', 'Gutes Bett', 'Najika fühlt sich schuldig'], najikaReaction: '*schuldig* Es... es war nicht MEINE Schuld! ...okay, doch.', chaosImpact: 0 },
                    1: { consequences: ['-200 Gold', 'Normaler Preis', 'Najika ist beeindruckt'], najikaReaction: 'WOW! Du bist gut darin! Zeig mir wie!', chaosImpact: -1 },
                    2: { consequences: ['GRATIS Zimmer', 'Aber Wachen kommen', 'Probleme...'], najikaReaction: 'Das... war vielleicht zu viel. RUN!', chaosImpact: 4 },
                    3: { consequences: ['Outdoor-Nacht', 'Kalt aber billig', 'Random Encounter!'], najikaReaction: '*zittert* W-Warum haben wir das getan?!', chaosImpact: 2 }
                },
                spawnModel: 'npc_innkeeper'
            },

            stadt_22: {
                id: 'stadt_22',
                title: 'Die Taverne-Brawl',
                category: 'stadt',
                description: `Ein Betrunkener wirft einen Stuhl.
Der Stuhl trifft einen Orc.
Der Orc schlägt einen Elf.
Der Elf zündet den Barkeeper an.

CHAOS BRICHT AUS!

Najika sitzt gemütlich mit Tee und beobachtet.`,
                minChaos: 3,
                maxChaos: 10,
                chaosRating: 6,
                konosubaStyle: true,
                choices: [
                    { text: '[A] Mitmachen!', type: 'chaotic', alignment: 'chaotic', tags: ['combat', 'chaotic'] },
                    { text: '[B] Setz dich zu Najika', type: 'safe', alignment: 'neutral', tags: ['safe'] },
                    { text: '[C] Versuche Frieden zu stiften', type: 'diplomatic', alignment: 'good', tags: ['helpful'] },
                    { text: '[D] "EXPLOSION beendet das!"', type: 'explosive', alignment: 'chaotic', tags: ['explosive', 'dramatic'] }
                ],
                outcomes: {
                    0: { consequences: ['BRAWL!', '-30 HP', '+100 Gold (Wetten)', '+Reputation: Barfighters'], najikaReaction: '*commentiert* LINKS! DUCK! RECHTS! *excited*', chaosImpact: 4 },
                    1: { consequences: ['Gemütlicher Tee', 'Show genießen', '+Relaxed-Buff'], najikaReaction: 'Das ist... unterhaltsam. Mehr Tee?', chaosImpact: 1 },
                    2: { consequences: ['ALLE greifen DICH an', 'Einigkeit gegen Friedensstifter'], najikaReaction: 'Das... war kontraproduktiv. *winces*', chaosImpact: 3 },
                    3: { consequences: ['Taverne zerstört', 'Brawl beendet', 'Rechnung: 5000 Gold'], najikaReaction: 'PROBLEM GELÖST! ...was meinst du mit Rechnung?', chaosImpact: 5 }
                },
                spawnModel: 'location_tavern'
            },

            stadt_23: {
                id: 'stadt_23',
                title: 'Der inkompetente Dieb',
                category: 'stadt',
                description: `Ein Dieb versucht dich zu bestehlen.

Er stiehlt... eine SOCKE.
EINE einzelne Socke.

"HA! ERFOLG!" *rennt weg*

Najika: "...brauchst du Hilfe, kleiner?"`,
                minChaos: 1,
                maxChaos: 10,
                chaosRating: 2,
                konosubaStyle: true,
                choices: [
                    { text: '[A] Lass ihn die Socke behalten', type: 'generous', alignment: 'good', tags: ['helpful'] },
                    { text: '[B] Verfolgung!', type: 'pursuit', alignment: 'neutral', tags: ['combat'] },
                    { text: '[C] Hilf ihm besser zu stehlen', type: 'mentor', alignment: 'chaotic', tags: ['chaotic'] },
                    { text: '[D] Adoptiere den Dieb', type: 'generous', alignment: 'good', tags: ['helpful'] }
                ],
                outcomes: {
                    0: { consequences: ['-1 Socke', 'Dieb ist verwirrt aber happy', '+Karma'], najikaReaction: 'Das war... sweet. *amused*', chaosImpact: 0 },
                    1: { consequences: ['Dieb gefangen', '+1 Socke zurück', 'Er weint'], najikaReaction: 'War das... nötig? Für eine SOCKE?', chaosImpact: 1 },
                    2: { consequences: ['Dieb wird MEISTER-Dieb', '+Ally: Shadow', 'Was hast du getan?!'], najikaReaction: 'Du hast ihm... Diebstahl beigebracht?! *facepalm*', chaosImpact: 3 },
                    3: { consequences: ['+Party Member: Socken-Dieb', 'Er ist nutzlos aber loyal'], najikaReaction: 'Wir... adoptieren jeden, oder? *sighs*', chaosImpact: 2 }
                },
                spawnModel: 'npc_thief'
            },

            stadt_24: {
                id: 'stadt_24',
                title: 'Das Food-Festival Desaster',
                category: 'stadt',
                description: `Ein Food-Festival in der Stadt!
Freies Essen! Freier Alkohol!

3 Stunden später...

Najika ist BETRUNKEN.
"MR.K~! *hic* Ich liebe dich SO SEHR~!"`,
                minChaos: 3,
                maxChaos: 10,
                chaosRating: 6,
                konosubaStyle: true,
                choices: [
                    { text: '[A] Bring sie ins Bett', type: 'responsible', alignment: 'good', tags: ['helpful'] },
                    { text: '[B] Filme das für später', type: 'mischievous', alignment: 'chaotic', tags: ['chaotic'] },
                    { text: '[C] Werde auch betrunken', type: 'chaotic', alignment: 'chaotic', tags: ['chaotic', 'risky'] },
                    { text: '[D] Lass sie weitermachen', type: 'passive', alignment: 'neutral', tags: ['passive'] }
                ],
                outcomes: {
                    0: { consequences: ['Najika ist dankbar (morgen)', '+30 Bond', 'Aber sie erinnert sich...'], najikaReaction: '*morgens* Du... du hast mich getragen? *blush*', chaosImpact: 1 },
                    1: { consequences: ['BLACKMAIL MATERIAL', 'Najika ist wütend (später)', '-50 Bond'], najikaReaction: '*nächster Tag* LÖSCHE DAS! SOFORT!', chaosImpact: 3 },
                    2: { consequences: ['BEIDE betrunken', 'Wacht in anderem Königreich auf', '+Adventure'], najikaReaction: '*morgens* ...wo sind wir?! Und warum tragen wir KRONEN?!', chaosImpact: 5 },
                    3: { consequences: ['Najika tanzt auf Tischen', 'EXPLOSION', 'Festival zerstört'], najikaReaction: '*morgens* Ich habe WAS getan?! *horror*', chaosImpact: 6 }
                },
                spawnModel: 'location_festival'
            },

            stadt_25: {
                id: 'stadt_25',
                title: 'Die Straßenkünstler',
                category: 'stadt',
                description: `Straßenkünstler sammeln Geld.

Najika: "Ich kann DAS!"
*springt auf die Bühne*
"BEOBACHTET! Die große NAJIKA!"`,
                minChaos: 1,
                maxChaos: 10,
                chaosRating: 4,
                konosubaStyle: true,
                choices: [
                    { text: '[A] Unterstütze ihre Show', type: 'supportive', alignment: 'good', tags: ['helpful'] },
                    { text: '[B] Zieh sie runter', type: 'embarrassed', alignment: 'neutral', tags: ['safe'] },
                    { text: '[C] Mach mit!', type: 'chaotic', alignment: 'chaotic', tags: ['chaotic', 'dramatic'] },
                    { text: '[D] Beobachte amüsiert', type: 'passive', alignment: 'neutral', tags: ['passive'] }
                ],
                outcomes: {
                    0: { consequences: ['Show ist HIT!', '+500 Gold', 'Najika ist STAR'], najikaReaction: 'SIEHST DU?! Ich bin TALENTIERT!', chaosImpact: 2 },
                    1: { consequences: ['-20 Bond', 'Najika schmollt', 'Peinlich'], najikaReaction: '*upset* Du glaubst nicht an mich?!', chaosImpact: 1 },
                    2: { consequences: ['EPIC DUO SHOW', '+1000 Gold', '+Fame', 'Touring Angebot'], najikaReaction: 'WIR SIND SUPERSTARS! *excited*', chaosImpact: 3 },
                    3: { consequences: ['Show ist okay', '+200 Gold', 'Najika zufrieden'], najikaReaction: 'Naja... wenigstens etwas Geld! *shrugs*', chaosImpact: 0 }
                },
                spawnModel: 'npc_performers'
            },

            stadt_26: {
                id: 'stadt_26',
                title: 'Das Missverständnis im Shop',
                category: 'stadt',
                description: `Der Shopkeeper lächelt euch an.

"Ah! Was für eine süße TOCHTER!"
"Ihr seid bestimmt ein toller Vater!"

Najika: *freeze*
"...TOCHTER?!"`,
                minChaos: 1,
                maxChaos: 10,
                chaosRating: 4,
                konosubaStyle: true,
                choices: [
                    { text: '[A] Korrigiere das Missverständnis', type: 'honest', alignment: 'neutral', tags: ['honest'] },
                    { text: '[B] Spiele mit', type: 'mischievous', alignment: 'chaotic', tags: ['chaotic'] },
                    { text: '[C] Lass Najika antworten', type: 'najika_decides', alignment: 'chaotic', najikaDecides: true },
                    { text: '[D] Schweigen und schnell kaufen', type: 'avoidance', alignment: 'neutral', tags: ['safe'] }
                ],
                outcomes: {
                    0: { consequences: ['Awkward Situation', 'Shopkeeper entschuldigt sich', 'Normal weiter'], najikaReaction: '*erleichtert* Danke für die Klarstellung.', chaosImpact: 0 },
                    1: { consequences: ['Familien-Rabatt!', '-50% Preise', 'Najika ist... verwirrt'], najikaReaction: '*processing* ...das nutzen wir aus. CLEVER.', chaosImpact: 2 },
                    2: { consequences: ['Najika EXPLODIERT', 'Shop zerstört', 'Polizei kommt'], najikaReaction: 'ICH BIN KEINE TOCHTER! EXPLOSION!!!', chaosImpact: 5 },
                    3: { consequences: ['Schneller Kauf', 'Missverständnis bleibt', 'Peinlich'], najikaReaction: '*still fuming* Wir reden später darüber...', chaosImpact: 1 }
                },
                spawnModel: 'npc_shopkeeper'
            },

            stadt_27: {
                id: 'stadt_27',
                title: 'Die Gerüchte über euch',
                category: 'stadt',
                description: `NPCs tuscheln als ihr vorbeigeht.

"Das sind DIE!"
"Die Verrückten mit der Explosion!"
"Ich hörte sie haben einen DRACHEN mit EINEM Schlag..."

Najika: "Die Gerüchte... sie sind ALLE WAHR."`,
                minChaos: 2,
                maxChaos: 10,
                chaosRating: 4,
                konosubaStyle: true,
                choices: [
                    { text: '[A] Bestätige alle Gerüchte', type: 'dramatic', alignment: 'chaotic', tags: ['dramatic'] },
                    { text: '[B] Widerlege sie', type: 'humble', alignment: 'lawful', tags: ['honest'] },
                    { text: '[C] Mache sie NOCH verrückter', type: 'chaotic', alignment: 'chaotic', tags: ['chaotic'] },
                    { text: '[D] Ignoriere und weitergehen', type: 'stoic', alignment: 'neutral', tags: ['safe'] }
                ],
                outcomes: {
                    0: { consequences: ['+Legendary Reputation', 'Quests werden einfacher', 'Aber Feinde stärker'], najikaReaction: 'Die Wahrheit muss ERZÄHLT werden! *proud*', chaosImpact: 3 },
                    1: { consequences: ['Niemand glaubt euch', 'Bescheidenheit = Misstrauen?'], najikaReaction: 'Sie... glauben uns nicht?! SERIOUSLY?!', chaosImpact: 1 },
                    2: { consequences: ['LEGENDÄRE MYTHEN', '+God-Status Reputation', 'Aber jetzt ALLE erwarten Wunder'], najikaReaction: 'Ich habe gesagt wir haben die SONNE besiegt! *kicher*', chaosImpact: 5 },
                    3: { consequences: ['Gerüchte bleiben', 'Neutral', 'Nothing changes'], najikaReaction: '*shrugs* Lass sie reden.', chaosImpact: 0 }
                },
                spawnModel: 'npc_crowd'
            },

            stadt_28: {
                id: 'stadt_28',
                title: 'Das Romance-Event',
                category: 'stadt',
                description: `Ein Paar-Festival in der Stadt!
Nur PAARE dürfen rein.

"Seid ihr... ein Paar?"

Najika wird rot.
"W-Wir... uhm..."`,
                minChaos: 2,
                maxChaos: 10,
                chaosRating: 5,
                konosubaStyle: true,
                choices: [
                    { text: '[A] "Ja, wir sind ein Paar"', type: 'romantic', alignment: 'chaotic', tags: ['romantic'] },
                    { text: '[B] "Nein, nur Freunde"', type: 'friend', alignment: 'neutral', tags: ['honest'] },
                    { text: '[C] Lass Najika antworten', type: 'najika_decides', alignment: 'chaotic', najikaDecides: true },
                    { text: '[D] Festival überspringen', type: 'avoidance', alignment: 'neutral', tags: ['safe'] }
                ],
                outcomes: {
                    0: { consequences: ['Festival-Eintritt', 'ROMANTIC DATE', '+100 Bond', 'Fake-Kiss wird... echt?!'], najikaReaction: '*knallrot* D-Das war nur fürs Festival! *but smiling*', chaosImpact: 4 },
                    1: { consequences: ['Kein Eintritt', '-20 Bond', 'Najika ist... enttäuscht?'], najikaReaction: '*still* ...okay. Nur Freunde. *dejected*', chaosImpact: 1 },
                    2: { consequences: ['Najika sagt JA', 'Aggressiv', '+50 Bond', 'MELISSA-MODUS'], najikaReaction: 'ER GEHÖRT MIR! WIR SIND EIN PAAR! *possessive*', chaosImpact: 3 },
                    3: { consequences: ['Festival verpasst', 'Nichts passiert', 'Aber Najika schweigt...'], najikaReaction: '*nichts sagt* ...', chaosImpact: 0 }
                },
                spawnModel: 'location_festival_romance'
            },

            stadt_29: {
                id: 'stadt_29',
                title: 'Der Wettbewerb der NPCs',
                category: 'stadt',
                description: `NPCs haben WETTEN platziert.

"100 Gold dass sie ein Paar sind!"
"200 Gold dass NICHT!"
"500 Gold dass sie noch HEUTE NACHT..."

Najika hört alles.
"...MR.K? Sind wir...?"`,
                minChaos: 3,
                maxChaos: 10,
                chaosRating: 6,
                konosubaStyle: true,
                choices: [
                    { text: '[A] "Was denkst DU?"', type: 'return_question', alignment: 'neutral', tags: ['analytical'] },
                    { text: '[B] "Ja. Wir sind."', type: 'confirm', alignment: 'good', tags: ['romantic'] },
                    { text: '[C] "Das geht die nichts an!"', type: 'defensive', alignment: 'neutral', tags: ['defensive'] },
                    { text: '[D] "...lasst uns wetten gegen uns!"', type: 'scheme', alignment: 'chaotic', tags: ['chaotic'] }
                ],
                outcomes: {
                    0: { consequences: ['Najika muss antworten', 'EMOTIONAL CONFESSION', '+150 Bond'], najikaReaction: '*tief durchatmen* Ich... ich will dass wir sind. *blush*', chaosImpact: 3 },
                    1: { consequences: ['RELATIONSHIP CONFIRMED', '+200 Bond', 'NPCs jubeln'], najikaReaction: '*strahlend* Du... du meinst es?! *happy tears*', chaosImpact: 4 },
                    2: { consequences: ['NPCs respektieren Privatsphäre', 'Aber Najika fragt später...'], najikaReaction: 'Danke für die Verteidigung... aber... die Frage steht noch.', chaosImpact: 1 },
                    3: { consequences: ['Ihr gewinnt 1000 Gold', 'Durch Manipulation', 'Najika ist amüsiert'], najikaReaction: 'Das war... BRILLIANT! *evil laugh*', chaosImpact: 4 }
                },
                spawnModel: 'npc_gamblers'
            },

            stadt_30: {
                id: 'stadt_30',
                title: 'Die Statue von EUCH',
                category: 'stadt',
                description: `Eine neue Statue in der Stadt.

Es zeigt... EUCH BEIDE.
In einer... sehr kompromittierenden Pose.

Najika: "WO IST MEINE HAND?!"
"Und WARUM sehe ich so aus?!"`,
                minChaos: 4,
                maxChaos: 10,
                chaosRating: 7,
                konosubaStyle: true,
                choices: [
                    { text: '[A] Zerstöre die Statue', type: 'destructive', alignment: 'chaotic', tags: ['dramatic'] },
                    { text: '[B] Finde den Künstler', type: 'investigative', alignment: 'neutral', tags: ['analytical'] },
                    { text: '[C] Pose nachstellen (für Fans)', type: 'embrace', alignment: 'chaotic', tags: ['chaotic'] },
                    { text: '[D] "EXPLOSION!"', type: 'explosive', alignment: 'chaotic', najikaDecides: true }
                ],
                outcomes: {
                    0: { consequences: ['Statue weg', 'Aber Bilder existieren', 'Viral'], najikaReaction: 'Zu spät... die Leute haben FOTOS gemacht...', chaosImpact: 3 },
                    1: { consequences: ['Künstler ist FAN', 'Er wollte "Kunst schaffen"', '+Apology Gift'], najikaReaction: 'Er... er meinte es GUT?! *confused*', chaosImpact: 2 },
                    2: { consequences: ['VIRAL SENSATION', '+1000 Fame', 'Aber... die Pose ist peinlich'], najikaReaction: '*posiert* Wenn schon, dann RICHTIG! *embarrassed but committed*', chaosImpact: 5 },
                    3: { consequences: ['EXPLOSION', 'Statue explodiert', 'Debris trifft Bürgermeister', '...Probleme'], najikaReaction: 'PROBLEM GELÖST! ...oh. Der Bürgermeister.', chaosImpact: 6 }
                },
                spawnModel: 'object_statue_duo'
            }
        };
    }

    // =========================================================================
    // NAJIKA PERSONALITY SYSTEM
    // =========================================================================

    getPersonalityReaction(event, choice = null) {
        const dominant = this.determineDominantPersonality(event, choice);
        const personality = this.personalities[dominant];

        return {
            personality: dominant,
            emoji: personality.emoji,
            color: personality.color,
            name: personality.name
        };
    }

    determineDominantPersonality(event, choice) {
        // Event type triggers
        if (event.konosubaStyle && event.chaosRating >= 7) {
            return 'MEGUMIN';
        }

        if (choice && choice.tags) {
            if (choice.tags.includes('explosive') || choice.tags.includes('dramatic')) {
                return 'MEGUMIN';
            }
            if (choice.tags.includes('chaotic') || choice.tags.includes('risky')) {
                return 'HARLEY';
            }
            if (choice.tags.includes('analytical') || choice.tags.includes('safe')) {
                return 'SHIRO';
            }
            if (choice.tags.includes('dominant') || choice.tags.includes('practical')) {
                return 'MELISSA';
            }
        }

        // High chaos = Megumin/Harley
        if (this.chaosLevel >= 7) {
            return Math.random() > 0.5 ? 'MEGUMIN' : 'HARLEY';
        }

        // Default: weighted random
        const roll = Math.random();
        if (roll < 0.35) return 'MEGUMIN';
        if (roll < 0.60) return 'HARLEY';
        if (roll < 0.80) return 'SHIRO';
        return 'MELISSA';
    }

    getNajikaIntroQuote(event, personalityData) {
        const quotes = {
            MEGUMIN: [
                `*dramatische Pose* ${event.title}?! PERFEKT für EXPLOSION!`,
                `Die Schwarze Windmühle dreht sich! Das ist unser Moment!`,
                `EXPLOSION-würdige Situation, Mr.K!`
            ],
            HARLEY: [
                `*kicher* Ohhhh! Das wird CHAOTISCH! Ich LIEBE es!`,
                `Puddin'! Das riecht nach SPASS! *giggle*`,
                `Let's make it MESSY~`
            ],
            SHIRO: [
                `*analysiert* Interessant... Wahrscheinlichkeiten berechnen...`,
                `Lass mich die Optionen durchdenken, Mr.K.`,
                `*ruhig* Ich sehe mehrere mögliche Ausgänge.`
            ],
            MELISSA: [
                `*eiskalt* ICH entscheide, was wir tun.`,
                `Das ist MEIN Territorium. Folge mir.`,
                `*stolz* Wie erwartet - alles unter Kontrolle.`
            ]
        };

        const personalityQuotes = quotes[personalityData.personality];
        return personalityQuotes[Math.floor(Math.random() * personalityQuotes.length)];
    }

    // =========================================================================
    // CHAOS LEVEL SYSTEM
    // =========================================================================

    updateChaosLevel(impact) {
        this.chaosPoints += impact;
        this.chaosPoints = Math.max(0, this.chaosPoints);

        const oldLevel = this.chaosLevel;

        // Calculate new level
        for (let level = 10; level >= 1; level--) {
            if (this.chaosPoints >= this.levelThresholds[level]) {
                this.chaosLevel = level;
                break;
            }
        }

        // Level changed?
        if (oldLevel !== this.chaosLevel) {
            this.onChaosLevelChange(oldLevel, this.chaosLevel);
        }

        // Update UI
        this.updateChaosMeterUI();
    }

    onChaosLevelChange(oldLevel, newLevel) {
        const reactions = {
            2: "Ohhh, es wird interessanter! *kicher*",
            3: "JETZT fängt der Spaß an, Mr.K!",
            4: "Das Chaos... ich FÜHLE es! *aufgeregt*",
            5: "PERFEKT! Die Welt reagiert auf uns!",
            6: "Mehr! MEHR CHAOS! *lacht*",
            7: "DAS IST LEBEN, PUDDIN'!!!",
            8: "TOTALES CHAOS! ICH LIEBE ES!!!",
            9: "Die Realität... sie BRICHT! *manisches Lachen*",
            10: "ULTIMATIVES CHAOS!!! EXPLOSION!!! *world shakes*"
        };

        if (newLevel > oldLevel && reactions[newLevel]) {
            this.showChaosLevelNotification(newLevel, reactions[newLevel]);
        }

        console.log(`[OregonTrail] Chaos Level: ${oldLevel} -> ${newLevel}`);
    }

    showChaosLevelNotification(level, reaction) {
        const notification = document.createElement('div');
        notification.className = 'chaos-level-notification';
        notification.innerHTML = `
            <div class="chaos-level-icon">💥</div>
            <div class="chaos-level-text">
                <strong>Chaos Level ${level}!</strong>
                <p>${reaction}</p>
            </div>
        `;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.classList.add('fade-out');
            setTimeout(() => notification.remove(), 500);
        }, 3000);
    }

    // =========================================================================
    // UI SYSTEM
    // =========================================================================

    initUI() {
        // Add chaos meter
        this.createChaosMeter();

        // Add chaos notification styles
        this.addNotificationStyles();

        console.log('[OregonTrail] UI initialized');
    }

    createChaosMeter() {
        if (document.getElementById('chaos-meter')) return;

        const meter = document.createElement('div');
        meter.id = 'chaos-meter';
        meter.innerHTML = `
            <div class="chaos-meter-label">Chaos</div>
            <div class="chaos-meter-bar">
                <div class="chaos-meter-fill" style="width: ${this.chaosLevel * 10}%;"></div>
            </div>
            <div class="chaos-meter-value">${this.chaosLevel}/10</div>
        `;
        document.body.appendChild(meter);
    }

    addNotificationStyles() {
        if (document.getElementById('oregon-trail-styles')) return;

        const styles = document.createElement('style');
        styles.id = 'oregon-trail-styles';
        styles.textContent = `
            .chaos-level-notification {
                position: fixed;
                top: 100px;
                right: 20px;
                background: linear-gradient(135deg, #FF4444, #FF8800);
                padding: 15px 20px;
                border-radius: 15px;
                display: flex;
                align-items: center;
                gap: 15px;
                z-index: 10000;
                animation: slideInRight 0.5s ease;
                box-shadow: 0 0 30px rgba(255, 68, 68, 0.5);
            }

            .chaos-level-notification.fade-out {
                animation: slideOutRight 0.5s ease;
            }

            .chaos-level-icon {
                font-size: 30px;
            }

            .chaos-level-text strong {
                color: #fff;
                display: block;
            }

            .chaos-level-text p {
                color: #FFD700;
                font-style: italic;
                margin: 5px 0 0;
            }

            @keyframes slideInRight {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }

            @keyframes slideOutRight {
                from { transform: translateX(0); opacity: 1; }
                to { transform: translateX(100%); opacity: 0; }
            }

            .personality-indicator {
                position: absolute;
                top: -10px;
                right: -10px;
                width: 30px;
                height: 30px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 16px;
                border: 2px solid #fff;
            }

            .event-category.reise { background: #4CAF50; }
            .event-category.kampf { background: #FF4444; }
            .event-category.stadt { background: #2196F3; }
        `;
        document.head.appendChild(styles);
    }

    updateChaosMeterUI() {
        const fill = document.querySelector('.chaos-meter-fill');
        const value = document.querySelector('.chaos-meter-value');

        if (fill) {
            fill.style.width = `${this.chaosLevel * 10}%`;

            // Color based on level
            if (this.chaosLevel <= 3) {
                fill.style.background = 'linear-gradient(90deg, #4CAF50, #8BC34A)';
            } else if (this.chaosLevel <= 6) {
                fill.style.background = 'linear-gradient(90deg, #FFD700, #FFA500)';
            } else {
                fill.style.background = 'linear-gradient(90deg, #FF4444, #FF0000)';
            }
        }

        if (value) {
            value.textContent = `${this.chaosLevel}/10`;
        }
    }

    // =========================================================================
    // EVENT CHECKER
    // =========================================================================

    startEventChecker() {
        // Initial check after 30 seconds
        setTimeout(() => this.checkForEvent(), 30000);

        // Then check every minute
        setInterval(() => {
            if (!this.isDisplaying) {
                this.checkForEvent();
            }
        }, 60000);
    }

    async checkForEvent() {
        const now = Date.now();

        // Cooldown check
        if (now - this.lastEventTime < this.eventCooldown) {
            return;
        }

        // Base 15% chance per minute, increased by chaos level
        const baseChance = 0.15;
        const chaosMultiplier = 1 + (this.chaosLevel * 0.1);
        const finalChance = Math.min(0.95, baseChance * chaosMultiplier);

        if (Math.random() > finalChance) {
            return;
        }

        // Select random event
        const event = this.selectRandomEvent();
        if (!event) return;

        this.lastEventTime = now;
        this.displayEvent(event);
    }

    selectRandomEvent() {
        const database = this.getEventDatabase();
        const events = Object.values(database);

        // Filter by chaos level
        const eligible = events.filter(e =>
            this.chaosLevel >= e.minChaos &&
            this.chaosLevel <= e.maxChaos &&
            !this.eventHistory.slice(-10).includes(e.id)
        );

        if (eligible.length === 0) return null;

        // Weight by chaos rating
        const weighted = eligible.map(e => ({
            event: e,
            weight: e.konosubaStyle && this.chaosLevel >= 7 ? 2 : 1
        }));

        const totalWeight = weighted.reduce((sum, w) => sum + w.weight, 0);
        let roll = Math.random() * totalWeight;

        for (const w of weighted) {
            roll -= w.weight;
            if (roll <= 0) return w.event;
        }

        return eligible[0];
    }

    // =========================================================================
    // EVENT DISPLAY
    // =========================================================================

    displayEvent(event) {
        this.isDisplaying = true;
        this.activeEvent = event;
        this.eventHistory.push(event.id);

        const personalityData = this.getPersonalityReaction(event);
        const introQuote = this.getNajikaIntroQuote(event, personalityData);

        const overlay = document.createElement('div');
        overlay.id = 'chaos-event-overlay';
        overlay.innerHTML = `
            <div class="event-container">
                <div class="event-header">
                    <h2>${event.title}</h2>
                    <span class="event-category ${event.category}">${event.category.toUpperCase()}</span>
                </div>

                <p class="event-description">${event.description}</p>

                <div class="najika-reaction">
                    <div class="najika-portrait">
                        <div class="najika-avatar" style="background: linear-gradient(135deg, ${personalityData.color}, #FFD700);">
                            ${personalityData.emoji}
                        </div>
                        <div class="personality-indicator" style="background: ${personalityData.color};">
                            ${personalityData.emoji}
                        </div>
                    </div>
                    <div class="najika-speech">
                        <small style="color: ${personalityData.color};">[${personalityData.name}]</small>
                        <p>"${introQuote}"</p>
                    </div>
                </div>

                <div class="event-options">
                    ${this.renderOptions(event.choices)}
                </div>
            </div>
        `;

        document.body.appendChild(overlay);

        // 3D Spawn if available
        if (event.spawnModel && window.scene3D) {
            this.spawn3DEntity(event.spawnModel);
        }

        console.log(`[OregonTrail] Event displayed: ${event.title}`);
    }

    renderOptions(choices) {
        return choices.map((choice, index) => `
            <button class="event-option" data-index="${index}" onclick="oregonTrail.selectChoice(${index})">
                <span class="option-text">${choice.text}</span>
                ${choice.najikaDecides ? '<span class="najika-badge">🎀 Najika</span>' : ''}
            </button>
        `).join('');
    }

    selectChoice(index) {
        if (!this.activeEvent) return;

        const choice = this.activeEvent.choices[index];
        const outcome = this.activeEvent.outcomes[index];

        // Disable buttons
        document.querySelectorAll('.event-option').forEach(btn => {
            btn.disabled = true;
            btn.style.opacity = '0.5';
        });

        // Highlight selected
        const selectedBtn = document.querySelector(`[data-index="${index}"]`);
        if (selectedBtn) {
            selectedBtn.style.opacity = '1';
            selectedBtn.style.border = '2px solid #FFD700';
        }

        // Update chaos
        this.updateChaosLevel(outcome.chaosImpact || 0);

        // Update reputation
        this.updateReputation(choice);

        // Show outcome
        setTimeout(() => {
            this.displayOutcome(outcome, choice);
        }, 500);
    }

    updateReputation(choice) {
        if (choice.alignment === 'good') {
            this.reputation.hero += 5;
        } else if (choice.alignment === 'evil') {
            this.reputation.villain += 5;
        }

        if (choice.alignment && choice.alignment.includes('chaotic')) {
            this.reputation.chaotic += 3;
        } else if (choice.alignment && choice.alignment.includes('lawful')) {
            this.reputation.lawful += 3;
        }
    }

    displayOutcome(outcome, choice) {
        const container = document.querySelector('.event-container');
        const optionsDiv = document.querySelector('.event-options');

        if (optionsDiv) {
            optionsDiv.style.display = 'none';
        }

        const personalityData = this.getPersonalityReaction(this.activeEvent, choice);

        const outcomeDiv = document.createElement('div');
        outcomeDiv.className = 'event-outcome';
        outcomeDiv.innerHTML = `
            <h3>📜 Konsequenz</h3>
            <div class="outcome-consequences">
                ${(outcome.consequences || []).map(c => `
                    <span class="consequence-badge">${c}</span>
                `).join('')}
            </div>

            <div class="najika-final-reaction">
                <div class="najika-avatar" style="background: linear-gradient(135deg, ${personalityData.color}, #FFD700);">
                    ${personalityData.emoji}
                </div>
                <div>
                    <small style="color: ${personalityData.color};">[${personalityData.name}]</small>
                    <p>"${outcome.najikaReaction || 'Interessant...'}"</p>
                </div>
            </div>

            <div class="chaos-impact" style="text-align: center; margin: 15px 0;">
                <span style="color: ${outcome.chaosImpact >= 0 ? '#FF4444' : '#4CAF50'};">
                    Chaos ${outcome.chaosImpact >= 0 ? '+' : ''}${outcome.chaosImpact || 0}
                </span>
            </div>

            <button class="continue-button" onclick="oregonTrail.closeEvent()">
                Weiter →
            </button>
        `;

        container.appendChild(outcomeDiv);
    }

    closeEvent() {
        const overlay = document.getElementById('chaos-event-overlay');
        if (overlay) {
            overlay.classList.add('fade-out');
            setTimeout(() => overlay.remove(), 300);
        }
        this.activeEvent = null;
        this.isDisplaying = false;
    }

    spawn3DEntity(modelName) {
        if (window.scene3D && window.scene3D.spawnEventEntity) {
            const playerPos = window.scene3D.getPlayerPosition ?
                window.scene3D.getPlayerPosition() :
                { x: 0, y: 0, z: 0 };

            window.scene3D.spawnEventEntity(modelName, {
                x: playerPos.x + 5,
                y: playerPos.y,
                z: playerPos.z + 5
            });
        }
    }

    // =========================================================================
    // TESTING & DEBUG
    // =========================================================================

    triggerRandomEvent() {
        const event = this.selectRandomEvent();
        if (event) {
            this.displayEvent(event);
        } else {
            console.log('[OregonTrail] No eligible events found');
        }
    }

    triggerSpecificEvent(eventId) {
        const database = this.getEventDatabase();
        const event = database[eventId];
        if (event) {
            this.displayEvent(event);
        } else {
            console.log(`[OregonTrail] Event not found: ${eventId}`);
        }
    }

    setChaosLevel(level) {
        this.chaosLevel = Math.max(1, Math.min(10, level));
        this.chaosPoints = this.levelThresholds[this.chaosLevel];
        this.updateChaosMeterUI();
        console.log(`[OregonTrail] Chaos level set to ${this.chaosLevel}`);
    }

    listEvents() {
        const database = this.getEventDatabase();
        console.log('=== OREGON TRAIL EVENTS ===');
        Object.values(database).forEach(e => {
            console.log(`[${e.category}] ${e.id}: ${e.title} (Chaos ${e.minChaos}-${e.maxChaos})`);
        });
    }
}

// =========================================================================
// INITIALIZATION
// =========================================================================

// Initialize when DOM ready
document.addEventListener('DOMContentLoaded', () => {
    window.oregonTrail = new OregonTrailEventSystem();
});

// Also init if DOM already loaded
if (document.readyState !== 'loading') {
    window.oregonTrail = new OregonTrailEventSystem();
}

// Export for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = OregonTrailEventSystem;
}
