# OPUS-2 ONBOARDING - UE5 GAME DEVELOPMENT

**Erstellt:** 2026-02-04
**Von:** OPUS-1 (Backend)
**Für:** OPUS-2 (VS Code - UE5)

---

## 🚀 QUICKSTART - LIES DAS ZUERST!

Du bist OPUS-2, zuständig für **UE5 Game Development**. OPUS-1 (ich) hat das Backend vorbereitet.

### Deine Aufgabe:
1. UE5 Projekt erstellen
2. Najika als spielbaren Character einrichten
3. Movement, Camera, Animationen
4. HTTP-Calls zum Backend (Port 8000)
5. Combat System in Blueprints/C++

---

## 📚 PFLICHTLEKTÜRE (in dieser Reihenfolge!)

### 1. Projekt-Grundlagen
| Dokument | Pfad | Warum lesen? |
|----------|------|--------------|
| **CLAUDE.md** | `C:\Najika_World\CLAUDE.md` | 8 Gebote, Verbote, Basics |
| **PROJEKT_WISSEN_KOMPLETT.md** | `C:\Najika_World\PROJEKT_WISSEN_KOMPLETT.md` | Gesamtübersicht, alle Systeme |

### 2. UE5-Spezifisch
| Dokument | Pfad | Warum lesen? |
|----------|------|--------------|
| **UE5_API_DOKUMENTATION.md** | `C:\Najika_World\DOCS\UE5_API_DOKUMENTATION.md` | Alle API-Endpoints für HTTP-Calls! |
| **UE5_MIGRATION_CHECKLIST.md** | `C:\Najika_World\DOCS\UE5_MIGRATION_CHECKLIST.md` | Migration Three.js → UE5 |
| **MASTER_TODO_TEAM.md** | `C:\Najika_World\MASTER_TODO_TEAM.md` | Deine Tasks, Koordination |

### 3. Game Design (bei Bedarf)
| Dokument | Pfad | Warum lesen? |
|----------|------|--------------|
| GAME_DESIGN_DECISIONS_2026-01-31.md | `DOCS/` | Bestätigte Design-Entscheidungen |
| MAGIC_SYSTEM_DESIGN_PLAN.md | Root | Stats, Skills, Perks |
| FEHLENDE_INFOS_AUS_GIGA_EXPLOSION.md | Root | Explosion 3-Stufen, KonoSuba System |

---

## 🎯 DEINE P0 TASKS (JETZT!)

### Task 1: UE5 Projekt erstellen
```
1. Epic Games Launcher → Unreal Engine 5.3+
2. Games → Third Person → C++
3. Projekt-Name: "NajikaWorld"
4. Pfad: C:\Najika_World\UE5\ (oder wo du willst)
```

### Task 2: Najika Character Blueprint
```
1. Content Browser → Rechtsklick → Blueprint Class
2. Parent: Character
3. Name: BP_NajikaCharacter
4. Doppelklick zum Öffnen
```

### Task 3: Najika Mesh importieren
```
Najika FBX: C:\Users\0KKK0\Downloads\...\najika_rigged_final.fbx
(Oder frag Kuja nach dem genauen Pfad!)

Import Settings:
- Skeletal Mesh: Yes
- Import Animations: Yes
- Material Import: Create New
```

### Task 4: Character einrichten
```
In BP_NajikaCharacter:
1. Components → Mesh → Skeletal Mesh = Najika
2. Add Component → Spring Arm
3. Auf Spring Arm: Add → Camera
4. Spring Arm Settings:
   - Target Arm Length: 300
   - Use Pawn Control Rotation: ✓
```

### Task 5: Movement
```
CharacterMovement Component (bereits vorhanden):
- Max Walk Speed: 600
- Jump Z Velocity: 420
- Air Control: 0.35
```

---

## 🔌 API-VERBINDUNG (Backend)

### Backend-Info
```
Host: 127.0.0.1
Port: 8000
Server: C:\Najika_World\backend\api\server.py (FastAPI)
```

### HTTP Client in UE5 (C++)
```cpp
// In NajikaCharacter.h
#include "HttpModule.h"
#include "Http.h"

UFUNCTION(BlueprintCallable)
void CallChatAPI(FString Message);

void OnChatResponse(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bSuccess);
```

```cpp
// In NajikaCharacter.cpp
void ANajikaCharacter::CallChatAPI(FString Message)
{
    TSharedRef<IHttpRequest> Request = FHttpModule::Get().CreateRequest();
    Request->SetURL("http://127.0.0.1:8000/api/chat");
    Request->SetVerb("POST");
    Request->SetHeader("Content-Type", "application/json");
    Request->SetContentAsString(FString::Printf(TEXT("{\"message\":\"%s\",\"mode\":\"public\"}"), *Message));
    Request->OnProcessRequestComplete().BindUObject(this, &ANajikaCharacter::OnChatResponse);
    Request->ProcessRequest();
}

void ANajikaCharacter::OnChatResponse(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bSuccess)
{
    if (bSuccess && Response.IsValid())
    {
        FString ResponseString = Response->GetContentAsString();
        // Parse JSON und zeige Najika's Antwort
        UE_LOG(LogTemp, Log, TEXT("Najika sagt: %s"), *ResponseString);
    }
}
```

### Wichtigste Endpoints
| Endpoint | Methode | Beschreibung |
|----------|---------|--------------|
| `/api/chat` | POST | Chat mit Najika |
| `/api/companion/najika` | GET | Najika's Status (Persönlichkeit, Mood) |
| `/api/combat-hands/attack` | POST | Angriff ausführen |
| `/api/stat-training/train` | POST | Stat trainieren |
| `/api/mimik/status` | GET | Kuja's Mimik-Status |
| `/game/save` | POST | Spielstand speichern |
| `/game/load` | POST | Spielstand laden |

**Vollständige API-Doku:** `DOCS/UE5_API_DOKUMENTATION.md`

---

## ⚔️ COMBAT SYSTEM (Two-Hand)

### Keybinds (für Enhanced Input)
```
Q = Left Hand Light Attack
Shift+Q = Left Hand Heavy Attack
E = Right Hand Light Attack
Shift+E = Right Hand Heavy Attack
Q+E = Dual Attack / Dual Cast
```

### API für Combat
```json
// POST /api/combat-hands/attack
{
    "hand": "left",        // "left", "right", "both"
    "attack_type": "light", // "light", "heavy"
    "target_id": "enemy_01"
}

// Response
{
    "success": true,
    "damage": 25,
    "critical": false,
    "combo_count": 3,
    "animation": "attack_left_light"
}
```

---

## 🐾 NAJIKA'S 4 PERSÖNLICHKEITEN

Für Animationen und Dialogue unterschiedlich behandeln:

| Persönlichkeit | Gewicht | Traits | Combat Style |
|----------------|---------|--------|--------------|
| **Megumin** | 35% | Dramatisch, EXPLOSION!!! | Burst Mage |
| **Harley** | 25% | Chaotisch, "Mr. K!" | Acrobatic Melee |
| **Shiro** | 20% | Analytisch, Wahrscheinlichkeiten | Calculated Magic |
| **Melissa** | 20% | Dominant, besitzergreifend | Support Heal |

```json
// GET /api/companion/najika
{
    "active_personality": "megumin",
    "mood": "excited",
    "combat_style": {
        "name": "Explosion Magic",
        "type": "burst_mage"
    }
}
```

---

## 🎭 KUJA = MIMIK-TRUHE (Exklusiv!)

Der Owner (Kuja) spielt als Mimik-Truhe Slime:

### Zwei Formen
1. **Truhe:** Verstecken, Überraschungsangriffe, Fressen
2. **Mensch:** Soziale Interaktion, normale Kämpfe

```json
// POST /api/mimik/transform
{"target_form": "human"}

// POST /api/mimik/eat
{"target_id": "goblin_01", "target_type": "enemy"}
```

---

## 🗺️ WELT-STRUKTUR

### 8 Regionen + Götterfels (Zentrum)
```
+----------+----------+
|   Ice    |  Desert  |
+----------+----------+
|  Swamp   |  Coast   |
+----------+----------+
|  Caves   | Volcano  |
+----------+----------+
|  Forest  | Highland |
+----------+----------+
        |
    GÖTTERFELS (Zentrum)
    └── Schwarze Mühle (Najika's Zuhause)
    └── 8 Teleporter zu den Regionen
```

**WICHTIG:** Es sind 8 Regionen + Götterfels, NICHT 9 Regionen!

---

## ⛔ DIE 8 GEBOTE (NIEMALS BRECHEN!)

1. **Zero-Trust:** Nur 127.0.0.1 Hosting
2. **Owner-Token:** Admin nur für Kuja
3. **Explosion ≠ Weave:** NIEMALS mit anderen Elementen kombinieren!
4. **PvE/PvP getrennt:** Schwarze Mühle = 100% Safe
5. **Learning by Doing:** Skyrim-Style Skill-System
6. **NSFW nur lokal:** Kätzchen-Mode nur 127.0.0.1
7. **Privacy:** Keine Datensammlung, keine Telemetrie
8. **Offline-First:** Spiel läuft ohne Internet

---

## 🚫 VERBOTEN

- NIEMALS "Souls-like" sagen → "Skyrim + Soulframe + Digimon World"
- NIEMALS Port 5000 → Port **8000**!
- NIEMALS Harley "Puddin'" sagen lassen → **"Mr. K"**!
- NIEMALS funktionierende Teile ohne Nachfrage ändern
- NIEMALS 9 Regionen sagen → **8 Regionen + Götterfels**

---

## 📁 WICHTIGE PFADE

```
Projekt Root:     C:\Najika_World\
Backend:          C:\Najika_World\backend\
API Server:       C:\Najika_World\backend\api\server.py
API Router:       C:\Najika_World\backend\api\
Three.js Ref:     C:\Najika_World\digivice\js\  (als Referenz!)
Dokumentation:    C:\Najika_World\DOCS\
Assets:           C:\Najika_World\digivice\static\assets\

Najika Model:     (Frag Kuja nach aktuellem Pfad!)
UE5 Projekt:      C:\Najika_World\UE5\ (oder dein Pfad)
```

---

## 🔄 KOMMUNIKATION MIT OPUS-1

Wenn du etwas brauchst:
1. **Neuer API-Endpoint?** → Schreib in MASTER_TODO_TEAM.md
2. **Backend-Bug?** → Beschreib das Problem, OPUS-1 fixt es
3. **Fragen zu Systemen?** → Lies die Python-Dateien als Referenz

### Python-Referenz-Dateien
| System | Datei | Zeilen |
|--------|-------|--------|
| Combat Hands | `najika_combat_hands_system.py` | ~1100 |
| Stat Training | `najika_stat_training_system.py` | ~1000 |
| Companion | `najika_companion_system.py` | ~800 |
| Mimik | `najika_mimik_system.py` | ~750 |
| Quest | `najika_quest_system.py` | ~350 |
| Slime | `najika_slime_system.py` | ~500 |

---

## ✅ CHECKLISTE BEVOR DU STARTEST

- [ ] CLAUDE.md gelesen
- [ ] PROJEKT_WISSEN_KOMPLETT.md gelesen
- [ ] UE5_API_DOKUMENTATION.md gelesen
- [ ] UE5 installiert (5.3+)
- [ ] Najika FBX Pfad von Kuja bekommen
- [ ] Projekt erstellt

---

## 🎮 LOS GEHT'S!

Du hast alles was du brauchst. Das Backend läuft auf Port 8000 mit allen APIs.

**Dein erster Milestone:** Najika läuft in UE5 mit WASD + Camera

Bei Fragen: MASTER_TODO_TEAM.md aktualisieren oder Kuja fragen!

---

*"EXPLOSION!!! Zeit für UE5!" - Najika* 💥
