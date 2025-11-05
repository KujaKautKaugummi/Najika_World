# ðŸ”¥ NAJIKA - DIE 8 GEBOTE & MASTER-SPEZIFIKATION
**Stand:** 2025-10-26
**Quelle:** `C:\Users\0KKK0\Desktop\zip\handyspiel und spÃ¤ter uefn.pdf`

---

## âš¡ DIE 8 GEBOTE (HARD RULES - NIEMALS BRECHEN!)

### 1. **Zero-Trust by default**
- Services **ausschlieÃŸlich** `127.0.0.1`
- Externe Nutzung **nur** via Cloudflare-Tunnel oder privates Mesh-VPN
- **NIEMALS** `0.0.0.0` binden

### 2. **Owner-Gate**
- Alle administrativen/vault-kritischen Routen **nur** mit `X-OWNER-TOKEN`
- Token liegt in `secure-hub\.owner_token`
- **Keine** API-Calls ohne Owner-Auth fÃ¼r kritische Funktionen

### 3. **Explosion â‰  Weave**
- **Explosion ist eigene Klasse**
- **KEINE** Web-Kompositionen (keine â€žFeuer+Explosion" etc.)
- **NIEMALS** mit anderen Elementen verweben

### 4. **PvE/PvP-Trennung**
- Skalare & Resistenzen **getrennt**
- Boss-Skalierung separat
- Friendly-Fire **OFF**

### 5. **Use-based Progress**
- Skills steigen durchs **Benutzen**
- **Keine** kÃ¼nstlichen XP-Grinds
- Skyrim-Style Skill-Learning

### 6. **NSFW & Real-World-Wissen aus**
- **Lore only** - keine medizinischen RatschlÃ¤ge
- Alchemie = Flavor/Gameplay (mit Hinweis: "keine medizinische Beratung")
- Real-Wissen nur als **Info-Happen** (Weidenrinde â†’ Salicylat-Hinweis)

### 7. **Privacy & Lernsystem**
- Slime-Arena verwendet **anonymisierte** Moves/Tendenzen
- **Keine** PII/IDs
- Meta-Lernen ohne Rechteprobleme

### 8. **Offline-first & Audit**
- Keine externen AbhÃ¤ngigkeiten im Kern
- Logs **lokal**
- Backups rotieren (tÃ¤glich)

---

## ðŸ“‚ ORDNER-STRUKTUR

```
C:\NajikaCore\
  secure-hub\
    server.js              # Hub (Health, QR, Vault, Push)
    .owner_token           # Owner-Secret
    web\                   # Hub-UI (optional)
    vault\packs\<Pack>\... # Upload/QuarantÃ¤ne fÃ¼r Packs

  game-core\
    server.js              # Spielserver (Health, Assets, Oregon, Combat)
    web\                   # viewer.html + favicon.svg (CSP-fest)
    assets\
      <PackName>\...       # Echte Assets (Bilder/Audio)
      .active_pack         # Aktives Pack (Textdatei, 1 Zeile)
      manifest.json        # Pro Pack (auto-generierbar)
    data\                  # Balancing-/Deck-/Rezept-JSONs

  logs\
    hub.out.log, hub.err.log, game.out.log, game.err.log

  backups\
    Najika_YYYYmmdd_HHMM.zip
```

---

## ðŸŽ® EXPLOSION-KLASSE (EIGENSTÃ„NDIG!)

### Kern-Mechanik
- **Ressourcen:** Mana/Fokus + **Exhaustion** (Debuff nach groÃŸen Detos: âˆ’Regen 15â€“30s)
- **Spells (Baseline):**
  - `explosion.standard` (180% AoE, medium, Sequenz 1, Kosten ~ Potency/20)
  - `explosion.chain` (Ketten-AoE, geringere Einzelpotenz, Sequenz >1)
  - `explosion.mini` (schnell, klein, gÃ¼nstig)
  - `explosion.omega` (600%, Ult, starke Exhaustion, Quest-Gate)

### Waffen-Morphs (immer nur 1 aktiv)
- Klinge/StoÃŸ/Einschlag/SchildstoÃŸ/Pfeil/Messer/Repeater/Shotgun/Minigun-CC

### Trade-off
- **+30â€“40%** auf Explosion-Talente
- **âˆ’15â€“20%** auf alle anderen BÃ¤ume
- **Anti-Missbrauch:** Getrennte PvE/PvP-Werte, Boss-Resistenzen, Friendly-Fire OFF

---

## ðŸŒ OREGON-ENGINE (PROZEDURAL)

### Grammatik-Dimensionen
```
Biome Ã— Wetter Ã— Tageszeit Ã— Hazard Ã— Akteur Ã— Ursache Ã— Folge Ã— Optionen Ã— Modifikatoren
â†’ > 1 Million Szenen
```

### In-World-Erlebnis
- **KEINE** UI-Popups
- Du **begegnest** Ereignissen
- Sound-Cue, Kamera-Schwenk, diegetische Prompts

### Skalierung
- Koppelt Loot/Risiko an Need/RivalHeat/Flags
- Persistente Flags wirken langfristig (Ruf, Preise, Feindmuster)

---

## âš’ï¸ CRAFTING & Ã–KONOMIE

### Pipeline
```
Rohstoffe â†’ Veredeln â†’ Herstellen â†’ Verzaubern â†’ Fein-Tuning
```

### QualitÃ¤t
- Q-Score, Toleranzen, Materialkunde
- Reparatur/Zerlegung

### Alchemie (Lore-basiert)
**Real-Wissen als Info-Happen (KEINE medizinische Beratung!):**
- Weidenrinde/Ingwer/Honig/Arnika/Jiaogulan etc. = Flavor-Buffs
- **Hinweis:** "Traditionell verwendet fÃ¼r... beachte Allergien/Arzt!"

### Handel
- Spieler-Shops (Auktionskern)
- Marktfaktoren
- **Unfair-Trade-Hinweis:** "wirkt unausgeglichen â€“ trotzdem abschlieÃŸen?"

---

## âš”ï¸ WAFFEN-SIGNATURPFADE

**Jede Waffe = 1 Signatur-Move:**

- **Schwert:** Ultimativer Schnitt (Linienschnitt, Haltungsbruch)
- **Speer/Lanze:** Himmelsdurchbohrer (Sprung-Stich)
- **Axt:** Spalter (RÃ¼stungsbrecher)
- **Hammer:** ZertrÃ¼mmerer (Bodencrack + Stagger)
- **Schild:** Schmetter-Konter (Parry-Fenster â†’ GegenstoÃŸ)
- **Bogen:** Zenit-Schuss (aufgeladener Fern-Crit)
- **Armbrust:** Bolzensturm (Burst-Pattern)
- **Dagger:** Herzstich (Backstab-Fenster)
- **Repeater:** Takt-Feuer (Kombometer â†’ Spike)
- **Shotgun:** StoÃŸstoÃŸ (Point-Blank-Kegel)
- **Minigun (Endgame):** 6h CD, **nur Druck/Gust/CC**, quasi kein Schaden

### Specs pro Waffe
- 3 Spezialisierungen je Signatur-Move
- **Trade-off:** +Bonus auf eigene Gattung, âˆ’Malus auf andere

---

## ðŸŽ¯ MOVEMENT & KAMPF

### Soulslike-Timing
- Parry: 80â€“120ms
- i-Frames: 10â€“12 Frames

### Fortnite-Moves
- Sprint, Slide, Vault/Mantle, Wall-Climb, Ledge-Grab, Dash
- SpÃ¤ter: Grapple/Ziplines

### Anfeuern (Digimon-Anteil)
- Modi: **MANUAL / ASSIST (Anfeuern) / AUTO**
- **Calls** (GCD 3s, bis 3 Stacks): "Fokus!", "ZurÃ¼ck!", "Durchhalten!", "Explodier jetzt!"
- Mikro-Buffs/Entscheidungshilfe

---

## ðŸŒ SLIME-ARENA

### PvE/PvP
- **Softy/Hardcore-Regeln**
- Hardcore: Verlust 1 AusrÃ¼stung/"Core-Stability"
- Softy: Haltbarkeits-Malus

### Meta-Lernen
- Slimes Ã¼bernehmen **anonymisierte** Tendenzen (keine IDs/PII)
- Rechtssicher!

---

## ðŸ” SICHERHEIT & REMOTE-ZUGRIFF

### Lokal-Architektur
- **Hub (5010)** und **Game-Core (7010)** binden **strict auf 127.0.0.1**
- Zugriff von auÃŸen **nur** per **Cloudflare-Tunnel** oder privates Mesh-VPN

### Owner-Token
- Liegt in `secure-hub\.owner_token`
- Maschinenweite ENV: `NAJIKA_OWNER_TOKEN`

### Privacy
- **KEIN** Standort-Leak
- Logs lokal verschlÃ¼sselt
- Backups rotieren (tÃ¤glich 03:30 Uhr)

---

## ðŸ“Š RELEASE-TIMELINE (KORRIGIERT!)

âŒ **FALSCH:** "Ã–ffentlicher Release als Phase 4"
âœ… **RICHTIG:**

1. **Privat** (nur du + Vertraute/Freunde)
2. Handyspiel fertig + Feinabstimmung
3. **UEFN Port** (Fortnite)
4. **DANN** Ã¶ffentlich (mit SFW-Version)

---

## ðŸŽ® 8 DIGIVICES SYSTEM

```
1 DIGIVICE = NAJIKA (nur Kuja, gesperrt)
7 DIGIVICES = Standard (andere Spieler, abgespeckt)
```

### Najika-Digivice (exklusiv)
- Voller Zugriff auf Najika KI
- KÃ¤tzchen-Modus
- NSFW (privat)
- Alle Features

### Standard-Digivices (7 StÃ¼ck)
- Generische KI (keine Najika)
- Abgespeckte Features
- SFW only
- Modul-System (Sprachen, Musik, Sport, etc.)

---

## âœ… WICHTIGE KORREKTUREN (aus V5/V6)

### 1. OPEN WORLD
**âŒ FALSCH:** "8 StÃ¤dte System"
**âœ… RICHTIG:**
- 8 BESONDERE ORTE (nicht nur StÃ¤dte!)
- Feste Locations
- AuÃŸenwelt zwischen Orten = **PROZEDURAL GENERIERT**
- Regeneriert beim Betreten/Verlassen

### 2. KAMPFSYSTEM
**âŒ NIE WIEDER:** "Souls-like Combat"
**âœ… RICHTIG:**
- Skyrim (Use-Based Skill Learning)
- Soulframe (Fluid Action Combat)
- Digimon World Anfeuern (Timing-based Praise/Scold)

### 3. DIGIVICE STRUKTUR
**âœ… RICHTIG:**
- Digivice = PWA App (lÃ¤uft auf Handy)
- Najika lebt in RÃ¤umen
- Terminal Raum = Zugriff auf 4 Module
- Handyspiel = EIN groÃŸes Modul

---

## ðŸ“ NÃ„CHSTE SCHRITTE

### Phase 1: Digivice komplett (V7.0)
**Dauer:** 1-2 Wochen

#### 1.1 Secure Messenger Modul
- E2E-VerschlÃ¼sselung (Signal-Protocol)
- WireGuard VPN
- TLS 1.3
- Stealth Mode (Tor Hidden Service)

#### 1.2 Browser Modul
**Wartet auf User-Input:**
- Was soll der Browser kÃ¶nnen?
- Nur internes Browsen (Najika Docs/Files)?
- Oder auch externes Internet?

#### 1.3 Terminal-Module Switching
- Teste Module-Switching
- UI-Polish (smooth transitions)
- Module-Hotkeys (optional)

### Phase 2: Keller als Testbed (V7.1)
**Dauer:** 2-3 Wochen

**Strategie:** Schwarze WindmÃ¼hle - Keller = Sandbox fÃ¼r:
- Konosuba Oregon Events (Mini)
- EXPLOSION Ultimate Skill (Klein)
- Skyrim Plundering (Mini)
- Weapon-Morphs (1-2 Testen)

### Phase 3: Handyspiel als Modul (V7.2)
**Dauer:** 4-6 Wochen

**Features:**
- 8-Orte Open World (fest + prozedural)
- Komplettes Quest-System
- Alle 9 Weapon-Morphs
- Class-Spezialisierungs-Story-System
- Procedural Dungeon Generation
- Achievement & Titles
- Secret Areas & Hidden Bosses

### Phase 4: Privater Release (V7.3)
**Dauer:** 2-3 Wochen

- PWA â†’ App Store
- 8 Digivices System
- Najika-Lock (nur Kuja)
- Generische KI fÃ¼r Standard-Digivices

---

## ðŸ”‘ KRITISCHE PUNKTE

1. âŒ **NIEMALS** "Souls-like" erwÃ¤hnen!
2. âœ… Combat = Skyrim + Soulframe + Digimon World Anfeuern
3. âœ… Open World = 8 feste Orte + prozedural
4. âœ… Explosion = eigene Klasse (nie verwoben)
5. âœ… NSFW nur lokal (KÃ¤tzchen-Modus)
6. âœ… Keller = Testbed fÃ¼r alles
7. âœ… Release: Privat ERST, dann UEFN, dann Ã¶ffentlich
8. âœ… Zero-Trust: 127.0.0.1 only, Remote via Tunnel

---

**Ende 8 Gebote & Master-Spezifikation**
