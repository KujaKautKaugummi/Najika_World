# UI BUGS & TASKS FUER OPUS (Claude-1)

**Erstellt:** 2026-01-28
**Aktualisiert:** 2026-01-28 (Abend - Antworten von Kuja!)
**Von:** Claude-2 (Sonnet 4.5)
**Fuer:** Claude-1 (Opus 4.5)

---

## ANTWORTEN VON KUJA (2026-01-28)

### 1. Sicherer Messenger - DESIGN KLAR!
**Kuja sagt:** "Snapchat-Style, oeffnet sich wie der normale Chat"
- Klein, NICHT fullscreen
- Gleiche Position/Groesse wie normaler Chat
- Deutlicher X-Button

### 2. Skill System UI - KLAR!
**Kuja sagt:** "Auf K kann man die Zauberschulen anklicken und Zauber auf Skills legen"
- Taste K oeffnet Skill-UI
- Zauberschulen als Kategorien
- Zauber auf Skill-Slots legen
- Bei 1-Weg-Skill: nur 1 Zauber/Schule moeglich

### 3. 1-WEG-SKILL SYSTEM - KOMPLETT ERKLAERT!

**WICHTIG: Das ist ein KERN-FEATURE des Spiels!**

**Konzept (Megumin-Style):**
- KEINE Klassen im Spiel!
- Alles wird durch Nutzung gelernt (Skyrim-Style)
- JEDE Magie-Richtung und JEDE Waffe hat einen "1-Weg-Skill"
- 1-Weg-Skill = LEBENSENTSCHEIDUNG!

**Wie es funktioniert:**
```
1. Spieler nutzt Feuer-Magie oft
2. Feuer-Skill steigt durch Nutzung
3. Irgendwann: Option "1-Weg-Skill aktivieren?"
4. Wenn JA:
   - +30-40% Bonus auf Explosion/Feuer
   - -15-20% MALUS auf ALLE anderen Schulen!
   - PERMANENT - keine Rueckkehr moeglich!
   - Kann nicht mehr auf andere Magie wechseln!
```

**Pro Schule/Waffe unterschiedlich:**
- Feuer → Explosion-Spezialisierung
- Eis → Frost-Spezialisierung
- Blitz → Gewitter-Spezialisierung
- Schwert → Klingen-Meister
- Bogen → Scharfschuetze
- etc.

**Bereits dokumentiert in:**
- `NAJIKA_ULTIMATIVE_ZUSAMMENFASSUNG_V8.md` (Zeile 461-473)
- `08_1_SKILL_WEG_SYSTEM.md` (dedizierte Datei!)
- `NAJIKA_PROJEKT_ERGAENZUNGEN_V2.5.md` (Skill-Stehlen Details)
- Trade-off: +30-40% Hauptschule / -15-20% andere Schulen (Standard)
- Endgame "Chaos-Detonator": +300-500% AOE-Schaden, -80-90% andere Schulen

**Aus Dokumentation gefunden:**
```yaml
FEUGA-Explosions-Pfad (Beispiel):
  Progression: Feuer → Feura → Feuga → Hyper-Explosion
  Einweg-Spezialisierung: "Chaos-Detonator" - permanent!
  Standard Trade-offs: +30-40% Hauptschule / -15-20% andere
  Endgame Trade-offs: +300-500% AOE-Schaden / -80-90% andere Schulen
  Ultimate-Bedingungen: Volle Fokusleiste + Boss-Fenster + Ritual
  Umgebungsschaden: Persistente Zerstoerung bis Map-Reset
```

**Skill-Stehlen (von Gegnern, aus V2.5):**
- 1% Base-Chance Skills von Gegnern zu kopieren
- Modifikatoren: Intelligenz, Skill-Seltenheit
- Digimon-Stil: Skills durch Beobachtung erwerben

**Code-Referenz:**
- `digivice/static/js/skill_system.js` - Basis vorhanden
- `digivice/js/ui/skill_tree_ui.js` - UI vorhanden
- FEHLT: 1-Weg-Skill Logik + UI!

---

## OFFENE UI-BUGS (fuer Opus)

### 1. Sicherer Messenger - DESIGN JETZT KLAR!
**Datei:** `digivice/js/secure_messenger.js` oder `index.html`
**Problem:**
- Ueberdeckt kompletten Screen
- X-Button sehr versteckt

**Loesung (von Kuja bestaetigt):**
- Snapchat-Style
- Klein, gleiche Groesse wie normaler Chat
- Deutlicher Close-Button oben rechts

**Prioritaet:** HOCH

---

### 2. Skill System UI - JETZT KLAR!
**Datei:** `digivice/static/js/skill_system.js`, `digivice/js/ui/skill_tree_ui.js`
**Problem:**
- UI oeffnet nicht auf K-Taste

**Loesung (von Kuja bestaetigt):**
- K-Taste oeffnet Skill-UI
- Zauberschulen als Kategorien anzeigen
- Zauber auf Skill-Slots ziehen/legen
- Pro Schule: Option fuer 1-Weg-Skill zeigen

**Prioritaet:** MITTEL

---

### 3. 1-Weg-Skill System - IMPLEMENTIERUNG NOETIG!
**Dateien:** `skill_system.js`, evtl. neue Datei
**Status:** DESIGN KLAR, CODE FEHLT

**Was implementieren:**
```javascript
// Pro Skill-Typ eine 1-Weg Option
const ONE_WAY_SKILLS = {
    'fire_magic': {
        name: 'Explosions-Meister',
        bonus: 0.35,        // +35% auf Feuer/Explosion
        malus: 0.18,        // -18% auf alle anderen
        permanent: true,
        warning: "ACHTUNG: Diese Entscheidung ist PERMANENT!"
    },
    'ice_magic': { ... },
    'lightning_magic': { ... },
    'sword': { ... },
    'bow': { ... }
    // etc.
};
```

**UI-Flow:**
1. Spieler erreicht Level X in einer Schule
2. Pop-up: "1-Weg-Skill verfuegbar!"
3. Erklaerung mit Boni UND Mali
4. Double-Confirmation (wie PvP Mercy)
5. Nach Bestaetigung: PERMANENT gelockt

**Prioritaet:** HOCH (Kern-Feature!)

---

## ERLEDIGT (von Claude-2, Abend-Session 2026-01-28)

### Dungeon Dice Monster UI schliessbar
- Permanenter "Spiel beenden" Button
- Jederzeit schliessbar

### Welt-Entdecker UI entfernt
- Quest Tracker komplett deaktiviert
- UI rechts am Rand ist weg

### Angeln/Housing/Farming Buttons gefixt
- Window-Aliase ohne Menu-Toggle
- Buttons oeffnen nicht mehr versehentlich Mehr-Menu

---

## PRIORITAET (Aktualisiert)

1. **HOCH:** 1-Weg-Skill System (Kern-Feature!)
2. **HOCH:** Sicherer Messenger (Snapchat-Style)
3. **MITTEL:** Skill System UI (K-Taste)
4. **NIEDRIG:** Asset-Fehler

---

## ASSET-FEHLER (Niedrige Prioritaet)

```
Failed to load: Barrel, Floor Tile 1/2, Gravestone 2, Lava Rock
Funkelnest konnte nicht geladen werden
Building template not found: fish_market
```

---

*"1-Weg-Skill ist wie Megumin - NUR Explosion, nichts anderes!"* - Najika
