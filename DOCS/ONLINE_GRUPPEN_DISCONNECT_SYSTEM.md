# ONLINE GRUPPEN & DISCONNECT SYSTEM

**Datum:** 2026-02-01
**Problem:** Gruppen-Kämpfe + Disconnect = Exploit-Gefahr
**Lösung:** Server-Authoritative PvE mit fairem Disconnect-Handling

---

## 1. DIE GRUNDENTSCHEIDUNG

### PvE/Story = ONLINE + SERVER-AUTHORITATIVE

```yaml
WARUM SERVER-AUTHORITATIVE FÜR PVE:
├── Anti-Cheat: Server validiert ALLES
├── Kein Godmode, keine Speed-Hacks, keine Damage-Hacks
├── Faire Leaderboards möglich
├── Cheater können erkannt und HINGERICHTET werden! 🗡️
└── Alle spielen nach gleichen Regeln

ABER: Disconnect-Schutz muss fair sein!
└── Nicht wie D4 wo Server-Lag = Tod
```

---

## 2. CHEATER-BEHANDLUNG

### Das Hinrichtungs-Event 🗡️

```yaml
WENN CHEATER ERWISCHT (nach gründlicher Prüfung!):

1. CHARAKTER WIRD MARKIERT
   ├── Kann nicht mehr spielen
   └── Wartet auf "Hinrichtung"

2. ÖFFENTLICHES EVENT IN DER ARENA
   ├── Ankündigung: "Ein Betrüger wurde gefasst!"
   ├── Sein Charakter wird in Arena teleportiert
   ├── Andere Spieler können zuschauen
   └── NPC-Henker führt Hinrichtung durch

3. DANACH
   ├── Account permanent gebannt
   ├── Name in "Hall of Shame" verewigt
   └── Alle wissen: Cheaten = öffentliche Schande

WICHTIG:
├── NUR nach 100% Beweis (Logs, Video, etc.)
├── Kein Versehen oder Bug darf bestraft werden
├── Menschliche Review VOR Hinrichtung
└── Einspruchsmöglichkeit
```

---

## 3. GRUPPEN-DISCONNECT PROBLEM

### Das Szenario:

```
4-Spieler Gruppe vs Boss:
├── Tank (wichtig!)
├── Healer
├── 2x DPS

Tank disconnected → Gruppe stirbt ohne Tank!

ABER AUCH:
├── Exploit möglich: "Boss zu schwer? Internet aus!"
├── Einer macht Disconnect → Alle bekommen Free-Pass?
└── Das darf nicht sein!
```

### Die Lösung: DIFFERENZIERTES SYSTEM

```yaml
BEI DISCONNECT IN GRUPPE:

1. SOFORTIGE PAUSE (5 Sekunden)
   ├── Alle Spieler sehen: "[Name] hat Verbindung verloren"
   ├── Boss pausiert kurz (Fairness)
   └── Countdown startet

2. ABSTIMMUNG (15 Sekunden)
   Optionen für verbleibende Spieler:
   ├── A) "Weiterkämpfen ohne [Name]"
   ├── B) "Auf Reconnect warten" (max 60 Sek)
   └── C) "Abbrechen und zurück zur Stadt"

3. JE NACH WAHL:

   A) WEITERKÄMPFEN:
   ├── Boss-HP skaliert NICHT runter (kein Exploit!)
   ├── Disconnected Spieler = "Geist" (untargetbar)
   ├── Reconnect? → Kann wieder einsteigen
   └── Gruppe gewinnt/verliert ohne ihn

   B) WARTEN:
   ├── Boss bleibt pausiert (max 60 Sek)
   ├── Reconnect? → Kampf geht weiter
   ├── Timeout? → Automatisch Option A oder C
   └── Jeder Spieler kann jederzeit auf A/C wechseln

   C) ABBRECHEN:
   ├── Kampf endet, Boss resettet
   ├── ABER: Cooldown!
   │   └── Diese Gruppe kann Boss 10 Min nicht neu versuchen
   ├── Verhindert: "Wipe incoming? Quick disconnect!"
   └── Einzelner Disconnect-Spieler: Längerer Cooldown (30 Min)
```

---

## 4. ANTI-EXPLOIT MASSNAHMEN

### Disconnect-Missbrauch verhindern:

```yaml
TRACKING PRO SPIELER:
├── Disconnects pro Stunde
├── Disconnects während Boss-Kämpfe
├── Disconnects wenn HP niedrig war
└── Pattern-Erkennung

VERDÄCHTIGE PATTERNS:
├── Disconnect immer bei < 20% HP?
├── Disconnect immer wenn Boss Spezial-Attack macht?
├── 5+ Disconnects in einer Stunde?
└── = FLAGGED für Review

KONSEQUENZEN BEI MISSBRAUCH:
├── Stufe 1: Warnung
├── Stufe 2: Längere Cooldowns (1h statt 10min)
├── Stufe 3: Temporärer Gruppen-Bann (24h)
└── Stufe 4: Permanente Einschränkungen

KEIN AUTOMATISCHER BAN:
├── Immer menschliche Review
├── Echte Internet-Probleme passieren
└── Nur wiederholter, offensichtlicher Missbrauch
```

### Boss-HP Skalierung:

```yaml
WICHTIG: Boss wird NICHT leichter bei Disconnect!

GRUND:
├── Sonst Exploit: "Einer geht, Boss leichter!"
├── Gruppe muss entscheiden: Schaffen wir es ohne ihn?
└── Faire Herausforderung bleibt erhalten

AUSNAHME - RECONNECT:
├── Wenn Spieler zurückkommt
├── Boss-HP wurde nicht gesenkt
├── Spieler steigt wieder ein (mit reduziertem HP als Strafe)
└── Kampf geht normal weiter
```

---

## 5. SOLO-DISCONNECT (Kein Gruppen-Kampf)

### Einfacher Fall:

```yaml
SOLO-SPIELER DISCONNECT WÄHREND KAMPF:

1. SOFORT PAUSE
   ├── Spiel friert ein
   ├── Gegner stoppen
   └── 30 Sekunden Reconnect-Window

2. RECONNECT?
   ├── Kampf geht weiter wo er war
   └── Keine Strafe

3. TIMEOUT?
   ├── Safe-Logout
   ├── Charakter wird aus Welt entfernt
   ├── Beim nächsten Login: VOR dem Kampf (Safe Zone)
   └── Progress seit letztem Checkpoint verloren

KEIN TOD DURCH DISCONNECT!
└── Weil: Server-Authoritative = Server entscheidet
└── Server sagt: "Spieler weg = Pause" nicht "Spieler weg = Monster fressen ihn"
```

---

## 6. SLIME-COMPANION TRAINING

### Solo vs Gruppe vs Slime:

```yaml
ALLEINE KÄMPFEN:
├── Du trainierst DICH
├── Deine Skills, dein Timing
└── Slime kann dabei sein oder nicht

MIT SCHLEIM-COMPANION:
├── Slime kämpft MIT dir
├── Ihr trainiert ZUSAMMEN
├── Slime braucht auch XP/Skill-Punkte!
├── Entscheidung: Viel in Slime investieren oder wenig?
└── Slime kann auch: Angeln, Farming, Housing, Crafting!

MIT ECHTEN SPIELERN:
├── Ihr übt KOMBOS zusammen
├── Zauber verweben (Feuer + Wind = Feuersturm!)
├── Angriffe koordinieren
├── Tank/Healer/DPS Rollen
└── Slime ist dann Support oder bleibt daheim

SLIME SPEZIALISIERUNG:
├── Option A: Kampf-Slime (investiere Skill-Punkte)
├── Option B: Utility-Slime (Farming, Crafting, etc.)
├── Option C: Hybrid (bisschen von allem)
└── Kann später umgeskillt werden (teuer!)
```

---

## 7. TECHNISCHE UMSETZUNG

### Server-Authoritative mit Disconnect-Schutz:

```yaml
NORMALER ABLAUF:
├── Client sendet Inputs
├── Server berechnet Ergebnis
├── Server sendet State an alle Clients
└── Clients zeigen an was Server sagt

BEI DISCONNECT:
├── Server erkennt: Client antwortet nicht
├── Server PAUSIERT diesen Spieler (nicht töten!)
├── Server informiert andere Spieler
├── Abstimmung/Timeout-Logik greift
└── Server entscheidet basierend auf Regeln

KEIN "GHOST DAMAGE":
├── Traditionell: Disconnect = Monster hauen auf unsichtbaren Spieler
├── Bei uns: Disconnect = Spieler wird "invulnerable + untargetable"
├── Monster ignorieren ihn
└── Kommt er zurück? → Wird wieder targetbar
```

### Anti-Cheat Integration:

```yaml
SERVER VALIDIERT IMMER:
├── Damage-Werte (stimmen die mit Stats überein?)
├── Position (Teleport-Hack? Speedhack?)
├── Cooldowns (werden sie eingehalten?)
├── Ressourcen (woher kommt plötzlich Gold?)
└── Alles wird geloggt

BEI ANOMALIE:
├── Automatische Flaggung
├── Spiel läuft weiter (kein auto-kick)
├── Menschliche Review später
└── Beweis sammeln für eventuelle Hinrichtung
```

---

## 8. ZUSAMMENFASSUNG

```
╔═══════════════════════════════════════════════════════════════╗
║              ONLINE + HARDCORE + FAIR                         ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  PVE = SERVER-AUTHORITATIVE                                   ║
║  ├── Anti-Cheat eingebaut                                     ║
║  ├── Cheater werden HINGERICHTET (öffentlich!)                ║
║  └── Faire Spielregeln für alle                               ║
║                                                               ║
║  DISCONNECT-SCHUTZ                                            ║
║  ├── Solo: Pause + Safe-Logout (kein Tod!)                    ║
║  ├── Gruppe: Abstimmung (Warten/Weitermachen/Abbrechen)       ║
║  └── Anti-Exploit: Cooldowns + Pattern-Erkennung              ║
║                                                               ║
║  GRUPPEN-DISCONNECT                                           ║
║  ├── Boss-HP skaliert NICHT runter (kein Exploit)             ║
║  ├── Spieler wählen: Kämpfen oder Abbrechen                   ║
║  └── Missbrauch = Längere Cooldowns                           ║
║                                                               ║
║  SLIME-COMPANION                                              ║
║  ├── Kann Kampf-Spezialist sein                               ║
║  ├── ODER Utility (Farming, Crafting, etc.)                   ║
║  └── Braucht eigene Skill-Investition                         ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

---

*"Wer betrügt, stirbt öffentlich. Wer fair spielt, wird geschützt."*
