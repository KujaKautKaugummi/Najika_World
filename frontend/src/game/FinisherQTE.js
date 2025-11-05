// Finisher QTE System - Digimon World Style
// "FINISH!!!" Button-Mashing für erhöhten Damage

export class FinisherQTE {
  constructor() {
    this.active = false;
    this.meter = 0; // 0-100
    this.duration = 3000; // 3 Sekunden
    this.startTime = 0;
    this.mashCount = 0;
    this.lastMashTime = 0;
    this.mashCooldown = 100; // 100ms zwischen Mashes
  }

  // Starte Finisher QTE
  start() {
    this.active = true;
    this.meter = 0;
    this.startTime = Date.now();
    this.mashCount = 0;
    this.lastMashTime = 0;

    console.log('🔥 FINISHER QTE GESTARTET!');

    return {
      active: true,
      message: '🔥 FINISH!!! 🔥',
      instruction: 'SPACE schnell drücken!'
    };
  }

  // Registriere Mash-Input
  onMash() {
    if (!this.active) return { success: false };

    const now = Date.now();

    // Cooldown-Check (verhindert Spam)
    if (now - this.lastMashTime < this.mashCooldown) {
      return { success: false, reason: 'too_fast' };
    }

    this.lastMashTime = now;
    this.mashCount++;

    // Erhöhe Meter (jeder Mash = +5%)
    this.meter = Math.min(100, this.meter + 5);

    console.log(`Mash ${this.mashCount}: Meter ${this.meter}%`);

    return {
      success: true,
      meter: this.meter,
      mashCount: this.mashCount
    };
  }

  // Update (muss jeden Frame aufgerufen werden)
  update(delta) {
    if (!this.active) return null;

    const now = Date.now();
    const elapsed = now - this.startTime;

    // Zeit abgelaufen?
    if (elapsed >= this.duration) {
      return this.finish();
    }

    // Meter sinkt langsam wenn nicht gemashed
    if (now - this.lastMashTime > 200) {
      this.meter = Math.max(0, this.meter - (delta * 10)); // -10% pro Sekunde
    }

    return {
      active: true,
      meter: this.meter,
      timeLeft: this.duration - elapsed,
      mashCount: this.mashCount
    };
  }

  // Beende Finisher und berechne Damage Multiplier
  finish() {
    if (!this.active) return null;

    this.active = false;

    // Berechne Damage Multiplier basierend auf Meter
    // 0%   = 1.0x (normal)
    // 50%  = 1.5x
    // 100% = 2.0x (max)
    const multiplier = 1.0 + (this.meter / 100);

    let rank = 'C';
    if (this.meter >= 90) rank = 'S';
    else if (this.meter >= 70) rank = 'A';
    else if (this.meter >= 50) rank = 'B';

    console.log(`✨ FINISHER BEENDET! Meter: ${this.meter}%, Multiplier: ${multiplier.toFixed(2)}x, Rank: ${rank}`);

    return {
      active: false,
      completed: true,
      meter: this.meter,
      multiplier: multiplier,
      mashCount: this.mashCount,
      rank: rank,
      message: this.getFinishMessage(rank, multiplier)
    };
  }

  // Finisher Nachricht basierend auf Performance
  getFinishMessage(rank, multiplier) {
    const messages = {
      'S': '✨ PERFEKT! MAXIMALER SCHADEN! ✨',
      'A': '🔥 EXCELLENT! KRITISCHER TREFFER! 🔥',
      'B': '⚡ GOOD! STARKER ANGRIFF! ⚡',
      'C': '💥 OK! Treffer gelandet! 💥'
    };

    return messages[rank] || messages['C'];
  }

  // Abbrechen (falls Spieler stirbt etc.)
  cancel() {
    if (!this.active) return null;

    this.active = false;

    return {
      active: false,
      completed: false,
      cancelled: true,
      message: 'Finisher abgebrochen!'
    };
  }

  // Ist QTE gerade aktiv?
  isActive() {
    return this.active;
  }

  // Hole UI-Daten
  getUIData() {
    if (!this.active) {
      return {
        active: false,
        showPrompt: false
      };
    }

    const now = Date.now();
    const elapsed = now - this.startTime;
    const timeLeft = Math.max(0, this.duration - elapsed);
    const timePercent = (timeLeft / this.duration) * 100;

    return {
      active: true,
      showPrompt: true,
      meter: Math.floor(this.meter),
      timeLeft: Math.ceil(timeLeft / 1000), // In Sekunden
      timePercent: timePercent,
      mashCount: this.mashCount,
      instruction: 'SPACE SCHNELL DRÜCKEN!'
    };
  }

  // Advanced Finisher (für höhere Evolution-Stufen)
  // Timing-Circles wie in Digimon World: Next Order
  startAdvancedQTE() {
    // TODO: Implement advanced QTE with timing circles
    // Für Champion+: Timing-Kreis statt nur Mashing
    // Für Ultimate+: Multiple Timing-Kreise
    // Für Mega: Cinematic Finish mit Kuja zusammen

    console.log('⚠️ Advanced QTE noch nicht implementiert - nutze Basic QTE');
    return this.start();
  }
}
