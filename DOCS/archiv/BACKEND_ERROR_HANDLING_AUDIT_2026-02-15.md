# BACKEND ERROR-HANDLING AUDIT 2026-02-15

**Durchgeführt von:** SONNET (Claude Sonnet 4.5)
**Datum:** 2026-02-15
**Scope:** Alle FastAPI Endpoints in `backend/api/`

---

## 📊 ZUSAMMENFASSUNG

| Metrik | Wert |
|--------|------|
| **Gesamt API-Dateien** | 51 |
| **Gesamt Endpoints** | ~350 |
| **Endpoints OHNE Try/Except** | **290** (83%) |
| **Kritische Risiko-Endpoints** | ~50 |

---

## ⚠️ KRITISCHE ERKENNTNISSE

### ❌ Problem: 83% der Endpoints haben KEIN Error-Handling!

**Betroffene Endpoints:**
- ❌ `chat_v2.py:chat_v2` - **KRITISCH!** Hauptchat-Endpoint
- ❌ `battle_v2.py` - Alle 7 Battle-Endpoints
- ❌ `battle_unified.py` - Alle 18 Unified-Endpoints
- ❌ `state_v2.py` - State-Management Endpoints
- ❌ `living_v2.py` - Living-System Endpoints
- ❌ ~240 weitere Endpoints

**Konsequenzen:**
- 🔥 **Unhandled Exceptions crashen den Request**
- 🔥 **Keine Fehler-Logs** für Debugging
- 🔥 **500 Errors ohne Details** für Frontend
- 🔥 **Kein Graceful Degradation**

---

## ✅ LÖSUNG: Zentralisiertes Error-Handling

### Neue Utility: `backend/utils/error_handling.py`

**Features:**
1. ✅ `@handle_errors()` Decorator - Automatisches Try/Except
2. ✅ **Strukturiertes Logging** - Alle Exceptions werden geloggt
3. ✅ **HTTP Exception Conversion** - Saubere API-Fehler
4. ✅ **Custom Error Classes** - ValidationError, NotFoundError, etc.

**Usage:**
```python
from backend.utils import handle_errors

@router.post("/example")
@handle_errors()
async def example_endpoint(data: dict):
    # Code hier - Exceptions werden automatisch gefangen!
    return {"status": "ok"}
```

---

## 🎯 PRIORITÄTEN

### P0 - KRITISCH (SOFORT):
1. ✅ `chat_v2.py` - Chat-Endpoint (GEFIXT!)
2. ⬜ `battle_v2.py` - Alle Battle-Endpoints
3. ⬜ `state_v2.py` - State-Management
4. ⬜ `living_v2.py` - Living-System
5. ⬜ `websocket.py` - WebSocket-Endpoints

### P1 - WICHTIG (DIESE WOCHE):
6. ⬜ `slime_v3.py` - Slime-System
7. ⬜ `quest_v2.py` - Quest-System
8. ⬜ `minigame_v2.py` - Minigames
9. ⬜ `combat_magic.py` - Magic-System
10. ⬜ `battle_unified.py` - Unified Combat

### P2 - NICE TO HAVE (SPÄTER):
11. ⬜ Alle restlichen ~240 Endpoints
12. ⬜ Helper-Functions (non-route)
13. ⬜ Read-Only Endpoints

---

## 📝 NÄCHSTE SCHRITTE

**SONNET Tasks (diese Woche):**
1. ✅ Error-Handling Utils erstellt
2. ✅ chat_v2.py gefixt (Beispiel)
3. ⬜ battle_v2.py fixen (7 Endpoints)
4. ⬜ state_v2.py fixen (11 Endpoints)
5. ⬜ living_v2.py fixen (15 Endpoints)
6. ⬜ websocket.py fixen (1 Endpoint)

**Geschätzte Zeit:** ~2-3 Stunden für P0 (34 Endpoints)

---

## 🧪 TESTING

**Nach jedem Fix:**
1. ✅ Server starten: `python backend/main_fastapi.py`
2. ✅ Endpoint testen: `curl -X POST http://localhost:8001/api/v2/chat`
3. ✅ Fehler provozieren (z.B. Ollama stoppen)
4. ✅ Prüfen: Kommt sauberer HTTP 500 + Log-Entry?

---

## 📚 DOKUMENTATION

**Für OPUS (Frontend-Dev):**
- Error-Responses sind jetzt **strukturiert**
- HTTPException hat immer `detail` Feld
- Status-Codes sind korrekt (400, 404, 500, etc.)
- Frontend kann Fehler sauber anzeigen

**Beispiel Error-Response:**
```json
{
  "detail": "Internal server error in chat_v2: Connection refused (Ollama)"
}
```

---

## 🎉 ERFOLGE

- ✅ Error-Handling Utils erstellt
- ✅ Decorator-Pattern implementiert
- ✅ chat_v2.py als Beispiel gefixt
- ✅ Audit-Report dokumentiert

**Next:** Battle-Endpoints fixen! ⚔️
