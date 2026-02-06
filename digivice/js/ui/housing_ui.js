/**
 * Housing UI - Najika World
 * ==========================
 *
 * UI für das Housing System in der Schwarzen Mühle
 * Möbel platzieren, Räume einrichten, Dekorieren
 *
 * Copyright: Najika World
 * Author: Claude Code (CLI)
 * Date: 2026-01-24
 */

class HousingUI {
    constructor() {
        this.apiBase = '/api/housing';
        this.isOpen = false;
        this.selectedCategory = 'all';
        this.selectedFurniture = null;
        this.playerGold = 1000;
        this.placedFurniture = [];

        this.init();
    }

    init() {
        this.createUI();
        this.attachEventListeners();
        console.log('✅ Housing UI geladen');
    }

    createUI() {
        const container = document.createElement('div');
        container.id = 'housing-ui-container';
        container.className = 'housing-ui-container hidden';
        container.innerHTML = `
            <div class="housing-panel">
                <div class="housing-header">
                    <h2>🏠 Schwarze Mühle - Einrichtung</h2>
                    <div class="housing-gold">
                        <span>💰</span>
                        <span id="housing-gold-amount">${this.playerGold}</span>
                    </div>
                    <button class="housing-close-btn" id="housing-close-btn">✖</button>
                </div>

                <div class="housing-content">
                    <!-- Kategorien -->
                    <div class="housing-categories">
                        <button class="cat-btn active" data-cat="all">Alle</button>
                        <button class="cat-btn" data-cat="bedroom">🛏️ Schlafzimmer</button>
                        <button class="cat-btn" data-cat="living">🛋️ Wohnzimmer</button>
                        <button class="cat-btn" data-cat="kitchen">🍳 Küche</button>
                        <button class="cat-btn" data-cat="bathroom">🚿 Bad</button>
                        <button class="cat-btn" data-cat="decor">🎨 Deko</button>
                        <button class="cat-btn" data-cat="special">⭐ Spezial</button>
                    </div>

                    <!-- Möbel-Katalog -->
                    <div class="housing-catalog" id="housing-catalog">
                        <!-- Wird dynamisch geladen -->
                    </div>

                    <!-- Aktuelle Auswahl -->
                    <div class="housing-selection" id="housing-selection">
                        <p>Wähle ein Möbelstück aus dem Katalog</p>
                    </div>

                    <!-- Aktionen -->
                    <div class="housing-actions">
                        <button class="housing-btn" onclick="HousingUI.placeSelected()">
                            📦 Platzieren
                        </button>
                        <button class="housing-btn secondary" onclick="HousingUI.rotateSelected()">
                            🔄 Drehen
                        </button>
                        <button class="housing-btn danger" onclick="HousingUI.removeSelected()">
                            🗑️ Entfernen
                        </button>
                    </div>
                </div>

                <!-- Räume Tabs -->
                <div class="housing-rooms">
                    <button class="room-btn active" data-room="wohnzimmer">Wohnzimmer</button>
                    <button class="room-btn" data-room="schlafzimmer">Schlafzimmer</button>
                    <button class="room-btn" data-room="kueche">Küche</button>
                    <button class="room-btn" data-room="badezimmer">Bad</button>
                    <button class="room-btn" data-room="keller">Keller</button>
                </div>
            </div>
        `;

        // Styles
        const styles = document.createElement('style');
        styles.textContent = `
            .housing-ui-container {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.85);
                z-index: 10000;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .housing-ui-container.hidden {
                display: none;
            }
            .housing-panel {
                background: linear-gradient(135deg, #2d1f1f 0%, #1a1a1a 100%);
                border: 2px solid #8B4513;
                border-radius: 15px;
                width: 95%;
                max-width: 900px;
                max-height: 85vh;
                overflow: hidden;
                box-shadow: 0 10px 40px rgba(139,69,19,0.4);
            }
            .housing-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 15px 20px;
                background: linear-gradient(90deg, #8B4513, #654321);
            }
            .housing-header h2 {
                margin: 0;
                color: #FFD700;
            }
            .housing-gold {
                display: flex;
                align-items: center;
                gap: 5px;
                background: rgba(0,0,0,0.3);
                padding: 8px 15px;
                border-radius: 20px;
                color: #FFD700;
                font-weight: bold;
            }
            .housing-close-btn {
                background: rgba(255,255,255,0.2);
                border: none;
                color: white;
                font-size: 20px;
                width: 35px;
                height: 35px;
                border-radius: 50%;
                cursor: pointer;
            }
            .housing-content {
                padding: 15px;
                max-height: 55vh;
                overflow-y: auto;
            }
            .housing-categories {
                display: flex;
                gap: 5px;
                flex-wrap: wrap;
                margin-bottom: 15px;
            }
            .cat-btn {
                padding: 8px 12px;
                background: rgba(139,69,19,0.3);
                border: 1px solid #8B4513;
                color: #DEB887;
                border-radius: 8px;
                cursor: pointer;
                font-size: 12px;
            }
            .cat-btn:hover, .cat-btn.active {
                background: #8B4513;
                color: white;
            }
            .housing-catalog {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
                gap: 10px;
                margin-bottom: 15px;
                max-height: 200px;
                overflow-y: auto;
                padding: 10px;
                background: rgba(0,0,0,0.3);
                border-radius: 10px;
            }
            .furniture-item {
                background: rgba(139,69,19,0.2);
                border: 1px solid rgba(139,69,19,0.5);
                border-radius: 8px;
                padding: 10px;
                text-align: center;
                cursor: pointer;
                transition: all 0.2s;
            }
            .furniture-item:hover {
                background: rgba(139,69,19,0.4);
                transform: scale(1.05);
            }
            .furniture-item.selected {
                border-color: #FFD700;
                box-shadow: 0 0 10px rgba(255,215,0,0.5);
            }
            .furniture-icon {
                font-size: 30px;
                margin-bottom: 5px;
            }
            .furniture-name {
                font-size: 11px;
                color: #DEB887;
            }
            .furniture-price {
                font-size: 10px;
                color: #FFD700;
            }
            .housing-selection {
                background: rgba(0,0,0,0.3);
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 15px;
                text-align: center;
                color: #DEB887;
            }
            .housing-actions {
                display: flex;
                gap: 10px;
                justify-content: center;
            }
            .housing-btn {
                padding: 12px 25px;
                background: linear-gradient(135deg, #8B4513, #654321);
                border: none;
                color: white;
                border-radius: 8px;
                cursor: pointer;
                font-size: 14px;
            }
            .housing-btn:hover {
                filter: brightness(1.2);
            }
            .housing-btn.secondary {
                background: linear-gradient(135deg, #555, #333);
            }
            .housing-btn.danger {
                background: linear-gradient(135deg, #8B0000, #550000);
            }
            .housing-rooms {
                display: flex;
                background: rgba(0,0,0,0.5);
                padding: 10px;
                gap: 5px;
                justify-content: center;
            }
            .room-btn {
                padding: 8px 15px;
                background: rgba(139,69,19,0.3);
                border: 1px solid #8B4513;
                color: #DEB887;
                border-radius: 5px;
                cursor: pointer;
            }
            .room-btn:hover, .room-btn.active {
                background: #8B4513;
                color: white;
            }
        `;

        document.head.appendChild(styles);
        document.body.appendChild(container);

        this.loadCatalog();
    }

    attachEventListeners() {
        // Close Button
        document.getElementById('housing-close-btn')?.addEventListener('click', () => this.close());

        // Escape zum Schließen
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isOpen) {
                this.close();
            }
        });

        // Kategorie-Buttons
        document.querySelectorAll('.cat-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                document.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
                this.selectedCategory = e.target.dataset.cat;
                this.loadCatalog();
            });
        });

        // Raum-Buttons
        document.querySelectorAll('.room-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                document.querySelectorAll('.room-btn').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
                // Raum wechseln
            });
        });
    }

    async loadCatalog() {
        const catalog = document.getElementById('housing-catalog');
        if (!catalog) return;

        try {
            const response = await fetch(`${this.apiBase}/furniture/catalog`);
            const data = await response.json();

            const items = data.catalog || [];
            const filtered = this.selectedCategory === 'all'
                ? items
                : items.filter(i => i.category === this.selectedCategory);

            catalog.innerHTML = filtered.map(item => `
                <div class="furniture-item" data-type="${item.type}" onclick="window.housingUI.selectFurniture('${item.type}', '${item.name}', ${item.cost})">
                    <div class="furniture-icon">${this.getIcon(item.type)}</div>
                    <div class="furniture-name">${item.name}</div>
                    <div class="furniture-price">💰 ${item.cost}</div>
                </div>
            `).join('');
        } catch (e) {
            catalog.innerHTML = '<p style="color:#888;">Katalog konnte nicht geladen werden</p>';
        }
    }

    getIcon(type) {
        const icons = {
            'bed': '🛏️', 'table': '🪑', 'chair': '🪑', 'sofa': '🛋️',
            'bookshelf': '📚', 'desk': '🖥️', 'wardrobe': '🚪', 'lamp': '💡',
            'rug': '🟫', 'plant': '🌿', 'painting': '🖼️', 'tv': '📺',
            'fireplace': '🔥', 'kitchen_counter': '🍳', 'refrigerator': '🧊'
        };
        return icons[type] || '📦';
    }

    selectFurniture(type, name, cost) {
        this.selectedFurniture = { type, name, cost };

        document.querySelectorAll('.furniture-item').forEach(item => {
            item.classList.remove('selected');
            if (item.dataset.type === type) {
                item.classList.add('selected');
            }
        });

        const selection = document.getElementById('housing-selection');
        if (selection) {
            selection.innerHTML = `
                <strong>${name}</strong><br>
                <span style="color:#FFD700;">💰 ${cost} Gold</span><br>
                <small>Klicke auf "Platzieren" um das Möbelstück zu setzen</small>
            `;
        }
    }

    open() {
        const container = document.getElementById('housing-ui-container');
        if (container) {
            container.classList.remove('hidden');
            this.isOpen = true;
            this.loadCatalog();
        }
    }

    close() {
        const container = document.getElementById('housing-ui-container');
        if (container) {
            container.classList.add('hidden');
            this.isOpen = false;
        }
    }

    static placeSelected() {
        const ui = window.housingUI;
        if (!ui?.selectedFurniture) {
            alert('Wähle zuerst ein Möbelstück aus!');
            return;
        }

        if (ui.playerGold < ui.selectedFurniture.cost) {
            alert('Nicht genug Gold!');
            return;
        }

        ui.playerGold -= ui.selectedFurniture.cost;
        document.getElementById('housing-gold-amount').textContent = ui.playerGold;

        ui.placedFurniture.push(ui.selectedFurniture);
        alert(`${ui.selectedFurniture.name} wurde platziert!`);

        // Hier würde die 3D-Platzierung erfolgen
        if (typeof HousingSystem !== 'undefined' && HousingSystem.placeFurniture) {
            HousingSystem.placeFurniture(ui.selectedFurniture.type);
        }
    }

    static rotateSelected() {
        alert('🔄 Rotation: Nutze Q/E im 3D-Modus');
    }

    static removeSelected() {
        alert('🗑️ Entfernen: Klicke auf ein platziertes Möbelstück');
    }
}

// Initialize
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.housingUI = new HousingUI();
    });
} else {
    window.housingUI = new HousingUI();
}

window.HousingUI = HousingUI;

console.log('✅ Housing UI System geladen');
