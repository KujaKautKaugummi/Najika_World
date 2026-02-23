// Private Mode Indicator with SSE
(function() {
    let eventSource = null;
    const indicator = document.getElementById('privateIndicator');

    function connect() {
        if (eventSource) {
            eventSource.close();
        }

        eventSource = new EventSource('http://localhost:8000/api/status/stream');

        eventSource.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                updatePrivateMode(data.private_mode || false);
            } catch (error) {
                console.warn('Private Mode: parse error', error);
            }
        };

        eventSource.onerror = () => {
            eventSource.close();
            setTimeout(connect, 3000);
        };
    }

    function updatePrivateMode(active) {
        if (indicator) {
            if (active) {
                indicator.classList.add('active');
            } else {
                indicator.classList.remove('active');
            }
        }
        if (window.Scene3D && typeof window.Scene3D.setPrivateMode === 'function') {
            window.Scene3D.setPrivateMode(active);
        }
        // Chat-Mode synchronisieren
        if (window.chatUI) {
            window.chatUI.chatMode = active ? 'private' : 'public';
            window.chatUI.updateModeButton();
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', connect);
    } else {
        connect();
    }

    console.log('✅ Private Mode monitor started');
})();
