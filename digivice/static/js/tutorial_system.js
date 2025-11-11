/**
 * NAJIKA WORLD - TUTORIAL SYSTEM
 * ================================
 *
 * Tutorial-System für neue Spieler:
 * - First-Time Detection
 * - Tutorial Popups
 * - Progressive Hints
 */

class TutorialSystem {
    constructor() {
        this.tutorialComplete = false;
        this.currentStep = 0;
        this.shownHints = new Set();

        // Tutorial steps
        this.steps = [
            {
                id: 'welcome',
                title: '🎮 Willkommen in Najika World!',
                text: 'Dies ist eine vollständige 3D-RPG-Welt!\n\nNutze WASD zum Bewegen und die Maus für die Kamera.',
                duration: 5000
            },
            {
                id: 'movement',
                title: '🚶 Bewegung',
                text: 'WASD: Bewegen\nMaus: Kamera drehen\nC: Kamera-Modus wechseln (Orbit/Third/First)',
                duration: 4000
            },
            {
                id: 'interact',
                title: '💬 Interaktion',
                text: 'E: Mit NPCs sprechen / Gebäude betreten\nTAB/I: Inventar öffnen\nQ/J: Quest Log öffnen\nK: Skills anzeigen',
                duration: 5000
            },
            {
                id: 'combat',
                title: '⚔️ Kampf',
                text: 'Q/E: Linke/Rechte Hand angreifen\nSPACE: Beide Hände\nX: Blocken\nC: Ausweichen\nV: Parieren',
                duration: 5000
            },
            {
                id: 'exploration',
                title: '🗺️ Erkunden',
                text: 'Besuche die 5 Städte in der Welt!\n\nJede Stadt hat NPCs, Quests, und besondere Features.\n\nViel Spaß!',
                duration: 5000
            }
        ];

        // Check first launch
        this.checkFirstLaunch();

        console.log('📚 Tutorial-System initialisiert');
    }

    checkFirstLaunch() {
        const hasPlayed = localStorage.getItem('najika_has_played');

        if (!hasPlayed) {
            // First time!
            this.startTutorial();
            localStorage.setItem('najika_has_played', 'true');
        } else {
            this.tutorialComplete = true;
            console.log('📚 Tutorial übersprungen (bereits gespielt)');
        }
    }

    startTutorial() {
        console.log('📚 Tutorial gestartet!');
        this.showStep(0);
    }

    showStep(stepIndex) {
        if (stepIndex >= this.steps.length) {
            this.completeTutorial();
            return;
        }

        const step = this.steps[stepIndex];
        this.currentStep = stepIndex;

        // Create popup
        const popup = this.createPopup(step);

        // Auto-advance after duration
        setTimeout(() => {
            this.closePopup(popup);

            // Show next step after 1 second
            setTimeout(() => {
                this.showStep(stepIndex + 1);
            }, 1000);
        }, step.duration);
    }

    createPopup(step) {
        const popup = document.createElement('div');
        popup.className = 'tutorial-popup';
        popup.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) scale(0.8);
            background: rgba(0, 0, 0, 0.95);
            padding: 30px;
            border-radius: 15px;
            border: 3px solid #4CAF50;
            color: white;
            font-family: 'Courier New', monospace;
            z-index: 10000;
            max-width: 500px;
            text-align: center;
            box-shadow: 0 0 30px rgba(76, 175, 80, 0.5);
            animation: popupIn 0.3s ease-out forwards;
        `;

        popup.innerHTML = `
            <div style="font-size: 24px; font-weight: bold; color: #4CAF50; margin-bottom: 15px;">
                ${step.title}
            </div>
            <div style="font-size: 16px; line-height: 1.6; white-space: pre-line;">
                ${step.text}
            </div>
            <div style="margin-top: 20px; font-size: 12px; color: #aaa;">
                Schritt ${this.currentStep + 1}/${this.steps.length}
            </div>
        `;

        // Add CSS animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes popupIn {
                to { transform: translate(-50%, -50%) scale(1); }
            }
            @keyframes popupOut {
                to { transform: translate(-50%, -50%) scale(0.8); opacity: 0; }
            }
        `;
        document.head.appendChild(style);

        document.body.appendChild(popup);
        return popup;
    }

    closePopup(popup) {
        popup.style.animation = 'popupOut 0.3s ease-out forwards';
        setTimeout(() => {
            if (popup.parentNode) {
                document.body.removeChild(popup);
            }
        }, 300);
    }

    completeTutorial() {
        this.tutorialComplete = true;
        console.log('✅ Tutorial abgeschlossen!');

        // Show completion message
        const popup = document.createElement('div');
        popup.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0, 0, 0, 0.95);
            padding: 30px;
            border-radius: 15px;
            border: 3px solid #FFD700;
            color: white;
            font-family: 'Courier New', monospace;
            z-index: 10000;
            text-align: center;
        `;

        popup.innerHTML = `
            <div style="font-size: 48px; margin-bottom: 15px;">🎉</div>
            <div style="font-size: 24px; font-weight: bold; color: #FFD700; margin-bottom: 15px;">
                Tutorial Abgeschlossen!
            </div>
            <div style="font-size: 16px;">
                Viel Spaß beim Erkunden von Najika World!
            </div>
            <button onclick="this.parentElement.remove()" style="
                margin-top: 20px;
                padding: 10px 20px;
                background: #4CAF50;
                border: none;
                border-radius: 5px;
                color: white;
                font-family: 'Courier New', monospace;
                font-size: 16px;
                cursor: pointer;
            ">Los geht's! 🚀</button>
        `;

        document.body.appendChild(popup);
    }

    // Show contextual hints
    showHint(hintId, text, duration = 3000) {
        if (this.shownHints.has(hintId)) return;

        this.shownHints.add(hintId);

        const hint = document.createElement('div');
        hint.style.cssText = `
            position: fixed;
            bottom: 100px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(0, 0, 0, 0.9);
            padding: 15px 25px;
            border-radius: 8px;
            border: 2px solid #4CAF50;
            color: white;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            z-index: 9000;
            text-align: center;
        `;

        hint.innerHTML = `💡 ${text}`;

        document.body.appendChild(hint);

        setTimeout(() => {
            hint.style.transition = 'opacity 0.3s';
            hint.style.opacity = '0';
            setTimeout(() => {
                if (hint.parentNode) {
                    document.body.removeChild(hint);
                }
            }, 300);
        }, duration);
    }

    // Reset tutorial
    resetTutorial() {
        localStorage.removeItem('najika_has_played');
        this.tutorialComplete = false;
        this.currentStep = 0;
        this.shownHints.clear();
        console.log('📚 Tutorial zurückgesetzt');
    }
}

// Export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TutorialSystem;
}
