/**
 * Finisher Category Selector UI
 * Player chooses brutality category before creating finisher
 */

export class FinisherCategorySelector {
    constructor(apiClient) {
        this.apiClient = apiClient;
        this.categories = [];
        this.selectedCategory = null;
        this.onCategorySelected = null; // Callback
    }

    /**
     * Load available categories from API
     */
    async loadCategories() {
        try {
            const response = await this.apiClient.get('http://localhost:8000/api/game/arena/finisher/categories');
            this.categories = response.data.categories;
            return this.categories;
        } catch (error) {
            console.error('Failed to load finisher categories:', error);
            return [];
        }
    }

    /**
     * Show category selection dialog
     */
    async show(defeatedMonsterId) {
        // Load categories if not loaded
        if (this.categories.length === 0) {
            await this.loadCategories();
        }

        // Create overlay
        const overlay = document.createElement('div');
        overlay.className = 'finisher-category-overlay';
        overlay.innerHTML = `
            <div class="finisher-category-dialog">
                <div class="category-header">
                    <h2>💀 FINISH HIM! 💀</h2>
                    <p>Wähle die Art des Todes:</p>
                </div>

                <div class="category-grid">
                    ${this.categories.map(cat => this.renderCategoryCard(cat)).join('')}
                </div>

                <div class="category-footer">
                    <button class="btn-cancel" onclick="this.closest('.finisher-category-overlay').remove()">
                        Abbrechen
                    </button>
                </div>
            </div>
        `;

        document.body.appendChild(overlay);

        // Add styles if not already added
        this.addStyles();

        // Store monster ID for later
        this.defeatedMonsterId = defeatedMonsterId;

        return new Promise((resolve) => {
            this.onCategorySelected = resolve;
        });
    }

    /**
     * Render a category card
     */
    renderCategoryCard(category) {
        return `
            <div class="category-card" data-category="${category.name}" onclick="window.finisherSelector.selectCategory('${category.name}')">
                <div class="category-icon">${category.icon}</div>
                <div class="category-name">${category.name}</div>
                <div class="category-description">${category.description}</div>

                <div class="category-stats">
                    <div class="stat">
                        <span class="stat-label">Brutalität</span>
                        <div class="stat-bar">
                            <div class="stat-fill brutality" style="width: ${category.brutality * 10}%"></div>
                        </div>
                        <span class="stat-value">${category.brutality}/10</span>
                    </div>

                    <div class="stat">
                        <span class="stat-label">Humor</span>
                        <div class="stat-bar">
                            <div class="stat-fill humor" style="width: ${category.humor * 10}%"></div>
                        </div>
                        <span class="stat-value">${category.humor}/10</span>
                    </div>
                </div>

                <button class="btn-select">WÄHLEN</button>
            </div>
        `;
    }

    /**
     * Select a category and show ingredient input
     */
    async selectCategory(categoryName) {
        this.selectedCategory = categoryName;

        // Remove category dialog
        const overlay = document.querySelector('.finisher-category-overlay');
        if (overlay) {
            overlay.remove();
        }

        // Show ingredient input dialog
        this.showIngredientDialog();
    }

    /**
     * Show ingredient input dialog
     */
    async showIngredientDialog() {
        // Get random ingredient suggestions
        const response = await this.apiClient.get('http://localhost:8000/api/game/arena/finisher/random-ingredients');
        const suggestions = response.data.ingredients;

        const overlay = document.createElement('div');
        overlay.className = 'finisher-ingredient-overlay';
        overlay.innerHTML = `
            <div class="finisher-ingredient-dialog">
                <div class="ingredient-header">
                    <h2>🎯 ${this.selectedCategory}</h2>
                    <p>Gib 1-5 Stichwörter ein:</p>
                </div>

                <div class="ingredient-input-section">
                    <input type="text" id="ingredient-input" class="ingredient-input"
                           placeholder="z.B. Dynamit, Feuer, Chaos..." maxlength="100">

                    <div class="ingredient-suggestions">
                        <p>💡 Vorschläge:</p>
                        ${suggestions.map(s => `
                            <button class="suggestion-btn" onclick="document.getElementById('ingredient-input').value += '${s}, '">
                                ${s}
                            </button>
                        `).join('')}
                    </div>

                    <div class="ingredient-list" id="ingredient-list">
                        <!-- Added ingredients will appear here -->
                    </div>
                </div>

                <div class="ingredient-footer">
                    <button class="btn-cancel" onclick="this.closest('.finisher-ingredient-overlay').remove()">
                        Abbrechen
                    </button>
                    <button class="btn-create" id="create-finisher-btn">
                        🔥 FINISHER ERSTELLEN!
                    </button>
                </div>
            </div>
        `;

        document.body.appendChild(overlay);

        // Add event listener for create button
        const createBtn = document.getElementById('create-finisher-btn');
        createBtn.addEventListener('click', () => {
            this.createFinisher();
        });

        // Focus input
        document.getElementById('ingredient-input').focus();
    }

    /**
     * Create finisher with selected category and ingredients
     */
    async createFinisher() {
        const input = document.getElementById('ingredient-input');
        const ingredientsText = input.value.trim();

        if (!ingredientsText) {
            alert('⚠️ Bitte gib mindestens ein Stichwort ein!');
            return;
        }

        // Split ingredients by comma
        const ingredients = ingredientsText
            .split(',')
            .map(i => i.trim())
            .filter(i => i.length > 0);

        if (ingredients.length === 0) {
            alert('⚠️ Bitte gib mindestens ein Stichwort ein!');
            return;
        }

        // Show loading
        const createBtn = document.getElementById('create-finisher-btn');
        createBtn.disabled = true;
        createBtn.textContent = '⏳ Erstelle Finisher...';

        try {
            // Create finisher via API
            const response = await this.apiClient.post('http://localhost:8000/api/game/arena/finisher/create', {
                category: this.selectedCategory,
                ingredients: ingredients,
                defeated_monster_id: this.defeatedMonsterId
            });

            const finisher = response.data.finisher;

            // Remove dialog
            const overlay = document.querySelector('.finisher-ingredient-overlay');
            if (overlay) {
                overlay.remove();
            }

            // Show finisher animation
            this.playFinisherAnimation(finisher);

            // Trigger callback if set
            if (this.onCategorySelected) {
                this.onCategorySelected({
                    category: this.selectedCategory,
                    ingredients: ingredients,
                    finisher: finisher
                });
            }

        } catch (error) {
            console.error('Failed to create finisher:', error);
            alert('❌ Fehler beim Erstellen des Finishers!');
            createBtn.disabled = false;
            createBtn.textContent = '🔥 FINISHER ERSTELLEN!';
        }
    }

    /**
     * Play finisher animation
     */
    playFinisherAnimation(finisher) {
        const overlay = document.createElement('div');
        overlay.className = 'finisher-animation-overlay';
        overlay.innerHTML = `
            <div class="finisher-animation">
                <h1 class="finisher-name">${finisher.name}</h1>
                <div class="finisher-category">${finisher.category}</div>

                <div class="animation-sequence" id="animation-sequence">
                    <!-- Animation steps will be added here -->
                </div>

                <div class="finisher-stats">
                    <div class="stat">Brutalität: ${finisher.brutality_level}/10</div>
                    <div class="stat">Humor: ${finisher.humor_level}/10</div>
                    <div class="stat">Schaden: ${(finisher.damage_multiplier * 100).toFixed(0)}%</div>
                </div>
            </div>
        `;

        document.body.appendChild(overlay);

        // Animate each phase
        const sequence = document.getElementById('animation-sequence');
        let delay = 0;

        finisher.animation_steps.forEach((step, index) => {
            setTimeout(() => {
                const stepDiv = document.createElement('div');
                stepDiv.className = 'animation-step';
                stepDiv.innerHTML = `
                    <div class="step-phase">${step.phase}</div>
                    <div class="step-description">${step.description}</div>
                    <div class="step-visual">${step.visual}</div>
                `;
                sequence.appendChild(stepDiv);

                // Add animation effect
                stepDiv.style.animation = 'fadeInUp 0.5s ease-out';
            }, delay * 1000);

            delay += step.duration;
        });

        // Remove overlay after animation completes
        setTimeout(() => {
            overlay.style.animation = 'fadeOut 1s ease-out';
            setTimeout(() => {
                overlay.remove();
            }, 1000);
        }, (delay + 2) * 1000);
    }

    /**
     * Add CSS styles
     */
    addStyles() {
        if (document.getElementById('finisher-category-styles')) {
            return;
        }

        const style = document.createElement('style');
        style.id = 'finisher-category-styles';
        style.textContent = `
            /* Category Selector Overlay */
            .finisher-category-overlay, .finisher-ingredient-overlay, .finisher-animation-overlay {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.95);
                z-index: 3000;
                display: flex;
                align-items: center;
                justify-content: center;
                animation: fadeIn 0.3s ease-out;
            }

            .finisher-category-dialog, .finisher-ingredient-dialog {
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                border: 5px solid #e94560;
                border-radius: 20px;
                padding: 40px;
                max-width: 1000px;
                max-height: 90vh;
                overflow-y: auto;
                box-shadow: 0 0 50px rgba(233, 69, 96, 0.8);
            }

            .category-header, .ingredient-header {
                text-align: center;
                margin-bottom: 30px;
            }

            .category-header h2, .ingredient-header h2 {
                font-size: 48px;
                margin: 0;
                color: #e94560;
                text-shadow: 0 0 20px rgba(233, 69, 96, 0.8);
            }

            .category-header p, .ingredient-header p {
                font-size: 20px;
                color: #ccc;
                margin: 10px 0 0 0;
            }

            .category-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }

            .category-card {
                background: linear-gradient(135deg, #0f3460 0%, #1a1a2e 100%);
                border: 3px solid #e94560;
                border-radius: 15px;
                padding: 20px;
                text-align: center;
                cursor: pointer;
                transition: all 0.3s;
            }

            .category-card:hover {
                transform: translateY(-10px) scale(1.05);
                border-color: #ff6b9d;
                box-shadow: 0 10px 40px rgba(233, 69, 96, 0.6);
            }

            .category-icon {
                font-size: 60px;
                margin-bottom: 15px;
            }

            .category-name {
                font-size: 20px;
                font-weight: bold;
                color: white;
                margin-bottom: 10px;
            }

            .category-description {
                font-size: 14px;
                color: #aaa;
                margin-bottom: 15px;
                min-height: 40px;
            }

            .category-stats {
                margin: 15px 0;
            }

            .stat {
                margin: 10px 0;
            }

            .stat-label {
                font-size: 12px;
                color: #ccc;
                display: block;
                margin-bottom: 5px;
            }

            .stat-bar {
                height: 8px;
                background: #333;
                border-radius: 4px;
                overflow: hidden;
                margin-bottom: 5px;
            }

            .stat-fill {
                height: 100%;
                transition: width 0.5s ease-out;
            }

            .stat-fill.brutality {
                background: linear-gradient(90deg, #e94560 0%, #ff0000 100%);
            }

            .stat-fill.humor {
                background: linear-gradient(90deg, #4ecdc4 0%, #ffeb3b 100%);
            }

            .stat-value {
                font-size: 12px;
                color: white;
            }

            .btn-select {
                width: 100%;
                padding: 12px;
                background: #e94560;
                border: none;
                border-radius: 8px;
                color: white;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.3s;
            }

            .btn-select:hover {
                background: #ff6b9d;
                transform: scale(1.05);
            }

            /* Ingredient Input */
            .ingredient-input-section {
                margin: 30px 0;
            }

            .ingredient-input {
                width: 100%;
                padding: 15px;
                font-size: 18px;
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid #e94560;
                border-radius: 10px;
                color: white;
                margin-bottom: 20px;
            }

            .ingredient-suggestions {
                margin: 20px 0;
            }

            .ingredient-suggestions p {
                color: #ccc;
                margin-bottom: 10px;
            }

            .suggestion-btn {
                background: rgba(233, 69, 96, 0.2);
                border: 1px solid #e94560;
                border-radius: 20px;
                padding: 8px 15px;
                color: white;
                margin: 5px;
                cursor: pointer;
                transition: all 0.3s;
            }

            .suggestion-btn:hover {
                background: #e94560;
                transform: scale(1.05);
            }

            /* Footer */
            .category-footer, .ingredient-footer {
                display: flex;
                gap: 15px;
                justify-content: center;
                margin-top: 30px;
            }

            .btn-cancel, .btn-create {
                padding: 15px 40px;
                border: none;
                border-radius: 10px;
                font-size: 18px;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.3s;
            }

            .btn-cancel {
                background: #555;
                color: white;
            }

            .btn-cancel:hover {
                background: #777;
            }

            .btn-create {
                background: linear-gradient(135deg, #e94560 0%, #ff0000 100%);
                color: white;
                box-shadow: 0 0 20px rgba(233, 69, 96, 0.5);
            }

            .btn-create:hover {
                transform: scale(1.05);
                box-shadow: 0 0 30px rgba(233, 69, 96, 0.8);
            }

            .btn-create:disabled {
                opacity: 0.5;
                cursor: not-allowed;
            }

            /* Finisher Animation */
            .finisher-animation {
                text-align: center;
                color: white;
            }

            .finisher-name {
                font-size: 64px;
                margin-bottom: 20px;
                color: #e94560;
                text-shadow: 0 0 30px rgba(233, 69, 96, 1);
                animation: pulse 1s infinite;
            }

            .finisher-category {
                font-size: 32px;
                margin-bottom: 40px;
                color: #ff6b9d;
            }

            .animation-step {
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid #e94560;
                border-radius: 15px;
                padding: 30px;
                margin: 20px 0;
            }

            .step-phase {
                font-size: 24px;
                font-weight: bold;
                color: #4ecdc4;
                margin-bottom: 10px;
            }

            .step-description {
                font-size: 20px;
                margin: 10px 0;
            }

            .step-visual {
                font-size: 16px;
                color: #aaa;
                font-style: italic;
            }

            .finisher-stats {
                display: flex;
                gap: 30px;
                justify-content: center;
                margin-top: 40px;
                font-size: 20px;
            }

            /* Animations */
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }

            @keyframes fadeOut {
                from { opacity: 1; }
                to { opacity: 0; }
            }

            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            @keyframes pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.05); }
            }
        `;

        document.head.appendChild(style);
    }
}

// Make globally available
window.FinisherCategorySelector = FinisherCategorySelector;
