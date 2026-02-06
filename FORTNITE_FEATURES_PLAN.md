# 🎮 FORTNITE FEATURES FÜR NAJIKA WORLD

**Erstellt:** 2026-02-06
**Status:** PLAN - Bereit zur Implementation

---

## 📋 ÜBERSICHT

Wir übernehmen die besten Elemente aus:
1. **Fortnite Battle Royale** - Kamera, Steuerung, UI
2. **Lego Fortnite** - Building (✅ bereits implementiert!)
3. **Fortnite Festival** - Music Mode (NUR ZUM SPASS, keine Buffs!)

---

# 1️⃣ KAMERA-SYSTEM (3 MODI - JEDERZEIT WECHSELBAR!)

## 1.0 Übersicht - Freie Kamera-Wahl!

```
┌─────────────────────────────────────────────────────────────────────────────┐
│              3 KAMERA-MODI (Jederzeit nahtlos wechselbar!)                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   Der Spieler kann JEDERZEIT zwischen allen 3 Modi wechseln!                │
│   Übergang ist NAHTLOS (smooth 0.3s transition)                             │
│                                                                              │
│   WECHSEL-TASTEN:                                                            │
│   • [P] = Nächster Modus (Third → First → Free → Third...)                  │
│   • [Mausrad-Klick] = Schnellwechsel                                        │
│   • [1] [2] [3] auf Numpad = Direkt zu Modus                                │
│                                                                              │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                     │
│   │ THIRD-PERSON│◄──►│ FIRST-PERSON│◄──►│  FREE CAM   │                     │
│   │  (Fortnite) │    │  (CS2/Val)  │    │   (MMORPG)  │                     │
│   └─────────────┘    └─────────────┘    └─────────────┘                     │
│         ▲                                      ▲                             │
│         └──────────────────────────────────────┘                             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 1.1 Third-Person Kamera (Fortnite Battle Royale Settings!)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│            MODUS 1: THIRD-PERSON (Fortnite Battle Royale Settings)           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌─────────────────────────────────────────────┐                           │
│   │                                             │                           │
│   │                    ┌───┐                    │                           │
│   │                    │ N │  ← Najika          │                           │
│   │                    │ a │                    │                           │
│   │                    │ j │                    │                           │
│   │                    │ i │                    │                           │
│   │                    │ k │                    │                           │
│   │                    │ a │                    │                           │
│   │                    └───┘                    │                           │
│   │              ↑                              │                           │
│   │         Kamera etwas rechts                 │                           │
│   │         über der Schulter                   │                           │
│   └─────────────────────────────────────────────┘                           │
│                                                                              │
│   FORTNITE BR SETTINGS (1:1 übernommen!):                                   │
│   • Offset: Rechts +40, Hoch +60 (Over-the-Shoulder)                        │
│   • Distanz: 300 Units (normal)                                             │
│   • Distanz ADS: 150 Units (näher rangezoomt)                               │
│   • FOV: 80° (normal)                                                       │
│   • FOV ADS: 60° (gezoomt)                                                  │
│   • Lag: Sanftes Nachfolgen (CameraLagSpeed = 10)                           │
│   • [V] = Schulter wechseln (links/rechts)                                  │
│                                                                              │
│   BESTE FÜR: Combat, Exploration, Building                                  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 1.2 First-Person Kamera (Fortnite BALLISTIC Settings!)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│             MODUS 2: FIRST-PERSON (Fortnite BALLISTIC Settings!)             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌─────────────────────────────────────────────┐                           │
│   │                     +                        │                           │
│   │                  ╱     ╲                     │  ← Fadenkreuz            │
│   │                +    ●    +                   │                           │
│   │                  ╲     ╱                     │                           │
│   │                     +                        │                           │
│   │                                             │                           │
│   │   ┌─────────────────────────────────────┐   │                           │
│   │   │  Spell/Waffe sichtbar (3D Model)    │   │  ← Hände + Waffe         │
│   │   └─────────────────────────────────────┘   │                           │
│   └─────────────────────────────────────────────┘                           │
│                                                                              │
│   FORTNITE BALLISTIC SETTINGS (1:1 übernommen!):                            │
│   • Distanz: 0 (Kamera = Najikas Augen)                                     │
│   • FOV: 103° (Ballistic Default!)                                          │
│   • FOV ADS: 70° (gezoomt)                                                  │
│   • Character Model: Nur Hände + Waffe/Spell sichtbar                       │
│   • Viewmodel FOV: Separate Einstellung für Waffen-Größe                    │
│   • Kann Najika im Wasser-Reflektion sehen!                                 │
│                                                                              │
│   BESTE FÜR: Präzises Zielen, Immersion, Innenräume, Arena-Kämpfe           │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 1.3 Free Camera (MMORPG-Style)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MODUS 3: FREE CAM (wie WoW/FFXIV/GW2)                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌─────────────────────────────────────────────┐                           │
│   │         🎥 ←── Kamera frei drehbar          │                           │
│   │        ╱                                    │                           │
│   │       ╱   kann komplett um Najika           │                           │
│   │      ╱    rotieren (360°)                   │                           │
│   │     ▼                                       │                           │
│   │           ┌───┐                             │                           │
│   │           │ N │                             │                           │
│   │           │ a │  ← Najika immer sichtbar    │                           │
│   │           │ j │                             │                           │
│   │           └───┘                             │                           │
│   └─────────────────────────────────────────────┘                           │
│                                                                              │
│   PARAMETER:                                                                 │
│   • Distanz: 100-800 Units (Mausrad = Zoom!)                                │
│   • Rotation: 360° horizontal, -80° bis +80° vertikal                       │
│   • FOV: 70°                                                                │
│   • RMB gehalten = Kamera drehen                                            │
│   • LMB gehalten = Charakter drehen mit Kamera                              │
│   • Mausrad = Zoom rein/raus                                                │
│                                                                              │
│   BESTE FÜR: Screenshots, Übersicht, Selfie-Mode, Cutscenes                 │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 1.4 ADS/Zielen (in jedem Modus!)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ADS (Aim Down Sights) - RMB gehalten                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ADS funktioniert in JEDEM Kamera-Modus!                                   │
│                                                                              │
│   THIRD-PERSON + ADS:                                                        │
│   • Kamera zoomt näher ran (300 → 150 Units)                                │
│   • FOV wird kleiner (80° → 60°)                                            │
│   • Bleibt Third-Person, nur präziser                                       │
│                                                                              │
│   FIRST-PERSON + ADS:                                                        │
│   • FOV wird kleiner (90° → 60°)                                            │
│   • Waffe/Spell wird zentriert                                              │
│   • Wie CS2 Scope                                                           │
│                                                                              │
│   FREE CAM + ADS:                                                            │
│   • Kamera springt automatisch hinter Charakter                             │
│   • Wird temporär zu Third-Person ADS                                       │
│   • Nach Loslassen zurück zu Free Cam                                       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 1.3 Steuerung (Input)

### Bewegung (ALLE Fortnite-Mechaniken):
| Taste | Aktion | Fortnite-Identisch |
|-------|--------|-------------------|
| W/A/S/D | Bewegung | ✅ |
| Shift | Sprint | ✅ |
| Ctrl | Crouch/Ducken | ✅ |
| Ctrl (gehalten) + W | **CRAWL** (Krabbeln) | ✅ |
| Z | **PRONE** (Hinlegen) | ✅ |
| Space | Springen | ✅ |
| Space (an Kante) | Mantling (Hochziehen) | ✅ |

### Bewegungs-Modi im Detail:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         BEWEGUNGS-MODI                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   1. STANDING (Normal):                                                      │
│      ╔═══╗    • Volle Geschwindigkeit                                       │
│      ║   ║    • Kann springen                                               │
│      ║ N ║    • Kann sprinten                                               │
│      ╚═══╝                                                                   │
│                                                                              │
│   2. CROUCH (Ducken) - Ctrl:                                                │
│      ╔═══╗    • 50% Geschwindigkeit                                         │
│       ╲_╱     • Leiser                                                      │
│               • Kleinere Hitbox                                              │
│                                                                              │
│   3. CRAWL (Krabbeln) - Ctrl gehalten + Bewegung:                           │
│       ___     • 25% Geschwindigkeit                                         │
│      /   \    • Sehr leise                                                  │
│      \_N_/    • Noch kleinere Hitbox                                        │
│               • Kann unter niedrigen Hindernissen durch                      │
│                                                                              │
│   4. PRONE (Hinlegen) - Z:                                                  │
│      ────     • Keine/minimale Bewegung                                     │
│      │ N │    • Fast unsichtbar im Gras                                     │
│      ────     • Kleinste Hitbox                                             │
│               • Perfekt zum Verstecken                                       │
│               • Kann zielen aber nicht laufen                                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Kamera:
| Taste | Aktion | Fortnite-Identisch |
|-------|--------|-------------------|
| Maus | Umsehen | ✅ |
| RMB (gehalten) | ADS / First-Person Zoom | ✅ |
| Mausrad | Items wechseln | ✅ |
| V | Kamera-Schulter wechseln | ✅ |

### Combat:
| Taste | Aktion | Anpassung für Najika |
|-------|--------|---------------------|
| LMB | Primär-Angriff | Linke Hand |
| Q | Sekundär-Angriff | Rechte Hand |
| E | Interagieren | Wie Fortnite |
| R | Nachladen/Spezial | Spell wechseln |
| F | Waffe aufheben | Wie Fortnite |
| G | Grab (Wrestling) | NEU für Najika |
| T | TIDS (Gag-Move) | NEU für Najika |

### Building (Lego Fortnite Style):
| Taste | Aktion |
|-------|--------|
| B | Building-Modus Toggle |
| 1-6 | Gebäude auswählen |
| LMB | Platzieren |
| RMB | Rotieren |
| Mausrad | Höhe anpassen |

## 1.5 UE5 Implementation

### Camera Mode Enum:
```cpp
UENUM(BlueprintType)
enum class ECameraMode : uint8
{
    ThirdPerson  UMETA(DisplayName = "Third-Person (Fortnite)"),
    FirstPerson  UMETA(DisplayName = "First-Person (CS2)"),
    FreeCam      UMETA(DisplayName = "Free Camera (MMORPG)")
};
```

### Camera Component (BP_NajikaCharacter):
```cpp
// Current Camera Mode
UPROPERTY(BlueprintReadWrite, Category = "Camera")
ECameraMode CurrentCameraMode = ECameraMode::ThirdPerson;

// === THIRD-PERSON SETTINGS (FORTNITE BATTLE ROYALE!) ===
UPROPERTY(EditAnywhere, Category = "Camera|ThirdPerson")
float ThirdPersonDistance = 300.0f;  // Fortnite BR Default

UPROPERTY(EditAnywhere, Category = "Camera|ThirdPerson")
float ThirdPersonADSDistance = 150.0f;  // Fortnite BR ADS

UPROPERTY(EditAnywhere, Category = "Camera|ThirdPerson")
FVector ThirdPersonOffset = FVector(0, 40, 60); // Over-the-Shoulder

UPROPERTY(EditAnywhere, Category = "Camera|ThirdPerson")
float ThirdPersonFOV = 80.0f;  // Fortnite BR Default

UPROPERTY(EditAnywhere, Category = "Camera|ThirdPerson")
float ThirdPersonADSFOV = 60.0f;  // Fortnite BR ADS

// === FIRST-PERSON SETTINGS (FORTNITE BALLISTIC!) ===
UPROPERTY(EditAnywhere, Category = "Camera|FirstPerson")
float FirstPersonFOV = 103.0f;  // Fortnite Ballistic Default!

UPROPERTY(EditAnywhere, Category = "Camera|FirstPerson")
float FirstPersonADSFOV = 70.0f;  // Fortnite Ballistic ADS

UPROPERTY(EditAnywhere, Category = "Camera|FirstPerson")
float ViewmodelFOV = 70.0f;  // Separate FOV für Waffen-Model

// === FREE CAM SETTINGS ===
UPROPERTY(EditAnywhere, Category = "Camera|FreeCam")
float FreeCamMinDistance = 100.0f;

UPROPERTY(EditAnywhere, Category = "Camera|FreeCam")
float FreeCamMaxDistance = 800.0f;

UPROPERTY(EditAnywhere, Category = "Camera|FreeCam")
float FreeCamDefaultDistance = 400.0f;

UPROPERTY(EditAnywhere, Category = "Camera|FreeCam")
float FreeCamFOV = 70.0f;

// === TRANSITION ===
UPROPERTY(EditAnywhere, Category = "Camera|Transition")
float CameraModeTransitionSpeed = 3.0f;  // 0.3s smooth transition

UPROPERTY(EditAnywhere, Category = "Camera|Transition")
float ADSTransitionSpeed = 5.0f;

// === GENERAL ===
UPROPERTY(EditAnywhere, Category = "Camera")
float CameraLagSpeed = 10.0f;

UPROPERTY(EditAnywhere, Category = "Camera")
bool bShoulderRight = true;  // V to toggle
```

### Camera Mode Functions:
```cpp
// Cycle to next camera mode (P key)
UFUNCTION(BlueprintCallable, Category = "Camera")
void CycleCameraMode();

// Set specific camera mode
UFUNCTION(BlueprintCallable, Category = "Camera")
void SetCameraMode(ECameraMode NewMode);

// Toggle shoulder side (V key) - only in Third-Person
UFUNCTION(BlueprintCallable, Category = "Camera")
void ToggleShoulderSide();

// Free Cam zoom (Mouse Wheel)
UFUNCTION(BlueprintCallable, Category = "Camera")
void FreeCamZoom(float Delta);
```

### Movement States (Enum):
```cpp
UENUM(BlueprintType)
enum class EMovementState : uint8
{
    Standing    UMETA(DisplayName = "Standing"),
    Crouching   UMETA(DisplayName = "Crouching"),
    Crawling    UMETA(DisplayName = "Crawling"),
    Prone       UMETA(DisplayName = "Prone"),
    Sprinting   UMETA(DisplayName = "Sprinting"),
    Jumping     UMETA(DisplayName = "Jumping"),
    Mantling    UMETA(DisplayName = "Mantling")
};
```

### Movement Speeds:
```cpp
UPROPERTY(EditAnywhere, Category = "Movement")
float WalkSpeed = 400.0f;

UPROPERTY(EditAnywhere, Category = "Movement")
float SprintSpeed = 700.0f;

UPROPERTY(EditAnywhere, Category = "Movement")
float CrouchSpeed = 200.0f;  // 50%

UPROPERTY(EditAnywhere, Category = "Movement")
float CrawlSpeed = 100.0f;   // 25%

UPROPERTY(EditAnywhere, Category = "Movement")
float ProneSpeed = 25.0f;    // Fast keine Bewegung
```

### Input Actions (Enhanced Input):
```
// MOVEMENT
IA_Move       - Vector2D (WASD)
IA_Look       - Vector2D (Mouse)
IA_Jump       - Bool (Space)
IA_Sprint     - Bool (Shift)
IA_Crouch     - Bool (Ctrl)
IA_Prone      - Bool (Z)           // Hinlegen
IA_Mantle     - Auto-Trigger bei Kante

// CAMERA (NEU - 3 Modi!)
IA_CycleCamera     - Bool (P)              // Nächster Kamera-Modus
IA_CameraMode1     - Bool (Numpad 1)       // Third-Person
IA_CameraMode2     - Bool (Numpad 2)       // First-Person
IA_CameraMode3     - Bool (Numpad 3)       // Free Cam
IA_ToggleShoulder  - Bool (V)              // Schulter wechseln
IA_CameraZoom      - Float (Mausrad)       // Free Cam Zoom
IA_ADS             - Bool (RMB)            // Aim Down Sights

// COMBAT
IA_Attack_L   - Bool (LMB)
IA_Attack_R   - Bool (Q)
IA_Interact   - Bool (E)
IA_Grab       - Bool (G)
IA_TIDS       - Bool (T)
IA_Build      - Bool (B)
```

---

# 2️⃣ MUSIC MODE (NUR ZUM SPASS!)

## ⚠️ WICHTIG: KEINE BUFFS DURCH MUSIK!
**Musik ist rein für Spaß, Atmosphäre und Immersion!**
**Keine Gameplay-Vorteile durch Musik spielen!**

## 2.1 Konzept

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    NAJIKA MUSIC MODE (NUR ZUM SPASS!)                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   Instrumente die Najika spielen kann:                                      │
│                                                                              │
│   🎵 OCARINA          - Zelda-Style, schöne Melodien                        │
│   🎸 ECHOHARP         - Barden-Instrument, Atmosphäre                       │
│   🥁 TAIKO-TROMMEL    - Rhythmus, Festival-Feeling                          │
│   🎺 EXPLOSION-HORN   - Megumin-Spezial! (Dramatische Fanfare)              │
│                                                                              │
│   GAMEPLAY:                                                                  │
│   ─────────────────────────────────────────────────────────────────────────│
│   • Rhythm-Game UI wenn Instrument gespielt wird                            │
│   • Noten treffen = Besserer Score (NUR FÜR HIGHSCORE!)                    │
│   • Perfekter Song = Cooler Rank (S, A, B, C...)                           │
│   • Multiplayer: Zusammen spielen = Mehr Spaß!                              │
│                                                                              │
│   ⚠️ KEINE GAMEPLAY-BUFFS! ⚠️                                               │
│   ─────────────────────────────────────────────────────────────────────────│
│   • Musik ist nur zur Unterhaltung                                          │
│   • Keine Heilung durch Songs                                               │
│   • Keine ATK/DEF Boosts                                                    │
│   • Nur Spaß und Atmosphäre!                                                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 2.2 Rhythm-Game Mechanik

```
   RHYTHM UI:
   ═══════════════════════════════════════════════════════════════

         ♪    ♪         ♪              ♪    ♪
         │    │         │              │    │
         │    │    ───► │ ◄─── TREFFER │    │
         │    │         │    LINIE     │    │
         │    │         │              │    │
   ─────────────────────●──────────────────────────────────
                        ↑
                   [SPACE/LMB]

   Bewertung (NUR FÜR HIGHSCORE!):
   • PERFECT - 100 Punkte
   • GREAT   - 75 Punkte
   • GOOD    - 50 Punkte
   • MISS    - 0 Punkte

   Ranks (NUR ZUM ANGEBEN!):
   • ⭐ PERFECT ⭐ - 100%
   • S - Amazing! - 95%+
   • A - Great!   - 90%+
   • B - Good!    - 80%+
   • C - Nice!    - 70%+
   • D - Practice - 60%+
   • F - Try again
```

## 2.3 Songs & Stimmungen

| Song | Instrument | Stimmung | Beschreibung |
|------|------------|----------|--------------|
| Song of Healing | Ocarina | Friedlich | Beruhigende Melodie |
| Song of Soaring | Ocarina | Fröhlich | Macht gute Laune |
| Najika's Lullaby | Ocarina | Schläfrig | Für gemütliche Abende |
| Adventure Theme | Echoharp | Episch | Für Abenteurer |
| Campfire Song | Echoharp | Gemütlich | Am Lagerfeuer |
| War Drums | Taiko | Intensiv | Kraftvolle Beats |
| Festival Beat | Taiko | Festlich | Zum Feiern |
| EXPLOSION ANTHEM | Horn | DRAMATISCH | EXPLOSION!!! 💥 |

---

# 3️⃣ CREATIVE MODE ELEMENTE

## 3.1 Najika's Lebensraum

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CREATIVE MODE - NAJIKAS ZUHAUSE                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   Die SCHWARZE MÜHLE ist Najikas Basis.                                     │
│   Spieler können sie AUSBAUEN und DEKORIEREN!                               │
│                                                                              │
│   ZONEN:                                                                     │
│   ─────────────────────────────────────────────────────────────────────────│
│                                                                              │
│   🏠 INNENRAUM (sicher):                                                    │
│      • Schlafzimmer (Najika schläft hier!)                                  │
│      • Küche (Kochen)                                                       │
│      • Werkstatt (Crafting)                                                 │
│      • Bibliothek (Skill-Training)                                          │
│      • Musik-Zimmer (Instrumente üben - NUR ZUM SPASS!)                     │
│                                                                              │
│   🌳 AUSSENBEREICH:                                                         │
│      • Garten (Pflanzen anbauen)                                            │
│      • Teich (Fischen)                                                      │
│      • Training Area (Combat-Übungen)                                       │
│      • Slime-Gehege (Slime-Pflege)                                          │
│      • Portal-Plattform (zu anderen Regionen)                               │
│                                                                              │
│   NAJIKA VERHALTEN:                                                          │
│   ─────────────────────────────────────────────────────────────────────────│
│   • Najika hat einen TAGESABLAUF                                            │
│   • Sie interagiert mit Gebäuden/Möbeln                                     │
│   • Sie kommentiert neue Dekorationen                                       │
│   • Sie schlägt Verbesserungen vor                                          │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 3.2 Prefab-System

```
PREFABS (Vorgefertigte Strukturen):
═════════════════════════════════════════════════════════════════

BASIC (freigeschaltet von Anfang):
├── Small House       - 4 Wände, Dach, Tür
├── Simple Bridge     - Überquerung für Flüsse
├── Watch Tower       - Aussichtspunkt
└── Storage Shed      - Lager für Items

INTERMEDIATE (nach Crafting-Level 10):
├── Two-Story House   - Mit Treppen!
├── Greenhouse        - Pflanzen wachsen schneller
├── Workshop          - Crafting-Bonus
└── Stable            - Für Mounts (später)

ADVANCED (nach Crafting-Level 25):
├── Castle Tower      - Verteidigung
├── Magic Laboratory  - Alchemie
├── Concert Stage     - Zum Musik spielen (kein Buff!)
└── Portal Room       - Schnellreise-Hub

NAJIKA SPECIAL (Quest-Belohnungen):
├── Megumin's Tower   - EXPLOSION-Deko!
├── Harley's Fun House - Bunte Chaos-Deko
├── Shiro's Library   - Voller Bücher
└── Melissa's Garden  - Schöne Blumen
```

## 3.3 Najika's Tagesablauf

```
UHRZEIT (IN-GAME)   │ NAJIKA'S AKTIVITÄT
════════════════════│═══════════════════════════════════════════
06:00 - 08:00      │ Aufwachen, Strecken, Frühstücken
08:00 - 10:00      │ Garten gießen, Slimes füttern
10:00 - 12:00      │ Training / Skill-Übungen
12:00 - 13:00      │ Mittagessen, Chat mit Spieler
13:00 - 16:00      │ Abenteuer / Begleitet Spieler
16:00 - 18:00      │ Crafting / Werkstatt
18:00 - 19:00      │ Abendessen kochen
19:00 - 21:00      │ Musik spielen / Entspannen (NUR SPASS!)
21:00 - 22:00      │ Tagebuch schreiben
22:00 - 06:00      │ Schlafen (kann geweckt werden!)

WENN SPIELER ONLINE:
• Najika passt Aktivitäten an
• Folgt dem Spieler auf Abenteuer
• Kommentiert Aktionen
• Hilft bei Kämpfen

WENN SPIELER OFFLINE:
• Najika folgt Tagesablauf autonom
• Trainiert Skills
• Pflegt Garten & Slimes
• Macht "Offline-Fortschritt"
```

---

# 4️⃣ IMPLEMENTATION REIHENFOLGE

## Phase 1: Kamera-System & Bewegung (PRIORITÄT!)

1. **UE5 Camera Component**
   - SpringArm mit Fortnite-Settings
   - Over-the-Shoulder Offset
   - ADS → First-Person Transition
   - Camera Lag

2. **Enhanced Input System**
   - Input Actions erstellen
   - Input Mapping Context
   - Keybindings

3. **Movement Component**
   - Sprint
   - Crouch
   - **CRAWL** (Krabbeln) - NEU!
   - **PRONE** (Hinlegen) - NEU!
   - Mantling

4. **Testing**
   - In Digivice (Three.js vereinfacht)
   - In UE5 (voll)

## Phase 2: Music Mode (NUR SPASS!)

1. **Instrument System**
   - Instrument Items
   - Equip/Unequip

2. **Rhythm-Game UI**
   - Note Highway
   - Timing System
   - Score/Combo (NUR HIGHSCORE!)

3. **High-Score System**
   - Persönliche Bestscores
   - KEINE Gameplay-Vorteile!

4. **Multiplayer Jam**
   - Sync zwischen Spielern
   - Zusammen Spaß haben!

## Phase 3: Creative Mode

1. **Prefab System**
   - Prefab Data (JSON)
   - Placement Logic
   - Snapping

2. **Najika AI Schedule**
   - Tagesablauf
   - Aktivitäten
   - Interaktionen

3. **Room System**
   - Raum-Erkennung
   - Raum-Effekte (nur dekorativ!)

---

# 5️⃣ API ENDPOINTS (Backend)

## Kamera & Bewegung (Client-Side, kein Backend)

## Music Mode (✅ IMPLEMENTIERT!):
```
POST /api/music/start-song      - Song starten
POST /api/music/note-hit        - Note getroffen
POST /api/music/song-complete   - Song beendet (NUR SCORE!)
GET  /api/music/songs           - Verfügbare Songs
GET  /api/music/instruments     - Instrumente
GET  /api/music/high-scores     - Highscores pro Spieler
POST /api/music/jam/join        - Multiplayer Jam beitreten
```

## Creative Mode:
```
GET  /api/creative/prefabs      - Alle Prefabs
POST /api/creative/place        - Prefab platzieren
GET  /api/creative/schedule     - Najikas Tagesplan
POST /api/creative/room/add     - Raum hinzufügen
GET  /api/creative/rooms        - Alle Räume
```

---

# 6️⃣ DATEIEN ZU ERSTELLEN

## Backend:
- [x] `backend/api/music.py` - Music Mode API (KEINE BUFFS!)
- [ ] `backend/api/creative.py` - Creative Mode API
- [ ] `backend/services/najika_schedule.py` - Tagesablauf

## UE5:
- [ ] `BP_FortniteCamera` - Kamera Blueprint
- [ ] `IA_NajikaInput` - Input Actions
- [ ] `IMC_NajikaDefault` - Input Mapping
- [ ] `BP_MovementComponent` - Mit Crawl + Prone!
- [ ] `BP_InstrumentBase` - Instrument Basis
- [ ] `WBP_RhythmGame` - Rhythm UI Widget

## Flutter (Digivice):
- [ ] Vereinfachte Kamera-Steuerung (Touch)
- [ ] Music-Mode Mini-UI

---

*"EXPLOSION!!! Musik zum Spaß, Krabbeln zum Verstecken!" - Najika* 💥🎵🐍
