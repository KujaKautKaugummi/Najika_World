/**
 * CLEANUP MANAGER
 * ===============
 * Globales System zur Verwaltung von EventListeners und Timers
 * Verhindert Memory Leaks durch automatisches Cleanup
 *
 * Usage:
 *   CleanupManager.addEventListener(window, 'keydown', handler, 'system-name');
 *   CleanupManager.setInterval(callback, 1000, 'system-name');
 *   CleanupManager.cleanupSystem('system-name');  // Cleanup einzelnes System
 *   CleanupManager.cleanupAll();  // Cleanup alles
 */

class CleanupManagerClass {
    constructor() {
        // Event Listeners Storage
        this.eventListeners = new Map();  // system -> [{target, event, handler, controller}]

        // Timers Storage
        this.timers = new Map();  // system -> [{id, type: 'interval'|'timeout'}]

        // Abort Controllers per System
        this.abortControllers = new Map();  // system -> AbortController

        console.log('[CLEANUP MANAGER] ✅ Initialized');
    }

    /**
     * EVENT LISTENER mit Auto-Cleanup
     * @param {EventTarget} target - window, document, element
     * @param {string} event - 'keydown', 'click', etc.
     * @param {Function} handler - Event Handler Function
     * @param {string} systemName - Name des Systems (z.B. 'chat-ui', 'quest-system')
     * @param {object} options - addEventListener options
     */
    addEventListener(target, event, handler, systemName = 'default', options = {}) {
        // Erstelle AbortController für dieses System (falls noch nicht existent)
        if (!this.abortControllers.has(systemName)) {
            this.abortControllers.set(systemName, new AbortController());
        }

        const controller = this.abortControllers.get(systemName);

        // Füge signal zu options hinzu
        const listenerOptions = { ...options, signal: controller.signal };

        // Registriere Listener
        target.addEventListener(event, handler, listenerOptions);

        // Speichere für Tracking
        if (!this.eventListeners.has(systemName)) {
            this.eventListeners.set(systemName, []);
        }

        this.eventListeners.get(systemName).push({
            target,
            event,
            handler,
            controller
        });

        console.log(`[CLEANUP MANAGER] 📌 Listener registered: ${systemName}.${event}`);
    }

    /**
     * SET INTERVAL mit Auto-Cleanup
     * @param {Function} callback - Function to execute
     * @param {number} interval - Interval in ms
     * @param {string} systemName - Name des Systems
     * @returns {number} intervalId
     */
    setInterval(callback, interval, systemName = 'default') {
        const intervalId = setInterval(callback, interval);

        // Speichere Timer
        if (!this.timers.has(systemName)) {
            this.timers.set(systemName, []);
        }

        this.timers.get(systemName).push({
            id: intervalId,
            type: 'interval'
        });

        console.log(`[CLEANUP MANAGER] ⏱️ Interval registered: ${systemName} (${interval}ms)`);

        return intervalId;
    }

    /**
     * SET TIMEOUT mit Auto-Cleanup
     * @param {Function} callback - Function to execute
     * @param {number} timeout - Timeout in ms
     * @param {string} systemName - Name des Systems
     * @returns {number} timeoutId
     */
    setTimeout(callback, timeout, systemName = 'default') {
        const timeoutId = setTimeout(callback, timeout);

        // Speichere Timer
        if (!this.timers.has(systemName)) {
            this.timers.set(systemName, []);
        }

        this.timers.get(systemName).push({
            id: timeoutId,
            type: 'timeout'
        });

        console.log(`[CLEANUP MANAGER] ⏱️ Timeout registered: ${systemName} (${timeout}ms)`);

        return timeoutId;
    }

    /**
     * CLEANUP EINZELNES SYSTEM
     * Entfernt alle EventListeners und Timers eines Systems
     * @param {string} systemName - Name des Systems
     */
    cleanupSystem(systemName) {
        let cleanedCount = 0;

        // Cleanup EventListeners (via AbortController)
        if (this.abortControllers.has(systemName)) {
            const controller = this.abortControllers.get(systemName);
            controller.abort();  // Alle Listener mit diesem signal werden entfernt
            this.abortControllers.delete(systemName);

            const listenerCount = this.eventListeners.get(systemName)?.length || 0;
            cleanedCount += listenerCount;

            this.eventListeners.delete(systemName);
            console.log(`[CLEANUP MANAGER] 🧹 Removed ${listenerCount} event listeners from: ${systemName}`);
        }

        // Cleanup Timers
        if (this.timers.has(systemName)) {
            const timers = this.timers.get(systemName);
            timers.forEach(timer => {
                if (timer.type === 'interval') {
                    clearInterval(timer.id);
                } else {
                    clearTimeout(timer.id);
                }
                cleanedCount++;
            });

            console.log(`[CLEANUP MANAGER] 🧹 Cleared ${timers.length} timers from: ${systemName}`);
            this.timers.delete(systemName);
        }

        if (cleanedCount > 0) {
            console.log(`[CLEANUP MANAGER] ✅ System cleaned: ${systemName} (${cleanedCount} items)`);
        }
    }

    /**
     * CLEANUP ALLES
     * Entfernt ALLE EventListeners und Timers
     */
    cleanupAll() {
        console.log('[CLEANUP MANAGER] 🧹 Cleaning up ALL systems...');

        let totalCleaned = 0;

        // Cleanup alle AbortControllers
        for (const [systemName, controller] of this.abortControllers.entries()) {
            controller.abort();
            const listenerCount = this.eventListeners.get(systemName)?.length || 0;
            totalCleaned += listenerCount;
        }
        this.abortControllers.clear();
        this.eventListeners.clear();

        // Cleanup alle Timers
        for (const [systemName, timers] of this.timers.entries()) {
            timers.forEach(timer => {
                if (timer.type === 'interval') {
                    clearInterval(timer.id);
                } else {
                    clearTimeout(timer.id);
                }
                totalCleaned++;
            });
        }
        this.timers.clear();

        console.log(`[CLEANUP MANAGER] ✅ Cleaned up ${totalCleaned} items`);
    }

    /**
     * GET STATUS
     * Zeigt aktuellen Status des Managers
     */
    getStatus() {
        const systems = new Set([
            ...this.eventListeners.keys(),
            ...this.timers.keys()
        ]);

        const status = {
            total_systems: systems.size,
            total_listeners: Array.from(this.eventListeners.values()).reduce((sum, arr) => sum + arr.length, 0),
            total_timers: Array.from(this.timers.values()).reduce((sum, arr) => sum + arr.length, 0),
            systems: {}
        };

        systems.forEach(systemName => {
            status.systems[systemName] = {
                listeners: this.eventListeners.get(systemName)?.length || 0,
                timers: this.timers.get(systemName)?.length || 0
            };
        });

        return status;
    }

    /**
     * PRINT STATUS (Debug)
     */
    printStatus() {
        const status = this.getStatus();
        console.log('[CLEANUP MANAGER] 📊 Status:', status);
        console.table(status.systems);
    }

    /**
     * CLEAR SINGLE TIMER
     * Für manuelle Timer-Entfernung
     * @param {number} timerId
     * @param {string} systemName
     */
    clearTimer(timerId, systemName) {
        if (!this.timers.has(systemName)) return;

        const timers = this.timers.get(systemName);
        const index = timers.findIndex(t => t.id === timerId);

        if (index > -1) {
            const timer = timers[index];
            if (timer.type === 'interval') {
                clearInterval(timer.id);
            } else {
                clearTimeout(timer.id);
            }
            timers.splice(index, 1);
            console.log(`[CLEANUP MANAGER] 🧹 Cleared timer: ${systemName}.${timerId}`);
        }
    }
}

// Global Instance
window.CleanupManager = new CleanupManagerClass();

// Auto-Cleanup bei Page Unload
window.addEventListener('beforeunload', () => {
    console.log('[CLEANUP MANAGER] 🧹 Page unload - cleaning up...');
    window.CleanupManager.cleanupAll();
});

// Cleanup Interval für Debug (zeigt Status alle 60s)
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    setInterval(() => {
        const status = window.CleanupManager.getStatus();
        if (status.total_listeners > 50 || status.total_timers > 10) {
            console.warn('[CLEANUP MANAGER] ⚠️ High resource usage detected!');
            window.CleanupManager.printStatus();
        }
    }, 60000);  // Alle 60s checken
}

console.log('[CLEANUP MANAGER] ✅ Cleanup Manager loaded - Use window.CleanupManager');
