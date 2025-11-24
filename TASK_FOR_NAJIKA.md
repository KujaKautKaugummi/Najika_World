# AUFGABE FÜR NAJIKA (Lokales Modell)

## Ziel
Erstelle ein Python-Script `scale_najika_world_to_9600m.py`, das `digivice/najika_world_UNIFIED.html` von **133m auf 3200m pro Region** (9.6km Gesamt) skaliert.

## Input-Datei Struktur
```javascript
// Line 601: Region-Größe
const regionSize = 133.32;  // → ÄNDERN zu 3200

// Line 602-615: Region-Positionen
const regions = [
    { name: 'ice',      x: -133.32, z: 133.32,  y: 0 },   // → x: -3200, z: 3200
    { name: 'highland', x: 0,       z: 133.32,  y: 0 },   // → x: 0, z: 3200
    { name: 'desert',   x: 133.32,  z: 133.32,  y: 0 },   // → x: 3200, z: 3200
    { name: 'swamp',    x: -133.32, z: 0,       y: 0 },   // → x: -3200, z: 0
    { name: 'mountain', x: 0,       z: 0,       y: 5 },   // → x: 0, z: 0, y: 50 (10× höher!)
    { name: 'coast',    x: 133.32,  z: 0,       y: 0 },   // → x: 3200, z: 0
    { name: 'caves',    x: -133.32, z: -133.32, y: 0 },   // → x: -3200, z: -3200
    { name: 'forest',   x: 0,       z: -133.32, y: 0 },   // → x: 0, z: -3200
    { name: 'volcano',  x: 133.32,  z: -133.32, y: 0 }    // → x: 3200, z: -3200
];

// Line 633: Grid-Größe
const gridHelper = new THREE.GridHelper(400, 80, ...);  // → 9600 (world size)

// PlaneGeometry (Line 618)
new THREE.PlaneGeometry(regionSize, regionSize, 20, 20);  // Nutzt regionSize Variable

// WICHTIG: Finde alle Stellen mit festen Zahlen wie:
// - 133.32 (regionSize)
// - ±66.66 (halbe Region)
// - 400 (alte World Size)
```

## Zu ändernde Werte

### 1. Region-Größe
```python
# Pattern: const regionSize = 133.32;
old: "const regionSize = 133.32;"
new: "const regionSize = 3200;"
```

### 2. Region-Positionen (9 Stück)
```python
# X/Z-Koordinaten skalieren: 133.32 → 3200, -133.32 → -3200
# WICHTIG: Y-Koordinate bei mountain: 5 → 50 (Berg 10× höher!)

replacements = [
    ("x: -133.32, z: 133.32,", "x: -3200, z: 3200,"),    # ice
    ("x: 0,       z: 133.32,", "x: 0,     z: 3200,"),    # highland
    ("x: 133.32,  z: 133.32,", "x: 3200,  z: 3200,"),    # desert
    ("x: -133.32, z: 0,", "x: -3200, z: 0,"),            # swamp
    ("x: 0, z: 0,       y: 5", "x: 0, z: 0, y: 50"),     # mountain (y auch!)
    ("x: 133.32,  z: 0,", "x: 3200,  z: 0,"),            # coast
    ("x: -133.32, z: -133.32,", "x: -3200, z: -3200,"),  # caves
    ("x: 0,       z: -133.32,", "x: 0,     z: -3200,"),  # forest
    ("x: 133.32,  z: -133.32,", "x: 3200,  z: -3200,")   # volcano
]
```

### 3. Grid-Größe
```python
# Pattern: const gridHelper = new THREE.GridHelper(400, 80,
old: "const gridHelper = new THREE.GridHelper(400, 80,"
new: "const gridHelper = new THREE.GridHelper(9600, 80,"  # Mehr Grid-Lines ok
```

### 4. Shadow-Camera (optional, aber gut)
```python
# Lines 587-590: Shadow frustum größer für große Map
old: "directionalLight.shadow.camera.left = -150;"
new: "directionalLight.shadow.camera.left = -5000;"
# Auch right, top, bottom entsprechend
```

### 5. Kamera-Start-Position
```python
# Line ~50: camera.position.set(0, 50, 100);
# Für größere Map:
old: "camera.position.set(0, 50, 100);"
new: "camera.position.set(0, 300, 400);"  # Höher und weiter weg
```

### 6. Bewegungs-Geschwindigkeit
Suche nach Patterns wie:
```javascript
const moveSpeed = 20;  // → 80 (4× schneller)
const sprintSpeed = 40; // → 200
```

### 7. Combat-System: Enemy-Spawn-Bereich
Suche nach Random-Spawns:
```javascript
// Pattern: Math.random() * 100 - 50
// → Math.random() * 3000 - 1500  (±1500 statt ±50)
```

### 8. NPC/Location-Positionen
Falls NPCs/Locations hardcoded sind:
```javascript
// Pattern: position.set(10, 0, 15)
// → Skalieren mit Faktor 24 (133.32 → 3200)
```

## Script-Anforderungen

1. **Backup erstellen:** `.html.backup` vor Änderungen
2. **Regex-Patterns:** Nutze `re.sub()` für präzise Replacements
3. **Logging:** Gib aus, welche Änderungen gemacht wurden
4. **Safety:** Prüfe ob Datei existiert, handle Fehler
5. **Encoding:** UTF-8 für Windows (codecs.getwriter)
6. **Keine Emojis:** Windows Console kann keine Emojis

## Erfolgs-Kriterien
- ✅ regionSize: 133.32 → 3200
- ✅ 9 Region-Positionen korrekt skaliert
- ✅ Mountain y: 5 → 50
- ✅ Grid: 400 → 9600
- ✅ Kamera-Position angepasst
- ✅ Backup erstellt
- ✅ Konsole zeigt alle Änderungen

## Output
Script soll ausgeben:
```
[+] Gefunden: const regionSize = 133.32
[✓] Geaendert zu: const regionSize = 3200
[+] Gefunden: 9 Region-Positionen
[✓] Alle Positionen skaliert (133.32 → 3200)
[+] Mountain y-Hoehe: 5 → 50
[✓] Grid-Groesse: 400 → 9600
...
[OK] 15 Aenderungen erfolgreich!
```

## Testing
Nach dem Lauf:
1. Öffne `najika_world_UNIFIED.html` im Browser
2. Prüfe JavaScript Console: Sollte `regionSize = 3200` loggen
3. Teste WASD-Bewegung: Sollte schneller sein
4. Prüfe Map-Größe: Sollte viel größer aussehen

---

**Pfad zur Datei:**
`C:\Najika_World\digivice\najika_world_UNIFIED.html`

**Scale-Faktor:**
133.32 → 3200 (≈ 24×)

**Wichtig:**
- Nutze `re.sub()` mit rohen Strings `r"..."` für Patterns
- Escape Punkte in Zahlen: `133\.32`
- Behalte Whitespace-Formatierung bei (Tabs/Spaces)
- Teste jeden Replace einzeln mit `if re.search()` vorher
