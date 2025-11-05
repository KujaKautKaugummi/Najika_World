// Najika Combat System - Soulframe + Skyrim Hybrid
// IMPORTANT: NOT Dark Souls! Fluid & forgiving, not punishing!
export class CombatSystem {
  constructor() {
    this.player = {
      hp: 100,
      maxHp: 100,
      mana: 50,
      maxMana: 50,
      stamina: 100,
      maxStamina: 100,
      staminaRegen: 10 // per second (generous!)
    };

    this.combos = [];
    this.comboTimer = 0;
    this.comboWindow = 1500; // 1.5s to continue combo

    this.elements = ['fire', 'water', 'earth', 'air', 'light', 'shadow'];

    // Stamina costs (NOT brutal like Souls!)
    this.staminaCosts = {
      lightAttack: 5,
      heavyAttack: 30,
      dodge: 20,
      sprint: 10, // per second
      block: 15, // per second
      parry: 10,
      weave: 25
    };

    // Combat state
    this.isBlocking = false;
    this.isDodging = false;
    this.iFrames = 0; // Invincibility frames
    this.lastActionTime = 0;

    // Dual-wielding slots (Skyrim style)
    this.leftHand = null; // weapon or element
    this.rightHand = null; // weapon or element
  }

  // Update system (called every frame)
  update(deltaTime) {
    // Stamina regeneration (generous, unlike Souls!)
    if (!this.isBlocking && !this.isDodging) {
      this.player.stamina = Math.min(
        this.player.maxStamina,
        this.player.stamina + this.staminaRegen * deltaTime
      );
    }

    // Combo timer decay
    if (this.comboTimer > 0) {
      this.comboTimer -= deltaTime * 1000;
      if (this.comboTimer <= 0) {
        this.resetCombo();
      }
    }

    // i-Frames decay
    if (this.iFrames > 0) {
      this.iFrames -= deltaTime * 1000;
    }
  }

  // Light Attack (fast, low damage)
  lightAttack() {
    if (this.player.stamina < this.staminaCosts.lightAttack) {
      return { success: false, reason: 'no_stamina' };
    }

    this.player.stamina -= this.staminaCosts.lightAttack;
    this.combos.push('light');
    this.comboTimer = this.comboWindow;

    // Check combo
    const comboResult = this.checkCombo();

    return {
      success: true,
      damage: 10,
      stamina: this.player.stamina,
      combo: comboResult,
      animation: 'light_attack'
    };
  }

  // Heavy Attack (charged, high damage)
  heavyAttack() {
    if (this.player.stamina < this.staminaCosts.heavyAttack) {
      return { success: false, reason: 'no_stamina' };
    }

    this.player.stamina -= this.staminaCosts.heavyAttack;
    this.combos.push('heavy');
    this.comboTimer = this.comboWindow;

    const comboResult = this.checkCombo();

    return {
      success: true,
      damage: 25,
      stamina: this.player.stamina,
      combo: comboResult,
      animation: 'heavy_attack',
      chargeTime: 0.8 // 800ms charge
    };
  }

  // Parry (timing-based, generous window for mobile)
  parry() {
    if (this.player.stamina < this.staminaCosts.parry) {
      return { success: false, reason: 'no_stamina' };
    }

    this.player.stamina -= this.staminaCosts.parry;

    // Parry window: 80-200ms (more forgiving than Souls!)
    const parryWindow = {
      perfect: { start: 80, end: 120 }, // 40ms window
      good: { start: 50, end: 200 }     // 150ms window
    };

    // For now, simplified timing (integrate with enemy attack timing later)
    const timing = Math.random();
    let result;

    if (timing < 0.3) { // 30% perfect
      result = 'perfect';
      this.combos.push('parry_perfect');
      return {
        success: true,
        timing: 'perfect',
        damage: 0,
        counterDamage: 60, // Riposte opportunity!
        stamina: this.player.stamina,
        animation: 'parry_perfect'
      };
    } else if (timing < 0.7) { // 40% good
      result = 'good';
      return {
        success: true,
        timing: 'good',
        damage: 0,
        stamina: this.player.stamina,
        animation: 'parry_good'
      };
    } else { // 30% fail
      return {
        success: false,
        timing: 'miss',
        damage: 0,
        stamina: this.player.stamina,
        animation: 'parry_miss'
      };
    }
  }

  // Dodge Roll (i-Frames, fluid like Soulframe)
  dodge() {
    if (this.player.stamina < this.staminaCosts.dodge) {
      return { success: false, reason: 'no_stamina' };
    }

    this.player.stamina -= this.staminaCosts.dodge;
    this.isDodging = true;
    this.iFrames = 300; // 300ms invincibility (generous!)

    setTimeout(() => {
      this.isDodging = false;
    }, 500); // 500ms dodge duration

    return {
      success: true,
      stamina: this.player.stamina,
      iFrames: true,
      animation: 'dodge_roll'
    };
  }

  // Block (hold to reduce damage, Skyrim style)
  block(isHolding) {
    if (isHolding) {
      if (this.player.stamina <= 0) {
        this.isBlocking = false;
        return { success: false, reason: 'no_stamina' };
      }

      this.isBlocking = true;
      return {
        success: true,
        damageReduction: 0.5, // 50% reduction
        staminaDrain: this.staminaCosts.block,
        animation: 'blocking'
      };
    } else {
      this.isBlocking = false;
      return { success: true, blocking: false };
    }
  }

  // Check combo sequences
  checkCombo() {
    const combo = this.combos.slice(-3).join('-'); // Last 3 attacks

    const comboPatterns = {
      'light-light-light': { name: 'Triple Strike', damage: 50, animation: 'triple_strike' },
      'light-heavy': { name: 'Smash', damage: 80, animation: 'smash' },
      'parry_perfect-heavy': { name: 'Riposte', damage: 120, animation: 'riposte' },
      'dodge-light': { name: 'Counter', damage: 60, animation: 'counter' }
    };

    return comboPatterns[combo] || null;
  }

  // Reset combo
  resetCombo() {
    this.combos = [];
    this.comboTimer = 0;
  }

  // Weave Elements (Skyrim dual-casting style)
  // EXPANDED: 15 combinations instead of 6!
  weaveElements(element1, element2) {
    if (this.player.stamina < this.staminaCosts.weave) {
      return { success: false, reason: 'no_stamina' };
    }

    this.player.stamina -= this.staminaCosts.weave;

    // All 15 combinations (6 elements = 15 unique pairs)
    const combinations = {
      // Fire combinations
      'fire_water': { result: 'steam', effect: 'blind_aoe', damage: 40, description: 'Dampfexplosion blendet Gegner' },
      'fire_earth': { result: 'lava', effect: 'dot_slow', damage: 60, description: 'Lava-Pfütze verlangsamt und verbrennt' },
      'fire_air': { result: 'inferno', effect: 'explosion_boost', damage: 80, description: 'Feuersturm mit Explosionsboost' },
      'fire_light': { result: 'holy_flame', effect: 'purify', damage: 70, description: 'Heiliges Feuer reinigt Status' },
      'fire_shadow': { result: 'hellfire', effect: 'fear', damage: 90, description: 'Dunkle Flammen verursachen Angst' },

      // Water combinations
      'water_earth': { result: 'mud', effect: 'root', damage: 30, description: 'Schlammfalle wurzelt Gegner' },
      'water_air': { result: 'storm', effect: 'lightning_chain', damage: 75, description: 'Gewitter mit Kettenblitz' },
      'water_light': { result: 'healing_rain', effect: 'heal_aoe', damage: 0, description: 'Heilender Regen für Verbündete' },
      'water_shadow': { result: 'mist', effect: 'stealth', damage: 20, description: 'Nebel ermöglicht Tarnung' },

      // Earth combinations
      'earth_air': { result: 'sandstorm', effect: 'blind_dot', damage: 50, description: 'Sandsturm blendet und schadet' },
      'earth_light': { result: 'crystal', effect: 'shield', damage: 0, description: 'Kristallschild reflektiert Schaden' },
      'earth_shadow': { result: 'decay', effect: 'poison', damage: 65, description: 'Verfall vergiftet über Zeit' },

      // Air combinations
      'air_light': { result: 'flash', effect: 'stun', damage: 35, description: 'Blendender Blitz betäubt' },
      'air_shadow': { result: 'void', effect: 'silence', damage: 45, description: 'Leere unterdrückt Magie' },

      // Light + Shadow
      'light_shadow': { result: 'chaos', effect: 'random', damage: 100, description: 'Chaosmagie mit zufälligem Effekt' }
    };

    const key = [element1, element2].sort().join('_');
    const weave = combinations[key];

    if (weave) {
      return {
        success: true,
        weave: weave.result,
        effect: weave.effect,
        damage: weave.damage,
        description: weave.description,
        stamina: this.player.stamina,
        animation: `weave_${weave.result}`
      };
    }

    // Invalid combination - basic cast
    return {
      success: true,
      weave: 'basic',
      damage: 15,
      stamina: this.player.stamina,
      animation: 'cast_basic'
    };
  }

  // Finisher QTE (when enemy HP < 20%)
  triggerFinisher(enemy) {
    if (enemy.hp > enemy.maxHp * 0.2) {
      return { success: false, reason: 'hp_too_high' };
    }

    return {
      success: true,
      qteActive: true,
      requiredPresses: 20 + (enemy.level * 2),
      timeWindow: 3000, // 3 seconds
      damage: 999, // Instant kill
      animation: 'finisher_qte'
    };
  }

  // Dual-wield setup (Skyrim style)
  equip(hand, item) {
    if (hand === 'left') {
      this.leftHand = item;
    } else if (hand === 'right') {
      this.rightHand = item;
    }

    return { success: true, leftHand: this.leftHand, rightHand: this.rightHand };
  }

  // Get current stats for UI
  getStats() {
    return {
      hp: this.player.hp,
      maxHp: this.player.maxHp,
      stamina: this.player.stamina,
      maxStamina: this.player.maxStamina,
      mana: this.player.mana,
      maxMana: this.player.maxMana,
      isBlocking: this.isBlocking,
      isDodging: this.isDodging,
      hasIFrames: this.iFrames > 0,
      combo: this.combos.slice(-3),
      leftHand: this.leftHand,
      rightHand: this.rightHand
    };
  }
}
