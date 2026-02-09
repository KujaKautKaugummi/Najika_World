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
            alert('🍖 Najika ist satt!');
            break;
        case 'Reden':
            const text = prompt('Sag etwas zu Najika:');
            if (text) {
                const r = await api('/api/chat', 'POST', {message: text});
                alert('Najika: ' + (r.response || '…'));
            }
            break;
        case 'Schlafen':
            alert('😴 Najika schläft...');
            break;
        case 'Lesen':
            alert('📚 Najika liest ein Buch.');
            break;
        case 'Kochen':
            alert('👩‍🍳 Najika kocht etwas Leckeres!');
            break;
        case 'Toilette':
            alert('🚽 Kurze Pause...');
            break;
        case 'Waschen':
            alert('🧼 Najika wäscht sich.');
            break;
        case 'Gießen':
            await api('/api/minigame/garden', 'POST', {mode: 'water'});
            alert('🌿 Garten gegossen!');
            break;
        case 'Ernten':
            alert('🌾 Ernte eingeholt!');
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
            alert('💊 Geheilt! HP: ' + h.hp);
            updateBattleHUD({hp: h.hp, max_hp: 100});
            break;
        case 'Cloud':
            toggleCloud();
            break;
        case 'Status':
            const s = await api('/health');
            alert('Status:\n' + JSON.stringify(s, null, 2));
            break;
        case 'Studieren':
            const ev = await api('/api/event/next', 'POST', {});
            alert('📜 Event: ' + ev.title + '\n\n' + ev.text);
            break;
        case 'Crafting':
            const c = await api('/api/crafting', 'POST', {});
            alert('🔨 ' + c.msg);
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

