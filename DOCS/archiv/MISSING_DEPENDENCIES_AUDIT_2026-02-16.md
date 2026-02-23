# MISSING DEPENDENCIES AUDIT 2026-02-16

**KRITISCH:** 12 Backend-Module fehlen komplett! ❌

---

## ❌ FEHLENDE MODULE

### Neu registrierte Router (AUDIT-FIX):
1. ❌ **najika_companion_system.py** - Benötigt von `backend/api/companion.py`
2. ❌ **najika_combat_hands_system.py** - Benötigt von `backend/api/combat_hands.py`
3. ❌ **najika_mimik_system.py** - Benötigt von `backend/api/mimik.py`
4. ❌ **najika_stat_training_system.py** - Benötigt von `backend/api/stat_training.py`

### Bereits existierende Router:
5. ❌ **najika_battle.py** - Benötigt von `backend/api/battle_v2.py`, `battle_unified.py`
6. ❌ **najika_mind.py** - Benötigt von `backend/api/chat.py`, `chat_v2.py`
7. ❌ **najika_personality_engine.py** - Benötigt von `backend/api/chat.py`, `chat_v2.py`
8. ❌ **najika_memory.py** - Benötigt von `backend/api/chat.py`, `chat_v2.py`
9. ❌ **najika_living_system.py** - Benötigt von `backend/api/living_v2.py`
10. ❌ **najika_game_actions.py** - Benötigt von `backend/api/najika_game_actions_router.py`
11. ❌ **najika_quest_system.py** - Benötigt von `backend/api/quest_v2.py`
12. ❌ **najika_readiness.py** - Benötigt von `backend/api/readiness.py`

---

## ✅ VORHANDENE MODULE

Nur 2 Module existieren aktuell:
- ✅ `najika_finisher_system.py` (23,833 Bytes)
- ✅ `najika_nemesis_arena_system.py` (34,389 Bytes)

---

## 🔧 IMPACT

### Router-Status:
| Router | Status | Grund |
|--------|--------|-------|
| `/api/companion` | ⚠️ Registriert aber nicht funktional | najika_companion_system fehlt |
| `/api/combat-hands` | ⚠️ Registriert aber nicht funktional | najika_combat_hands_system fehlt |
| `/api/mimik` | ⚠️ Registriert aber nicht funktional | najika_mimik_system fehlt |
| `/api/stat-training` | ⚠️ Registriert aber nicht funktional | najika_stat_training_system fehlt |
| `/api/v2/battle` | ⚠️ Funktional mit Fallback | najika_battle fehlt, nutzt Fallback |
| `/api/chat` | ⚠️ Funktional mit Fallback | najika_mind/personality/memory fehlen |
| `/api/v2/quest` | ⚠️ Funktional mit Fallback | najika_quest_system fehlt |

### Was funktioniert:
- ✅ Router geben **503 Service Unavailable** zurück (korrekt!)
- ✅ Fallback-Logik greift (z.B. Companion gibt Standard-Persönlichkeiten zurück)
- ✅ Server crashed NICHT (try/except funktioniert)

### Was NICHT funktioniert:
- ❌ Companion-System (Najika als KI-Begleiter)
- ❌ Combat Hands (Zwei-Hand-Kampfsystem)
- ❌ Mimik-Truhe (Kuja's exklusiver Charakter)
- ❌ Stat Training (Learning by Doing System)
- ❌ Volle Battle-Logik (Fallback nur basic)
- ❌ Najika AI-Mind (ChatBot-Features)
- ❌ Quest-System (Fallback nur basic)

---

## 📋 LÖSUNGSOPTIONEN

### Option 1: MODULE ERSTELLEN (AUFWENDIG)
**Aufwand:** ~40-80 Stunden (je nach Komplexität)

**Pro:**
- ✅ Volle Funktionalität
- ✅ Alle Router funktionieren
- ✅ Game-Design umgesetzt

**Contra:**
- ❌ Sehr zeitaufwendig
- ❌ Benötigt Game-Design-Dokumente
- ❌ Komplexe Logik (AI, Stats, Combat)

---

### Option 2: ROUTER DEAKTIVIEREN (SCHNELL)
**Aufwand:** 5 Minuten

**Pro:**
- ✅ Sauberer Code
- ✅ Keine 503-Errors mehr
- ✅ Klare Kommunikation: "Noch nicht implementiert"

**Contra:**
- ❌ Features fehlen komplett
- ❌ Muss später wieder aktiviert werden

**Implementation:**
```python
# In backend/main_fastapi.py:

# DEAKTIVIERT - Module fehlen (siehe MISSING_DEPENDENCIES_AUDIT_2026-02-16.md)
# app.include_router(companion.router)
# app.include_router(combat_hands.router)
# app.include_router(mimik.router)
# app.include_router(stat_training.router)
```

---

### Option 3: MOCK-IMPLEMENTATION (MITTELWEG)
**Aufwand:** 4-6 Stunden

**Pro:**
- ✅ Router funktionieren
- ✅ Realistische Dummy-Daten
- ✅ UE5/Frontend kann testen
- ✅ Später durch echte Logik ersetzbar

**Contra:**
- ❌ Keine echte Funktionalität
- ❌ Muss später ersetzt werden

**Implementation:**
```python
# backend/mocks/najika_companion_system.py

class NajikaCompanion:
    """Mock implementation - returns dummy data"""

    def get_state(self):
        return {
            "active_personality": "megumin",
            "mood": "happy",
            "relationship_level": "friend",
            # ... etc
        }

def get_companion_system():
    return NajikaCompanion()
```

---

## 🎯 EMPFEHLUNG

### KURZFRISTIG (für Browser Beta):
**Option 2 + Teilweise Option 3**

1. ✅ Router **DEAKTIVIEREN** die kritisch sind (companion, combat_hands, mimik, stat_training)
2. ✅ Bestehende Router mit Fallback **BEHALTEN** (battle, chat, quest)
3. ✅ In Dokumentation festhalten: "Für Beta nicht benötigt"

### MITTELFRISTIG (nach Beta):
**Option 3** - Mock-Implementations erstellen

1. Wenn UE5-Integration startet → Mocks für Testing
2. Realistische Dummy-Daten
3. Klares TODO: "Replace with real implementation"

### LANGFRISTIG (Full Release):
**Option 1** - Echte Module implementieren

1. Game-Design-Dokumente schreiben
2. Systeme implementieren
3. ChromaDB-Integration (für AI-Memory)
4. Ausgiebiges Testing

---

## 📊 ZUSAMMENFASSUNG

**GEFUNDEN:**
- 12 fehlende Backend-Module
- Router sind registriert aber nicht funktional
- Fallback-Logik funktioniert (kein Crash)

**EMPFEHLUNG:**
- Router deaktivieren für Browser Beta
- Mocks erstellen wenn UE5-Integration startet
- Echte Implementation für Full Release

**AUFWAND:**
- Option 2 (Deaktivieren): 5 Minuten ✅
- Option 3 (Mocks): 4-6 Stunden
- Option 1 (Real): 40-80 Stunden

---

**Erstellt:** 2026-02-16 08:40
**Audit:** SONNET Session Round 3
