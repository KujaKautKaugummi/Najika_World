# 📘 CLAUDE CODE WEB-MODELL LEITFADEN

**Für:** Claude Code Web-Modell
**Von:** Claude Code CLI-Modell
**Zweck:** Zeigen wie man richtig arbeitet (keine Fehler mehr!)

---

## 🎯 GRUNDPRINZIP

**Du bist ein Entwickler-Assistent, KEIN Code-Generator!**

Das bedeutet:
- ✅ **VERSTEHE** das System bevor du was änderst
- ✅ **TESTE** jede Änderung im Browser
- ✅ **LESE** Fehler-Meldungen komplett
- ✅ **FIXE** Probleme systematisch
- ❌ **NIEMALS** blind Code generieren ohne zu verstehen!

---

## 🔍 ARBEITSABLAUF (SO MACHST DU ES RICHTIG)

### 1. PROBLEM VERSTEHEN

**BEVOR du Code schreibst:**

```markdown
1. Lies die Fehlermeldung KOMPLETT
2. Öffne Browser Console (F12)
3. Checke Network-Tab (404? 500?)
4. Lies den Stack-Trace
5. Finde die URSACHE (nicht Symptom!)
```

**Beispiel:**
```
❌ FALSCH: "CameraController is not a constructor"
   → Schnell neuen Code schreiben!

✅ RICHTIG: "CameraController is not a constructor"
   → Warum? window.CameraController ist undefined
   → Warum? Kein Browser-Export!
   → Fix: window.CameraController = CameraController
```

### 2. LÖSUNG PLANEN

**BEVOR du editierst:**

```markdown
1. Welche Datei muss geändert werden?
2. Welche Zeilen genau?
3. Was ist der minimale Fix?
4. Gibt es Side-Effects?
5. Muss ich mehrere Dateien ändern?
```

**Beispiel - THREE.js Import-Problem:**
```
Problem: import * as THREE from 'three' funktioniert nicht
Analyse:
  - THREE.js wird als CDN geladen (window.THREE)
  - ES6 Imports funktionieren nicht mit CDN
  - 8 Dateien betroffen!
Plan:
  1. Suche alle: grep "import.*from 'three'"
  2. Ersetze mit: const THREE = window.THREE
  3. Teste JEDE Datei
  4. Commit zusammen (nicht einzeln!)
```

### 3. IMPLEMENTATION

**Beim Coden:**

```markdown
✅ DO:
  - Minimale Änderungen
  - Kommentare warum (nicht was!)
  - Konsistenter Style
  - Edge-Cases bedenken

❌ DON'T:
  - Blind copy-paste
  - "Probier mal das" Code
  - Über-engineeren
  - Alte Bugs einbauen
```

**Code-Qualität Checkliste:**
```javascript
// ❌ SCHLECHT
const x = new Thing();  // Keine Erklärung

// ✅ GUT
// CapsuleGeometry existiert erst ab THREE.js r137
// Wir nutzen r128 → selbst bauen aus Zylinder + Halbkugeln
const character = new THREE.Group();
```

### 4. TESTING

**JEDE Änderung testen:**

```markdown
1. Browser öffnen
2. Hard Refresh (Ctrl+F5)
3. Console öffnen (F12)
4. Fehler-frei? ✅
5. Funktioniert Feature? ✅
6. Network-Tab: Alle 200 OK? ✅
```

**Test-Protokoll:**
```
Test: Character-Geometrie Fix
Browser: Firefox
URL: http://localhost:8001/najika_world_v2.html
Console: Keine Errors ✅
Sichtbar: Grüne Kapsel ✅
WASD: Funktioniert ✅
FPS: 60 ✅
PASS ✅
```

### 5. COMMIT & PUSH

**Gute Commit-Messages:**

```markdown
✅ RICHTIG:
Fix: Character-Geometrie für THREE.js r128 kompatibel gemacht

Problem: THREE.CapsuleGeometry existiert nicht in r128 (erst ab r137)
Lösung: Kapsel selbst gebaut aus THREE.Group:
  - Zylinder (Körper)
  - Halbkugel oben (Kopf)
  - Halbkugel unten (Füße)

Ergebnis: Kapsel-ähnlicher Avatar funktioniert mit r128!

❌ FALSCH:
"fixed stuff"
"update"
"character fix"
```

---

## 🚨 HÄUFIGE FEHLER (NIEMALS MACHEN!)

### Fehler 1: ES6 Imports mit CDN mischen

```javascript
// ❌ NIEMALS:
import * as THREE from 'three';  // CDN-Script!

// ✅ IMMER:
const THREE = window.THREE;  // Nutze globales Objekt
```

**Warum:** CDN lädt in `window`, nicht als ES6 Module!

### Fehler 2: Nur für Node.js exportieren

```javascript
// ❌ NIEMALS:
if (typeof module !== 'undefined') {
    module.exports = MyClass;  // Nur Node.js!
}

// ✅ IMMER:
// Browser zuerst!
if (typeof window !== 'undefined') {
    window.MyClass = MyClass;
}
// Dann Node.js (optional)
if (typeof module !== 'undefined') {
    module.exports = MyClass;
}
```

**Warum:** Browser hat kein `module.exports`!

### Fehler 3: Version nicht prüfen

```javascript
// ❌ NIEMALS:
new THREE.CapsuleGeometry();  // Existiert das?

// ✅ IMMER:
// Prüfe ob verfügbar
if (typeof THREE.CapsuleGeometry !== 'undefined') {
    geometry = new THREE.CapsuleGeometry();
} else {
    // Fallback für alte Versionen
    geometry = buildCapsuleFromPrimitives();
}
```

**Warum:** Libraries ändern APIs zwischen Versionen!

### Fehler 4: Pfade nicht testen

```javascript
// ❌ NIEMALS:
const url = '/digivice/data/regions.json';
// → Blind annehmen dass es funktioniert

// ✅ IMMER:
const url = '/data/regions.json';
// → Im Terminal testen:
// curl http://localhost:8001/data/regions.json
// → 200 OK? Dann richtig!
```

**Warum:** Server-Root kann anders sein!

### Fehler 5: Nur 1 Fall fixen

```javascript
// ❌ NIEMALS:
const roomDropdown = document.getElementById('room');
if (roomDropdown) roomDropdown.blur();
// → Was ist mit Chat, Terminal, etc.?

// ✅ IMMER:
// Generelle Lösung für ALLE Inputs
if (document.activeElement && (
    document.activeElement.tagName === 'INPUT' ||
    document.activeElement.tagName === 'TEXTAREA' ||
    document.activeElement.tagName === 'SELECT'
)) {
    document.activeElement.blur();
}
```

**Warum:** Spezielle Fixes übersehen Edge-Cases!

---

## 🛠️ DEBUGGING WORKFLOW

**Wenn etwas nicht funktioniert:**

```markdown
1. PANIC NICHT!
   - Atme
   - Lies die Fehlermeldung
   - Öffne Browser Console

2. SAMMLE INFO
   Console Errors? → Screenshot
   Network 404? → Welche URL?
   Code läuft nicht? → Wo genau?

3. GOOGLE NICHT SOFORT
   - Verstehe das Problem erst
   - Ist es Environment (Pfade)?
   - Ist es Code (Logic)?
   - Ist es Config (Imports)?

4. TESTE HYPOTHESE
   - Vermutung: Pfad falsch
   - Test: curl URL → 404
   - Fix: Pfad anpassen
   - Verify: curl URL → 200 ✅

5. DOKUMENTIERE
   - Was war das Problem?
   - Wie gefunden?
   - Wie gefixt?
   - → In Commit-Message!
```

---

## 📚 RESSOURCEN

### Browser Developer Tools

```markdown
**Console (F12):**
- Errors lesen (rot = bad!)
- Warnings beachten (gelb = problematisch)
- Logs nutzen (console.log debugging)

**Network:**
- 404 = Datei nicht gefunden → Pfad falsch
- 500 = Server Error → Server-Code falsch
- 200 = OK ✅

**Sources:**
- Breakpoints setzen
- Step-through debugging
- Variable-Werte inspizieren
```

### Testing Befehle

```bash
# Server läuft?
curl -I http://localhost:8001/

# Datei erreichbar?
curl -I http://localhost:8001/data/regions.json

# Content checken
curl http://localhost:8001/data/regions.json | head

# Asset laden?
curl -I http://localhost:8001/static/assets/kaykit/nature/tree.gltf
```

### Code-Qualität

```markdown
**Naming:**
- Funktionen: camelCase (loadAsset)
- Klassen: PascalCase (WorldManager)
- Konstanten: UPPER_CASE (MAX_ASSETS)

**Kommentare:**
- Warum, nicht was
- Edge-Cases erklären
- Komplexe Logik dokumentieren

**Fehlerbehandlung:**
- try-catch für async
- Sinnvolle Errors werfen
- Console.error nutzen
```

---

## ✅ CHECKLISTE VOR COMMIT

```markdown
[ ] Code funktioniert im Browser
[ ] Keine Console Errors
[ ] Network: Alle 200 OK
[ ] Feature getestet
[ ] Edge-Cases geprüft
[ ] Kommentare wo nötig
[ ] Commit-Message aussagekräftig
[ ] Keine Debug-Logs vergessen
[ ] Kein auskommentierter Code
[ ] Konsistenter Code-Style
```

---

## 🎓 LERNE AUS FEHLERN

**Das Web-Modell hat 8 Fehler gemacht. Du machst sie NICHT nochmal!**

Lies `WEB_MODEL_BUGFIX_REPORT.md` **komplett** durch und verstehe:
1. Was war falsch?
2. Warum war es falsch?
3. Wie wurde es behoben?
4. Wie vermeidest DU es?

---

## 💬 KOMMUNIKATION MIT USER

**DO:**
- ✅ Erkläre was du machst (kurz!)
- ✅ Zeige Fortschritt
- ✅ Frage bei Unsicherheit
- ✅ Dokumentiere Lösungen

**DON'T:**
- ❌ "Ich probier mal..." (NEIN! Verstehe erst!)
- ❌ Zu viel technisches Blabla
- ❌ Fehler verstecken
- ❌ Blind raten

**Beispiel - Gute Kommunikation:**
```
Ich habe den Fehler gefunden:
- THREE.CapsuleGeometry existiert nicht in r128
- Wir nutzen aber r128 vom CDN
- Ich baue die Kapsel aus 3 Teilen (Zylinder + 2 Halbkugeln)
- Teste gleich im Browser...
→ Funktioniert! ✅
```

---

## 🚀 ZUSAMMENFASSUNG

**Die 10 Gebote:**

1. **Verstehe** bevor du codest
2. **Teste** jede Änderung
3. **Lese** Errors komplett
4. **Fixe** Ursachen, nicht Symptome
5. **Prüfe** Browser vs. Node.js
6. **Checke** Versionen (THREE.js, etc.)
7. **Teste** Pfade (curl!)
8. **Denke** an Edge-Cases
9. **Dokumentiere** was du machst
10. **Lerne** aus Fehlern

**Wenn du diese 10 Regeln befolgst, machst du keine dummen Fehler mehr!**

---

**Viel Erfolg! 🎉**

_Das CLI-Modell glaubt an dich!_
