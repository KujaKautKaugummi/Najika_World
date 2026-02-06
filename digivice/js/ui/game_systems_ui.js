/**
 * Game Systems UI - Najika World
 * ================================
 *
 * Zentrales Menü für alle Game-Systeme
 * Öffnet sich mit TAB-Taste
 *
 * Features:
 * - Tab-basierte Navigation
 * - Triple Triad Access
 * - Dice Monsters Access
 * - Housing Access
 * - Arena Access
 * - World Map Access
 *
 * Copyright: Najika World
 * Author: Claude Code (CLI)
 * Date: 2026-01-24
 */

class GameSystemsUI {
    constructor() {
        this.isOpen = false;
        this.activeTab = 'overview';
        this.init();
    }

    init() {
        this.createUI();
        this.attachEventListeners();
        console.log('✅ Game Systems UI geladen');
    }

    createUI() {
        const container = document.createElement('div');
        container.id = 'game-systems-container';
        container.className = 'game-systems-container hidden';
        container.innerHTML = `
            <div class="game-systems-panel">
                <div class="gs-header">
                    <h2>🎮 Game Systems</h2>
                    <button class="gs-close-btn" id="gs-close-btn">✖</button>
                </div>

                <div class="gs-tabs">
                    <button class="gs-tab active" data-tab="overview">📋 Übersicht</button>
                    <button class="gs-tab" data-tab="cards">🃏 Karten</button>
                    <button class="gs-tab" data-tab="arena">⚔️ Arena</button>
                    <button class="gs-tab" data-tab="housing">🏠 Housing</button>
                    <button class="gs-tab" data-tab="world">🗺️ Welt</button>
                </div>

                <div class="gs-content">
                    <!-- Overview Tab -->
                    <div id="gs-overview" class="gs-tab-content active">
                        <h3>Willkommen in Najika World!</h3>
                        <div class="gs-quick-actions">
                            <button class="gs-action-btn" onclick="GameSystemsUI.openTripleTriad()">
                                🃏 Triple Triad
                            </button>
                            <button class="gs-action-btn" onclick="GameSystemsUI.openDiceMonsters()">
                                🎲 Dice Monsters
                            </button>
                            <button class="gs-action-btn" onclick="GameSystemsUI.openArena()">
                                ⚔️ Nemesis Arena
                            </button>
                            <button class="gs-action-btn" onclick="GameSystemsUI.openHousing()">
                                🏠 Housing
                            </button>
                            <button class="gs-action-btn" onclick="GameSystemsUI.openDungeon()">
                                🗡️ Dungeon
                            </button>
                            <button class="gs-action-btn" onclick="GameSystemsUI.openSlimeArena()">
                                🟢 Slime Arena
                            </button>
                        </div>
                        <div class="gs-stats">
                            <h4>Dein Fortschritt</h4>
                            <div class="stat-row"><span>Triple Triad Siege:</span><span id="gs-tt-wins">0</span></div>
                            <div class="stat-row"><span>Arena Rang:</span><span id="gs-arena-rank">Neuling</span></div>
                            <div class="stat-row"><span>Dungeon Tiefe:</span><span id="gs-dungeon-depth">0</span></div>
                        </div>
                    </div>

                    <!-- Cards Tab -->
                    <div id="gs-cards" class="gs-tab-content">
                        <h3>🃏 Kartenspiele</h3>
                        <div class="gs-game-grid">
                            <div class="gs-game-card" onclick="GameSystemsUI.openTripleTriad()">
                                <div class="game-icon">🃏</div>
                                <div class="game-title">Triple Triad</div>
                                <div class="game-desc">FF8-Style Kartenspiel</div>
                            </div>
                            <div class="gs-game-card" onclick="GameSystemsUI.openDiceMonsters()">
                                <div class="game-icon">🎲</div>
                                <div class="game-title">Dice Monsters</div>
                                <div class="game-desc">Yu-Gi-Oh Würfelspiel</div>
                            </div>
                        </div>
                    </div>

                    <!-- Arena Tab -->
                    <div id="gs-arena" class="gs-tab-content">
                        <h3>⚔️ Kampfarena</h3>
                        <div class="gs-game-grid">
                            <div class="gs-game-card" onclick="GameSystemsUI.openArena()">
                                <div class="game-icon">🏛️</div>
                                <div class="game-title">Nemesis Arena</div>
                                <div class="game-desc">Shadow of Mordor System</div>
                            </div>
                            <div class="gs-game-card" onclick="GameSystemsUI.openSlimeArena()">
                                <div class="game-icon">🟢</div>
                                <div class="game-title">Slime Arena</div>
                                <div class="game-desc">Slime vs Slime Kämpfe</div>
                            </div>
                            <div class="gs-game-card" onclick="GameSystemsUI.openDungeon()">
                                <div class="game-icon">🗡️</div>
                                <div class="game-title">Dungeon</div>
                                <div class="game-desc">Prozedurales Dungeon</div>
                            </div>
                        </div>
                    </div>

                    <!-- Housing Tab -->
                    <div id="gs-housing" class="gs-tab-content">
                        <h3>🏠 Housing & Crafting</h3>
                        <div class="gs-game-grid">
                            <div class="gs-game-card" onclick="GameSystemsUI.openHousing()">
                                <div class="game-icon">🏠</div>
                                <div class="game-title">Schwarze Mühle</div>
                                <div class="game-desc">Dein Zuhause einrichten</div>
                            </div>
                            <div class="gs-game-card" onclick="GameSystemsUI.openGarden()">
                                <div class="game-icon">🌱</div>
                                <div class="game-title">Garten</div>
                                <div class="game-desc">Pflanzen anbauen</div>
                            </div>
                            <div class="gs-game-card" onclick="GameSystemsUI.openFishing()">
                                <div class="game-icon">🎣</div>
                                <div class="game-title">Angeln</div>
                                <div class="game-desc">Fische fangen</div>
                            </div>
                        </div>
                    </div>

                    <!-- World Tab -->
                    <div id="gs-world" class="gs-tab-content">
                        <h3>🗺️ Weltkarte</h3>
                        <div class="gs-world-info">
                            <p>Die Welt von Najika besteht aus 9 einzigartigen Regionen.</p>
                            <button class="gs-action-btn large" onclick="GameSystemsUI.openWorldMap()">
                                🗺️ Weltkarte öffnen
                            </button>
                        </div>
                        <div class="gs-regions-list" id="gs-regions-list">
                            <!-- Wird dynamisch geladen -->
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Styles
        const styles = document.createElement('style');
        styles.textContent = `
            .game-systems-container {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.8);
                z-index: 10000;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .game-systems-container.hidden {
                display: none;
            }
            .game-systems-panel {
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                border: 2px solid #667eea;
                border-radius: 15px;
                width: 90%;
                max-width: 800px;
                max-height: 80vh;
                overflow: hidden;
                box-shadow: 0 10px 40px rgba(102,126,234,0.3);
            }
            .gs-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 15px 20px;
                background: linear-gradient(90deg, #667eea, #764ba2);
            }
            .gs-header h2 {
                margin: 0;
                color: white;
            }
            .gs-close-btn {
                background: rgba(255,255,255,0.2);
                border: none;
                color: white;
                font-size: 20px;
                width: 35px;
                height: 35px;
                border-radius: 50%;
                cursor: pointer;
            }
            .gs-close-btn:hover {
                background: rgba(255,255,255,0.3);
            }
            .gs-tabs {
                display: flex;
                background: rgba(0,0,0,0.3);
                padding: 10px;
                gap: 5px;
                flex-wrap: wrap;
            }
            .gs-tab {
                flex: 1;
                min-width: 80px;
                padding: 10px 15px;
                background: rgba(255,255,255,0.1);
                border: none;
                color: #aaa;
                border-radius: 8px;
                cursor: pointer;
                transition: all 0.2s;
            }
            .gs-tab:hover {
                background: rgba(255,255,255,0.2);
                color: white;
            }
            .gs-tab.active {
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
            }
            .gs-content {
                padding: 20px;
                max-height: 50vh;
                overflow-y: auto;
            }
            .gs-tab-content {
                display: none;
            }
            .gs-tab-content.active {
                display: block;
            }
            .gs-quick-actions {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
                gap: 10px;
                margin: 15px 0;
            }
            .gs-action-btn {
                padding: 15px;
                background: linear-gradient(135deg, #667eea, #764ba2);
                border: none;
                color: white;
                border-radius: 10px;
                cursor: pointer;
                font-size: 14px;
                transition: transform 0.2s;
            }
            .gs-action-btn:hover {
                transform: scale(1.05);
            }
            .gs-action-btn.large {
                padding: 20px 40px;
                font-size: 16px;
            }
            .gs-stats {
                background: rgba(0,0,0,0.3);
                padding: 15px;
                border-radius: 10px;
                margin-top: 15px;
            }
            .gs-stats h4 {
                margin: 0 0 10px 0;
                color: #667eea;
            }
            .stat-row {
                display: flex;
                justify-content: space-between;
                padding: 5px 0;
                border-bottom: 1px solid rgba(255,255,255,0.1);
            }
            .gs-game-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
                gap: 15px;
            }
            .gs-game-card {
                background: rgba(255,255,255,0.1);
                padding: 20px;
                border-radius: 12px;
                text-align: center;
                cursor: pointer;
                transition: all 0.3s;
            }
            .gs-game-card:hover {
                background: rgba(102,126,234,0.3);
                transform: translateY(-5px);
            }
            .game-icon {
                font-size: 40px;
                margin-bottom: 10px;
            }
            .game-title {
                font-weight: bold;
                color: white;
                margin-bottom: 5px;
            }
            .game-desc {
                font-size: 12px;
                color: #aaa;
            }
            .gs-world-info {
                text-align: center;
                margin-bottom: 20px;
            }
            .gs-regions-list {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 10px;
            }
        `;

        document.head.appendChild(styles);
        document.body.appendChild(container);
    }

    attachEventListeners() {
        // TAB-Taste zum Öffnen/Schließen
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Tab' && !e.target.matches('input, textarea')) {
                e.preventDefault();
                this.toggle();
            }
            if (e.key === 'Escape' && this.isOpen) {
                this.close();
            }
        });

        // Close Button
        document.getElementById('gs-close-btn')?.addEventListener('click', () => this.close());

        // Tab Navigation
        document.querySelectorAll('.gs-tab').forEach(tab => {
            tab.addEventListener('click', (e) => {
                const tabName = e.target.dataset.tab;
                this.switchTab(tabName);
            });
        });
    }

    switchTab(tabName) {
        // Deaktiviere alle Tabs
        document.querySelectorAll('.gs-tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.gs-tab-content').forEach(c => c.classList.remove('active'));

        // Aktiviere gewählten Tab
        document.querySelector(`.gs-tab[data-tab="${tabName}"]`)?.classList.add('active');
        document.getElementById(`gs-${tabName}`)?.classList.add('active');

        this.activeTab = tabName;

        // Lade Tab-spezifische Daten
        if (tabName === 'world') {
            this.loadRegions();
        }
    }

    async loadRegions() {
        try {
            const response = await fetch('/api/world/regions');
            const data = await response.json();
            const list = document.getElementById('gs-regions-list');
            if (list && data.regions) {
                list.innerHTML = data.regions.map(r => `
                    <div class="region-item">${r.name}</div>
                `).join('');
            }
        } catch (e) {
            console.log('Regionen konnten nicht geladen werden');
        }
    }

    toggle() {
        if (this.isOpen) {
            this.close();
        } else {
            this.open();
        }
    }

    open() {
        const container = document.getElementById('game-systems-container');
        if (container) {
            container.classList.remove('hidden');
            this.isOpen = true;
        }
    }

    close() {
        const container = document.getElementById('game-systems-container');
        if (container) {
            container.classList.add('hidden');
            this.isOpen = false;
        }
    }

    // Static Methods für Quick Actions
    static openTripleTriad() {
        window.gameSystemsUI?.close();
        // TripleTriadUI ist das UI-System, TripleTriad ist das Backend
        if (typeof TripleTriadUI !== 'undefined' && TripleTriadUI.open) {
            // Öffne mit Najika als Default-NPC
            TripleTriadUI.open('najika');
        } else if (typeof TripleTriad !== 'undefined') {
            // Fallback: Zeige Sammlung
            const collection = TripleTriad.getCollection();
            alert(`🃏 Triple Triad\n\nDeine Karten: ${collection.cards.length}\nSiege: ${collection.wins}\nNiederlagen: ${collection.losses}\n\nSprich mit einem NPC um zu spielen!`);
        } else {
            alert('Triple Triad wird geladen...');
        }
    }

    static openDiceMonsters() {
        window.gameSystemsUI?.close();
        if (typeof DiceMonstersUI !== 'undefined') {
            DiceMonstersUI.open();
        } else {
            alert('🎲 Dice Monsters\n\nKommt bald!');
        }
    }

    static openArena() {
        window.gameSystemsUI?.close();
        if (window.NemesisArena) {
            window.NemesisArena.showArenaPanel();
        } else {
            alert('⚔️ Arena wird geladen...');
        }
    }

    static openSlimeArena() {
        window.gameSystemsUI?.close();
        // SlimeArenaUI ist als window.slimeArenaUI instanziiert
        if (window.slimeArenaUI && typeof window.slimeArenaUI.open === 'function') {
            window.slimeArenaUI.open();
        } else if (typeof SlimeArenaUI !== 'undefined') {
            // Fallback: Erstelle neue Instanz
            window.slimeArenaUI = new SlimeArenaUI();
            window.slimeArenaUI.open();
        } else {
            alert('🟢 Slime Arena\n\nGehe zur "Schlammigen Münze" in den Heißen Dünen!');
        }
    }

    static openHousing() {
        window.gameSystemsUI?.close();
        if (typeof HousingSystem !== 'undefined' && HousingSystem.open) {
            HousingSystem.open();
        } else {
            alert('🏠 Housing System\n\nGehe zur Schwarzen Mühle!');
        }
    }

    static openDungeon() {
        window.gameSystemsUI?.close();
        if (typeof enterDungeon === 'function') {
            enterDungeon();
        } else {
            alert('🗡️ Dungeon\n\nDrücke den Dungeon-Button!');
        }
    }

    static openGarden() {
        window.gameSystemsUI?.close();
        if (typeof GardenSystem !== 'undefined') {
            GardenSystem.open();
        } else {
            alert('🌱 Garten ist im Außenbereich der Mühle!');
        }
    }

    static openFishing() {
        window.gameSystemsUI?.close();
        if (typeof FishingSystem !== 'undefined') {
            FishingSystem.open();
        } else {
            alert('🎣 Gehe zu einem Gewässer zum Angeln!');
        }
    }

    static openWorldMap() {
        window.gameSystemsUI?.close();
        if (typeof WorldMapUI !== 'undefined') {
            WorldMapUI.open();
        } else {
            alert('🗺️ Weltkarte\n\nDrücke M für die Karte!');
        }
    }
}

// Initialize
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.gameSystemsUI = new GameSystemsUI();
    });
} else {
    window.gameSystemsUI = new GameSystemsUI();
}

// Global Access
window.GameSystemsUI = GameSystemsUI;

console.log('✅ Game Systems UI geladen - Drücke TAB zum Öffnen');
