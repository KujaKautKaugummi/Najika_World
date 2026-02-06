# TECHNISCHE ANFORDERUNGEN: LAG-FREIES HARDCORE

**Datum:** 2026-02-01
**Regel:** Tod = Tod. Keine Ausreden. Also: KEINE LAGS!

---

## 0. WAS ANDERE FALSCH MACHEN

### Diablo 4 Problem:
```
- Always-Online = Server-Abhängig
- Server laggt → Du stirbst → Dein Problem
- "Scroll of Escape" = Pflaster auf Schusswunde
- 2025: Immer noch Disconnect-Deaths

Quelle: Spieler verlieren HC-Chars weil Blizzard-Server hängen
```

### Path of Exile Problem:
```
- Online-Only = Kein Offline-Modus
- Kein Disconnect-Schutz
- "2-3 Sekunden Lag = HC Char weg"
- Community-Tipp: "Spiel einfach nicht HC lol"
```

### Last Epoch:
```
- Hat "Offline Mode" = Besser!
- Aber Online-HC hat gleiche Probleme
- Disconnect = Tot (char wird Softcore)
```

### Elden Ring/Dark Souls:
```
- Peer-to-Peer System seit 2011
- Host = ein Spieler, andere verbinden sich
- Problem: "Phantom Hits" = du wirst getroffen obwohl ausgewichen
- Lag-Switch Exploits möglich
- Funktioniert OK weil: Invasions sind optional!
```

### UNSERE SITUATION:
```
Wir SIND online! Für:
├── Echte Spieler-Söldner
├── Rettungen
├── Multiplayer-Features
└── Eventuell PvP später

ABER: Hardcore + Online = Problem!
Wie lösen wir das?
```

---

## 1. DAS PRINZIP

```
Online-Spiel + Hardcore + Lag-Tod = UNFAIR
Aber wir WOLLEN online sein für Community-Features!

LÖSUNG: HYBRID-SYSTEM
├── DEIN Kampf = Client-Authoritative (du entscheidest)
├── Söldner-Kampf = Söldner entscheidet
├── Server = Sync + Validation (nicht Combat-Authority)
└── Bei Disconnect = Graceful Handling
```

---

## 2. CLIENT-AUTHORITATIVE COMBAT

### Was heißt das?

```yaml
TRADITIONELL (Diablo, PoE):
├── Server sagt: "Du hast X Schaden bekommen"
├── Server sagt: "Du bist tot"
├── Client zeigt nur an was Server sagt
└── Server laggt? → Du stirbst ohne es zu sehen!

UNSER ANSATZ:
├── DEIN Client sagt: "Ich wurde getroffen"
├── DEIN Client sagt: "Ich bin tot"
├── Server validiert und synct
└── Server laggt? → Dein Kampf läuft trotzdem weiter!
```

### Wie funktioniert das bei Söldnern?

```yaml
SÖLDNER-ESKORTE:

Dein Kampf:
├── Du steuerst deinen Charakter
├── DEIN Client berechnet deine Treffer/Schaden
├── Du entscheidest ob du getroffen wurdest
└── Server bekommt Updates, entscheidet aber NICHT

Söldner-Kampf:
├── AI-Söldner: Lokal auf deinem Client berechnet
├── Echter Spieler: Auf SEINEM Client berechnet
├── Du siehst nur die Ergebnisse
└── Sein Lag = Sein Problem, nicht deins!

BEI LAG/DISCONNECT:
├── Söldner friert ein oder verschwindet
├── DEIN Kampf läuft weiter (du bist Client-Auth!)
├── Du stirbst NICHT weil Söldner laggt
└── Reconnect? → Söldner macht weiter wo er war
```

### Was ist mit Cheating?

```yaml
REALITÄT:
├── Client-Authority = Theoretisch cheatbar
├── ABER: Story/PvE = Wen interessiert's?
├── Leaderboards: Separate Server-Validierung
├── PvP: Anderes System (später designen)
└── Lieber fair für ehrliche Spieler als paranoid!

ELDEN RING MACHT ES AUCH SO:
├── Peer-to-Peer, Host hat Authority
├── Cheater gibt es, aber Spiel funktioniert
├── Invasions sind optional = wer will, nimmt Risiko
└── Bei uns: Söldner sind optional = gleiches Prinzip
```

---

## 3. DISCONNECT-HANDLING

### Das Diablo 4 Problem:
```
Server-Authoritative + Disconnect = SOFORT TOT
Weil: Server sagt "Spieler weg" → Monster hauen weiter
      Server sagt "Spieler tot" → Char weg

Bei uns NICHT so weil: DU entscheidest, nicht Server!
```

### Verbindung verloren während Kampf

```yaml
SOFORT:
├── Spiel PAUSIERT
├── Gegner frieren ein
├── Timer: 30 Sekunden Reconnect-Window
└── UI: "Verbindung unterbrochen..."

NACH 30 SEK:
├── Immer noch weg? → Safe-Logout
├── Charakter verschwindet aus Welt
├── Kein Tod, kein Progress-Loss
└── Beim nächsten Login: Vor dem Kampf

WARUM FUNKTIONIERT DAS:
└── Offline-First = Kein Server nötig für Kampf
└── Pause ist IMMER möglich
└── Multiplayer-Session endet einfach
```

---

## 4. PERFORMANCE-ANFORDERUNGEN

### Minimum FPS

```yaml
ZIEL: Konstante 60 FPS auf Ziel-Hardware

BEI FPS < 30:
├── Automatische Grafik-Reduktion
├── Partikel reduzieren
├── Draw Distance runter
└── Gameplay MUSS flüssig bleiben

BEI FPS < 15:
├── PAUSE (wie Disconnect)
├── "Performance-Probleme erkannt"
├── Optionen zum Anpassen
└── Weitermachen nur wenn stabil
```

### Memory Management

```yaml
KEINE MEMORY LEAKS:
├── Regelmäßige Cleanup-Passes
├── Object Pooling für alles
├── Streaming für große Welten
└── Max Memory Budget einhalten

BEI MEMORY SPIKE:
├── Graceful Degradation
├── Assets ausladen
├── NICHT: Crash während Kampf
```

---

## 5. COMBAT FAIRNESS

### Keine "Bullshit Deaths"

```yaml
REGELN FÜR FAIRE KÄMPFE:

1. TELEGRAPHED ATTACKS
   ├── Jeder gefährliche Angriff hat Vorwarnung
   ├── Mindestens 0.5 Sekunden Reaktionszeit
   └── Visuell UND Audio

2. KEINE ONE-SHOTS (außer spezielle Bosse)
   ├── Trash Mobs: Max 50% HP pro Hit
   ├── Bosse: Max 70% HP (telegraphed!)
   └── Instakills: NUR mit 3+ Sekunden Vorwarnung

3. KLARE HITBOXEN
   ├── Was du siehst = was trifft
   ├── Keine unsichtbaren Hitboxen
   └── Debug-Mode zeigt Hitboxen

4. KONSISTENTE MECHANIKEN
   ├── Gleicher Move = Gleiches Timing
   ├── Keine random Speed-Variation
   └── Lernbar durch Wiederholung

5. ESCAPE IMMER MÖGLICH
   ├── Kein Lock-in ohne Warnung
   ├── Notfall-Roll hat i-frames
   └── Wegrennen = valide Strategie
```

---

## 6. TESTING-ANFORDERUNGEN

### Vor Release

```yaml
STRESS TESTS:
├── 1000+ Stunden Kampf-Testing
├── Jeder Boss 100+ mal getestet
├── Edge Cases dokumentiert
└── "Kann man unfair sterben?" = Release-Blocker

LAG SIMULATION:
├── Teste mit künstlichem Lag (100ms, 500ms, 1000ms)
├── Teste mit Packet Loss (10%, 30%, 50%)
├── Alles muss graceful handlen
└── Kein Tod durch Netzwerk-Probleme

HARDWARE VARIATION:
├── Teste auf Low-End Hardware
├── Teste auf verschiedenen GPUs
├── Teste mit wenig RAM
└── Überall muss es funktionieren
```

---

## 7. ZUSAMMENFASSUNG

```
╔═══════════════════════════════════════════════════════════════╗
║             ONLINE-SPIEL + HARDCORE = SO GEHT'S               ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  DAS PROBLEM:                                                 ║
║  ├── Diablo 4/PoE: Server entscheidet → Server-Lag = Tod     ║
║  └── Wir wollen online sein aber Lag-Tod verhindern!         ║
║                                                               ║
║  UNSERE LÖSUNG: CLIENT-AUTHORITATIVE COMBAT                  ║
║  ├── DEIN Client entscheidet über DEINEN Charakter           ║
║  ├── Server synct nur, entscheidet NICHT                     ║
║  ├── Disconnect? → Spiel pausiert, du stirbst NICHT          ║
║  └── Söldner laggt? → Sein Problem, nicht deins              ║
║                                                               ║
║  CHEATING?                                                    ║
║  ├── PvE/Story: Wen interessiert's?                          ║
║  ├── Leaderboards: Extra Server-Validierung                  ║
║  └── PvP: Separates System (später)                          ║
║                                                               ║
║  WIE ELDEN RING:                                              ║
║  ├── Peer-to-Peer, jeder kontrolliert sich selbst            ║
║  ├── Optional (Invasions) = Wer will, nimmt Risiko           ║
║  └── Funktioniert trotz theoretischer Cheater                ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

---

*"Ein Held stirbt durch den Feind, nicht durch die Technik."*
