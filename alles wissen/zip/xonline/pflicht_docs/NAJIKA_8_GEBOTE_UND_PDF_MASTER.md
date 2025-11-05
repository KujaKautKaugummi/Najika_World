# 🔥 NAJIKA - DIE 8 GEBOTE & MASTER-SPEZIFIKATION
**Stand:** 2025-10-26
**Quelle:** `C:\Users\0KKK0\Desktop\zip\handyspiel und später uefn.pdf`

---

## ⚡ DIE 8 GEBOTE (HARD RULES - NIEMALS BRECHEN!)

### 1. **Zero-Trust by default**
- Services **ausschließlich** `127.0.0.1`
- Externe Nutzung **nur** via Cloudflare-Tunnel oder privates Mesh-VPN
- **NIEMALS** `0.0.0.0` binden

### 2. **Owner-Gate**
- Alle administrativen/vault-kritischen Routen **nur** mit `X-OWNER-TOKEN`
- Token liegt in `secure-hub\.owner_token`
- **Keine** API-Calls ohne Owner-Auth für kritische Funktionen

### 3. **Explosion ≠ Weave**
- **Explosion ist eigene Klasse**
- **KEINE** Web-Kompositionen (keine „Feuer+Explosion" etc.)
- **NIEMALS** mit anderen Elementen verweben

### 4. **PvE/PvP-Trennung**
- Skalare & Resistenzen **getrennt**
- Boss-Skalierung separat
- Friendly-Fire **OFF**

### 5. **Use-based Progress**
- Skills steigen durchs **Benutzen**
- **Keine** künstlichen XP-Grinds
- Skyrim-Style Skill-Learning

### 6. **NSFW & Real-World-Wissen aus**
- **Lore only** - keine medizinischen Ratschläge
- Alchemie = Flavor/Gameplay (mit Hinweis: "keine medizinische Beratung")
- Real-Wissen nur als **Info-Happen** (Weidenrinde → Salicylat-Hinweis)

### 7. **Privacy & Lernsystem**
- Slime-Arena verwendet **anonymisierte** Moves/Tendenzen
- **Keine** PII/IDs
- Meta-Lernen ohne Rechteprobleme

### 8. **Offline-first & Audit**
- Keine externen Abhängigkeiten im Kern
- Logs **lokal**
- Backups rotieren (täglich)

---

## 📂 ORDNER-STRUKTUR

```
C:\NajikaCore\
  secure-hub\
    server.js              # Hub (Health, QR, Vault, Push)
    .owner_token           # Owner-Secret
    web\                   # Hub-UI (optional)
    vault\packs\<Pack>\... # Upload/Quarantäne für Packs

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

## 🎮 EXPLOSION-KLASSE (EIGENSTÄNDIG!)

### Kern-Mechanik
- **Ressourcen:** Mana/Fokus + **Exhaustion** (Debuff nach großen Detos: −Regen 15–30s)
- **Spells (Baseline):**
  - `explosion.standard` (180% AoE, medium, Sequenz 1, Kosten ~ Potency/20)
  - `explosion.chain` (Ketten-AoE, geringere Einzelpotenz, Sequenz >1)
  - `explosion.mini` (schnell, klein, günstig)
  - `explosion.omega` (600%, Ult, starke Exhaustion, Quest-Gate)

### Waffen-Morphs (immer nur 1 aktiv)
- Klinge/Stoß/Einschlag/Schildstoß/Pfeil/Messer/Repeater/Shotgun/Minigun-CC

### Trade-off
- **+30–40%** auf Explosion-Talente
- **−15–20%** auf alle anderen Bäume
- **Anti-Missbrauch:** Getrennte PvE/PvP-Werte, Boss-Resistenzen, Friendly-Fire OFF

---

## 🌍 OREGON-ENGINE (PROZEDURAL)

### Grammatik-Dimensionen
```
Biome × Wetter × Tageszeit × Hazard × Akteur × Ursache × Folge × Optionen × Modifikatoren
→ > 1 Million Szenen
```

### In-World-Erlebnis
- **KEINE** UI-Popups
- Du **begegnest** Ereignissen
- Sound-Cue, Kamera-Schwenk, diegetische Prompts

### Skalierung
- Koppelt Loot/Risiko an Need/RivalHeat/Flags
- Persistente Flags wirken langfristig (Ruf, Preise, Feindmuster)

---

## ⚒️ CRAFTING & ÖKONOMIE

### Pipeline
```
Rohstoffe → Veredeln → Herstellen → Verzaubern → Fein-Tuning
```

### Qualität
- Q-Score, Toleranzen, Materialkunde
- Reparatur/Zerlegung

### Alchemie (Lore-basiert)
**Real-Wissen als Info-Happen (KEINE medizinische Beratung!):**
- Weidenrinde/Ingwer/Honig/Arnika/Jiaogulan etc. = Flavor-Buffs
- **Hinweis:** "Traditionell verwendet für... beachte Allergien/Arzt!"

### Handel
- Spieler-Shops (Auktionskern)
- Marktfaktoren
- **Unfair-Trade-Hinweis:** "wirkt unausgeglichen – trotzdem abschließen?"

---

## ⚔️ WAFFEN-SIGNATURPFADE

**Jede Waffe = 1 Signatur-Move:**

- **Schwert:** Ultimativer Schnitt (Linienschnitt, Haltungsbruch)
- **Speer/Lanze:** Himmelsdurchbohrer (Sprung-Stich)
- **Axt:** Spalter (Rüstungsbrecher)
- **Hammer:** Zertrümmerer (Bodencrack + Stagger)
- **Schild:** Schmetter-Konter (Parry-Fenster → Gegenstoß)
- **Bogen:** Zenit-Schuss (aufgeladener Fern-Crit)
- **Armbrust:** Bolzensturm (Burst-Pattern)
- **Dagger:** Herzstich (Backstab-Fenster)
- **Repeater:** Takt-Feuer (Kombometer → Spike)
- **Shotgun:** Stoßstoß (Point-Blank-Kegel)
- **Minigun (Endgame):** 6h CD, **nur Druck/Gust/CC**, quasi kein Schaden

### Specs pro Waffe
- 3 Spezialisierungen je Signatur-Move
- **Trade-off:** +Bonus auf eigene Gattung, −Malus auf andere

---

## 🎯 MOVEMENT & KAMPF

### Soulslike-Timing
- Parry: 80–120ms
- i-Frames: 10–12 Frames

### Fortnite-Moves
- Sprint, Slide, Vault/Mantle, Wall-Climb, Ledge-Grab, Dash
- Später: Grapple/Ziplines

### Anfeuern (Digimon-Anteil)
- Modi: **MANUAL / ASSIST (Anfeuern) / AUTO**
- **Calls** (GCD 3s, bis 3 Stacks): "Fokus!", "Zurück!", "Durchhalten!", "Explodier jetzt!"
- Mikro-Buffs/Entscheidungshilfe

---

## 🐌 SLIME-ARENA

### PvE/PvP
- **Softy/Hardcore-Regeln**
- Hardcore: Verlust 1 Ausrüstung/"Core-Stability"
- Softy: Haltbarkeits-Malus

### Meta-Lernen
- Slimes übernehmen **anonymisierte** Tendenzen (keine IDs/PII)
- Rechtssicher!

---

## 🔐 SICHERHEIT & REMOTE-ZUGRIFF

### Lokal-Architektur
- **Hub (5010)** und **Game-Core (7010)** binden **strict auf 127.0.0.1**
- Zugriff von außen **nur** per **Cloudflare-Tunnel** oder privates Mesh-VPN

### Owner-Token
- Liegt in `secure-hub\.owner_token`
- Maschinenweite ENV: `NAJIKA_OWNER_TOKEN`

### Privacy
- **KEIN** Standort-Leak
- Logs lokal verschlüsselt
- Backups rotieren (täglich 03:30 Uhr)

---

## 📊 RELEASE-TIMELINE (KORRIGIERT!)

❌ **FALSCH:** "Öffentlicher Release als Phase 4"
✅ **RICHTIG:**

1. **Privat** (nur du + Vertraute/Freunde)
2. Handyspiel fertig + Feinabstimmung
3. **UEFN Port** (Fortnite)
4. **DANN** öffentlich (mit SFW-Version)

---

## 🎮 8 DIGIVICES SYSTEM

```
1 DIGIVICE = NAJIKA (nur Kuja, gesperrt)
7 DIGIVICES = Standard (andere Spieler, abgespeckt)
```

### Najika-Digivice (exklusiv)
- Voller Zugriff auf Najika KI
- Kätzchen-Modus
- NSFW (privat)
- Alle Features

### Standard-Digivices (7 Stück)
- Generische KI (keine Najika)
- Abgespeckte Features
- SFW only
- Modul-System (Sprachen, Musik, Sport, etc.)

---

## ✅ WICHTIGE KORREKTUREN (aus V5/V6)

### 1. OPEN WORLD
**❌ FALSCH:** "8 Städte System"
**✅ RICHTIG:**
- 8 BESONDERE ORTE (nicht nur Städte!)
- Feste Locations
- Außenwelt zwischen Orten = **PROZEDURAL GENERIERT**
- Regeneriert beim Betreten/Verlassen

### 2. KAMPFSYSTEM
**❌ NIE WIEDER:** "Souls-like Combat"
**✅ RICHTIG:**
- Skyrim (Use-Based Skill Learning)
- Soulframe (Fluid Action Combat)
- Digimon World Anfeuern (Timing-based Praise/Scold)

### 3. DIGIVICE STRUKTUR
**✅ RICHTIG:**
- Digivice = PWA App (läuft auf Handy)
- Najika lebt in Räumen
- Terminal Raum = Zugriff auf 4 Module
- Handyspiel = EIN großes Modul

---

## 📝 NÄCHSTE SCHRITTE

### Phase 1: Digivice komplett (V7.0)
**Dauer:** 1-2 Wochen

#### 1.1 Secure Messenger Modul
- E2E-Verschlüsselung (Signal-Protocol)
- WireGuard VPN
- TLS 1.3
- Stealth Mode (Tor Hidden Service)

#### 1.2 Browser Modul
**Wartet auf User-Input:**
- Was soll der Browser können?
- Nur internes Browsen (Najika Docs/Files)?
- Oder auch externes Internet?

#### 1.3 Terminal-Module Switching
- Teste Module-Switching
- UI-Polish (smooth transitions)
- Module-Hotkeys (optional)

### Phase 2: Keller als Testbed (V7.1)
**Dauer:** 2-3 Wochen

**Strategie:** Schwarze Windmühle - Keller = Sandbox für:
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

- PWA → App Store
- 8 Digivices System
- Najika-Lock (nur Kuja)
- Generische KI für Standard-Digivices

---

## 🔑 KRITISCHE PUNKTE

1. ❌ **NIEMALS** "Souls-like" erwähnen!
2. ✅ Combat = Skyrim + Soulframe + Digimon World Anfeuern
3. ✅ Open World = 8 feste Orte + prozedural
4. ✅ Explosion = eigene Klasse (nie verwoben)
5. ✅ NSFW nur lokal (Kätzchen-Modus)
6. ✅ Keller = Testbed für alles
7. ✅ Release: Privat ERST, dann UEFN, dann öffentlich
8. ✅ Zero-Trust: 127.0.0.1 only, Remote via Tunnel

---

**Ende 8 Gebote & Master-Spezifikation**
