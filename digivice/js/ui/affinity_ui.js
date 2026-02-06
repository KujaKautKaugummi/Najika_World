/**
 * NAJIKA WORLD - AFFINITY/BOND SYSTEM UI
 * =======================================
 * Beziehungssystem zwischen Kuja und Najika
 *
 * Bond-Strength beeinflusst:
 * - Najika's Reaktionen
 * - Combat-Boni (Anfeuern)
 * - Dialog-Optionen
 * - Spezielle Events
 */

class AffinityUI {
    constructor() {
        this.isOpen = false;
        this.overlay = null;

        // Bond Stats
        this.bondStrength = 0; // 0-100
        this.totalInteractions = 0;

        // Relationship Level Names
        this.levels = [
            { min: 0, max: 24, name: 'Bekannte', icon: '🌱', color: '#888888' },
            { min: 25, max: 49, name: 'Freunde', icon: '🌸', color: '#ff69b4' },
            { min: 50, max: 74, name: 'Enge Freunde', icon: '💜', color: '#9b59b6' },
            { min: 75, max: 89, name: 'Seelenverwandte', icon: '💖', color: '#e74c3c' },
            { min: 90, max: 100, name: 'UNTRENNBAR', icon: '✨💕✨', color: '#FFD700' }
        ];

        // Mood States
        this.moodStates = {
            happy: { icon: '😊', name: 'Glücklich', color: '#4CAF50' },
            excited: { icon: '🤩', name: 'Aufgeregt', color: '#FFD700' },
            loving: { icon: '😍', name: 'Verliebt', color: '#ff69b4' },
            playful: { icon: '😜', name: 'Verspielt', color: '#9b59b6' },
            tired: { icon: '😴', name: 'Müde', color: '#666666' },
            hungry: { icon: '😋', name: 'Hungrig', color: '#e67e22' },
            angry: { icon: '😤', name: 'Wütend', color: '#e74c3c' },
            sad: { icon: '😢', name: 'Traurig', color: '#3498db' },
            jealous: { icon: '😒', name: 'Eifersüchtig', color: '#8e44ad' },
            explosion: { icon: '💥', name: 'EXPLOSION!', color: '#ff0066' }
        };

        this.currentMood = 'happy';

        // Activity History
        this.recentActivities = [];
        this.maxActivities = 10;

        // Personality Dominance (changes based on interactions)
        this.personalityWeights = {
            megumin: 35,
            harley: 25,
            shiro: 20,
            melissa: 20
        };

        console.log('💕 Affinity System UI initialisiert');
    }

    getCurrentLevel() {
        return this.levels.find(l => this.bondStrength >= l.min && this.bondStrength <= l.max) || this.levels[0];
    }

    addBondXP(amount, reason = 'Interaktion') {
        const oldLevel = this.getCurrentLevel();
        this.bondStrength = Math.min(100, Math.max(0, this.bondStrength + amount));
        const newLevel = this.getCurrentLevel();

        // Track activity
        this.addActivity(reason, amount);

        // Level up notification
        if (newLevel.min > oldLevel.min) {
            console.log(`💕 Beziehung verbessert: ${newLevel.name}!`);
            if (window.showNotification) {
                window.showNotification(`💕 Beziehung: ${newLevel.icon} ${newLevel.name}!`, 4000);
            }
        }

        this.totalInteractions++;
    }

    addActivity(reason, bondChange) {
        this.recentActivities.unshift({
            reason,
            bondChange,
            timestamp: Date.now()
        });

        if (this.recentActivities.length > this.maxActivities) {
            this.recentActivities.pop();
        }
    }

    setMood(mood) {
        if (this.moodStates[mood]) {
            this.currentMood = mood;
        }
    }

    open() {
        if (this.isOpen) return;
        this.isOpen = true;

        this.overlay = document.createElement('div');
        this.overlay.id = 'affinity-overlay';
        this.overlay.style.cssText = `
            position: fixed; top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0, 0, 0, 0.95);
            z-index: 10000;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: 'Courier New', monospace;
        `;

        this.overlay.innerHTML = this.renderUI();
        document.body.appendChild(this.overlay);

        // Event Listeners
        this.overlay.querySelector('.close-btn').onclick = () => this.close();
        this.overlay.onclick = (e) => {
            if (e.target === this.overlay) this.close();
        };
    }

    renderUI() {
        const level = this.getCurrentLevel();
        const mood = this.moodStates[this.currentMood];
        const bondPercent = this.bondStrength;

        return `
            <div style="
                background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
                border: 3px solid ${level.color};
                border-radius: 20px;
                padding: 30px;
                min-width: 500px;
                max-width: 600px;
                color: white;
                box-shadow: 0 0 50px ${level.color}44;
            ">
                <!-- Header -->
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px;">
                    <h1 style="margin: 0; color: ${level.color};">💕 NAJIKA & KUJA</h1>
                    <button class="close-btn" style="
                        background: #ff4444;
                        border: none;
                        color: white;
                        padding: 8px 16px;
                        border-radius: 5px;
                        cursor: pointer;
                    ">✕</button>
                </div>

                <!-- Najika Portrait + Mood -->
                <div style="display: flex; gap: 20px; margin-bottom: 25px;">
                    <div style="
                        width: 120px;
                        height: 120px;
                        background: linear-gradient(135deg, #667eea, #764ba2);
                        border-radius: 60px;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        font-size: 50px;
                        border: 4px solid ${level.color};
                    ">
                        🎀
                    </div>
                    <div style="flex: 1;">
                        <div style="font-size: 24px; font-weight: bold; color: #ff69b4; margin-bottom: 5px;">
                            Najika
                        </div>
                        <div style="font-size: 14px; color: #888; margin-bottom: 10px;">
                            Gothic-Lolita • Explosion-Meisterin • Mädchen
                        </div>
                        <div style="display: flex; gap: 10px; align-items: center;">
                            <div style="
                                background: ${mood.color}33;
                                border: 2px solid ${mood.color};
                                padding: 8px 15px;
                                border-radius: 20px;
                                font-size: 14px;
                            ">
                                ${mood.icon} ${mood.name}
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Bond Level -->
                <div style="
                    background: rgba(0, 0, 0, 0.4);
                    border-radius: 15px;
                    padding: 20px;
                    margin-bottom: 20px;
                ">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <div style="font-size: 18px; color: ${level.color};">
                            ${level.icon} ${level.name}
                        </div>
                        <div style="font-size: 24px; font-weight: bold; color: ${level.color};">
                            ${bondPercent}%
                        </div>
                    </div>
                    <div style="background: #222; height: 20px; border-radius: 10px; overflow: hidden;">
                        <div style="
                            background: linear-gradient(90deg, ${level.color}, ${level.color}88);
                            height: 100%;
                            width: ${bondPercent}%;
                            transition: width 0.5s;
                        "></div>
                    </div>
                    <div style="font-size: 11px; color: #666; margin-top: 5px; text-align: right;">
                        ${this.totalInteractions} Interaktionen
                    </div>
                </div>

                <!-- Personality Distribution -->
                <div style="margin-bottom: 20px;">
                    <div style="font-size: 14px; color: #aaa; margin-bottom: 10px;">Persönlichkeits-Gewichtung:</div>
                    <div style="display: flex; gap: 10px;">
                        ${this.renderPersonalityBar('megumin', '💥', '#ff0066')}
                        ${this.renderPersonalityBar('harley', '🃏', '#e74c3c')}
                        ${this.renderPersonalityBar('shiro', '🎮', '#3498db')}
                        ${this.renderPersonalityBar('melissa', '👑', '#9b59b6')}
                    </div>
                </div>

                <!-- Recent Activities -->
                <div style="
                    background: rgba(0, 0, 0, 0.3);
                    border-radius: 10px;
                    padding: 15px;
                    max-height: 150px;
                    overflow-y: auto;
                ">
                    <div style="font-size: 12px; color: #888; margin-bottom: 10px;">Letzte Aktivitäten:</div>
                    ${this.recentActivities.length > 0 ? this.recentActivities.map(act => `
                        <div style="display: flex; justify-content: space-between; font-size: 11px; padding: 5px 0; border-bottom: 1px solid #333;">
                            <span style="color: #aaa;">${act.reason}</span>
                            <span style="color: ${act.bondChange >= 0 ? '#4CAF50' : '#e74c3c'};">
                                ${act.bondChange >= 0 ? '+' : ''}${act.bondChange}
                            </span>
                        </div>
                    `).join('') : '<div style="color: #555; font-size: 11px;">Noch keine Aktivitäten...</div>'}
                </div>

                <!-- Credo -->
                <div style="
                    margin-top: 20px;
                    text-align: center;
                    font-style: italic;
                    color: #666;
                    font-size: 12px;
                ">
                    "VERRAT KOSTET IMMER BLUT" 🗡️
                </div>
            </div>
        `;
    }

    renderPersonalityBar(key, icon, color) {
        const weight = this.personalityWeights[key];
        return `
            <div style="flex: 1; text-align: center;">
                <div style="font-size: 18px; margin-bottom: 5px;">${icon}</div>
                <div style="background: #222; height: 60px; border-radius: 5px; position: relative; overflow: hidden;">
                    <div style="
                        position: absolute;
                        bottom: 0;
                        left: 0;
                        right: 0;
                        background: ${color};
                        height: ${weight}%;
                    "></div>
                </div>
                <div style="font-size: 10px; color: #888; margin-top: 3px;">${weight}%</div>
            </div>
        `;
    }

    // Mini Widget für HUD
    createMiniWidget() {
        let widget = document.getElementById('affinity-mini-widget');
        if (!widget) {
            widget = document.createElement('div');
            widget.id = 'affinity-mini-widget';
            widget.style.cssText = `
                position: fixed;
                top: 100px;
                right: 20px;
                background: rgba(0, 0, 0, 0.85);
                border: 2px solid #ff69b4;
                border-radius: 10px;
                padding: 10px;
                color: white;
                font-family: 'Courier New', monospace;
                font-size: 12px;
                cursor: pointer;
                z-index: 500;
                transition: all 0.2s;
            `;
            widget.onclick = () => this.open();
            document.body.appendChild(widget);
        }

        const level = this.getCurrentLevel();
        const mood = this.moodStates[this.currentMood];

        widget.innerHTML = `
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 20px;">🎀</span>
                <div>
                    <div style="color: ${level.color};">${level.icon} ${this.bondStrength}%</div>
                    <div style="font-size: 10px; color: ${mood.color};">${mood.icon} ${mood.name}</div>
                </div>
            </div>
        `;
    }

    close() {
        if (this.overlay) {
            this.overlay.remove();
            this.overlay = null;
        }
        this.isOpen = false;
    }

    // Save/Load
    toJSON() {
        return {
            bondStrength: this.bondStrength,
            totalInteractions: this.totalInteractions,
            currentMood: this.currentMood,
            personalityWeights: this.personalityWeights,
            recentActivities: this.recentActivities.slice(0, 5)
        };
    }

    fromJSON(data) {
        if (!data) return;
        Object.assign(this, data);
    }
}

// Global instance
window.affinityUI = new AffinityUI();

// Keyboard shortcut [B] for Bond/Affinity
document.addEventListener('keydown', (e) => {
    if (e.key === 'b' || e.key === 'B') {
        if (!e.target.matches('input, textarea')) {
            if (window.affinityUI.isOpen) {
                window.affinityUI.close();
            } else {
                window.affinityUI.open();
            }
        }
    }
    if (e.key === 'Escape' && window.affinityUI.isOpen) {
        window.affinityUI.close();
    }
});

// Update mini widget periodically
setInterval(() => {
    if (window.affinityUI) {
        window.affinityUI.createMiniWidget();
    }
}, 10000);

// Initial widget
setTimeout(() => {
    if (window.affinityUI) {
        window.affinityUI.createMiniWidget();
    }
}, 2000);

console.log('💕 Affinity UI geladen - [B] zum Öffnen');
