// Render Room Actions - SAFE VERSION
async function renderActions(room) {
    const resp = await api('/api/room/actions', 'POST', {room});
    const wrap = document.getElementById('room-actions');
    if (!wrap) return;
    
    wrap.innerHTML = '';
    
    (resp.actions || []).forEach(a => {
        const b = document.createElement('button');
        b.className = 'action-btn';
        b.textContent = a;
        b.onclick = () => handleAction(room, a);
        wrap.appendChild(b);
    });
    
    // Safe battlePanel check
    const battlePanel = document.getElementById('battlePanel');
    if (battlePanel) {
        if (resp.battle) {
            // Keep visible if already in battle
        } else {
            battlePanel.style.display = 'none';
        }
    }
}

// Action Handler - SAFE VERSION
async function handleAction(room, action) {
    switch(action) {
        case 'Füttern':
            if (typeof notify === 'function') notify('🍖 Najika ist satt!', 'success');
            break;
        case 'Reden':
            // Chat über das Eingabefeld im UI statt prompt()
            if (typeof notify === 'function') notify('💬 Nutze das Chat-Feld um mit Najika zu reden', 'info');
            break;
        case 'Schlafen':
            if (typeof notify === 'function') notify('😴 Najika schläft...', 'info');
            break;
        case 'Lesen':
            if (typeof notify === 'function') notify('📚 Najika liest ein Buch.', 'info');
            break;
        case 'Kochen':
            if (typeof notify === 'function') notify('👩‍🍳 Najika kocht etwas Leckeres!', 'success');
            break;
        case 'Toilette':
            if (typeof notify === 'function') notify('🚽 Kurze Pause...', 'info');
            break;
        case 'Waschen':
            if (typeof notify === 'function') notify('🧼 Najika wäscht sich.', 'info');
            break;
        case 'Gießen':
            await api('/api/minigame/garden', 'POST', {mode: 'water'});
            if (typeof notify === 'function') notify('🌿 Garten gegossen!', 'success');
            break;
        case 'Ernten':
            if (typeof notify === 'function') notify('🌾 Ernte eingeholt!', 'success');
            break;
        case 'Garten-Spiel':
            const gg = await api('/api/minigame/garden', 'POST', {});
            MiniGames.open('garden');
            break;
        case 'Rhythmus-Spiel':
            const rr = await api('/api/minigame/rhythm', 'POST', {});
            MiniGames.open('rhythm');
            break;
        case 'Heilen':
            const h = await api('/api/heal', 'POST', {});
            if (typeof notify === 'function') notify('💊 Geheilt! HP: ' + h.hp, 'success');
            updateBattleHUD({hp: h.hp, max_hp: 100});
            break;
        case 'Cloud':
            toggleCloud();
            break;
        case 'Status':
            const s = await api('/health');
            if (typeof notify === 'function') notify('📊 Status geladen (siehe Konsole)', 'info');
            console.log('📊 Status:', s);
            break;
        case 'Studieren':
            const ev = await api('/api/event/next', 'POST', {});
            if (typeof notify === 'function') notify('📜 ' + (ev.title || 'Event') + ': ' + (ev.text || ''), 'info');
            break;
        case 'Crafting':
            const c = await api('/api/crafting', 'POST', {});
            if (typeof notify === 'function') notify('🔨 ' + (c.msg || 'Crafting abgeschlossen!'), 'success');
            break;
        case 'Reflex-Spiel':
            const rx = await api('/api/minigame/reflex', 'POST', {});
            MiniGames.open('reflex');
            break;
        case 'Trainieren':
            // Stille Notification statt Alert
            if (typeof showNotification === 'function') {
                showNotification('🏋️ Training absolviert!');
            } else {
                console.log('🏋️ Training absolviert!');
            }
            break;
        case 'Kampf starten':
            const kb = await api('/api/battle/start', 'POST', {room});
            if (kb.ok) {
                const panel = document.getElementById('battlePanel');
                if (panel) {
                    panel.style.display = 'block';
                    updateBattleHUD({hp: 100, max_hp: 100, wave: 1, enemies: 3});
                }
                // Stille Notification statt Alert
                if (typeof showNotification === 'function') {
                    showNotification('⚔️ Kampf gestartet! Nutze den Angriff-Button!');
                }
            }
            break;
        case 'Erkunden':
            if (typeof showNotification === 'function') {
                showNotification('🔎 Du erkundest den Keller der Schwarzen Mühle...');
            }
            break;
        default:
            console.log('Aktion: ' + action);
    }
}

