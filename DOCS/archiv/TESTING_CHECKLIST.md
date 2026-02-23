# 🧪 NAJIKA WORLD - TESTING CHECKLIST

## Quick Test (OHNE Backend)

### 1. Start Game
```bash
START_NAJIKA_GAME.bat
```

### 2. Open World Map (UNIFIED)
✅ **URL:** http://localhost:5173/najika_world_UNIFIED.html

**Erwartungen:**
- [ ] Map lädt ohne Fehler
- [ ] Character spawnt bei (0, 55, 0) auf Berg
- [ ] 9 farbige Regionen sichtbar
- [ ] Lila Marker bei y=300 (Mühle)
- [ ] Console: "✅ Schwarze Windmühle auf Berg-Gipfel platziert!"
- [ ] Status oben rechts: "Backend Offline" (roter Punkt) = OK!

### 3. Movement Test
- [ ] **W** - Vorwärts läuft
- [ ] **A/D** - Seitlich läuft
- [ ] **S** - Rückwärts läuft
- [ ] **Shift+W** - Sprint (spürbar schneller)
- [ ] Speed fühlt sich "normal" an (~6-9 m/s)
- [ ] NICHT zu schnell (keine 100 km/h!)

### 4. Schwarze Mühle Test
**Zum Berg laufen (Center bei 0,0):**
- [ ] Mühle ist sichtbar (großes schwarzes Gebäude)
- [ ] Lila Marker pulsiert über der Mühle
- [ ] Bei Annäherung: "Schwarze Windmühle betreten" erscheint
- [ ] **E** drücken → Neues Fenster öffnet sich
- [ ] **URL:** http://localhost:5173/index.html (Digivice)

### 5. Digivice (Mühle Interior) Test
**Im neuen Fenster:**
- [ ] Lädt ohne 404-Fehler in Console (F12 prüfen!)
- [ ] 12 Raum-Buttons sichtbar
- [ ] Status: "Offline" (roter Punkt) = OK ohne Backend!
- [ ] Keine fehlenden JS-Dateien
- [ ] CSS lädt korrekt

**Test Raum-Wechsel (OHNE Backend funktioniert nur teilweise):**
- [ ] Wohnzimmer Button funktioniert
- [ ] 3D-Scene lädt (oder Fallback)
- [ ] Raum-Wechsel möglich

### 6. Stadt Test
**Zu einer Stadt laufen:**
- Positionen siehe START_NAJIKA_WORLD_GUIDE.md
- [ ] Stadt-Marker sichtbar (farbige Kugeln bei +150m)
- [ ] Bei Annäherung: "[Stadt-Name] betreten" erscheint
- [ ] **E** drücken → Interior lädt (vereinfacht, ohne NPCs)

### 7. Combat Test
**Enemy finden (laufe durch Regionen):**
- [ ] Enemies spawnen (~30-45 total)
- [ ] Verteilt über ±1500m pro Region
- [ ] Bei Annäherung: Combat startet automatisch
- [ ] Combat UI erscheint (HP, Stamina, Cheer)
- [ ] **Tab** wechselt Mode (MANUAL/ASSIST/AUTO)

**MANUAL Mode:**
- [ ] **Q** - Linke Hand Attack
- [ ] **E** - Rechte Hand Attack
- [ ] **Space** - Both Hands
- [ ] **C** - Dodge
- [ ] **X** - Block
- [ ] **V** - Parry

---

## Full Test (MIT Backend)

### Backend starten:
```bash
cd backend
python najika_server.py
```

**Erwartungen:**
- [ ] Server startet auf Port 8000
- [ ] Console zeigt "✅ Coqui TTS aktiviert" (oder Fallback)
- [ ] Keine Fehler beim Start

### Im Game (nach Backend Start):
- [ ] Status oben rechts: "Backend Online" (grüner Punkt)
- [ ] Najika Stats werden geladen (Hunger, Energy, Happiness)
- [ ] Alle Werte > 0

### Digivice mit Backend:
- [ ] Chat funktioniert (Najika antwortet)
- [ ] Teleport-Buttons funktionieren
- [ ] Raum-Wechsel mit Effekten
- [ ] Status-Updates in Echtzeit
- [ ] Combat-Log synchronisiert

---

## Performance Test

### FPS Check:
- [ ] Open World: 30+ FPS
- [ ] Digivice: 60 FPS
- [ ] Combat: 30+ FPS
- [ ] Keine Freezes beim Raum-Wechsel

### Map Size Validation:
**Console (F12) sollte zeigen:**
```
regionSize = 3200
Grid: 9600
```

**Manuelle Prüfung:**
- [ ] Von Berg zu Desert: ~3200m
- [ ] Laufzeit: ~5-7 Minuten @ 6 m/s
- [ ] Diagonal über Map: ~30+ Minuten

---

## Bug Checks

### Bekannte Fixed Issues:
- [x] Mühle unsichtbar → FIXED (Scale 25×)
- [x] Mühle nicht betretbar → FIXED (150m Radius)
- [x] Character zu groß → FIXED (1.35m)
- [x] Movement zu schnell → FIXED (6-9 m/s)
- [x] Städte falsch positioniert → FIXED (±3200m)
- [x] Digivice 404 Errors → FIXED (Pfade korrigiert)
- [x] Backend auf 5173 → FIXED (Port 8000)

### Neue Bugs zu testen:
- [ ] Enemies spawnen außerhalb der Map?
- [ ] Character fällt durch Boden?
- [ ] Combat bricht ab?
- [ ] Raum-Wechsel friert ein?
- [ ] Teleport funktioniert nicht?

---

## Console Errors zu ignorieren (OHNE Backend):

```
❌ NORMAL (Backend Offline):
- 404: /api/najika/status
- 404: /api/chat/...
- 404: /api/room/teleport
- Error: Backend nicht erreichbar
```

```
✅ NICHT NORMAL (Bug!):
- 404: /js/...
- 404: /static/js/...
- 404: /css/...
- TypeError: ... is not a function
- Three.js errors
```

---

## Success Criteria

### Minimum (OHNE Backend):
- [x] Map lädt und ist begehbar
- [x] Mühle ist sichtbar und betretbar
- [x] Digivice öffnet ohne 404s
- [x] Raum-Wechsel funktioniert (Basic)
- [x] Combat funktioniert
- [x] Performance OK (30+ FPS)

### Full (MIT Backend):
- [ ] Najika Chat antwortet
- [ ] Teleport funktioniert
- [ ] Stats synchronisieren
- [ ] Combat-Log funktioniert
- [ ] Voice (falls TTS installiert)

---

## Nächste Schritte nach Testing:

### Falls alles funktioniert:
1. **Phase 2:** Terrain Variation (Berge, Täler)
2. **NPCs:** JSON-Daten einbinden (36 Dateien)
3. **Quests:** Quest-System aktivieren
4. **Multiplayer:** Fishing/Farming integrieren

### Falls Bugs:
1. Console (F12) → Fehler kopieren
2. Screenshot machen
3. Bug beschreiben
4. Ich fixe es! 🔧

---

**Viel Erfolg beim Testing! 🎮**
