# UE5 SOURCE FILES - NAJIKA WORLD

Diese Dateien in dein UE5 Projekt kopieren!

---

## INSTALLATION

### 1. Dateien kopieren
```
Kopiere alles aus diesem Ordner nach:
C:\Najika_World\UE5\NajikaWorld\Source\NajikaWorld\
```

### 2. Build.cs anpassen
In `NajikaWorld.Build.cs` diese Module hinzufügen:
```csharp
PublicDependencyModuleNames.AddRange(new string[] {
    "Core",
    "CoreUObject",
    "Engine",
    "InputCore",
    "HTTP",           // <-- NEU!
    "Json",           // <-- NEU!
    "JsonUtilities"   // <-- NEU!
});
```

### 3. Projekt neu kompilieren
- In UE5: Ctrl+Alt+F11 (oder "Compile" Button)
- Oder: Solution in Visual Studio öffnen und Build

---

## DATEIEN

| Datei | Beschreibung |
|-------|--------------|
| `NajikaAPITypes.h` | Alle Datenstrukturen (Stats, Combat, Companion, etc.) |
| `NajikaAPIClient.h` | HTTP Client Header (Blueprint-aufrufbar) |
| `NajikaAPIClient.cpp` | HTTP Client Implementation |

---

## NUTZUNG IN BLUEPRINTS

### 1. Component hinzufügen
In deinem Character Blueprint:
- Add Component → `Najika API Client`

### 2. Chat mit Najika
```
Event: On Key Pressed (Enter)
→ Get Najika API Client Component
→ Call "Send Chat"
   - Message: "Hallo Najika!"
   - Private Mode: false
   - On Success: Bind to custom event
   - On Error: Bind to error handler
```

### 3. Angriff (Q = Links, E = Rechts)
```
Event: IA_Attack_Left
→ Get Najika API Client
→ Call "Attack"
   - Hand: Left
   - Attack Type: Light
   - Target ID: Enemy reference ID
   - On Success: Play animation, apply damage
```

### 4. Mimik Form wechseln
```
Event: On Key Pressed (T)
→ Get Najika API Client
→ Call "Transform Mimik"
   - Target Form: Human (oder Chest)
```

---

## API ENDPOINTS

Der Client ruft diese Endpoints auf `http://127.0.0.1:8000`:

| Funktion | Endpoint | Methode |
|----------|----------|---------|
| Chat | `/api/chat` | POST |
| Attack | `/api/combat-hands/attack` | POST |
| Companion Status | `/api/companion/najika` | GET |
| Mimik Transform | `/api/mimik/transform` | POST |
| Train Stat | `/api/stat-training/train` | POST |
| Save Game | `/game/save` | POST |
| Load Game | `/game/load` | POST |

---

## WICHTIG: PORT 8000!

Der Backend-Server läuft auf **Port 8000** (NICHT 5000!).

Falls Backend nicht läuft:
```
cd C:\Najika_World\backend
python api/server.py
```

---

## DEBUGGING

### Logs prüfen
In UE5 Output Log nach "NajikaAPIClient" suchen.

### Backend-Status prüfen
```
CheckHealth() aufrufen
→ "Backend is running!" = OK
→ "ERROR: Backend not reachable" = Server starten!
```

---

*"EXPLOSION!!! Der Code ist bereit!" - Najika*
