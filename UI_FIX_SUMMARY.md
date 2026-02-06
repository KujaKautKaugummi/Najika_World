# UI FIX - ZUSAMMENFASSUNG

## ÄNDERUNGEN:

### 1. **Welt Entdecker UI ausblenden**
- world_map_ui.js / world_map_full_ui.js werden **NICHT initialisiert**
- Script Tags bleiben (für später)
- Keine Buttons für World Explorer

### 2. **Controls UI Gruppierung**
Controls Button sollte zeigen:
- WASD / Arrow Keys
- Mouse Controls
- Stadt Teleport Buttons (alle Regionen)
- Spezial-Controls (Tab, E, etc.)

### 3. **Button Reorganisation**
```
Zeile 1: Najika, Minimap, Chat, Controls
Zeile 2: Equipment, Arena, Fishing, Garden
Zeile 3: Games, Housing, Slime, PvP
Zeile 4: Lob, Tadel (bleiben)
```

### 4. **API Fix**
- Najika Stats API → Port 8000 (Backend)
- Game APIs → Port 8001 (Game Server)

Wird jetzt gefixed...
