// =============================================================================
// DIRECTION RESOLVER - Maus-Delta -> 4 Angriffs-Richtungen
// For Honor Style: OBEN / LINKS / RECHTS / UNTEN
// Kein UI-Pfeil - echte Bewegung entscheidet
// =============================================================================

const DirectionResolver = (function () {

    // Richtungs-Konstanten
    const DIR = {
        NEUTRAL: 'neutral',
        UP:      'up',
        DOWN:    'down',
        LEFT:    'left',
        RIGHT:   'right'
    };

    // Config
    const WINDOW_MS      = 300;   // Maus-Delta-Fenster in Millisekunden
    const MIN_THRESHOLD  = 12;    // Pixel-Mindestbewegung fuer Richtungserkennung
    const ATTACK_HOLD_MS = 150;   // Wie lange nach Attack-Press wird Maus-Delta gesammelt

    // State
    let mouseSamples = [];        // { dx, dy, t } - rollierendes Fenster
    let lastMouseX   = null;
    let lastMouseY   = null;
    let isListening  = false;

    // Attack-Capture State
    let captureActive    = false;
    let captureStartTime = 0;
    let captureBuffer    = [];    // Samples waehrend Attack-Druck
    let captureCallback  = null;  // Wird mit DIR-Wert aufgerufen

    // -------------------------------------------------------------------------
    // Intern: Maus-Bewegung aufzeichnen
    // -------------------------------------------------------------------------
    function onMouseMove(e) {
        const now = performance.now();

        if (lastMouseX !== null) {
            const dx = e.clientX - lastMouseX;
            const dy = e.clientY - lastMouseY;

            // Nur relevante Bewegungen speichern
            if (Math.abs(dx) > 0.5 || Math.abs(dy) > 0.5) {
                mouseSamples.push({ dx, dy, t: now });

                // Capture-Buffer befuellen wenn aktiv
                if (captureActive) {
                    captureBuffer.push({ dx, dy });
                }
            }
        }

        lastMouseX = e.clientX;
        lastMouseY = e.clientY;

        // Altes Sample-Fenster bereinigen
        const cutoff = now - WINDOW_MS;
        while (mouseSamples.length > 0 && mouseSamples[0].t < cutoff) {
            mouseSamples.shift();
        }
    }

    // -------------------------------------------------------------------------
    // Intern: Delta-Array -> Richtung mappen
    // -------------------------------------------------------------------------
    function samplesToDirection(samples) {
        if (!samples || samples.length === 0) return DIR.NEUTRAL;

        let totalDx = 0;
        let totalDy = 0;
        for (const s of samples) {
            totalDx += s.dx;
            totalDy += s.dy;
        }

        const mag = Math.sqrt(totalDx * totalDx + totalDy * totalDy);

        // Zu wenig Bewegung = neutral
        if (mag < MIN_THRESHOLD) return DIR.NEUTRAL;

        // Normieren und in 4 Sektoren aufteilen (je 90 Grad)
        // Y-Achse: negativ = Maus nach OBEN (Bildschirm-Koordinaten!)
        const absX = Math.abs(totalDx);
        const absY = Math.abs(totalDy);

        if (absY >= absX) {
            // Vertikale Dominanz
            return totalDy < 0 ? DIR.UP : DIR.DOWN;
        } else {
            // Horizontale Dominanz
            return totalDx < 0 ? DIR.LEFT : DIR.RIGHT;
        }
    }

    // -------------------------------------------------------------------------
    // Public: Event-Listener starten
    // -------------------------------------------------------------------------
    function init() {
        if (isListening) return;
        document.addEventListener('mousemove', onMouseMove, { passive: true });
        isListening = true;
        console.log('[DirectionResolver] Initialisiert');
    }

    // -------------------------------------------------------------------------
    // Public: Aktuelle Richtung aus rollendem Fenster lesen
    // Nuetzlich fuer Block-Richtung (kontinuierlich)
    // -------------------------------------------------------------------------
    function getCurrentDirection() {
        return samplesToDirection(mouseSamples);
    }

    // -------------------------------------------------------------------------
    // Public: Attack-Capture starten
    // Wird beim Druecken der Angriffs-Taste aufgerufen.
    // Sammelt Maus-Delta fuer ATTACK_HOLD_MS und gibt dann Richtung zurueck.
    //
    // callback(direction) wird nach ATTACK_HOLD_MS aufgerufen.
    // Wenn Spieler Maus vorher klar bewegt hat (>= MIN_THRESHOLD) wird sofort
    // aufgeloest ohne auf den vollen Timer zu warten.
    // -------------------------------------------------------------------------
    function startAttackCapture(callback) {
        captureBuffer   = [];
        captureActive   = true;
        captureStartTime = performance.now();
        captureCallback  = callback;

        // Auch aktuelles rollierendes Fenster einbeziehen (Voraus-Bewegung)
        const preBuffer = mouseSamples.slice(-10); // letzte 10 Samples

        // Sofort aufloesen wenn schon klare Richtung vorhanden
        const preDir = samplesToDirection(preBuffer);
        if (preDir !== DIR.NEUTRAL) {
            _resolveCapture(preDir);
            return;
        }

        // Sonst warten und nach ATTACK_HOLD_MS aufloesen
        setTimeout(() => {
            if (!captureActive) return; // Wurde schon aufgeloest
            const combined = [...preBuffer, ...captureBuffer];
            const dir = samplesToDirection(combined);
            _resolveCapture(dir);
        }, ATTACK_HOLD_MS);
    }

    function _resolveCapture(dir) {
        if (!captureActive) return;
        captureActive = false;
        if (typeof captureCallback === 'function') {
            captureCallback(dir);
        }
        captureCallback = null;
        captureBuffer   = [];
    }

    // -------------------------------------------------------------------------
    // Public: Block-Richtung (kontinuierlich, kein Capture-Fenster)
    // Fuer Block-Taste halten: liest aktuellen Maus-Delta
    // -------------------------------------------------------------------------
    function getBlockDirection() {
        // Letzte 150ms fuer Block-Richtung
        const now    = performance.now();
        const recent = mouseSamples.filter(s => s.t > now - 150);
        return samplesToDirection(recent);
    }

    // -------------------------------------------------------------------------
    // Public: Cleanup
    // -------------------------------------------------------------------------
    function destroy() {
        document.removeEventListener('mousemove', onMouseMove);
        isListening     = false;
        captureActive   = false;
        mouseSamples    = [];
        captureBuffer   = [];
        captureCallback = null;
        lastMouseX      = null;
        lastMouseY      = null;
    }

    // -------------------------------------------------------------------------
    // Public API
    // -------------------------------------------------------------------------
    return {
        init,
        getCurrentDirection,
        startAttackCapture,
        getBlockDirection,
        destroy,
        DIR   // Konstanten exportieren fuer andere Module
    };

})();

// Global verfuegbar machen
window.DirectionResolver = DirectionResolver;
