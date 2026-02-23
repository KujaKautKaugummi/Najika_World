# HOUSING & FARMING SYSTEM STATUS 2026-02-15

**Überprüft von:** SONNET
**Status:** ✅ **BEIDE SYSTEME IMPLEMENTIERT!**

---

## ✅ HOUSING-SYSTEM (KOMPLETT)

**Datei:** `backend/api/housing.py`

### Implementierte Features:
- ✅ **Haus-Level System** (Level 1-10+)
- ✅ **Furniture Placement** (Möbel platzieren)
- ✅ **Furniture Removal** (Möbel entfernen)
- ✅ **Upgrade-System** (Haus upgraden)
- ✅ **Max-Furniture Scaling** (20 + Level*5 = bis 70 Möbel)

### Endpoints:
```
GET  /api/housing/house/{player_id}     - Haus-Daten abrufen
POST /api/housing/furniture/place       - Möbel platzieren
POST /api/housing/furniture/remove      - Möbel entfernen
POST /api/housing/house/upgrade         - Haus upgraden
```

### Datenbank-Modell:
```python
class PlayerHouse:
    id: int
    owner_id: int
    furniture: List[dict]        # JSON Array mit Möbeln
    decorations: List[dict]      # JSON Array mit Deko
    level: int                   # Haus-Level
    max_furniture: int           # Max Möbel-Anzahl
    upgraded_at: datetime        # Letztes Upgrade
```

---

## ✅ FARMING-SYSTEM (KOMPLETT)

**Datei:** `backend/api/farming.py`

### Implementierte Features:
- ✅ **Farm-Plots** (4 Felder pro Spieler)
- ✅ **Crop Planting** (Pflanzen säen)
- ✅ **Crop Harvesting** (Ernten)
- ✅ **Growth-Stages** (Wachstumsphasen)
- ✅ **Watering System** (Bewässerung)
- ✅ **Fishing System** (Angeln als Bonus!)

### Endpoints:
```
GET  /api/farming/plots/{player_id}     - Farm-Plots abrufen
POST /api/farming/plant                 - Pflanzen säen
POST /api/farming/harvest               - Ernten
POST /api/farming/water                 - Bewässern
POST /api/farming/fish                  - Angeln
```

### Datenbank-Modell:
```python
class FarmPlot:
    id: int
    owner_id: int
    plot_index: int              # 0-3 (4 Felder)
    crop_type: str               # z.B. "wheat", "tomato"
    growth_stage: int            # 0-100%
    ready_to_harvest: bool
    planted_at: datetime
    watered_at: datetime
```

---

## ⚠️ WAS FEHLT (FÜR M&B2 FEATURES)

### 1. NPC-Servants (geplant im M&B2 Doc):
- ❌ **Butler/Maid einstellen**
- ❌ **Koch für Haus**
- ❌ **Gärtner (automatische Farm-Bewässerung)**
- ❌ **Wachen für Haus**

**Lösung:**
→ Neues System: `backend/api/lebensraum.py` erweitern
→ NPC-Recruitment wie in M&B2 Features-Doc beschrieben

### 2. Haus-Tiers (aktuell nur Level 1-10):
- ❌ **Tier-System fehlt** (Small Hütte → Medium Haus → Large Anwesen → Festung)
- ✅ **Level-System existiert** (kann dafür genutzt werden!)

**Lösung:**
→ Level 1-10 = Tier 1 (Small Hütte)
→ Level 11-20 = Tier 2 (Medium Haus)
→ Level 21-30 = Tier 3 (Large Anwesen)
→ Level 31+ = Tier 4 (Festung)

### 3. Farm-Upgrades:
- ❌ **Mehr als 4 Felder** (aktuell fix 4)
- ❌ **Tiergehege** (Monster/Tiere züchten)
- ❌ **Bewässerungs-System** (automatisch)

**Lösung:**
→ Farm-Expansion durch Housing-Level
→ Level 10+ = 8 Felder
→ Level 20+ = 12 Felder + Tiergehege
→ Level 30+ = Auto-Bewässerung

### 4. Lebensraum-NPCs & Monster:
- ❌ **NPC-Arbeiter** (Schmied, Alchemist, Koch)
- ❌ **Monster-Rekrutierung** (Slimes, Wölfe als Wachen)
- ❌ **Trupp-Management** (nur in Lebensraum!)

**Lösung:**
→ Siehe `MOUNT_BLADE_FEATURES_IMPLEMENTATION_2026-02-15.md`
→ Neues System: `backend/systems/recruitment.py`

---

## 📋 NÄCHSTE SCHRITTE

### P0 - SOFORT (SONNET):
1. ✅ Housing-Tiers definieren (Level → Tier Mapping)
2. ✅ Farm-Expansion-System (mehr Felder bei höherem Level)

### P1 - DIESE WOCHE (SONNET + OPUS):
3. ⬜ NPC-Recruitment-System (Backend: SONNET)
4. ⬜ Lebensraum-Management-UI (Frontend: OPUS)
5. ⬜ Monster-Fangen-System erweitern (für Lebensraum-Zuordnung)

### P2 - SPÄTER (OPUS):
6. ⬜ Tiergehege-System (Design + Content)
7. ⬜ Trupp-Management-UI (nur Lebensraum!)
8. ⬜ Mass-Battle-System (optional, sehr komplex)

---

## 💡 DESIGN-EMPFEHLUNGEN

### Housing-Tier-System:
```yaml
tier_1_kleine_huette:
  level_range: 1-10
  max_furniture: 20-70
  features:
    - "1 Raum"
    - "Kleiner Garten"
    - "4 Farm-Plots"
  max_npcs: 0
  cost_per_level: 1000 Münzen

tier_2_bauernhof:
  level_range: 11-20
  max_furniture: 75-120
  features:
    - "3 Räume (Wohn, Küche, Lager)"
    - "Großer Garten"
    - "8 Farm-Plots"
    - "Kleiner Stall"
  max_npcs: 3  # 1 Koch, 1 Gärtner, 1 Arbeiter
  cost_per_level: 5000 Münzen
  upgrade_cost: 10000 Münzen (Level 10 → 11)

tier_3_anwesen:
  level_range: 21-30
  max_furniture: 125-170
  features:
    - "8 Räume"
    - "Schmiede, Alchemie-Labor"
    - "12 Farm-Plots + Auto-Bewässerung"
    - "Großer Stall (10 Tiere/Monster)"
  max_npcs: 8  # Schmied, Alchemist, 2 Gärtner, 2 Wachen, Koch, Butler
  cost_per_level: 10000 Münzen
  upgrade_cost: 50000 Münzen (Level 20 → 21)

tier_4_festung:
  level_range: 31-50
  max_furniture: 175-270
  features:
    - "20+ Räume"
    - "Mauern, Türme"
    - "20 Farm-Plots"
    - "Riesiger Stall (30 Tiere/Monster)"
    - "Trainingsplatz (für Mass-Battles)"
    - "Kaserne (NPC-Truppen)"
  max_npcs: 20
  max_monsters: 30
  cost_per_level: 25000 Münzen
  upgrade_cost: 200000 Münzen (Level 30 → 31)
  unlock_requirement: "Quest 'Lord der Lande'"
```

---

**Status:** Basis-Systeme existieren ✅, Erweiterungen geplant ⬜
