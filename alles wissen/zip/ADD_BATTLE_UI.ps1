# ==============================================================================
# ADD_BATTLE_UI.ps1
# Fügt sichtbares Kampf-Interface hinzu
# ==============================================================================

Write-Host ""
Write-Host "=== BATTLE UI INTEGRATION ===" -ForegroundColor Cyan
Write-Host ""

$htmlPath = "C:\NajikaCore\index_3d.html"

if (-not (Test-Path $htmlPath)) {
    Write-Host "FEHLER: index_3d.html nicht gefunden!" -ForegroundColor Red
    Read-Host "Enter"
    exit
}

# Lese HTML
$html = Get-Content $htmlPath -Raw -Encoding UTF8

# Füge Battle UI CSS hinzu (vor </style>)
$battleCSS = @'

/* BATTLE SYSTEM UI */
#battle-overlay {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0,0,0,0.95);
    z-index: 2000;
    overflow-y: auto;
}

#battle-overlay.active {
    display: flex;
    flex-direction: column;
}

#battle-header {
    background: linear-gradient(145deg, #c0392b, #e74c3c);
    padding: 20px;
    text-align: center;
    color: white;
    font-size: 24px;
    font-weight: bold;
}

#battle-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    padding: 20px;
    max-width: 800px;
    margin: 0 auto;
    width: 100%;
}

#battle-allies {
    background: rgba(0, 255, 65, 0.1);
    border: 2px solid #00ff41;
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 20px;
}

.battle-character {
    display: flex;
    align-items: center;
    margin: 10px 0;
    padding: 10px;
    background: rgba(255,255,255,0.05);
    border-radius: 8px;
}

.battle-character-name {
    flex: 1;
    color: white;
    font-weight: bold;
    font-size: 16px;
}

.battle-hp-bar {
    width: 200px;
    height: 20px;
    background: #333;
    border-radius: 10px;
    overflow: hidden;
    margin: 0 10px;
}

.battle-hp-fill {
    height: 100%;
    background: linear-gradient(90deg, #e74c3c, #c0392b);
    transition: width 0.3s;
}

.battle-hp-fill.ally {
    background: linear-gradient(90deg, #00ff41, #00cc33);
}

.battle-hp-text {
    color: white;
    font-size: 14px;
    min-width: 80px;
}

#battle-enemies {
    background: rgba(255, 0, 0, 0.1);
    border: 2px solid #e74c3c;
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 20px;
}

.enemy-defeated {
    opacity: 0.3;
}

#battle-actions {
    background: rgba(0,0,0,0.7);
    border: 2px solid #00ff41;
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 20px;
}

.battle-btn {
    background: linear-gradient(145deg, #444, #222);
    border: 2px solid #00ff41;
    border-radius: 10px;
    color: white;
    padding: 15px 20px;
    margin: 5px;
    cursor: pointer;
    font-size: 16px;
    font-weight: bold;
    transition: 0.2s;
}

.battle-btn:hover {
    background: linear-gradient(145deg, #00ff41, #00cc33);
    color: black;
    transform: scale(1.05);
}

.battle-btn:disabled {
    opacity: 0.3;
    cursor: not-allowed;
}

#battle-log {
    background: rgba(0,0,0,0.8);
    border: 2px solid #555;
    border-radius: 10px;
    padding: 15px;
    max-height: 200px;
    overflow-y: auto;
    color: white;
    font-size: 14px;
}

.battle-log-entry {
    padding: 5px 0;
    border-bottom: 1px solid #333;
}

.battle-log-entry:last-child {
    border-bottom: none;
}

#battle-turn-indicator {
    text-align: center;
    font-size: 20px;
    font-weight: bold;
    color: #00ff41;
    margin: 15px 0;
    text-transform: uppercase;
}
'@

$html = $html -replace '(</style>)', "$battleCSS`n`$1"

# Füge Battle UI HTML hinzu (vor </body>)
$battleHTML = @'

    <!-- BATTLE OVERLAY -->
    <div id="battle-overlay">
        <div id="battle-header">⚔️ KAMPFARENA ⚔️</div>
        <div id="battle-content">
            
            <!-- Verbündete -->
            <div id="battle-allies">
                <h3 style="color: #00ff41; margin-bottom: 10px;">VERBÜNDETE</h3>
                <div class="battle-character">
                    <div class="battle-character-name">Kuja (Du)</div>
                    <div class="battle-hp-bar">
                        <div class="battle-hp-fill ally" id="player-hp-bar" style="width: 100%;"></div>
                    </div>
                    <div class="battle-hp-text" id="player-hp-text">100/100</div>
                </div>
                <div class="battle-character">
                    <div class="battle-character-name">Najika 💜</div>
                    <div class="battle-hp-bar">
                        <div class="battle-hp-fill ally" id="najika-hp-bar" style="width: 100%;"></div>
                    </div>
                    <div class="battle-hp-text" id="najika-hp-text">150/150</div>
                </div>
            </div>
            
            <!-- Gegner -->
            <div id="battle-enemies">
                <h3 style="color: #e74c3c; margin-bottom: 10px;">GEGNER</h3>
                <div id="enemy-list"></div>
            </div>
            
            <!-- Turn Indicator -->
            <div id="battle-turn-indicator"></div>
            
            <!-- Aktionen -->
            <div id="battle-actions"></div>
            
            <!-- Log -->
            <div id="battle-log"></div>
            
        </div>
    </div>
'@

$html = $html -replace '(</body>)', "$battleHTML`n`$1"

# Speichere
Set-Content $htmlPath $html -Encoding UTF8

Write-Host "✓ Battle UI in HTML eingefügt!" -ForegroundColor Green
Write-Host ""

# ==============================================================================
# UPDATE BATTLE.JS MIT UI-FUNKTIONEN
# ==============================================================================

Write-Host "Update battle.js mit UI-Funktionen..." -ForegroundColor Yellow

$battleJSPath = "C:\NajikaCore\js\battle.js"

$enhancedBattleJS = @'
// NAJIKA BATTLE SYSTEM - MIT UI
class NajikaBattle {
    constructor() {
        this.player = {
            hp: 100,
            maxHp: 100,
            attack: 15,
            defense: 10,
            speed: 12
        };
        
        this.najika = {
            hp: 150,
            maxHp: 150,
            attack: 20,
            defense: 15,
            speed: 18
        };
        
        this.enemies = [];
        this.turn = 'player';
        this.battleActive = false;
    }
    
    startBattle(enemyCount = 1) {
        console.log(`Battle Start: ${enemyCount} Gegner!`);
        
        // Reset
        this.player.hp = this.player.maxHp;
        this.najika.hp = this.najika.maxHp;
        
        // Gegner generieren
        this.enemies = [];
        for (let i = 0; i < enemyCount; i++) {
            this.enemies.push(this.generateEnemy(i));
        }
        
        this.battleActive = true;
        this.turn = 'player';
        
        // Zeige UI
        document.getElementById('battle-overlay').classList.add('active');
        
        this.updateUI();
        this.addLog('Najika: Lass uns kämpfen, Kuja! EXPLOSION!');
    }
    
    endBattle() {
        this.battleActive = false;
        document.getElementById('battle-overlay').classList.remove('active');
    }
    
    generateEnemy(index) {
        const types = [
            {name: 'Schwacher Gegner', hp: 40, atk: 8, def: 3},
            {name: 'Normaler Gegner', hp: 60, atk: 12, def: 6},
            {name: 'Starker Gegner', hp: 90, atk: 18, def: 10}
        ];
        
        const type = types[Math.min(index, 2)];
        
        return {
            id: index,
            name: `${type.name} ${index + 1}`,
            hp: type.hp,
            maxHp: type.hp,
            attack: type.atk,
            defense: type.def,
            alive: true
        };
    }
    
    playerAttack(enemyIndex) {
        if (!this.battleActive || this.turn !== 'player') return;
        
        const enemy = this.enemies[enemyIndex];
        if (!enemy || !enemy.alive) return;
        
        const damage = Math.max(1, this.player.attack - enemy.defense + Math.floor(Math.random() * 10) - 5);
        enemy.hp = Math.max(0, enemy.hp - damage);
        
        this.addLog(`Du greifst ${enemy.name} an! ${damage} Schaden!`);
        
        if (enemy.hp <= 0) {
            enemy.alive = false;
            this.addLog(`${enemy.name} wurde besiegt!`);
        }
        
        this.updateUI();
        
        if (this.checkBattleEnd()) return;
        
        this.turn = 'najika';
        setTimeout(() => this.najikaAttack(), 1000);
    }
    
    najikaAttack() {
        if (!this.battleActive || this.turn !== 'najika') return;
        
        const aliveEnemies = this.enemies.filter(e => e.alive);
        if (aliveEnemies.length === 0) return;
        
        const target = aliveEnemies[Math.floor(Math.random() * aliveEnemies.length)];
        const damage = Math.max(1, this.najika.attack - target.defense + Math.floor(Math.random() * 15) - 7);
        target.hp = Math.max(0, target.hp - damage);
        
        this.addLog(`Najika: EXPLOSION! ${damage} Schaden an ${target.name}!`);
        
        if (target.hp <= 0) {
            target.alive = false;
            this.addLog(`${target.name} wurde vernichtet!`);
        }
        
        this.updateUI();
        
        if (this.checkBattleEnd()) return;
        
        this.turn = 'enemy';
        setTimeout(() => this.enemyTurn(), 1500);
    }
    
    enemyTurn() {
        if (!this.battleActive || this.turn !== 'enemy') return;
        
        const aliveEnemies = this.enemies.filter(e => e.alive);
        
        aliveEnemies.forEach(enemy => {
            const target = Math.random() < 0.5 ? 'player' : 'najika';
            const targetObj = target === 'player' ? this.player : this.najika;
            
            const damage = Math.max(1, enemy.attack - targetObj.defense + Math.floor(Math.random() * 8) - 4);
            targetObj.hp = Math.max(0, targetObj.hp - damage);
            
            this.addLog(`${enemy.name} greift ${target === 'player' ? 'Dich' : 'Najika'} an! ${damage} Schaden!`);
        });
        
        this.updateUI();
        
        if (this.checkBattleEnd()) return;
        
        this.turn = 'player';
        this.updateUI();
    }
    
    checkBattleEnd() {
        const aliveEnemies = this.enemies.filter(e => e.alive).length;
        
        if (aliveEnemies === 0) {
            this.battleActive = false;
            this.addLog('🎉 SIEG! Najika: Wir haben gewonnen, Kuja!');
            setTimeout(() => this.endBattle(), 3000);
            return true;
        }
        
        if (this.player.hp <= 0 || this.najika.hp <= 0) {
            this.battleActive = false;
            this.addLog('💀 NIEDERLAGE! Najika: Wir müssen stärker werden!');
            setTimeout(() => this.endBattle(), 3000);
            return true;
        }
        
        return false;
    }
    
    updateUI() {
        // Update Ally HP
        this.updateHPBar('player', this.player);
        this.updateHPBar('najika', this.najika);
        
        // Update Enemies
        this.updateEnemyList();
        
        // Update Actions
        this.updateActions();
        
        // Update Turn Indicator
        const indicator = document.getElementById('battle-turn-indicator');
        if (indicator) {
            if (this.battleActive) {
                if (this.turn === 'player') {
                    indicator.textContent = '▶ DEIN ZUG';
                    indicator.style.color = '#00ff41';
                } else if (this.turn === 'najika') {
                    indicator.textContent = '▶ NAJIKA\'S ZUG';
                    indicator.style.color = '#9b59b6';
                } else {
                    indicator.textContent = '▶ GEGNER-ZUG';
                    indicator.style.color = '#e74c3c';
                }
            } else {
                indicator.textContent = '';
            }
        }
    }
    
    updateHPBar(id, character) {
        const bar = document.getElementById(`${id}-hp-bar`);
        const text = document.getElementById(`${id}-hp-text`);
        
        if (bar) {
            const percent = (character.hp / character.maxHp) * 100;
            bar.style.width = `${percent}%`;
        }
        
        if (text) {
            text.textContent = `${character.hp}/${character.maxHp}`;
        }
    }
    
    updateEnemyList() {
        const list = document.getElementById('enemy-list');
        if (!list) return;
        
        list.innerHTML = '';
        
        this.enemies.forEach(enemy => {
            const div = document.createElement('div');
            div.className = 'battle-character' + (enemy.alive ? '' : ' enemy-defeated');
            
            div.innerHTML = `
                <div class="battle-character-name">${enemy.name}</div>
                <div class="battle-hp-bar">
                    <div class="battle-hp-fill" style="width: ${(enemy.hp / enemy.maxHp) * 100}%;"></div>
                </div>
                <div class="battle-hp-text">${enemy.hp}/${enemy.maxHp}</div>
            `;
            
            list.appendChild(div);
        });
    }
    
    updateActions() {
        const actions = document.getElementById('battle-actions');
        if (!actions) return;
        
        actions.innerHTML = '';
        
        if (this.turn === 'player' && this.battleActive) {
            this.enemies.forEach((enemy, i) => {
                if (enemy.alive) {
                    const btn = document.createElement('button');
                    btn.className = 'battle-btn';
                    btn.textContent = `⚔️ Angriff auf ${enemy.name}`;
                    btn.onclick = () => this.playerAttack(i);
                    actions.appendChild(btn);
                }
            });
        } else {
            const info = document.createElement('div');
            info.style.color = 'white';
            info.style.textAlign = 'center';
            info.style.padding = '20px';
            info.textContent = this.battleActive ? 'Warte...' : 'Kampf beendet';
            actions.appendChild(info);
        }
    }
    
    addLog(message) {
        const log = document.getElementById('battle-log');
        if (!log) return;
        
        const entry = document.createElement('div');
        entry.className = 'battle-log-entry';
        entry.textContent = message;
        
        log.appendChild(entry);
        log.scrollTop = log.scrollHeight;
        
        console.log(message);
    }
}

window.battle = new NajikaBattle();

// Test-Funktion für Kampfraum
if (typeof window.testBattle === 'undefined') {
    window.testBattle = function() {
        battle.startBattle(3);
    };
}
'@

Set-Content $battleJSPath $enhancedBattleJS -Encoding UTF8

Write-Host "✓ battle.js mit UI-Funktionen aktualisiert!" -ForegroundColor Green
Write-Host ""

# ==============================================================================
# KAMPFRAUM ACTION HINZUFÜGEN
# ==============================================================================

Write-Host "Füge Kampf-Button im Kampfraum hinzu..." -ForegroundColor Yellow

# Finde und update room_config
$configPath = "C:\NajikaCore\assets\room_config_detailed.json"

if (Test-Path $configPath) {
    $config = Get-Content $configPath -Raw -Encoding UTF8 | ConvertFrom-Json
    
    # Füge Kampf-Action hinzu wenn nicht vorhanden
    if ($config.battle.actions -notcontains 'start_battle') {
        $config.battle.actions += @{
            id = 'start_battle'
            label = '⚔️ Kampf starten'
            onclick = 'battle.startBattle(3)'
        }
        
        $config | ConvertTo-Json -Depth 10 | Set-Content $configPath -Encoding UTF8
        Write-Host "✓ Kampf-Action in room_config hinzugefügt!" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "=== BATTLE UI FERTIG! ===" -ForegroundColor Green
Write-Host ""

Write-Host "TESTEN:" -ForegroundColor Yellow
Write-Host "  1. Starte Python Server" -ForegroundColor White
Write-Host "  2. Öffne http://localhost:8000/index_3d.html" -ForegroundColor White
Write-Host "  3. Gehe zur Kampfarena" -ForegroundColor White
Write-Host "  4. Klicke '⚔️ Kampf starten'" -ForegroundColor White
Write-Host ""
Write-Host "ODER im Browser Console:" -ForegroundColor Yellow
Write-Host "  battle.startBattle(3)" -ForegroundColor White
Write-Host ""

Read-Host "Enter zum Beenden"