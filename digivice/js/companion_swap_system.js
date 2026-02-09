/**
 * NAJIKA WORLD - CHARACTER & COMPANION SYSTEM
 * =============================================
 *
 * CHARAKTER-ERSTELLUNG (ALLE SPIELER):
 *   → Wähle: MENSCH oder MONSTER (eines das in der Spielwelt existiert)
 *   → Monster-Spieler personalisieren ihr gewähltes Monster
 *   → Kuja wählt: MIMIK (EXKLUSIV - nur für ihn!)
 *
 * SLIME-BEGLEITER (ALLE SPIELER):
 *   → Jeder Spieler bekommt einen Slime-Begleiter
 *   → Slime nimmt die Form eines Monsters aus der Startregion an
 *   → Zbsp. Start in Düne → Dünen-Viper Slime
 *   → Slime sieht 1:1 AUS wie das Monster (nicht wie ein Slime MIT Monster-Features!)
 *   → Slime kann neue Formen freispielen (Training, Quests, etc.)
 *   → Slime-Formen = NUR OPTISCH (8 Gebote!)
 *
 * WARUM SLIME UND NICHT MONSTER ALS BEGLEITER?
 *   → 2 Kreatur-Kategorien: "Lebende" (NPCs mit Verstand) + "Vieh" (Minecraft-Tiere)
 *   → "Vieh" (Kat.2) kann GEZÄHMT werden (Füttern, Geduld - KEIN Pokeball!)
 *   → "Lebende" (Kat.1) können ANGEWORBEN werden (Geld, Ruf, Schutz) oder versklavt
 *   → Slime = persönlicher BEGLEITER (separates System, nicht verwechseln!)
 *   → Siehe KREATUR_SYSTEM_KONZEPT.md für Details
 *
 * KUJA (EXKLUSIV):
 *   → Hauptcharakter = Kuja als MIMIK (einzigartiges Monster, NUR er!)
 *   → Begleiterin = Najika (KEIN Slime! Einfach seine Begleiterin!)
 *   → Najika ändert ihre Form NICHT
 *   → Beim TRAINING: Kuja übernimmt den Formen-Part
 *     (bei anderen Spielern macht das der Slime, bei Kuja macht er es SELBST)
 *   → Kuja's Mimik-Formen = NUR OPTISCH (gleiche Regeln wie Slime-Formen)
 *
 * FAIRNESS:
 *   → Normaler Spieler: Charakter + Slime-Companion (Slime wechselt Formen)
 *   → Kuja: Mimik-Charakter (ER wechselt Formen) + Najika (Begleiterin, keine Formen)
 *   → GAMEPLAY MECHANIK IST IDENTISCH
 *   → Training, Evolution, Skills, Care = 1:1 gleich
 *   → Der einzige Unterschied: WER die Formen wechselt (Slime vs Kuja selbst)
 *
 * "Najika ist meine Begleiterin. Sie ändert ihre Form nicht.
 *  Ich bin der Hauptcharakter und wähle die Mimik als Monsterform.
 *  Beim Training tauschen wir optisch die Rollen." - Kuja
 */

(function() {
    'use strict';

    // ==========================================
    // CHARAKTER-ERSTELLUNG
    // ==========================================

    const CHARACTER_TYPES = {
        mensch: {
            id: 'mensch',
            name: 'Mensch',
            description: 'Ein normaler Charakter. Dein Slime-Begleiter übernimmt die Formen!',
            icon: '🧑',
        },
        monster: {
            id: 'monster',
            name: 'Monster',
            description: 'Wähle ein Monster aus der Spielwelt und personalisiere es!',
            icon: '🐉',
            // Verfügbare Monster hängen von der Region ab
        },
        mimik: {
            id: 'mimik',
            name: 'Mimik',
            description: 'EXKLUSIV für Kuja! Ein Formwandler der jede Gestalt annehmen kann.',
            icon: '🫠',
            exclusive: true, // NUR für Owner/Kuja!
        },
    };

    // Monster die in der Spielwelt existieren (Spieler können diese als Charakter wählen)
    const WORLD_MONSTERS = {
        samtmoos: [
            { id: 'waldwolf', name: 'Waldwolf', icon: '🐺', color: '#4CAF50' },
            { id: 'moosspinne', name: 'Moosspinne', icon: '🕷️', color: '#2E7D32' },
            { id: 'baumgeist', name: 'Baumgeist', icon: '🌳', color: '#1B5E20' },
        ],
        heisse_duenen: [
            { id: 'duenen_viper', name: 'Dünen-Viper', icon: '🐍', color: '#FF8F00' },
            { id: 'sandgolem', name: 'Sandgolem', icon: '🗿', color: '#E65100' },
            { id: 'skorpion', name: 'Wüstenskorpion', icon: '🦂', color: '#BF360C' },
        ],
        salzwind: [
            { id: 'meerdrache', name: 'Meerdrache', icon: '🐉', color: '#0277BD' },
            { id: 'krabben_krieger', name: 'Krabbenkrieger', icon: '🦀', color: '#01579B' },
            { id: 'nebelqualle', name: 'Nebelqualle', icon: '🪼', color: '#4FC3F7' },
        ],
        magmastroeme: [
            { id: 'lavaschlange', name: 'Lavaschlange', icon: '🔥', color: '#D84315' },
            { id: 'aschengolem', name: 'Aschengolem', icon: '🌋', color: '#4E342E' },
            { id: 'flammengeist', name: 'Flammengeist', icon: '👻', color: '#FF6D00' },
        ],
        gruenschlamm: [
            { id: 'sumpfkroete', name: 'Sumpfkröte', icon: '🐸', color: '#558B2F' },
            { id: 'giftpilz', name: 'Giftpilz-Golem', icon: '🍄', color: '#7B1FA2' },
            { id: 'moorwurm', name: 'Moorwurm', icon: '🐛', color: '#33691E' },
        ],
        blitzebene: [
            { id: 'sturmfalke', name: 'Sturmfalke', icon: '🦅', color: '#1565C0' },
            { id: 'blitzhirsch', name: 'Blitzhirsch', icon: '🦌', color: '#FFD600' },
            { id: 'donnereber', name: 'Donnereber', icon: '🐗', color: '#37474F' },
        ],
        tiefenhoehlen: [
            { id: 'kristallkafer', name: 'Kristallkäfer', icon: '🪲', color: '#E1BEE7' },
            { id: 'schattenratte', name: 'Schattenratte', icon: '🐀', color: '#424242' },
            { id: 'tiefenwurm', name: 'Tiefenwurm', icon: '🪱', color: '#3E2723' },
        ],
        reich_der_drei: [
            { id: 'frostwolf', name: 'Frostwolf', icon: '🐺', color: '#B3E5FC' },
            { id: 'eisgolem', name: 'Eisgolem', icon: '🧊', color: '#E1F5FE' },
            { id: 'schneeeule', name: 'Schneeeule', icon: '🦉', color: '#ECEFF1' },
        ],
    };

    // ==========================================
    // SLIME-BEGLEITER (für ALLE Spieler)
    // ==========================================
    // Der Slime nimmt beim Start die Form eines Monsters aus der Region an
    // WICHTIG: Slime sieht 1:1 aus wie das Monster! Nicht "Slime mit Monster-Features"
    // sondern EXAKT wie das echte Monster. Nur der Spieler weiß dass es ein Slime ist.
    // Freispielen neuer Formen durch Training/Quests

    function getStartingSlimeForm(startRegion) {
        const regionMonsters = WORLD_MONSTERS[startRegion];
        if (!regionMonsters || regionMonsters.length === 0) {
            return { id: 'basis_slime', name: 'Basis-Slime', icon: '🟢', color: '#4CAF50' };
        }
        // Zufälliges Monster aus der Startregion
        const idx = Math.floor(Math.random() * regionMonsters.length);
        const base = regionMonsters[idx];
        return {
            id: `slime_${base.id}`,
            name: `${base.name}-Slime`,
            icon: base.icon,
            color: base.color,
            baseMonster: base.id,
            region: startRegion,
            looksExactlyLike: base.name, // Sieht 1:1 aus wie das echte Monster!
        };
    }

    // ==========================================
    // MIMIK FORMEN (NUR für Kuja!)
    // ==========================================
    // Äquivalent zu den Slime-Formen anderer Spieler
    // NUR OPTISCH - keine Stat-Boni! (8 Gebote!)
    // Beim Training wechselt KUJA die Formen (nicht Najika!)

    const MIMIK_FORMS = {
        basis: {
            name: 'Mimik-Basis',
            icon: '🫠',
            description: 'Grundform. Ein schleimiger, formloser Blob.',
            color: '#9C27B0',
            requirement: null, // Startform
        },
        krieger: {
            name: 'Krieger-Mimik',
            icon: '⚔️',
            description: 'Humanoid mit Waffen-Gliedern. Bedrohlich!',
            color: '#F44336',
            requirement: { stat: 'kampf_training', min: 50 },
        },
        schatten: {
            name: 'Schatten-Mimik',
            icon: '🌑',
            description: 'Fast unsichtbar. Perfekt für Spion-Berufe.',
            color: '#212121',
            requirement: { stat: 'stealth_training', min: 30 },
        },
        riese: {
            name: 'Riesen-Mimik',
            icon: '🗿',
            description: 'Massiv und schwer. Ein wandelnder Felsen.',
            color: '#795548',
            requirement: { stat: 'kraft_training', min: 40 },
        },
        fluegel: {
            name: 'Flügel-Mimik',
            icon: '🦅',
            description: 'Geflügelte Form. Schnell und wendig.',
            color: '#03A9F4',
            requirement: { stat: 'geschick_training', min: 35 },
        },
        bestie: {
            name: 'Bestien-Mimik',
            icon: '🐺',
            description: 'Vierbeinige Bestienform. Wild und schnell.',
            color: '#FF9800',
            requirement: { stat: 'wild_training', min: 25 },
        },
        kristall: {
            name: 'Kristall-Mimik',
            icon: '💎',
            description: 'Kristalline Form. Reflektiert Licht und Magie.',
            color: '#E1BEE7',
            requirement: { stat: 'magie_training', min: 45 },
        },
        goettlich: {
            name: 'Göttliche Mimik',
            icon: '✨',
            description: 'Leuchtende, überirdische Form. Nur durch Zeitstadt erreichbar.',
            color: '#FFD700',
            requirement: { stat: 'total_training', min: 200, special: 'zeitstadt_zugang' },
        },
        mensch: {
            name: 'Menschliche Mimik',
            icon: '🧑',
            description: 'Perfekte menschliche Gestalt. Seelenbund erreicht!',
            color: '#FFCCBC',
            requirement: { stat: 'trust_level', min: 6, special: 'seelenbund' },
        },
    };

    // ==========================================
    // SLIME FORMEN (für normale Spieler)
    // ==========================================
    // Entspricht den Mimik-Formen, aber für den Slime-Companion
    // Slime wechselt die Formen, nicht der Spieler!

    const SLIME_FORMS = {
        basis: {
            name: 'Basis-Slime',
            icon: '🟢',
            description: 'Die Startform aus der Region.',
            color: '#4CAF50',
            requirement: null,
        },
        feuer: {
            name: 'Feuer-Slime',
            icon: '🔥',
            description: 'Brennende Aura. Aus Magmaström-Training.',
            color: '#F44336',
            requirement: { stat: 'kampf_training', min: 50 },
        },
        wasser: {
            name: 'Wasser-Slime',
            icon: '💧',
            description: 'Fließende Form. Aus Salzwind-Training.',
            color: '#2196F3',
            requirement: { stat: 'geschick_training', min: 35 },
        },
        erde: {
            name: 'Erd-Slime',
            icon: '🪨',
            description: 'Steinhart. Aus Tiefenhöhlen-Training.',
            color: '#795548',
            requirement: { stat: 'kraft_training', min: 40 },
        },
        schatten: {
            name: 'Schatten-Slime',
            icon: '🌑',
            description: 'Unsichtbar im Dunkeln. Stealth-Training.',
            color: '#212121',
            requirement: { stat: 'stealth_training', min: 30 },
        },
        gift: {
            name: 'Gift-Slime',
            icon: '☠️',
            description: 'Toxisch. Aus Grünschlamm-Training.',
            color: '#7B1FA2',
            requirement: { stat: 'wild_training', min: 25 },
        },
        kristall: {
            name: 'Kristall-Slime',
            icon: '💎',
            description: 'Reflektiert Magie. Aus Magie-Training.',
            color: '#E1BEE7',
            requirement: { stat: 'magie_training', min: 45 },
        },
        heilig: {
            name: 'Heiliger Slime',
            icon: '✨',
            description: 'Göttliche Aura. Zeitstadt-Zugang nötig.',
            color: '#FFD700',
            requirement: { stat: 'total_training', min: 200, special: 'zeitstadt_zugang' },
        },
        menschlich: {
            name: 'Menschliche Form',
            icon: '🧑',
            description: 'Menschengestalt. Seelenbund mit dem Spieler!',
            color: '#FFCCBC',
            requirement: { stat: 'trust_level', min: 6, special: 'seelenbund' },
        },
    };

    // ==========================================
    // STATE MANAGEMENT
    // ==========================================

    let state = loadState();

    function loadState() {
        try {
            return JSON.parse(localStorage.getItem('najika_companion_system') || 'null') || createFreshState();
        } catch { return createFreshState(); }
    }

    function createFreshState() {
        return {
            // Charakter-Erstellung
            characterType: null,          // 'mensch', 'monster', 'mimik'
            chosenMonster: null,           // Wenn monster: welches? z.B. 'duenen_viper'
            startRegion: null,             // z.B. 'heisse_duenen'
            creationComplete: false,

            // Slime-Begleiter (ALLE normalen Spieler)
            slime: {
                form: null,               // Aktuelle Slime-Form
                startForm: null,           // Startform (Region-basiert)
                unlockedForms: ['basis'],
            },

            // Mimik-Formen (NUR Kuja)
            mimikForm: 'basis',
            unlockedMimikForms: ['basis'],

            // Begleiterin (Kuja-Modus: Najika)
            companion: {
                name: null,               // 'Najika' für Kuja, Slime-Name für andere
                type: null,               // 'najika' oder 'slime'
            },

            // Training-Stats (IDENTISCH für alle!)
            trainingStats: {
                kampf_training: 0,
                stealth_training: 0,
                kraft_training: 0,
                geschick_training: 0,
                wild_training: 0,
                magie_training: 0,
                total_training: 0,
                trust_level: 1,
            },

            // V-Pet Stats (identisch für alle!)
            hungerHearts: 4,
            strengthHearts: 4,
            effortHearts: 0,
            careMistakes: 0,
            trainingCount: 0,

            // Evolution
            stage: 1,
            evolutionPath: 'NORMAL',
            birthTime: Date.now(),
            lastFed: Date.now(),
            lastTrained: Date.now(),
            lastPlayed: Date.now(),
        };
    }

    function saveState() {
        localStorage.setItem('najika_companion_system', JSON.stringify(state));
    }

    // ==========================================
    // CHARAKTER-ERSTELLUNG
    // ==========================================

    function createCharacter(characterType, options = {}) {
        if (!CHARACTER_TYPES[characterType]) {
            return { success: false, reason: `Unbekannter Charakter-Typ: ${characterType}` };
        }

        // Mimik ist EXKLUSIV für Kuja
        if (characterType === 'mimik' && !options.isOwner) {
            return { success: false, reason: 'Mimik ist exklusiv für Kuja!' };
        }

        const startRegion = options.startRegion || 'goetterfels';

        state.characterType = characterType;
        state.startRegion = startRegion;

        if (characterType === 'monster') {
            // Spieler wählt ein Monster aus der Spielwelt
            if (!options.monsterId) {
                return { success: false, reason: 'Bitte wähle ein Monster!', availableMonsters: WORLD_MONSTERS[startRegion] };
            }
            state.chosenMonster = options.monsterId;
        }

        if (characterType === 'mimik') {
            // Kuja-Modus: Najika als Begleiterin (KEIN Slime!)
            state.companion = {
                name: 'Najika',
                type: 'najika',    // Najika ist keine Kategorie, einfach Begleiterin
            };
            state.mimikForm = 'basis';
            state.unlockedMimikForms = ['basis'];
        } else {
            // Alle anderen: Slime-Begleiter aus der Startregion
            const slimeForm = getStartingSlimeForm(startRegion);
            state.slime = {
                form: slimeForm,
                startForm: slimeForm,
                unlockedForms: ['basis'],
            };
            state.companion = {
                name: slimeForm.name,
                type: 'slime',
            };
        }

        state.creationComplete = true;
        saveState();

        if (typeof notify === 'function') {
            const ct = CHARACTER_TYPES[characterType];
            notify(`${ct.icon} Charakter erstellt: ${ct.name}!`, 'success');
            if (state.companion.type === 'slime') {
                notify(`🟢 Slime-Begleiter: ${state.slime.form.name}!`, 'info');
            } else {
                notify(`💥 Begleiterin: Najika!`, 'info');
            }
        }

        return {
            success: true,
            characterType,
            companion: state.companion,
            slimeForm: state.slime?.form || null,
        };
    }

    function isKujaMode() {
        return state.characterType === 'mimik';
    }

    // ==========================================
    // FORMEN-SYSTEM
    // ==========================================
    // Bei normalen Spielern: SLIME wechselt Formen
    // Bei Kuja: KUJA SELBST wechselt Formen (Mimik)

    function changeForm(formId) {
        if (isKujaMode()) {
            return changeMimikForm(formId);
        } else {
            return changeSlimeForm(formId);
        }
    }

    function changeMimikForm(formId) {
        if (!MIMIK_FORMS[formId]) return { success: false, reason: 'Form existiert nicht.' };
        if (!state.unlockedMimikForms.includes(formId)) {
            return { success: false, reason: `"${MIMIK_FORMS[formId].name}" noch nicht freigeschaltet!` };
        }

        state.mimikForm = formId;
        saveState();

        const form = MIMIK_FORMS[formId];
        if (typeof notify === 'function') {
            notify(`${form.icon} Mimik-Form: ${form.name}!`, 'success');
        }
        return { success: true, form, who: 'kuja' };
    }

    function changeSlimeForm(formId) {
        if (!SLIME_FORMS[formId]) return { success: false, reason: 'Form existiert nicht.' };
        if (!state.slime.unlockedForms.includes(formId)) {
            return { success: false, reason: `"${SLIME_FORMS[formId].name}" noch nicht freigeschaltet!` };
        }

        state.slime.form = { ...state.slime.form, ...SLIME_FORMS[formId], id: formId };
        saveState();

        const form = SLIME_FORMS[formId];
        if (typeof notify === 'function') {
            notify(`${form.icon} Slime-Form: ${form.name}!`, 'success');
        }
        return { success: true, form, who: 'slime' };
    }

    function checkFormUnlocks() {
        const stats = state.trainingStats;
        let newUnlocks = [];

        const forms = isKujaMode() ? MIMIK_FORMS : SLIME_FORMS;
        const unlockedList = isKujaMode() ? state.unlockedMimikForms : state.slime.unlockedForms;

        Object.entries(forms).forEach(([formId, form]) => {
            if (unlockedList.includes(formId)) return;
            if (!form.requirement) return;

            const req = form.requirement;
            const currentStat = stats[req.stat] || 0;

            if (currentStat >= req.min) {
                if (req.special) {
                    if (req.special === 'zeitstadt_zugang') {
                        if (localStorage.getItem('zeitstadt_unlocked') !== 'true') return;
                    }
                    if (req.special === 'seelenbund') {
                        if (stats.trust_level < 6) return;
                    }
                }

                unlockedList.push(formId);
                newUnlocks.push(form);

                const who = isKujaMode() ? 'Mimik' : 'Slime';
                if (typeof notify === 'function') {
                    notify(`✨ NEUE ${who.toUpperCase()}-FORM: ${form.icon} ${form.name}!`, 'success');
                }
            }
        });

        if (newUnlocks.length > 0) saveState();
        return newUnlocks;
    }

    function getAvailableForms() {
        if (isKujaMode()) {
            return state.unlockedMimikForms.map(f => ({ id: f, ...MIMIK_FORMS[f] }));
        }
        return state.slime.unlockedForms.map(f => ({ id: f, ...SLIME_FORMS[f] }));
    }

    function getCurrentForm() {
        if (isKujaMode()) {
            return { id: state.mimikForm, ...MIMIK_FORMS[state.mimikForm], who: 'kuja' };
        }
        return { ...state.slime.form, who: 'slime' };
    }

    // ==========================================
    // TRAINING
    // ==========================================
    // Bei normalen Spielern: Spieler trainiert MIT Slime → Slime ändert Formen
    // Bei Kuja: Kuja trainiert MIT Najika → Kuja ändert Formen (optischer Rollentausch!)
    //
    // "Beim Training tauschen wir optisch die Rollen" - Kuja
    // → Bei anderen: Spieler steht da, Slime übt Formen
    // → Bei Kuja: Najika steht da, KUJA übt die Mimik-Formen
    // → Mechanik ist 1:1 IDENTISCH, nur optisch getauscht

    function train(trainingType) {
        state.trainingCount++;
        state.effortHearts++;
        state.strengthHearts = Math.min(4, state.strengthHearts + 1);

        if (state.trainingStats[trainingType] !== undefined) {
            state.trainingStats[trainingType]++;
        }
        state.trainingStats.total_training++;
        state.lastTrained = Date.now();

        const newForms = checkFormUnlocks();
        saveState();

        // Optischer Rollentausch bei Kuja
        const trainingVisual = isKujaMode()
            ? { trainer: 'kuja', observer: 'najika', description: 'Kuja übt Mimik-Formen, Najika beobachtet und gibt Tipps' }
            : { trainer: 'slime', observer: 'player', description: 'Slime übt neue Formen, Spieler trainiert mit' };

        return {
            strengthHearts: state.strengthHearts,
            effortHearts: state.effortHearts,
            newFormsUnlocked: newForms,
            visual: trainingVisual,
        };
    }

    function feed() {
        state.hungerHearts = Math.min(4, state.hungerHearts + 1);
        state.lastFed = Date.now();
        saveState();
        return { hungerHearts: state.hungerHearts };
    }

    function play() {
        state.strengthHearts = Math.min(4, state.strengthHearts + 1);
        state.lastPlayed = Date.now();
        saveState();
        return { strengthHearts: state.strengthHearts };
    }

    // ==========================================
    // EVOLUTION (gleiche Stufen für alle!)
    // ==========================================

    function checkEvolution() {
        const age = (Date.now() - state.birthTime) / 1000;
        const stages = [
            { stage: 6, time: 1209600 },  // 14 Tage
            { stage: 5, time: 604800 },   // 7 Tage
            { stage: 4, time: 259200 },   // 3 Tage
            { stage: 3, time: 86400 },    // 24h
            { stage: 2, time: 3600 },     // 1h
        ];

        for (const s of stages) {
            if (age >= s.time && state.stage < s.stage) {
                return s.stage;
            }
        }
        return null;
    }

    function evolve() {
        const nextStage = checkEvolution();
        if (!nextStage) return { success: false, reason: 'Noch nicht bereit.' };

        state.stage = nextStage;

        const effort = state.effortHearts;
        const mistakes = state.careMistakes;

        if (effort > 50 && mistakes < 3) state.evolutionPath = 'PERFECT';
        else if (effort > 25 && mistakes < 10) state.evolutionPath = 'GOOD';
        else if (mistakes > 20) state.evolutionPath = 'BAD';
        else state.evolutionPath = 'NORMAL';

        saveState();

        const stageNames = ['', 'EGG', 'BABY', 'KIND', 'REIF', 'CHAMPION', 'ULTIMATIV'];
        if (typeof notify === 'function') {
            notify(`✨ EVOLUTION! Stufe ${nextStage}: ${stageNames[nextStage]}! Pfad: ${state.evolutionPath}`, 'success');
        }

        return { success: true, stage: nextStage, path: state.evolutionPath };
    }

    // ==========================================
    // TRUST LEVEL (Seelenbund = Level 6)
    // ==========================================

    function updateTrust() {
        const oldLevel = state.trainingStats.trust_level;
        const totalEffort = state.effortHearts + state.trainingCount;
        const mistakePenalty = state.careMistakes * 5;
        const score = totalEffort - mistakePenalty;

        let newLevel = 1;
        if (score > 500)  newLevel = 6; // SEELENBUND! → Menschenform
        else if (score > 300) newLevel = 5;
        else if (score > 150) newLevel = 4;
        else if (score > 50)  newLevel = 3;
        else if (score > 15)  newLevel = 2;

        state.trainingStats.trust_level = newLevel;

        if (newLevel > oldLevel) {
            const trustNames = ['', 'Fremd', 'Bekannt', 'Freund', 'Vertraut', 'Seelenverwandt', 'SEELENBUND!'];
            if (typeof notify === 'function') {
                notify(`💖 Trust Level ${newLevel}: ${trustNames[newLevel]}!`, 'success');
            }
            if (newLevel === 6 && typeof notify === 'function') {
                const who = isKujaMode() ? 'Menschliche Mimik' : 'Menschliche Slime-Form';
                notify(`🧑 SEELENBUND! ${who} freigeschaltet!`, 'success');
            }
        }

        saveState();
        return newLevel;
    }

    // ==========================================
    // V-PET UPDATE LOOP
    // ==========================================

    function update() {
        const now = Date.now();

        // Hunger verfällt (alle 30 Minuten -1 Heart)
        const minutesSinceFed = (now - state.lastFed) / 60000;
        const heartLoss = Math.floor(minutesSinceFed / 30);
        if (heartLoss > 0) {
            state.hungerHearts = Math.max(0, 4 - heartLoss);
            if (state.hungerHearts === 0) {
                state.careMistakes++;
            }
        }

        updateTrust();
        checkFormUnlocks();
        saveState();
    }

    // ==========================================
    // COMPANION DATA (für UI/3D-Rendering)
    // ==========================================

    function getCompanionData() {
        if (isKujaMode()) {
            return {
                mode: 'kuja',
                character: {
                    type: 'mimik',
                    form: MIMIK_FORMS[state.mimikForm],
                    formId: state.mimikForm,
                    whoChangesForm: 'kuja',   // KUJA wechselt die Formen!
                },
                companion: {
                    name: 'Najika',
                    type: 'begleiterin',       // Einfach Begleiterin, kein Slime!
                    changesForm: false,         // Najika ändert ihre Form NICHT
                },
                training: {
                    description: 'Kuja übt Mimik-Formen, Najika begleitet und gibt Tipps',
                    whoTransforms: 'kuja',
                },
                stage: state.stage,
                path: state.evolutionPath,
                hungerHearts: state.hungerHearts,
                strengthHearts: state.strengthHearts,
                effortHearts: state.effortHearts,
                trustLevel: state.trainingStats.trust_level,
                unlockedForms: state.unlockedMimikForms.map(f => ({ id: f, ...MIMIK_FORMS[f] })),
            };
        }

        // Normaler Spieler
        return {
            mode: 'standard',
            character: {
                type: state.characterType,       // 'mensch' oder 'monster'
                chosenMonster: state.chosenMonster,
                whoChangesForm: 'niemand',         // Spieler-Charakter ändert Form nicht
            },
            companion: {
                name: state.companion.name,
                type: 'slime',
                form: state.slime.form,
                changesForm: true,                 // Der SLIME ändert die Formen!
            },
            training: {
                description: 'Spieler trainiert mit Slime, Slime übt neue Formen',
                whoTransforms: 'slime',
            },
            stage: state.stage,
            path: state.evolutionPath,
            hungerHearts: state.hungerHearts,
            strengthHearts: state.strengthHearts,
            effortHearts: state.effortHearts,
            trustLevel: state.trainingStats.trust_level,
            unlockedForms: (state.slime?.unlockedForms || []).map(f => ({ id: f, ...SLIME_FORMS[f] })),
        };
    }

    // ==========================================
    // FAIRNESS-CHECK (für Debug/Balance)
    // ==========================================

    function fairnessReport() {
        return {
            note: 'ALLE Mechaniken sind identisch!',
            comparison: {
                'Normaler Spieler': {
                    charakter: 'Mensch oder Monster (aus der Welt)',
                    begleiter: 'Slime (Region-basiert)',
                    formenWechsel: 'SLIME wechselt Formen',
                    training: 'Spieler + Slime trainieren zusammen',
                    evolution: 'Gleiche Stufen & Pfade',
                    vpet: 'Gleiche Care-Mechanik',
                },
                'Kuja': {
                    charakter: 'Mimik (EXKLUSIV)',
                    begleiter: 'Najika (Begleiterin, kein Slime)',
                    formenWechsel: 'KUJA wechselt Formen (optischer Rollentausch)',
                    training: 'Kuja + Najika trainieren zusammen',
                    evolution: 'Gleiche Stufen & Pfade',
                    vpet: 'Gleiche Care-Mechanik',
                },
            },
            fazit: 'Einziger Unterschied: WER die Formen wechselt. Gameplay = identisch!',
        };
    }

    // Auto-Update alle 5 Sekunden
    setInterval(update, 5000);

    // ==========================================
    // EXPORT
    // ==========================================

    window.CompanionSystem = {
        // Charakter-Erstellung
        CHARACTER_TYPES,
        WORLD_MONSTERS,
        createCharacter,
        isKujaMode,
        isCreated: () => state.creationComplete,

        // Formen (für beide Modi!)
        MIMIK_FORMS,
        SLIME_FORMS,
        changeForm,           // Automatisch Mimik oder Slime
        checkFormUnlocks,
        getAvailableForms,
        getCurrentForm,

        // V-Pet (identisch für alle!)
        train,
        feed,
        play,
        evolve,
        checkEvolution,

        // Trust
        updateTrust,
        getTrustLevel: () => state.trainingStats.trust_level,

        // Daten
        getCompanionData,
        fairnessReport,

        // State
        getState: () => ({ ...state }),
        saveState,
    };

    // Auch unter altem Namen exportieren für Kompatibilität
    window.CompanionSwap = window.CompanionSystem;

    // Log
    if (state.creationComplete) {
        const ct = CHARACTER_TYPES[state.characterType];
        console.log(`🎮 Character & Companion System geladen!`);
        console.log(`   Charakter: ${ct?.icon || '?'} ${ct?.name || state.characterType}`);
        console.log(`   Begleiter: ${state.companion.name} (${state.companion.type})`);
        if (isKujaMode()) {
            const form = MIMIK_FORMS[state.mimikForm];
            console.log(`   Mimik-Form: ${form.icon} ${form.name}`);
            console.log(`   ${state.unlockedMimikForms.length}/${Object.keys(MIMIK_FORMS).length} Formen freigeschaltet`);
        } else if (state.slime) {
            console.log(`   Slime: ${state.slime.form?.name || 'Basis'}`);
            console.log(`   ${state.slime.unlockedForms.length}/${Object.keys(SLIME_FORMS).length} Formen freigeschaltet`);
        }
    } else {
        console.log(`🎮 Character & Companion System geladen! (Charakter noch nicht erstellt)`);
    }

})();
