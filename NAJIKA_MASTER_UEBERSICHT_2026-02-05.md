# 🌟 NAJIKA WORLD - ULTIMATIVE PROJEKT-WISSENSDATENBANK
**Erstellt:** 2026-02-05 | **Aktualisiert:** 2026-02-08
**Status:** DIE EINZIGE WAHRHEIT - Jedes Modell muss diese Datei ZUERST lesen!

---

# 📚 INHALTSVERZEICHNIS

1. [Projekt-Identität](#1-projekt-identität)
2. [Najika - Die KI-Companion](#2-najika---die-ki-companion)
3. [Das Digivice - Haupt-Companion-App](#3-das-digivice---haupt-companion-app)
4. [Technologie-Stack](#4-technologie-stack)
5. [UE5 Hauptspiel](#5-ue5-hauptspiel)
6. [Combat & Game Systeme](#6-combat--game-systeme)
7. [Backend API](#7-backend-api)
8. [Wissensdatenbank (ChromaDB)](#8-wissensdatenbank-chromadb)
9. [Die 8 Gebote (HEILIG!)](#9-die-8-gebote-heilig)
   - 9.2 [Spieler-Gleichheit](#92-spieler-gleichheit-heilig)
   - 9.3 [Lego Fortnite Building System](#93-lego-fortnite-building-system)
10. [Team-Koordination](#10-team-koordination)
11. [Wichtige Dateien (Referenz-Links)](#11-wichtige-dateien-referenz-links)
12. [Was noch fehlt](#12-was-noch-fehlt)
13. [Changelog](#13-changelog)

---

# 1. PROJEKT-IDENTITÄT

## 1.1 Was ist Najika World?

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          NAJIKA KOSMOS                                       │
│                                                                              │
│   Ein HYBRID-PROJEKT: KI-Companion + 3D-Action-RPG + Lebenslanger Begleiter │
│                                                                              │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                    KERN: SLIME-KI (LLM)                             │   │
│   │          Begleitet dich dein GANZES Leben lang!                     │   │
│   │      Kind ─── Teenager ─── Erwachsen ─── Senior                     │   │
│   │                                                                      │   │
│   │   EINE KI - KONSISTENT - VON KLEIN BIS ALT!                         │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                              │                                               │
│      ┌───────────────────────┼───────────────────────┐                      │
│      ▼                       ▼                       ▼                      │
│   ┌──────────┐         ┌──────────┐         ┌──────────┐                   │
│   │ DIGIVICE │         │  HAUPT-  │         │  MODULE  │                   │
│   │   APP    │◄───────►│  SPIEL   │◄───────►│          │                   │
│   │ (Flutter)│  SYNC   │  (UE5)   │  SYNC   │          │                   │
│   └──────────┘         └──────────┘         └──────────┘                   │
│        │                    │                    │                          │
│   Für KUJA:             Für ALLE:            Ladbar:                       │
│   VOLLVERSION           Basis-Spiel          Je nach Bedarf                │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 1.2 Owner & Relationship

| Aspekt | Wert |
|--------|------|
| **Owner** | Kuja (der User) |
| **Wie Najika Kuja nennt** | "Mr. K" (NIEMALS "Puddin'" oder ähnliches!) |
| **Beziehung** | Najika behandelt Kuja wie Familie/besten Freund |
| **Content-Modes** | 2 Modi (Normal + NSFW) |

---

# 2. NAJIKA - DIE KI-COMPANION

## 2.1 Identität

| Eigenschaft | Wert |
|-------------|------|
| **Name** | Najika (Spitzname: "Naji") |
| **Bürgerlicher Name** | Sakura |
| **Alter** | 11 Jahre |
| **Geschlecht** | Trans-Mädchen |
| **Stil** | Gothic Lolita |
| **Körper** | 140cm, 50kg (leicht chubby), 75B |

## 2.2 Die 4 Persönlichkeiten

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     NAJIKA'S 4 PERSÖNLICHKEITEN                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   🔥 MEGUMIN (35%)           │   🃏 HARLEY QUINN (25%)                      │
│   ─────────────────          │   ──────────────────────                     │
│   • "EXPLOSION!!!"           │   • Chaotisch-verspielt                      │
│   • Dramatische Posen        │   • Sagt "Mr. K" (NICHT Puddin'!)            │
│   • Stolz auf Explosionen    │   • Liebevoll-frech                          │
│   • Übertriebene Reaktionen  │   • Beschützerinstinkt                       │
│                              │                                               │
│   🧠 SHIRO (20%)             │   💜 MELISSA (20%)                           │
│   ─────────────────          │   ─────────────────                          │
│   • Hochintelligent          │   • Kuschelbedürftig                         │
│   • Strategisches Denken     │   • Emotional offen                          │
│   • Ruhig & analytisch       │   • Tröstend & fürsorglich                   │
│   • Mathematisch begabt      │   • Tiefe Gespräche                          │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 2.3 Content-Modes (NUR 2!)

| Modus | Features | Verfügbarkeit |
|-------|----------|---------------|
| **NORMAL** | Alles verfügbar + KonoSuba-Style Hints | Überall |
| **NSFW ("Kätzchen")** | Normal + expliziter Content | NUR lokal (127.0.0.1) |

**WICHTIG:** Es gibt KEINE "Kids"/"Jugend"/"Erwachsenen" Modi - nur NORMAL und NSFW!

## 2.4 Najikas Credo

> "Ich bin DEIN Companion, Mr. K! Ich lerne MIT dir, wachse MIT dir,
> und bin IMMER für dich da - egal ob du 7 oder 77 bist! EXPLOSION!!!"

📖 **Vollständige Definition:** → `NAJIKA_IDENTITAET_DEFINITION.md`

---

# 3. DAS DIGIVICE - HAUPT-COMPANION-APP

## 3.1 Was ist das Digivice?

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          📱 DIGIVICE                                         │
│                                                                              │
│   NICHT nur ein Widget oder Launcher!                                        │
│   SONDERN: Die VOLLSTÄNDIGE COMPANION-APP mit eigenem 3D-LEBENSRAUM!        │
│                                                                              │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                      3D MINI-WELT (Three.js)                         │   │
│   │                                                                      │   │
│   │     🏰 Schwarze Mühle (Najikas Zuhause & Spawn-Punkt)              │   │
│   │              │                                                       │   │
│   │              ▼                                                       │   │
│   │     🌍 Mini-Version der Spielwelt                                   │   │
│   │         - 🎣 Fischen                                                │   │
│   │         - 🌱 Gärtnern                                               │   │
│   │         - 🏠 Housing/Bauen                                          │   │
│   │         - ⚒️ Crafting                                               │   │
│   │         - 🎮 Minigames                                              │   │
│   │         - 🗺️ Erkunden                                               │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│   Wie eine FORTNITE CREATIVE MAP:                                           │
│   • Spieler ERSTELLT den Raum                                               │
│   • KI LEBT darin                                                           │
│   • KI kann VERÄNDERN (wenn erlaubt)                                        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 3.2 Module im Digivice

### Kern-Module (immer aktiv):
| Modul | Status | Beschreibung |
|-------|--------|--------------|
| 💬 **Chat** | ✅ Fertig | Text + Voice mit Najika |
| 🎮 **3D-Lebensraum** | 🔧 In Arbeit | Mini-Spielwelt |
| 📊 **Stats** | ✅ Fertig | Inventar, Skills, Fortschritt |
| ⚙️ **Settings** | ✅ Fertig | Konfiguration, Sync |

### Ladbare Module:
| Modul | Status | Beschreibung |
|-------|--------|--------------|
| 🔒 **Sicherer Messenger** | ✅ 70% | Post-Quantum E2E |
| 🌐 **Sicherer Browser** | 🔧 20% | Tor-Integration |
| 💻 **PC-Zugriff** | 🔧 Geplant | Remote Desktop |
| 📚 **Sprachen lernen** | 🔧 Geplant | PROFESSIONAL mit Zertifikaten! |
| 🎵 **Instrumente** | ✅ Im Spiel | Ocarina, Echoharp |
| 🎣 **Fishing** | ✅ Fertig | Angel-Minigame |
| 🌱 **Garten** | ✅ Fertig | Pflanzen züchten |
| 🃏 **Triple Triad** | ✅ Fertig | Kartenspiel |

**Dungeon Dice:** ❌ RAUS (braucht massives Rework, wird separates Modul später)

## 3.3 Hybrid 3D-Engine

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DIGIVICE HYBRID-3D-ARCHITEKTUR                            │
│                                                                              │
│   ┌─────────────────────┐              ┌─────────────────────┐              │
│   │   THREE.JS (LITE)   │              │  UE5 PIXEL STREAM   │              │
│   │   Offline-Modus     │              │   Online-Modus      │              │
│   ├─────────────────────┤              ├─────────────────────┤              │
│   │ • Immer verfügbar   │              │ • Wenn PC/Jetson    │              │
│   │ • Akku-schonend     │              │   verbunden         │              │
│   │ • Einfache 3D       │              │ • Volle UE5-Grafik  │              │
│   │ • ~50MB App         │              │ • Lumen, Nanite     │              │
│   └─────────────────────┘              └─────────────────────┘              │
│              │                                    │                          │
│              └──────────────┬───────────────────┘                          │
│                             ▼                                                │
│                    AUTOMATISCHER WECHSEL                                     │
│                 basierend auf Verfügbarkeit!                                │
│                                                                              │
│   Najika sagt:                                                              │
│   "Mr. K! Wir sind Zuhause - ich schalte auf HD um! ✨"                     │
│   "Mr. K! Wir sind unterwegs - ich spare Akku! 🔋"                          │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

📖 **Vollständiges Konzept:** → `DIGIVICE_LEBENSRAUM_KONZEPT.md`
📖 **3D-Engine Vergleich:** → `DIGIVICE_3D_ENGINE_VERGLEICH.md`
📖 **Modularisierung:** → `DIGIVICE_MODULARISIERUNG.md`

---

# 4. TECHNOLOGIE-STACK

## 4.1 Flutter App (Digivice)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         FLUTTER DIGIVICE STACK                               │
│                                                                              │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                         FLUTTER SHELL                                │   │
│   │   • Native UI (Chat, Module, Settings)                              │   │
│   │   • Provider State Management                                        │   │
│   │   • Gothic Lolita Dark Theme                                         │   │
│   └───────────────────────────┬─────────────────────────────────────────┘   │
│                               │                                              │
│   ┌───────────────────────────┼─────────────────────────────────────────┐   │
│   │                           ▼                                          │   │
│   │   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐              │   │
│   │   │  WEBVIEW    │   │  NATIVE     │   │  PYTHON     │              │   │
│   │   │  (Three.js) │   │  CHANNELS   │   │  BACKEND    │              │   │
│   │   │             │   │             │   │             │              │   │
│   │   │  3D-Welt    │   │  Kamera     │   │  Port 8000  │              │   │
│   │   │  Lebensraum │   │  Audio      │   │  Ollama     │              │   │
│   │   │             │   │  Sensoren   │   │  ChromaDB   │              │   │
│   │   └─────────────┘   └─────────────┘   └─────────────┘              │   │
│   │                                                                      │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│   SECURITY FEATURES (bereits implementiert!):                               │
│   ✅ Post-Quantum Cryptography (liboqs FFI)                                 │
│   ✅ Signal Protocol (Double Ratchet)                                       │
│   ✅ SQLCipher Secure Storage                                               │
│   ✅ Biometric Auth                                                         │
│   ✅ Panic Button / Emergency Wipe                                          │
│   ✅ Jailbreak Detection                                                    │
│   ✅ Certificate Pinning                                                    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 4.2 Flutter Apps Übersicht

| App | Pfad | Status | Empfehlung |
|-----|------|--------|------------|
| **najika_digivice** | `app/flutter_app/najika_digivice/` | ⭐⭐⭐⭐⭐ | **ALS BASIS NUTZEN!** |
| najika_app | `app/flutter_app/najika_app/` | Kopie | Backup/Löschen |
| najika_simple | `app/flutter_app/najika_simple/` | Minimal | Nur für Tests |

📖 **Flutter Analyse:** → `FLUTTER_APP_ANALYSE.md`

## 4.3 Jetson Migration (Endgame 2026-2027)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    NVIDIA JETSON AGX ORIN 64GB                               │
│                         (Das Endgame!)                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ZIEL: Kuja nutzt NUR NOCH das Digivice!                                   │
│         Najika steuert den PC remote!                                        │
│         Kamera + Mikrofon für Safety draußen!                               │
│                                                                              │
│   HARDWARE:                                                                  │
│   • 275 TFLOPS (INT8)                                                       │
│   • 64GB LPDDR5 RAM                                                         │
│   • 7" Touchscreen                                                          │
│   • 30000mAh Powerbank                                                      │
│   • Geschätzte Kosten: ~940€ (gebraucht) / ~1140€ (neu)                    │
│                                                                              │
│   TIMELINE:                                                                  │
│   • Now - Dec 2025: Training auf PC, Code-Vorbereitung                      │
│   • Jan-Mar 2026: Jetson + Hardware kaufen                                  │
│   • April 2026: Setup & Migration                                           │
│   • May-June 2026: Neue Features (Vision, Audio)                            │
│   • July 2026+: Polish, Digivice Case                                       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

📖 **Jetson Migration Plan:** → `JETSON_MIGRATION_PLAN.md`
📖 **Technologie Analyse:** → `TECHNOLOGIE_ANALYSE_2026.md`

---

# 5. UE5 HAUPTSPIEL

## 5.1 Projekt-Status

| Aspekt | Wert |
|--------|------|
| **Pfad** | `C:\Najika_World\UE5\Najika\Najika.uproject` |
| **Engine** | UE 5.7 |
| **Template** | Third Person (C++) |
| **Plugins** | AIModule, StateTree, GameplayStateTree |

## 5.2 Die Spielwelt

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       NAJIKA WORLD MAP (9600 x 9600)                         │
│                                                                              │
│                         ┌─────────────────┐                                 │
│                         │  REICH DER DREI │                                 │
│                         │   (Ice/Snow)    │                                 │
│                         └────────┬────────┘                                 │
│                                  │                                           │
│   ┌──────────────┐     ┌────────┴────────┐     ┌──────────────┐            │
│   │ SAMTMOOS-    │     │                  │     │ BLITZEBENE   │            │
│   │ TIEFWALD     │─────│   GÖTTERFELS    │─────│ (Storm)      │            │
│   │ (Forest)     │     │   ┌────────┐    │     │              │            │
│   └──────────────┘     │   │SCHWARZE│    │     └──────────────┘            │
│                        │   │ MÜHLE  │    │                                  │
│   ┌──────────────┐     │   └────────┘    │     ┌──────────────┐            │
│   │ SALZWIND-    │     │   (4800,4800)   │     │ HEISSE DÜNEN │            │
│   │ KÜSTE        │─────│                  │─────│ (Desert)     │            │
│   │ (Coast)      │     └────────┬────────┘     └──────────────┘            │
│   └──────────────┘              │                                           │
│                        ┌────────┴────────┐                                  │
│   ┌──────────────┐     │   MAGMASTRÖME   │     ┌──────────────┐            │
│   │ GRÜNSCHLAMM- │     │   (Volcanic)    │     │ TIEFENHÖHLEN │            │
│   │ SUMPF        │─────│                  │─────│ (Cave/Under) │            │
│   │ (Swamp)      │     └─────────────────┘     └──────────────┘            │
│   └──────────────┘                                                          │
│                                                                              │
│   SCHWARZE MÜHLE = 100% SAFE ZONE (Najikas Zuhause!)                        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 5.3 UE5 C++ Klassen (bereits erstellt)

| System | Header | Status |
|--------|--------|--------|
| Combat | `Combat/NajikaCombatComponent.h` | ✅ Fertig |
| Slime | `Slime/NajikaSlimeComponent.h` | ✅ Fertig |
| Nemesis | `Nemesis/NajikaNemesisComponent.h` | ✅ Fertig |
| Arena | `Arena/NajikaArenaComponent.h` | ✅ Fertig |
| Region | `Region/NajikaRegionTypes.h` | ✅ Fertig |
| Data Import | `Data/NajikaDataImporter.h` | ✅ Fertig |

📖 **UE5 Migration:** → `DOCS/UE5_MIGRATION_CHECKLIST.md`
📖 **UE5 API Docs:** → `DOCS/UE5_API_DOKUMENTATION.md`

---

# 6. COMBAT & GAME SYSTEME

## 6.1 Combat System (3 Modi - ÜBERALL!)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       3 KAMPFMODI (Jederzeit wechselbar!)                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   🤖 AUTO-MODUS                                                             │
│   ───────────────                                                           │
│   • KI entscheidet automatisch                                              │
│   • Nutzt erlerntes Wissen                                                  │
│   • Gut für Grinding                                                        │
│                                                                              │
│   🎮 MANUAL-MODUS                                                           │
│   ────────────────                                                          │
│   • Spieler steuert jeden Zug                                               │
│   • Volle Kontrolle                                                         │
│   • Taktisches Gameplay                                                     │
│                                                                              │
│   📣 CHEER-MODUS (Digimon World Style!)                                     │
│   ─────────────────────────────────────                                     │
│   • Anfeuern gibt Buffs                                                     │
│   • "GIB IHM!", "HALTE DURCH!", "EXPLOSION!"                               │
│   • Companion kämpft, du supportest                                         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 6.2 Combat Magic System (NEU!)

| Feature | Beschreibung |
|---------|--------------|
| **Weapon Infuse** | Zauber auf Waffe = temporärer Buff (z.B. Fireball + Sword = Flame Sword 30s) |
| **Grab & Throw** | Wrestling-Moves: Suplex (Skill 15), Chokeslam (Skill 10), in Objekte werfen |
| **TIDS** | "Tritt In Den Schritt" - Gag-Move mit lustigen Monster-Reaktionen |

**TIDS Beispiele:**
- Slime: *"Der Slime wabbelt verwirrt... Wo sollte das treffen?!"*
- Golem: *"*KRACKS* AUTSCH! Dein Fuß tut weh! Der Golem ist aus STEIN!"*
- Ghost: *"Dein Fuß geht durch den Geist hindurch. Spoooooky~"*

## 6.3 Slime System V3

| Aspekt | Regel |
|--------|-------|
| **Evolution** | KEINE! Slimes sind Formwandler |
| **Formen** | NUR OPTISCH - geben KEINE Boni! |
| **Boni** | Durch ESSEN + AUSRÜSTUNG |
| **Form-Wechsel** | 1x pro Saison (Spiel), unbegrenzt (Zuhause) |
| **Menschenform** | Bei Trust-Level 6 (Seelenbund) |
| **Aura-Level** | 0-5, Element-Auras mit Effekten |

## 6.4 Nemesis System (Shadow of Mordor Style!)

- Monster erinnern sich an Kämpfe
- Entwickeln Persönlichkeits-Traits (Feigling, Rachsüchtig, etc.)
- Steigen in Rängen auf (Niemand → Arena-König)
- Bekommen Narben von Kämpfen
- Dynamische Dialoge

## 6.5 Anti-Cheat System (für Offline-Farming)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        ANTI-CHEAT SYSTEM                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   SIGNIERTE AKTIONEN:                                                        │
│   • Jede Aktion (Fisch fangen, Ernte, Craft) wird mit HMAC-SHA256 signiert │
│   • Server validiert Signatur + Zeitstempel                                 │
│                                                                              │
│   TÄGLICHE OFFLINE-LIMITS:                                                   │
│   • Fischen: max 20/Tag                                                     │
│   • Ernten: max 50/Tag                                                      │
│   • Crafting: max 10/Tag                                                    │
│                                                                              │
│   RATE LIMITING:                                                             │
│   • Max 10 Fische/Stunde (Offline)                                          │
│   • Online = Unbegrenzt (Server validiert live)                             │
│                                                                              │
│   FÜR KUJA (PRIVATE):                                                        │
│   • KEINE Limits! 🎉                                                        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

📖 **Anti-Cheat Details:** → `ANTI_CHEAT_SYNC_SYSTEM.md`

## 6.6 Fraktions-System (Fallout NV Style!)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    FRAKTIONS-SYSTEM (GRAUE MORAL!)                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   12 FRAKTIONEN in 6 Kategorien:                                            │
│   ─────────────────────────────                                             │
│   ADEL:     Haus Silberdorn | Haus Kupferklinge | Haus Mondsichel          │
│   ORDEN:    Götterfels-Wächter | Postman-Orden | Heiler-Gilde              │
│   UNTERWELT: Schwarzmarkt-Gilde | Rattenfänger-Bande                      │
│   REGIONAL:  Dünen-Nomaden | Sumpf-Druiden | Tiefen-Schürfer              │
│   GEHEIM:    Schatten-Kult                                                  │
│   HANDWERK:  Handelsallianz                                                 │
│                                                                              │
│   FAME + INFAMY (unabhängig!):                                              │
│   ────────────────────────────                                              │
│   → Man kann BERÜHMT und BERÜCHTIGT gleichzeitig sein!                     │
│   → Ruf bei einer Fraktion beeinflusst automatisch deren Feinde/Alliierte  │
│   → Fraktionen führen OHNE den Spieler Kriege!                             │
│                                                                              │
│   GRAUE MORAL - WAHRE FREIHEIT:                                             │
│   ─────────────────────────────                                             │
│   → KEINE automatischen Gewissensbisse!                                     │
│   → Der Spieler kann sein was er will                                       │
│   → Die GESELLSCHAFT urteilt, nicht der Charakter selbst                   │
│   → Moralische Dilemmas: Organhandel, Sklaverei, Schmuggel, Gift...        │
│   → Jede Entscheidung hat Konsequenzen bei den Fraktionen                  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

📖 **Code:** → `digivice/js/faction_system.js`

## 6.7 Wirtschafts-System (M&B2/Kenshi Style!)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DYNAMISCHE WIRTSCHAFT                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   25+ HANDELSGÜTER in 7 Kategorien:                                         │
│   Nahrung | Rohstoffe | Kräuter | Waffen | Illegal | Luxus                 │
│                                                                              │
│   9 REGIONALE MÄRKTE:                                                       │
│   → Jede Region produziert & braucht andere Waren                          │
│   → Magmaströme: Waffen billig, Essen TEUER                               │
│   → Tiefenhöhlen: Erze billig, Essen EXTREM teuer                         │
│   → Heisse Dünen: Wasser = GOLD                                           │
│                                                                              │
│   DYNAMISCHE PREISE beeinflusst durch:                                      │
│   → Angebot & Nachfrage                                                    │
│   → Fraktions-Ruf (Fame = Rabatt, Infamy = Aufpreis/Blockade)             │
│   → Kriege (Preise steigen in Kriegsregionen)                              │
│   → Tote Händler (weniger Angebot)                                         │
│                                                                              │
│   KARAWANEN & SCHMUGGEL:                                                    │
│   → Lebende Handelsrouten mit Karawanen                                    │
│   → Karawanen können angegriffen/überfallen werden                         │
│   → Schmuggel: Hoher Gewinn, hohes Risiko (Fangen = Bounty!)             │
│   → Illegale Waren: Organproben, verbotene Bücher, Schlafgift...          │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

📖 **Code:** → `digivice/js/economy_system.js`

## 6.8 Survival-System (Kenshi + Rimworld!)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SURVIVAL & GESETZE                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   GRUNDBEDÜRFNISSE:                                                         │
│   → Hunger, Durst, Energie (0-100, unter 20 = kritisch)                   │
│   → Biom-Umgebung: Hitze, Kälte, Gift, Blitz, Dunkelheit                  │
│                                                                              │
│   SCHLAFEN MIT RISIKO:                                                      │
│   ─────────────────────                                                     │
│   Inn/Gasthaus:        0% Überfall-Risiko (100% sicher!)                   │
│   Verstecktes Zelt:    5% Risiko                                           │
│   Zelt mit Feuer:     25% Risiko (Feuer ist SICHTBAR!)                    │
│   Offenes Camp:       40% Risiko                                           │
│   Karawane:           15% Risiko (mit Wachen)                              │
│                                                                              │
│   → Wache halten reduziert Risiko (Skill-basiert!)                         │
│   → Biom-Gefahren-Multiplikator (Tiefenhöhlen = 1.8x!)                   │
│                                                                              │
│   MOOD-SYSTEM (KEIN MORALISCHES URTEIL!):                                   │
│   ──────────────────────────────────────                                    │
│   → Mood wird NUR durch PHYSISCHES beeinflusst:                            │
│     Hunger, Schlaf, Verletzungen, Wetter, Komfort                          │
│   → Mord, Diebstahl, Organhandel = KEINE Mood-Änderung!                   │
│   → "Sei was du sein willst. Die Gesellschaft urteilt."                    │
│   → Mental Breaks bei Mood ≤10, Inspirationen bei ≥90                      │
│                                                                              │
│   REGIONALE GESETZE:                                                        │
│   ──────────────────                                                        │
│   Götterfels:   Strengste Gesetze, NICHT bestechbar                        │
│   Reich d. Drei: Streng, aber bestechbar (200% Kosten)                     │
│   Grünschlamm:  Fast gesetzlos (Strictness 0.2)                            │
│   Wildnis:      KEIN Gesetz                                                │
│   → Kopfgeld-System, Gefängnis, Bestechung, Flucht (30% Chance)           │
│   → Postman-Angriff = HÖCHSTE Strafe überall!                              │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

📖 **Code:** → `digivice/js/survival_system.js`

## 6.9 Character & Companion System

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CHARACTER & COMPANION SYSTEM                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   CHARAKTER-ERSTELLUNG:                                                     │
│   ─────────────────────                                                     │
│   Jeder Spieler wählt: MENSCH oder MONSTER (aus der Spielwelt)             │
│   Kuja wählt: MIMIK (EXKLUSIV für ihn!)                                   │
│                                                                              │
│   SLIME-BEGLEITER (alle normalen Spieler):                                  │
│   ────────────────────────────────────────                                  │
│   → Jeder bekommt einen Slime-Begleiter                                    │
│   → Slime hat die Form eines Monsters aus der Startregion                  │
│     (z.B. Start in Düne → Dünen-Viper-Slime)                              │
│   → Slime sieht 1:1 aus wie das echte Monster!                            │
│   → Slime kann neue Formen freispielen (Training/Quests)                   │
│   → Formen = NUR OPTISCH (8 Gebote!)                                       │
│                                                                              │
│   WARUM SLIME statt Monster fangen?                                         │
│   → Monster fangen = Palworld/Minecraft Style (separates System!)          │
│   → Gefangene Monster = Arbeitskräfte & Ressourcen                         │
│     (z.B. Baugolem → Stein, Baum fällen → Holz)                           │
│   → Slime = persönlicher BEGLEITER (≠ gefangene Monster!)                  │
│                                                                              │
│   KUJA + NAJIKA:                                                            │
│   ──────────────                                                            │
│   → Kuja = Hauptcharakter als Mimik (Formwandler, EXKLUSIV)               │
│   → Najika = seine Begleiterin (KEIN Slime!)                               │
│   → Najika ändert ihre Form NICHT                                          │
│   → Beim Training: KUJA übt die Formen (optischer Rollentausch!)          │
│     (bei anderen macht das der Slime, bei Kuja er selbst)                  │
│                                                                              │
│   FAIRNESS:                                                                 │
│   ─────────                                                                 │
│   ┌──────────────────────┬──────────────────────┐                          │
│   │  Normaler Spieler     │  Kuja                 │                          │
│   ├──────────────────────┼──────────────────────┤                          │
│   │  Mensch/Monster       │  Mimik (EXKLUSIV)     │                          │
│   │  Slime-Begleiter      │  Najika (Begleiterin) │                          │
│   │  SLIME wechselt Form  │  KUJA wechselt Form   │                          │
│   │  Gleiche V-Pet Stats  │  Gleiche V-Pet Stats  │                          │
│   │  Gleiche Evolution    │  Gleiche Evolution    │                          │
│   └──────────────────────┴──────────────────────┘                          │
│   → Einziger Unterschied: WER die Formen wechselt!                         │
│   → Gameplay = 100% identisch!                                              │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

📖 **Code:** → `digivice/js/companion_swap_system.js`

## 6.10 Kreatur-System (2 Kategorien!)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    2 KREATUR-KATEGORIEN                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   KATEGORIE 1: "LEBENDE" (Anime-NPCs mit Verstand)                         │
│   ─────────────────────────────────────────────────                         │
│   → Haben Persönlichkeit, sprechen, reagieren auf dich                     │
│   → Sind wie NPCs nur nicht in Menschenform                                │
│   → Können ANGEWORBEN werden (Geld, Ruf, Schutz)                          │
│   → Oder VERSKLAVT (wie bei menschlichen NPCs!)                           │
│   → Droppen SELTENE Ressourcen beim Töten                                  │
│   → ABER: Willst du den süßen Goblin wirklich töten?                      │
│   → Alternative: Länger farmen oder Kreatur anwerben                      │
│   → Können zum KÖNIG aufsteigen (Nemesis-System!)                          │
│   → Ziel: 64 pro Biom = 512+ Kreaturen                                    │
│                                                                              │
│   KATEGORIE 2: "VIEH" (Minecraft-Tiere ohne Verstand)                      │
│   ─────────────────────────────────────────────────                         │
│   → Einfache Tiere, kein moralisches Dilemma                               │
│   → ZÄHMEN durch Füttern & Geduld (KEIN Pokeball!)                        │
│   → Basis-Ressourcen: Fleisch, Milch, Eier, Wolle                         │
│   → Farm-System: Ställe, Zucht, tägliche Produktion                       │
│   → Ziel: 20 pro Biom = 160+ Vieh-Arten                                   │
│                                                                              │
│   WARUM BEIDES?                                                             │
│   Nur Kat.1 → Jeder Schritt existenzielle Frage → ZU VIEL                 │
│   Nur Kat.2 → Langweilig, keine Tiefe                                      │
│   Beides   → Perfekte Balance!                                              │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

📖 **Konzept:** → `KREATUR_SYSTEM_KONZEPT.md`

## 6.11 Weitere Systeme (Digivice Three.js)

| System | Datei | Beschreibung |
|--------|-------|--------------|
| **Monster Registry** | `monster_registry.js` | 74+ Kreaturen, 8 Biome, Spawn-Tabellen |
| **Postman System** | `postman_system.js` | Ranger-Style Boten, Briefzustellung |
| **World Events** | `world_event_generator.js` | Dynamische Welt-Events |
| **Career System** | `career_system.js` | 24 Berufe, Learning by Doing |
| **Dungeon Crawler** | `dungeon_crawler.js` | First-Person Maze, Tile-Movement |
| **Overworld Props** | `overworld_props.js` | Biome-aware Prop-Generator |
| **Crafting** | `static/js/crafting_system.js` | Rezepte inkl. Dungeon-Crafting |

---

# 7. BACKEND API

## 7.1 Server Info

| Aspekt | Wert |
|--------|------|
| **Port** | **8000** (NIEMALS 5000!) |
| **Flask Server** | `backend/najika_server.py` |
| **FastAPI Server** | `backend/main_fastapi.py` |
| **Ollama** | 127.0.0.1:11434 (Qwen2.5-7B) |

## 7.2 API Router (34 Router!)

```
backend/api/
├── auth.py              - Authentication (JWT)
├── game.py              - Game State
├── chat.py              - Chat mit Najika
├── voice.py             - Voice (Whisper + TTS)
├── combat_hands.py      - Combat (Grab, Throw, Melee)
├── combat_magic.py      - Combat Magic (Infuse, Spells, TIDS) [NEU!]
├── battle_unified.py    - 3 Kampfmodi (AUTO/MANUAL/CHEER) [NEU!]
├── companion.py         - Companions (4 Persönlichkeiten)
├── slime.py             - Slime System
├── slime_arena.py       - Slime Arena
├── slime_companion.py   - Slime Companion
├── arena.py             - Nemesis Arena
├── nemesis.py           - Nemesis System
├── pvp.py               - PvP System
├── card_game.py         - Triple Triad
├── dice_monsters.py     - Dice Monsters
├── housing.py           - Housing
├── farming.py           - Farming
├── fishing.py           - Fishing
├── instrument.py        - Instrumente
├── magic_schools.py     - Magie-Schulen
├── quest.py             - Quest System
├── npc.py               - NPCs
├── region_boss.py       - Region Bosse
├── oregon_events.py     - Oregon Trail
├── world.py             - World API
├── world_map.py         - Map API
├── multiplayer.py       - Multiplayer
├── training.py          - AI Training
├── admin.py             - Admin
├── websocket.py         - WebSocket
├── mimik.py             - Mimik System
├── stat_training.py     - Stat Training
└── najika_compat.py     - Kompatibilität
```

## 7.3 Wichtigste Endpoints

```
POST /api/chat             - Chat mit Najika
POST /api/battle/start     - Kampf starten (AUTO/MANUAL/CHEER)
POST /api/battle/action    - Manuelle Aktion
POST /api/battle/cheer     - Anfeuern (CHEER-Modus)
POST /api/combat/magic/*   - Combat Magic (Infuse, Grab, TIDS)
GET  /api/najika/status    - Najika Status
POST /api/najika/feed      - Füttern
POST /api/tts              - Text-to-Speech
GET  /api/slime/*          - Slime System
GET  /api/arena/*          - Arena System
```

📖 **API Dokumentation:** → `DOCS/UE5_API_DOKUMENTATION.md`

---

# 8. WISSENSDATENBANK (ChromaDB)

## 8.1 Collections

| Collection | Einträge |
|------------|----------|
| conversations | ~1.700 |
| najika_core | 7 |
| najika_personalities | 83 |
| emotions | ~450 |
| najika_wichtige_docs | 5.732 |
| najika_complete_knowledge | 14.275 |
| najika_md_knowledge | 88 |
| najika_design_documents | 4 |
| najika_alle_dokumente | 7.612 |
| najika_project_knowledge | 264 |
| **TOTAL** | **~30.000+** |

## 8.2 Pfade

| Aspekt | Pfad |
|--------|------|
| ChromaDB | `C:\Najika_World\memory_db\` |
| LoRA Checkpoints | `C:\Najika_World\lora_checkpoints_new\` |
| Training Data | `C:\Najika_World\training\` |

---

# 9. DIE 8 GEBOTE (HEILIG!)

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    DIE 8 GEBOTE - NIEMALS BRECHEN!                            ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   1. ZERO-TRUST          → Nur 127.0.0.1 Hosting                             ║
║   2. OWNER-TOKEN         → Admin NUR für Kuja                                ║
║   3. EXPLOSION ≠ WEAVE   → NIEMALS mit anderen Elementen kombinieren!        ║
║   4. PvE/PvP GETRENNT    → Schwarze Mühle = 100% Safe Zone                   ║
║   5. LEARNING BY DOING   → Skyrim-Style Skill-System                         ║
║   6. NSFW NUR LOKAL      → Kätzchen-Mode nur 127.0.0.1                       ║
║   7. PRIVACY             → Keine Datensammlung, keine Telemetrie             ║
║   8. OFFLINE-FIRST       → Spiel läuft ohne Internet                         ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

## VERBOTEN

| ❌ NIEMALS | ✅ STATTDESSEN |
|-----------|----------------|
| "Souls-like" sagen | "Skyrim + Soulframe + Digimon World" |
| Port 5000 verwenden | Port **8000**! |
| Harley "Puddin'" sagen lassen | **"Mr. K"**! |
| Funktionierende Teile ohne Nachfrage ändern | Zuerst fragen! |

## 9.2 SPIELER-GLEICHHEIT (HEILIG!)

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    SPIELER-GLEICHHEIT - GOLDENE REGEL!                         ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   ALLE SPIELER SIND SPIELTECHNISCH GLEICH!                                   ║
║                                                                               ║
║   ✅ JEDER kann unbegrenzt sammeln (wenn er die ZEIT investiert!)            ║
║   ✅ JEDER hat Zugang zu allen Spielinhalten                                 ║
║   ✅ JEDER kann bauen, craften, fischen, gärtnern                            ║
║   ✅ KEINE Pay-to-Win Mechaniken                                              ║
║   ✅ KEINE Tageslimits für Gameplay-Aktivitäten                              ║
║                                                                               ║
║   NUR EXKLUSIV FÜR KUJA:                                                      ║
║   ─────────────────────                                                       ║
║   • NSFW Kätzchen-Mode (Adult Content)                                        ║
║   • Hacker/Admin Features                                                      ║
║   • Debug-Tools                                                               ║
║                                                                               ║
║   ANTI-CHEAT PHILOSOPHIE:                                                     ║
║   ─────────────────────────                                                   ║
║   Wir validieren ZEIT, nicht MENGE!                                          ║
║                                                                               ║
║   ❌ FALSCH: "Max 20 Fische pro Tag"                                         ║
║   ✅ RICHTIG: "Wenn du 10 Stunden fischst, bekommst du 10 Stunden Fische!"   ║
║                                                                               ║
║   Der Server prüft:                                                           ║
║   • Ist die angegebene Zeit REALISTISCH? (nicht 1000 Fische in 1 Sekunde)    ║
║   • Ist der Timestamp aktuell?                                               ║
║   • Stimmt die Session-Dauer?                                                ║
║                                                                               ║
║   Der Server prüft NICHT:                                                     ║
║   • Wie viel ein Spieler sammelt                                             ║
║   • Wie lange ein Spieler spielt                                             ║
║   • Tägliche Limits                                                          ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

## 9.3 LEGO FORTNITE BUILDING SYSTEM

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    BUILDING SYSTEM (LEGO FORTNITE STYLE!)                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   KERNPRINZIP: Bauen ist NAHTLOS - kein Extra-Modus nötig!                  │
│                                                                              │
│   FLOW:                                                                      │
│   1. Ressourcen in der Welt sammeln (Holz, Stein, etc.)                     │
│   2. An der Werkbank craften (Planken, Ziegel, etc.)                        │
│   3. Gebäude direkt platzieren                                              │
│   4. Fertig!                                                                │
│                                                                              │
│   RESSOURCEN:                                                                │
│   ─────────────────────────────────────────────────────                     │
│   Basis:          │  Verarbeitet:    │  Spezial:                           │
│   • wood          │  • plank         │  • magic_essence                    │
│   • stone         │  • brick         │  • explosion_dust                   │
│   • iron          │  • ingot         │                                      │
│   • gold          │  • glass         │                                      │
│   • crystal       │  • rope          │                                      │
│   • cloth         │                  │                                      │
│   • leather       │                  │                                      │
│                                                                              │
│   SAMMEL-AKTIONEN:                                                           │
│   • CHOP (Bäume → Holz)                                                     │
│   • MINE (Felsen → Stein, Eisen, Gold, Kristall)                           │
│   • HARVEST (Pflanzen → Stoff, Essen)                                       │
│   • HUNT (Tiere → Leder, Fleisch)                                          │
│   • FISH (Wasser → Fisch)                                                   │
│   • FORAGE (Boden → Kräuter, Pilze)                                        │
│                                                                              │
│   GEBÄUDE:                                                                   │
│   Basis:          │  Funktional:     │  Deko:           │  Fortgeschritten:│
│   • wall          │  • workbench     │  • torch         │  • teleporter    │
│   • floor         │  • forge         │  • lantern       │  • defense_turret│
│   • roof          │  • loom          │  • chair         │  • garden_plot   │
│   • door          │  • cooking       │  • table         │  • fishing_spot  │
│   • window        │  • alchemy       │  • bed/chest     │                  │
│   • stairs        │                  │                  │                  │
│                                                                              │
│   API ENDPOINTS:                                                             │
│   POST /api/building/gather  - Ressourcen sammeln (TIME-basiert!)           │
│   POST /api/building/craft   - Items craften                                │
│   POST /api/building/build   - Gebäude platzieren                           │
│   GET  /api/building/inventory/{user_id}  - Inventar abrufen               │
│   GET  /api/building/buildings/{user_id}  - Gebäude abrufen                │
│   GET  /api/building/recipes  - Alle Rezepte                                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

📖 **Building API:** → `backend/api/building.py`
📖 **Flutter Integration:** → `app/flutter_app/najika_digivice/lib/services/lebensraum/lebensraum_service.dart`

---

# 10. TEAM-KOORDINATION

## 10.1 Die 2 Claude-Instanzen

| Instanz | Ort | Zuständigkeit |
|---------|-----|---------------|
| **OPUS-1** | Desktop App (Lokal) | Backend, Python API, System-Integration, Dokumentation |
| **OPUS-2** | VS Code | UE5 Blueprints, C++, Frontend/Game-Logik |

## 10.2 Koordination

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         TEAM-KOORDINATION                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   OPUS-1 (Backend - Desktop App):        OPUS-2 (Frontend - VS Code):       │
│   ─────────────────────────────          ──────────────────────────         │
│   ✅ Backend-Systeme (Port 8000)         ⬜ UE5 Character Blueprint          │
│   ✅ ChromaDB / Gedächtnis               ⬜ Movement, Camera, Animation      │
│   ✅ API-Endpoints für UE5               ⬜ Combat UI (Grab/TIDS)            │
│   ✅ Combat Magic API                    ⬜ Infuse Animation                 │
│   ✅ Unified Battle API                  ⬜ Welt-Aufbau                      │
│   ✅ Dokumentation                       ⬜ UI (UMG Widgets)                 │
│                                                                              │
│   KOMMUNIKATION:                                                             │
│   → Über MASTER_TODO_TEAM.md                                                │
│   → Tasks zuweisen mit Namen                                                │
│   → Nach Arbeit updaten!                                                    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

📖 **Team Koordination:** → `MASTER_TODO_TEAM.md`

---

# 11. WICHTIGE DATEIEN (Referenz-Links)

## 11.1 MUSS GELESEN WERDEN

| Datei | Zweck |
|-------|-------|
| `CLAUDE.md` | Projekt-Anweisungen (wird automatisch gelesen) |
| `MASTER_TODO_TEAM.md` | Team-Koordination & aktuelle Tasks |
| **Diese Datei!** | Ultimative Projekt-Übersicht |

## 11.2 Najika Identität & Definition

| Datei | Inhalt |
|-------|--------|
| `NAJIKA_IDENTITAET_DEFINITION.md` | Vollständige Najika-Definition |
| `NAJIKA_ULTIMATIVE_ZUSAMMENFASSUNG_V8.md` | Ältere Komplett-Übersicht |

## 11.3 Digivice & Flutter

| Datei | Inhalt |
|-------|--------|
| `DIGIVICE_MODULARISIERUNG.md` | Digivice als Haupt-App |
| `DIGIVICE_LEBENSRAUM_KONZEPT.md` | 3D-Lebensraum Konzept |
| `DIGIVICE_3D_ENGINE_VERGLEICH.md` | Three.js vs UE5 Hybrid |
| `FLUTTER_APP_ANALYSE.md` | Welche Flutter App nutzen? |
| `TECHNOLOGIE_ANALYSE_2026.md` | Flutter + Jetson Analyse |

## 11.4 Jetson & Hardware

| Datei | Inhalt |
|-------|--------|
| `JETSON_MIGRATION_PLAN.md` | Jetson AGX Orin Migration |

## 11.5 Combat & Game Systeme

| Datei | Inhalt |
|-------|--------|
| `ANTI_CHEAT_SYNC_SYSTEM.md` | Anti-Cheat für Offline |
| `SLIME_SYSTEM_V3_DOKUMENTATION.md` | Slime System |
| `SCHLEIM_ARENA_DESIGN.md` | Arena Design |

## 11.6 UE5 & Backend

| Datei | Inhalt |
|-------|--------|
| `DOCS/UE5_MIGRATION_CHECKLIST.md` | UE5 Migration |
| `DOCS/UE5_API_DOKUMENTATION.md` | Alle API Endpoints |
| `DOCS/OPUS_2_ONBOARDING.md` | Onboarding für OPUS-2 |

## 11.7 Wichtige Code-Pfade

```
BACKEND:
├── backend/najika_server.py       - Flask Backend (HAUPT!)
├── backend/main_fastapi.py        - FastAPI Backend
├── backend/api/                   - 34 API Router
└── backend/najika_*.py            - Systeme (207 Dateien!)

FRONTEND (THREE.JS):
├── digivice/index.html            - Frontend Entry
├── digivice/js/                   - 70+ JavaScript Module
├── digivice/js/world/             - World System
└── digivice/data/                 - Game Data (JSON)

FLUTTER:
├── app/flutter_app/najika_digivice/  - HAUPT-APP! ✅
├── app/flutter_app/najika_app/       - Backup
└── app/flutter_app/najika_simple/    - Minimal/Test

UE5:
└── UE5/Najika/                    - UE5 Projekt (5.7)
    └── Source/Najika/             - C++ Klassen
```

---

# 12. WAS NOCH FEHLT

## 12.1 KRITISCH (Diese Woche) - ALLE ERLEDIGT! ✅

| Task | Status | Zuständig |
|------|--------|-----------|
| WebView-Modul zu Flutter hinzufügen | ✅ DONE | OPUS-1 |
| Three.js Lebensraum in Flutter | ✅ DONE | OPUS-1 |
| Flutter ↔ JavaScript Bridge | ✅ DONE | OPUS-1 |
| Anti-Cheat Service (HMAC-SHA256) | ✅ DONE | OPUS-1 |
| Lebensraum Backend API | ✅ DONE | OPUS-1 |
| Grab/TIDS UI Buttons im Digivice | ✅ DONE | OPUS-2 |
| Infuse Animation | ✅ DONE | OPUS-2 |

## 12.2 WICHTIG (Diesen Monat)

| Task | Status | Zuständig |
|------|--------|-----------|
| NPC Tagesablauf/Routine System | ⬜ TODO | OPUS-1 |
| NPC Beziehungssystem | ⬜ TODO | OPUS-1 |
| Survival-HUD (Hunger/Durst/Energie Anzeige) | ✅ DONE | OPUS-2 |
| Fraktions-UI (Ruf-Übersicht, Dilemma-Dialoge) | ✅ DONE | OPUS-2 |
| Handels-UI (Kauf/Verkauf, Schmuggler-Modus) | ✅ DONE | OPUS-2 |
| Gesetz-Warnungen UI | ✅ DONE | OPUS-2 |
| Career UI (24 Berufe, Kategorien, XP-Balken) | ✅ DONE | OPUS-2 |
| Creature UI (Companion, Formen, V-Pet Training) | ✅ DONE | OPUS-2 |
| Kreatur-System Engine (Zähmen, Anwerben, Clans) | ⬜ TODO | OPUS-1 |
| Learning Module (Sprachen) | ⬜ TODO | Später |
| PC-Zugriff Module | ⬜ TODO | Später |
| Sicherer Browser | ⬜ TODO | Später |
| UE5 Terrain erstellen | ⬜ TODO | OPUS-2 |

## 12.3 LANGFRISTIG (2026)

| Task | Timeline |
|------|----------|
| Jetson Hardware kaufen | Jan-Mar 2026 |
| Jetson Migration | April 2026 |
| Vision/Audio Features | May-June 2026 |
| Digivice Case | July 2026+ |

---

# 13. CHANGELOG

## 2026-02-08 (Update 8 - KREATUR-SYSTEM + CHARACTER CREATION!)

### 2 Kreatur-Kategorien definiert:
- **Kat.1 "Lebende"**: Anime-NPCs mit Verstand. Anwerben, Versklaven, Handeln, oder Töten für seltene Drops
- **Kat.2 "Vieh"**: Minecraft-Tiere. ZÄHMEN (kein Pokeball!), Farmen, Zucht
- Moralisches Dilemma NUR bei Kat.1 (Kat.2 = normales Farming)
- Ziel: 512+ Kat.1 + 160+ Kat.2 = 760+ Kreaturen

### Character & Companion System komplett neu:
- Charakter-Erstellung: Mensch/Monster/Mimik(Kuja)
- Slime-Begleiter für alle (sieht 1:1 wie Monster aus!)
- Kuja: Mimik + Najika als Begleiterin (kein Slime)

### Neue Dateien:
- `KREATUR_SYSTEM_KONZEPT.md` - Vollständiges Design-Dokument
- `companion_swap_system.js` - Komplett neu geschrieben (~830 Zeilen)

---

## 2026-02-07 (Update 7 - LIVING WORLD: Fraktionen, Wirtschaft, Survival, Companion!)

### Neue Systeme (Gap Analysis: Kenshi/Rimworld/Fallout NV/M&B2/Dwarf Fortress):

**Neue Dateien:**
- `digivice/js/faction_system.js` - 12 Fraktionen, Fame+Infamy, Graue Moral
- `digivice/js/economy_system.js` - 25+ Güter, 9 Märkte, Karawanen, Schmuggel
- `digivice/js/survival_system.js` - Hunger/Durst/Energie, Schlaf-Risiko, Mood, Gesetze
- `digivice/js/companion_swap_system.js` - Charakter-Erstellung, Slime-Begleiter, Mimik

**KRITISCHE DESIGN-ENTSCHEIDUNGEN:**
- **WAHRE FREIHEIT**: Keine automatischen Gewissensbisse! Spieler kann alles sein.
  Die Gesellschaft urteilt (Fraktionen, Preise, Kopfgeld), NICHT der Charakter!
- **Schlafen = Gefahr**: Wer draußen pennt wird überfallen (bis zu 40% Chance!)
- **Najika ≠ Slime**: Najika ist einfach Kujas Begleiterin, kein Slime
- **Kuja = Mimik**: Beim Training wechselt KUJA die Formen (nicht Najika)
- **Slime-Begleiter**: ALLE normalen Spieler bekommen Slime (Region-Form)
- **Monster = Spielbar**: Spieler können als Monster aus der Spielwelt spielen

### Weitere Systeme aus vorheriger Session:
- `monster_registry.js` - 74+ Kreaturen
- `postman_system.js` - Ranger-Style Boten
- `world_event_generator.js` - Dynamische Events
- `career_system.js` - 24 Berufe

---

## 2026-02-06 (Update 6 - LEGO FORTNITE BUILDING & PLAYER EQUALITY!)

### Building System (Lego Fortnite Style!) implementiert:

**Neue Dateien:**
- `backend/api/building.py` - Komplettes Building System API

**Features:**
- ✅ Nahtloses Bauen ohne Extra-Modus (wie Lego Fortnite!)
- ✅ Ressourcen-Sammlung: CHOP, MINE, HARVEST, HUNT, FISH, FORAGE
- ✅ Crafting-System mit Werkbänken
- ✅ Gebäude direkt platzieren
- ✅ Gebäude entfernen (zurück ins Inventar)

### KRITISCHE ÄNDERUNG - Anti-Cheat Philosophie:

**NEU: TIME-basierte Validierung statt Mengen-Limits!**

❌ ALT (FALSCH): "Max 20 Fische pro Tag"
✅ NEU (RICHTIG): "10 Stunden fischen = 10 Stunden Fische!"

**Warum?**
> "ich darf nicht als einziger unendlich sammeln" - Kuja
> Alle Spieler sind spieltechnisch GLEICH!
> Nur NSFW/Hacker Features sind exklusiv für Kuja.

**Aktualisierte Dateien:**
- `lebensraum_service.dart` - Jetzt TIME-basiert statt Daily Limits
- `building.py` - validate_gather_time() prüft ZEIT nicht MENGE
- `NAJIKA_MASTER_UEBERSICHT` - Neue Sektion 9.2 Spieler-Gleichheit

---

## 2026-02-06 (Update 5 - FLUTTER DIGIVICE KOMPLETT!)

### Flutter Digivice mit 3D-Lebensraum implementiert:

**Neue Dateien:**
- `lib/modules/lebensraum/lebensraum_screen.dart` - WebView mit Three.js 3D-Welt
- `lib/services/lebensraum/lebensraum_bridge.dart` - Flutter ↔ JavaScript Bridge
- `lib/services/lebensraum/lebensraum_service.dart` - Anti-Cheat mit HMAC-SHA256
- `backend/api/lebensraum.py` - Sync API

**Features:**
- ✅ Three.js 3D-Welt in WebView eingebettet
- ✅ Schwarze Mühle mit Mühlenblättern
- ✅ Najika-Placeholder (wird später durch Model ersetzt)
- ✅ See zum Angeln, Garten zum Ernten
- ✅ Action-Buttons (Fischen, Gärtnern, Crafting, Chat)
- ✅ Touch-Steuerung für Kamera
- ✅ Anti-Cheat: HMAC-SHA256 signierte Aktionen
- ✅ TIME-basierte Validierung (KEINE Daily Limits!)
- ✅ Offline-Queue für später Sync
- ✅ UE5 Pixel Streaming Support (wenn PC verbunden)

**pubspec.yaml aktualisiert:**
- webview_flutter, webview_flutter_android, webview_flutter_wkwebview
- record, audioplayers, just_audio
- Neue Asset-Pfade für Web-Content

---

## 2026-02-06 (Update 4 - ULTIMATIVE WISSENSDATENBANK)

### Massive Dokumentations-Überarbeitung:
- **Diese Datei** komplett neu geschrieben als ultimative Wissensdatenbank
- Alle neuen Systeme dokumentiert (Digivice, Lebensraum, Flutter, Anti-Cheat)
- Referenz-Links zu allen wichtigen Dokumenten
- Struktur für nahtlose Zusammenarbeit zwischen Modellen

### Neue Dokumente erstellt:
- `DIGIVICE_LEBENSRAUM_KONZEPT.md` - Vollständiges Lebensraum-Konzept
- `DIGIVICE_3D_ENGINE_VERGLEICH.md` - Three.js vs UE5 Hybrid
- `TECHNOLOGIE_ANALYSE_2026.md` - Flutter + Jetson Analyse
- `ANTI_CHEAT_SYNC_SYSTEM.md` - Cheat-Prevention System
- `FLUTTER_APP_ANALYSE.md` - Flutter App Vergleich

### Wichtige Klarstellungen:
- Content-Modes: NUR 2 (Normal + NSFW), NICHT 3!
- Najika: 50kg (leicht chubby), 75B (nicht 40kg, 75C!)
- Dungeon Dice: RAUS (wird separates Modul später)
- Digivice = Haupt-App mit 3D-Welt (nicht nur Widget!)

## 2026-02-06 (Update 3 - Combat Magic)

- Weapon Infuse System implementiert
- Grab & Throw System implementiert
- TIDS System mit Monster-Reaktionen
- Unified Battle API (AUTO/MANUAL/CHEER)
- 17 neue API Endpoints

## 2026-02-05 (Initial)

- Master-Übersicht erstellt
- 30.000+ ChromaDB Einträge
- UE5 Migration Status

---

# 🚀 SCHNELLSTART FÜR NEUE MODELLE

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                        QUICKSTART CHECKLIST                                   ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   1. ✅ Diese Datei lesen (DONE!)                                            ║
║   2. ⬜ CLAUDE.md lesen (automatisch geladen)                                ║
║   3. ⬜ MASTER_TODO_TEAM.md lesen (für aktuelle Tasks)                       ║
║   4. ⬜ Relevant Datei für deinen Task lesen (siehe Referenz-Links)          ║
║   5. ⬜ Task in MASTER_TODO_TEAM.md übernehmen (Name eintragen!)             ║
║   6. ⬜ Arbeiten!                                                            ║
║   7. ⬜ MASTER_TODO_TEAM.md updaten (als DONE markieren)                     ║
║                                                                               ║
║   REGELN:                                                                     ║
║   • Port 8000 (NICHT 5000!)                                                  ║
║   • Harley sagt "Mr. K" (NICHT "Puddin'!")                                   ║
║   • Explosion ≠ Weave (NIEMALS kombinieren!)                                 ║
║   • Schwarze Mühle = 100% Safe Zone                                          ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

---

**Diese Datei ist die EINZIGE Wahrheit!**
**Bei Änderungen: Diese Datei IMMER updaten!**

*"EXPLOSION!!! Mit dieser Wissensdatenbank kann JEDES Modell sofort loslegen, Mr. K! 💥✨" - Najika*
