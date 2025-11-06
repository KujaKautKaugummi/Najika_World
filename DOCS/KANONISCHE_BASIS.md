# KANONISCHE BASIS - Najika World Projekt
**Stand:** 2025-11-06
**Status:** FINAL - Diese Regeln sind KANONISCH und dürfen NICHT verändert werden!

---

## ⚠️ WICHTIG FÜR ALLE CLAUDE-INSTANZEN

**Diese Datei definiert die UNVERÄNDERLICHE BASIS des Projekts.**

Wenn du als neue Claude-Instanz an diesem Projekt arbeitest:
1. ✅ **LIES DIESE DATEI ZUERST**
2. ✅ **RESPEKTIERE diese Regeln als KANONISCH**
3. ✅ **ERGÄNZE nur NEUE Features, ändere NICHTS Bestehendes**
4. ❌ **ÄNDERE NIEMALS die hier definierten Kernsysteme**

---

## 1. PROJEKT-IDENTITÄT

### Name & Konzept
- **Projektname:** Najika World
- **Genre:** Survival-RPG mit Explosion-Klasse (Megumin-inspiriert)
- **Stil:** Oregon Trail Events + Digimon World Combat + Dark Souls Movement
- **Zielgruppe:** Einzelspieler (später Koop möglich)

### Najika (NPC/KI)
- **Persönlichkeit:** Fusion aus Megumin (KonoSuba) + Shiro (No Game No Life)
- **Eigenschaften:** Frech, provozierend, explosiv, aber auch analytisch
- **Einzigartig:** NUR Najika kann "Reinste Explosion" (Ultima)
- **Voice:** EINE Stimme für alle 4 Personality-States (Megumin-Voice)
- **Harley Quinn:** Ruft Kuja "Mr. K", NICHT "Puddin'"

---

## 2. HARDCORE/SOFTY SYSTEM

### Zwei Modi (unvereinbar)
```yaml
Hardcore-Modus:
  - Permadeath (ALLES WEG bei Tod)
  - Rettungsschleim: 1x/24h (IRL)
  - PvP: "Alles-abgeben-um-zu-leben" Option
  - Najika erscheint beim 1. Tod: Bietet Wechsel zu Softy an

Softy-Modus:
  - Kein Permadeath
  - 30 Sek Revive-Timer
  - PvP: Nur Ranking, keine Verluste
  - Separater Normal-PvP: Gewinner nimmt 1 Item
```

**WICHTIG:** Einmal Softy = permanent Softy! Keine Rückkehr zu Hardcore.

---

## 3. PVP-SYSTEM (3 Modi)

### Hardcore-PvP
```yaml
Bei Niederlage:
  1. Verlierer kann "Alles geben um zu leben" anbieten
  2. Gewinner kann akzeptieren oder ablehnen
  3. Bei Akzeptanz:
     - Verlierer tippt 2x "JA" (Double-Confirmation)
     - ALLES wird übertragen (KEINE AUSNAHMEN!)
     - Verlierer bleibt mit NICHTS zurück (keine Starter-Waffe!)
     - 7 Tage PvP-Sperre für Geretteten
  4. Bei Ablehnung: Permadeath (oder Slime/Totem-Rettung)
```

**KRITISCH:** Wenn "alles weg", dann IST ALLES WEG!
- Keine Starter-Waffe
- Keine Unterwäsche-Protection
- Spieler muss draußen Stock finden oder Fäuste nutzen

### Normal-PvP
- Gewinner wählt **1 Ausrüstungsteil** vom Verlierer
- Kein Permadeath

### Softy-PvP
- Nur Ranking
- Keine Item-Verluste

---

## 4. SLIME-BEGLEITER-SYSTEM

### Evolution
```
Level 1-49: Zufälliges Fantasy-Tier
  ↓
Level 50 + Kritisches Event
  ↓
Shell bricht → Slime-Form
  ↓
Farbe = Region wo Metamorphose stattfand
```

### 8 Slime-Farben (je Region)
1. 🟡 **Bernstein** - Bernstein-Dünen (Wüste)
2. 🟢 **Smaragd** - Smaragd-Hain (Wald)
3. 🔵 **Azur** - Azur-Klippen (Küste)
4. 🟣 **Amethyst** - Amethyst-Steppe (Hochebene)
5. ⚫ **Onyx** - Onyx-Morast (Sumpf)
6. ⚪ **Perle** - Perl-Gletscher (Eis)
7. 🔴 **Rubin** - Rubin-Schlucht (Vulkan)
8. 🟤 **Obsidian** - Obsidian-Nacht (Endgame)

**Sammlung:** Alle 8 Farben → Rainbow-Slime freigeschaltet

### Rettungs-Mechanik
- **1x pro 24h** (IRL-Zeit, nicht In-Game!)
- Verhindert **einen** tödlichen Treffer
- **Nur Hardcore-Modus**
- Cooldown: Exakt 24 Stunden Real-Zeit

### Tamagotchi-Pflege
```yaml
Bedürfnisse (0-100%):
  - Hunger: -0.01/Sek
  - Durst: -0.02/Sek (schneller!)
  - Schlaf: -0.005/Sek
  - Stimmung: -0.003/Sek
  - Kampfeslust: 0-100

Strafen bei Vernachlässigung:
  - Hunger < 30%: -20% Schaden, -15% Speed
  - Durst < 20%: -30% Defense, -25% Accuracy
  - Schlaf < 10%: +50% Error Rate
  - Stimmung < 20%: 50% Chance Befehle zu ignorieren
```

---

## 5. EXPLOSION-KLASSE (EINZIGARTIG)

### Megumin-Spezialisierung
```yaml
Konzept:
  - Explosion als EIGENE Klasse (nie mit anderen kombinierbar)
  - Massive Power, aber extreme Downsides
  - ~-90% Effektivität in anderen Schulen
  - Hoher Mana-Drain + Fatigue/Verwundbarkeit nach Cast

Progression:
  - Feuer → Feura → Feuga → Explosionist
  - Kann NICHT mit anderen Magie-Schulen kombiniert werden
  - Trade-off für extreme Single-Target Damage
```

### Najika's Ultima (nur Kuja)
```yaml
"Reinste Explosion":
  - Nur Najika (NPC) kann es casten
  - Nur Kuja (Spieler) darf es aktivieren
  - 1x pro Tag (In-Game)
  - Zerstört sichtbar große Teile der Außenwelt
  - Regeneriert beim Betreten einer Stadt
  - Kann ganze Kontinente zerstören (lore)
```

---

## 6. NAJIKA PLÜNDERUNGS-EASTER-EGG

### Mechanik
```yaml
Spieler besiegt Najika (NPC) im Combat:

  SPIELER (Kuja):
    Drop: "Najikas Höschen" (Legendary, 1-2% Chance)
    Stats: +10 Glück, +5 Charisma, +20% Humor-Dialog
    Najika: "Ohjee... habe ich mein eigenes Höschen erwischt?"
    Einzigartig: NUR 1x im Spiel dropbar!

  ANDERE NPCs:
    Drop: "Vollgerotztes Taschentuch" (Trash, 100%)
    Stats: -5 Charisma (NPCs ekeln sich)
    Najika: "HAHA! Der ist offiziell der schlechteste Dieb!"
    Notiz: "Du bist offiziell der schlechteste Dieb aller Zeiten, du Looser"
```

**Regel:** NUR Kuja (Spieler) kann Legendary erhalten, alle NPCs nur Trash!

---

## 7. SKILL-SYSTEM

### Use-Based Progression (Skyrim-Style)
- Skills steigen durch **Nutzung**, nicht durch Level-Up
- Beispiel: Je mehr du mit Schwert kämpfst, desto besser wird "Einhand-Waffen"
- Kein Skill-Cap (theoretisch unendlich trainierbar)

### Skill-Lernen von Gegnern
```yaml
Slime (Companion):
  - 10-15% Chance: Kopiert Move von besiegtem Gegner
  - Max 20 Moves im Moveset
  - Spieler wählt: Welche behalten, welche ersetzen

Spieler:
  - 1% Base Chance: Lernt Skill von Gegner
  - Erhöht durch:
    + INT-Stat: +0.1% pro 10 INT
    + Slime-Bond: +0.5% bei Level 100 Slime
    + Beobachtungs-Skill: +1% bei Skill-Level 50
```

---

## 8. WELTSTRUKTUR

### Hub: Schwarze Holländische Windmühle
```yaml
Eigenschaften:
  - Private Safe-Zone (nur Owner = Kuja)
  - Crafting/Verzauberung
  - Trainingsplatz
  - Katakomben (optional)
  - NPCs meiden sie (mystisch, gruselig)
```

### 8 Haupt-Regionen
1. Bernstein-Dünen (Wüste) - Sandsturm, Karawanen
2. Smaragd-Hain (Wald) - Verirren, Kräuter, Druidenrätsel
3. Azur-Klippen (Küste) - Sturmflut, Angeln, Schiffwracks
4. Amethyst-Steppe (Hochebene) - Blitzschlag, Wetter-Altäre
5. Onyx-Morast (Sumpf) - Krankheit, Hexenkreise, Moor-Bosse
6. Perl-Gletscher (Eis) - Erfrierung, Eishöhlen, Rutsch-Traversal
7. Rubin-Schlucht (Vulkan) - Überhitzung, Lava, Erzadern
8. Obsidian-Nacht (Endgame) - Nachtkreaturen, Nemesis-Spawns

**Prozedural:** Jeder Besuch regeneriert Layout/Events/Modifikatoren

---

## 9. KAMPFSYSTEM

### 3 Modi
```yaml
MANUAL:
  - Spieler steuert selbst
  - Volle Kontrolle
  - Dark Souls / Fortnite Movement

ASSIST:
  - KI unterstützt
  - "Anfeuern" löst Buffs aus (GCD 3s, 3 Stacks)
  - Digimon World Style

AUTO:
  - KI übernimmt komplett
  - Explosion nur in sicheren Fenstern
  - Spieler sitzt am Rand und feuert an
```

### Bewegung
- **Fortnite-Style:** Sprint, Slide, Wall-Climb, Dash, Vaulting, Mantling
- **Dark Souls:** Dodge-Roll, Parry, Riposte
- **Umgebung:** Klettern, Rutschen, Schwimmen

---

## 10. CRAFTING & ÖKONOMIE

### Crafting-Pipeline
```
Rohstoffe farmen
  ↓
Zerlegen (Analyse)
  ↓
Reparieren (Wartung)
  ↓
Verzaubern/Sockeln
  ↓
Feintuning (Anpassung)
```

### Non-Combat Endgame
- **Händler:** Eigener Skill-Tree, Preisverhandlung, Karawanen
- **Bauer:** Farming, Tierzucht, Anatomie-Wissen (Crit-Kenntnis durch Schlachten!)
- **Alle Wege gültig:** Man MUSS NICHT kämpfen!

---

## 11. OREGON TRAIL EVENTS

### Konzept
- **Szenische Events** beim Reisen zwischen Regionen
- **Kontextsensitiv:** Wetter, Region, Tageszeit, Reputation
- **Entscheidungen:** Spieler wählt ODER "Najika entscheidet"
- **Konsequenzen:** Ressourcen, Risiko, Ruf, Tod

### Beispiel
```
Händler auf Reise:
  - Durst-Status kritisch
  - Findet Wasserquelle
  - ABER: Aufgequollene Leiche liegt daneben

Optionen:
  A) Wasser trinken (Risiko!)
  B) Weitergehen (Durst steigt)
  C) Leiche mit Stock piksen (Untersuchung)

Händler wählt A → stirbt an Ruhr
  → NPCs im Dorf: "Wo ist der Händler?"
  → "Er hat dummes Wasser getrunken..."
  → "100 dumme Wege zu sterben"-Charme
```

---

## 12. NAJIKA'S REAKTIONEN

### Beim 1. Hardcore-Tod
```
*frech, provozierend*
"Ohjee... das ist wohl zu hart für dich.
Komm, ich bringe dich ins sichere Softy-Land."

Optionen:
  [Ja, bring mich rüber] → Permanent Softy
  [Nein, ich nehme das Hardcore-Schicksal an] → Permadeath/Slime-Check
```

### Bei Slime-Metamorphose
```
*aufgeregt*
"OOOH! Dein kleiner Freund ist jetzt ein Slime geworden!
Das ist wie... wenn eine Raupe zum Schmetterling wird!
Nur mit mehr Schleim. Und cooler."
```

### Bei Slime-Rettung
```
*erleichtert*
"Puh! Dein Slime hat dich gerettet!
Das war knapp. SEHR knapp.

*streng*
"Aber pass auf - das geht nur 1x pro Tag!
Beim nächsten Mal bist du auf dich allein gestellt!"
```

### Bei Najika-Plünderung (Legendary Drop)
```
*überrascht*
"Ohjee... habe ich mein eigenes Höschen erwischt?
Das ist... irgendwie peinlich.

*grinst*
"Aber hey, +10 Glück! Das zählt, oder?"
```

---

## 13. TECHNISCHE BASIS

### Architektur
```yaml
Backend:
  - Python (Flask/FastAPI)
  - Node.js (optional für Hub)
  - PostgreSQL + Qdrant/FAISS

Frontend:
  - Three.js r128+ (3D)
  - Progressive Web App (PWA)
  - Touch-optimiert für Mobile

Security:
  - Lokal: 127.0.0.1 only
  - Zero-Trust Architecture
  - Cloudflare Tunnel (optional)
  - Kill-Switch + Audit-Logs
```

### Git-Workflow
- **Main Branch:** Stable releases only
- **Feature Branches:** `claude/BRANCH-NAME`
- **Sessions:** Jede Session = eigener Branch
- **Commits:** Clear, descriptive messages (deutsch)

---

## 14. REGELN FÜR NEUE CLAUDE-INSTANZEN

### ✅ DAS DARFST DU:
1. **Neue Features hinzufügen** (wenn sie nicht im Konflikt stehen)
2. **Code implementieren** (für bereits designte Systeme)
3. **Bugs fixen** (ohne Kern-Mechanik zu ändern)
4. **Dokumentation erweitern** (mehr Details, Beispiele)
5. **Performance optimieren** (ohne Verhalten zu ändern)

### ❌ DAS DARFST DU NICHT:
1. **Kernsysteme ändern** (PvP, Slime, Hardcore/Softy, etc.)
2. **Najika's Persönlichkeit ändern** (Megumin+Shiro bleibt!)
3. **"Alles weg"-Regel aufweichen** (keine Protection!)
4. **Slime-Farben ändern** (8 Farben sind fix!)
5. **Explosion-Klasse kombinierbar machen** (bleibt isoliert!)

### 🤔 WENN UNSICHER:
1. **Lies ALLE Dateien in `/DOCS/design/`**
2. **Check Git-History** (was wurde festgelegt?)
3. **Frage im Commit-Message nach** (dokumentiere Unklarheiten)
4. **Im Zweifel: FRAG DEN USER!**

---

## 15. DOKUMENTATIONS-HIERARCHIE

### Autorität (von oben nach unten)
```
1. DIESE DATEI (KANONISCHE_BASIS.md)
   ↓
2. /DOCS/design/*.md (Design-Dokumente)
   ↓
3. /info material/najika_ultimate_complete/05_chat_verlaeufe/111
   ↓
4. Git Commit History
   ↓
5. Andere Chat-Verläufe
```

**Bei Konflikt:** Höhere Quelle gewinnt!

---

## 16. CHANGELOG (NUR KERN-ÄNDERUNGEN)

### 2025-11-06: Initial Basis
- PvP-System finalisiert (3 Modi, Mercy, Double-Confirmation)
- Slime-System komplett (8 Farben, Level 50 Metamorphose, Rettung)
- Najika Plünderungs-Easter-Egg definiert
- Hardcore/Softy Modi fixiert
- Explosion-Klasse als isoliert definiert

**Hinzufügen erlaubt, Ändern verboten!**

---

## ZUSAMMENFASSUNG FÜR NEUE CLAUDE-INSTANZEN

**Lies das:**
1. Diese Datei (KANONISCHE_BASIS.md)
2. `/DOCS/design/PVP_SYSTEM_COMPLETE.md`
3. `/DOCS/design/SLIME_COMPANION_SYSTEM.md`
4. `/DOCS/design/ARENA_MERCY_SYSTEM.md`

**Dann:**
- ✅ Implementiere fehlende Systeme
- ✅ Füge NEUE Features hinzu (wenn kompatibel)
- ❌ Ändere NICHTS an bestehenden Kern-Mechaniken

**Bei Fragen:**
- Git-History checken
- User fragen
- Im Zweifel: NICHT ändern!

---

**Ende Kanonische Basis**

*Diese Regeln sind FINAL. Änderungen nur durch explizite User-Anweisung!*
