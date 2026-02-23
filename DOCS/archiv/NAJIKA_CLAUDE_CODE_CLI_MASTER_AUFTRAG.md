# 🚀 NAJIKA PROJEKT - VOLLSTÄNDIGER IMPLEMENTIERUNGS-AUFTRAG
## Für Claude Code CLI (Lokales Modell)

**Datum:** 26. November 2025  
**Projekt:** C:\Najika_World\ und C:\Najika\  
**Ziel:** ALLES zum Laufen bringen - Browser + Mobile APK

---

# ⚠️ WICHTIG: LIES ALLES BEVOR DU STARTEST!

Dieser Auftrag hat **7 BLÖCKE**. Arbeite sie **DER REIHE NACH** ab.
Nach jedem Block: TESTEN ob es funktioniert!

---

# BLOCK 1: EQUIPMENT-BASIERTES COMBAT SYSTEM

## 1.1 DAS KONZEPT (WICHTIG!)

**NICHT** separate Light/Heavy Buttons pro Hand!
**STATTDESSEN:** Was in der Hand ausgerüstet ist, bestimmt den Angriff:

```
AUSRÜSTUNG          → LIGHT ATTACK (LMB/Tap)    → HEAVY ATTACK (R/Hold)
─────────────────────────────────────────────────────────────────────
Schwert (Linke Hand) → Schneller Hieb (15 DMG)  → Kraftschlag (40 DMG)
Schwert (Rechte Hand)→ Schneller Hieb (15 DMG)  → Kraftschlag (40 DMG)
Feuerball-Zauber     → Feuerball (20 DMG)       → Inferno (60 DMG)
Eiszauber            → Eissplitter (18 DMG)     → Blizzard (55 DMG)
Bogen                → Schnellschuss (12 DMG)   → Gezielter Schuss (45 DMG)
Schild               → Schildstoß (8 DMG)       → Block (Parry-Window)
Heilzauber           → Kleine Heilung (+20 HP)  → Große Heilung (+60 HP)
LEER (Faust)         → Fauststoß (5 DMG)        → Uppercut (15 DMG)

ZWEIHÄNDIG (z.B. Großschwert, Stab):
→ Beide Hände = Ein Angriff (aber stärker!)
→ Großschwert Light: 25 DMG | Heavy: 70 DMG
→ Explosions-Stab Light: 30 DMG | Heavy: 100 DMG (EXPLOSION!)
```

## 1.2 Neue Datei: `C:\Najika_World\digivice\js\equipment_combat.js`

```javascript
// =============================================================================
// EQUIPMENT-BASED COMBAT SYSTEM
// Was ausgerüstet ist = Was der Angriff macht
// =============================================================================

class EquipmentCombatSystem {
    constructor() {
        // Equipment Slots
        this.leftHand = null;   // Item-Objekt oder null
        this.rightHand = null;  // Item-Objekt oder null
        this.isTwoHanded = false;
        
        // Combat State
        this.stamina = 100;
        this.maxStamina = 100;
        this.staminaRegen = 10; // pro Sekunde
        this.lastAttackTime = { left: 0, right: 0 };
        this.comboCount = 0;
        this.lastComboTime = 0;
        
        // Equipment Database
        this.equipmentDB = this.initEquipmentDB();
        
        // Start Stamina Regen
        setInterval(() => this.regenStamina(), 100);
    }
    
    initEquipmentDB() {
        return {
            // WAFFEN
            "iron_sword": {
                name: "Eisenschwert",
                type: "weapon",
                slot: "one_hand",
                attacks: {
                    light: { damage: 15, stamina: 10, cooldown: 400, anim: "slash_quick" },
                    heavy: { damage: 40, stamina: 25, cooldown: 800, anim: "slash_power" }
                }
            },
            "fire_sword": {
                name: "Flammenschwert",
                type: "weapon",
                slot: "one_hand",
                element: "fire",
                attacks: {
                    light: { damage: 18, stamina: 12, cooldown: 450, anim: "slash_fire", effect: "burn" },
                    heavy: { damage: 50, stamina: 30, cooldown: 900, anim: "slash_inferno", effect: "burn_aoe" }
                }
            },
            "greatsword": {
                name: "Großschwert",
                type: "weapon",
                slot: "two_hand",
                attacks: {
                    light: { damage: 25, stamina: 20, cooldown: 600, anim: "greatsword_swing" },
                    heavy: { damage: 70, stamina: 40, cooldown: 1200, anim: "greatsword_slam" }
                }
            },
            "bow": {
                name: "Langbogen",
                type: "weapon",
                slot: "two_hand",
                attacks: {
                    light: { damage: 12, stamina: 8, cooldown: 500, anim: "bow_quick", range: 50 },
                    heavy: { damage: 45, stamina: 25, cooldown: 1500, anim: "bow_aimed", range: 100 }
                }
            },
            
            // ZAUBER (werden wie Waffen ausgerüstet)
            "spell_fireball": {
                name: "Feuerball",
                type: "spell",
                slot: "one_hand",
                element: "fire",
                attacks: {
                    light: { damage: 20, mana: 15, cooldown: 600, anim: "cast_fire", projectile: true },
                    heavy: { damage: 60, mana: 40, cooldown: 1500, anim: "cast_inferno", aoe: true }
                }
            },
            "spell_ice": {
                name: "Eiszauber",
                type: "spell",
                slot: "one_hand",
                element: "ice",
                attacks: {
                    light: { damage: 18, mana: 12, cooldown: 500, anim: "cast_ice", effect: "slow" },
                    heavy: { damage: 55, mana: 35, cooldown: 1400, anim: "cast_blizzard", effect: "freeze" }
                }
            },
            "spell_lightning": {
                name: "Blitzzauber",
                type: "spell",
                slot: "one_hand",
                element: "lightning",
                attacks: {
                    light: { damage: 22, mana: 18, cooldown: 400, anim: "cast_spark", effect: "stun_chance" },
                    heavy: { damage: 65, mana: 45, cooldown: 1200, anim: "cast_thunder", effect: "chain" }
                }
            },
            "spell_heal": {
                name: "Heilzauber",
                type: "spell",
                slot: "one_hand",
                element: "holy",
                attacks: {
                    light: { heal: 20, mana: 20, cooldown: 1000, anim: "cast_heal" },
                    heavy: { heal: 60, mana: 50, cooldown: 3000, anim: "cast_heal_major" }
                }
            },
            "spell_explosion": {
                name: "EXPLOSION!!!",
                type: "spell",
                slot: "two_hand",
                element: "chaos",
                attacks: {
                    light: { damage: 30, mana: 25, cooldown: 800, anim: "cast_explosion_small" },
                    heavy: { damage: 200, mana: 100, cooldown: 10000, anim: "cast_EXPLOSION", 
                             exhaustion: 5000, najika_line: "EXPROOOOSION!!! *kollabiert*" }
                }
            },
            
            // SCHILDE
            "iron_shield": {
                name: "Eisenschild",
                type: "shield",
                slot: "one_hand",
                attacks: {
                    light: { damage: 8, stamina: 5, cooldown: 300, anim: "shield_bash" },
                    heavy: { block: true, stamina_drain: 15, parry_window: 150, anim: "shield_block" }
                }
            },
            
            // FAUST (wenn nichts ausgerüstet)
            "fist": {
                name: "Faust",
                type: "unarmed",
                slot: "one_hand",
                attacks: {
                    light: { damage: 5, stamina: 3, cooldown: 200, anim: "punch" },
                    heavy: { damage: 15, stamina: 10, cooldown: 500, anim: "uppercut" }
                }
            }
        };
    }
    
    // Equipment anlegen
    equip(itemId, slot) {
        const item = this.equipmentDB[itemId];
        if (!item) return { success: false, error: "Item nicht gefunden" };
        
        if (item.slot === "two_hand") {
            // Zweihändig: Belegt beide Slots
            this.leftHand = item;
            this.rightHand = item;
            this.isTwoHanded = true;
            return { success: true, message: `${item.name} in beiden Händen ausgerüstet` };
        }
        
        if (slot === "left") {
            this.leftHand = item;
        } else {
            this.rightHand = item;
        }
        this.isTwoHanded = false;
        
        return { success: true, message: `${item.name} in ${slot === 'left' ? 'linker' : 'rechter'} Hand` };
    }
    
    // Equipment ablegen
    unequip(slot) {
        if (slot === "left" || this.isTwoHanded) {
            this.leftHand = null;
        }
        if (slot === "right" || this.isTwoHanded) {
            this.rightHand = null;
        }
        this.isTwoHanded = false;
    }
    
    // Angriff ausführen
    attack(hand, attackType) {
        const now = Date.now();
        const equipment = hand === "left" ? this.leftHand : this.rightHand;
        const item = equipment || this.equipmentDB["fist"];
        const attack = item.attacks[attackType];
        
        if (!attack) return { success: false, error: "Angriff nicht verfügbar" };
        
        // Cooldown Check
        if (now - this.lastAttackTime[hand] < attack.cooldown) {
            return { success: false, error: "Noch auf Cooldown" };
        }
        
        // Stamina/Mana Check
        if (attack.stamina && this.stamina < attack.stamina) {
            return { success: false, error: "Nicht genug Stamina" };
        }
        if (attack.mana && window.playerState?.mana < attack.mana) {
            return { success: false, error: "Nicht genug Mana" };
        }
        
        // Kosten abziehen
        if (attack.stamina) this.stamina -= attack.stamina;
        if (attack.mana && window.playerState) window.playerState.mana -= attack.mana;
        
        // Cooldown setzen
        this.lastAttackTime[hand] = now;
        
        // Combo tracking
        if (now - this.lastComboTime < 1500) {
            this.comboCount++;
        } else {
            this.comboCount = 1;
        }
        this.lastComboTime = now;
        
        // Ergebnis
        const result = {
            success: true,
            item: item.name,
            attackType: attackType,
            damage: attack.damage || 0,
            heal: attack.heal || 0,
            effect: attack.effect || null,
            anim: attack.anim,
            combo: this.comboCount,
            comboBonus: this.comboCount > 1 ? (this.comboCount - 1) * 0.1 : 0, // +10% pro Combo
            isTwoHanded: this.isTwoHanded,
            exhaustion: attack.exhaustion || 0,
            najikaLine: attack.najika_line || null
        };
        
        // Zweihändig = stärker, aber beide Hände auf Cooldown
        if (this.isTwoHanded) {
            this.lastAttackTime["left"] = now;
            this.lastAttackTime["right"] = now;
        }
        
        return result;
    }
    
    // Weave: Beide Hände gleichzeitig (wenn unterschiedliche Elemente)
    weave() {
        if (this.isTwoHanded) {
            return { success: false, error: "Weave nicht möglich mit Zweihänder" };
        }
        
        const leftItem = this.leftHand;
        const rightItem = this.rightHand;
        
        if (!leftItem?.element || !rightItem?.element) {
            return { success: false, error: "Beide Hände brauchen Elementar-Zauber" };
        }
        
        if (leftItem.element === rightItem.element) {
            return { success: false, error: "Verschiedene Elemente benötigt" };
        }
        
        // Weave Combos
        const combo = [leftItem.element, rightItem.element].sort().join("+");
        const weaves = {
            "fire+ice": { name: "Thermoschock", damage: 80, effect: "stun" },
            "fire+lightning": { name: "Plasmasturm", damage: 100, effect: "burn_chain" },
            "ice+lightning": { name: "Frostblitz", damage: 90, effect: "freeze_stun" },
            "fire+holy": { name: "Heiliges Feuer", damage: 70, heal: 30 },
            "chaos+fire": { name: "MEGA EXPLOSION", damage: 150, effect: "devastation" }
        };
        
        const result = weaves[combo] || { name: "Elementar-Fusion", damage: 60, effect: "mixed" };
        
        // Mana kosten für beide
        const manaCost = 50;
        if (window.playerState?.mana < manaCost) {
            return { success: false, error: "Nicht genug Mana für Weave" };
        }
        window.playerState.mana -= manaCost;
        
        return {
            success: true,
            weave: result,
            elements: [leftItem.element, rightItem.element]
        };
    }
    
    // Stamina regenerieren
    regenStamina() {
        if (this.stamina < this.maxStamina) {
            this.stamina = Math.min(this.maxStamina, this.stamina + this.staminaRegen / 10);
        }
    }
    
    // Parry (mit Schild)
    parry() {
        const shield = this.leftHand?.type === "shield" ? this.leftHand : 
                       this.rightHand?.type === "shield" ? this.rightHand : null;
        
        if (!shield) {
            return { success: false, error: "Kein Schild ausgerüstet" };
        }
        
        return {
            success: true,
            parryWindow: shield.attacks.heavy.parry_window,
            staminaDrain: shield.attacks.heavy.stamina_drain
        };
    }
    
    // Status für UI
    getStatus() {
        return {
            leftHand: this.leftHand?.name || "Leer",
            rightHand: this.rightHand?.name || "Leer",
            isTwoHanded: this.isTwoHanded,
            stamina: Math.round(this.stamina),
            maxStamina: this.maxStamina,
            comboCount: this.comboCount
        };
    }
}

// Global Instance
window.equipmentCombat = new EquipmentCombatSystem();
```

## 1.3 Touch Controls für Equipment Combat (Mobile)

Erstelle/Erweitere `C:\Najika_World\digivice\js\touch_combat.js`:

```javascript
// =============================================================================
// TOUCH COMBAT - Mobile Controls für Equipment-basiertes System
// =============================================================================

class TouchCombatUI {
    constructor() {
        this.ec = window.equipmentCombat;
        this.createUI();
        this.bindEvents();
    }
    
    createUI() {
        const html = `
        <div id="touch-combat-ui">
            <!-- Equipment Display -->
            <div id="equipment-display">
                <div id="left-hand-display" class="hand-slot" data-hand="left">
                    <span class="hand-label">L</span>
                    <span class="item-name">Leer</span>
                </div>
                <div id="right-hand-display" class="hand-slot" data-hand="right">
                    <span class="hand-label">R</span>
                    <span class="item-name">Leer</span>
                </div>
            </div>
            
            <!-- Attack Buttons -->
            <div id="attack-buttons">
                <!-- Linke Hand -->
                <div class="attack-group left">
                    <button id="btn-left-light" class="attack-btn light">
                        <span class="icon">⚔️</span>
                        <span class="label">Light</span>
                    </button>
                    <button id="btn-left-heavy" class="attack-btn heavy">
                        <span class="icon">💥</span>
                        <span class="label">Heavy</span>
                    </button>
                </div>
                
                <!-- Rechte Hand -->
                <div class="attack-group right">
                    <button id="btn-right-light" class="attack-btn light">
                        <span class="icon">⚔️</span>
                        <span class="label">Light</span>
                    </button>
                    <button id="btn-right-heavy" class="attack-btn heavy">
                        <span class="icon">💥</span>
                        <span class="label">Heavy</span>
                    </button>
                </div>
            </div>
            
            <!-- Utility Buttons -->
            <div id="utility-buttons">
                <button id="btn-dodge" class="util-btn">💨 Dodge</button>
                <button id="btn-weave" class="util-btn weave">✨ Weave</button>
                <button id="btn-parry" class="util-btn">🛡️ Parry</button>
            </div>
            
            <!-- Stamina Bar -->
            <div id="stamina-bar">
                <div id="stamina-fill"></div>
                <span id="stamina-text">100/100</span>
            </div>
            
            <!-- Combo Display -->
            <div id="combo-display" class="hidden">
                <span id="combo-count">0</span>
                <span>COMBO!</span>
            </div>
        </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', html);
        this.injectCSS();
    }
    
    bindEvents() {
        // Left Hand Attacks
        document.getElementById('btn-left-light').addEventListener('touchstart', (e) => {
            e.preventDefault();
            this.doAttack('left', 'light');
        });
        document.getElementById('btn-left-heavy').addEventListener('touchstart', (e) => {
            e.preventDefault();
            this.doAttack('left', 'heavy');
        });
        
        // Right Hand Attacks
        document.getElementById('btn-right-light').addEventListener('touchstart', (e) => {
            e.preventDefault();
            this.doAttack('right', 'light');
        });
        document.getElementById('btn-right-heavy').addEventListener('touchstart', (e) => {
            e.preventDefault();
            this.doAttack('right', 'heavy');
        });
        
        // Utility
        document.getElementById('btn-weave').addEventListener('touchstart', (e) => {
            e.preventDefault();
            this.doWeave();
        });
        document.getElementById('btn-parry').addEventListener('touchstart', (e) => {
            e.preventDefault();
            this.doParry();
        });
        document.getElementById('btn-dodge').addEventListener('touchstart', (e) => {
            e.preventDefault();
            this.doDodge();
        });
        
        // Equipment Swap (Long Press on Hand Slot)
        ['left', 'right'].forEach(hand => {
            const el = document.getElementById(`${hand}-hand-display`);
            let timer;
            el.addEventListener('touchstart', () => {
                timer = setTimeout(() => this.openEquipmentMenu(hand), 500);
            });
            el.addEventListener('touchend', () => clearTimeout(timer));
        });
        
        // Update Loop
        setInterval(() => this.updateUI(), 100);
    }
    
    doAttack(hand, type) {
        const result = this.ec.attack(hand, type);
        
        if (result.success) {
            this.showDamage(result.damage || result.heal, result.heal ? 'heal' : 'damage');
            this.showCombo(result.combo);
            this.vibrate(type === 'heavy' ? 100 : 30);
            
            // Najika Special Line (für EXPLOSION etc.)
            if (result.najikaLine) {
                this.showNajikaLine(result.najikaLine);
            }
            
            // Exhaustion (nach EXPLOSION)
            if (result.exhaustion > 0) {
                this.showExhaustion(result.exhaustion);
            }
        } else {
            this.showError(result.error);
        }
    }
    
    doWeave() {
        const result = this.ec.weave();
        
        if (result.success) {
            this.showWeaveEffect(result.weave);
            this.vibrate(200);
        } else {
            this.showError(result.error);
        }
    }
    
    doParry() {
        const result = this.ec.parry();
        
        if (result.success) {
            this.showParryWindow(result.parryWindow);
            this.vibrate(50);
        } else {
            this.showError(result.error);
        }
    }
    
    doDodge() {
        // Dodge mit i-Frames
        this.vibrate(20);
        this.showDodge();
    }
    
    openEquipmentMenu(hand) {
        // Equipment Selection Popup
        const items = Object.entries(this.ec.equipmentDB);
        const menu = document.createElement('div');
        menu.id = 'equipment-menu';
        menu.innerHTML = `
            <div class="menu-content">
                <h3>${hand === 'left' ? 'Linke' : 'Rechte'} Hand</h3>
                ${items.map(([id, item]) => `
                    <button class="equip-item" data-id="${id}">
                        ${item.name} (${item.type})
                    </button>
                `).join('')}
                <button class="equip-item unequip">❌ Ablegen</button>
                <button class="close-menu">Schließen</button>
            </div>
        `;
        document.body.appendChild(menu);
        
        menu.querySelectorAll('.equip-item').forEach(btn => {
            btn.addEventListener('click', () => {
                const id = btn.dataset.id;
                if (id) {
                    this.ec.equip(id, hand);
                } else {
                    this.ec.unequip(hand);
                }
                menu.remove();
                this.updateUI();
            });
        });
        
        menu.querySelector('.close-menu').addEventListener('click', () => menu.remove());
    }
    
    updateUI() {
        const status = this.ec.getStatus();
        
        // Equipment Display
        document.querySelector('#left-hand-display .item-name').textContent = status.leftHand;
        document.querySelector('#right-hand-display .item-name').textContent = status.rightHand;
        
        // Stamina Bar
        document.getElementById('stamina-fill').style.width = `${(status.stamina / status.maxStamina) * 100}%`;
        document.getElementById('stamina-text').textContent = `${status.stamina}/${status.maxStamina}`;
        
        // Two-Handed Mode: Verstecke eine Seite
        if (status.isTwoHanded) {
            document.querySelector('.attack-group.left').classList.add('hidden');
            document.querySelector('.attack-group.right').classList.add('two-handed');
        } else {
            document.querySelector('.attack-group.left').classList.remove('hidden');
            document.querySelector('.attack-group.right').classList.remove('two-handed');
        }
    }
    
    showDamage(value, type) {
        const el = document.createElement('div');
        el.className = `floating-number ${type}`;
        el.textContent = type === 'heal' ? `+${value}` : value;
        el.style.left = `${50 + (Math.random() - 0.5) * 30}%`;
        document.body.appendChild(el);
        setTimeout(() => el.remove(), 1000);
    }
    
    showCombo(count) {
        if (count > 1) {
            const display = document.getElementById('combo-display');
            document.getElementById('combo-count').textContent = count;
            display.classList.remove('hidden');
            setTimeout(() => display.classList.add('hidden'), 1500);
        }
    }
    
    showWeaveEffect(weave) {
        const el = document.createElement('div');
        el.className = 'weave-effect';
        el.innerHTML = `<span>${weave.name}</span><span>${weave.damage} DMG</span>`;
        document.body.appendChild(el);
        setTimeout(() => el.remove(), 2000);
    }
    
    showNajikaLine(line) {
        const el = document.createElement('div');
        el.className = 'najika-combat-line';
        el.textContent = line;
        document.body.appendChild(el);
        setTimeout(() => el.remove(), 3000);
    }
    
    showExhaustion(duration) {
        document.getElementById('touch-combat-ui').classList.add('exhausted');
        setTimeout(() => {
            document.getElementById('touch-combat-ui').classList.remove('exhausted');
        }, duration);
    }
    
    showError(msg) {
        console.log('[Combat] Error:', msg);
    }
    
    vibrate(ms) {
        if (navigator.vibrate) navigator.vibrate(ms);
    }
    
    injectCSS() {
        const css = `
        #touch-combat-ui {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            padding: 10px;
            pointer-events: none;
            z-index: 5000;
        }
        
        #touch-combat-ui.exhausted {
            opacity: 0.3;
            pointer-events: none !important;
        }
        
        #equipment-display {
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
            pointer-events: auto;
        }
        
        .hand-slot {
            background: rgba(0,0,0,0.7);
            border: 2px solid #4CAF50;
            border-radius: 10px;
            padding: 8px 15px;
            color: white;
            display: flex;
            gap: 10px;
            align-items: center;
        }
        
        .hand-label {
            background: #4CAF50;
            padding: 2px 8px;
            border-radius: 5px;
            font-weight: bold;
        }
        
        #attack-buttons {
            display: flex;
            justify-content: space-between;
            pointer-events: auto;
        }
        
        .attack-group {
            display: flex;
            gap: 10px;
        }
        
        .attack-group.hidden { display: none; }
        .attack-group.two-handed .attack-btn { width: 80px; height: 80px; }
        
        .attack-btn {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            border: 3px solid #4CAF50;
            background: rgba(0,0,0,0.8);
            color: white;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        
        .attack-btn.heavy { border-color: #FF4444; }
        .attack-btn .icon { font-size: 24px; }
        .attack-btn .label { font-size: 10px; }
        
        #utility-buttons {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-top: 10px;
            pointer-events: auto;
        }
        
        .util-btn {
            padding: 10px 20px;
            border-radius: 20px;
            border: 2px solid #4CAF50;
            background: rgba(0,0,0,0.8);
            color: white;
        }
        
        .util-btn.weave {
            background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
            border: none;
        }
        
        #stamina-bar {
            position: absolute;
            bottom: 180px;
            left: 50%;
            transform: translateX(-50%);
            width: 150px;
            height: 20px;
            background: #333;
            border-radius: 10px;
            overflow: hidden;
        }
        
        #stamina-fill {
            height: 100%;
            background: #4CAF50;
            transition: width 0.1s;
        }
        
        #stamina-text {
            position: absolute;
            width: 100%;
            text-align: center;
            color: white;
            font-size: 12px;
            line-height: 20px;
        }
        
        #combo-display {
            position: fixed;
            top: 40%;
            left: 50%;
            transform: translateX(-50%);
            background: linear-gradient(90deg, #FFD700, #FFA500);
            padding: 10px 30px;
            border-radius: 10px;
            font-size: 24px;
            font-weight: bold;
            animation: comboPop 0.3s;
        }
        
        #combo-display.hidden { display: none; }
        
        .floating-number {
            position: fixed;
            top: 40%;
            font-size: 32px;
            font-weight: bold;
            animation: floatUp 1s forwards;
            pointer-events: none;
        }
        
        .floating-number.damage { color: #FF4444; }
        .floating-number.heal { color: #4CAF50; }
        
        .weave-effect {
            position: fixed;
            top: 30%;
            left: 50%;
            transform: translateX(-50%);
            background: linear-gradient(135deg, #FF6B6B, #4ECDC4);
            padding: 20px 40px;
            border-radius: 15px;
            text-align: center;
            animation: weaveFlash 2s forwards;
        }
        
        .najika-combat-line {
            position: fixed;
            top: 20%;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(255, 215, 0, 0.9);
            color: #000;
            padding: 15px 30px;
            border-radius: 10px;
            font-style: italic;
            font-size: 18px;
            animation: slideDown 3s forwards;
        }
        
        #equipment-menu {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0,0,0,0.9);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 9999;
        }
        
        .menu-content {
            background: #1a1a2e;
            padding: 20px;
            border-radius: 15px;
            max-width: 300px;
            width: 90%;
        }
        
        .equip-item {
            display: block;
            width: 100%;
            padding: 12px;
            margin: 5px 0;
            border: 2px solid #4CAF50;
            background: transparent;
            color: white;
            border-radius: 8px;
        }
        
        .equip-item.unequip { border-color: #FF4444; }
        .close-menu { background: #4CAF50; border: none; margin-top: 15px; }
        
        @keyframes floatUp {
            0% { opacity: 1; transform: translateY(0); }
            100% { opacity: 0; transform: translateY(-80px); }
        }
        
        @keyframes comboPop {
            0% { transform: translateX(-50%) scale(0.5); }
            50% { transform: translateX(-50%) scale(1.2); }
            100% { transform: translateX(-50%) scale(1); }
        }
        
        @keyframes slideDown {
            0% { opacity: 0; transform: translateX(-50%) translateY(-20px); }
            20% { opacity: 1; transform: translateX(-50%) translateY(0); }
            80% { opacity: 1; }
            100% { opacity: 0; }
        }
        `;
        
        const style = document.createElement('style');
        style.textContent = css;
        document.head.appendChild(style);
    }
}

// Init wenn Touch-Device
if ('ontouchstart' in window) {
    document.addEventListener('DOMContentLoaded', () => {
        window.touchCombatUI = new TouchCombatUI();
    });
}
```

---

# BLOCK 2: CHAOS EVENT SYSTEM (Konosuba x Oregon Trail)

## 2.1 Backend: ChaosEngine in `najika_server.py`

Füge die komplette ChaosEngine Klasse hinzu (siehe vorherige Anweisung).
**30 Events, 4 Kategorien, Najika-Reaktionen, Chaos-Level 0-10**

## 2.2 Frontend: `chaos_event_ui.js` + `chaos_events.css`

(Siehe vorherige Anweisung - KOMPLETT ÜBERNEHMEN)

---

# BLOCK 3: PC ORCHESTRATOR & HACKER-MODUS

## 3.1 Das Konzept

Najika kann deinen PC steuern über natürliche Sprache:
- "Öffne Chrome" → Startet Chrome
- "Wie viel RAM verbrauche ich?" → Zeigt Systeminfo
- "Erstelle einen Ordner auf dem Desktop" → Führt aus

## 3.2 Neue Datei: `C:\Najika_World\backend\najika_pc_orchestrator.py`

```python
# =============================================================================
# NAJIKA PC ORCHESTRATOR - Steuert Windows über natürliche Sprache
# =============================================================================

import os
import subprocess
import psutil
import json
import platform
from datetime import datetime

class NajikaPCOrchestrator:
    def __init__(self):
        self.enabled = True
        self.safe_mode = True  # Nur sichere Befehle
        self.command_history = []
        self.allowed_apps = [
            "chrome", "firefox", "edge", "notepad", "explorer",
            "calc", "cmd", "powershell", "code", "spotify"
        ]
    
    def parse_natural_language(self, text):
        """Wandelt natürliche Sprache in Befehle um"""
        text_lower = text.lower()
        
        # App starten
        for app in self.allowed_apps:
            if f"öffne {app}" in text_lower or f"starte {app}" in text_lower:
                return {"action": "open_app", "app": app}
        
        # System Info
        if any(x in text_lower for x in ["ram", "speicher", "memory"]):
            return {"action": "system_info", "type": "memory"}
        if any(x in text_lower for x in ["cpu", "prozessor"]):
            return {"action": "system_info", "type": "cpu"}
        if any(x in text_lower for x in ["festplatte", "disk", "speicherplatz"]):
            return {"action": "system_info", "type": "disk"}
        
        # Datei-Operationen
        if "erstelle ordner" in text_lower or "neuer ordner" in text_lower:
            # Extrahiere Ordnername
            name = text_lower.split("ordner")[-1].strip().replace('"', '').replace("'", "")
            if not name:
                name = "Neuer_Ordner"
            return {"action": "create_folder", "name": name}
        
        if "desktop" in text_lower and "öffne" in text_lower:
            return {"action": "open_folder", "path": "desktop"}
        
        # Screenshot
        if "screenshot" in text_lower:
            return {"action": "screenshot"}
        
        # Herunterfahren (nur mit Bestätigung!)
        if "herunterfahren" in text_lower or "shutdown" in text_lower:
            return {"action": "shutdown_request"}
        
        return {"action": "unknown", "text": text}
    
    def execute(self, command):
        """Führt geparsten Befehl aus"""
        action = command.get("action")
        result = {"success": False, "message": "", "data": None}
        
        try:
            if action == "open_app":
                result = self._open_app(command["app"])
            
            elif action == "system_info":
                result = self._get_system_info(command["type"])
            
            elif action == "create_folder":
                result = self._create_folder(command["name"])
            
            elif action == "open_folder":
                result = self._open_folder(command["path"])
            
            elif action == "screenshot":
                result = self._take_screenshot()
            
            elif action == "shutdown_request":
                result = {
                    "success": True,
                    "message": "⚠️ Herunterfahren angefragt! Bestätige mit 'shutdown confirm'",
                    "requires_confirm": True
                }
            
            elif action == "unknown":
                result = {
                    "success": False,
                    "message": f"Konnte Befehl nicht verstehen: {command.get('text', '')}"
                }
            
            # Log
            self.command_history.append({
                "time": datetime.now().isoformat(),
                "command": command,
                "result": result
            })
            
        except Exception as e:
            result = {"success": False, "message": f"Fehler: {str(e)}"}
        
        return result
    
    def _open_app(self, app):
        """Startet eine Anwendung"""
        app_paths = {
            "chrome": "chrome",
            "firefox": "firefox",
            "edge": "msedge",
            "notepad": "notepad",
            "explorer": "explorer",
            "calc": "calc",
            "cmd": "cmd",
            "powershell": "powershell",
            "code": "code",
            "spotify": "spotify"
        }
        
        if app not in app_paths:
            return {"success": False, "message": f"App '{app}' nicht erlaubt"}
        
        try:
            subprocess.Popen(app_paths[app], shell=True)
            return {"success": True, "message": f"✅ {app} gestartet!"}
        except Exception as e:
            return {"success": False, "message": f"Konnte {app} nicht starten: {e}"}
    
    def _get_system_info(self, info_type):
        """Holt System-Informationen"""
        if info_type == "memory":
            mem = psutil.virtual_memory()
            return {
                "success": True,
                "message": f"💾 RAM: {mem.percent}% verwendet ({mem.used // (1024**3)}GB / {mem.total // (1024**3)}GB)",
                "data": {
                    "percent": mem.percent,
                    "used_gb": mem.used // (1024**3),
                    "total_gb": mem.total // (1024**3)
                }
            }
        
        elif info_type == "cpu":
            cpu_percent = psutil.cpu_percent(interval=1)
            return {
                "success": True,
                "message": f"🖥️ CPU: {cpu_percent}% Auslastung",
                "data": {"percent": cpu_percent}
            }
        
        elif info_type == "disk":
            disk = psutil.disk_usage('/')
            return {
                "success": True,
                "message": f"💿 Festplatte: {disk.percent}% verwendet ({disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB)",
                "data": {
                    "percent": disk.percent,
                    "used_gb": disk.used // (1024**3),
                    "total_gb": disk.total // (1024**3)
                }
            }
        
        return {"success": False, "message": "Unbekannter Info-Typ"}
    
    def _create_folder(self, name):
        """Erstellt einen Ordner auf dem Desktop"""
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        folder_path = os.path.join(desktop, name)
        
        try:
            os.makedirs(folder_path, exist_ok=True)
            return {"success": True, "message": f"📁 Ordner '{name}' auf Desktop erstellt!"}
        except Exception as e:
            return {"success": False, "message": f"Fehler: {e}"}
    
    def _open_folder(self, path):
        """Öffnet einen Ordner"""
        if path == "desktop":
            folder = os.path.join(os.path.expanduser("~"), "Desktop")
        else:
            folder = path
        
        try:
            os.startfile(folder)
            return {"success": True, "message": f"📂 Ordner geöffnet!"}
        except Exception as e:
            return {"success": False, "message": f"Fehler: {e}"}
    
    def _take_screenshot(self):
        """Macht einen Screenshot"""
        try:
            import pyautogui
            screenshot = pyautogui.screenshot()
            path = os.path.join(os.path.expanduser("~"), "Desktop", f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            screenshot.save(path)
            return {"success": True, "message": f"📸 Screenshot gespeichert: {path}"}
        except ImportError:
            return {"success": False, "message": "pyautogui nicht installiert. Führe aus: pip install pyautogui"}
        except Exception as e:
            return {"success": False, "message": f"Fehler: {e}"}
    
    def get_history(self, limit=10):
        """Gibt Befehlsverlauf zurück"""
        return self.command_history[-limit:]

# Singleton
PC_ORCHESTRATOR = NajikaPCOrchestrator()
```

## 3.3 API Endpoints für PC Orchestrator

In `najika_server.py` hinzufügen:

```python
from najika_pc_orchestrator import PC_ORCHESTRATOR

@app.route('/api/pc/command', methods=['POST'])
def pc_command():
    data = request.json
    text = data.get('text', '')
    
    # Parse natural language
    command = PC_ORCHESTRATOR.parse_natural_language(text)
    
    # Execute
    result = PC_ORCHESTRATOR.execute(command)
    
    # Najika Reaktion
    if result['success']:
        najika_response = f"*tippt auf Tastatur* Erledigt, Mr.K! {result['message']}"
    else:
        najika_response = f"*kratzt sich am Kopf* Hmm... {result['message']}"
    
    return jsonify({
        "ok": result['success'],
        "result": result,
        "najika": najika_response
    })

@app.route('/api/pc/history', methods=['GET'])
def pc_history():
    return jsonify({
        "ok": True,
        "history": PC_ORCHESTRATOR.get_history()
    })

@app.route('/api/pc/status', methods=['GET'])
def pc_status():
    return jsonify({
        "ok": True,
        "enabled": PC_ORCHESTRATOR.enabled,
        "safe_mode": PC_ORCHESTRATOR.safe_mode,
        "platform": platform.system(),
        "python_version": platform.python_version()
    })
```

## 3.4 Terminal Raum UI für Hacker-Modus

Erweitere `terminal_modules.js` um PC-Befehle:

```javascript
// Im Terminal Raum: Hacker-Modus aktivieren
async function executeHackerCommand(input) {
    const response = await fetch('/api/pc/command', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ text: input })
    });
    
    const data = await response.json();
    
    // Zeige Najika's Reaktion
    addTerminalOutput(`> ${input}`);
    addTerminalOutput(`[NAJIKA] ${data.najika}`);
    
    if (data.result.data) {
        addTerminalOutput(`[DATA] ${JSON.stringify(data.result.data, null, 2)}`);
    }
}
```

---

# BLOCK 4: ALLE SCRIPT-TAGS IN INDEX.HTML

Füge diese Script-Tags VOR `</body>` ein:

```html
<!-- ============================================ -->
<!-- CORE SYSTEMS -->
<!-- ============================================ -->
<script src="js/command_system.js"></script>
<script src="js/equipment_combat.js"></script>
<script src="js/touch_combat.js"></script>

<!-- ============================================ -->
<!-- TERMINAL MODULES -->
<!-- ============================================ -->
<script src="js/terminal_modules.js"></script>
<script src="js/code_editor.js"></script>
<script src="js/secure_messenger.js"></script>
<script src="js/system_monitor.js"></script>
<script src="js/file_manager.js"></script>
<script src="js/voice_call.js"></script>

<!-- ============================================ -->
<!-- CHAOS EVENT SYSTEM -->
<!-- ============================================ -->
<script src="js/chaos_event_ui.js"></script>
<script src="js/oregon.js"></script>

<!-- ============================================ -->
<!-- WORLD SYSTEM -->
<!-- ============================================ -->
<script src="js/terrain_generator.js"></script>
<script src="js/biome_system.js"></script>
<script src="js/vegetation_system.js"></script>
<script src="js/region_streaming.js"></script>
<script src="js/lod_manager.js"></script>
<script src="js/asset_loader.js"></script>
<script src="js/dungeon_generator.js"></script>

<!-- ============================================ -->
<!-- BATTLE SYSTEM -->
<!-- ============================================ -->
<script src="js/battle_core.js"></script>
<script src="js/battle_api.js"></script>

<!-- ============================================ -->
<!-- INIT ALL -->
<!-- ============================================ -->
<script>
document.addEventListener('DOMContentLoaded', () => {
    console.log('[Najika] Initializing all systems...');
    
    // Equipment Combat
    if (typeof EquipmentCombatSystem !== 'undefined') {
        window.equipmentCombat = new EquipmentCombatSystem();
        console.log('[Najika] ✓ Equipment Combat System');
    }
    
    // Touch Combat (Mobile)
    if ('ontouchstart' in window && typeof TouchCombatUI !== 'undefined') {
        window.touchCombatUI = new TouchCombatUI();
        console.log('[Najika] ✓ Touch Combat UI');
    }
    
    // Chaos Events
    if (typeof ChaosEventUI !== 'undefined') {
        window.chaosEventUI = new ChaosEventUI();
        console.log('[Najika] ✓ Chaos Event System');
    }
    
    // Command System
    if (typeof CommandSystem !== 'undefined') {
        window.commandSystem = new CommandSystem();
        console.log('[Najika] ✓ Command System');
    }
    
    console.log('[Najika] ✅ All systems initialized!');
});
</script>
```

---

# BLOCK 5: CSS-LINKS IM HEAD

```html
<link rel="stylesheet" href="static/css/terminal_modules.css">
<link rel="stylesheet" href="static/css/code_editor.css">
<link rel="stylesheet" href="static/css/secure_messenger.css">
<link rel="stylesheet" href="static/css/system_monitor.css">
<link rel="stylesheet" href="static/css/file_manager.css">
<link rel="stylesheet" href="static/css/chaos_events.css">
<link rel="stylesheet" href="static/css/combat_ui.css">
```

---

# BLOCK 6: NAJIKA KI-INTEGRATION VERVOLLSTÄNDIGEN

## 6.1 Stelle sicher dass Ollama läuft

```bash
ollama list
# Sollte zeigen: najika-local (Qwen2.5-7B oder ähnlich)
```

## 6.2 Prüfe najika_server.py Imports

Am Anfang der Datei sollte stehen:
```python
from najika_enhanced_personality import generate_enhanced_persona
from najika_memory_enhanced import NajikaMemoryEnhanced
from najika_pc_orchestrator import PC_ORCHESTRATOR
```

## 6.3 Chat-Endpoint muss Personality nutzen

```python
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    # Get Personality Prompt
    persona = generate_enhanced_persona()
    
    # Get Memory Context
    memory_context = ""
    if NAJIKA_MEMORY:
        memories = NAJIKA_MEMORY.retrieve(user_message, top_k=3)
        if memories:
            memory_context = "\n".join([m['content'] for m in memories])
    
    # Build Full Prompt
    full_prompt = f"""{persona}

ERINNERUNGEN:
{memory_context}

User (Kuja): {user_message}

Najika:"""
    
    # Call AI
    response = call_ollama(full_prompt)
    
    # Store in Memory
    if NAJIKA_MEMORY:
        NAJIKA_MEMORY.store(user_message, response)
    
    return jsonify({
        "ok": True,
        "response": response,
        "personality": "megumin"  # oder dynamisch
    })
```

---

# BLOCK 7: MOBILE APK BUILD

## 7.1 PWA Manifest prüfen

`C:\Najika_World\digivice\manifest.json`:
```json
{
    "name": "Najika World",
    "short_name": "Najika",
    "start_url": "/",
    "display": "standalone",
    "orientation": "portrait",
    "background_color": "#1a1a2e",
    "theme_color": "#4CAF50",
    "icons": [
        {"src": "/icons/icon-192.png", "sizes": "192x192", "type": "image/png"},
        {"src": "/icons/icon-512.png", "sizes": "512x512", "type": "image/png"}
    ]
}
```

## 7.2 Service Worker

`C:\Najika_World\digivice\sw.js`:
```javascript
const CACHE_NAME = 'najika-v1';
const urlsToCache = [
    '/',
    '/index.html',
    '/js/equipment_combat.js',
    '/js/touch_combat.js',
    '/js/chaos_event_ui.js',
    '/static/css/chaos_events.css'
];

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(urlsToCache))
    );
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => response || fetch(event.request))
    );
});
```

## 7.3 APK Build (mit Capacitor oder PWA Builder)

```bash
# Option 1: PWABuilder.com
# Gehe zu https://pwabuilder.com
# URL eingeben: http://deine-ip:8000
# APK generieren lassen

# Option 2: Capacitor
npm install @capacitor/core @capacitor/cli
npx cap init Najika com.najika.world
npx cap add android
npx cap sync
# Dann in Android Studio öffnen und APK bauen
```

---

# ✅ CHECKLISTE NACH IMPLEMENTIERUNG

## Backend:
- [ ] Server startet ohne Fehler
- [ ] `/api/chaos/check_event` gibt JSON zurück
- [ ] `/api/pc/command` führt Befehle aus
- [ ] `/api/chat` nutzt Najika Personality

## Frontend:
- [ ] Browser zeigt keine JS-Fehler (F12)
- [ ] Chaos Meter erscheint rechts oben
- [ ] Equipment UI zeigt Waffen korrekt
- [ ] Light/Heavy Attacks funktionieren

## Mobile:
- [ ] Touch-Buttons erscheinen unten
- [ ] Equipment-Wechsel per Long-Press
- [ ] Weave-Button erscheint bei 2 Elementen
- [ ] Vibration funktioniert

---

# 📝 WICHTIGE HINWEISE

1. **Backup machen** bevor du startest!
2. **Nach Backend-Änderungen**: Server neu starten
3. **Nach Frontend-Änderungen**: Ctrl+F5 im Browser
4. **Bei Fehlern**: Console-Log prüfen (F12)
5. **Mobile testen**: Chrome DevTools → Toggle Device Toolbar

---

**VIEL ERFOLG!** 🚀

Diese Anweisung deckt ab:
- ✅ Equipment-basiertes Combat (NICHT separate Buttons pro Hand!)
- ✅ Chaos Event System (Konosuba x Oregon Trail)
- ✅ PC Orchestrator (Hacker-Modus)
- ✅ Najika KI-Integration
- ✅ Mobile Touch Controls
- ✅ APK Build
