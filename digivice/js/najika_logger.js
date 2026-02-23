/**
 * NAJIKA LOGGER - Claude Code Session Logging
 * Sendet alle wichtigen Events an Najika's Backend
 */

const NajikaLogger = (function() {
    const API_BASE = window.API_BASE_URL || 'http://localhost:8000';

    // Log-Queue für Offline-Modus
    let logQueue = [];
    let isOnline = true;

    // Log Types
    const LOG_TYPES = {
        INFO: 'info',
        ACTION: 'action',
        ERROR: 'error',
        TASK: 'task',
        CHAT: 'chat',
        SYSTEM: 'system'
    };

    /**
     * Sendet ein Log an Najika's Backend
     */
    async function log(type, message, details = {}) {
        const logEntry = {
            type: type,
            message: message,
            details: {
                ...details,
                timestamp: new Date().toISOString(),
                url: window.location.href
            }
        };

        try {
            const response = await fetch(`${API_BASE}/api/log/claude`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(logEntry)
            });

            if (response.ok) {
                console.log(`[NajikaLogger] ✅ ${type}: ${message}`);
                isOnline = true;
                // Flush queue if any
                flushQueue();
            } else {
                throw new Error('Server error');
            }
        } catch (error) {
            console.warn(`[NajikaLogger] ⚠️ Offline - queuing: ${message}`);
            isOnline = false;
            logQueue.push(logEntry);
            // Keep only last 50 in queue
            if (logQueue.length > 50) logQueue.shift();
        }
    }

    /**
     * Sendet Queue wenn wieder online
     */
    async function flushQueue() {
        if (logQueue.length === 0) return;

        const toSend = [...logQueue];
        logQueue = [];

        for (const entry of toSend) {
            try {
                await fetch(`${API_BASE}/api/log/claude`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(entry)
                });
            } catch (e) {
                // Put back in queue
                logQueue.push(entry);
            }
        }
    }

    // ===== CONVENIENCE METHODS =====

    function info(message, details) {
        return log(LOG_TYPES.INFO, message, details);
    }

    function action(message, details) {
        return log(LOG_TYPES.ACTION, message, details);
    }

    function error(message, details) {
        return log(LOG_TYPES.ERROR, message, details);
    }

    function task(message, details) {
        return log(LOG_TYPES.TASK, message, details);
    }

    function chat(message, details) {
        return log(LOG_TYPES.CHAT, message, details);
    }

    function system(message, details) {
        return log(LOG_TYPES.SYSTEM, message, details);
    }

    // ===== AUTO-LOGGING HOOKS =====

    // Log page load
    document.addEventListener('DOMContentLoaded', () => {
        system('Page loaded', { page: document.title });
    });

    // Log errors
    window.addEventListener('error', (event) => {
        error('JavaScript Error', {
            message: event.message,
            filename: event.filename,
            lineno: event.lineno,
            colno: event.colno
        });
    });

    // Log unhandled promise rejections
    window.addEventListener('unhandledrejection', (event) => {
        error('Unhandled Promise Rejection', {
            reason: String(event.reason)
        });
    });

    // Retry queue every 30 seconds
    setInterval(flushQueue, 30000);

    console.log('[NajikaLogger] ✅ Initialized - Najika sieht alles!');

    // Export
    return {
        log,
        info,
        action,
        error,
        task,
        chat,
        system,
        LOG_TYPES,
        getQueue: () => [...logQueue],
        isOnline: () => isOnline
    };
})();

// Global export
window.NajikaLogger = NajikaLogger;
