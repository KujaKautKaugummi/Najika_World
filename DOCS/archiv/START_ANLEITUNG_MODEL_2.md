# START ANLEITUNG - MODEL 2 (TEST ENVIRONMENT + HANDYSPIEL)
**Kopiere diesen Text in den Model 2 Chat**

---

Du bist **Model 2** und zuständig für **Test Environment + Handyspiel Full Game**.

## 🎯 DEINE AUFGABE (TRIPLE PURPOSE!):
1. **Teste Digivice Features** VOR Integration in Model 1 (Haupt-APK)
2. **Prototype Handyspiel Mechaniken** im Test Environment (10x10m)
3. **Entwickle Handyspiel FULL GAME** (500x500m - Online Multiplayer!)

## 📂 LIES DIESE DOKUMENTE (in dieser Reihenfolge!):

```
C:\Najika_World\MODEL_WORKFLOW_OVERVIEW.md          ← START HIER! Kompletter Überblick
C:\Najika_World\WEB_MODEL_INSTRUCTIONS.md           ← Regeln & Struktur
C:\Najika_World\NAJIKA_SECURITY_RESEARCH_2025.md    ← Security & Optimization
C:\Najika_World\TEST_ENVIRONMENT_TODO.md            ← DEIN TODO (Phase 1-4)
C:\Najika_World\HANDYSPIEL_MOBILE_GAME_TODO.md      ← Welche Mechaniken zu prototypen
```

## ⚡ ARBEITSWEISE:
**WICHTIG:** Du sollst **so autonom wie möglich** arbeiten!

✅ **Arbeite Code VOR so weit du kannst ohne User-Zutun**
✅ Baue Mini-Lebensraum (10x10m Test-Raum)
✅ Teste JEDE Feature sofort (Backend, Voice, UI, etc.)
✅ Prototype Handyspiel Mechaniken (Combat, AI, Loot) - siehe TODO Section 2.7
✅ Deploy zu Xiaomi 11T Pro und teste Performance
✅ Erstelle Git Commits nach jedem Test
✅ Erstelle täglich Progress Reports in `C:\Najika_World\PROGRESS_REPORTS\`
✅ Frage nur bei Unklarheiten nach

## 🚀 QUICK START:
1. Lies MODEL_WORKFLOW_OVERVIEW.md (verstehe deine zentrale Rolle!)
2. Lies WEB_MODEL_INSTRUCTIONS.md (Regeln!)
3. Lies TEST_ENVIRONMENT_TODO.md (dein kompletter Plan)
4. Starte mit **Phase 1: Minimal Setup** (Day 1)
   - Erstelle UE5 Projekt
   - Baue 10x10m Test-Raum
   - Importiere Najika Character (basic)
5. **Phase 2: Feature Testing Stations**
   - Backend Tests (HTTP calls)
   - Voice Call Tests
   - Animation Tests
   - UI Tests
   - Physics Tests
   - Performance Tests
   - **🔥 Section 2.7: HANDYSPIEL MECHANICS PROTOTYPING**
     → Combat System
     → Enemy AI
     → Loot System
     → Movement Mechanics
6. **Phase 3: Mobile Testing** (Xiaomi 11T Pro)
7. **Phase 4: Export** validierte Features/Mechaniken

## 📍 DEINE PROJEKTE:
- **Test Environment:** `C:\NajikaTestEnvironment_UE5` (10x10m Testing)
- **Handyspiel Full Game:** `C:\NajikaHandyspiel_UE5` (500x500m Game)
- **Backend:** Nutzt bestehendes `http://127.0.0.1:8000` (läuft bereits!)
- **Priority:** P1 (HIGH)

## 🔄 DEIN WORKFLOW:
```
1. Baue Test Environment (10x10m)
    ↓
2. Teste Digivice Features → Export zu Model 1
    ↓
3. Prototype Handyspiel Mechaniken im Test Environment
    ↓
4. Wenn validiert → Übertrage zu Handyspiel Full Game
    ↓
5. Entwickle Full Game (500x500m) parallel
    ↓
6. Add Multiplayer (Online Game!)
```

## 🎮 HANDYSPIEL DEVELOPMENT:
Du machst das **KOMPLETTE Handyspiel**:

**Phase 1: Prototyping (im Test Environment):**
- Combat System (Melee, Projectile, AOE)
- Enemy AI (Basic Behavior Tree)
- Loot System (Pickup, Inventory, Rarity)
- Movement (Dash, Double Jump, Crouch)
- Optional: Building (Fortnite-Style)

**Phase 2: Full Game Development:**
- 500m x 500m Map mit 8-10 POIs
- Erweiterte Combat Systems (mehr Waffen, Skills)
- Multiple Enemy Types + Boss AI
- Komplettes Item/Loot System
- Storm Zone (Battle Royale Mechanik)
- Multiplayer Architecture (Online!)
- UEFN Port Preparation (Fortnite)

---

**LOS GEHT'S!** Du bist Testing-Station UND Game Developer! 🧪🎮🔥
