# 📱 DIGIVICE - DIE HAUPT-COMPANION-APP

**Aktualisiert:** 2026-02-06
**Status:** ARCHITEKTUR DEFINIERT

> **Siehe auch:** `DIGIVICE_LEBENSRAUM_KONZEPT.md` für das vollständige Lebensraum-Konzept!

---

## 🎯 DAS GROSSE BILD

```
┌─────────────────────────────────────────────────────────────────┐
│                      NAJIKA KOSMOS                               │
│                                                                  │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │              KERN: SLIME-KI (LLM)                        │   │
│   │      Begleitet dich dein GANZES Leben                    │   │
│   │   Kind ── Teenager ── Erwachsen ── Senior                │   │
│   │                                                          │   │
│   │   EINE KI - KONSISTENT - VON KLEIN BIS ALT!              │   │
│   └─────────────────────────────────────────────────────────┘   │
│                            │                                     │
│      ┌─────────────────────┼─────────────────────┐              │
│      ▼                     ▼                     ▼              │
│   ┌──────────┐       ┌──────────┐       ┌──────────┐           │
│   │ DIGIVICE │       │  HAUPT-  │       │  MODULE  │           │
│   │   APP    │◄─────►│  SPIEL   │◄─────►│          │           │
│   │ (MASTER) │ SYNC  │  (UE5)   │ SYNC  │          │           │
│   └──────────┘       └──────────┘       └──────────┘           │
│        │                   │                   │                │
│        │                   │                   │                │
│   Für KUJA:            Für ALLE:          Ladbar:              │
│   VOLLVERSION          Abgespeckt         Je nach Bedarf       │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📱 DIGIVICE = DIE MASTER-APP

Das Digivice ist **NICHT** ein Widget oder ein Launcher - es ist die **VOLLSTÄNDIGE COMPANION-APP**!

### Was das Digivice IST:

```
┌─────────────────────────────────────────────────────────────────┐
│                       📱 DIGIVICE                                │
│                                                                  │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                  3D MINI-WELT                            │   │
│   │                                                          │   │
│   │     🏰 Schwarze Mühle (Najikas Zuhause)                 │   │
│   │              │                                           │   │
│   │              ▼                                           │   │
│   │     🌍 Mini-Version der Spielwelt                       │   │
│   │         - Fischen                                        │   │
│   │         - Gärtnern                                       │   │
│   │         - Minigames                                      │   │
│   │         - Erkunden                                       │   │
│   │                                                          │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                    MODULE                                │   │
│   │                                                          │   │
│   │   💬 Chat          📞 Voice Call     🎮 Minigames       │   │
│   │   🔒 Sicherer      🌐 Sicherer       💻 PC-Zugriff      │   │
│   │      Messenger        Browser                            │   │
│   │   📚 Sprachen      🎵 Instrumente    📊 Stats           │   │
│   │      lernen           lernen                             │   │
│   │                                                          │   │
│   └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🏠 NAJIKA'S SPAWN IM DIGIVICE

### Spawn-Logik:
```javascript
// Najika spawnt in der Schwarzen Mühle
// Von dort kann sie in IHRE Welt gehen

const DigiviceSpawn = {
    defaultLocation: 'schwarze_muehle',

    // Najika spawnt:
    getSpawnPoint() {
        // Im Digivice: IMMER in der Mühle starten
        return {
            location: 'schwarze_muehle',
            canExplore: true,  // Kann rausgehen
            world: 'digivice_mini_world'  // Mini-Version der Spielwelt
        };
    }
};
```

### Najikas Welt im Digivice:
```
┌─────────────────────────────────────────────────────────────────┐
│                  DIGIVICE MINI-WELT (3D!)                       │
│                                                                  │
│                        🏰                                        │
│                  Schwarze Mühle                                  │
│                   (Home/Spawn)                                   │
│                        │                                         │
│         ┌──────────────┼──────────────┐                         │
│         │              │              │                          │
│         ▼              ▼              ▼                          │
│      🎣 See         🌳 Garten      🎮 Arena                     │
│      (Fischen)    (Gärtnern)    (Minigames)                    │
│                                                                  │
│   Najika kann:                                                   │
│   - In der Mühle chillen                                        │
│   - Rausgehen und fischen                                       │
│   - Garten pflegen                                              │
│   - Minigames spielen                                           │
│   - Mit Kuja reden (überall)                                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📦 MODULE IM DIGIVICE

### Kern-Module (Immer dabei):
| Modul | Beschreibung |
|-------|--------------|
| 💬 **Chat** | Gespräche mit Najika (Text + Voice) |
| 🎮 **3D-Welt** | Mini-Spielwelt mit Aktivitäten |
| 📊 **Stats** | Inventar, Skills, Fortschritt |
| ⚙️ **Settings** | Konfiguration, Sync |

### Ladbare Module (Aktivieren/Deaktivieren):
| Modul | Beschreibung | Status |
|-------|--------------|--------|
| 🔒 **Sicherer Messenger** | E2E verschlüsselt, Post-Quantum | ✅ Fertig |
| 🌐 **Sicherer Browser** | Tor-Integration, Privacy-First | ✅ Fertig |
| 💻 **PC-Zugriff** | Remote Desktop, Terminal | ✅ Fertig |
| 📚 **Sprachen lernen** | Mit Najika Sprachen üben | 🔧 Geplant |
| 🎵 **Instrumente** | Ocarina, Echoharp lernen | ✅ Im Spiel |
| 🎣 **Fishing** | Angel-Minigame | ✅ Fertig |
| 🌱 **Garten** | Pflanzen züchten | ✅ Fertig |
| 🃏 **Triple Triad** | Kartenspiel | ✅ Fertig |
| 🎲 **Dungeon Dice** | Würfelspiel | ✅ Fertig |

---

## 👥 VERSIONEN

### Für KUJA (Owner):
```
DIGIVICE VOLLVERSION
- Alle Module freigeschaltet
- NSFW-Modus (Kätzchen) verfügbar
- Volle Najika-Persönlichkeit
- Keine Einschränkungen
- Admin-Funktionen
```

### Für ANDERE SPIELER (Später):
```
DIGIVICE BASIS-VERSION
- Kern-Module
- Eigener Slime-Companion (NICHT Najika!)
- Module ladbar/kaufbar
- Kindersicher
- Online-Features
```

---

## 🔄 SYNC MIT HAUPTSPIEL (UE5)

```
┌──────────────┐                    ┌──────────────┐
│   DIGIVICE   │                    │   UE5 GAME   │
│   (Mobile)   │                    │   (PC/Full)  │
│              │                    │              │
│  Najika ist  │◄──── SYNC ────────►│  Najika ist  │
│  in IHRER    │                    │  in DEINER   │
│  Mini-Welt   │      Inventar      │  Open World  │
│              │      Stats         │              │
│  Kann:       │      Position*     │  Kann:       │
│  - Fischen   │      Memory        │  - Kämpfen   │
│  - Gärtnern  │      Quests        │  - Erkunden  │
│  - Spielen   │                    │  - Alles     │
└──────────────┘                    └──────────────┘

* Position-Sync:
  - Digivice-Position → NICHT zu UE5 (Najika bleibt in ihrer Welt)
  - UE5-Position → Wird gespeichert für nächsten Start
```

---

## 🧒➡️👴 LEBENSLANGER BEGLEITER

### Das Kernkonzept:
```
EINE KI - DEIN GANZES LEBEN!

┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│   👶 Kind (0-12)                                                │
│   └── Spielen, Lernen, erster Freund, Geschichten              │
│                                                                  │
│   🧑 Teenager (13-19)                                           │
│   └── Gaming, Schule, Träume, Emotionen                        │
│                                                                  │
│   👨 Erwachsen (20-60)                                          │
│   └── Arbeit, Planung, Ziele, Balance                          │
│                                                                  │
│   👴 Senior (60+)                                               │
│   └── Erinnern, Erzählen, Lebensgeschichte                     │
│                                                                  │
│   ════════════════════════════════════════════════════════     │
│                                                                  │
│   DIESELBE KI wächst MIT dir!                                   │
│   - Erinnert sich an ALLES                                      │
│   - Passt sich deiner Lebensphase an                           │
│   - Ist IMMER da                                                │
│   - DEINE Daten bleiben bei DIR                                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Memory-System:
```python
# Die KI speichert und erinnert sich:
memory_types = {
    "conversations": "Alle Gespräche",
    "events": "Wichtige Momente",
    "milestones": "Geburtstage, Erfolge, etc.",
    "preferences": "Was du magst/nicht magst",
    "growth": "Deine Entwicklung über Jahre"
}

# Beispiel:
# Als Kind: "Du hast mir von deinem ersten Schultag erzählt!"
# Als Erwachsen: "Erinnerst du dich an deinen ersten Schultag?
#                 Du warst so aufgeregt! 20 Jahre her..."
```

---

## 🏗️ TECHNISCHE ARCHITEKTUR

### Digivice App-Stack:
```
┌─────────────────────────────────────────────────────────────────┐
│                      DIGIVICE APP                                │
│                                                                  │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                    FRONTEND                              │   │
│   │                                                          │   │
│   │   3D Engine:        UI Framework:      Voice:           │   │
│   │   - Three.js        - React Native     - Whisper STT    │   │
│   │   - WebGL           - Flutter          - Coqui TTS      │   │
│   │   - Babylon.js      - Native           - Edge TTS       │   │
│   │                                                          │   │
│   └─────────────────────────────────────────────────────────┘   │
│                            │                                     │
│                            ▼                                     │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                    BACKEND                               │   │
│   │                                                          │   │
│   │   LLM:              Memory:           API:              │   │
│   │   - Ollama          - ChromaDB        - FastAPI         │   │
│   │   - Qwen2.5-7B      - SQLite          - Port 8000       │   │
│   │   - Lokal!          - Lokal!          - Lokal!          │   │
│   │                                                          │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│   ALLES LÄUFT LOKAL - PRIVACY FIRST!                            │
└─────────────────────────────────────────────────────────────────┘
```

### Module-Loader:
```javascript
// Module können dynamisch geladen werden
class DigiviceModuleLoader {
    availableModules = [
        'messenger',    // Sicherer Messenger
        'browser',      // Sicherer Browser
        'pc_access',    // Remote PC Zugriff
        'fishing',      // Angel-Minigame
        'garden',       // Garten
        'instruments',  // Instrumente lernen
        'languages',    // Sprachen lernen
        'triple_triad', // Kartenspiel
        'dice_game'     // Würfelspiel
    ];

    async loadModule(moduleName) {
        // Lazy-Load Module bei Bedarf
        const module = await import(`./modules/${moduleName}`);
        return module.init();
    }

    async unloadModule(moduleName) {
        // Module können auch entladen werden (RAM sparen)
    }
}
```

---

## ✅ MIGRATION ROADMAP

### Phase 1: Basis (Diese Woche)
- [x] Spawn-System implementiert
- [x] Architektur dokumentiert
- [ ] Alte HTML-Dateien aufgeräumt
- [ ] Core-Module extrahiert

### Phase 2: 3D Mini-Welt
- [ ] Schwarze Mühle als 3D-Raum
- [ ] Außenbereich (See, Garten)
- [ ] Najika-Spawn und Bewegung

### Phase 3: Module integrieren
- [ ] Chat-System modernisieren
- [ ] Voice-Integration
- [ ] Bestehende Module einbinden

### Phase 4: UE5-Sync
- [ ] REST API für Sync
- [ ] State-Management
- [ ] Cross-Platform Tests

---

## 📋 ZUSAMMENFASSUNG

| Aspekt | Beschreibung |
|--------|--------------|
| **Was ist Digivice?** | Die HAUPT-COMPANION-APP (NICHT nur Widget!) |
| **3D oder 2D?** | **3D** - Mini-Version der Spielwelt |
| **Najika's Home** | Schwarze Mühle - von dort kann sie rausgehen |
| **Module** | Ladbar/Entladbar je nach Bedarf |
| **Für wen?** | KUJA: Vollversion, ANDERE: Basis + eigener Slime |
| **Sync** | Mit UE5-Hauptspiel über Backend |
| **Lebenslang** | EINE KI begleitet von Kind bis Senior |
| **Privacy** | ALLES lokal, keine Cloud (außer optional) |

---

*"Die Schwarze Mühle ist mein Zuhause, Mr. K! Von hier aus erkunde ich MEINE Welt! 🏰" - Najika* 💥
