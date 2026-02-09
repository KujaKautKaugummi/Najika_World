/**
 * Game Systems UI - Najika World
 * ================================
 *
 * Unified UI for:
 * - Region Boss (Gebietsherrscher)
 * - Oregon Events (Konosuba Touch)
 * - Magic Schools (9 Schools)
 * - Instrument Playing (Mundharmonika)
 * - World Info (Weather, Time, etc.)
 *
 * Copyright: Najika World
 * Author: Claude Code (CLI)
 * Date: 2025-11-17
 */

// ============================================================================
// REGION BOSS UI
// ============================================================================

class RegionBossUI {
  constructor() {
    this.apiBase = 'http://localhost:8000/api/region-boss';
    this.createUI();
  }

  createUI() {
    const container = document.createElement('div');
    container.id = 'boss-ui-container';
    container.className = 'boss-ui-container hidden';
    container.innerHTML = `
      <div class="boss-modal">
        <h2>⚔️ Gebietsherrscher</h2>

        <!-- Region Overview -->
        <div class="boss-regions-grid" id="boss-regions">
          <!-- Regions werden dynamisch geladen -->
        </div>

        <!-- Challenge Dialog -->
        <div class="boss-challenge-dialog hidden" id="boss-challenge">
          <h3>Challenge erstellen</h3>
          <select id="challenge-type">
            <option value="krieg">⚔️ Krieg (PvP)</option>
            <option value="handel">💰 Handel (Wirtschaft)</option>
            <option value="diplomatie">🤝 Diplomatie (Politik)</option>
            <option value="quest_line">📜 Quest-Line (PvE)</option>
          </select>
          <button id="create-challenge-btn">Challenge starten</button>
        </div>

        <!-- Ultimate Ruler Display -->
        <div class="ultimate-ruler hidden" id="ultimate-ruler">
          <h3>👑 Ultimate Herrscher</h3>
          <p id="ultimate-name">-</p>
        </div>

        <button class="close-btn">Schließen</button>
      </div>
    `;
    document.body.appendChild(container);

    this.attachListeners();
  }

  attachListeners() {
    document.querySelector('#boss-ui-container .close-btn')?.addEventListener('click', () => {
      this.hide();
    });
  }

  async show() {
    await this.loadRegions();
    await this.loadUltimateRuler();
    document.getElementById('boss-ui-container').classList.remove('hidden');
  }

  async loadRegions() {
    try {
      const response = await fetch(`${this.apiBase}/state/export`);
      const state = await response.json();

      const regionsDiv = document.getElementById('boss-regions');
      if (regionsDiv) {
        regionsDiv.innerHTML = '';

        if (state && state.region_bosses && typeof state.region_bosses === 'object') {
          for (const [region, boss] of Object.entries(state.region_bosses)) {
            const card = document.createElement('div');
            card.className = 'boss-region-card';
            card.innerHTML = `
              <h4>${region}</h4>
              <p class="boss-name">${boss ? `Boss: ${boss.player_id}` : 'Kein Boss'}</p>
              ${boss ? `
                <p>Tax: ${boss.tax_rate}%</p>
                <p>Seit: ${boss.crowned_at}</p>
              ` : `
                <button class="challenge-btn" data-region="${region}">Herausfordern</button>
              `}
            `;
            regionsDiv.appendChild(card);
          }
        } else {
          // Fallback if backend offline or no data
          regionsDiv.innerHTML = '<p>⚠️ Keine Regionen verfügbar (Backend offline)</p>';
        }
      }
    } catch (error) {
      console.error('Fehler beim Laden der Regionen:', error);
      const regionsDiv = document.getElementById('boss-regions');
      if (regionsDiv) {
        regionsDiv.innerHTML = '<p>⚠️ Fehler beim Laden der Regionen</p>';
      }
    }
  }

  async loadUltimateRuler() {
    try {
      const response = await fetch(`${this.apiBase}/ultimate`);
      const data = await response.json();

      if (data.ultimate_ruler) {
        document.getElementById('ultimate-ruler').classList.remove('hidden');
        document.getElementById('ultimate-name').textContent =
          `${data.ultimate_ruler.player_id} - ${data.ultimate_ruler.regions_controlled} Regionen`;
      }
    } catch (error) {
      console.error('Fehler beim Laden des Ultimate Rulers:', error);
    }
  }

  hide() {
    document.getElementById('boss-ui-container').classList.add('hidden');
  }
}

// ============================================================================
// OREGON EVENTS UI
// ============================================================================

class OregonEventsUI {
  constructor() {
    this.apiBase = 'http://localhost:8000/api/oregon';
    this.currentEvent = null;
    this.createUI();
  }

  createUI() {
    const container = document.createElement('div');
    container.id = 'oregon-ui-container';
    container.className = 'oregon-ui-container hidden';
    container.innerHTML = `
      <div class="oregon-modal">
        <h2 id="oregon-title">Oregon Trail Event</h2>

        <div class="oregon-content">
          <p class="oregon-text" id="oregon-text"></p>

          <!-- Najika Reaction -->
          <div class="najika-reaction hidden" id="najika-reaction">
            <img src="/assets/najika_avatar.png" alt="Najika" class="najika-avatar" />
            <p class="najika-quote" id="najika-quote"></p>
          </div>

          <!-- Choices -->
          <div class="oregon-choices" id="oregon-choices">
            <!-- Choices werden hier eingefügt -->
          </div>

          <!-- Option E: Lass Najika entscheiden -->
          <button class="najika-decide-btn" id="najika-decide-btn">
            🎲 Lass Najika entscheiden
          </button>

          <!-- Result -->
          <div class="oregon-result hidden" id="oregon-result">
            <h3>Konsequenz:</h3>
            <p id="result-text"></p>
            <div id="result-effects"></div>
            <button class="continue-btn" id="continue-btn">Weiter</button>
          </div>
        </div>

        <!-- Chaos Display -->
        <div class="chaos-display">
          <span>Chaos Level: <strong id="chaos-level">1</strong></span>
          <div class="chaos-bar">
            <div class="chaos-fill" id="chaos-fill" style="width: 10%"></div>
          </div>
          <span class="chaos-points" id="chaos-points">0 / 100</span>
        </div>
      </div>
    `;
    document.body.appendChild(container);

    this.attachListeners();
  }

  attachListeners() {
    document.getElementById('najika-decide-btn')?.addEventListener('click', () => {
      this.najikaDecide();
    });

    document.getElementById('continue-btn')?.addEventListener('click', () => {
      this.hide();
    });
  }

  async show() {
    // Show the UI container
    const container = document.getElementById('oregon-ui-container');
    if (container) {
      container.classList.remove('hidden');
    }

    // Start a random event
    try {
      const response = await fetch(`${this.apiBase}/random`);
      if (response.ok) {
        const event = await response.json();
        await this.showEvent(event);
      } else {
        // Fallback: Show dummy event if backend offline
        this.showEvent({
          title: "Händler-Karawane",
          text: "Eine Karawane bietet dir ihre Waren an.",
          options: [
            { text: "Kaufen", effect: { gold: -10, items: 1 } },
            { text: "Ablehnen", effect: {} }
          ],
          najika_reaction: "*kicher* Die haben glänzende Sachen, Puddin'!"
        });
      }
    } catch (error) {
      console.error('Error loading Oregon event:', error);
    }
  }

  async showEvent(event) {
    this.currentEvent = event;

    document.getElementById('oregon-title').textContent = event.title;
    document.getElementById('oregon-text').textContent = event.text;

    // Najika Reaction
    if (event.najika_reaction) {
      document.getElementById('najika-reaction').classList.remove('hidden');
      document.getElementById('najika-quote').textContent = event.najika_reaction;
    }

    // Choices
    const choicesDiv = document.getElementById('oregon-choices');
    choicesDiv.innerHTML = event.options.map((opt, idx) => `
      <button class="choice-btn" data-index="${idx}">
        ${String.fromCharCode(65 + idx)}) ${opt.text}
      </button>
    `).join('');

    // Choice listeners
    document.querySelectorAll('.choice-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const index = parseInt(e.target.dataset.index);
        this.selectChoice(index);
      });
    });

    // Update chaos display
    await this.updateChaosDisplay();

    // Show modal
    document.getElementById('oregon-ui-container').classList.remove('hidden');
  }

  async selectChoice(choiceIndex) {
    try {
      const response = await fetch(`${this.apiBase}/choice`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          choice_index: choiceIndex,
          player_state: {} // TODO: Get from game state
        })
      });

      const result = await response.json();
      this.showResult(result);

    } catch (error) {
      console.error('Fehler bei Choice:', error);
    }
  }

  async najikaDecide() {
    // Najika entscheidet automatisch (backend wählt basierend auf Persönlichkeit)
    const randomChoice = Math.floor(Math.random() * this.currentEvent.options.length);
    await this.selectChoice(randomChoice);
  }

  showResult(result) {
    // Hide choices
    document.getElementById('oregon-choices').classList.add('hidden');
    document.getElementById('najika-decide-btn').classList.add('hidden');

    // Show result
    document.getElementById('oregon-result').classList.remove('hidden');
    document.getElementById('result-text').textContent = result.outcome;

    const effectsDiv = document.getElementById('result-effects');
    effectsDiv.innerHTML = Object.entries(result.effects || {}).map(([key, value]) => `
      <div class="effect-item">
        <span>${key}:</span> <span class="${value > 0 ? 'positive' : 'negative'}">${value > 0 ? '+' : ''}${value}</span>
      </div>
    `).join('');
  }

  async updateChaosDisplay() {
    try {
      const response = await fetch(`${this.apiBase}/chaos`);
      const data = await response.json();

      document.getElementById('chaos-level').textContent = data.level;
      document.getElementById('chaos-points').textContent = `${data.chaos_points} / 100`;
      document.getElementById('chaos-fill').style.width = `${data.chaos_points}%`;

    } catch (error) {
      console.error('Fehler beim Laden des Chaos:', error);
    }
  }

  hide() {
    document.getElementById('oregon-ui-container').classList.add('hidden');
  }
}

// ============================================================================
// MAGIC SCHOOLS UI
// ============================================================================

class MagicSchoolsUI {
  constructor() {
    this.apiBase = 'http://localhost:8000/api/magic';
    this.createUI();
  }

  createUI() {
    const container = document.createElement('div');
    container.id = 'magic-ui-container';
    container.className = 'magic-ui-container hidden';
    container.innerHTML = `
      <div class="magic-modal">
        <h2>🔮 Magieschulen</h2>

        <!-- School Selection -->
        <div class="magic-schools-grid" id="magic-schools">
          <!-- Schools werden hier eingefügt -->
        </div>

        <!-- Spell Casting -->
        <div class="spell-casting hidden" id="spell-casting">
          <h3 id="selected-school">Feuer</h3>
          <div class="spells-list" id="spells-list">
            <!-- Spells werden hier eingefügt -->
          </div>
          <button class="back-btn" id="back-to-schools">Zurück</button>
        </div>

        <button class="close-btn">Schließen</button>
      </div>
    `;
    document.body.appendChild(container);

    this.attachListeners();
  }

  attachListeners() {
    document.querySelector('#magic-ui-container .close-btn')?.addEventListener('click', () => {
      this.hide();
    });

    document.getElementById('back-to-schools')?.addEventListener('click', () => {
      document.getElementById('spell-casting').classList.add('hidden');
      document.getElementById('magic-schools').classList.remove('hidden');
    });
  }

  async show() {
    await this.loadSchools();
    document.getElementById('magic-ui-container').classList.remove('hidden');
  }

  async loadSchools() {
    try {
      const response = await fetch(`${this.apiBase}/schools`);
      const schools = await response.json();

      const schoolsDiv = document.getElementById('magic-schools');
      if (schoolsDiv) {
        if (schools && schools.schools && Array.isArray(schools.schools)) {
          schoolsDiv.innerHTML = schools.schools.map(school => `
            <div class="magic-school-card" data-school="${school.id}">
              <h3>${school.name}</h3>
              <p>Level: ${school.level || 1}</p>
              <p>XP: ${school.xp || 0}</p>
              <button class="select-school-btn">Wählen</button>
            </div>
          `).join('');

          // School selection listeners
          document.querySelectorAll('.select-school-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
              const school = e.target.closest('.magic-school-card').dataset.school;
              this.selectSchool(school);
            });
          });
        } else {
          // Fallback if backend offline
          schoolsDiv.innerHTML = '<p>⚠️ Keine Magieschulen verfügbar (Backend offline)</p>';
        }
      }

    } catch (error) {
      console.error('Fehler beim Laden der Schulen:', error);
      const schoolsDiv = document.getElementById('magic-schools');
      if (schoolsDiv) {
        schoolsDiv.innerHTML = '<p>⚠️ Fehler beim Laden der Magieschulen</p>';
      }
    }
  }

  async selectSchool(schoolId) {
    try {
      const response = await fetch(`${this.apiBase}/school/${schoolId}/spells`);
      const data = await response.json();

      document.getElementById('selected-school').textContent = data.school_name;

      const spellsList = document.getElementById('spells-list');
      spellsList.innerHTML = data.spells.map(spell => `
        <div class="spell-card ${spell.unlocked ? '' : 'locked'}">
          <h4>${spell.name}</h4>
          <p class="spell-tier">${spell.tier}</p>
          <p class="spell-cost">Mana: ${spell.mana_cost}</p>
          ${spell.unlocked ? `
            <button class="cast-spell-btn" data-spell="${spell.id}">Casten</button>
          ` : `
            <p class="locked-text">🔒 Level ${spell.min_level} erforderlich</p>
          `}
        </div>
      `).join('');

      // Hide schools, show spells
      document.getElementById('magic-schools').classList.add('hidden');
      document.getElementById('spell-casting').classList.remove('hidden');

    } catch (error) {
      console.error('Fehler beim Laden der Spells:', error);
    }
  }

  hide() {
    document.getElementById('magic-ui-container').classList.add('hidden');
  }
}

// ============================================================================
// INSTRUMENT UI
// ============================================================================

class InstrumentUI {
  constructor() {
    this.apiBase = 'http://localhost:8000/api/instrument';
    this.currentInstrument = 'mundharmonika';
    this.createUI();
  }

  createUI() {
    const container = document.createElement('div');
    container.id = 'instrument-ui-container';
    container.className = 'instrument-ui-container hidden';
    container.innerHTML = `
      <div class="instrument-modal">
        <h2>🎵 Instrument spielen</h2>

        <!-- Instrument Selection -->
        <div class="instrument-selector">
          <label>Instrument:</label>
          <select id="instrument-select">
            <option value="mundharmonika">Mundharmonika</option>
            <option value="gitarre">Gitarre</option>
            <option value="klavier">Klavier</option>
            <option value="flöte">Flöte</option>
          </select>
        </div>

        <!-- Note Keyboard -->
        <div class="note-keyboard">
          <button class="note-key" data-note="C" data-octave="4">C</button>
          <button class="note-key black" data-note="C#" data-octave="4">C#</button>
          <button class="note-key" data-note="D" data-octave="4">D</button>
          <button class="note-key black" data-note="D#" data-octave="4">D#</button>
          <button class="note-key" data-note="E" data-octave="4">E</button>
          <button class="note-key" data-note="F" data-octave="4">F</button>
          <button class="note-key black" data-note="F#" data-octave="4">F#</button>
          <button class="note-key" data-note="G" data-octave="4">G</button>
          <button class="note-key black" data-note="G#" data-octave="4">G#</button>
          <button class="note-key" data-note="A" data-octave="4">A</button>
          <button class="note-key black" data-note="A#" data-octave="4">A#</button>
          <button class="note-key" data-note="H" data-octave="4">H</button>
        </div>

        <!-- Octave Control -->
        <div class="octave-control">
          <button id="octave-down">Oktave -</button>
          <span id="current-octave">4</span>
          <button id="octave-up">Oktave +</button>
        </div>

        <!-- Song Selector -->
        <div class="song-selector">
          <h3>Songs lernen</h3>
          <select id="song-select">
            <option value="">-- Song wählen --</option>
          </select>
          <button id="play-song-btn">Song abspielen</button>
        </div>

        <!-- Progress Display -->
        <div class="instrument-progress">
          <p>Level: <strong id="instrument-level">1</strong></p>
          <p>XP: <strong id="instrument-xp">0</strong></p>
          <p>Perfect Notes: <strong id="perfect-notes">0</strong></p>
        </div>

        <button class="close-btn">Schließen</button>
      </div>
    `;
    document.body.appendChild(container);

    this.attachListeners();
  }

  attachListeners() {
    // Note keys
    document.querySelectorAll('.note-key').forEach(key => {
      key.addEventListener('click', (e) => {
        const note = e.target.dataset.note;
        const octave = parseInt(e.target.dataset.octave);
        this.playNote(note, octave);
      });
    });

    // Octave control
    document.getElementById('octave-down')?.addEventListener('click', () => {
      this.changeOctave(-1);
    });

    document.getElementById('octave-up')?.addEventListener('click', () => {
      this.changeOctave(1);
    });

    // Instrument selection
    document.getElementById('instrument-select')?.addEventListener('change', (e) => {
      this.switchInstrument(e.target.value);
    });

    // Song playing
    document.getElementById('play-song-btn')?.addEventListener('click', () => {
      const songId = document.getElementById('song-select').value;
      if (songId) this.playSong(songId);
    });

    // Close
    document.querySelector('#instrument-ui-container .close-btn')?.addEventListener('click', () => {
      this.hide();
    });
  }

  async show() {
    await this.loadSongs();
    await this.loadProgress();
    document.getElementById('instrument-ui-container').classList.remove('hidden');
  }

  async playNote(note, octave) {
    try {
      const response = await fetch(`${this.apiBase}/play-note`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          instrument: this.currentInstrument,
          note,
          octave,
          duration: 0.5,
          velocity: 0.8,
          quality: 'good'
        })
      });

      const result = await response.json();

      // Update progress display
      if (result.level_up) {
        alert(`🎉 Level Up! Neues Level: ${result.level}`);
      }

      this.loadProgress();

      // TODO: Play actual audio

    } catch (error) {
      console.error('Fehler beim Note spielen:', error);
    }
  }

  changeOctave(delta) {
    const octaveSpan = document.getElementById('current-octave');
    let octave = parseInt(octaveSpan.textContent) + delta;
    octave = Math.max(1, Math.min(8, octave));
    octaveSpan.textContent = octave;

    // Update all note keys
    document.querySelectorAll('.note-key').forEach(key => {
      key.dataset.octave = octave;
    });
  }

  async switchInstrument(instrument) {
    try {
      await fetch(`${this.apiBase}/switch`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ instrument })
      });

      this.currentInstrument = instrument;
      console.log(`Instrument gewechselt: ${instrument}`);

    } catch (error) {
      console.error('Fehler beim Instrument wechseln:', error);
    }
  }

  async loadSongs() {
    try {
      const response = await fetch(`${this.apiBase}/songs`);
      const data = await response.json();

      const songSelect = document.getElementById('song-select');
      if (songSelect) {
        if (data && data.songs && Array.isArray(data.songs)) {
          songSelect.innerHTML = '<option value="">-- Song wählen --</option>' +
            data.songs.map(song => `
              <option value="${song.id}">${song.name} (${song.difficulty})</option>
            `).join('');
        } else {
          // Fallback if backend offline or no songs
          songSelect.innerHTML = '<option value="">-- Keine Songs verfügbar --</option>';
        }
      }

    } catch (error) {
      console.error('Fehler beim Laden der Songs:', error);
    }
  }

  async playSong(songId) {
    try {
      const response = await fetch(`${this.apiBase}/play-song`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          song_id: songId,
          note_accuracies: [] // TODO: Implement actual accuracy tracking
        })
      });

      const result = await response.json();

      alert(`🎵 Song beendet!\nRank: ${result.rank}\nAccuracy: ${result.accuracy.toFixed(1)}%`);

      this.loadProgress();

    } catch (error) {
      console.error('Fehler beim Song spielen:', error);
    }
  }

  async loadProgress() {
    try {
      const response = await fetch(`${this.apiBase}/progress`);
      const progress = await response.json();

      if (progress && typeof progress.level !== 'undefined') {
        document.getElementById('instrument-level').textContent = progress.level || 1;
        document.getElementById('instrument-xp').textContent = (progress.total_xp || 0).toFixed(0);
        document.getElementById('perfect-notes').textContent = progress.perfect_notes || 0;
      } else {
        // Fallback if backend offline
        document.getElementById('instrument-level').textContent = '1';
        document.getElementById('instrument-xp').textContent = '0';
        document.getElementById('perfect-notes').textContent = '0';
      }

    } catch (error) {
      console.error('Fehler beim Laden des Progress:', error);
      // Set defaults on error
      document.getElementById('instrument-level').textContent = '1';
      document.getElementById('instrument-xp').textContent = '0';
      document.getElementById('perfect-notes').textContent = '0';
    }
  }

  hide() {
    document.getElementById('instrument-ui-container').classList.add('hidden');
  }
}

// ============================================================================
// WORLD INFO UI (Weather, Time, etc.)
// ============================================================================

class WorldInfoUI {
  constructor() {
    this.apiBase = 'http://localhost:8000/api/world';
    this.createUI();
    this.startAutoUpdate();
  }

  createUI() {
    const container = document.createElement('div');
    container.id = 'world-info-hud';
    container.className = 'world-info-hud';
    container.innerHTML = `
      <div class="world-info-compact">
        <div class="time-display">
          <span class="time-icon">🕐</span>
          <span id="game-time">12:00</span>
          <span id="time-of-day" class="tod-badge">Noon</span>
        </div>
        <div class="weather-display">
          <span class="weather-icon" id="weather-icon">☀️</span>
          <span id="weather-type">Clear</span>
          <span id="temperature">20°C</span>
        </div>
      </div>
    `;
    document.body.appendChild(container);
  }

  async updateWorldInfo() {
    try {
      // Get time
      const timeResponse = await fetch(`${this.apiBase}/time`);
      const timeData = await timeResponse.json();

      document.getElementById('game-time').textContent = timeData.current_time.substring(0, 5);
      document.getElementById('time-of-day').textContent = timeData.time_of_day;

      // TODO: Get current biome from player position
      const biome = 'samtmoos_tiefwald';

      // Get weather
      const weatherResponse = await fetch(`${this.apiBase}/weather/${biome}`);
      const weatherData = await weatherResponse.json();

      document.getElementById('weather-type').textContent = weatherData.weather.type;
      document.getElementById('temperature').textContent = `${weatherData.weather.temperature}°C`;

      // Update weather icon
      const icon = this.getWeatherIcon(weatherData.weather.type);
      document.getElementById('weather-icon').textContent = icon;

    } catch (error) {
      console.error('Fehler beim World Info Update:', error);
    }
  }

  getWeatherIcon(weatherType) {
    const icons = {
      'clear': '☀️',
      'cloudy': '☁️',
      'rain': '🌧️',
      'heavy_rain': '⛈️',
      'snow': '❄️',
      'blizzard': '🌨️',
      'fog': '🌫️',
      'sandstorm': '🌪️',
      'thunderstorm': '⚡',
      'ash_rain': '🌋'
    };
    return icons[weatherType] || '☀️';
  }

  show() {
    const container = document.getElementById('world-info-container');
    if (container) {
      container.classList.remove('hidden');
      this.updateWorldInfo();
    }
  }

  hide() {
    const container = document.getElementById('world-info-container');
    if (container) {
      container.classList.add('hidden');
    }
  }

  startAutoUpdate() {
    // Update every 30 seconds
    setInterval(() => {
      this.updateWorldInfo();
    }, 30000);

    // Initial update
    this.updateWorldInfo();
  }
}

// ============================================================================
// AUTO-INITIALIZE ALL SYSTEMS
// ============================================================================

function initializeGameSystemsUI() {
  // Prevent double-initialization
  if (window.gameSystemsUIInitialized) {
    console.log('⚠️ Game Systems UI already initialized');
    return;
  }

  try {
    window.regionBossUI = new RegionBossUI();
    window.oregonEventsUI = new OregonEventsUI();
    window.magicSchoolsUI = new MagicSchoolsUI();
    window.instrumentUI = new InstrumentUI();
    window.worldInfoUI = new WorldInfoUI();

    window.gameSystemsUIInitialized = true;
    console.log('✅ All Game Systems UI initialized!');
  } catch (error) {
    console.error('❌ Error initializing Game Systems UI:', error);
  }
}

// Initialize on DOMContentLoaded
window.addEventListener('DOMContentLoaded', initializeGameSystemsUI);

// Also expose function for manual initialization if needed
window.initializeGameSystemsUI = initializeGameSystemsUI;
