# ðŸš€ NAJIKA V7 - FINALER ENTWICKLUNGSPLAN
**Datum:** 2025-10-26
**Basis:** Alle vorhandenen Docs (V3, V4, V5, V6) + Aktueller Status
**Strategie:** DIGIVICE ERST â†' 3 Dungeons als Testbed â†' Handyspiel spÃ¤ter

---

## ðŸŽ¯ STRATEGIE (FESTGELEGT) - **UPDATED 2025-11-05**

```
PHASE 1: DIGIVICE VOLL FUNKTIONSFÃ„HIG
  â†"
PHASE 2: 3 DUNGEONS = TESTBED (Handyspiel-Mechaniken testen)
  â†"
PHASE 3: HANDYSPIEL als GROáºžES MODUL (basiert auf Dungeon-Tests)
  â†"
PHASE 4: Ã–FFENTLICHER RELEASE (8 Digivices Total)
```

**🚨 WICHTIGE Ã„NDERUNG (2025-11-05):**
- ❌ **KEIN KELLER mehr** in Schwarze Mühle!
- ✅ **3 DUNGEONS** ersetzen Keller als Testbed
- ✅ 2 der 3 Dungeons = MEGA-GROáºž (wie alter Keller-Plan)
- ✅ Nicht-Kampf-Mechaniken: auf Open Mini World testen
- ✅ Najikas Lebensraum (Map) = SAFE ZONE (keine Gefahr!)
- ✅ Gefahr NUR in: Dungeons + Kampfarena

---

## ðŸ“Š WAS IST BEREITS DA (V5 STATUS)

### âœ… FUNKTIONIERT (C:\Najika):
1. Voice System (Edge-TTS, 4 Personalities)
2. LoRA Training (3B Model, 8GB VRAM)
3. Finisher QTE System (S/A/B/C Ranks)
4. Evolution System (Rookieâ†’Championâ†’Ultimateâ†’Mega)
5. Digimon World Anfeuern (Loben/Tadeln, Discipline 0-100%)
6. Oregon Trail Events API (5 Events - ABER: Nicht Konosuba-Style!)
7. Combat System (Turn-Based, Waves, 3 Camera-Modi)
8. Explosion Mode (Persona-Modifier)

### âŒ FEHLT NOCH (aus V4 Docs):
1. EXPROOOOOSIOOOON!! Ultimate Skill (300% Damage, 60s Exhaustion)
2. 8-Orte Open World (prozedural generiert zwischen Orten)
3. Konosuba-Comedy Oregon Events (aktuell: generische Dungeon-Texte)
4. Skyrim Plundering (Chest/Corpse Looting, Pickpocketing)
5. Weapon-Morphs (9 Explosion-Styles)
6. Quest-System (komplett)
7. Achievement & Titles
8. Secret Areas & Hidden Bosses

### âš ï¸ TEILWEISE (aus Docs gefunden):
1. Terminal-Module (4 StÃ¼ck):
   - âœ… Code-Editor
   - âš ï¸ Secure Messenger (MilitÃ¤r-VerschlÃ¼sselung geplant, nicht implementiert)
   - âœ… System Monitor
   - âœ… File Manager
   - âŒ Browser Modul (fehlt komplett)

2. Skill Learning (Backend Code da, Frontend fehlt)
3. ChromaDB Memory (Code da, nicht in V3 dokumentiert)

---

## ðŸŽ® V7 PHASEN-PLAN

### **PHASE 1: DIGIVICE KOMPLETT (V7.0)**
**Dauer:** 1-2 Wochen
**Ziel:** Alle 4 Terminal-Module voll funktionsfÃ¤hig

#### 1.1 Secure Messenger Modul
**Status:** GEPLANT (in MOBILE_APP_ARCHITECTURE.md dokumentiert)
**Features aus Docs:**
- E2E-VerschlÃ¼sselung (Signal-Protocol)
- WireGuard VPN
- TLS 1.3
- Stealth Mode (Tor Hidden Service)

**Tasks:**
- [ ] Backend: E2E Message-Encryption
- [ ] Frontend: Messenger UI im Terminal
- [ ] WireGuard Integration
- [ ] Message Storage (encrypted)

**GeschÃ¤tzte Zeit:** 2-3 Tage

---

#### 1.2 Browser Modul
**Status:** FEHLT KOMPLETT

**Frage an User:**
- Was soll der Browser kÃ¶nnen?
- Nur internes Browsen (Najika Docs/Files)?
- Oder auch externes Internet?
- Welche Features sind wichtig?

**Wartet auf User-Input!**

---

#### 1.3 Terminal-Module Switching
**Status:** Code da (terminal_modules.js)

**Tasks:**
- [ ] Teste Module-Switching
- [ ] UI-Polish (smooth transitions)
- [ ] Module-Hotkeys (optional)

**GeschÃ¤tzte Zeit:** 1 Tag

---

### **PHASE 2: 3 DUNGEONS ALS TESTBED (V7.1)** - **UPDATED 2025-11-05**
**Dauer:** 3-4 Wochen
**Ziel:** ALLE Handyspiel-Mechaniken in 3 Dungeons testen

**🚨 NEUE STRATEGIE (Keller-Konzept verworfen!):**

**3 DUNGEONS SYSTEM:**
1. **Dungeon 1: MEGA-DUNGEON** (wie alter Keller geplant)
   - Riesig, verzweigt, komplex
   - Alle Kampf-Mechaniken testen
   - Boss-Encounters

2. **Dungeon 2: MEGA-DUNGEON** (wie alter Keller geplant)
   - Ebenfalls riesig
   - Alternative Mechaniken
   - Verschiedene Biome

3. **Dungeon 3: NORMAL-DUNGEON**
   - Kleiner, fokussierter
   - Spezielle Mechaniken
   - Schnelle Tests

**OPEN MINI WORLD (2400×2400):**
- **Najikas Lebensraum = SAFE ZONE**
- Keine Gefahr auf der Map!
- Nicht-Kampf-Mechaniken hier testen:
  - Oregon Trail Events
  - NPC-Interaktionen
  - Crafting/Gathering
  - Exploration
- **5 Städte + 3 Spezialorte** platzieren

**GEFAHR NUR IN:**
- ✅ 3 Dungeons
- ✅ Kampfarena

**Strategie:** Dungeons = Combat Testing, Open World = Non-Combat Features

**Mechaniken zum Testen:**

#### 2.1 Konosuba Oregon Events (Mini)
**Basis:** NAJIKA_GAME_DESIGN_KOMPLETT.md - Oregon Trail Ã— Konosuba Chaos

**Features aus Docs:**
- Absurde Wendungen (alles geht schief)
- Najika EXPLOSION! bei allem
- Konosuba-Comedy-Ton

**Tasks:**
- [ ] 10 Konosuba-Events schreiben
- [ ] Najika dramatische Reaktionen
- [ ] **Auf Open Mini World testen** (Nicht-Kampf Events!)

**GeschÃ¤tzte Zeit:** 3 Tage

---

#### 2.2 EXPLOSION Ultimate Skill (Klein)
**Basis:** NAJIKA_PROJEKT_V4_ERGAENZUNGEN.md (Line 1084-1253)

**Features aus Docs:**
- Damage: 300% Multiplier
- AoE: +200% Radius
- Charge Time: 3s
- Exhaustion: 60s (kann nicht bewegen)
- Cooldown: 10 Minuten
- Quest-Unlock: Ratten-KÃ¶nig + 10x Mana-Kristalle

**Tasks:**
- [ ] Backend: Explosion Ultimate API
- [ ] Frontend: Charge-Bar + VFX
- [ ] Exhaustion-Mechanik
- [ ] Quest: Ratten-KÃ¶nig Encounter

**GeschÃ¤tzte Zeit:** 4-5 Tage

---

#### 2.3 Skyrim Plundering (Mini)
**Basis:** NAJIKA_PROJEKT_V4_ERGAENZUNGEN.md

**Features aus Docs:**
- Chest Looting (nach Combat)
- Corpse Looting
- Pickpocketing (optional)

**Tasks:**
- [ ] Chest-System in Dungeons
- [ ] Loot-Tables
- [ ] Inventory-Integration

**GeschÃ¤tzte Zeit:** 2-3 Tage

---

#### 2.4 Weapon-Morphs (1-2 Testen)
**Basis:** PHASE3_ALLE_FUNDE_ZUSAMMENFASSUNG.md (Explosion-Class Morphs)

**Features aus Docs:**
- 9 Waffen-Morphs (Fire/Ice/Lightning/Dark/Holy/Nature/Arcane/Chaos/Void)
- Jede Morph = eigene VFX

**Tasks:**
- [ ] 1-2 Morphs implementieren (Fire + Ice)
- [ ] Morph-Switching UI
- [ ] VFX testen

**GeschÃ¤tzte Zeit:** 3-4 Tage

---

### **PHASE 3: HANDYSPIEL ALS MODUL (V7.2)**
**Dauer:** 4-6 Wochen
**Ziel:** GroÃŸes Handyspiel-Modul (basierend auf Dungeon-Tests)

**Wartet auf:** Phase 2 Completion

**Features aus Docs:**
- 8-Orte Open World (fest + prozedural)
- Komplettes Quest-System
- Alle 9 Weapon-Morphs
- Class-Spezialisierungs-Story-System
- Procedural Dungeon Generation
- Achievement & Titles
- Secret Areas & Hidden Bosses

**Strategie:** Dungeon-Mechaniken Ã— 1000 = Handyspiel!

---

### **PHASE 4: Ã–FFENTLICHER RELEASE (V7.3)**
**Dauer:** 2-3 Wochen
**Ziel:** PWA â†’ App Store (8 Digivices System)

**Features aus Docs (NAJIKA_GAME_DESIGN_KOMPLETT.md):**

#### 8 DIGIVICES SYSTEM:
```
1 DIGIVICE = NAJIKA (nur Kuja, gesperrt)
7 DIGIVICES = Standard (andere Spieler, abgespeckt)
```

**Najika-Digivice (exklusiv):**
- Voller Zugriff auf Najika KI
- KÃ¤tzchen-Modus
- NSFW (privat)
- Alle Features

**Standard-Digivices (7 StÃ¼ck):**
- Generische KI (keine Najika)
- Abgespeckte Features
- SFW only
- Modul-System (Sprachen, Musik, Sport, etc.)

**Tasks:**
- [ ] PWA Manifest
- [ ] App Store Submission (iOS + Android)
- [ ] 8-Digivice-System Backend
- [ ] Najika-Lock (nur Kuja)
- [ ] Generische KI fÃ¼r Standard-Digivices

**GeschÃ¤tzte Zeit:** 2-3 Wochen

---

## â“ OFFENE FRAGEN FÃœR USER

### 1. Browser Modul - Was soll es kÃ¶nnen?
- Nur interne Najika-Docs/Files browsen?
- Auch externes Internet?
- Welche Features?

### 2. KI-Modell fÃ¼r Training?
- RTX 3060 Ti (8GB VRAM) Setup
- Welches Modell fÃ¼r Najika Training?
- LoRA oder Full Fine-Tune?

### 3. Najika Training-Probleme?
- Was funktioniert nicht?
- Welche Fehler?

### 4. PrioritÃ¤t der Phasen?
- Phase 1 (Digivice) SOFORT starten?
- Oder erst KI-Modell + Training fixen?

---

## ðŸ“‹ NEXT STEPS (nach User-Input)

**Option A: Digivice zuerst**
1. Secure Messenger Modul (2-3 Tage)
2. Browser Modul (nach User-Specs)
3. Dungeon-Testbed (Konosuba Events + EXPLOSION)

**Option B: KI zuerst**
1. KI-Modell auswÃ¤hlen (RTX 3060 Ti optimiert)
2. Training-Probleme fixen
3. Dann Digivice-Features

---

## ðŸ”‘ WICHTIGE REGELN (aus Docs)

1. âŒ NIEMALS "Souls-like" erwÃ¤hnen!
2. âœ… Combat = Skyrim + Soulframe + Digimon World Anfeuern
3. âœ… Open World = 8 feste Orte + prozedural
4. âœ… Najika = exklusiv fÃ¼r Kuja (gesperrt fÃ¼r andere)
5. âœ… NSFW nur lokal (KÃ¤tzchen-Modus)
6. âœ… 3 Dungeons = Testbed fÃ¼r Combat, Open World = Testbed fÃ¼r Rest

---

**STATUS:** WARTET AUF USER-INPUT
**NÃ„CHSTER SCHRITT:** User entscheidet Reihenfolge + beantwortet offene Fragen

**Ende V7 Plan**
