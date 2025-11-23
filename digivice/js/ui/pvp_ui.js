/**
 * PvP UI - Najika World
 * =====================
 *
 * UI for PvP System (3 Modi + Mercy)
 *
 * Features:
 * - Mode Selection Dialog
 * - Mercy Confirmation (Double-Confirmation!)
 * - Battle Results
 * - PvP Stats Display
 *
 * Copyright: Najika World
 * Author: Claude Code (CLI)
 * Date: 2025-11-17
 */

class PvPUI {
  constructor() {
    this.apiBase = '/api/pvp';
    this.currentBattle = null;
    this.playerInventory = [];

    this.init();
  }

  init() {
    this.createUI();
    this.attachEventListeners();
  }

  createUI() {
    // Main PvP Container
    const pvpContainer = document.createElement('div');
    pvpContainer.id = 'pvp-container';
    pvpContainer.className = 'pvp-container hidden';
    pvpContainer.innerHTML = `
      <div class="pvp-modal">
        <!-- Mode Selection -->
        <div class="pvp-mode-selection" id="pvp-mode-selection">
          <h2>PvP Mode wählen</h2>
          <div class="mode-cards">
            <div class="mode-card hardcore" data-mode="hardcore">
              <h3>🔥 HARDCORE</h3>
              <p class="mode-desc">Permadeath oder Mercy</p>
              <ul>
                <li>Alles-abgeben-um-zu-leben Option</li>
                <li>7 Tage PvP-Sperre nach Mercy</li>
                <li>Höchstes Risiko, höchste Belohnung</li>
              </ul>
              <button class="mode-btn btn-hardcore">HARDCORE wählen</button>
            </div>

            <div class="mode-card normal" data-mode="normal">
              <h3>⚔️ NORMAL</h3>
              <p class="mode-desc">1 Item Verlust</p>
              <ul>
                <li>Gewinner wählt 1 Item</li>
                <li>Kein Permadeath</li>
                <li>Balanciertes Risiko</li>
              </ul>
              <button class="mode-btn btn-normal">NORMAL wählen</button>
            </div>

            <div class="mode-card softy" data-mode="softy">
              <h3>🏆 SOFTY</h3>
              <p class="mode-desc">Nur Ranking</p>
              <ul>
                <li>Keine Item-Verluste</li>
                <li>Rating ±10/5</li>
                <li>Spaß ohne Risiko</li>
              </ul>
              <button class="mode-btn btn-softy">SOFTY wählen</button>
            </div>
          </div>
          <button class="close-btn">Abbrechen</button>
        </div>

        <!-- Mercy Dialog -->
        <div class="pvp-mercy-dialog hidden" id="pvp-mercy-dialog">
          <h2>⚠️ NIEDERLAGE! ⚠️</h2>
          <p class="mercy-text">Du wurdest besiegt!</p>

          <div class="mercy-options">
            <div class="option-card option-mercy">
              <h3>💰 ALLES GEBEN um zu LEBEN</h3>
              <p>Du gibst ALLES ab und überlebst</p>
              <ul id="mercy-items-list">
                <!-- Items werden hier eingefügt -->
              </ul>
              <p class="warning">⚠️ 7 Tage PvP-Sperre!</p>
              <button class="mercy-btn btn-accept-mercy">Mercy anbieten</button>
            </div>

            <div class="option-card option-death">
              <h3>💀 Kämpfe bis zum Tod</h3>
              <p>Permadeath akzeptieren</p>
              <p class="warning">⚠️ Character unwiederbringlich verloren!</p>
              <button class="mercy-btn btn-refuse-mercy">Sterben</button>
            </div>
          </div>
        </div>

        <!-- Mercy Confirmation (Double!) -->
        <div class="pvp-mercy-confirm hidden" id="pvp-mercy-confirm">
          <h2>⚠️ BESTÄTIGUNG <span id="confirm-step">1</span>/2 ⚠️</h2>
          <div class="confirm-content">
            <p class="confirm-text" id="confirm-text"></p>
            <div class="items-lost" id="items-lost-list"></div>
            <input
              type="text"
              id="confirm-input"
              placeholder="Tippe 'JA' um zu bestätigen"
              class="confirm-input"
            />
            <button class="confirm-btn" id="confirm-btn">Bestätigen</button>
            <button class="cancel-btn" id="cancel-btn">Abbrechen</button>
          </div>
        </div>

        <!-- Battle Results -->
        <div class="pvp-results hidden" id="pvp-results">
          <h2 class="result-title" id="result-title"></h2>
          <div class="result-content">
            <div class="result-items" id="result-items"></div>
            <div class="result-stats" id="result-stats"></div>
          </div>
          <button class="close-btn">Schließen</button>
        </div>

        <!-- Stats Display -->
        <div class="pvp-stats hidden" id="pvp-stats">
          <h2>📊 PvP Statistiken</h2>
          <div class="stats-grid">
            <div class="stat-item">
              <span class="stat-label">Wins:</span>
              <span class="stat-value" id="stat-wins">0</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Losses:</span>
              <span class="stat-value" id="stat-losses">0</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Win Rate:</span>
              <span class="stat-value" id="stat-winrate">0%</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Mercy Count (7d):</span>
              <span class="stat-value" id="stat-mercy">0</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Rating:</span>
              <span class="stat-value" id="stat-rating">1000</span>
            </div>
          </div>
          <button class="close-btn">Schließen</button>
        </div>
      </div>

      <!-- Compact HUD Overlay -->
      <div class="pvp-hud hidden" id="pvp-hud">
        <div class="pvp-mode-indicator" id="pvp-mode-indicator">
          <span class="mode-badge">PvP: <span id="current-mode">NORMAL</span></span>
        </div>
      </div>
    `;

    document.body.appendChild(pvpContainer);
  }

  attachEventListeners() {
    // Mode Selection
    document.querySelectorAll('.mode-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const mode = e.target.closest('.mode-card').dataset.mode;
        this.selectMode(mode);
      });
    });

    // Mercy Dialog
    document.querySelector('.btn-accept-mercy')?.addEventListener('click', () => {
      this.offerMercy();
    });

    document.querySelector('.btn-refuse-mercy')?.addEventListener('click', () => {
      this.refuseMercy();
    });

    // Confirmation
    document.getElementById('confirm-btn')?.addEventListener('click', () => {
      this.confirmMercy();
    });

    document.getElementById('cancel-btn')?.addEventListener('click', () => {
      this.cancelMercy();
    });

    // Close buttons
    document.querySelectorAll('.close-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        this.hide();
      });
    });
  }

  // ========================================================================
  // MODE SELECTION
  // ========================================================================

  showModeSelection() {
    document.getElementById('pvp-container').classList.remove('hidden');
    document.getElementById('pvp-mode-selection').classList.remove('hidden');
  }

  async selectMode(mode) {
    console.log(`PvP Mode selected: ${mode}`);

    // Update HUD
    document.getElementById('current-mode').textContent = mode.toUpperCase();
    document.getElementById('pvp-hud').classList.remove('hidden');

    // Hide mode selection
    document.getElementById('pvp-mode-selection').classList.add('hidden');
    document.getElementById('pvp-container').classList.add('hidden');
  }

  // ========================================================================
  // MERCY SYSTEM
  // ========================================================================

  showMercyDialog(battleId, playerInventory) {
    this.currentBattle = battleId;
    this.playerInventory = playerInventory;

    // Show items that will be lost
    const itemsList = document.getElementById('mercy-items-list');
    itemsList.innerHTML = playerInventory.map(item =>
      `<li>${item.name} (${item.rarity})</li>`
    ).join('');

    // Show dialog
    document.getElementById('pvp-container').classList.remove('hidden');
    document.getElementById('pvp-mercy-dialog').classList.remove('hidden');
  }

  async offerMercy() {
    // Hide mercy dialog
    document.getElementById('pvp-mercy-dialog').classList.add('hidden');

    // Show double-confirmation
    this.showMercyConfirmation(1);
  }

  async refuseMercy() {
    // Player accepts permadeath
    const confirmed = confirm('⚠️ Du wirst PERMANENT sterben! Bist du sicher?');

    if (confirmed) {
      try {
        const response = await fetch(`${this.apiBase}/mercy/decide`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            battle_id: this.currentBattle,
            player_id: 1, // TODO: Get from game state
            accept_mercy: false,
            player_inventory: []
          })
        });

        const result = await response.json();

        if (result.permadeath) {
          this.showPermadeath();
        }

      } catch (error) {
        console.error('Fehler beim Mercy-Ablehnen:', error);
      }
    }
  }

  showMercyConfirmation(step) {
    const confirmDialog = document.getElementById('pvp-mercy-confirm');
    const confirmText = document.getElementById('confirm-text');
    const confirmStep = document.getElementById('confirm-step');
    const itemsList = document.getElementById('items-lost-list');

    confirmStep.textContent = step;

    if (step === 1) {
      confirmText.innerHTML = `
        Du wirst <strong>ALLES</strong> verlieren:<br/>
        - ${this.playerInventory.length} Ausrüstungsteile<br/>
        - 7 Tage PvP-Sperre<br/><br/>
        Tippe 'JA' um zu bestätigen.
      `;

      itemsList.innerHTML = this.playerInventory.map(item =>
        `<div class="lost-item">${item.name}</div>`
      ).join('');

    } else if (step === 2) {
      confirmText.innerHTML = `
        <strong>LETZTE CHANCE!</strong><br/>
        Dies ist FINAL und kann NICHT rückgängig gemacht werden!<br/><br/>
        Tippe nochmal 'JA' um ENDGÜLTIG zu bestätigen.
      `;
    }

    confirmDialog.classList.remove('hidden');
  }

  async confirmMercy() {
    const input = document.getElementById('confirm-input');
    const step = parseInt(document.getElementById('confirm-step').textContent);

    if (input.value.toUpperCase() !== 'JA') {
      alert('❌ Du musst "JA" tippen!');
      return;
    }

    input.value = '';

    if (step === 1) {
      // Show step 2
      this.showMercyConfirmation(2);

    } else if (step === 2) {
      // Final confirmation - execute mercy
      try {
        const response = await fetch(`${this.apiBase}/mercy/decide`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            battle_id: this.currentBattle,
            player_id: 1, // TODO: Get from game state
            accept_mercy: true,
            player_inventory: this.playerInventory
          })
        });

        const result = await response.json();

        // Hide confirmation
        document.getElementById('pvp-mercy-confirm').classList.add('hidden');

        // Show result
        this.showMercyResult(result);

      } catch (error) {
        console.error('Fehler beim Mercy-Bestätigen:', error);
      }
    }
  }

  cancelMercy() {
    document.getElementById('pvp-mercy-confirm').classList.add('hidden');
    document.getElementById('pvp-mercy-dialog').classList.remove('hidden');
  }

  // ========================================================================
  // RESULTS
  // ========================================================================

  showMercyResult(result) {
    const resultsDiv = document.getElementById('pvp-results');
    const titleDiv = document.getElementById('result-title');
    const itemsDiv = document.getElementById('result-items');
    const statsDiv = document.getElementById('result-stats');

    titleDiv.textContent = '💔 Mercy Akzeptiert';

    itemsDiv.innerHTML = `
      <h3>Verlorene Items:</h3>
      <ul>
        ${result.items_lost.map(item => `<li>${item.name}</li>`).join('')}
      </ul>
    `;

    statsDiv.innerHTML = `
      <p class="mercy-info">⏳ PvP-Sperre bis: ${result.pvp_cooldown_until}</p>
      <p class="mercy-info">📊 Mercy Count (7d): ${result.mercy_count_7d}</p>
    `;

    resultsDiv.classList.remove('hidden');
  }

  showPermadeath() {
    alert('💀 Du bist gestorben. Character permanent verloren.');
    // TODO: Handle character deletion
  }

  showBattleResult(winner, mode, itemsWon = []) {
    const resultsDiv = document.getElementById('pvp-results');
    const titleDiv = document.getElementById('result-title');
    const itemsDiv = document.getElementById('result-items');
    const statsDiv = document.getElementById('result-stats');

    titleDiv.textContent = winner ? '🎉 SIEG!' : '💔 NIEDERLAGE';

    if (mode === 'normal' && itemsWon.length > 0) {
      itemsDiv.innerHTML = `
        <h3>Gewonnene Items:</h3>
        <ul>
          ${itemsWon.map(item => `<li>${item.name}</li>`).join('')}
        </ul>
      `;
    } else if (mode === 'softy') {
      statsDiv.innerHTML = `<p>Rating: ${winner ? '+10' : '-5'}</p>`;
    }

    document.getElementById('pvp-container').classList.remove('hidden');
    resultsDiv.classList.remove('hidden');
  }

  // ========================================================================
  // STATS
  // ========================================================================

  async loadStats(playerId) {
    try {
      const response = await fetch(`${this.apiBase}/stats/${playerId}`);
      const stats = await response.json();

      document.getElementById('stat-wins').textContent = stats.wins;
      document.getElementById('stat-losses').textContent = stats.losses;
      document.getElementById('stat-winrate').textContent =
        `${((stats.wins / (stats.wins + stats.losses)) * 100).toFixed(1)}%`;
      document.getElementById('stat-mercy').textContent = stats.mercy_count_7d;
      document.getElementById('stat-rating').textContent = stats.rating || 1000;

      document.getElementById('pvp-container').classList.remove('hidden');
      document.getElementById('pvp-stats').classList.remove('hidden');

    } catch (error) {
      console.error('Fehler beim Laden der Stats:', error);
    }
  }

  // ========================================================================
  // UTILITY
  // ========================================================================

  hide() {
    document.getElementById('pvp-container').classList.add('hidden');
    document.querySelectorAll('.pvp-modal > div').forEach(div => {
      div.classList.add('hidden');
    });
  }
}

// Auto-initialize
window.addEventListener('DOMContentLoaded', () => {
  window.pvpUI = new PvPUI();
});
