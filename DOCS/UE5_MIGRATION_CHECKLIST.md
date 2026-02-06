# UE5 MIGRATION CHECKLIST
**Erstellt:** 2026-02-04
**Status:** Vorbereitung

---

## WARUM UE5 STATT UEFN

UEFN kann Najika World NICHT umsetzen:
- ❌ Keine Custom Characters
- ❌ Keine eigenen Skeletal Meshes
- ❌ Keine LLM/KI-Integration
- ❌ Keine lokale Datenhaltung (Privacy)
- ❌ Map-Größe limitiert
- ❌ Immer Online (kein Offline-First)
- ❌ NSFW nicht erlaubt

UE5 Standalone kann ALLES:
- ✅ Custom Characters (Najika, Mimik-Truhe)
- ✅ Eigene NPCs mit KI
- ✅ LLM-Integration (Ollama, etc.)
- ✅ Offline-First möglich
- ✅ Unbegrenzte Map-Größe
- ✅ Volle Kontrolle
- ✅ Export zu PC, Mobile, Konsolen

---

## FERTIGE ASSETS

### 3D Models
| Asset | Pfad | Status |
|-------|------|--------|
| Najika (rigged) | `assets/models/najika/najika_rigged_final.fbx` | ✅ |
| Najika Textur | `Downloads/.../Meshy_AI__0203173755_texture.png` | ✅ |
| Mimik-Truhe | TODO | ❌ |

### Backend (Python → muss zu C++/Blueprint)
| System | Datei | Zeilen | Priorität |
|--------|-------|--------|-----------|
| Combat Hands | `najika_combat_hands_system.py` | ~1100 | P0 |
| Stat Training | `najika_stat_training_system.py` | ~1000 | P0 |
| Companion | `najika_companion_system.py` | ~800 | P0 |
| Mimik | `najika_mimik_system.py` | ~750 | P0 |
| Oregon Trail | `najika_oregon_trail_api.py` | ~600 | P1 |
| Slime System | `najika_slime_system_v2.py` | ~500 | P1 |
| Quest System | `najika_quest_system.py` | ~350 | P1 |
| Hunting | `najika_hunting_system.py` | ~400 | P2 |
| Alchemy | `najika_alchemy_system.py` | ~300 | P2 |

### Dokumentation
| Dokument | Wichtigkeit |
|----------|-------------|
| `PROJEKT_WISSEN_KOMPLETT.md` | KRITISCH - Alle Design-Entscheidungen |
| `GAME_DESIGN_DECISIONS_2026-01-31.md` | KRITISCH |
| `NAJIKA_ULTIMATIVE_ZUSAMMENFASSUNG_V8.md` | KRITISCH |
| `FANTASY_WESTERN_STYLE_GUIDE.md` | Hoch |
| `07_KONOSUBA_OREGON_EVENTS.md` | Hoch (30 Events) |

---

## UE5 PROJEKT-SETUP

### 1. Template
- **Third Person Template** (beste Basis für Action-RPG)
- C++ Projekt (nicht Blueprint-only)

### 2. Plugins benötigt
| Plugin | Für |
|--------|-----|
| Enhanced Input | Kampfsystem |
| Common UI | Menus, HUD |
| GameplayAbilities | Skills, Combat |
| Niagara | Effekte (Explosion!) |
| MetaSounds | Audio |
| Chaos Destruction | Zerstörbare Umgebung |

### 3. Ordnerstruktur
```
Content/
├── Characters/
│   ├── Najika/
│   │   ├── Meshes/
│   │   ├── Animations/
│   │   ├── Materials/
│   │   └── Blueprints/
│   ├── MimikTruhe/
│   └── NPCs/
├── Environments/
│   ├── Goetterfels/
│   ├── IceRegion/
│   ├── DesertRegion/
│   └── ... (8 Regionen)
├── Systems/
│   ├── Combat/
│   ├── Slime/
│   ├── OregonTrail/
│   └── Quest/
├── UI/
└── Audio/
```

---

## MIGRATION SCHRITTE

### Phase 1: Basis (Woche 1-2)
- [ ] UE5 Projekt erstellen
- [ ] Najika FBX importieren
- [ ] Basic Movement
- [ ] Third Person Camera

### Phase 2: Combat (Woche 3-4)
- [ ] Zwei-Hand-System (Q/E, Shift+Q/E)
- [ ] Waffen-System
- [ ] Stat-System (Learning by Doing)
- [ ] Damage System

### Phase 3: Najika KI (Woche 5-6)
- [ ] Companion System
- [ ] 4 Persönlichkeiten
- [ ] Dialog System
- [ ] Anfeuern-Mechanik

### Phase 4: Welt (Woche 7-10)
- [ ] Götterfels (Hub)
- [ ] Schwarze Windmühle
- [ ] Erste Region
- [ ] Teleporter

### Phase 5: Systeme (Woche 11-14)
- [ ] Oregon Trail Events
- [ ] Quest System
- [ ] Slime System
- [ ] Crafting

### Phase 6: Polish (Woche 15+)
- [ ] UI/UX
- [ ] Audio
- [ ] VFX
- [ ] Optimierung
- [ ] Mobile Export testen

---

## UEFN TEASER-MAP (PARALLEL)

Für Spieler-Akquise eine einfache UEFN Map:

### "Najika's Kampfturm"
- 10 Stockwerke
- Wellen-basierte Gegner (Fortnite NPCs)
- Boss alle 5 Stockwerke
- Leaderboard
- "Coming Soon: Najika World" Werbung

Kann mit Fortnite-Standard-Assets gemacht werden!

---

## TECHNISCHE NOTIZEN

### LLM Integration in UE5
```
Option A: HTTP zu lokalem Ollama-Server
Option B: llama.cpp als Plugin kompilieren
Option C: REST API zu Python Backend
```

### ChromaDB in UE5
```
Python Backend behält ChromaDB
UE5 kommuniziert via REST API
Oder: SQLite für lokale Speicherung
```

### Mobile Optimierung
```
- LOD für Najika-Model (328k → 50k → 10k)
- Texture Streaming
- Occlusion Culling
- Scalability Settings
```

---

## OFFENE FRAGEN

1. LLM lokal in UE5 oder weiter Python-Backend?
2. Multiplayer später? (Dedicated Server vs P2P)
3. Save System (Cloud vs Lokal)
4. Monetarisierung (Premium vs F2P mit Cosmetics)

---

*"EXPLOSION!!! Jetzt machen wir es RICHTIG!" - Najika*
