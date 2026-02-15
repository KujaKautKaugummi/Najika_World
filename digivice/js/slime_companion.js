/**
 * NAJIKA WORLD - SLIME COMPANION SYSTEM V3
 * =========================================
 * FORMWANDLER + AURA + VERTRAUEN + ERINNERUNGEN
 *
 * V3 KOMPLETT NEU - V2 war FALSCH!
 * ❌ ENTFERNT: Evolution-Stufen, Synthese, +N System, Effort Hearts, Care Mistakes
 * ✅ NEU: Formwandler, Aura (0-5), Vertrauen (0-6), Form-Lernen, Erinnerungen
 *
 * Inspirationen: Digimon V-Pet (Pflege) + Fortnite (Begleiter) + Formwandler-Fantasy
 *
 * Backend API Endpoints (V3):
 * - POST /api/slime/status        - Slime-Status laden
 * - POST /api/slime/feed          - Fuettern
 * - POST /api/slime/play          - Spielen
 * - POST /api/slime/heal          - Heilen
 * - POST /api/slime/change-form   - Form wechseln
 * - POST /api/slime/learn-form    - Form lernen (nach Kampf)
 * - POST /api/slime/human-transform - Menschen-Verwandlung
 * - GET  /api/slime/forms         - Alle gelernten Formen
 * - GET  /api/slime/trust         - Vertrauens-Level
 * - POST /api/slime/rescue/use    - Rescue aktivieren
 */

// =============================================================================
// CONSTANTS & CONFIG (V3)
// =============================================================================

const SLIME_CONFIG = {
    API_BASE: window.API_BASE_URL || 'http://localhost:8001',

    // 8 Regionale Start-Kreaturen
    REGIONAL_FORMS: {
        heisse_duenen:      { name: 'Wuesten-Echse',       icon: '🦎', color: '#FFD54F', region: 'Heisse Duenen',      element: 'Earth',     slimeColor: '🟡' },
        samtmoos_tiefwald:  { name: 'Wald-Wolf',           icon: '🐺', color: '#4CAF50', region: 'Samtmoos-Tiefwald',  element: 'Nature',    slimeColor: '🟢' },
        salzwind_kueste:    { name: 'Wellen-Qualle',       icon: '🌊', color: '#2196F3', region: 'Salzwind-Kueste',    element: 'Water',     slimeColor: '🔵' },
        blitzebene:         { name: 'Blitz-Vogel',         icon: '⚡', color: '#9C27B0', region: 'Blitzebene',         element: 'Lightning', slimeColor: '🟣' },
        gruenschlamm_sumpf: { name: 'Sumpf-Molch',         icon: '🐸', color: '#1B5E20', region: 'Gruenschlamm-Sumpf', element: 'Poison',    slimeColor: '⚫' },
        reich_der_drei:     { name: 'Eis-Hase',            icon: '🐰', color: '#81D4FA', region: 'Reich der Drei',     element: 'Ice',       slimeColor: '⚪' },
        magmastroeme:       { name: 'Vulkan-Salamander',   icon: '🔥', color: '#FF5722', region: 'Magmastroeme',       element: 'Fire',      slimeColor: '🔴' },
        tiefenhoehlen:      { name: 'Kristall-Spinne',     icon: '💎', color: '#E0E0E0', region: 'Tiefenhoehlen',      element: 'Crystal',   slimeColor: '🟤' }
    },

    // Spezial-Formen (Events/Achievements)
    SPECIAL_FORMS: {
        regenbogen_blob:  { name: 'Regenbogen-Blob',  icon: '🌈', color: 'rainbow',  unlock: 'Alle 8 Regional-Formen' },
        koenig_schleim:   { name: 'Koenig-Schleim',    icon: '👑', color: '#FFD700',   unlock: '1000 Kaempfe gewonnen' },
        skelett_form:     { name: 'Skelett-Form',      icon: '💀', color: '#BDBDBD',   unlock: 'Halloween Event' },
        mini_drache:      { name: 'Mini-Drache',       icon: '🐉', color: '#FF6F00',   unlock: 'Drachen-Boss besiegt' }
    },

    // Nutztier-Formen (0.1% Easter Egg!)
    FARM_FORMS: {
        praerie_kuh:   { name: 'Praerie-Kuh',   icon: '🐄', color: '#8D6E63', element: 'Earth' },
        wuesten_huhn:  { name: 'Wuesten-Huhn',  icon: '🐔', color: '#FFB74D', element: 'Earth' },
        eis_schwein:   { name: 'Eis-Schwein',    icon: '🐷', color: '#F48FB1', element: 'Ice' }
    },

    // Form-Affinitaet Boni (FORMEN GEBEN BONI!)
    FORM_AFFINITY: {
        heisse_duenen:      { bonusType: 'Wuesten-Schaden',      baseBonus: 0.10, secondaryType: 'Hitze-Resistenz',        secondaryBonus: 0.15 },
        samtmoos_tiefwald:  { bonusType: 'Wald-Bewegung',        baseBonus: 0.15, secondaryType: 'Faehrten-Findung',       secondaryBonus: 0.10 },
        salzwind_kueste:    { bonusType: 'Schwimm-Speed',        baseBonus: 0.12, secondaryType: 'Fisch-Qualitaet',        secondaryBonus: 0.15 },
        blitzebene:         { bonusType: 'Angriffs-Speed',       baseBonus: 0.10, secondaryType: 'Paralyse-Chance',        secondaryBonus: 0.08 },
        gruenschlamm_sumpf: { bonusType: 'Gift-Resistenz',       baseBonus: 0.15, secondaryType: 'Alchemie-Effektivitaet', secondaryBonus: 0.12 },
        reich_der_drei:     { bonusType: 'Kaelte-Resistenz',     baseBonus: 0.15, secondaryType: 'Eis-Schaden',            secondaryBonus: 0.10 },
        magmastroeme:       { bonusType: 'Feuer-Schaden',        baseBonus: 0.12, secondaryType: 'Schmiede-Bonus',         secondaryBonus: 0.15 },
        tiefenhoehlen:      { bonusType: 'Nacht-Crit',           baseBonus: 0.20, secondaryType: 'Licht-Radius',           secondaryBonus: 0.15 }
    },

    // Aura Stufen (0-5) - skaliert Form-Boni
    AURA_LEVELS: {
        0: { name: 'Keine',      multiplier: 1.00, fights: 0,    visual: 'Normal' },
        1: { name: 'Schwach',    multiplier: 1.05, fights: 10,   visual: 'Leichtes Leuchten' },
        2: { name: 'Mittel',     multiplier: 1.10, fights: 50,   visual: 'Deutliche Aura' },
        3: { name: 'Stark',      multiplier: 1.20, fights: 200,  visual: 'Aura + Partikel' },
        4: { name: 'Legendaer',  multiplier: 1.35, fights: 1000, visual: 'Epische Aura' },
        5: { name: 'Goettlich',  multiplier: 1.50, fights: -1,   visual: 'Strahlend' }  // Spezial-Achievement
    },

    // 13 Element-Auras
    ELEMENT_AURAS: {
        flammen:    { name: 'Flammen-Aura',    icon: '🔥', effect: '+Feuer-Schaden, -Eis-Resist',          training: 'Feuer' },
        frost:      { name: 'Frost-Aura',      icon: '❄️', effect: '+Slow-Effekt, Eisruestung',            training: 'Eis' },
        schatten:   { name: 'Schatten-Aura',    icon: '🌑', effect: '+Crit, +Stealth',                      training: 'Schatten' },
        heilig:     { name: 'Heilig-Aura',      icon: '✨', effect: '+Heilung, +Anti-Undead',                training: 'Licht' },
        explosion:  { name: 'Explosion-Aura',   icon: '💥', effect: '1x/Tag BOOM! (Megumin!)',              training: 'INT 25+' },
        metall:     { name: 'Metall-Aura',      icon: '🛡️', effect: 'Immun <10 DMG',                       training: 'DEF' },
        natur:      { name: 'Natur-Aura',       icon: '🌿', effect: '+HoT, +Gift-Resist',                   training: 'Natur' },
        blitz:      { name: 'Blitz-Aura',       icon: '⚡', effect: '+Speed, Paralyse',                     training: 'Blitz' },
        wasser:     { name: 'Wasser-Aura',      icon: '💧', effect: '+Swim, Wasseratmung',                  training: 'Wasser' },
        gift:       { name: 'Gift-Aura',        icon: '☠️', effect: '+DoT, Gift-Immun',                     training: 'Gift' },
        kristall:   { name: 'Kristall-Aura',    icon: '💎', effect: 'Magic Reflect, Licht',                  training: 'Kristall' },
        sand:       { name: 'Sand-Aura',        icon: '🏜️', effect: '+Evasion, Graben',                    training: 'Sand' },
        goettliche: { name: 'Goettliche-Aura',  icon: '🌈', effect: 'ALLE kombiniert!',                     training: 'ALLE Max' }
    },

    // Vertrauens-Level (0-6)
    TRUST_LEVELS: {
        0: { name: 'Fremd',       points: 0,    effect: 'Folgt zoegerlich' },
        1: { name: 'Bekannt',     points: 51,   effect: 'Normale Loyalitaet' },
        2: { name: 'Freund',      points: 151,  effect: 'Bessere Kampf-AI' },
        3: { name: 'Vertraut',    points: 301,  effect: 'Spezial-Moves, schuetzt aktiv' },
        4: { name: 'Familie',     points: 501,  effect: 'Opfert sich, Rescue ohne CD' },
        5: { name: 'Seelenbund',  points: 801,  effect: 'Menschen-Form moeglich!' }
    },

    // Form-Lern-Chancen
    FORM_LEARN_CHANCES: {
        voelker: 0.02,    // 2% - organisierte Kreaturen
        wild: 0.008,      // 0.8% - einzelne Monster
        nutztier: 0.001   // 0.1% - Easter Egg!
    },

    // Skill Copy Chancen (getrennt von Form-Lernen)
    SKILL_COPY_CHANCE: { min: 0.01, max: 0.05 },
    MAX_SKILLS: 20,

    // Pflege
    HUNGER_DECAY: 3600000,    // 60 Min = 1 Herz verloren
    MAX_HUNGER_HEARTS: 4,
    RESCUE_COOLDOWN: 86400000, // 24h

    // Update
    UPDATE_INTERVAL: 5000,

    // Erinnerungs-System
    MEMORY_MILESTONES: {
        1: 'Ich bin kein normales Monster...',
        3: 'Ich erinnere mich... an andere Formen...',
        5: 'Diese Welt... ich war schon ueberall...',
        8: 'Volle Erinnerung wiederhergestellt!'
    }
};

// =============================================================================
// SLIME COMPANION CLASS (V3 - FORMWANDLER)
// =============================================================================

class SlimeCompanion {
    constructor() {
        // Basic Info
        this.id = null;
        this.name = 'Schleim';
        this.currentForm = null;         // Key aus REGIONAL_FORMS / SPECIAL_FORMS / FARM_FORMS
        this.startRegion = null;         // Wo der Slime gefunden wurde

        // Formwandler
        this.learnedForms = [];          // Array von Form-Keys die gelernt wurden
        this.formChangesSeason = 0;      // Wie oft in dieser Saison gewechselt
        this.currentSeason = 1;
        this.isAtHome = false;           // In Schwarzer Muehle = unbegrenzt wechseln

        // Aura System (statt Evolution!)
        this.auraLevel = 0;              // 0-5
        this.elementAura = null;         // Key aus ELEMENT_AURAS
        this.totalFights = 0;

        // Vertrauen (0-6 Level, Punkte-basiert)
        this.trustPoints = 0;
        this.trustLevel = 0;

        // V-Pet Pflege (VEREINFACHT - nur Hunger!)
        this.hungerHearts = SLIME_CONFIG.MAX_HUNGER_HEARTS;
        this.lastFed = Date.now();

        // Companion-Modus
        this.companionMode = 'physical'; // 'physical' oder 'aura'

        // Skills (getrennt von Formen!)
        this.skills = ['tackle'];
        this.maxSkills = SLIME_CONFIG.MAX_SKILLS;

        // Erinnerungs-System
        this.memoriesUnlocked = 0;
        this.memoryLog = [];
        this.thinksItIsMonster = true;   // Anfangs denkt es, es IST das Monster

        // Menschen-Form
        this.humanFormUnlocked = false;
        this.isInHumanForm = false;

        // Rescue System
        this.rescueCharges = 1;
        this.lastRescueUsed = null;

        // Battle Stats
        this.battles = 0;
        this.wins = 0;

        // Timestamps
        this.birthTime = Date.now();
        this.lastPlayed = Date.now();

        // State
        this.isSleeping = false;
        this.isAlive = true;

        // Position (follows player)
        this.position = { x: 0, y: 0, z: 0 };

        // UI State
        this.uiVisible = true;
        this._uiElement = null;

        console.log('🐾 Slime Companion System V3 (Formwandler) initialized');
    }

    // =========================================================================
    // TRUST SYSTEM
    // =========================================================================

    addTrust(points, reason) {
        this.trustPoints += points;
        if (this.trustPoints < 0) this.trustPoints = 0;

        const oldLevel = this.trustLevel;
        this.trustLevel = this._calculateTrustLevel();

        if (this.trustLevel > oldLevel) {
            const lvlData = SLIME_CONFIG.TRUST_LEVELS[this.trustLevel];
            this.showNotification(`💕 Vertrauen gestiegen! Level ${this.trustLevel}: ${lvlData.name}`, 5000);

            // Level 5 = Menschen-Form Quest trigger
            if (this.trustLevel >= 5 && !this.humanFormUnlocked) {
                this.showNotification('✨ Quest freigeschaltet: "Wunsch der Seele" - Menschen-Form moeglich!', 8000);
            }
        }

        if (reason) {
            console.log(`💕 Trust ${points > 0 ? '+' : ''}${points}: ${reason} (Total: ${this.trustPoints})`);
        }
    }

    _calculateTrustLevel() {
        const levels = SLIME_CONFIG.TRUST_LEVELS;
        let level = 0;
        for (let i = 5; i >= 0; i--) {
            if (this.trustPoints >= levels[i].points) {
                level = i;
                break;
            }
        }
        return level;
    }

    // =========================================================================
    // FORM SYSTEM (Formwandler)
    // =========================================================================

    tryLearnForm(enemyType, source = 'wild') {
        // Bestimme Chance basierend auf Quelle
        let baseChance = SLIME_CONFIG.FORM_LEARN_CHANCES[source] || SLIME_CONFIG.FORM_LEARN_CHANCES.wild;

        // Modifiers
        baseChance += this.trustLevel * 0.001;   // +0.1% pro Trust-Level
        // Slime hatte den Kill? Wird vom Aufrufer gesetzt
        // Seltener Typ? Wird vom Aufrufer gesetzt

        if (Math.random() < baseChance) {
            return this._learnForm(enemyType);
        }
        return false;
    }

    _learnForm(formKey) {
        if (this.learnedForms.includes(formKey)) return false;

        this.learnedForms.push(formKey);
        const formData = this._getFormData(formKey);
        const formName = formData ? formData.name : formKey;

        this.showNotification(`✨ NEUE FORM GELERNT! "${formName}" absorbiert!`, 6000);

        // Erinnerungs-System triggern
        this._checkMemoryMilestone();

        return true;
    }

    changeForm(formKey) {
        if (!this.learnedForms.includes(formKey) && formKey !== this.currentForm) {
            this.showNotification('⚠️ Diese Form wurde noch nicht gelernt!', 3000);
            return false;
        }

        // Im Spiel: 1x pro Saison
        if (!this.isAtHome) {
            if (this.formChangesSeason >= 1) {
                this.showNotification('⚠️ Form-Wechsel nur 1x pro Saison im Spiel! (Zuhause: unbegrenzt)', 4000);
                return false;
            }
            this.formChangesSeason++;
        }

        this.currentForm = formKey;
        this.showNotification(`🔄 Form gewechselt: ${this._getFormData(formKey)?.name || formKey}`, 3000);
        return true;
    }

    getFormAffinity() {
        if (!this.currentForm) return null;
        const affinity = SLIME_CONFIG.FORM_AFFINITY[this.currentForm];
        if (!affinity) return null;

        const auraMultiplier = SLIME_CONFIG.AURA_LEVELS[this.auraLevel].multiplier;
        return {
            primary: {
                type: affinity.bonusType,
                value: affinity.baseBonus * auraMultiplier
            },
            secondary: {
                type: affinity.secondaryType,
                value: affinity.secondaryBonus * auraMultiplier
            },
            auraMultiplier
        };
    }

    _getFormData(formKey) {
        return SLIME_CONFIG.REGIONAL_FORMS[formKey] ||
               SLIME_CONFIG.SPECIAL_FORMS[formKey] ||
               SLIME_CONFIG.FARM_FORMS[formKey] ||
               null;
    }

    getAllLearnedFormsData() {
        return this.learnedForms.map(key => ({
            key,
            ...this._getFormData(key)
        })).filter(f => f.name);
    }

    // =========================================================================
    // MEMORY / ERINNERUNGS-SYSTEM
    // =========================================================================

    _checkMemoryMilestone() {
        const formsCount = this.learnedForms.length;
        const milestones = SLIME_CONFIG.MEMORY_MILESTONES;

        for (const [count, message] of Object.entries(milestones)) {
            if (formsCount >= parseInt(count) && this.memoriesUnlocked < parseInt(count)) {
                this.memoriesUnlocked = parseInt(count);

                if (parseInt(count) === 1) {
                    this.thinksItIsMonster = false;
                }

                this.memoryLog.push({
                    timestamp: Date.now(),
                    formsAtTime: formsCount,
                    message
                });

                this.showNotification(`🧠 Erinnerung: "${message}"`, 8000);

                // Alle 8 Regional-Formen = volle Erinnerung
                if (parseInt(count) === 8) {
                    this.showNotification('🌈 VOLLE ERINNERUNG! Original-Form kann jetzt frei gestaltet werden!', 10000);
                }
            }
        }
    }

    // =========================================================================
    // AURA SYSTEM
    // =========================================================================

    updateAura() {
        const oldLevel = this.auraLevel;
        const levels = SLIME_CONFIG.AURA_LEVELS;

        for (let i = 4; i >= 0; i--) {
            if (this.totalFights >= levels[i].fights) {
                this.auraLevel = i;
                break;
            }
        }
        // Level 5 = Spezial-Achievement (nicht kaempfe-basiert)

        if (this.auraLevel > oldLevel) {
            const lvl = levels[this.auraLevel];
            this.showNotification(`✨ Aura aufgestiegen! Stufe ${this.auraLevel}: ${lvl.name} (${lvl.visual})`, 6000);
        }
    }

    setElementAura(auraKey) {
        if (!SLIME_CONFIG.ELEMENT_AURAS[auraKey]) return false;
        this.elementAura = auraKey;
        const aura = SLIME_CONFIG.ELEMENT_AURAS[auraKey];
        this.showNotification(`${aura.icon} ${aura.name} freigeschaltet! ${aura.effect}`, 5000);
        return true;
    }

    // =========================================================================
    // COMPANION MODE
    // =========================================================================

    setCompanionMode(mode) {
        if (mode !== 'physical' && mode !== 'aura') return false;
        this.companionMode = mode;
        if (mode === 'physical') {
            this.showNotification('🐾 Koerperlicher Modus: Slime reist physisch mit dir!', 3000);
        } else {
            this.showNotification('✨ Aura-Modus: Slime wird zu deiner Aura! (+Buffs, kein physischer Kampf)', 3000);
        }
        return true;
    }

    // =========================================================================
    // HUMAN TRANSFORM
    // =========================================================================

    unlockHumanForm() {
        if (this.trustLevel < 5) {
            this.showNotification('⚠️ Vertrauen Level 5 (Seelenbund) benoetigt!', 3000);
            return false;
        }
        this.humanFormUnlocked = true;
        this.showNotification('👤 Menschen-Form freigeschaltet! Dein Slime kann jetzt menschliche Gestalt annehmen!', 8000);
        return true;
    }

    toggleHumanForm() {
        if (!this.humanFormUnlocked) {
            this.showNotification('⚠️ Menschen-Form noch nicht freigeschaltet!', 3000);
            return false;
        }
        this.isInHumanForm = !this.isInHumanForm;
        if (this.isInHumanForm) {
            this.showNotification(`👤 ${this.name} nimmt menschliche Gestalt an!`, 4000);
        } else {
            this.showNotification(`🐾 ${this.name} kehrt zur Slime-Form zurueck.`, 3000);
        }
        return true;
    }

    // =========================================================================
    // PFLEGE (vereinfacht - nur Hunger!)
    // =========================================================================

    async feed() {
        if (!this.id) return;
        try {
            const response = await fetch(`${SLIME_CONFIG.API_BASE}/api/slime/feed`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ slime_id: this.id })
            });
            if (response.ok) {
                const data = await response.json();
                if (data.success) {
                    this.hungerHearts = Math.min(SLIME_CONFIG.MAX_HUNGER_HEARTS, this.hungerHearts + 1);
                    this.lastFed = Date.now();
                    this.addTrust(1, 'Fuettern');
                    this.showNotification(`🍖 ${this.name} wurde gefuettert!`, 2000);
                } else {
                    this.showNotification(`⚠️ ${data.message}`, 2000);
                }
            }
        } catch (error) {
            // Offline-Fallback
            this.hungerHearts = Math.min(SLIME_CONFIG.MAX_HUNGER_HEARTS, this.hungerHearts + 1);
            this.lastFed = Date.now();
            this.addTrust(1, 'Fuettern (offline)');
            this.showNotification(`🍖 ${this.name} wurde gefuettert!`, 2000);
        }
    }

    async play() {
        if (!this.id) return;
        try {
            const response = await fetch(`${SLIME_CONFIG.API_BASE}/api/slime/play`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ slime_id: this.id })
            });
            if (response.ok) {
                const data = await response.json();
                if (data.success) {
                    this.lastPlayed = Date.now();
                    this.addTrust(2, 'Spielen');
                    this.showNotification(`😊 ${this.name} hat gespielt!`, 2000);
                } else {
                    this.showNotification(`⚠️ ${data.message}`, 2000);
                }
            }
        } catch (error) {
            this.lastPlayed = Date.now();
            this.addTrust(2, 'Spielen (offline)');
            this.showNotification(`😊 ${this.name} hat gespielt!`, 2000);
        }
    }

    async heal() {
        if (!this.id) return;
        try {
            const response = await fetch(`${SLIME_CONFIG.API_BASE}/api/slime/heal`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ slime_id: this.id })
            });
            if (response.ok) {
                const data = await response.json();
                if (data.success) {
                    this.addTrust(3, 'Heilen');
                    this.showNotification(`💊 ${this.name} wurde geheilt!`, 2000);
                }
            }
        } catch (error) {
            this.addTrust(3, 'Heilen (offline)');
            this.showNotification(`💊 ${this.name} wurde geheilt!`, 2000);
        }
    }

    sleep() {
        this.isSleeping = true;
        this.hungerHearts = SLIME_CONFIG.MAX_HUNGER_HEARTS;
        this.showNotification(`💤 ${this.name} schlaeft... (HP & Hearts regenerieren)`, 3000);
    }

    wake() {
        this.isSleeping = false;
        this.showNotification(`☀️ ${this.name} ist aufgewacht!`, 2000);
    }

    // =========================================================================
    // RESCUE SYSTEM
    // =========================================================================

    canUseRescue() {
        if (this.rescueCharges <= 0) return false;

        // Trust Level 4+ (Familie) = kein Cooldown!
        if (this.trustLevel >= 4) return true;

        if (this.lastRescueUsed) {
            const timeSince = Date.now() - this.lastRescueUsed;
            return timeSince >= SLIME_CONFIG.RESCUE_COOLDOWN;
        }
        return true;
    }

    useRescue() {
        if (!this.canUseRescue()) return false;

        this.rescueCharges--;
        this.lastRescueUsed = Date.now();

        this.showNotification('💖 RETTUNG! Dein Slime hat sich geopfert - du ueberlebst mit 1 HP!', 8000);

        if (window.realtimeCombat) {
            window.realtimeCombat.rescueActivated();
        }

        // Rescue = +10 Trust
        this.addTrust(10, 'Rettung');

        return true;
    }

    getRescueCooldownRemaining() {
        if (this.trustLevel >= 4) return 0; // Kein Cooldown bei Familie+
        if (!this.lastRescueUsed) return 0;
        const remaining = SLIME_CONFIG.RESCUE_COOLDOWN - (Date.now() - this.lastRescueUsed);
        return Math.max(0, remaining);
    }

    // =========================================================================
    // SKILL COPY (getrennt von Form-Lernen!)
    // =========================================================================

    tryLearnSkill(enemySkill) {
        if (this.skills.length >= this.maxSkills) return false;
        if (this.skills.includes(enemySkill.name || enemySkill)) return false;

        const chance = SLIME_CONFIG.SKILL_COPY_CHANCE.min +
                       Math.random() * (SLIME_CONFIG.SKILL_COPY_CHANCE.max - SLIME_CONFIG.SKILL_COPY_CHANCE.min);

        if (Math.random() < chance) {
            const skillName = enemySkill.name || enemySkill;
            this.skills.push(skillName);
            this.showNotification(`📚 ${this.name} lernte "${skillName}"!`, 4000);
            return true;
        }
        return false;
    }

    forgetSkill(skillName) {
        const idx = this.skills.indexOf(skillName);
        if (idx > 0) { // Index 0 = tackle, nicht vergessen
            this.skills.splice(idx, 1);
            this.showNotification(`📚 ${this.name} hat "${skillName}" vergessen.`, 3000);
            return true;
        }
        return false;
    }

    // =========================================================================
    // BATTLE TRACKING
    // =========================================================================

    recordBattle(won) {
        this.battles++;
        this.totalFights++;
        if (won) {
            this.wins++;
            this.addTrust(1, 'Kampf gewonnen');
        }
        this.updateAura();
    }

    // =========================================================================
    // API CALLS
    // =========================================================================

    async loadFromBackend() {
        try {
            const response = await fetch(`${SLIME_CONFIG.API_BASE}/api/slime/status`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            if (response.ok) {
                const data = await response.json();
                if (data.slime) {
                    this.fromJSON(data.slime);
                    console.log('✅ Slime V3 loaded from backend');
                }
            }
        } catch (error) {
            console.debug('Slime backend nicht erreichbar - Offline-Modus');
            this._loadFromLocalStorage();
        }
    }

    async createNewSlime(regionKey, name) {
        const formData = SLIME_CONFIG.REGIONAL_FORMS[regionKey];
        if (!formData) {
            console.error('Unknown region:', regionKey);
            return;
        }

        this.id = 'slime_' + Date.now();
        this.name = name || formData.name;
        this.currentForm = regionKey;
        this.startRegion = regionKey;
        this.learnedForms = [regionKey];
        this.birthTime = Date.now();
        this.thinksItIsMonster = true;
        this.trustPoints = 0;
        this.trustLevel = 0;
        this.auraLevel = 0;

        this.showNotification(`🐾 ${this.name} ist dein Begleiter! (${formData.name} aus ${formData.region})`, 6000);

        try {
            await fetch(`${SLIME_CONFIG.API_BASE}/api/slime/create`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(this.toJSON())
            });
        } catch (e) {
            console.debug('Backend nicht erreichbar - lokal gespeichert');
        }

        this._saveToLocalStorage();
        this.createUI();
    }

    // =========================================================================
    // UI (V3 - komplett neu)
    // =========================================================================

    createUI() {
        let ui = document.getElementById('slime-companion-ui');
        if (!ui) {
            ui = document.createElement('div');
            ui.id = 'slime-companion-ui';
            document.body.appendChild(ui);
        }
        this._uiElement = ui;

        if (!this.uiVisible) { ui.style.display = 'none'; return; }
        ui.style.display = 'block';

        // Kein Slime? Zeige Erstellungs-UI
        if (!this.id) {
            this._renderCreateUI(ui);
            return;
        }

        this._renderMainUI(ui);
    }

    _renderCreateUI(ui) {
        const regions = SLIME_CONFIG.REGIONAL_FORMS;
        let buttons = '';
        for (const [key, data] of Object.entries(regions)) {
            buttons += `<button onclick="window.slimeCompanion.createNewSlime('${key}', '${data.name}')"
                style="background:${data.color}22; border:1px solid ${data.color}; padding:8px; border-radius:8px;
                color:white; cursor:pointer; font-size:11px; font-family:inherit;">
                ${data.icon} ${data.name}</button>`;
        }

        ui.innerHTML = `
            <div style="position:fixed; bottom:120px; left:20px; background:rgba(10,10,30,0.95);
                border:2px solid #00E676; border-radius:12px; padding:20px; color:white;
                font-family:'Courier New',monospace; z-index:500; min-width:280px; max-width:320px;">
                <button style="position:absolute;top:8px;right:8px;background:none;border:none;
                    color:#ff4444;font-size:20px;cursor:pointer;" onclick="window.slimeCompanion.toggleUI()">×</button>
                <h3 style="margin:0 0 12px 0;color:#00E676;">🐾 SLIME BEGLEITER (V3)</h3>
                <p style="font-size:11px;color:#aaa;margin-bottom:12px;">
                    Waehle deine Start-Region! Dein Slime nimmt die Kreatur-Form dieser Region an.
                </p>
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:6px;">
                    ${buttons}
                </div>
            </div>`;
    }

    _renderMainUI(ui) {
        const formData = this._getFormData(this.currentForm) || { name: 'Blob', icon: '🟢', color: '#4CAF50' };
        const auraData = SLIME_CONFIG.AURA_LEVELS[this.auraLevel];
        const trustData = SLIME_CONFIG.TRUST_LEVELS[this.trustLevel];
        const rescueReady = this.canUseRescue();
        const rescueCd = this.getRescueCooldownRemaining();
        const rescueStr = rescueCd > 0
            ? `${Math.floor(rescueCd / 3600000)}h ${Math.floor((rescueCd % 3600000) / 60000)}m`
            : 'BEREIT!';

        const affinity = this.getFormAffinity();
        let affinityStr = '';
        if (affinity) {
            affinityStr = `<div style="font-size:10px;color:#aaa;padding:4px 8px;background:rgba(0,0,0,0.3);border-radius:6px;margin-bottom:6px;">
                📊 ${affinity.primary.type}: +${(affinity.primary.value * 100).toFixed(1)}% |
                ${affinity.secondary.type}: +${(affinity.secondary.value * 100).toFixed(1)}%
                ${affinity.auraMultiplier > 1 ? `<span style="color:#FFD700;">(Aura ×${affinity.auraMultiplier})</span>` : ''}
            </div>`;
        }

        const auraStars = '★'.repeat(this.auraLevel) + '☆'.repeat(5 - this.auraLevel);
        const modeIcon = this.companionMode === 'physical' ? '🐾' : '✨';
        const modeLabel = this.companionMode === 'physical' ? 'Koerperlich' : 'Aura';
        const memoryIcon = this.thinksItIsMonster ? '❓' : `📚 ${this.memoriesUnlocked}/8`;

        const elementAuraStr = this.elementAura
            ? `${SLIME_CONFIG.ELEMENT_AURAS[this.elementAura].icon} ${SLIME_CONFIG.ELEMENT_AURAS[this.elementAura].name}`
            : 'Keine';

        ui.innerHTML = `
            <div style="position:fixed; bottom:120px; left:20px; background:linear-gradient(135deg,rgba(0,0,0,0.95),rgba(30,30,30,0.95));
                border:2px solid ${formData.color}; border-radius:15px; padding:15px; color:white;
                font-family:'Courier New',monospace; z-index:500; min-width:270px; max-width:310px;
                box-shadow:0 8px 32px rgba(0,0,0,0.8);">

                <button style="position:absolute;top:8px;right:8px;background:rgba(255,255,255,0.1);
                    border:none;color:white;width:20px;height:20px;border-radius:50%;cursor:pointer;font-size:12px;"
                    onclick="window.slimeCompanion.toggleUI()">×</button>

                <!-- Header -->
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;padding-bottom:8px;
                    border-bottom:1px solid ${formData.color}40;">
                    <div style="font-size:36px;filter:drop-shadow(0 0 8px ${formData.color});">
                        ${this.isInHumanForm ? '👤' : formData.icon}
                    </div>
                    <div style="flex:1;">
                        <div style="font-weight:bold;color:${formData.color};font-size:14px;">${formData.icon} ${this.name}</div>
                        <div style="font-size:10px;color:#888;">Form: ${formData.name} | ${modeIcon} ${modeLabel}</div>
                        <div style="font-size:10px;color:#888;">✨ Aura: ${auraStars} ${auraData.name}</div>
                    </div>
                </div>

                <!-- Form-Affinitaet Boni -->
                ${affinityStr}

                <!-- Hunger Hearts -->
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                    <span style="font-size:11px;color:#aaa;">❤️ Hunger</span>
                    <span>${'❤️'.repeat(this.hungerHearts)}${'🖤'.repeat(SLIME_CONFIG.MAX_HUNGER_HEARTS - this.hungerHearts)}</span>
                </div>

                <!-- Vertrauen -->
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                    <span style="font-size:11px;color:#aaa;">💕 Vertrauen</span>
                    <span style="font-size:11px;color:#E91E63;">Lv.${this.trustLevel} ${trustData.name} (${this.trustPoints})</span>
                </div>

                <!-- Stats Row -->
                <div style="display:flex;gap:8px;font-size:10px;color:#aaa;margin-bottom:8px;padding:6px;
                    background:rgba(0,0,0,0.3);border-radius:6px;">
                    <span>📚 Skills: ${this.skills.length}/${this.maxSkills}</span>
                    <span>🔄 Formen: ${this.learnedForms.length}</span>
                    <span>${memoryIcon}</span>
                </div>

                <!-- Element-Aura -->
                <div style="font-size:10px;color:#aaa;margin-bottom:6px;">
                    Element-Aura: ${elementAuraStr}
                </div>

                <!-- Rescue -->
                <div style="background:${rescueReady ? 'rgba(76,175,80,0.15)' : 'rgba(255,0,0,0.1)'};
                    border:1px solid ${rescueReady ? '#4CAF5080' : '#ff444480'};
                    padding:6px;border-radius:6px;font-size:11px;margin-bottom:8px;">
                    <span style="color:${rescueReady ? '#4CAF50' : '#ff6666'};font-weight:bold;">
                        💖 Rescue: ${this.rescueCharges}/1
                    </span>
                    <span style="color:#888;font-size:10px;margin-left:8px;">${rescueStr}</span>
                    ${this.trustLevel >= 4 ? '<span style="color:#FFD700;font-size:9px;"> (Kein CD: Familie!)</span>' : ''}
                </div>

                <!-- Buttons -->
                <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:5px;">
                    <button onclick="window.slimeCompanion.feed()" style="${this._btnStyle(formData.color)}">🍖 Fuettern</button>
                    <button onclick="window.slimeCompanion.play()" style="${this._btnStyle(formData.color)}">😊 Spielen</button>
                    <button onclick="window.slimeCompanion.heal()" style="${this._btnStyle(formData.color)}">💊 Heilen</button>
                    <button onclick="window.slimeCompanion.showFormDialog()" style="${this._btnStyle(formData.color)}">🔄 Formen</button>
                    ${this.humanFormUnlocked ? `<button onclick="window.slimeCompanion.toggleHumanForm()"
                        style="${this._btnStyle('#E91E63')}">👤 ${this.isInHumanForm ? 'Slime-Form' : 'Menschen-Form'}</button>` : ''}
                    <button onclick="window.slimeCompanion.toggleCompanionMode()"
                        style="${this._btnStyle(formData.color)}">${this.companionMode === 'physical' ? '✨ Aura-Modus' : '🐾 Koerperlich'}</button>
                </div>
            </div>`;
    }

    _btnStyle(color) {
        return `background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.2);
            border-radius:6px;padding:7px;color:white;font-size:11px;cursor:pointer;
            font-family:'Courier New',monospace;transition:all 0.2s;`;
    }

    // =========================================================================
    // FORM DIALOG
    // =========================================================================

    showFormDialog() {
        const existing = document.getElementById('slime-form-dialog');
        if (existing) { existing.remove(); return; }

        const dialog = document.createElement('div');
        dialog.id = 'slime-form-dialog';

        let formButtons = '';
        for (const key of this.learnedForms) {
            const data = this._getFormData(key);
            if (!data) continue;
            const isCurrent = key === this.currentForm;
            formButtons += `<button onclick="window.slimeCompanion.changeForm('${key}'); document.getElementById('slime-form-dialog').remove();"
                style="display:flex;align-items:center;gap:8px;width:100%;padding:8px;
                background:${isCurrent ? 'rgba(76,175,80,0.3)' : 'rgba(255,255,255,0.05)'};
                border:1px solid ${isCurrent ? '#4CAF50' : 'rgba(255,255,255,0.15)'};
                border-radius:8px;color:white;cursor:pointer;font-family:inherit;font-size:12px;text-align:left;">
                <span style="font-size:20px;">${data.icon}</span>
                <span>${data.name} ${isCurrent ? '(aktiv)' : ''}</span>
            </button>`;
        }

        const seasonWarning = !this.isAtHome && this.formChangesSeason >= 1
            ? '<div style="color:#ff6666;font-size:10px;margin-top:8px;">⚠️ Saisonwechsel aufgebraucht! Geh nach Hause fuer unbegrenzten Wechsel.</div>'
            : '';

        dialog.innerHTML = `
            <div style="position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);
                background:rgba(10,10,30,0.98);border:2px solid #FFD700;border-radius:15px;
                padding:20px;color:white;font-family:'Courier New',monospace;z-index:1000;
                min-width:300px;max-width:350px;max-height:70vh;overflow-y:auto;">
                <button onclick="document.getElementById('slime-form-dialog').remove()"
                    style="position:absolute;top:8px;right:8px;background:none;border:none;
                    color:#ff4444;font-size:20px;cursor:pointer;">×</button>
                <h3 style="margin:0 0 12px 0;color:#FFD700;">🔄 FORM WAEHLEN</h3>
                <p style="font-size:10px;color:#aaa;margin-bottom:12px;">
                    Formen geben Affinitaets-Boni! Im Spiel: 1x/Saison. Zuhause: unbegrenzt.
                </p>
                <div style="display:flex;flex-direction:column;gap:6px;">
                    ${formButtons}
                </div>
                ${seasonWarning}
            </div>`;

        document.body.appendChild(dialog);
    }

    // =========================================================================
    // COMPANION MODE TOGGLE
    // =========================================================================

    toggleCompanionMode() {
        this.setCompanionMode(this.companionMode === 'physical' ? 'aura' : 'physical');
        this.createUI();
    }

    // =========================================================================
    // UI TOGGLE & NOTIFICATION
    // =========================================================================

    toggleUI() {
        this.uiVisible = !this.uiVisible;
        this.createUI();
    }

    showNotification(message, duration = 3000) {
        if (window.showNotification) {
            window.showNotification(message, duration);
        } else {
            console.log(message);
        }
    }

    // =========================================================================
    // UPDATE LOOP
    // =========================================================================

    update() {
        this.createUI();

        // Hunger Decay (1 Herz pro 60 Min wenn aktiv)
        if (!this.isSleeping && this.id) {
            const timeSinceFed = Date.now() - this.lastFed;
            const heartsToLose = Math.floor(timeSinceFed / SLIME_CONFIG.HUNGER_DECAY);

            if (heartsToLose > 0 && this.hungerHearts > 0) {
                this.hungerHearts = Math.max(0, this.hungerHearts - heartsToLose);
                this.lastFed = Date.now();

                if (this.hungerHearts === 0) {
                    this.addTrust(-5, 'Verhungert');
                    this.showNotification(`⚠️ ${this.name} verhungert! Vertrauen sinkt!`, 5000);
                } else if (this.hungerHearts <= 1) {
                    this.showNotification(`⚠️ ${this.name} ist hungrig!`, 3000);
                }
            }
        }

        // Rescue Charge regenerieren
        if (this.rescueCharges <= 0 && this.lastRescueUsed) {
            const timeSince = Date.now() - this.lastRescueUsed;
            if (timeSince >= SLIME_CONFIG.RESCUE_COOLDOWN) {
                this.rescueCharges = 1;
            }
        }

        // Auto-save alle 30s
        this._saveToLocalStorage();
    }

    // =========================================================================
    // SAVE / LOAD
    // =========================================================================

    toJSON() {
        return {
            id: this.id,
            name: this.name,
            currentForm: this.currentForm,
            startRegion: this.startRegion,
            learnedForms: this.learnedForms,
            formChangesSeason: this.formChangesSeason,
            currentSeason: this.currentSeason,
            auraLevel: this.auraLevel,
            elementAura: this.elementAura,
            totalFights: this.totalFights,
            trustPoints: this.trustPoints,
            trustLevel: this.trustLevel,
            hungerHearts: this.hungerHearts,
            companionMode: this.companionMode,
            skills: this.skills,
            memoriesUnlocked: this.memoriesUnlocked,
            memoryLog: this.memoryLog,
            thinksItIsMonster: this.thinksItIsMonster,
            humanFormUnlocked: this.humanFormUnlocked,
            isInHumanForm: this.isInHumanForm,
            rescueCharges: this.rescueCharges,
            lastRescueUsed: this.lastRescueUsed,
            battles: this.battles,
            wins: this.wins,
            birthTime: this.birthTime,
            lastFed: this.lastFed,
            lastPlayed: this.lastPlayed,
            isSleeping: this.isSleeping,
            isAlive: this.isAlive,
            isAtHome: this.isAtHome
        };
    }

    fromJSON(data) {
        if (!data) return;
        this.id = data.id ?? this.id;
        this.name = data.name ?? this.name;
        this.currentForm = data.currentForm ?? data.current_form ?? this.currentForm;
        this.startRegion = data.startRegion ?? data.start_region ?? this.startRegion;
        this.learnedForms = data.learnedForms ?? data.learned_forms ?? this.learnedForms;
        this.formChangesSeason = data.formChangesSeason ?? data.form_changes_season ?? this.formChangesSeason;
        this.currentSeason = data.currentSeason ?? data.current_season ?? this.currentSeason;
        this.auraLevel = data.auraLevel ?? data.aura_level ?? this.auraLevel;
        this.elementAura = data.elementAura ?? data.element_aura ?? this.elementAura;
        this.totalFights = data.totalFights ?? data.total_fights ?? this.totalFights;
        this.trustPoints = data.trustPoints ?? data.trust_points ?? this.trustPoints;
        this.trustLevel = data.trustLevel ?? data.trust_level ?? this._calculateTrustLevel();
        this.hungerHearts = data.hungerHearts ?? data.hunger_hearts ?? this.hungerHearts;
        this.companionMode = data.companionMode ?? data.companion_mode ?? this.companionMode;
        this.skills = data.skills ?? this.skills;
        this.memoriesUnlocked = data.memoriesUnlocked ?? data.memories_unlocked ?? this.memoriesUnlocked;
        this.memoryLog = data.memoryLog ?? data.memory_log ?? this.memoryLog;
        this.thinksItIsMonster = data.thinksItIsMonster ?? data.thinks_it_is_monster ?? this.thinksItIsMonster;
        this.humanFormUnlocked = data.humanFormUnlocked ?? data.human_form_unlocked ?? this.humanFormUnlocked;
        this.isInHumanForm = data.isInHumanForm ?? data.is_in_human_form ?? this.isInHumanForm;
        this.rescueCharges = data.rescueCharges ?? data.rescue_charges ?? this.rescueCharges;
        this.lastRescueUsed = data.lastRescueUsed ?? data.last_rescue_used ?? this.lastRescueUsed;
        this.battles = data.battles ?? this.battles;
        this.wins = data.wins ?? this.wins;
        this.birthTime = data.birthTime ?? data.birth_time ?? this.birthTime;
        this.lastFed = data.lastFed ?? data.last_fed ?? this.lastFed;
        this.lastPlayed = data.lastPlayed ?? data.last_played ?? this.lastPlayed;
        this.isSleeping = data.isSleeping ?? data.is_sleeping ?? this.isSleeping;
        this.isAlive = data.isAlive ?? data.is_alive ?? this.isAlive;
        this.isAtHome = data.isAtHome ?? data.is_at_home ?? this.isAtHome;
    }

    _saveToLocalStorage() {
        try {
            localStorage.setItem('najika_slime_v3', JSON.stringify(this.toJSON()));
        } catch (e) { /* localStorage voll oder nicht verfuegbar */ }
    }

    _loadFromLocalStorage() {
        try {
            const saved = localStorage.getItem('najika_slime_v3');
            if (saved) {
                this.fromJSON(JSON.parse(saved));
                console.log('✅ Slime V3 loaded from localStorage');
            }
        } catch (e) { /* Kein Save vorhanden */ }
    }
}

// =============================================================================
// GLOBAL INSTANCE & AUTO-INIT
// =============================================================================

window.slimeCompanion = new SlimeCompanion();

// Auto-load
window.addEventListener('load', () => {
    if (window.slimeCompanion) {
        window.slimeCompanion.loadFromBackend();
    }
});

// Update Loop
setInterval(() => {
    if (window.slimeCompanion) {
        window.slimeCompanion.update();
    }
}, SLIME_CONFIG.UPDATE_INTERVAL);

console.log('✅ Slime Companion System V3 (Formwandler + Aura + Vertrauen) loaded');
