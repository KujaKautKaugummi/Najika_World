// Najika Cheer System - Digimon World Style
// Used in ORBIT CAM mode - Player cheers for autonomous Najika

export class CheerSystem {
  constructor() {
    this.cheerMeter = 0; // 0-100
    this.cheerBonus = 0; // Stat multiplier
    this.lastCheerTime = 0;
    this.cooldown = 2000; // 2s base cooldown
    this.badCheerCount = 0;
    this.specialFinisherReady = false;

    // Najika's combat states
    this.najikaState = 'idle';
    this.stateStartTime = Date.now();

    // Cheer timing windows (in ms)
    this.timings = {
      PERFECT: {
        window: [0, 200],
        statBonus: 0.20,
        cheerGain: 20,
        cooldown: 2000
      },
      GOOD: {
        window: [200, 500],
        statBonus: 0.10,
        cheerGain: 10,
        cooldown: 2500
      },
      BAD: {
        window: [500, Infinity],
        statBonus: 0.0,
        cheerGain: -5,
        cooldown: 3000
      },
      TERRIBLE: { // Während Najika Schaden nimmt
        statBonus: -0.05,
        cheerGain: -10,
        cooldown: 4000
      }
    };

    // States where cheering is perfect
    this.perfectStates = ['attacking', 'dodging', 'blocking', 'casting'];
    this.goodStates = ['preparing_attack', 'recovering', 'moving'];
    this.badStates = ['idle', 'focusing', 'resting'];
    this.terribleStates = ['taking_damage', 'stunned'];
  }

  // Update Najika's current state
  updateNajikaState(newState) {
    this.najikaState = newState;
    this.stateStartTime = Date.now();
  }

  // Player presses SPACE to cheer
  onCheerInput() {
    const now = Date.now();

    // Check cooldown
    if (now - this.lastCheerTime < this.cooldown) {
      return {
        result: 'ON_COOLDOWN',
        message: 'Warte kurz...'
      };
    }

    // Check Najika's state
    const timingResult = this.evaluateTiming();
    this.lastCheerTime = now;
    this.cooldown = timingResult.cooldown;

    // Update cheer meter
    this.cheerMeter = Math.max(0, Math.min(100, this.cheerMeter + timingResult.cheerGain));
    this.cheerBonus = this.calculateBonus();

    // Track bad cheers
    if (timingResult.result === 'BAD' || timingResult.result === 'TERRIBLE') {
      this.badCheerCount++;

      // Too many bad cheers = disable temporarily
      if (this.badCheerCount >= 5) {
        this.disableCheerTemporarily(30000); // 30s
        return {
          result: 'DISABLED',
          message: 'Kuja... lass mich das alleine machen.',
          affinityChange: -0.02
        };
      }
    } else {
      // Good cheer resets bad count
      this.badCheerCount = Math.max(0, this.badCheerCount - 1);
    }

    // Check for special finisher
    if (this.cheerMeter >= 100 && !this.specialFinisherReady) {
      this.specialFinisherReady = true;
      return {
        ...timingResult,
        specialUnlocked: true,
        message: 'KUJA! JETZT! GEMEINSAM!'
      };
    }

    return timingResult;
  }

  // Evaluate timing based on Najika's state
  evaluateTiming() {
    const stateTime = Date.now() - this.stateStartTime;

    // TERRIBLE - Najika is taking damage
    if (this.terribleStates.includes(this.najikaState)) {
      return {
        result: 'TERRIBLE',
        statBonus: this.timings.TERRIBLE.statBonus,
        cheerGain: this.timings.TERRIBLE.cheerGain,
        cooldown: this.timings.TERRIBLE.cooldown,
        message: 'KUJA! Du lenkst mich ab!!',
        animation: 'angry',
        najikaReaction: 'frustrated'
      };
    }

    // PERFECT - Najika is in action state
    if (this.perfectStates.includes(this.najikaState)) {
      // Check if within perfect window (first 200ms of action)
      if (stateTime <= this.timings.PERFECT.window[1]) {
        return {
          result: 'PERFECT',
          statBonus: this.timings.PERFECT.statBonus,
          cheerGain: this.timings.PERFECT.cheerGain,
          cooldown: this.timings.PERFECT.cooldown,
          message: 'Ja! Genau richtig!',
          animation: 'thumbs_up',
          najikaReaction: 'excited'
        };
      }
      // Good window (200-500ms)
      else if (stateTime <= this.timings.GOOD.window[1]) {
        return {
          result: 'GOOD',
          statBonus: this.timings.GOOD.statBonus,
          cheerGain: this.timings.GOOD.cheerGain,
          cooldown: this.timings.GOOD.cooldown,
          message: 'OK!',
          animation: 'nod',
          najikaReaction: 'positive'
        };
      }
    }

    // GOOD - Najika is preparing
    if (this.goodStates.includes(this.najikaState)) {
      return {
        result: 'GOOD',
        statBonus: this.timings.GOOD.statBonus,
        cheerGain: this.timings.GOOD.cheerGain,
        cooldown: this.timings.GOOD.cooldown,
        message: 'Danke!',
        animation: 'nod',
        najikaReaction: 'positive'
      };
    }

    // BAD - Wrong timing
    return {
      result: 'BAD',
      statBonus: this.timings.BAD.statBonus,
      cheerGain: this.timings.BAD.cheerGain,
      cooldown: this.timings.BAD.cooldown,
      message: 'Nicht jetzt...',
      animation: 'annoyed_glance',
      najikaReaction: 'annoyed'
    };
  }

  // Calculate current stat bonus based on cheer meter
  calculateBonus() {
    if (this.cheerMeter >= 80) return 0.25; // +25% Stats
    if (this.cheerMeter >= 60) return 0.20;
    if (this.cheerMeter >= 40) return 0.15;
    if (this.cheerMeter >= 20) return 0.10;
    return 0;
  }

  // Use special finisher (resets meter)
  useSpecialFinisher() {
    if (!this.specialFinisherReady) return null;

    this.specialFinisherReady = false;
    this.cheerMeter = 0;
    this.cheerBonus = 0;

    return {
      damage: 300, // 3x normal damage
      animation: 'special_finish',
      message: 'EXPLOSION! Gemeinsam mit Kuja!',
      cinematicPlay: true
    };
  }

  // Disable cheer temporarily
  disableCheerTemporarily(duration) {
    const originalCooldown = this.cooldown;
    this.cooldown = duration;
    this.badCheerCount = 0;

    setTimeout(() => {
      this.cooldown = originalCooldown;
    }, duration);
  }

  // Decay cheer meter over time (passive drain)
  update(deltaTime) {
    // Cheer meter decays slowly when not cheering
    this.cheerMeter = Math.max(0, this.cheerMeter - deltaTime * 0.5); // -0.5 per second
    this.cheerBonus = this.calculateBonus();
  }

  // Get UI display data
  getUIData() {
    return {
      cheerMeter: this.cheerMeter,
      cheerBonus: this.cheerBonus,
      specialReady: this.specialFinisherReady,
      cooldownRemaining: Math.max(0, this.cooldown - (Date.now() - this.lastCheerTime)),
      meterDisplay: this.getMeterDisplay(),
      canCheer: (Date.now() - this.lastCheerTime) >= this.cooldown
    };
  }

  // Get visual meter display (for UI)
  getMeterDisplay() {
    const filled = Math.floor(this.cheerMeter / 20);
    const empty = 5 - filled;

    let display = '';
    if (this.cheerMeter >= 100) {
      display = '🔥🔥🔥🔥🔥'; // Full = FIRE!
    } else {
      display = '🟡'.repeat(filled) + '⚪'.repeat(empty);
    }

    let status = '';
    if (this.cheerMeter >= 80) status = 'Najika ist im Flow!';
    else if (this.cheerMeter >= 60) status = 'Najika ist begeistert!';
    else if (this.cheerMeter >= 40) status = 'Najika ist motiviert';
    else if (this.cheerMeter >= 20) status = 'Najika ist OK';
    else status = 'Najika ist frustriert';

    return { display, status };
  }

  // Show timing window indicator (for UI)
  shouldShowTimingWindow() {
    return this.perfectStates.includes(this.najikaState) ||
           this.goodStates.includes(this.najikaState);
  }

  // Reset system (new battle/area)
  reset() {
    this.cheerMeter = 0;
    this.cheerBonus = 0;
    this.badCheerCount = 0;
    this.specialFinisherReady = false;
    this.najikaState = 'idle';
  }
}
