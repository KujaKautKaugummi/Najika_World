// Najika Command System - Digimon World 1 Style
// Rookie → Champion → Ultimate → Mega Evolution

class CommandSystem {
  constructor() {
    // Battle XP for evolution
    this.battleXP = 0;
    this.evolutionStage = 'rookie'; // rookie, champion, ultimate, mega

    // Relationship stats - SYNC FROM SERVER!
    this.happiness = 50; // 0-100 (wird vom Server geladen)
    this.discipline = 50; // 0-100 (wird vom Server geladen)
    this.trust = 0; // 0-100
    this.understanding = 0; // 0-100
    this.synergy = 0; // 0-100

    // Sync with server on init
    this.syncFromServer();

    // Battle stats
    this.totalBattles = 0;
    this.victories = 0;
    this.commandsGiven = 0;
    this.perfectTimings = 0;
    this.learnedPatterns = [];

    // Current battle state
    this.lastCommandTime = 0;
    this.commandCooldown = 2000; // 2s cooldown
    this.overrideMode = false; // TAB toggle

    // AI preferences (learned over time)
    this.preferredStyle = 'balanced'; // offensive, defensive, balanced
    this.commandPreferences = {
      attack: 0,
      defend: 0,
      tech: 0,
      distance: 0
    };

    // Equipment-based Combat System
    this.equipment = {
      leftHand: null,   // Item-Objekt oder null
      rightHand: null,  // Item-Objekt oder null
      twoHanded: null   // Wenn Zweihänder ausgerüstet
    };
    this.lastAttackTime = { left: 0, right: 0 };

    // Equipment Types
    this.WEAPON_TYPES = {
      // Nahkampf
      sword: { type: 'melee', element: null, lightDmg: 20, heavyDmg: 50, lightCD: 300, heavyCD: 800 },
      axe: { type: 'melee', element: null, lightDmg: 25, heavyDmg: 70, lightCD: 400, heavyCD: 1000 },
      dagger: { type: 'melee', element: null, lightDmg: 12, heavyDmg: 30, lightCD: 150, heavyCD: 400 },

      // Zweihänder
      greatsword: { type: 'twohanded', element: null, lightDmg: 40, heavyDmg: 100, lightCD: 600, heavyCD: 1500 },
      staff: { type: 'twohanded', element: 'magic', lightDmg: 30, heavyDmg: 80, lightCD: 500, heavyCD: 1200 },

      // Zauber (auf Hand ausrüstbar)
      fireball: { type: 'spell', element: 'fire', lightDmg: 25, heavyDmg: 60, lightCD: 400, heavyCD: 1000, manaCost: 10 },
      icebolt: { type: 'spell', element: 'ice', lightDmg: 20, heavyDmg: 50, lightCD: 350, heavyCD: 900, manaCost: 8 },
      lightning: { type: 'spell', element: 'lightning', lightDmg: 30, heavyDmg: 70, lightCD: 500, heavyCD: 1100, manaCost: 15 },
      heal: { type: 'spell', element: 'light', lightDmg: -20, heavyDmg: -50, lightCD: 600, heavyCD: 1500, manaCost: 20 },

      // Schild (nur rechte Hand, nur Block)
      shield: { type: 'shield', element: null, blockValue: 50, parryWindow: 150 },

      // Faust (wenn nichts ausgerüstet)
      fist: { type: 'melee', element: null, lightDmg: 5, heavyDmg: 15, lightCD: 200, heavyCD: 500 }
    };
  }

  // Get current evolution stage
  getStage() {
    if (this.battleXP >= 1000) return 'mega';
    if (this.battleXP >= 500) return 'ultimate';
    if (this.battleXP >= 100) return 'champion';
    return 'rookie';
  }

  // Update evolution stage
  updateStage() {
    const oldStage = this.evolutionStage;
    this.evolutionStage = this.getStage();

    if (oldStage !== this.evolutionStage) {
      return {
        evolved: true,
        oldStage,
        newStage: this.evolutionStage,
        message: this.getEvolutionMessage(this.evolutionStage)
      };
    }

    return { evolved: false };
  }

  // Evolution messages
  getEvolutionMessage(stage) {
    const messages = {
      champion: "Kuja! Ich verstehe jetzt besser was du willst!",
      ultimate: "Wir sind ein Team, Kuja! Ich kann fast alleine kämpfen!",
      mega: "Perfekt! Ich kenne dich jetzt so gut, Kuja!"
    };
    return messages[stage] || '';
  }

  // Get available commands based on stage and override
  getAvailableCommands() {
    // Override mode = always rookie commands
    if (this.overrideMode) {
      return {
        mode: 'override',
        commands: [
          { key: '1', label: 'ATTACK', icon: '⚔️', description: 'Greif an!' },
          { key: '2', label: 'DEFEND', icon: '🛡️', description: 'Verteidige!' },
          { key: '3', label: 'TECH', icon: '⚡', description: 'Zauber!' },
          { key: '4', label: 'DISTANCE', icon: '💨', description: 'Zurück!' }
        ]
      };
    }

    // Stage-based commands
    switch (this.evolutionStage) {
      case 'rookie':
        return {
          mode: 'direct',
          commands: [
            { key: '1', label: 'ATTACK', icon: '⚔️', description: 'Greif an!' },
            { key: '2', label: 'DEFEND', icon: '🛡️', description: 'Verteidige!' },
            { key: '3', label: 'TECH', icon: '⚡', description: 'Zauber!' },
            { key: '4', label: 'DISTANCE', icon: '💨', description: 'Zurück!' }
          ]
        };

      case 'champion':
        return {
          mode: 'tactical',
          commands: [
            { key: '1', label: 'ATTACK', icon: '⚔️', description: 'Greif an (Najika wählt wie)' },
            { key: '2', label: 'DEFEND', icon: '🛡️', description: 'Verteidige (Najika wählt wie)' },
            { key: '3', label: 'TECH', icon: '⚡', description: 'Zauber (Najika wählt welchen)' },
            { key: '4', label: 'DISTANCE', icon: '💨', description: 'Zurück (Najika entscheidet wann)' }
          ]
        };

      case 'ultimate':
        return {
          mode: 'strategic',
          commands: [
            { key: '1', label: 'OFFENSIVE', icon: '⚔️', description: 'Aggressiv kämpfen' },
            { key: '2', label: 'DEFENSIVE', icon: '🛡️', description: 'Vorsichtig kämpfen' },
            { key: '3', label: 'BALANCED', icon: '⚖️', description: 'Ausgeglichen' },
            { key: '4', label: 'SPECIAL', icon: '✨', description: 'Finisher vorbereiten' }
          ]
        };

      case 'mega':
        return {
          mode: 'signals',
          commands: [
            { key: '1', label: 'NOW!', icon: '❗', description: 'Jetzt zuschlagen!' },
            { key: '2', label: 'WAIT!', icon: '✋', description: 'Zurückhalten!' },
            { key: '3', label: 'COMBO!', icon: '💥', description: 'Combo vorbereiten!' },
            { key: '4', label: 'SPECIAL', icon: '✨', description: 'Finisher!' }
          ]
        };

      default:
        return this.getAvailableCommands(); // Fallback to rookie
    }
  }

  // Execute command
  executeCommand(commandKey, najikaState) {
    const now = Date.now();

    // Check cooldown
    if (now - this.lastCommandTime < this.commandCooldown) {
      return {
        success: false,
        reason: 'cooldown',
        message: 'Warte kurz...'
      };
    }

    // Check if Najika will listen (discipline check)
    if (!this.overrideMode && Math.random() > this.discipline / 100) {
      // Low discipline = might ignore
      return {
        success: false,
        reason: 'ignored',
        message: 'Najika ignoriert dich! (Niedrige Discipline)',
        disciplineCheck: false
      };
    }

    this.lastCommandTime = now;
    this.commandsGiven++;

    // Track command preference
    const commandMap = { '1': 'attack', '2': 'defend', '3': 'tech', '4': 'distance' };
    if (commandMap[commandKey]) {
      this.commandPreferences[commandMap[commandKey]]++;
    }

    // Learn preferred style (after 50 commands)
    if (this.commandsGiven > 50) {
      this.updatePreferredStyle();
    }

    // Check timing (if champion+)
    const timingResult = this.evaluateTiming(commandKey, najikaState);

    return {
      success: true,
      command: commandKey,
      timing: timingResult,
      mode: this.overrideMode ? 'override' : this.evolutionStage,
      disciplineCheck: true
    };
  }

  // Evaluate command timing (Champion+)
  evaluateTiming(commandKey, najikaState) {
    if (this.evolutionStage === 'rookie' || this.overrideMode) {
      return { quality: 'normal', bonus: 0 };
    }

    // Perfect timing scenarios
    const perfectTimings = {
      '1': ['idle', 'recovering'], // Attack when enemy open
      '2': ['taking_damage', 'enemy_attacking'], // Defend when under attack
      '3': ['idle', 'preparing'], // Tech when ready
      '4': ['taking_damage', 'low_hp'] // Distance when in danger
    };

    if (perfectTimings[commandKey]?.includes(najikaState)) {
      this.perfectTimings++;
      this.trust = Math.min(100, this.trust + 2);
      return {
        quality: 'perfect',
        bonus: 0.3,
        message: 'Perfektes Timing!'
      };
    }

    // Good timing
    if (['idle', 'recovering', 'preparing'].includes(najikaState)) {
      return {
        quality: 'good',
        bonus: 0.1,
        message: 'Gutes Timing!'
      };
    }

    // Bad timing
    return {
      quality: 'bad',
      bonus: -0.1,
      message: 'Schlechtes Timing...'
    };
  }

  // Toggle override mode
  toggleOverride() {
    this.overrideMode = !this.overrideMode;

    return {
      enabled: this.overrideMode,
      message: this.overrideMode
        ? '⚠️ DIRECT COMMAND MODE - Najika folgt sofort!'
        : '✅ Zurück zu autonomem Modus'
    };
  }

  // Praise Najika
  async praise(context = 'normal') {
    // Call server API to update backend state
    try {
      const response = await fetch('/api/najika/praise', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });
      const data = await response.json();

      if (data.ok && data.najika) {
        // Update local values from server
        this.happiness = data.najika.happiness || this.happiness;
        this.discipline = data.najika.discipline || this.discipline;

        // Additional context-based updates (local only)
        if (context === 'after_good_move') {
          this.discipline = Math.min(100, this.discipline + 5); // Extra boost
          this.trust = Math.min(100, this.trust + 5);
          console.log('[CommandSystem] Praise (good move): Server updated, local bonuses applied');
          return {
            success: true,
            message: data.msg || 'Danke! Das motiviert mich!',
            happiness: this.happiness,
            discipline: this.discipline,
            trust: this.trust
          };
        } else {
          console.log('[CommandSystem] Praise: Server updated');
          return {
            success: true,
            message: data.msg || 'Danke, Kuja!',
            happiness: this.happiness,
            discipline: this.discipline
          };
        }
      }
    } catch (error) {
      console.error('[CommandSystem] Failed to praise via server:', error);
    }

    // Fallback to local-only update
    if (context === 'after_good_move') {
      this.happiness = Math.min(100, this.happiness + 10);
      this.discipline = Math.min(100, this.discipline + 10);
      this.trust = Math.min(100, this.trust + 5);
      return {
        success: true,
        message: 'Danke! Das motiviert mich!',
        happiness: +10,
        discipline: +10,
        trust: +5
      };
    } else {
      this.happiness = Math.min(100, this.happiness + 5);
      this.discipline = Math.max(0, this.discipline - 5);
      return {
        success: true,
        message: 'Danke, Kuja!',
        happiness: +5,
        discipline: -5
      };
    }
  }

  // Scold Najika
  async scold(context = 'normal') {
    // Call server API to update backend state
    try {
      const response = await fetch('/api/najika/scold', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });
      const data = await response.json();

      if (data.ok && data.najika) {
        // Update local values from server
        this.happiness = data.najika.happiness || this.happiness;
        this.discipline = data.najika.discipline || this.discipline;

        // Additional context-based updates (local only)
        if (context === 'after_mistake') {
          this.understanding = Math.min(100, this.understanding + 5);
          console.log('[CommandSystem] Scold (after mistake): Server updated, local bonuses applied');
          return {
            success: true,
            message: data.msg || 'Okay, ich pass besser auf!',
            discipline: this.discipline,
            happiness: this.happiness,
            understanding: this.understanding
          };
        } else {
          // Unfair scold - reduce trust locally
          this.trust = Math.max(0, this.trust - 10);
          console.log('[CommandSystem] Scold (unfair): Server updated, trust reduced');
          return {
            success: true,
            message: 'Was?! Das war unfair, Kuja!',
            discipline: this.discipline,
            happiness: this.happiness,
            trust: this.trust
          };
        }
      }
    } catch (error) {
      console.error('[CommandSystem] Failed to scold via server:', error);
    }

    // Fallback to local-only update
    if (context === 'after_mistake') {
      this.discipline = Math.min(100, this.discipline + 10);
      this.happiness = Math.max(0, this.happiness - 5);
      this.understanding = Math.min(100, this.understanding + 5);
      return {
        success: true,
        message: 'Okay, ich pass besser auf!',
        discipline: +10,
        happiness: -5,
        understanding: +5
      };
    } else {
      // Unfair scold
      this.discipline = Math.min(100, this.discipline + 5);
      this.happiness = Math.max(0, this.happiness - 15);
      this.trust = Math.max(0, this.trust - 10);
      return {
        success: true,
        message: 'Was?! Das war unfair, Kuja!',
        discipline: +5,
        happiness: -15,
        trust: -10
      };
    }
  }

  // Add battle XP
  addBattleXP(amount, victory = false) {
    this.battleXP += amount;
    this.totalBattles++;
    if (victory) this.victories++;

    // Update synergy
    this.synergy = Math.min(100, this.synergy + 1);

    return this.updateStage();
  }

  // Learn enemy pattern
  learnPattern(enemyType) {
    if (!this.learnedPatterns.includes(enemyType)) {
      this.learnedPatterns.push(enemyType);
      return {
        learned: true,
        message: `Ich kenne ${enemyType} jetzt!`
      };
    }
    return { learned: false };
  }

  // Update preferred style based on command history
  updatePreferredStyle() {
    const total = Object.values(this.commandPreferences).reduce((a, b) => a + b, 0);
    const attackPercent = this.commandPreferences.attack / total;
    const defendPercent = this.commandPreferences.defend / total;

    if (attackPercent > 0.6) {
      this.preferredStyle = 'offensive';
    } else if (defendPercent > 0.4) {
      this.preferredStyle = 'defensive';
    } else {
      this.preferredStyle = 'balanced';
    }
  }

  // Sync happiness/discipline from server
  async syncFromServer() {
    try {
      const response = await fetch('/api/status');
      const data = await response.json();
      if (data.najika) {
        this.happiness = data.najika.happiness || 50;
        this.discipline = data.najika.discipline || 50;
        console.log(`[CommandSystem] Synced from server: happiness=${this.happiness}, discipline=${this.discipline}`);
      }
    } catch (error) {
      console.warn('[CommandSystem] Failed to sync from server, using defaults');
    }
  }

  // Get stats for UI
  getStats() {
    return {
      // Evolution
      battleXP: this.battleXP,
      evolutionStage: this.evolutionStage,
      nextStageXP: this.getNextStageXP(),

      // Relationship
      happiness: this.happiness,
      discipline: this.discipline,
      trust: this.trust,
      understanding: this.understanding,
      synergy: this.synergy,

      // Battle history
      totalBattles: this.totalBattles,
      victories: this.victories,
      winRate: this.totalBattles > 0 ? (this.victories / this.totalBattles * 100).toFixed(1) : 0,
      commandsGiven: this.commandsGiven,
      perfectTimings: this.perfectTimings,

      // AI preferences
      preferredStyle: this.preferredStyle,
      learnedPatterns: this.learnedPatterns.length,

      // Current state
      overrideMode: this.overrideMode,
      canCommand: (Date.now() - this.lastCommandTime) >= this.commandCooldown
    };
  }

  // Get XP needed for next stage
  getNextStageXP() {
    switch (this.evolutionStage) {
      case 'rookie': return 100;
      case 'champion': return 500;
      case 'ultimate': return 1000;
      case 'mega': return null; // Max level
      default: return 100;
    }
  }

  // ========== EQUIPMENT-BASED COMBAT SYSTEM ==========

  // Equipment ausrüsten
  equipItem(hand, itemName) {
    const weapon = this.WEAPON_TYPES[itemName];
    if (!weapon) {
      return { success: false, reason: 'unknown_item' };
    }

    // Zweihänder nimmt beide Hände
    if (weapon.type === 'twohanded') {
      this.equipment.leftHand = null;
      this.equipment.rightHand = null;
      this.equipment.twoHanded = { name: itemName, ...weapon };
      return { success: true, message: `${itemName} ausgerüstet (Zweihänder)` };
    }

    // Schild nur rechte Hand
    if (weapon.type === 'shield' && hand === 'left') {
      return { success: false, reason: 'shield_right_hand_only' };
    }

    // Normales Item ausrüsten
    if (this.equipment.twoHanded) {
      this.equipment.twoHanded = null; // Zweihänder ablegen
    }

    if (hand === 'left') {
      this.equipment.leftHand = { name: itemName, ...weapon };
    } else {
      this.equipment.rightHand = { name: itemName, ...weapon };
    }

    return { success: true, message: `${itemName} in ${hand === 'left' ? 'linker' : 'rechter'} Hand` };
  }

  // Angriff ausführen (Light oder Heavy)
  executeAttack(hand, attackType) {
    const now = Date.now();

    // Hole aktives Weapon
    let weapon;
    if (this.equipment.twoHanded) {
      weapon = this.equipment.twoHanded;
      hand = 'both'; // Zweihänder nutzt beide Hände
    } else {
      weapon = hand === 'left' ? this.equipment.leftHand : this.equipment.rightHand;
    }

    // Fallback auf Faust
    if (!weapon) {
      weapon = { name: 'fist', ...this.WEAPON_TYPES.fist };
    }

    // Schild kann nicht angreifen
    if (weapon.type === 'shield') {
      return { success: false, reason: 'shield_cannot_attack' };
    }

    // Cooldown Check
    const cooldown = attackType === 'light' ? weapon.lightCD : weapon.heavyCD;
    const lastAttack = this.lastAttackTime[hand === 'both' ? 'left' : hand];

    if (now - lastAttack < cooldown) {
      return { success: false, reason: 'cooldown', remaining: cooldown - (now - lastAttack) };
    }

    // Update last attack time
    if (hand === 'both') {
      this.lastAttackTime.left = now;
      this.lastAttackTime.right = now;
    } else {
      this.lastAttackTime[hand] = now;
    }

    // Berechne Schaden
    const baseDamage = attackType === 'light' ? weapon.lightDmg : weapon.heavyDmg;
    const staminaCost = attackType === 'light' ? 5 : 20;
    const manaCost = weapon.manaCost ? (attackType === 'light' ? weapon.manaCost : weapon.manaCost * 2) : 0;

    return {
      success: true,
      weapon: weapon.name,
      hand: hand,
      attackType: attackType,
      damage: baseDamage,
      element: weapon.element,
      staminaCost: staminaCost,
      manaCost: manaCost,
      isTwoHanded: hand === 'both'
    };
  }

  // Weave ausführen (beide Hände mit Zauber gleichzeitig)
  executeWeave() {
    const left = this.equipment.leftHand;
    const right = this.equipment.rightHand;

    // Braucht beide Hände mit Zauber
    if (!left || !right) {
      return { success: false, reason: 'need_both_hands' };
    }

    if (left.type !== 'spell' || right.type !== 'spell') {
      return { success: false, reason: 'need_spells_both_hands', message: 'Weave braucht Zauber in beiden Händen!' };
    }

    // Element-Kombination
    const combo = [left.element, right.element].sort().join('+');

    const weaves = {
      'fire+ice': { name: 'Thermoschock', damage: 80, effect: 'stun', duration: 2000 },
      'fire+lightning': { name: 'Plasmasturm', damage: 100, effect: 'burn_chain', duration: 3000 },
      'fire+wind': { name: 'Feuersturm', damage: 90, effect: 'burn_aoe', radius: 5 },
      'ice+lightning': { name: 'Frostschock', damage: 85, effect: 'slow_paralysis', duration: 2500 },
      'ice+wind': { name: 'Blizzard', damage: 70, effect: 'slow_aoe', radius: 8 },
      'lightning+wind': { name: 'Sturmblitz', damage: 95, effect: 'knockback', force: 10 },
      'ice+water': { name: 'Gefrierwelle', damage: 65, effect: 'freeze', duration: 3000 },
      'fire+earth': { name: 'Lava-Eruption', damage: 110, effect: 'terrain_fire', duration: 5000 },
      'earth+lightning': { name: 'Erdbeben', damage: 100, effect: 'stun_aoe', radius: 6 }
    };

    const weave = weaves[combo] || { name: 'Magie-Fusion', damage: 60, effect: 'none' };
    const totalManaCost = (left.manaCost || 10) + (right.manaCost || 10);

    return {
      success: true,
      weave: weave,
      elements: [left.element, right.element],
      staminaCost: 30,
      manaCost: totalManaCost
    };
  }

  // Block (nur mit Schild oder Waffe)
  executeBlock() {
    const right = this.equipment.rightHand;

    if (right && right.type === 'shield') {
      return { success: true, blockValue: right.blockValue, type: 'shield_block' };
    }

    // Waffen-Block (weniger effektiv)
    if (right && right.type === 'melee') {
      return { success: true, blockValue: 20, type: 'weapon_block' };
    }

    // Zweihänder-Block
    if (this.equipment.twoHanded) {
      return { success: true, blockValue: 30, type: 'twohanded_block' };
    }

    return { success: false, reason: 'nothing_to_block_with' };
  }

  // Parry (Timing-basiert)
  executeParry() {
    const right = this.equipment.rightHand;
    const parryWindow = right && right.type === 'shield' ? right.parryWindow : 100; // ms

    return {
      success: true,
      parryWindow: parryWindow, // 100-150ms Fenster
      perfectWindow: 50, // Perfektes Parry in den ersten 50ms
      type: right && right.type === 'shield' ? 'shield_parry' : 'weapon_parry'
    };
  }

  // Combo System
  executeCombo(sequence) {
    const combos = {
      'light,light,light': { name: 'Triple Strike', multiplier: 1.5, finisher: false },
      'light,heavy': { name: 'Smash', multiplier: 1.3, finisher: false },
      'heavy,light,light': { name: 'Crusher', multiplier: 1.4, finisher: false },
      'light,light,heavy': { name: 'Finisher', multiplier: 1.8, finisher: true },
      'heavy,heavy': { name: 'Power Slam', multiplier: 2.0, finisher: true, staminaCost: 40 }
    };

    const key = sequence.join(',');
    return combos[key] || null;
  }

  // Aktuellen Equipment-Status holen
  getEquipmentStatus() {
    return {
      leftHand: this.equipment.leftHand ? this.equipment.leftHand.name : 'Faust',
      rightHand: this.equipment.rightHand ? this.equipment.rightHand.name : 'Faust',
      twoHanded: this.equipment.twoHanded ? this.equipment.twoHanded.name : null,
      canWeave: this.equipment.leftHand?.type === 'spell' && this.equipment.rightHand?.type === 'spell'
    };
  }
}
