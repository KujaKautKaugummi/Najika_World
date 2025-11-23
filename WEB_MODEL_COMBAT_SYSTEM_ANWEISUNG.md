# 🗡️ COMBAT SYSTEM - Vollständige Implementation Anweisung

**Datum:** 2025-11-19
**Priorität:** HOCH
**Status:** Bereit zur Umsetzung

---

## 📋 Übersicht

Dieses Dokument beschreibt die **vollständige Implementation** des Combat-Systems für Najika's World, basierend auf:
- ✅ Vorhandenem Code in `digivice/js/3d_scene.js` (COMBAT_SYSTEM Objekt)
- ✅ Spezifikationen aus `NAJIKA_PROJEKT_KOMPLETT_V3_MIT_UNSERER_KI.md`
- ✅ Beispiel aus `digivice/najika_world_9regions_test.html`

---

## 🎯 Ziel

Ein **Dual-Wield Combat System** mit:
1. **Light & Heavy Attacks** für jede Hand
2. **Maus-Integration** (LMB/RMB)
3. **Beide Hände gleichzeitig** (SPACE)
4. **Combo-System** mit Damage-Multiplikatoren
5. **Block/Parry/Dodge** Mechaniken
6. **Visual Feedback** (Damage Numbers, Effects)

---

## 📊 Aktueller Status

### ✅ **Bereits vorhanden** (digivice/js/3d_scene.js):

```javascript
// Zeile 70-210
const COMBAT_SYSTEM = {
    leftHand: null,
    rightHand: null,
    stamina: 100,
    health: 100,
    equipment: {
        leftHand: { type: 'wand', name: 'Najika Staff', damage: 25 },
        rightHand: { type: 'sword', name: 'Eisenschwert', damage: 35 },
        armor: { defense: 10 }
    },

    // Funktionen
    attackLeft() { ... },      // Zeile 119
    attackRight() { ... },     // Zeile 127
    parry() { ... },           // Zeile 135
    dodge() { ... },           // Zeile 144
    checkCombo() { ... },      // Zeile 158
    takeDamage(amount) { ... } // Zeile 184
}
```

**Tastenbelegung (aktuell):**
- **J** = Linke Hand
- **K** = Rechte Hand
- **Q** = Parry
- **Space** = Dodge Roll

**UI vorhanden:**
- Combat Stats Panel (HP/Stamina)
- Equipment Display
- Collapsible UI

### ❌ **Was fehlt:**

1. Light/Heavy Attack Unterscheidung
2. Maus-Integration (LMB/RMB)
3. Beide Hände gleichzeitig (SPACE)
4. Shift-Modifier für Heavy
5. Damage-Anwendung auf Gegner
6. Visual Effects (Particles, Animations)
7. Hitboxes/Targeting
8. Sound Effects

---

## 🔨 Implementation Plan

### **Phase 1: Light/Heavy Attack System**

#### 1.1 **Erweitere COMBAT_SYSTEM**

Füge zu `COMBAT_SYSTEM` hinzu (nach Zeile 116):

```javascript
// Light/Heavy Attack Stats
attackTypes: {
    light: {
        damageMultiplier: 0.7,
        staminaCost: 10,
        speed: 'fast',
        recoveryTime: 300  // ms
    },
    heavy: {
        damageMultiplier: 1.5,
        staminaCost: 25,
        speed: 'slow',
        recoveryTime: 800,  // ms
        canCancel: false
    }
},

// Attack State
currentAttack: null,
lastAttackTime: 0,
isAttacking: false,

// New Attack Functions
attackLeftLight() {
    if (!this.canAttack()) return false;
    const type = this.attackTypes.light;
    const baseDamage = this.equipment.leftHand.damage;
    const damage = Math.floor(baseDamage * type.damageMultiplier);

    this.executeAttack('left', 'light', damage, type);
    return true;
},

attackLeftHeavy() {
    if (!this.canAttack()) return false;
    const type = this.attackTypes.heavy;
    const baseDamage = this.equipment.leftHand.damage;
    const damage = Math.floor(baseDamage * type.damageMultiplier);

    this.executeAttack('left', 'heavy', damage, type);
    return true;
},

attackRightLight() {
    if (!this.canAttack()) return false;
    const type = this.attackTypes.light;
    const baseDamage = this.equipment.rightHand.damage;
    const damage = Math.floor(baseDamage * type.damageMultiplier);

    this.executeAttack('right', 'light', damage, type);
    return true;
},

attackRightHeavy() {
    if (!this.canAttack()) return false;
    const type = this.attackTypes.heavy;
    const baseDamage = this.equipment.rightHand.damage;
    const damage = Math.floor(baseDamage * type.damageMultiplier);

    this.executeAttack('right', 'heavy', damage, type);
    return true;
},

attackBothHands() {
    if (!this.canAttack()) return false;
    if (this.stamina < 35) return false;  // Beide Hände = teurer

    const leftDamage = Math.floor(this.equipment.leftHand.damage * 1.2);
    const rightDamage = Math.floor(this.equipment.rightHand.damage * 1.2);
    const totalDamage = leftDamage + rightDamage;

    this.stamina -= 35;
    this.comboBuffer += 'B';  // Both
    this.lastAttackTime = Date.now();
    this.isAttacking = true;

    this.applyDamageToTarget(totalDamage);

    if (typeof notify === 'function') {
        notify(`💥 DUAL STRIKE! ${totalDamage} DMG`, 'success');
    }

    setTimeout(() => { this.isAttacking = false; }, 600);
    return true;
},

canAttack() {
    const now = Date.now();
    const timeSinceLastAttack = now - this.lastAttackTime;

    if (this.isAttacking) return false;
    if (this.stamina < 10) return false;
    if (this.currentAttack && !this.currentAttack.canCancel) return false;

    return true;
},

executeAttack(hand, type, damage, attackData) {
    this.stamina -= attackData.staminaCost;
    this.comboBuffer += hand === 'left' ? 'L' : 'R';
    this.lastAttackTime = Date.now();
    this.isAttacking = true;
    this.currentAttack = { hand, type, damage, canCancel: attackData.canCancel !== false };

    this.applyDamageToTarget(damage);
    this.checkCombo();

    if (typeof notify === 'function') {
        const handIcon = hand === 'left' ? '🔮' : '⚔️';
        const typeText = type === 'heavy' ? 'HEAVY' : 'Light';
        notify(`${handIcon} ${typeText} Attack: ${damage} DMG`, 'info');
    }

    setTimeout(() => {
        this.isAttacking = false;
        this.currentAttack = null;
    }, attackData.recoveryTime);
},

applyDamageToTarget(damage) {
    // Integration mit Enemy System
    if (window.DungeonEnemies && typeof DungeonEnemies.damageNearestEnemy === 'function') {
        const actualDamage = DungeonEnemies.damageNearestEnemy(damage, characterGroup.position);
        if (actualDamage > 0) {
            console.log(`✅ Dealt ${actualDamage} damage to enemy!`);
        }
    } else {
        console.log(`⚔️ Attack: ${damage} damage (no target)`);
    }
}
```

#### 1.2 **Update Combo-System**

Erweitere `dualWieldCombos` (Zeile 102) um neue Combos:

```javascript
dualWieldCombos: {
    // Light Combos
    'LL': { damage: 20, stamina: 5, name: 'Schneller Doppelschlag', multiplier: 1.2 },
    'RR': { damage: 25, stamina: 8, name: 'Zweifach-Hieb', multiplier: 1.3 },
    'LR': { damage: 30, stamina: 15, name: 'Kreuz-Schlag', multiplier: 1.5 },

    // Heavy Combos
    'LHLH': { damage: 80, stamina: 50, name: 'Vernichtender Wirbel', multiplier: 2.0 },
    'RHRH': { damage: 90, stamina: 55, name: 'Todesschlag-Serie', multiplier: 2.2 },

    // Mixed Combos
    'LLR': { damage: 40, stamina: 25, name: 'Zauber-Schwertkette', multiplier: 1.6 },
    'RRL': { damage: 50, stamina: 25, name: 'Wirbel-Angriff', multiplier: 1.7 },
    'LRRL': { damage: 60, stamina: 30, name: 'Tödlicher Tanz', multiplier: 1.8 },

    // Both Hands Combos
    'BLR': { damage: 100, stamina: 60, name: 'Triple Strike Finale', multiplier: 2.5 },
    'BB': { damage: 120, stamina: 70, name: 'Dual Devastation', multiplier: 3.0 }
}
```

---

### **Phase 2: Maus-Integration**

#### 2.1 **Mouse Event Listeners**

Füge zu `installEventHandlers()` hinzu (nach Zeile 1510):

```javascript
window.addEventListener('mousedown', onMouseDown, false);
window.addEventListener('mouseup', onMouseUp, false);
```

#### 2.2 **Mouse Handler Funktionen**

Füge nach `onKeyUp()` ein (nach Zeile 1682):

```javascript
let mouseHoldTimer = null;
let isHoldingMouse = false;

function onMouseDown(event) {
    // Ignore if clicking on UI elements
    if (event.target.tagName === 'BUTTON' ||
        event.target.tagName === 'INPUT' ||
        event.target.closest('#combat-stats-ui') ||
        event.target.closest('.cloud-btn')) {
        return;
    }

    const isShiftPressed = event.shiftKey;

    // Left Mouse Button
    if (event.button === 0) {
        // Start hold timer for heavy attack
        mouseHoldTimer = setTimeout(() => {
            isHoldingMouse = true;
            if (COMBAT_SYSTEM.attackLeftHeavy()) {
                console.log('🔮 Linke Hand: HEAVY Zauber!');
            }
        }, 200);  // 200ms hold = heavy attack

        // If released before timer, it's a light attack
    }

    // Right Mouse Button
    if (event.button === 2) {
        event.preventDefault();  // Prevent context menu

        mouseHoldTimer = setTimeout(() => {
            isHoldingMouse = true;
            if (COMBAT_SYSTEM.attackRightHeavy()) {
                console.log('⚔️ Rechte Hand: HEAVY Schwert!');
            }
        }, 200);
    }
}

function onMouseUp(event) {
    const isShiftPressed = event.shiftKey;

    // Clear hold timer
    if (mouseHoldTimer) {
        clearTimeout(mouseHoldTimer);
        mouseHoldTimer = null;
    }

    // If not holding, execute light attack
    if (!isHoldingMouse) {
        if (event.button === 0) {
            if (COMBAT_SYSTEM.attackLeftLight()) {
                console.log('🔮 Linke Hand: Light Zauber!');
            }
        }

        if (event.button === 2) {
            if (COMBAT_SYSTEM.attackRightLight()) {
                console.log('⚔️ Rechte Hand: Light Schwert!');
            }
        }
    }

    isHoldingMouse = false;
}

// Disable context menu on canvas
document.addEventListener('contextmenu', (e) => {
    if (e.target.tagName === 'CANVAS') {
        e.preventDefault();
    }
});
```

---

### **Phase 3: Keyboard Updates**

#### 3.1 **Update onKeyDown()**

Ersetze die Combat-Tasten Section (Zeile 1627-1666) mit:

```javascript
// ⚔️ KAMPF-TASTEN

// Q = Linke Hand (Light/Heavy mit Shift)
if (event.code === 'KeyQ') {
    if (event.shiftKey) {
        if (COMBAT_SYSTEM.attackLeftHeavy()) {
            console.log('🔮 Linke Hand: HEAVY Zauber!');
        }
    } else {
        if (COMBAT_SYSTEM.attackLeftLight()) {
            console.log('🔮 Linke Hand: Light Zauber!');
        }
    }
}

// E = Rechte Hand (Light/Heavy mit Shift)
if (event.code === 'KeyE') {
    // Priorität: Interaktion vor Angriff
    if (currentInterior && currentInteractable) {
        handleInteraction();
        return;
    }
    if (nearBuilding && !currentInterior) {
        enterBuilding();
        return;
    }

    // Wenn keine Interaktion möglich, dann Angriff
    if (event.shiftKey) {
        if (COMBAT_SYSTEM.attackRightHeavy()) {
            console.log('⚔️ Rechte Hand: HEAVY Schwert!');
        }
    } else {
        if (COMBAT_SYSTEM.attackRightLight()) {
            console.log('⚔️ Rechte Hand: Light Schwert!');
        }
    }
}

// SPACE = Beide Hände gleichzeitig ODER Dodge
if (event.code === 'Space') {
    event.preventDefault();  // Prevent page scroll

    // Shift + Space = Dodge
    if (event.shiftKey) {
        if (COMBAT_SYSTEM.dodge()) {
            console.log('🌀 DODGE ROLL!');
            if (characterGroup) {
                const rollDistance = 15;
                const moveX = Math.sin(characterHeading) * rollDistance;
                const moveZ = Math.cos(characterHeading) * rollDistance;
                characterGroup.position.x += moveX;
                characterGroup.position.z += moveZ;
                clampCharacterToRoom(characterGroup.position);
            }
        }
    } else {
        // Normal Space = Both Hands Attack
        if (COMBAT_SYSTEM.attackBothHands()) {
            console.log('💥 BEIDE HÄNDE!');
        }
    }
}

// X = Block (Hold)
if (event.code === 'KeyX') {
    COMBAT_SYSTEM.isBlocking = true;
    console.log('🛡️ BLOCKING...');
}

// C = Parry
if (event.code === 'KeyC') {
    if (COMBAT_SYSTEM.parry()) {
        console.log('🛡️ PARRY bereit!');
    }
}

// V = Toggle Lock-On (später)
// if (event.code === 'KeyV') { ... }
```

#### 3.2 **Add onKeyUp Handler**

Erweitere `onKeyUp()` (Zeile 1680):

```javascript
function onKeyUp(event) {
    activeKeys.delete(event.code);

    // Release Block
    if (event.code === 'KeyX') {
        COMBAT_SYSTEM.isBlocking = false;
        console.log('🛡️ Block released');
    }
}
```

#### 3.3 **Add Blocking State**

Füge zu COMBAT_SYSTEM hinzu (nach Zeile 82):

```javascript
// Blocking
isBlocking: false,
blockDamageReduction: 0.5,  // 50%
```

#### 3.4 **Update takeDamage()**

Erweitere `takeDamage()` (Zeile 184):

```javascript
takeDamage(amount) {
    if (this.dodgeRoll.active) return 0;  // i-frames

    if (this.isParrying) {
        // Parry successful
        this.stamina = Math.min(this.maxStamina, this.stamina + 20);
        if (typeof notify === 'function') {
            notify('🛡️ PARRY!', 'success');
        }
        return 0;
    }

    if (this.isBlocking) {
        // Block reduces damage
        const blocked = Math.floor(amount * this.blockDamageReduction);
        const damage = amount - blocked;
        this.health = Math.max(0, this.health - damage);
        this.stamina = Math.max(0, this.stamina - 10);  // Stamina cost

        if (typeof notify === 'function') {
            notify(`🛡️ Blocked ${blocked} damage!`, 'info');
        }
        return damage;
    }

    const defense = this.equipment.armor.defense;
    const damage = Math.max(1, amount - defense);
    this.health = Math.max(0, this.health - damage);
    return damage;
}
```

---

### **Phase 4: Enemy Integration**

#### 4.1 **Add to DungeonEnemies** (digivice/js/dungeon_enemies.js)

Füge neue Funktion hinzu:

```javascript
damageNearestEnemy: function(damage, playerPos, maxDistance = 30) {
    if (!this.enemies || this.enemies.length === 0) return 0;

    let nearestEnemy = null;
    let minDist = Infinity;

    // Finde nächsten Gegner
    for (const enemy of this.enemies) {
        if (!enemy.isAlive || !enemy.mesh) continue;

        const dist = playerPos.distanceTo(enemy.mesh.position);
        if (dist < maxDistance && dist < minDist) {
            nearestEnemy = enemy;
            minDist = dist;
        }
    }

    if (!nearestEnemy) return 0;

    // Damage anwenden
    nearestEnemy.health -= damage;

    // Visual Feedback
    this.showDamageNumber(damage, nearestEnemy.mesh.position);

    // Check if dead
    if (nearestEnemy.health <= 0) {
        nearestEnemy.isAlive = false;
        this.onEnemyKilled(nearestEnemy);
    }

    return damage;
},

showDamageNumber: function(damage, position) {
    // Create floating damage text
    const div = document.createElement('div');
    div.textContent = `-${damage}`;
    div.style.cssText = `
        position: fixed;
        color: #ff3333;
        font-size: 32px;
        font-weight: bold;
        text-shadow: 2px 2px 4px #000;
        pointer-events: none;
        z-index: 9999;
        animation: floatUp 1s ease-out forwards;
    `;

    // Convert 3D position to screen position
    const vector = position.clone();
    vector.project(camera);

    const x = (vector.x * 0.5 + 0.5) * window.innerWidth;
    const y = (vector.y * -0.5 + 0.5) * window.innerHeight;

    div.style.left = x + 'px';
    div.style.top = y + 'px';

    document.body.appendChild(div);

    // Remove after animation
    setTimeout(() => div.remove(), 1000);
}
```

#### 4.2 **Add CSS Animation** (index.html)

Füge zu `<style>` hinzu:

```css
@keyframes floatUp {
    0% {
        opacity: 1;
        transform: translateY(0);
    }
    100% {
        opacity: 0;
        transform: translateY(-100px);
    }
}
```

---

### **Phase 5: Visual Effects**

#### 5.1 **Attack Particles**

Füge neue Funktion hinzu (nach updateCombatStatsUI):

```javascript
function createAttackEffect(position, hand, type) {
    if (!THREE) return;

    const color = hand === 'left' ? 0x00ffff : 0xff4444;  // Cyan für Zauber, Rot für Schwert
    const size = type === 'heavy' ? 3 : 1.5;

    const particleCount = type === 'heavy' ? 20 : 10;
    const geometry = new THREE.BufferGeometry();
    const positions = [];

    for (let i = 0; i < particleCount; i++) {
        const x = (Math.random() - 0.5) * size;
        const y = (Math.random() - 0.5) * size;
        const z = (Math.random() - 0.5) * size;
        positions.push(x, y, z);
    }

    geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));

    const material = new THREE.PointsMaterial({
        color: color,
        size: 0.3,
        transparent: true,
        opacity: 1.0,
        blending: THREE.AdditiveBlending
    });

    const particles = new THREE.Points(geometry, material);
    particles.position.copy(position);
    scene.add(particles);

    // Animate particles
    let frame = 0;
    const animate = () => {
        frame++;
        material.opacity = 1.0 - (frame / 30);
        particles.position.y += 0.2;

        if (frame < 30) {
            requestAnimationFrame(animate);
        } else {
            scene.remove(particles);
            geometry.dispose();
            material.dispose();
        }
    };
    animate();
}
```

#### 5.2 **Call from executeAttack()**

In `executeAttack()` hinzufügen:

```javascript
// Visual Effect
if (characterGroup && typeof createAttackEffect === 'function') {
    const effectPos = characterGroup.position.clone();
    effectPos.y += 2;
    const direction = new THREE.Vector3(
        Math.sin(characterHeading),
        0,
        Math.cos(characterHeading)
    );
    effectPos.add(direction.multiplyScalar(5));
    createAttackEffect(effectPos, hand, type);
}
```

---

### **Phase 6: Sound Effects**

#### 6.1 **Add Sound System**

Füge nach COMBAT_SYSTEM hinzu:

```javascript
// Combat Sound Effects
const COMBAT_SOUNDS = {
    lightAttack: new Audio('/digivice/sounds/light_attack.mp3'),
    heavyAttack: new Audio('/digivice/sounds/heavy_attack.mp3'),
    bothHands: new Audio('/digivice/sounds/dual_strike.mp3'),
    parry: new Audio('/digivice/sounds/parry.mp3'),
    dodge: new Audio('/digivice/sounds/dodge.mp3'),
    hit: new Audio('/digivice/sounds/hit.mp3'),
    block: new Audio('/digivice/sounds/block.mp3')
};

// Set volumes
Object.values(COMBAT_SOUNDS).forEach(sound => {
    sound.volume = 0.3;
});

function playSound(soundName) {
    if (COMBAT_SOUNDS[soundName]) {
        COMBAT_SOUNDS[soundName].currentTime = 0;
        COMBAT_SOUNDS[soundName].play().catch(e => console.warn('Sound play failed:', e));
    }
}
```

#### 6.2 **Call in Combat Functions**

In `executeAttack()`:
```javascript
playSound(type === 'heavy' ? 'heavyAttack' : 'lightAttack');
```

In `attackBothHands()`:
```javascript
playSound('bothHands');
```

In `parry()`:
```javascript
playSound('parry');
```

---

## 🧪 Testing Checklist

- [ ] Light Attack (Linke Hand): Q oder LMB (kurz)
- [ ] Heavy Attack (Linke Hand): Shift+Q oder LMB (lang)
- [ ] Light Attack (Rechte Hand): E oder RMB (kurz)
- [ ] Heavy Attack (Rechte Hand): Shift+E oder RMB (lang)
- [ ] Beide Hände: SPACE
- [ ] Dodge: Shift+SPACE
- [ ] Block: X (halten)
- [ ] Parry: C
- [ ] Combos: LL, RR, LR, BLR, etc.
- [ ] Stamina Verbrauch korrekt
- [ ] Damage Numbers erscheinen
- [ ] Enemy nimmt Schaden
- [ ] UI Updates (HP/Stamina)
- [ ] Visual Effects erscheinen
- [ ] Sounds abspielen
- [ ] Keine Errors in Console

---

## 📝 Implementation Reihenfolge

1. ✅ Phase 1: Light/Heavy System (COMBAT_SYSTEM erweitern)
2. ✅ Phase 2: Maus-Integration (Event Listeners)
3. ✅ Phase 3: Keyboard Updates (Q/E/SPACE)
4. ✅ Phase 4: Enemy Integration (Damage Application)
5. ✅ Phase 5: Visual Effects (Particles)
6. ⏳ Phase 6: Sound Effects (Optional)

**Geschätzte Zeit:** 4-6 Stunden

---

## 🎯 Nächste Schritte (nach Combat System)

1. **Inventory System** - Equipment wechseln
2. **Skills/Hotbar** - Zauber 1-9
3. **Loot System** - Items von Gegnern
4. **Quest System** - Aufgaben & Tracking
5. **NPC System** - Dialoge & Merchants

---

## 📚 Referenzen

### **Implementierte Code-Dateien:**
- **COMBAT_SYSTEM Code:** `digivice/js/3d_scene.js` Zeile 70-210
- **Enemy System:** `digivice/js/dungeon_enemies.js`
- **Dungeon Combat:** `digivice/js/dungeon_combat.js`
- **Dungeon Generator:** `digivice/js/dungeon_generator.js`
- **Beispiel (Test):** `digivice/najika_world_9regions_test.html` Zeile 1176-1180

### **Design-Spezifikationen:**
- **⭐ HAUPTDOKUMENT:** `alles wissen/Najika finale/05_COMBAT_SYSTEM.md`
  - Zeile 1-100: Orbit Cam + Anfeuern-System (Digimon World Style)
  - Zeile 202-250: Third/First Person Combat (Soulframe + Skyrim Hybrid)
  - Zeile 229-242: Vollständige Tastenbelegung
  - Zeile 254-299: Modus-Wechsel System (Phase 2)

- **Ergänzungen:** `alles wissen/.../NAJIKA_PROJEKT_KOMPLETT_V3_MIT_UNSERER_KI.md`
  - Zeile 1710-1790: Controller/Keyboard Layout
  - Zeile 1717-1718: Light/Heavy Attack Definition
  - Zeile 1747-1760: AttackSystem Python-Beispiel
  - Zeile 1762-1784: Block/Parry/Dodge Mechaniken

- **Installer Code:** `alles wissen/.../najika_installer_part3_frontend.ps1`
  - Zeile 157-162: lightAttack() / heavyAttack() Functions
  - Zeile 223-224: LMB = Light, RMB = Heavy
  - Zeile 300: Light/Heavy Attacks Feature-Liste

### **Wichtige Hinweise aus Dokumentation:**

**⚠️ NICHT Dark Souls-like!**
- ✅ **Soulframe** = Fluid, schnell, akrobatisch, großzügige i-Frames
- ❌ **Dark Souls** = Brutal, langsam, wenig Stamina, schwer

**3 Kamera-Modi geplant (Phase 1 = nur Third-Person Action):**
1. **Orbit Cam** - Najika kämpft, du feuerst an (Digimon World Style)
2. **Third-Person** - Du kämpfst (Soulframe + Skyrim)
3. **First-Person** - Du kämpfst (Optional)

---

**🤖 Generated for Web Model Implementation**
**Status: READY TO IMPLEMENT** ✅
