// Battle API - Verbindung zum Python Backend
// Kommuniziert mit C:\NajikaCore\najika_server.py

// BACKEND_URL is already defined globally in index.html
// const BACKEND_URL = 'http://localhost:8000';
const BACKEND_URL = window.BACKEND_URL || 'http://localhost:8000';

class BattleAPI {
  constructor() {
    this.battleActive = false;
    this.currentStatus = null;
  }

  // Starte neuen Kampf
  async startBattle() {
    try {
      const response = await fetch(`${BACKEND_URL}/api/battle/start`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const status = await response.json();
      this.battleActive = status.active || false;
      this.currentStatus = status;

      console.log('✅ Battle gestartet:', status);
      return status;
    } catch (error) {
      console.error('❌ Battle Start Error:', error);
      return {
        active: false,
        error: error.message,
        fallback: true,
        // Fallback-Daten falls Backend offline
        player: { hp: 100, max_hp: 100, mp: 50, max_mp: 50 },
        enemies: [{ name: 'Local Enemy', hp: 50, max_hp: 50 }],
        wave: 1,
        message: 'Offline-Modus (Backend nicht erreichbar)'
      };
    }
  }

  // Hole aktuellen Battle-Status
  async getBattleStatus() {
    try {
      const response = await fetch(`${BACKEND_URL}/api/battle/status`);

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const status = await response.json();
      this.battleActive = status.active || false;
      this.currentStatus = status;

      return status;
    } catch (error) {
      console.error('❌ Battle Status Error:', error);
      return {
        active: false,
        error: error.message,
        fallback: true
      };
    }
  }

  // Führe Spieler-Aktion aus
  async executeAction(action, options = {}) {
    try {
      const payload = {
        action: action, // 'attack', 'skill', 'item', 'defend', 'flee'
        target_index: options.targetIndex || 0,
        skill_name: options.skillName || null,
        item_name: options.itemName || null
      };

      const response = await fetch(`${BACKEND_URL}/api/battle/action`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const status = await response.json();
      this.battleActive = status.active || false;
      this.currentStatus = status;

      console.log(`✅ Action '${action}' ausgeführt:`, status);
      return status;
    } catch (error) {
      console.error(`❌ Battle Action '${action}' Error:`, error);
      return {
        active: this.battleActive,
        error: error.message,
        fallback: true,
        message: `Aktion fehlgeschlagen: ${error.message}`
      };
    }
  }

  // Command-System Integration
  // Übersetzt Digimon World Commands zu Battle Actions
  async executeCommand(commandKey, commandData) {
    const commandMap = {
      '1': 'attack',      // ATTACK → attack
      '2': 'defend',      // DEFEND → defend
      '3': 'skill',       // TECH → skill (random skill)
      '4': 'flee'         // DISTANCE → flee
    };

    const action = commandMap[commandKey] || 'attack';

    // Für TECH (3): Wähle zufällig verfügbaren Skill
    let skillName = null;
    if (action === 'skill') {
      const skills = await this.getAvailableSkills();
      if (skills && skills.length > 0) {
        skillName = skills[Math.floor(Math.random() * skills.length)].name;
      }
    }

    return await this.executeAction(action, { skillName });
  }

  // Hole verfügbare Skills
  async getAvailableSkills() {
    try {
      const response = await fetch(`${BACKEND_URL}/api/battle/skills`);

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const data = await response.json();
      return data.skills || [];
    } catch (error) {
      console.error('❌ Skills Error:', error);
      return [];
    }
  }

  // Reset Battle
  async resetBattle() {
    try {
      const response = await fetch(`${BACKEND_URL}/api/battle/reset`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const data = await response.json();
      this.battleActive = false;
      this.currentStatus = null;

      console.log('✅ Battle reset');
      return data;
    } catch (error) {
      console.error('❌ Battle Reset Error:', error);
      return { ok: false, error: error.message };
    }
  }

  // Prüfe ob Backend erreichbar ist
  async checkBackend() {
    try {
      const response = await fetch(`${BACKEND_URL}/health`);
      return response.ok;
    } catch (error) {
      console.warn('⚠️ Backend nicht erreichbar:', error.message);
      return false;
    }
  }

  // Battle XP für Evolution-System
  // Berechnet Battle XP basierend auf Backend-Battle-Status
  calculateBattleXP(status) {
    if (!status || !status.active) return 0;

    let xp = 0;

    // XP für besiegte Gegner (aus vorherigen Wellen)
    if (status.wave) {
      xp += (status.wave - 1) * 20; // 20 XP pro abgeschlossene Welle
    }

    // XP für Damage dealt
    if (status.player && status.player.damage_dealt) {
      xp += Math.floor(status.player.damage_dealt / 10);
    }

    // XP für Sieg
    if (status.result === 'victory') {
      xp += 50;
    }

    return xp;
  }

  // Sync CommandSystem mit Battle-Status
  // Gibt Najika's aktuellen State zurück für Timing-Evaluation
  getNajikaState(status) {
    if (!status || !status.active) return 'idle';

    // Prüfe Player HP
    if (status.player) {
      const hpPercent = (status.player.hp / status.player.max_hp) * 100;

      if (hpPercent < 30) {
        return 'low_hp'; // DISTANCE ist gut hier
      }

      // Prüfe ob gerade Damage genommen
      if (status.last_player_damage && status.last_player_damage > 0) {
        return 'taking_damage'; // DEFEND ist gut hier
      }
    }

    // Prüfe Enemies
    if (status.enemies && status.enemies.length > 0) {
      const firstEnemy = status.enemies[0];
      const enemyHpPercent = (firstEnemy.hp / firstEnemy.max_hp) * 100;

      if (enemyHpPercent < 20) {
        return 'enemy_low_hp'; // ATTACK ist gut hier
      }
    }

    // Prüfe ob Enemy gerade angreift (aus last_action)
    if (status.last_enemy_action === 'attack') {
      return 'enemy_attacking'; // DEFEND ist gut hier
    }

    // Default
    if (status.turn_count % 2 === 0) {
      return 'idle';
    } else {
      return 'preparing';
    }
  }
}

// Singleton Instance - Global verfügbar
window.battleAPI = new BattleAPI();
