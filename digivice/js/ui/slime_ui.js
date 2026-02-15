/**
 * Slime UI - Najika World
 * ========================
 *
 * Minimal Tamagotchi Interface for Slime Companion
 *
 * Features:
 * - Needs Display (Hunger, Thirst, Sleep, Mood, Battlel ust)
 * - Care Actions (Feed, Water, Sleep, Play, Battle)
 * - Evolution Display (Tier → Slime → Rainbow)
 * - Moveset Display
 * - Color Collection Tracker
 *
 * Copyright: Najika World
 * Author: Claude Code (CLI)
 * Date: 2025-11-17
 */

class SlimeUI {
  constructor() {
    this.apiBase = 'http://localhost:8001/api/slime';
    this.companionId = null;
    this.updateInterval = null;

    this.init();
  }

  init() {
    this.createUI();
    this.attachEventListeners();
  }

  createUI() {
    const slimeContainer = document.createElement('div');
    slimeContainer.id = 'slime-container';
    slimeContainer.className = 'slime-container';
    slimeContainer.innerHTML = `
      <!-- Compact Slime HUD -->
      <div class="slime-hud hidden" id="slime-hud">
        <div class="slime-avatar" id="slime-avatar">
          <img src="/assets/slime_default.png" alt="Slime" id="slime-image" />
          <span class="slime-level" id="slime-level">Lv 1</span>
        </div>

        <div class="slime-needs-mini">
          <div class="need-bar">
            <span class="need-icon">🍖</span>
            <div class="need-progress">
              <div class="need-fill hunger-fill" id="hunger-mini" style="width: 100%"></div>
            </div>
          </div>
          <div class="need-bar">
            <span class="need-icon">💧</span>
            <div class="need-progress">
              <div class="need-fill thirst-fill" id="thirst-mini" style="width: 100%"></div>
            </div>
          </div>
          <div class="need-bar">
            <span class="need-icon">😊</span>
            <div class="need-progress">
              <div class="need-fill mood-fill" id="mood-mini" style="width: 100%"></div>
            </div>
          </div>
        </div>

        <button class="slime-toggle-btn" id="slime-toggle-btn">▼</button>
      </div>

      <!-- Full Slime Panel -->
      <div class="slime-panel hidden" id="slime-panel">
        <div class="panel-header">
          <h2 id="slime-name">Dein Slime</h2>
          <button class="panel-close-btn" id="panel-close-btn">×</button>
        </div>

        <div class="panel-content">
          <!-- Evolution Display -->
          <div class="evolution-display">
            <div class="evo-stage" id="evo-stage">
              <span class="stage-label">Form:</span>
              <span class="stage-value" id="current-form">Tier</span>
            </div>
            <div class="evo-progress">
              <span>Level: <strong id="companion-level">1</strong></span>
              <span class="metamorphosis-hint" id="meta-hint">
                (Level 50 + Event für Metamorphose)
              </span>
            </div>
            <div class="slime-color-display hidden" id="color-display">
              <span>Farbe: <strong id="slime-color">-</strong></span>
            </div>
          </div>

          <!-- Needs Display -->
          <div class="needs-display">
            <h3>Bedürfnisse</h3>

            <div class="need-item">
              <div class="need-header">
                <span class="need-icon">🍖</span>
                <span class="need-label">Hunger</span>
                <span class="need-value" id="hunger-value">100%</span>
              </div>
              <div class="need-bar-full">
                <div class="need-fill-full hunger-fill" id="hunger-bar" style="width: 100%"></div>
              </div>
              <button class="care-btn" data-action="feed">Füttern</button>
            </div>

            <div class="need-item">
              <div class="need-header">
                <span class="need-icon">💧</span>
                <span class="need-label">Durst</span>
                <span class="need-value" id="thirst-value">100%</span>
              </div>
              <div class="need-bar-full">
                <div class="need-fill-full thirst-fill" id="thirst-bar" style="width: 100%"></div>
              </div>
              <button class="care-btn" data-action="water">Wasser geben</button>
            </div>

            <div class="need-item">
              <div class="need-header">
                <span class="need-icon">😴</span>
                <span class="need-label">Schlaf</span>
                <span class="need-value" id="sleep-value">100%</span>
              </div>
              <div class="need-bar-full">
                <div class="need-fill-full sleep-fill" id="sleep-bar" style="width: 100%"></div>
              </div>
              <button class="care-btn" data-action="sleep">Schlafen lassen</button>
            </div>

            <div class="need-item">
              <div class="need-header">
                <span class="need-icon">😊</span>
                <span class="need-label">Stimmung</span>
                <span class="need-value" id="mood-value">100%</span>
              </div>
              <div class="need-bar-full">
                <div class="need-fill-full mood-fill" id="mood-bar" style="width: 100%"></div>
              </div>
              <button class="care-btn" data-action="play">Spielen</button>
            </div>

            <div class="need-item">
              <div class="need-header">
                <span class="need-icon">⚔️</span>
                <span class="need-label">Kampfeslust</span>
                <span class="need-value" id="battleust-value">0%</span>
              </div>
              <div class="need-bar-full">
                <div class="need-fill-full battleust-fill" id="battleust-bar" style="width: 0%"></div>
              </div>
              <p class="battleust-info">(Steigt im Kampf)</p>
            </div>
          </div>

          <!-- Moveset Display -->
          <div class="moveset-display">
            <h3>Moveset (<span id="move-count">0</span>/20)</h3>
            <div class="moves-grid" id="moves-grid">
              <!-- Moves werden hier eingefügt -->
            </div>
          </div>

          <!-- Color Collection -->
          <div class="color-collection hidden" id="color-collection">
            <h3>Farb-Sammlung (Rainbow-Quest)</h3>
            <div class="colors-grid" id="colors-grid">
              <!-- Colors werden hier eingefügt -->
            </div>
          </div>

          <!-- Rescue Status -->
          <div class="rescue-status hidden" id="rescue-status">
            <h3>🛡️ Rettung (Hardcore)</h3>
            <p id="rescue-text">Verfügbar: 1x / 24h</p>
            <p class="rescue-cooldown hidden" id="rescue-cooldown">
              Nächste Rettung: <span id="rescue-timer">-</span>
            </p>
          </div>
        </div>
      </div>
    `;

    document.body.appendChild(slimeContainer);
  }

  attachEventListeners() {
    // Toggle button
    document.getElementById('slime-toggle-btn')?.addEventListener('click', () => {
      this.togglePanel();
    });

    // Close button
    document.getElementById('panel-close-btn')?.addEventListener('click', () => {
      this.hidePanel();
    });

    // Care actions
    document.querySelectorAll('.care-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const action = e.target.dataset.action;
        this.performCareAction(action);
      });
    });
  }

  // ========================================================================
  // COMPANION MANAGEMENT
  // ========================================================================

  async loadCompanion(companionId) {
    this.companionId = companionId;

    try {
      const response = await fetch(`${this.apiBase}/companion/${companionId}`);
      const companion = await response.json();

      this.updateDisplay(companion);

      // Show HUD
      document.getElementById('slime-hud').classList.remove('hidden');

      // Start auto-update
      this.startAutoUpdate();

    } catch (error) {
      console.error('Fehler beim Laden des Companions:', error);
    }
  }

  updateDisplay(companion) {
    // Name & Level
    document.getElementById('slime-name').textContent = companion.name || 'Dein Slime';
    document.getElementById('slime-level').textContent = `Lv ${companion.level}`;
    document.getElementById('companion-level').textContent = companion.level;

    // Form (Tier / Slime)
    document.getElementById('current-form').textContent =
      companion.metamorphosed ? 'Slime' : 'Tier';

    // Color (nur bei Slime-Form)
    if (companion.metamorphosed && companion.color) {
      document.getElementById('color-display').classList.remove('hidden');
      document.getElementById('slime-color').textContent = companion.color;
    }

    // Needs
    this.updateNeed('hunger', companion.needs.hunger);
    this.updateNeed('thirst', companion.needs.thirst);
    this.updateNeed('sleep', companion.needs.schlaf);
    this.updateNeed('mood', companion.needs.stimmung);
    this.updateNeed('battleust', companion.needs.kampfeslust);

    // Moveset
    this.updateMoveset(companion.moves);

    // Color Collection (nur bei Slime)
    if (companion.metamorphosed) {
      this.updateColorCollection(companion.collected_colors || []);
    }

    // Rescue Status (nur Hardcore + Slime)
    if (companion.is_hardcore && companion.metamorphosed) {
      this.updateRescueStatus(companion.rescue_available, companion.rescue_cooldown_until);
    }
  }

  updateNeed(need, value) {
    const percentage = Math.max(0, Math.min(100, value));

    // Full bars
    document.getElementById(`${need}-value`).textContent = `${Math.round(percentage)}%`;
    document.getElementById(`${need}-bar`).style.width = `${percentage}%`;

    // Mini bars (HUD)
    const miniBar = document.getElementById(`${need}-mini`);
    if (miniBar) {
      miniBar.style.width = `${percentage}%`;
    }

    // Warning colors
    const bar = document.getElementById(`${need}-bar`);
    if (percentage < 30) {
      bar.classList.add('critical');
    } else if (percentage < 50) {
      bar.classList.add('warning');
    } else {
      bar.classList.remove('critical', 'warning');
    }
  }

  updateMoveset(moves) {
    const movesGrid = document.getElementById('moves-grid');
    document.getElementById('move-count').textContent = moves.length;

    movesGrid.innerHTML = moves.map(move => `
      <div class="move-card">
        <span class="move-name">${move.name}</span>
        <span class="move-type">${move.type}</span>
        <span class="move-source">${move.learned_from}</span>
      </div>
    `).join('');
  }

  updateColorCollection(collectedColors) {
    const colorsGrid = document.getElementById('colors-grid');
    document.getElementById('color-collection').classList.remove('hidden');

    const allColors = [
      'moss_green', 'crystal_white', 'amethyst', 'onyx',
      'perle', 'rubin', 'azur', 'bernstein'
    ];

    colorsGrid.innerHTML = allColors.map(color => {
      const collected = collectedColors.includes(color);
      return `
        <div class="color-badge ${collected ? 'collected' : 'locked'}">
          <div class="color-dot" data-color="${color}"></div>
          <span class="color-name">${color}</span>
          ${collected ? '✓' : '🔒'}
        </div>
      `;
    }).join('');

    // Check for Rainbow
    if (collectedColors.length === 8) {
      colorsGrid.innerHTML += `
        <div class="color-badge rainbow collected">
          <div class="color-dot rainbow"></div>
          <span class="color-name">RAINBOW</span>
          ✓
        </div>
      `;
    }
  }

  updateRescueStatus(available, cooldownUntil) {
    document.getElementById('rescue-status').classList.remove('hidden');

    if (available) {
      document.getElementById('rescue-text').textContent = '✅ Rettung verfügbar!';
      document.getElementById('rescue-cooldown').classList.add('hidden');
    } else {
      document.getElementById('rescue-text').textContent = '⏳ Rettung auf Cooldown';
      document.getElementById('rescue-cooldown').classList.remove('hidden');
      document.getElementById('rescue-timer').textContent = cooldownUntil;
    }
  }

  // ========================================================================
  // CARE ACTIONS
  // ========================================================================

  async performCareAction(action) {
    if (!this.companionId) return;

    try {
      const response = await fetch(`${this.apiBase}/care`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          companion_id: this.companionId,
          action
        })
      });

      const result = await response.json();

      if (result.success) {
        // Update display with new values
        this.updateDisplay(result.companion);

        // Show feedback
        this.showFeedback(result.message);
      } else {
        if (typeof notify === 'function') notify(`❌ ${result.error}`, 'error');
      }

    } catch (error) {
      console.error(`Fehler bei ${action}:`, error);
    }
  }

  showFeedback(message) {
    if (typeof notify === 'function') {
      notify(`✅ ${message}`, 'success');
    } else {
      console.log(`✅ ${message}`);
    }
  }

  // ========================================================================
  // PANEL MANAGEMENT
  // ========================================================================

  togglePanel() {
    const panel = document.getElementById('slime-panel');
    panel.classList.toggle('hidden');

    const toggleBtn = document.getElementById('slime-toggle-btn');
    toggleBtn.textContent = panel.classList.contains('hidden') ? '▼' : '▲';
  }

  hidePanel() {
    document.getElementById('slime-panel').classList.add('hidden');
    document.getElementById('slime-toggle-btn').textContent = '▼';
  }

  // ========================================================================
  // AUTO-UPDATE
  // ========================================================================

  startAutoUpdate() {
    // Update every 10 seconds
    this.updateInterval = setInterval(async () => {
      if (this.companionId) {
        try {
          const response = await fetch(`${this.apiBase}/companion/${this.companionId}`);
          const companion = await response.json();
          this.updateDisplay(companion);
        } catch (error) {
          console.error('Auto-Update Fehler:', error);
        }
      }
    }, 10000);
  }

  stopAutoUpdate() {
    if (this.updateInterval) {
      clearInterval(this.updateInterval);
      this.updateInterval = null;
    }
  }
}

// Auto-initialize
window.addEventListener('DOMContentLoaded', () => {
  window.slimeUI = new SlimeUI();
});
