/**
 * NAJIKA WORLD - GLOBAL GAME EVENT BUS
 * =====================================
 * Verbindet alle Systeme miteinander.
 *
 * Events:
 *   enemyKilled    { enemyId, enemyType, biome, loot[] }
 *   itemCollected   { itemId, quantity, source }
 *   itemCrafted     { recipeId, resultItem }
 *   itemPurchased   { itemId, price, npcId }
 *   questCompleted  { questId, rewards }
 *   questAccepted   { questId }
 *   regionEntered   { regionId, biome }
 *   npcTalked       { npcId, npcName }
 *   combatStarted   { enemyData }
 *   combatEnded     { won, enemyData, loot }
 *   levelUp         { newLevel, stats }
 *   playerDamaged   { amount, source }
 */

(function() {
    'use strict';

    const listeners = {};
    let eventLog = [];
    const MAX_LOG = 100;

    const GameEvents = {
        /**
         * Event emittieren
         * @param {string} event - Event-Name
         * @param {object} data - Event-Daten
         */
        emit(event, data = {}) {
            const detail = { ...data, _timestamp: Date.now() };

            // Log für Debugging
            eventLog.push({ event, data: detail });
            if (eventLog.length > MAX_LOG) eventLog.shift();

            console.log(`🎮 [GameEvent] ${event}`, detail);

            // CustomEvent für DOM-basierte Listener
            document.dispatchEvent(new CustomEvent('game:' + event, { detail }));

            // Direkte Listener
            if (listeners[event]) {
                listeners[event].forEach(cb => {
                    try {
                        cb(detail);
                    } catch (err) {
                        console.error(`[GameEvent] Error in listener for "${event}":`, err);
                    }
                });
            }
        },

        /**
         * Auf Event lauschen
         * @param {string} event - Event-Name
         * @param {function} callback - Handler
         */
        on(event, callback) {
            if (!listeners[event]) listeners[event] = [];
            listeners[event].push(callback);
        },

        /**
         * Listener entfernen
         */
        off(event, callback) {
            if (!listeners[event]) return;
            listeners[event] = listeners[event].filter(cb => cb !== callback);
        },

        /**
         * Einmal-Listener
         */
        once(event, callback) {
            const wrapper = (data) => {
                callback(data);
                this.off(event, wrapper);
            };
            this.on(event, wrapper);
        },

        /**
         * Event-Log für Debugging
         */
        getLog() {
            return [...eventLog];
        },

        /**
         * Alle Listener entfernen
         */
        clear() {
            Object.keys(listeners).forEach(key => delete listeners[key]);
            eventLog = [];
        }
    };

    window.GameEvents = GameEvents;
    console.log('🎮 GameEvents Bus initialisiert');
})();
