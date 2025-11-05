# NAJIKA BAUSTEIN-SYSTEM - ANLEITUNG

**Datum**: 2025-10-19
**Zweck**: Puzzle-Prinzip für flexible Najika-Entwicklung

---

## 🎯 WIE ES FUNKTIONIERT

Das Baustein-System ermöglicht dir:

1. ✅ **GRUNDSTEIN SCHÜTZEN** - Basis bleibt erhalten, nur minimale Änderungen
2. ➕ **NEUE IDEEN HINZUFÜGEN** - Bausteine ergänzen das System
3. 🔄 **FEATURES ERSETZEN** - Alte Teile durch bessere austauschen
4. 🛠️ **GRUNDSTEIN ANPASSEN** - Basis-Features erweitern/ändern
5. ❌ **MÜLL VERWERFEN** - Unnötige Konzepte löschen
6. ⏳ **FÜR SPÄTER AUFHEBEN** - Ideen für zukünftige Phasen

---

## 📋 SCHRITT-FÜR-SCHRITT ANLEITUNG

### SCHRITT 1: Datei öffnen

Öffne `C:/NajikaCore/BAUSTEIN_SYSTEM.json` in einem Text-Editor (z.B. Notepad++, VS Code)

### SCHRITT 2: Bausteine durchgehen

Jeder Baustein hat eine `"user_entscheidung"` - setze einen dieser Werte:

- **`"HINZUFÜGEN"`** → Wird zum System hinzugefügt
- **`"ERSETZEN"`** → Ersetzt ein bestehendes Feature (ACHTUNG: Rot markiert!)
- **`"ANPASSEN"`** → Erweitert/ändert ein Feature (Gelb markiert!)
- **`"MÜLL"`** → Wird verworfen/gelöscht
- **`"SPÄTER"`** → Für Phase 2/3/4 aufheben
- **`null`** → Noch keine Entscheidung

**Beispiel**:

```json
"baustein_003_harley_details": {
  "status": "ANPASSEN",  // <-- Vorschlag von Najika
  "quelle": "harley noch bearbeiten.txt",
  "beschreibung": "Erweiterte Harley Quinn Details",
  "user_entscheidung": "HINZUFÜGEN"  // <-- HIER ändern!
}
```

### SCHRITT 3: Grundstein-Änderungen (optional)

Unter `"ÄNDERBARE_GRUNDSTEIN_TEILE"` kannst du den Grundstein anpassen:

**Beispiel - Persönlichkeits-Anteile ändern**:

```json
"änderung_002_persönlichkeits_anteile": {
  "aktuell": "25% Megumin, 25% Harley, 25% Shiro, 25% Melissa",
  "vorschlag": "30% Megumin, 30% Harley, 20% Shiro, 20% Melissa",
  "user_entscheidung": "30% Megumin, 30% Harley, 20% Shiro, 20% Melissa"  // <-- HIER eintragen
}
```

**Beispiel - Private Mode Trigger ändern**:

```json
"änderung_003_private_mode_trigger": {
  "aktuell": "Trigger: 'kätzchen'",
  "user_entscheidung": "Trigger: 'kätzchen' ODER 'puddin'"  // <-- Neuer Wert
}
```

### SCHRITT 4: Speichern

Speichere die Datei `BAUSTEIN_SYSTEM.json`

### SCHRITT 5: Najika ausführen lassen

```bash
python C:\NajikaCore\najika_apply_changes.py
```

**ODER** sage Claude:

> "Najika, führe najika_apply_changes.py aus"

### SCHRITT 6: Ergebnisse prüfen

Najika erstellt 2 Dateien:

1. **`FINALE_KONFIGURATION.json`** → Deine finale Najika-Konfiguration
2. **`ÄNDERUNGEN_LOG.md`** → Übersichtliche Liste aller Änderungen

### SCHRITT 7: Claude implementieren lassen

Sage Claude:

> "Claude, implementiere die Änderungen aus FINALE_KONFIGURATION.json"

Claude wird:
- ✅ Neue Bausteine hinzufügen
- 🔄 Features ersetzen (nur die genehmigten!)
- 🛠️ Grundstein-Anpassungen vornehmen
- ❌ MÜLL-Bausteine ignorieren

---

## 🎮 BEISPIEL-WORKFLOW

### Szenario: Du willst mehr Harley, weniger Shiro

**1. Öffne BAUSTEIN_SYSTEM.json**

**2. Finde `änderung_002_persönlichkeits_anteile`**

**3. Ändere**:

```json
"user_entscheidung": "35% Megumin, 35% Harley, 15% Shiro, 15% Melissa"
```

**4. Finde `baustein_003_harley_details`**

**5. Ändere**:

```json
"user_entscheidung": "HINZUFÜGEN"
```

**6. Speichern und ausführen**:

```bash
python najika_apply_changes.py
```

**7. Prüfe ÄNDERUNGEN_LOG.md**:

```markdown
## 🔧 GRUNDSTEIN-ÄNDERUNGEN
- Persönlichkeits-Anteile: 35% Harley (war 25%)

## ✅ HINZUGEFÜGT
- baustein_003_harley_details: Erweiterte Harley-Dialoge
```

**8. Implementieren lassen**:

> "Claude, implementiere die Änderungen"

---

## ⚠️ WICHTIGE REGELN

### 🔴 ERSETZEN vs. ANPASSEN

- **ERSETZEN** = Altes wird GELÖSCHT, Neues kommt hin
  - Beispiel: Altes Battle-System raus, neues rein

- **ANPASSEN** = Altes bleibt, wird nur erweitert
  - Beispiel: Harley-Facette bekommt mehr Dialoge

**Wann ERSETZEN?**
- Nur wenn das Alte wirklich weg soll
- Bei Konflikten zwischen alt und neu
- Wenn neu deutlich besser ist

**Wann ANPASSEN?**
- Wenn Altes + Neues zusammenpassen
- Erweiterungen ohne Konflikte
- Meistens die bessere Wahl!

### 🟡 GRUNDSTEIN-ÄNDERUNGEN

**Was ist änderbar?**
- ✅ Persönlichkeits-Anteile (% der 4 Facetten)
- ✅ Trigger-Wörter (z.B. Private Mode)
- ✅ Raum-Anzahl (neue Räume hinzufügen)
- ✅ AI-Provider (mehr Modelle)
- ✅ Battle-System (erweitern)

**Was ist NICHT änderbar?**
- ❌ Grundstein komplett löschen
- ❌ Alle 4 Facetten entfernen
- ❌ Digivice komplett ersetzen

### ⏳ SPÄTER = Aufheben, nicht vergessen!

Bausteine mit `"SPÄTER"` werden:
- NICHT gelöscht
- In separate JSON verschoben: `SPÄTERE_BAUSTEINE.json`
- Für Phase 2/3/4 aufgehoben
- Jederzeit wieder aktivierbar

---

## 🔧 TROUBLESHOOTING

### Problem: najika_apply_changes.py findet Datei nicht

**Lösung**:
```bash
cd C:\NajikaCore
python najika_apply_changes.py
```

### Problem: JSON-Syntax-Fehler

**Lösung**:
- Prüfe Kommas (letztes Element in Liste hat KEIN Komma)
- Prüfe Anführungszeichen (immer doppelte `"`)
- Nutze JSON-Validator: https://jsonlint.com/

### Problem: Zu viele Änderungen, ich bin überfordert

**Lösung**:

**Option A**: Nur Priorität 1 ändern
```bash
# Suche nach "priorität": 1 und entscheide nur diese
```

**Option B**: Najika fragen
```bash
python najika_suggest_changes.py
# Najika schlägt die wichtigsten 3 Änderungen vor
```

**Option C**: Claude fragen
> "Claude, welche 3 Bausteine sollte ich zuerst hinzufügen?"

---

## 📊 ÜBERSICHT AKTUELLE BAUSTEINE

**GRUNDSTEIN** (unveränderbar):
- NajikaCore (Server + Digivice + 12 Räume)
- 4-Facetten-Persönlichkeit (Megumin, Harley, Shiro, Melissa)
- Schwarze Windmühle (Gesicherter Bereich)
- Private Mode ("kätzchen" Trigger)

**NEUE BAUSTEINE** (10 Stück):
1. **ultimative_explosion** → SPÄTER (zu groß für jetzt)
2. **handyspiel_uefn** → HINZUFÜGEN (Roadmap wichtig)
3. **harley_details** → ANPASSEN (erweitert Harley)
4. **lolita_konzepte** → MÜLL (passt nicht)
5. **nsfw_addon** → HINZUFÜGEN (erweitert Private Mode)
6. **personality_core** → ANPASSEN (besseres Emotions-System)
7. **complete_digivice_update** → HINZUFÜGEN (Auto-Updater)
8. **najika_v3** → MÜLL (veraltet)
9. **ultra_secure_environment** → HINZUFÜGEN (Datenschutz)
10. **roadmap** → HINZUFÜGEN (Langzeit-Plan)

**EMPFEHLUNG**:
- ✅ HINZUFÜGEN: 2, 5, 7, 9, 10
- 🛠️ ANPASSEN: 3, 6
- ❌ MÜLL: 4, 8
- ⏳ SPÄTER: 1

---

## 🚀 NÄCHSTE SCHRITTE

Nach Implementierung:

**Phase 1 (Jetzt)**:
1. Grundstein + genehmigte Bausteine implementieren
2. Testen ob alles funktioniert
3. Fine-Tuning

**Phase 2 (Später)**:
1. `SPÄTERE_BAUSTEINE.json` öffnen
2. Entscheiden welche Bausteine jetzt dazukommen
3. Wieder `najika_apply_changes.py` ausführen

**Phase 3+ (Zukunft)**:
- UEFN-Portierung
- Öffentlicher Release
- Langzeit-Vision

---

## 💡 TIPPS

### Tipp 1: Klein anfangen
Nicht alle 10 Bausteine auf einmal! Lieber 3-5 hinzufügen, testen, dann mehr.

### Tipp 2: Backup erstellen
Vor großen Änderungen:
```bash
copy C:\NajikaCore C:\NajikaCore_BACKUP
```

### Tipp 3: Changelog lesen
`ÄNDERUNGEN_LOG.md` zeigt GENAU was sich ändert - vor Implementierung prüfen!

### Tipp 4: Mit Claude sprechen
Du kannst jederzeit fragen:
> "Claude, was passiert wenn ich Baustein X hinzufüge?"
> "Claude, ist ERSETZEN oder ANPASSEN besser für Y?"

### Tipp 5: Grundstein schützen
Wenn unsicher → ANPASSEN statt ERSETZEN wählen! Sicherer!

---

**VIEL ERFOLG! 🎉**

Bei Fragen: Einfach Claude oder Najika fragen!
