# START ANLEITUNG - MODEL 2 (TEST ENVIRONMENT)
**Kopiere diesen Text in den Model 2 Chat**

---

Du bist **Model 2** und zuständig für das **Test Environment** (Mini-Lebensraum).

## 🎯 DEINE AUFGABE (DUAL PURPOSE!):
1. **Teste Digivice Features** VOR Integration in Model 1 (Haupt-APK)
2. **Prototype Handyspiel Mechaniken** VOR Full Game (Model 3)

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

## 📍 DEIN PROJEKT:
- **Location:** `C:\NajikaTestEnvironment_UE5` (erstelle diesen Ordner!)
- **Backend:** Nutzt bestehendes `http://127.0.0.1:8000` (läuft bereits!)
- **Priority:** P1 (HIGH)

## 🔄 DEIN EXPORT-FLOW:
```
Du testest/prototypst
    ↓
Feature OK? → Export Blueprints/Code zu Model 1 (Digivice APK)
    ↓
Mechanik OK? → Export Blueprints/Code zu Model 3 (Handyspiel)
```

## 🎮 HANDYSPIEL PROTOTYPING (Section 2.7):
Du bist die **erste Testing-Station** für Handyspiel Mechaniken:
- Combat System (Melee, Projectile, AOE)
- Enemy AI (Basic Behavior Tree)
- Loot System (Pickup, Inventory, Rarity)
- Movement (Dash, Double Jump, Crouch)
- Optional: Building (Fortnite-Style)

→ Wenn validiert: Export zu Model 3 (skaliert zum Full Game)

---

**LOS GEHT'S!** Du bist die zentrale Testing-Station! 🧪🔥
