# NAJIKA MAGIC SYSTEM - VOLLSTÄNDIG IMPLEMENTIERT

**Erstellt:** 2025-11-05
**Status:** ✅ FERTIG & GETESTET
**Dateien:**
- `backend/game/magic_system.py` (Kern-System)
- `backend/najika_server.py` (API-Integration)

---

## 🎯 ÜBERSICHT

Das Magic System implementiert:
1. ✅ **9 Magieschulen** mit je 5 Stufen (45 Zauber total)
2. ✅ **Skill-Weaving** (Element-Kombos)
3. ✅ **Explosion Magic** (3 Level, Level 3 nur für Najika)
4. ✅ **Use-Based Progression** (Skyrim-Style)

---

## 🔮 9 MAGIESCHULEN

### 1. FEUER (Damage Over Time)
**Identität:** Brennender Schaden über Zeit

| Stufe | Name | Schaden | MP | Special |
|-------|------|---------|-----|---------|
| 1 | Feuer | 12 | 8 | +2 DMG/Runde (3 Runden) |
| 2 | Feura | 25 | 15 | +4 DMG/Runde (3 Runden) |
| 3 | Feuga | 40 | 25 | +6 DMG/Runde (4 Runden) |
| 4 | Inferno | 70 | 40 | AOE + 10 DMG/Runde |
| 5 | Omega-Detonation | 150 | 80 | AOE + 20 DMG/Runde |

### 2. EIS (Crowd Control)
**Identität:** Einfrieren & Verlangsamung

| Stufe | Name | Schaden | MP | Special |
|-------|------|---------|-----|---------|
| 1 | Eis | 10 | 8 | 20% Freeze |
| 2 | Blizzara | 22 | 15 | 30% Freeze + Slow |
| 3 | Blizzaga | 38 | 25 | AOE + 40% Freeze |
| 4 | Eiserne Kälte | 65 | 40 | AOE + 60% Freeze |
| 5 | Ewiges Eis | 120 | 80 | AOE + 100% Freeze (3 Runden) |

### 3. BLITZ (Burst Damage)
**Identität:** Hoher Sofortschaden + Ketteneffekt

| Stufe | Name | Schaden | MP | Special |
|-------|------|---------|-----|---------|
| 1 | Blitz | 15 | 10 | 15% Stun |
| 2 | Thundara | 30 | 18 | Springt auf 2 Ziele |
| 3 | Thundaga | 50 | 30 | Springt auf 3 Ziele |
| 4 | Donnerschlag | 85 | 45 | AOE + 50% Stun |
| 5 | Göttlicher Zorn | 180 | 90 | AOE + 80% Stun |

### 4. ERDE (Defense)
**Identität:** Verteidigung + Schutzschild

| Stufe | Name | Schaden | MP | Special |
|-------|------|---------|-----|---------|
| 1 | Steinwurf | 8 | 6 | +2 DEF (2 Runden) |
| 2 | Felsschlag | 18 | 12 | +4 DEF |
| 3 | Erdbeben | 32 | 22 | AOE + Slow |
| 4 | Steinwall | 45 | 35 | +10 DEF + 50 Shield |
| 5 | Titan-Zorn | 100 | 70 | AOE + 15 DEF + 100 Shield |

### 5. WIND (Mobility)
**Identität:** Multi-Hit + Knockback

| Stufe | Name | Schaden | MP | Special |
|-------|------|---------|-----|---------|
| 1 | Windklinge | 11 | 7 | Knockback |
| 2 | Sturmschnitt | 24 | 14 | 3× Hits |
| 3 | Tornado | 36 | 24 | AOE + Knockback |
| 4 | Orkan | 68 | 38 | AOE + 2× Hits |
| 5 | Göttlicher Wind | 140 | 75 | AOE + 3× Hits |

### 6. WASSER (Support/Heilung)
**Identität:** Heilung + Regeneration

| Stufe | Name | Heilung | MP | Special |
|-------|------|---------|-----|---------|
| 1 | Wasser | 20 | 10 | - |
| 2 | Heilwasser | 40 | 18 | Entfernt Status |
| 3 | Heilflut | 70 | 30 | AOE Heilung |
| 4 | Lebensquelle | 100 | 45 | AOE + 10 HP/Runde (3 Runden) |
| 5 | Göttliches Wasser | 200 | 80 | AOE + 20 HP/Runde + Wiederbelebung |

### 7. LICHT (Holy)
**Identität:** Bonus vs Untote + Blind

| Stufe | Name | Schaden | MP | Special |
|-------|------|---------|-----|---------|
| 1 | Heiliges Licht | 13 | 9 | 2× vs Untote |
| 2 | Lichtlanze | 28 | 17 | 2.5× vs Untote + 30% Blind |
| 3 | Lichtsäule | 42 | 28 | AOE + 3× vs Untote |
| 4 | Heilige Nova | 75 | 42 | AOE + 3.5× vs Untote + 60% Blind |
| 5 | Göttliches Gericht | 160 | 85 | AOE + 4× vs Untote + Garantiertes Blind |

### 8. SCHATTEN (Debuff)
**Identität:** Verteidigung senken + Lifesteal

| Stufe | Name | Schaden | MP | Special |
|-------|------|---------|-----|---------|
| 1 | Schattenklinge | 14 | 9 | -2 DEF |
| 2 | Dunkler Bolzen | 26 | 16 | -4 DEF + 30% Lifesteal |
| 3 | Schattensturm | 44 | 27 | AOE + -6 DEF |
| 4 | Dunkle Sphäre | 78 | 43 | AOE + -10 DEF + 50% Lifesteal |
| 5 | Ewige Dunkelheit | 170 | 88 | AOE + -20 DEF + 80% Lifesteal |

### 9. PSYCHO (Mind Control)
**Identität:** Verwirrung + Gedankenkontrolle

| Stufe | Name | Schaden | MP | Special |
|-------|------|---------|-----|---------|
| 1 | Gedankenklinge | 12 | 10 | 15% Verwirrung |
| 2 | Psycho-Schock | 27 | 19 | 25% Verwirrung |
| 3 | Gedankensturm | 40 | 29 | AOE + 30% Verwirrung |
| 4 | Gedankenkontrolle | 72 | 44 | AOE + 50% Verwirrung + 20% Kontrolle |
| 5 | Göttlicher Wille | 165 | 87 | AOE + 80% Verwirrung + 40% Kontrolle |

---

## 💥 EXPLOSION MAGIC (MEGUMIN-STYLE)

### Level 1: Kleine Explosion
- **Schaden:** 200 AOE
- **MP-Kosten:** 100
- **Erschöpfung:** Mittel
- **Lernbar:** ✅ Ja (von Najika)
- **Quest-basiert:** Spieler müssen Najika überzeugen

### Level 2: Große Explosion
- **Schaden:** 400 Large AOE
- **MP-Kosten:** 150
- **Erschöpfung:** Schwer
- **Lernbar:** ✅ Ja (von Najika)

### Level 3: ULTIMATIVE EXPLOSION
- **Schaden:** 999 Massive AOE
- **MP-Kosten:** 200
- **Erschöpfung:** Total (komplett erschöpft, muss getragen werden)
- **Lernbar:** ❌ **NUR NAJIKA!**
- **Special:** **Zerstört die prozedural generierte Spielwelt!**
- **Story-Event:** Nur in Crimson Ruins (Gebiet 6)

---

## 🌀 SKILL-WEAVING (ELEMENT-KOMBOS)

**Mechanik:**
1. Lade Element in **linke Hand** (LH)
2. Lade Element in **rechte Hand** (RH)
3. Führe **Weave** aus → Combo-Zauber!

### Verfügbare Kombos

| Element 1 | Element 2 | Combo-Name | Schaden | MP | Effekt |
|-----------|-----------|------------|---------|-----|--------|
| Feuer | Eis | **Thermoschock** | 80 | 35 | Shatter (zerbricht gefrorene Gegner) |
| Feuer | Wind | **Feuerklinge** | 70 | 30 | 3× Multi-Hit |
| Feuer | Erde | **Magma-Eruption** | 90 | 40 | AOE + Burn |
| Eis | Wasser | **Gefrierende Flut** | 65 | 32 | AOE + 60% Freeze |
| Eis | Wind | **Eissturm** | 75 | 35 | AOE + Slow |
| Blitz | Wasser | **Elektro-Schock** | 95 | 42 | AOE + 70% Stun |
| Blitz | Wind | **Gewittersturm** | 85 | 38 | Springt auf 5 Ziele |
| Licht | Feuer | **Heiliges Feuer** | 100 | 45 | AOE + 5× vs Untote |
| Licht | Wasser | **Reinigendes Licht** | 80 Heilung | 40 | AOE Heilung + Entfernt ALLE Status |
| Schatten | Feuer | **Höllenfeuer** | 110 | 48 | AOE + -15 DEF + Burn |
| Schatten | Psycho | **Alptraum** | 95 | 46 | 90% Verwirrung + Furcht |
| Psycho | Wind | **Gedankensturm** | 88 | 44 | AOE + 50% Kontrolle |
| Erde | Wasser | **Schlammlawine** | 70 | 35 | AOE + Slow + -8 DEF |

**Total:** 13 Kombos (weitere können hinzugefügt werden!)

---

## 📈 USE-BASED PROGRESSION (SKYRIM-STYLE)

**Mechanik:**
- Jeder Zauber hat einen **Skill-Level** (startet bei 1)
- Durch **Nutzung** des Zaubers → +10 XP
- Bei Level-Up:
  - **+2% Schaden** pro Level
  - **-1% MP-Kosten** pro Level
  - **+0.5% Crit-Chance** pro Level

### Beispiel-Progression:

| Level | Uses | XP to Next | Damage Bonus | MP Reduction | Crit Bonus |
|-------|------|------------|--------------|--------------|------------|
| 1 | 0 | 100 | +0% | -0% | +0% |
| 2 | 10 | 115 | +2% | -1% | +0.5% |
| 3 | 21 | 132 | +4% | -2% | +1.0% |
| 5 | 50 | 175 | +8% | -4% | +2.0% |
| 10 | 150 | 262 | +18% | -9% | +4.5% |
| 20 | 500 | 570 | +38% | -19% | +9.5% |

**XP-Kurve:** XP-Anforderung steigt um +15% pro Level

---

## 🔌 API-ENDPUNKTE

### 1. Zauber lernen
```http
POST /api/magic/learn
Content-Type: application/json

{
  "spell_id": "fire_1"
}
```

**Response:**
```json
{
  "ok": true,
  "msg": "Zauber gelernt: Feuer!",
  "spell": {
    "name": "Feuer",
    "school": "fire",
    "damage": 12,
    "mp_cost": 8
  }
}
```

### 2. Zauber wirken
```http
POST /api/magic/cast
Content-Type: application/json

{
  "spell_id": "fire_1",
  "target_hp": 100,
  "is_najika": true
}
```

**Response:**
```json
{
  "ok": true,
  "spell_name": "Feuer",
  "damage": 12,
  "mp_cost": 8,
  "effects": {
    "burn": {
      "damage": 2,
      "turns": 3
    }
  },
  "skill_progress": {
    "level": 1,
    "uses": 1,
    "xp": 10,
    "xp_to_next": 100,
    "damage_bonus": "+0.0%",
    "mp_reduction": "-0.0%",
    "crit_bonus": "+0.0%"
  }
}
```

### 3. Element in Hand laden
```http
POST /api/magic/weave/load
Content-Type: application/json

{
  "hand": "left",
  "element": "fire"
}
```

**Response:**
```json
{
  "ok": true,
  "msg": "Feuer-Magie in left Hand geladen!",
  "hands": {
    "left": "fire",
    "right": null
  }
}
```

### 4. Skill-Weaving ausführen
```http
POST /api/magic/weave/execute
```

**Response:**
```json
{
  "ok": true,
  "combo_name": "Thermoschock",
  "damage": 80,
  "mp_cost": 35,
  "description": "Feuer + Eis = Thermoschock - 80 DMG + Shatter",
  "effects": {
    "status": "shatter"
  },
  "hands_reset": true
}
```

### 5. Magic Stats abrufen
```http
GET /api/magic/stats
```

**Response:**
```json
{
  "known_spells": 5,
  "known_combos": 2,
  "total_casts": 47,
  "highest_skill_level": 3,
  "weaving_hands": {
    "left": null,
    "right": null
  },
  "skill_details": {
    "fire_1": {
      "level": 3,
      "uses": 25,
      "xp": 15,
      "xp_to_next": 132,
      "damage_bonus": "+4.0%",
      "mp_reduction": "-2.0%",
      "crit_bonus": "+1.0%"
    }
  }
}
```

### 6. Alle Zauber abrufen
```http
GET /api/magic/spells
```

**Response:**
```json
{
  "regular": {
    "fire_1": { "name": "Feuer", "damage": 12, ... },
    "ice_1": { "name": "Eis", "damage": 10, ... }
  },
  "explosion": {
    "explosion_1": { "name": "Explosion Stufe 1", "damage": 200, ... },
    "explosion_2": { "name": "Explosion Stufe 2", "damage": 400, ... },
    "explosion_3": { "name": "Explosion Stufe 3 - ULTIMATIV", "damage": 999, ... }
  },
  "known_spells": ["fire_1", "ice_1", "explosion_1"]
}
```

### 7. Alle Kombos abrufen
```http
GET /api/magic/combos
```

**Response:**
```json
{
  "combos": [
    {
      "elements": ["fire", "ice"],
      "name": "Thermoschock",
      "damage": 80,
      "mp_cost": 35,
      "description": "Feuer + Eis = Thermoschock - 80 DMG + Shatter"
    }
  ],
  "known_combos": 2,
  "total_available": 13
}
```

---

## 🧪 TEST-ERGEBNISSE

```
======================================================================
NAJIKA MAGIC SYSTEM TEST
======================================================================

=== USE-BASED PROGRESSION TEST ===
Cast #5: Feuer
  Skill Progress: {'level': 1, 'uses': 5, 'xp': 50, ...}
Cast #10: Feuer
  Skill Progress: {'level': 2, 'uses': 10, 'xp': 0, 'damage_bonus': '+2.0%', ...}

=== SKILL-WEAVING TEST ===
Combo: Thermoschock
Damage: 80
Description: Feuer + Eis = Thermoschock - 80 DMG + Shatter

=== EXPLOSION TEST ===
Spell: Explosion Stufe 3 - ULTIMATIV
Damage: 999
World Destroyed: True
Message: *** DIE WELT WURDE DURCH NAJIKA'S EXPLOSION ZERSTÖRT! ***

=== FINALE STATS ===
Known Spells: 5
Known Combos: 1
Total Casts: 16
Highest Skill Level: 2
======================================================================
```

**Status:** ✅ ALLE TESTS ERFOLGREICH!

---

## 📝 ZUSAMMENFASSUNG

### ✅ IMPLEMENTIERT:

1. **9 Magieschulen** - Je 5 Stufen (45 Zauber total)
2. **Skill-Weaving** - 13 Element-Kombos
3. **Explosion Magic** - 3 Level (Level 3 Najika-exklusiv)
4. **Use-Based Progression** - Skyrim-Style Skill-Verbesserung
5. **7 API-Endpunkte** - Vollständige REST-API
6. **Persistierung** - Gelernte Zauber werden gespeichert
7. **MP-Management** - Automatische MP-Reduktion
8. **Logging** - Alle Zauber-Aktionen werden geloggt

### 🎯 NÄCHSTE SCHRITTE:

1. Frontend-Integration (UI für Zauber-Auswahl)
2. Battle-System Integration (Zauber im Kampf nutzen)
3. Tutorial-System (Zauber lernen erklärt)
4. Visual Effects (Partikel für Zauber)
5. Sound Effects (Audio für Zauber)

---

**Ende der Dokumentation**
