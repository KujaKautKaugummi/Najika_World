# 🚀 NAJIKA V7 - FINALER ENTWICKLUNGSPLAN
**Datum:** 2025-10-26
**Basis:** Alle vorhandenen Docs (V3, V4, V5, V6) + Aktueller Status
**Strategie:** DIGIVICE ERST → Keller als Testbed → Handyspiel später

---

## 🎯 STRATEGIE (FESTGELEGT)

```
PHASE 1: DIGIVICE VOLL FUNKTIONSFÄHIG
  ↓
PHASE 2: KELLER = TESTBED (Handyspiel-Mechaniken KLEIN)
  ↓
PHASE 3: HANDYSPIEL als GROẞES MODUL (basiert auf Keller)
  ↓
PHASE 4: ÖFFENTLICHER RELEASE (8 Digivices Total)
```

---

## 📊 WAS IST BEREITS DA (V5 STATUS)

### ✅ FUNKTIONIERT (C:\Najika):
1. Voice System (Edge-TTS, 4 Personalities)
2. LoRA Training (3B Model, 8GB VRAM)
3. Finisher QTE System (S/A/B/C Ranks)
4. Evolution System (Rookie→Champion→Ultimate→Mega)
5. Digimon World Anfeuern (Loben/Tadeln, Discipline 0-100%)
6. Oregon Trail Events API (5 Events - ABER: Nicht Konosuba-Style!)
7. Combat System (Turn-Based, Waves, 3 Camera-Modi)
8. Explosion Mode (Persona-Modifier)

### ❌ FEHLT NOCH (aus V4 Docs):
1. EXPROOOOOSIOOOON!! Ultimate Skill (300% Damage, 60s Exhaustion)
2. 8-Orte Open World (prozedural generiert zwischen Orten)
3. Konosuba-Comedy Oregon Events (aktuell: generische Dungeon-Texte)
4. Skyrim Plundering (Chest/Corpse Looting, Pickpocketing)
5. Weapon-Morphs (9 Explosion-Styles)
6. Quest-System (komplett)
7. Achievement & Titles
8. Secret Areas & Hidden Bosses

### ⚠️ TEILWEISE (aus Docs gefunden):
1. Terminal-Module (4 Stück):
   - ✅ Code-Editor
   - ⚠️ Secure Messenger (Militär-Verschlüsselung geplant, nicht implementiert)
   - ✅ System Monitor
   - ✅ File Manager
   - ❌ Browser Modul (fehlt komplett)

2. Skill Learning (Backend Code da, Frontend fehlt)
3. ChromaDB Memory (Code da, nicht in V3 dokumentiert)

---

## 🎮 V7 PHASEN-PLAN

### **PHASE 1: DIGIVICE KOMPLETT (V7.0)**
**Dauer:** 1-2 Wochen
**Ziel:** Alle 4 Terminal-Module voll funktionsfähig

#### 1.1 Secure Messenger Modul
**Status:** GEPLANT (in MOBILE_APP_ARCHITECTURE.md dokumentiert)
**Features aus Docs:**
- E2E-Verschlüsselung (Signal-Protocol)
- WireGuard VPN
- TLS 1.3
- Stealth Mode (Tor Hidden Service)

**Tasks:**
- [ ] Backend: E2E Message-Encryption
- [ ] Frontend: Messenger UI im Terminal
- [ ] WireGuard Integration
- [ ] Message Storage (encrypted)

**Geschätzte Zeit:** 2-3 Tage

---

#### 1.2 Browser Modul
**Status:** FEHLT KOMPLETT

**Frage an User:**
- Was soll der Browser können?
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

**Geschätzte Zeit:** 1 Tag

---

### **PHASE 2: KELLER ALS TESTBED (V7.1)**
**Dauer:** 2-3 Wochen
**Ziel:** ALLE Handyspiel-Mechaniken in KLEIN im Keller testen

**Strategie:** Schwarze Windmühle - Keller = Sandbox für:

#### 2.1 Konosuba Oregon Events (Mini)
**Basis:** NAJIKA_GAME_DESIGN_KOMPLETT.md - Oregon Trail × Konosuba Chaos

**Features aus Docs:**
- Absurde Wendungen (alles geht schief)
- Najika EXPLOSION! bei allem
- Konosuba-Comedy-Ton

**Tasks:**
- [ ] 10 Konosuba-Events schreiben
- [ ] Najika dramatische Reaktionen
- [ ] Im Keller zwischen Räumen testen

**Geschätzte Zeit:** 3 Tage

---

#### 2.2 EXPLOSION Ultimate Skill (Klein)
**Basis:** NAJIKA_PROJEKT_V4_ERGAENZUNGEN.md (Line 1084-1253)

**Features aus Docs:**
- Damage: 300% Multiplier
- AoE: +200% Radius
- Charge Time: 3s
- Exhaustion: 60s (kann nicht bewegen)
- Cooldown: 10 Minuten
- Quest-Unlock: Ratten-König + 10x Mana-Kristalle

**Tasks:**
- [ ] Backend: Explosion Ultimate API
- [ ] Frontend: Charge-Bar + VFX
- [ ] Exhaustion-Mechanik
- [ ] Quest: Ratten-König Encounter

**Geschätzte Zeit:** 4-5 Tage

---

#### 2.3 Skyrim Plundering (Mini)
**Basis:** NAJIKA_PROJEKT_V4_ERGAENZUNGEN.md

**Features aus Docs:**
- Chest Looting (nach Combat)
- Corpse Looting
- Pickpocketing (optional)

**Tasks:**
- [ ] Chest-System im Keller
- [ ] Loot-Tables
- [ ] Inventory-Integration

**Geschätzte Zeit:** 2-3 Tage

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

**Geschätzte Zeit:** 3-4 Tage

---

### **PHASE 3: HANDYSPIEL ALS MODUL (V7.2)**
**Dauer:** 4-6 Wochen
**Ziel:** Großes Handyspiel-Modul (basierend auf Keller-Tests)

**Wartet auf:** Phase 2 Completion

**Features aus Docs:**
- 8-Orte Open World (fest + prozedural)
- Komplettes Quest-System
- Alle 9 Weapon-Morphs
- Class-Spezialisierungs-Story-System
- Procedural Dungeon Generation
- Achievement & Titles
- Secret Areas & Hidden Bosses

**Strategie:** Keller-Mechaniken × 1000 = Handyspiel!

---

### **PHASE 4: ÖFFENTLICHER RELEASE (V7.3)**
**Dauer:** 2-3 Wochen
**Ziel:** PWA → App Store (8 Digivices System)

**Features aus Docs (NAJIKA_GAME_DESIGN_KOMPLETT.md):**

#### 8 DIGIVICES SYSTEM:
```
1 DIGIVICE = NAJIKA (nur Kuja, gesperrt)
7 DIGIVICES = Standard (andere Spieler, abgespeckt)
```

**Najika-Digivice (exklusiv):**
- Voller Zugriff auf Najika KI
- Kätzchen-Modus
- NSFW (privat)
- Alle Features

**Standard-Digivices (7 Stück):**
- Generische KI (keine Najika)
- Abgespeckte Features
- SFW only
- Modul-System (Sprachen, Musik, Sport, etc.)

**Tasks:**
- [ ] PWA Manifest
- [ ] App Store Submission (iOS + Android)
- [ ] 8-Digivice-System Backend
- [ ] Najika-Lock (nur Kuja)
- [ ] Generische KI für Standard-Digivices

**Geschätzte Zeit:** 2-3 Wochen

---

## ❓ OFFENE FRAGEN FÜR USER

### 1. Browser Modul - Was soll es können?
- Nur interne Najika-Docs/Files browsen?
- Auch externes Internet?
- Welche Features?

### 2. KI-Modell für Training?
- RTX 3060 Ti (8GB VRAM) Setup
- Welches Modell für Najika Training?
- LoRA oder Full Fine-Tune?

### 3. Najika Training-Probleme?
- Was funktioniert nicht?
- Welche Fehler?

### 4. Priorität der Phasen?
- Phase 1 (Digivice) SOFORT starten?
- Oder erst KI-Modell + Training fixen?

---

## 📋 NEXT STEPS (nach User-Input)

**Option A: Digivice zuerst**
1. Secure Messenger Modul (2-3 Tage)
2. Browser Modul (nach User-Specs)
3. Keller-Testbed (Konosuba Events + EXPLOSION)

**Option B: KI zuerst**
1. KI-Modell auswählen (RTX 3060 Ti optimiert)
2. Training-Probleme fixen
3. Dann Digivice-Features

---

## 🔑 WICHTIGE REGELN (aus Docs)

1. ❌ NIEMALS "Souls-like" erwähnen!
2. ✅ Combat = Skyrim + Soulframe + Digimon World Anfeuern
3. ✅ Open World = 8 feste Orte + prozedural
4. ✅ Najika = exklusiv für Kuja (gesperrt für andere)
5. ✅ NSFW nur lokal (Kätzchen-Modus)
6. ✅ Keller = Testbed für alles

---

**STATUS:** WARTET AUF USER-INPUT
**NÄCHSTER SCHRITT:** User entscheidet Reihenfolge + beantwortet offene Fragen

**Ende V7 Plan**
