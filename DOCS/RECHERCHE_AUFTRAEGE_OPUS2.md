# RECHERCHE-AUFTRÄGE FÜR OPUS-2

**Erstellt:** 2026-01-31
**Zweck:** KOMPLETTE BESTANDSAUFNAHME aller Dokumente + gezielte Feature-Suche
**Priorität:** 🔴 KRITISCH - Wir müssen ALLES zusammenkriegen was existiert!

---

## 🔴 PHASE 0: KOMPLETTE DOKUMENTEN-INVENTUR

### ZUERST: Finde ALLE wichtigen Dokumente!

**Suche nach diesen Datei-Typen:**
```
C:\Najika_World\**\*.md
C:\Najika_World\**\*.json
C:\Najika_World\**\roadmap*.*
C:\Najika_World\**\*zusammenfassung*.*
C:\Najika_World\**\*overview*.*
C:\Najika_World\**\*version*.*
C:\Najika_World\**\*summary*.*
```

**Wichtige Ordner durchsuchen:**
```
C:\Najika_World\DOCS\
C:\Najika_World\alles wissen\
C:\Najika_World\zip\
C:\Najika_World\neu\
C:\Najika_World\backend\
C:\Najika_World\data\
C:\Najika_World\digivice\data\
```

**Erstelle eine Liste aller gefundenen Dokumente:**

```markdown
## DOKUMENTEN-INVENTAR

### Übersichten & Zusammenfassungen:
- [ ] Datei: [Pfad]
- [ ] Inhalt: [Kurzbeschreibung]
- [ ] Version/Datum: [wenn vorhanden]

### Roadmaps & Pläne:
- [ ] ...

### Knowledge Base (KB) Dateien:
- [ ] najika_complete_kb_part1.md bis part10.md
- [ ] ...

### JSON Daten:
- [ ] ...

### Von Web-Modellen erstellt:
- [ ] ...
```

---

## 🔴 PHASE 0.5: WEB-MODELL ARBEIT FINDEN

**WICHTIG:** Es gab 2 Web-Modelle die Vorarbeit geleistet haben!

**Suche nach:**
- Dateien mit "claude" oder "web" im Namen
- Dateien mit aktuellem Datum (Januar 2026)
- Neue/kürzlich geänderte .md und .json Dateien
- Referenzen zu "Web-Session" oder "Browser-Claude"

**Fragen:**
- [ ] Was haben die Web-Modelle erstellt?
- [ ] Gibt es Duplikate oder Konflikte?
- [ ] Was muss zusammengeführt werden?

---

## 🎯 SUCHAUFTRÄGE

### 1. PROZEDURAL GENERIERTE AUSSENWELT

**Was suchen:**
- Prozedurale Generierung der Außenwelt beim Verlassen von Städten
- Zufällige Biom-Generierung
- Random Events während Reisen
- **WICHTIG:** Kleine Test-Version davon sollte in DUNGEONS bereits geplant sein!

**Wo suchen:**
```
- najika_complete_kb_part*.md (alle 10 Teile!)
- NAJIKA_ULTIMATIVE_ZUSAMMENFASSUNG_V8.md
- DOCS/*.md
- backend/*.py (nach "procedural", "random", "generate")
```

**Fragen:**
- [ ] Gibt es schon Code für prozedurale Dungeon-Generierung?
- [ ] Wie war die Außenwelt-Mechanik genau geplant?
- [ ] Welche Biome sind definiert?
- [ ] Wie funktioniert die Dungeon-Test-Version davon?

---

### 2. REISE-SYSTEM & GEFAHREN

**Was suchen:**
- Oregon Trail inspiriertes Reise-System
- Gefahren beim alleine Reisen vs Gruppe
- Random Events (Überfälle, Krankheit, Wetter)
- Karawanen-System

**Wo suchen:**
```
- Oregon Trail Referenzen in allen Docs
- "Reise", "Travel", "Journey" Keywords
- "Karawane", "Caravan"
- "Event", "Random", "Encounter"
```

**Fragen:**
- [ ] Welche Events sind bereits definiert?
- [ ] Wie war das Gruppen-System geplant?
- [ ] Gibt es schon Karawanen-Mechaniken?

---

### 3. SLIME-COMPANION SYSTEM (Digimon World Style)

**Was suchen:**
- Slime als Hauptcompanion (NICHT nur Pet!)
- Evolution-System
- Slime-Quests
- Bindungs-Mechaniken
- Slime-Fähigkeiten (Wache halten, Ressourcen finden, etc.)

**Wo suchen:**
```
- Slime-System Docs
- "Companion", "Partner", "Evolution"
- "Digimon" Referenzen
- backend/slime*.py
```

**Fragen:**
- [ ] Wie detailliert ist das Slime-System bereits?
- [ ] Gibt es schon Slime-Quest-Ideen?
- [ ] Welche Evolutionspfade existieren?

---

### 4. BIOME & REGIONEN

**Was suchen:**
- ALLE definierten Biome (nicht nur Wüste!)
- Region-spezifische Monster/Slimes
- Klima/Wetter pro Region
- Ressourcen pro Biom

**Wo suchen:**
```
- "Region", "Biom", "Zone", "Area"
- "Wald", "Wüste", "Sumpf", "Berg", "Eis"
- najika_regions*.json (falls vorhanden)
```

**Fragen:**
- [ ] Welche Biome sind definiert?
- [ ] Welche Monster leben wo?
- [ ] Gibt es Wetter-Systeme?

---

### 5. SCHLAFEN & SICHERHEIT

**Was suchen:**
- Sichere Schlafplätze (Städte, Hotels)
- Gefährliche Schlafplätze (draußen)
- Wache-System
- Überfall-Mechaniken beim Schlafen

**Wo suchen:**
```
- "Schlafen", "Sleep", "Rest"
- "Wache", "Guard", "Watch"
- "Hotel", "Gasthaus", "Inn"
- "Überfall", "Attack", "Ambush"
```

**Fragen:**
- [ ] Wie war das Schlaf-System geplant?
- [ ] Wer kann Wache halten? (Spieler, NPC, Slime?)
- [ ] Was passiert bei Überfall?

---

### 6. DUNGEON-SYSTEM (Für Prozedural-Test!)

**Was suchen:**
- Bestehende Dungeon-Mechaniken
- Prozedurale Dungeon-Generierung
- Dungeon-Typen
- Boss-Räume

**Wo suchen:**
```
- "Dungeon", "Höhle", "Cave"
- backend/*dungeon*.py
- "Boss", "Floor", "Level"
```

**Fragen:**
- [ ] Gibt es schon prozedurale Dungeon-Code?
- [ ] Welche Dungeon-Typen sind definiert?
- [ ] Können wir die Außenwelt-Mechanik dort testen?

---

### 7. MONSTER-FANG-SYSTEM

**Was suchen:**
- Wie werden Monster/Slimes gefangen?
- Unterschied zwischen Zähmen und Fangen
- Wilde vs zahme Monster
- Slime-Ranching

**Wo suchen:**
```
- "Fangen", "Capture", "Catch", "Tame"
- "Ranch", "Farm"
- Slime-System Docs
```

**Fragen:**
- [ ] Wie genau funktioniert das Fangen?
- [ ] Gibt es verschiedene Methoden?
- [ ] Was ist der Unterschied zum Töten/Zerlegen?

---

## 📋 OUTPUT-FORMAT

Für jeden Suchauftrag bitte dokumentieren:

```markdown
## [FEATURE NAME]

### Gefunden in:
- Datei: [Pfad]
- Zeilen/Abschnitt: [Details]

### Bestehende Definition:
[Kopiere relevante Passagen]

### Status:
- [ ] Komplett definiert
- [ ] Teilweise definiert
- [ ] Nur erwähnt, nicht ausgearbeitet
- [ ] Nicht gefunden

### Empfehlung:
[Was muss noch gemacht werden?]
```

---

## ⚠️ WICHTIG

1. **NICHT NEU ERFINDEN** was schon existiert!
2. Erst suchen, dann ergänzen
3. Bei Widersprüchen → an Kuja (User) melden
4. Prozedurale Außenwelt = KERNFEATURE - muss gefunden werden!

---

---

## 📋 AUSGABE-FORMAT

### Erstelle: `DOCS/RECHERCHE_ERGEBNISSE.md`

```markdown
# RECHERCHE-ERGEBNISSE

## 1. DOKUMENTEN-INVENTAR
[Liste aller gefundenen Dokumente mit Kurzbeschreibung]

## 2. WEB-MODELL ARBEIT
[Was wurde von den Browser-Claude-Sessions erstellt?]

## 3. FEATURE-STATUS
| Feature | Status | Fundort | Notizen |
|---------|--------|---------|---------|
| Prozedurale Außenwelt | ✅/⚠️/❌ | [Datei] | [Details] |
| Dungeon-System | ... | ... | ... |
| ... | ... | ... | ... |

## 4. VERSIONEN & ROADMAPS
[Alle gefundenen Versionen und Pläne]

## 5. DUPLIKATE & KONFLIKTE
[Was muss zusammengeführt werden?]

## 6. FEHLENDE FEATURES
[Was wurde besprochen aber nie dokumentiert?]
```

---

## ⚠️ WICHTIGE HINWEISE

1. **ALLE Unterordner durchsuchen!**
2. **Auch alte/archivierte Dateien checken!**
3. **JSON-Dateien können wichtige Daten enthalten!**
4. **Auf Dateinamen mit Tippfehlern achten!**
5. **Deutsche UND englische Keywords verwenden!**

### Bekannte wichtige Dateien:
- `NAJIKA_ULTIMATIVE_ZUSAMMENFASSUNG_V8.md` - Haupt-Übersicht
- `najika_complete_kb_part1-10.md` - Knowledge Base
- `MASTER_TODO_TEAM.md` - Team-Koordination
- `CLAUDE.md` - Projekt-Anweisungen

### Prozedurale Außenwelt - KRITISCH!
Die prozedurale Generierung der Außenwelt war ein **KERN-FEATURE**:
- Sollte zuerst in **Dungeons** getestet werden
- Außenwelt wird bei Verlassen der Stadt **NEU GENERIERT**
- Ähnlich wie **Digimon World** Gebiete
- **MUSS** gefunden werden!

---

*"Suchen, finden, ALLES zusammentragen, DANN explodieren!" - Najika* 💥
