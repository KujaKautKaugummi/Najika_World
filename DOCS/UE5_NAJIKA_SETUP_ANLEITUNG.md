# NAJIKA CHARACTER SETUP - SCHRITT FÜR SCHRITT

**Stand:** 2026-02-04
**Voraussetzung:** Najika Model ist importiert unter Characters

---

## SCHRITT 1: CHARACTER BLUEPRINT ERSTELLEN

### 1.1 Blueprint erstellen
```
Content Browser:
1. Rechtsklick im Ordner "Characters" (wo dein Najika Mesh ist)
2. Blueprint Class
3. Im Popup: Suche nach "CombatCharacter" und wähle es
4. Name: BP_NajikaPlayer
5. Doppelklick zum Öffnen
```

### 1.2 Mesh zuweisen
```
Im Blueprint Editor:
1. Links: Components Panel
2. Klick auf "Mesh (Inherited)"
3. Rechts: Details Panel
4. Skeletal Mesh Asset: Wähle dein importiertes Najika Mesh
5. Compile (oben links) + Save
```

### 1.3 API Client hinzufügen
```
Im Blueprint Editor:
1. Components Panel → Add (grüner Button)
2. Suche: "Najika API Client"
3. Hinzufügen
4. Der Component erscheint in der Liste
5. Compile + Save
```

---

## SCHRITT 2: INPUT ACTIONS FÜR COMBAT

### 2.1 Neue Input Actions erstellen
```
Content Browser → Rechtsklick → Input → Input Action

Erstelle diese Actions:
- IA_Attack_Left      (Value Type: Digital/Bool)
- IA_Attack_Right     (Value Type: Digital/Bool)
- IA_Attack_Left_Heavy  (Value Type: Digital/Bool)
- IA_Attack_Right_Heavy (Value Type: Digital/Bool)
- IA_Dodge            (Value Type: Digital/Bool)
- IA_Interact         (Value Type: Digital/Bool)
```

### 2.2 Input Mapping Context erweitern
```
Öffne: IMC_Combat (oder erstelle neue IMC_Najika)

Mappings hinzufügen:

IA_Attack_Left:
  - Key: Q

IA_Attack_Right:
  - Key: E

IA_Attack_Left_Heavy:
  - Key: Q
  - Modifier: Shift (Add Modifier → Shift)

IA_Attack_Right_Heavy:
  - Key: E
  - Modifier: Shift

IA_Dodge:
  - Key: Left Ctrl

IA_Interact:
  - Key: F
```

---

## SCHRITT 3: BLUEPRINT LOGIC FÜR COMBAT

### 3.1 Input Events in BP_NajikaPlayer

Öffne BP_NajikaPlayer → Event Graph:

```
=== LINKER ANGRIFF (Q) ===

Event IA_Attack_Left (Started)
    │
    ▼
Get Component by Class → Najika API Client
    │
    ▼
Attack
  - Hand: Left
  - Attack Type: Light
  - Target ID: "enemy_target" (oder von Trace)
  - On Success: [Custom Event für Animation]
  - On Error: [Print String]
```

```
=== RECHTER ANGRIFF (E) ===

Event IA_Attack_Right (Started)
    │
    ▼
Get Component by Class → Najika API Client
    │
    ▼
Attack
  - Hand: Right
  - Attack Type: Light
  - Target ID: "enemy_target"
```

```
=== SCHWERER ANGRIFF LINKS (Shift+Q) ===

Event IA_Attack_Left_Heavy (Started)
    │
    ▼
Najika API Client → Attack
  - Hand: Left
  - Attack Type: Heavy
```

```
=== SCHWERER ANGRIFF RECHTS (Shift+E) ===

Event IA_Attack_Right_Heavy (Started)
    │
    ▼
Najika API Client → Attack
  - Hand: Right
  - Attack Type: Heavy
```

### 3.2 Chat mit Najika (Optional)

```
=== CHAT ÖFFNEN (T oder Enter) ===

Event Keyboard T
    │
    ▼
[Öffne Chat Widget]
    │
    ▼
Bei Text Submit:
Najika API Client → Send Chat
  - Message: [Text Input]
  - Private Mode: false
  - On Success: [Zeige Antwort im Widget]
```

---

## SCHRITT 4: ANIMATION BLUEPRINT

### 4.1 Animation Blueprint erstellen
```
Content Browser:
1. Rechtsklick → Animation → Animation Blueprint
2. Target Skeleton: Das Skeleton von deinem Najika Mesh
3. Name: ABP_Najika
4. Öffnen
```

### 4.2 Variablen erstellen
```
Im ABP_Najika:
Variables (links):
- Speed (Float)
- IsInAir (Bool)
- IsAttacking (Bool)
- AttackHand (Enum oder Int: 0=None, 1=Left, 2=Right, 3=Both)
```

### 4.3 Event Graph
```
Event Blueprint Update Animation
    │
    ▼
Try Get Pawn Owner → Cast to BP_NajikaPlayer
    │
    ▼
Get Velocity → Vector Length → Set Speed
    │
    ▼
Get Character Movement → Is Falling → Set IsInAir
```

### 4.4 Anim Graph - State Machine
```
Erstelle State Machine "Locomotion":

States:
┌─────────────────────────────────────┐
│                                     │
│    ┌──────┐     ┌──────┐           │
│    │ Idle │────►│ Walk │           │
│    └──────┘     └──────┘           │
│        ▲           │                │
│        │           ▼                │
│        │       ┌──────┐            │
│        └───────│ Run  │            │
│                └──────┘            │
│                                     │
│    ┌────────────────────┐          │
│    │   Jump (Blend)     │          │
│    └────────────────────┘          │
│                                     │
│    ┌────────────────────┐          │
│    │  Attack States     │          │
│    │  (Left/Right/Both) │          │
│    └────────────────────┘          │
└─────────────────────────────────────┘

Transitions:
- Idle → Walk: Speed > 10
- Walk → Run: Speed > 300
- Walk → Idle: Speed < 10
- Any → Attack: IsAttacking = true
- Attack → Idle: Animation Finished
```

### 4.5 ABP dem Character zuweisen
```
In BP_NajikaPlayer:
1. Mesh Component auswählen
2. Details → Animation
3. Anim Class: ABP_Najika
```

---

## SCHRITT 5: GAME MODE EINRICHTEN

### 5.1 Game Mode erstellen (falls nicht vorhanden)
```
Content Browser:
1. Rechtsklick → Blueprint Class
2. Parent: Game Mode Base (oder CombatGameMode)
3. Name: BP_NajikaGameMode
```

### 5.2 Default Pawn setzen
```
In BP_NajikaGameMode:
1. Class Defaults öffnen
2. Default Pawn Class: BP_NajikaPlayer
```

### 5.3 Level Settings
```
In deinem Level:
1. Window → World Settings
2. GameMode Override: BP_NajikaGameMode
```

---

## SCHRITT 6: TESTEN!

### 6.1 Quick Test
```
1. Drücke Play (Alt+P)
2. Prüfe:
   - [ ] Najika spawnt mit richtigem Mesh
   - [ ] WASD funktioniert
   - [ ] Kamera folgt
   - [ ] Q/E triggern (check Output Log)
```

### 6.2 API Test (Backend muss laufen!)
```
Starte Backend:
cd C:\Najika_World\backend
python api/server.py

Dann im Spiel:
- Drücke Q oder E
- Schau im Output Log nach "Attack request" Meldungen
```

---

## SCHRITT 7: MIMIK-TRUHE (KUJA'S CHARACTER)

### 7.1 Separater Character für Kuja
```
Erstelle: BP_MimikTruhe (von CombatCharacter)
- Braucht eigenes Mesh (Truhe + Mensch Form)
- Hat Morph Targets oder 2 Skeletal Meshes
```

### 7.2 Form-Wechsel Blueprint
```
Event: Input T (Transform)
    │
    ▼
Najika API Client → Transform Mimik
  - Target Form: [Toggle zwischen Chest/Human]
    │
    ▼
On Success:
  - Spiele Transformation Animation
  - Wechsle Mesh/Morph Target
```

---

## BONUS: NAJIKA KI-BEGLEITER

### Als NPC der mitläuft:
```
Erstelle: BP_NajikaCompanion (von Character)
- AI Controller mit Behavior Tree
- Folgt dem Spieler
- Greift Feinde an basierend auf Persönlichkeit
- Ruft /api/companion/attack auf
```

### Persönlichkeits-Wechsel:
```
Event: Combat Victory
    │
    ▼
Najika API Client → Get Companion Status
    │
    ▼
Switch auf Active Personality:
  - Megumin: "EXPLOSION!!!" Voiceline + Pose
  - Harley: "*kicher*" Voiceline
  - Shiro: Analytische Voiceline
  - Melissa: Dominante Voiceline
```

---

## CHECKLISTE

- [ ] BP_NajikaPlayer erstellt
- [ ] Najika Mesh zugewiesen
- [ ] API Client Component hinzugefügt
- [ ] Input Actions erstellt (Q/E, Shift+Q/E)
- [ ] Input Mapping Context konfiguriert
- [ ] Animation Blueprint erstellt
- [ ] Game Mode mit Najika als Default Pawn
- [ ] Backend läuft auf Port 8000
- [ ] Test: Spieler kann rumlaufen
- [ ] Test: Q/E Attacks funktionieren

---

*"EXPLOSION!!! Najika ist spielbereit!" - Najika* 💥
