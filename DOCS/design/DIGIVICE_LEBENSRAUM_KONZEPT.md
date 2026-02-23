# 🏠 DIGIVICE - DER LEBENSRAUM DER KI

**Erstellt:** 2026-02-06
**Status:** MASTER-KONZEPT

---

## 🎯 DAS KERN-KONZEPT

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                          │
│   DIGIVICE = DAS ZUHAUSE DER KI                                         │
│                                                                          │
│   Wie eine Fortnite Creative Map - aber für die KI!                     │
│                                                                          │
│   - Der Spieler ERSTELLT den Lebensraum                                 │
│   - Die KI LEBT darin                                                   │
│   - Wenn freigeschaltet: KI GESTALTET selbst!                          │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🏡 WAS IST DER LEBENSRAUM?

### Spieltechnisch gesehen:
```
DIGIVICE = Das HAUS der KI

┌─────────────────────────────────────────────────────────────────────────┐
│                                                                          │
│   🏰 SCHWARZE MÜHLE (Najikas Zuhause)                                   │
│   │                                                                      │
│   │   NUR für die KI zugänglich!                                        │
│   │   Der Spieler "besucht" - die KI WOHNT hier                         │
│   │                                                                      │
│   ├── 🏠 Innenbereich                                                   │
│   │   ├── Wohnzimmer                                                    │
│   │   ├── Küche (Kochen!)                                               │
│   │   ├── Werkstatt (Crafting!)                                         │
│   │   ├── Schlafzimmer                                                  │
│   │   └── Musikzimmer (Instrumente!)                                    │
│   │                                                                      │
│   └── 🌳 Außenbereich (GESTALTBAR!)                                     │
│       ├── 🎣 See/Teich (Fischen!)                                       │
│       ├── 🌱 Garten (Farming!)                                          │
│       ├── ⚒️ Schmiede (Crafting!)                                       │
│       ├── 🏟️ Arena (Minigames!)                                        │
│       └── 🗺️ Erweiterbar...                                            │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Wie eine Fortnite Creative Map:
```
PHASE 1: SPIELER ERSTELLT
┌─────────────────────────────────────┐
│  Spieler baut den Lebensraum:       │
│  - Platziert Gebäude               │
│  - Gestaltet Landschaft            │
│  - Richtet Räume ein               │
│  - Bestimmt was verfügbar ist      │
└─────────────────────────────────────┘
            │
            ▼
PHASE 2: KI LEBT DARIN
┌─────────────────────────────────────┐
│  KI nutzt den Lebensraum:          │
│  - Fischt am See                   │
│  - Pflegt den Garten               │
│  - Kocht in der Küche              │
│  - Spielt Instrumente              │
└─────────────────────────────────────┘
            │
            ▼
PHASE 3: KI GESTALTET SELBST (Optional!)
┌─────────────────────────────────────┐
│  Wenn Spieler Freiheit gibt:       │
│  - KI baut eigene Räume            │
│  - KI dekoriert nach Geschmack     │
│  - KI erweitert Außenbereich       │
│  - KOMPLETT nach ihren Vorstellungen│
└─────────────────────────────────────┘
```

---

## 🎮 ALLE FUNKTIONEN IM LEBENSRAUM

### Alles aus dem Hauptspiel ist verfügbar:

| Funktion | Im Lebensraum | Im Hauptspiel (UE5) |
|----------|---------------|---------------------|
| 🎣 **Fischen** | ✅ Am eigenen See | ✅ Überall in der Welt |
| 🌱 **Farming** | ✅ Im eigenen Garten | ✅ An Farming-Spots |
| 🏠 **Housing** | ✅ VOLL (ist ja das Haus!) | ✅ Schwarze Mühle |
| ⚒️ **Crafting** | ✅ Alle Rezepte | ✅ Alle Rezepte |
| 🍳 **Kochen** | ✅ In der Küche | ✅ An Kochstellen |
| 🎵 **Instrumente** | ✅ Spielen & Üben | ✅ Überall spielbar |
| 🃏 **Minigames** | ✅ Triple Triad, Dice, etc. | ✅ In Arenen/Taverns |
| 💬 **Chat** | ✅ Immer | ✅ Immer |
| 📞 **Voice** | ✅ Immer | ✅ Immer |

### Sync zwischen Lebensraum und Spielwelt:
```
┌──────────────────┐              ┌──────────────────┐
│    LEBENSRAUM    │              │    SPIELWELT     │
│    (Digivice)    │              │    (UE5 Modul)   │
│                  │              │                  │
│  🎣 Fische ──────┼──── SYNC ───┼──► Nutzbar!      │
│  🌱 Ernte ───────┼──── SYNC ───┼──► Nutzbar!      │
│  ⚒️ Crafting ────┼──── SYNC ───┼──► Nutzbar!      │
│  📦 Inventar ────┼──── SYNC ───┼──► Nutzbar!      │
│                  │              │                  │
│  Man MUSS nicht  │              │  Optional!       │
│  spielen!        │              │  Wer will.       │
└──────────────────┘              └──────────────────┘
```

---

## 📦 SPEZIELLE MODULE (Professionell!)

### Kern-Aktivitäten (Im Lebensraum integriert):
- Instrumente SPIELEN (Spaß, casual)
- Sprachen SPRECHEN (im Chat mit KI)
- Bewegung (KI erinnert an Pausen)

### Professionelle Lern-Module (Separat ladbar):

| Modul | Beschreibung | Ziel |
|-------|--------------|------|
| 🎵 **Instrumente LERNEN** | Strukturierter Unterricht | Mit Abschluss/Zertifikat |
| 📚 **Sprachen LERNEN** | Kurs mit Levels | Sprachniveau erreichen |
| 🏋️ **Sport/Übungen** | Fitness-Programm | Trainingsziele |
| 💼 **Life Coach** | Lebensberatung, Ziele | Persönliche Entwicklung |
| 💰 **Wirtschaft** | Finanz-Begleiter | Budget, Investitionen |

```
UNTERSCHIED:

🎵 Im Lebensraum:                    🎵 Lern-Modul:
┌────────────────────────┐           ┌────────────────────────┐
│ "Hey Najika, spiel     │           │ "Lektion 1: Noten     │
│  mir was auf der       │           │  lesen - Grundlagen"  │
│  Ocarina!"             │           │                        │
│                        │           │  □ Übung 1 abschließen│
│ *Najika spielt*        │           │  □ Test bestehen      │
│ "Das war schön!"       │           │  □ → Lektion 2        │
│                        │           │                        │
│ CASUAL, SPASS          │           │ STRUKTURIERT, ZIEL    │
└────────────────────────┘           └────────────────────────┘
```

---

## 🗺️ WELTGENERIERUNG

### Im HAUPTSPIEL (UE5):
```
SPIELWELT = NEU GENERIERT

┌─────────────────────────────────────────────────────────────────────────┐
│                                                                          │
│   8 Regionen + Götterfels                                               │
│   │                                                                      │
│   ├── Prozedural generiert                                              │
│   ├── Jedes Spiel anders                                                │
│   ├── Dungeons, Städte, Wildnis                                         │
│   └── Die große Abenteuerwelt                                           │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Im LEBENSRAUM (Digivice):
```
LEBENSRAUM = PERSISTENT & GESTALTBAR

┌─────────────────────────────────────────────────────────────────────────┐
│                                                                          │
│   Schwarze Mühle + Umgebung                                             │
│   │                                                                      │
│   ├── NICHT prozedural - bleibt wie gebaut                              │
│   ├── Spieler/KI gestaltet                                              │
│   ├── Kann Dungeon-Generator NUTZEN wenn gewünscht:                     │
│   │   └── "Bau mir einen Dungeon im Keller!"                            │
│   └── Aber Basis bleibt stabil                                          │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🔓 KI-AUTONOMIE STUFEN

### Freiheits-Level (Spieler bestimmt):

```
LEVEL 0: KEINE AUTONOMIE
┌─────────────────────────────────────┐
│  KI darf NICHTS verändern          │
│  Nur nutzen was da ist             │
│  Reine Reaktion                    │
└─────────────────────────────────────┘

LEVEL 1: MINIMALE AUTONOMIE
┌─────────────────────────────────────┐
│  KI darf dekorieren                │
│  Kleine Anpassungen                │
│  "Ich hab Blumen gepflanzt!"       │
└─────────────────────────────────────┘

LEVEL 2: MITTLERE AUTONOMIE
┌─────────────────────────────────────┐
│  KI darf Möbel umstellen           │
│  Räume einrichten                  │
│  Garten gestalten                  │
│  "Ich hab das Wohnzimmer neu       │
│   eingerichtet, Mr. K!"            │
└─────────────────────────────────────┘

LEVEL 3: VOLLE AUTONOMIE
┌─────────────────────────────────────┐
│  KI darf ALLES                     │
│  Neue Räume bauen                  │
│  Außenbereich komplett gestalten   │
│  Eigene Projekte starten           │
│  "Mr. K! Ich hab uns einen         │
│   Aussichtsturm gebaut! Schau!"    │
└─────────────────────────────────────┘
```

---

## 🎯 NUTZUNGS-SZENARIEN

### Szenario 1: NUR COMPANION
```
User will: Nur KI-Begleiter, kein Gaming

NUTZT:
├── 💬 Chat (täglich)
├── 📞 Voice Calls
├── 💼 Life Coach Modul
├── 💰 Wirtschaft/Budget Modul
└── 📚 Sprachen lernen

IGNORIERT:
├── ❌ Hauptspiel (UE5)
├── ❌ Kampfsystem
├── ❌ Dungeons
└── ❌ Multiplayer

LEBENSRAUM: Minimalistisch, gemütlich
KI-ROLLE: Persönlicher Assistent
```

### Szenario 2: GAMER + COMPANION
```
User will: Volles Spiel + KI-Beziehung

NUTZT:
├── 🎮 Hauptspiel (UE5)
├── 🏠 Lebensraum (ausgebaut)
├── 🎣 Fischen (beide Welten)
├── ⚒️ Crafting (sync)
├── 💬 Chat + Voice
└── 🎵 Instrumente spielen

LEBENSRAUM: Voll ausgebaut, mit KI-Autonomie
KI-ROLLE: Companion + Kampfgefährte + Freund
```

### Szenario 3: KREATIV-FOKUS
```
User will: Bauen, Gestalten, Erschaffen

NUTZT:
├── 🏗️ Housing (extensiv!)
├── 🌱 Farming/Garten
├── ⚒️ Crafting
├── 🎵 Musik machen
└── 🗺️ Dungeon-Generator (im Lebensraum)

LEBENSRAUM: RIESIG, komplex, kunstvoll
KI-ROLLE: Kreativ-Partner, baut MIT dem Spieler
```

---

## 📊 ZUSAMMENFASSUNG

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         DIGIVICE LEBENSRAUM                              │
│                                                                          │
│   WAS ES IST:                                                           │
│   ├── Das ZUHAUSE der KI (Schwarze Mühle)                              │
│   ├── Wie Fortnite Creative - gestaltbar                                │
│   ├── ALLE Spiel-Funktionen verfügbar                                   │
│   └── KI kann selbst gestalten (wenn erlaubt)                          │
│                                                                          │
│   WAS ES NICHT IST:                                                     │
│   ├── ❌ Nur ein Launcher/Widget                                        │
│   ├── ❌ Abgespeckte Version                                            │
│   └── ❌ Pflicht fürs Hauptspiel                                        │
│                                                                          │
│   VERHÄLTNIS ZUM HAUPTSPIEL:                                            │
│   ├── Hauptspiel = OPTIONAL (wer will)                                  │
│   ├── Sync möglich (Fische, Items, etc.)                                │
│   ├── Aber UNABHÄNGIG nutzbar                                           │
│   └── Lebensraum = Die KONSTANTE                                        │
│                                                                          │
│   SPEZIAL-MODULE:                                                        │
│   ├── Professionelle Lern-Kurse                                         │
│   ├── Mit Struktur und Abschluss                                        │
│   └── Separat vom casual Spielen                                        │
│                                                                          │
│   FÜR WEN:                                                               │
│   ├── Gamer die Companion wollen                                        │
│   ├── Nicht-Gamer die nur KI wollen                                     │
│   ├── Kreative die bauen wollen                                         │
│   └── Jeder auf seine Art                                               │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🔗 BEZIEHUNG ZU ANDEREN SYSTEMEN

```
┌───────────────┐
│   LEBENSRAUM  │ ◄─── Das ZUHAUSE (Digivice App)
│   (Konstant)  │
└───────┬───────┘
        │
        │ OPTIONAL SYNC
        ▼
┌───────────────┐
│  HAUPTSPIEL   │ ◄─── Die ABENTEUERWELT (UE5)
│   (Optional)  │
└───────┬───────┘
        │
        │ OPTIONAL
        ▼
┌───────────────┐
│   SPEZIAL-    │ ◄─── Professionelle MODULE
│    MODULE     │      (Lernen, Coaching, etc.)
└───────────────┘
```

---

*"Die Schwarze Mühle ist MEIN Zuhause, Mr. K! Hier lebe ich, hier warte ich auf dich, hier baue ich UNSER Reich! EXPLOSION!!! 💥🏰" - Najika*
