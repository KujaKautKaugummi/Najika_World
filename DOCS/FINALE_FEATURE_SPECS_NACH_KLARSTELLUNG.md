# 📋 FINALE FEATURE SPECIFICATIONS - NACH KLARSTELLUNG

**Erstellt:** 2025-11-17
**Basis:** User Feedback zu Gap-Analyse & FastAPI Branch
**Status:** ✅ FINAL - Keine weiteren Änderungen ohne User-Approval

---

## 🎮 SLIME COMPANION SYSTEM

### Rettungs-Mechanik (FINAL)

**Softy Mode:**
- ✅ 1x pro Tag (24h Cooldown)
- ✅ Slime rettet dich vor Tod
- ✅ Slime bleibt kampffähig

**Normal Mode:**
- ✅ 1x pro Tag (24h Cooldown)
- ✅ Slime rettet dich vor Tod
- ✅ Slime wird geschwächt (50% Stats für 1h)

**Hardcore Mode (EXTREME!):**
- ✅ 1x verwendbar (PERMANENT!)
- ✅ Slime rettet dich vor PERMADEATH
- ❗ **Slime wird SEHR geschwächt:**
  - Kampfunfähig für 4-6 Wochen (Echtzeit!)
  - Braucht **Ritual-Ressourcen** zum Wiederbeleben:
    - Seltene Items farmen (jeden Tag!)
    - Oregon Trail Events für Ritual-Items
    - Boss-Drops erforderlich
- ✅ Nach Ritual: Slime ist wieder kampffähig

**Implementation:**
```python
# backend/services/slime_system.py

def use_rescue(companion_id: int, game_mode: str):
    companion = get_companion(companion_id)

    if game_mode == "softy":
        # Simple rescue
        companion.last_rescue = datetime.now()
        # 24h cooldown
        return {"rescued": True, "cooldown": "24h"}

    elif game_mode == "normal":
        # Rescue + weakened
        companion.last_rescue = datetime.now()
        companion.stats_multiplier = 0.5  # 50% Stats
        companion.weakness_until = datetime.now() + timedelta(hours=1)
        return {"rescued": True, "weakened": "1h"}

    elif game_mode == "hardcore":
        # PERMANENT rescue - Slime sacrifice
        if companion.has_rescued_before:
            return {"error": "Slime already used rescue!"}

        companion.has_rescued_before = True
        companion.is_combat_ready = False
        companion.revival_ritual_started = datetime.now()
        companion.revival_ritual_end = datetime.now() + timedelta(weeks=random.randint(4, 6))

        # Generate ritual requirements
        ritual_items = generate_ritual_items()
        companion.ritual_requirements = ritual_items

        return {
            "rescued": True,
            "slime_status": "combat_disabled",
            "ritual_duration_weeks": (companion.revival_ritual_end - datetime.now()).days / 7,
            "required_items": ritual_items
        }
```

---

## ⚔️ PvP SYSTEM

### Hardcore PvP (FINAL - Nicht zu brutal!)

**Winner bekommt:**
- ✅ Gesamtes Inventar des Losers
- ✅ Alle Digimon des Losers (außer Slime!)
- ✅ Alle Kleidung
- ✅ Alle Accessoires

**Loser verliert:**
- ✅ Alles oben genannte
- ❌ **ABER:** Slime bleibt IMMER beim Spieler!
- ✅ Character bleibt am Leben (kein Permadeath durch PvP!)

**Mercy System:**
```python
# Winner kann entscheiden:

if mercy_level == "no_mercy":
    # Loser bekommt nichts zurück

elif mercy_level == "partial_mercy":
    # Loser wählt 1-3 Items aus (Winner entscheidet wie viele)
    # z.B. Winner sagt: "Pick 2 items"

elif mercy_level == "full_mercy":
    # Loser bekommt alles zurück
    # Winner bekommt nur EXP + Honor Points
```

**Warum NICHT zu brutal:**
- Loser behält Slime (kann weiter spielen)
- Loser behält Character (kein Permadeath)
- Mercy System gibt Winner Option, fair zu sein
- Hardcore PvP ist **optional** (kann Normal/Softy wählen)

---

## 🎲 OREGON TRAIL EVENTS

### Balancing (FINAL)

**Event Difficulty Distribution:**
```python
EVENT_DISTRIBUTION = {
    "positive": 30%,    # Gute Events (Treasure, Healing, Buffs)
    "neutral": 40%,     # Skill Checks, Choices
    "negative": 20%,    # Verluste (Items, HP, Gold)
    "brutal": 10%       # Sehr hart (Death, Permadeath risk in Hardcore)
}
```

**Chaos System:**
```python
# Chaos 0-100
if chaos < 30:
    event_chance = 5%   # Niedrig

elif chaos < 60:
    event_chance = 10%  # Normal

elif chaos < 80:
    event_chance = 15%  # Hoch

else:  # chaos >= 80
    event_chance = 20%  # Sehr hoch
```

**Event Severity by Game Mode:**
```python
if game_mode == "softy":
    # Keine Permadeath Events
    # Max Loss: 10% Gold, 1 Item

elif game_mode == "normal":
    # Seltene Permadeath Events (1%)
    # Max Loss: 30% Gold, 3 Items

elif game_mode == "hardcore":
    # Permadeath Events möglich (5%)
    # Max Loss: 100% Gold, alle Items (bei schlimmsten Events)
```

**User Feedback Integration:**
```python
# Nach Beta-Test:
# User sagt: "Event X zu hart"
# → Wir passen an (Wahrscheinlichkeit runter oder Belohnung hoch)

# User sagt: "Event Y zu einfach"
# → Wir passen an (Belohnung runter oder Difficulty hoch)
```

---

## 🥊 NEMESIS ARENA & FINISHERS

### Finisher System (FINAL)

**Alle Versionen (Private + Public + Fortnite):**
- ✅ Alle 134 Finisher verfügbar
- ✅ 16 Kategorien: Elemental, Weapon, Martial Arts, Magic, Brutal, Comedic, etc.
- ✅ Brutal Finisher = Game Content (wie Mortal Kombat)
- ✅ Visuals angepasst an Plattform

**Kuja's APK (Private):**
- ✅ Alle 134 Finisher
- ✅ Volle Gore-Level (Blut, Impact Effects)
- ✅ Keine Zensur

**Offizielle APK (Public):**
- ✅ Alle 134 Finisher
- ✅ Reduzierter Gore-Level (weniger Blut)
- ✅ Mehr stylized Effects (wie Fortnite)

**Fortnite/UEFN Port:**
- ✅ Alle 134 Finisher
- ✅ KEIN Gore, KEIN Blut
- ✅ Nur stylized Effects (Particles, Lights)
- ✅ PG-13 konform

**WICHTIG:**
- Finisher haben NICHTS mit NSFW zu tun!
- Finisher = Game Mechanic (Combat)
- NSFW = Separate Features (Najika Persönlichkeit, Private Mode)

---

## 🎓 MAGIC SCHOOLS SYSTEM

### Skill Trees (FINAL - Skyrim-Style)

**Inspiration:**
- Skyrim (Destruction, Conjuration, etc.)
- Oblivion (Magic Schools)
- Dragon Age (Spell Trees)

**8 Magic Schools:**
1. **Pyromancy** (Fire)
2. **Cryomancy** (Ice)
3. **Electromancy** (Lightning)
4. **Geomancy** (Earth)
5. **Aeromancy** (Wind)
6. **Hydromancy** (Water)
7. **Photomancy** (Light)
8. **Umbramancy** (Shadow)

**Skill Tree Structure (pro School):**
```
Level 1: Basic Spell
    ├─ Level 3: Intermediate Spell
    │   ├─ Level 5: Advanced Spell
    │   └─ Level 6: Combo Spell (requires 2 Schools!)
    └─ Level 4: Utility Spell

Level 10: ULTIMATE SPELL (Explosion-Level!)
```

**Progression:**
```python
# Spieler kann ALLE 8 Schools gleichzeitig lernen
# ABER: Jede School braucht separates Leveling

magic_schools = {
    "pyromancy": {
        "level": 5,
        "spells_unlocked": ["Fireball", "Flame Shield", "Meteor"]
    },
    "cryomancy": {
        "level": 3,
        "spells_unlocked": ["Ice Shard", "Frost Armor"]
    }
}
```

**Combo Magic (Skyrim-inspiriert):**
```python
# Wenn du 2 Schools Level 5+ hast:
if pyromancy.level >= 5 and cryomancy.level >= 5:
    unlock_spell("Steam Blast")  # Fire + Ice

if electromancy.level >= 5 and hydromancy.level >= 5:
    unlock_spell("Lightning Storm")  # Lightning + Water
```

**Beta Testing:**
- Wir definieren erstmal **20 Spells** (2-3 pro School)
- Nach Beta: User gibt Feedback → wir passen an
- Später: Mehr Spells + Skill Trees erweitern

---

## 🎵 MUSICAL INSTRUMENTS SYSTEM

### Cooldown & Mechanics (FINAL - Ocarina of Time Style)

**Inspiration:**
- Zelda: Ocarina of Time (keine Cooldowns, aber Mana)
- Zelda: Majora's Mask (Songs haben verschiedene Effekte)

**6 Instruments:**
1. **Flöte** - Movement Speed Buff
2. **Trommel** - Attack Speed Buff
3. **Harfe** - Defense Buff
4. **Horn** - Rallying Cry (Team Buff)
5. **Gitarre** - Morale Buff (Happiness +)
6. **Glocke** - Enemy Stun (Debuff)

**Mechanics:**
```python
# KEIN Cooldown (wie OoT!)
# ABER: Mana/Stamina Kosten

play_instrument(instrument="flute"):
    if player.stamina < 20:
        return {"error": "Not enough stamina"}

    player.stamina -= 20
    apply_buff("movement_speed", duration=60)  # 60 seconds

    # Rhythm Mini-Game
    success = rhythm_minigame()
    if success == "perfect":
        buff_strength = 150%  # 1.5x stronger
    elif success == "good":
        buff_strength = 100%  # normal
    else:
        buff_strength = 50%   # weak
```

**Rhythm Mini-Game:**
- Guitar Hero Style
- Wenn Perfect Hit → Buff ist stärker!
- Kann während Combat gespielt werden (risky!)

**Equipment:**
```python
# Instrumente sind Equipment
# Player kann 1 Instrument equipped haben
# Kann im Kampf wechseln (Inventory → Equipment Slot)
```

---

## 🐉 REGION BOSS SYSTEM

### Respawn Mechanics (FINAL)

**PvE Bosse (Open World):**
```python
# Bosse spawnen in ihren Regionen

boss_respawn_rules = {
    "first_kill": {
        # Nach erstem Kill:
        # Boss droppt GUTE Loot
        # Boss verschwindet permanent (für diesen Spieler!)
        "respawn": False,
        "loot_quality": "legendary"
    },

    "arena_mode": {
        # In Nemesis Arena:
        # Bosse können NICHT permanent sterben
        # Können unbegrenzt oft gekämpft werden
        # Aber: Weniger Loot als first kill
        "respawn": True,
        "loot_quality": "rare"
    },

    "multiplayer_world": {
        # Wenn Multiplayer aktiv:
        # Boss respawnt nach 24h (für ALLE Spieler)
        # Jeder Spieler kann 1x pro Tag kämpfen
        "respawn_time": "24h",
        "loot_quality": "rare"
    }
}
```

**Hardcore Mode - Boss Permadeath:**
```python
# Wenn Spieler im BOSS-Gebiet stirbt (Hardcore Mode):

if player.game_mode == "hardcore" and location == boss.region:
    if boss.health <= 0:
        # Boss ist tot → Spieler stirbt auch = PERMADEATH
        player.is_permadead = True

    else:
        # Boss lebt noch → Spieler kann von Slime gerettet werden
        if slime.can_rescue():
            slime.rescue(player)
            player.health = 1
        else:
            player.is_permadead = True
```

---

## 🎛️ ADMIN DASHBOARD

### Zugriff (FINAL)

**Wer hat Zugriff:**
```python
ADMIN_USERS = {
    1: {  # Kuja
        "username": "Kuja",
        "role": "super_admin",
        "permissions": ["all"]
    }
    # Später: Trusted Admins hinzufügen
}

# Admin Dashboard Route
@router.get("/admin/dashboard")
async def admin_dashboard(user_id: int):
    if user_id not in ADMIN_USERS:
        raise HTTPException(status_code=403, detail="Forbidden")

    # Show dashboard
    return dashboard_html
```

**Password Protection:**
```python
# Option 1: Basic Auth
# Username: admin
# Password: <strong_password>

# Option 2: JWT Token
# Login mit Admin-Account → Token → Dashboard Zugriff
```

**Später (Public Beta):**
```python
# Trusted Admins können hinzugefügt werden
# z.B. für Community Moderation

ADMIN_USERS[2] = {
    "username": "TrustedAdmin1",
    "role": "moderator",
    "permissions": ["view_users", "ban_users", "view_analytics"]
}
```

---

## ⚙️ CI/CD - GITHUB ACTIONS

### Free Tier Limits (FINAL)

**GitHub Actions Free Tier:**
- ✅ 2,000 Minuten pro Monat (für Private Repos)
- ✅ Unbegrenzt für Public Repos

**Unser Verbrauch (geschätzt):**
```python
# Pro Commit:
ci_tests = 5 min  # pytest + jest
deploy = 10 min   # docker build + push

# Pro Tag:
commits_per_day = 5
total_minutes = (5 + 10) * 5 = 75 min/day

# Pro Monat:
total_month = 75 * 30 = 2,250 min/month
```

**Problem:**
- Wir brauchen ~2,250 min/month
- Free Tier: 2,000 min/month
- **Überziehen um 250 min!**

**Lösung:**
```python
# Option 1: Selektives CI
# Nicht bei JEDEM Commit, nur bei:
# - Main Branch Commits
# - Pull Requests
# - Tagged Releases

# Option 2: Self-hosted Runner
# Eigener PC/Server läuft CI/CD
# Kostet: 0€ (aber Strom + Wartung)

# Option 3: Make Repo Public
# → Unbegrenzte Minutes!
# ABER: Code ist öffentlich sichtbar
```

**Meine Empfehlung:**
- **Jetzt:** Option 1 (Selektives CI)
- **Später:** Option 2 (Self-hosted Runner auf Jetson!)

---

## 📊 ZUSAMMENFASSUNG DER KLARSTELLUNGEN

### ✅ FINAL DECISIONS:

1. **Backend:** FastAPI als Master (Flask entfernen)
2. **Database:** SQLite (local), PostgreSQL (production)
3. **TOR:** Nur für Browser/Terminal Modul (nicht API)
4. **Multiplayer:** Private Beta → Offizielle Beta → Public
5. **Slime Rescue:** Hardcore = 4-6 Wochen Ritual (EXTREM!)
6. **PvP Hardcore:** Nicht zu brutal (Slime bleibt, kein Permadeath)
7. **NSFW Finisher:** Nur in Kuja's APK (später als Modul für 18+)
8. **Magic Schools:** Skyrim-Style Skill Trees
9. **Instruments:** Keine Cooldowns (wie OoT), aber Stamina-Kosten
10. **Region Bosses:** First Kill = permanent weg, Arena = respawn
11. **Admin Dashboard:** Nur Kuja (später: Trusted Admins)
12. **CI/CD:** Selektives CI (Free Tier sparen)

---

**FINALE SPECS - READY FOR IMPLEMENTATION! 🚀**
