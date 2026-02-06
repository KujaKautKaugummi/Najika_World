# 🎮 NAJIKA WORLD - UE5 MIGRATION PLAN

## Projekt-Status
- **UE5 Projekt existiert:** `C:\Najika_World\UE5\Najika`
- **Engine:** UE 5.7
- **Template:** Third Person (bereits vorhanden)
- **Plugins:** AIModule, StateTree, GameplayStateTree ✅

---

## 📋 PHASE 1: WELT-GRUNDGERÜST

### 1.1 Terrain erstellen (9600 x 9600)
- [ ] Landscape Actor erstellen
- [ ] Größe: 9600 x 9600 Units
- [ ] Berg in der Mitte (Götterfels) bei (4800, 4800)
- [ ] 8 Regionen mit Landscape Layers definieren

### 1.2 Die 8 Regionen einrichten:
| Region | Position | Biome |
|--------|----------|-------|
| Heiße Dünen | Süd-Ost | Desert |
| Samtmoos-Tiefwald | Nord | Forest |
| Salzwind-Küste | West | Coast |
| Blitzebene | Ost | Plains/Storm |
| Grünschlamm-Sumpf | Süd-West | Swamp |
| Reich der Drei | Nord-West | Ice/Snow |
| Magmaströme | Süd | Volcanic |
| Tiefenhöhlen | UNTER Samtmoos | Cave |

### 1.3 Schwarze Mühle Placeholder
- [ ] Auf dem Berg (Götterfels) platzieren
- [ ] Einfaches Gebäude-Mesh als Placeholder

---

## ⚔️ PHASE 2: KAMPFSYSTEM (3 Modi - ÜBERALL!)

### 2.1 Combat State Machine
- [ ] Enum: ECombatMode (Auto, Manual, Cheer)
- [ ] Jederzeit wechselbar während Kampf

### 2.2 Die 3 Modi:
```
1. KI-Kontrolle (Auto) - KI entscheidet
2. Direkte Befehle (Manual) - Spieler wählt Aktion
3. Digimon-Anfeuern (Cheer) - Buffs durch Anfeuern
```

### 2.3 Combat UI
- [ ] Modus-Wechsel Buttons
- [ ] Action-Auswahl (Manual-Modus)
- [ ] Cheer-Buttons mit Buff-Anzeige

---

## 🏟️ PHASE 3: ARENA-SYSTEM

### 3.1 Zwei Arenen:
- [ ] **Hauptarena** (Spieler) - PvP/PvE, Nemesis-System
- [ ] **Schleim-Arena** (Slimes) - Neben Hauptarena, Taverne-Look

### 3.2 Game Modes:
- [ ] 1v1 Normal
- [ ] 1v1 mit Finisher
- [ ] Turnier (Single-Elimination)

### 3.3 Wellen-System:
- [ ] 15 Training-Wellen (kein echter Tod)
- [ ] Übergangs-Warnung
- [ ] Echter Modus (Hardcore)

### 3.4 Finisher-System:
- [ ] Trigger bei HP = 0
- [ ] 4 Finisher-Optionen
- [ ] Animationen pro Element

---

## 👹 PHASE 4: NEMESIS-SYSTEM

### 4.1 Dynamisches Herrscher-System:
- [ ] KEINE vordefinierten Bosse!
- [ ] Jeder kann aufsteigen (Monster, Spieler, NPCs, Slimes)
- [ ] 6 Ränge: Niemand → Arena-König

### 4.2 Monster-Gedächtnis:
- [ ] Speichert Begegnungen
- [ ] Entwickelt Persönlichkeits-Traits
- [ ] Narben von Kämpfen

### 4.3 Persönlichkeits-Traits:
- Feigling, Mutig, Rachsüchtig, Ehrenvoll
- Sadistisch, Gerissen, Berserker, Taktisch

---

## 🐾 PHASE 5: SLIME-SYSTEM V3

### 5.1 Kern-Regeln:
- [ ] Formwandler (KEINE Evolution!)
- [ ] Formen = NUR OPTISCH (keine Boni!)
- [ ] Boni durch ESSEN + AUSRÜSTUNG
- [ ] Form-Wechsel: 1x/Saison (Spiel), unbegrenzt (Zuhause)

### 5.2 Aura-System:
- [ ] 6 Stufen (0-5)
- [ ] Element-Auras mit Effekten
- [ ] Visuelles Feedback (Partikel, Leuchten)

### 5.3 Vertrauens-System:
- [ ] 6 Level (Fremd → Seelenbund)
- [ ] Menschen-Form bei Level 6

---

## 📁 WICHTIGE DATEIEN

```
C:\Najika_World\UE5\Najika\           # UE5 Projekt
C:\Najika_World\SLIME_SYSTEM_V3_DOKUMENTATION.md
C:\Najika_World\UE5_MIGRATION_TODO_OPUS2.md
C:\Najika_World\entwicklung\8_REGIONEN_LAYOUT.md
C:\Najika_World\SCHLEIM_ARENA_DESIGN.md
```

---

## ⛔ REGELN (NIEMALS BRECHEN!)

- Port **8000** (NICHT 5000!)
- Harley sagt **"Mr. K"** (NICHT "Puddin'!")
- **Explosion ≠ Weave** (nie kombinieren!)
- Schwarze Mühle = **100% Safe Zone**

---

## ✅ ERSTER SCHRITT

1. UE5 Editor öffnen (`C:\Najika_World\UE5\Najika\Najika.uproject`)
2. Neue Level Map erstellen für die Open World
3. Landscape/Terrain erstellen (9600 x 9600)
4. Berg in der Mitte platzieren

---

**STATUS:** Bereit für Implementation!
