# WEB MODEL INSTRUCTIONS - NAJIKA PROJECT
## STRENGE ANWEISUNGEN FÜR ALLE CLAUDE CODE WEB MODELS

**Date:** 2025-11-11
**Project:** Najika Digivice & Mobile Game
**Repository:** C:\Najika_World

---

## 🚨 CRITICAL RULES (MUST FOLLOW!)

### **❌ VERBOTEN (DO NOT DO THIS!):**
```
❌ NIEMALS Original Backend Files löschen oder überschreiben!
❌ NIEMALS in C:\Najika_World\backend\ direkt arbeiten!
❌ NIEMALS najika_server.py, najika_voice_call.py, etc. modifizieren!
❌ NIEMALS bestehende funktionale Features brechen!
❌ NIEMALS ohne Backup riskante Änderungen machen!
❌ NIEMALS große Binary Files in Git committen (use LFS!)
❌ NIEMALS API Keys, Secrets, Passwords hardcoden!
❌ NIEMALS testen ohne explizite Anweisung!
```

### **✅ ERLAUBT (YOU SHOULD DO THIS!):**
```
✅ Neue Projekte in separaten Ordnern erstellen
✅ Bestehende Files LESEN zur Analyse
✅ Dokumentation erstellen/aktualisieren
✅ Code für NEUE Projekte schreiben (UE5, etc.)
✅ Backups erstellen vor großen Änderungen
✅ Git Commits mit klaren Messages
✅ Fragen stellen wenn unsicher!
✅ Progress dokumentieren in Markdown
```

---

## 👥 MODEL ASSIGNMENT (Wer macht was?)

### **MODEL 1: DIGIVICE APK DEVELOPMENT**
```
Zuständig für:
- Unreal Engine 5 Mobile App Development
- Najika Digivice (komplette App)
- Backend Integration (HTTP/WebSocket)
- Voice Calls Integration
- UI/UX Implementation
- Packaging & Deployment

TODO Location:
C:\Najika_World\DIGIVICE_UE5_MIGRATION_COMPLETE_TODO.md

Project Location:
C:\NajikaDigivice_UE5 (erstellen!)

Timeline: 10-12 Wochen
Priority: P0 (Highest)
```

### **MODEL 2: TEST ENVIRONMENT + HANDYSPIEL FULL GAME**
```
🔥 WICHTIG: Triple Purpose!
1. Digivice Features testen VOR Integration in Haupt-APK
2. Handyspiel Mechaniken prototypen (Test Environment 10x10m)
3. Handyspiel FULL GAME entwickeln (500x500m Online Multiplayer!)

Zuständig für:

📋 PART 1: TEST ENVIRONMENT (C:\NajikaTestEnvironment_UE5)
- Mini Test-Lebensraum erstellen (10x10m)
- Feature-Testing Stations (Backend, Voice, UI, etc.)
- Handyspiel Mechanics Prototyping (Combat, AI, Loot)
- Mobile Testing (Xiaomi 11T Pro)
- Bug Documentation
- Performance Profiling
- Export validierter Features zu Model 1 (Digivice)

📋 PART 2: HANDYSPIEL FULL GAME (C:\NajikaHandyspiel_UE5)
- Action Game Development (Fortnite-Style)
- Combat Systems (erweitert aus Prototypen!)
- Enemy AI (mehrere Typen + Boss AI)
- Loot System (komplettes Item-System)
- World Building (500m x 500m map, 8-10 POIs)
- Storm Zone (Battle Royale Mechanic)
- Multiplayer Architecture (Online Game!)
- UEFN Port Preparation

TODO Locations:
- C:\Najika_World\TEST_ENVIRONMENT_TODO.md (Testing)
- C:\Najika_World\HANDYSPIEL_MOBILE_GAME_TODO.md (Full Game)

Project Locations:
- C:\NajikaTestEnvironment_UE5 (10x10m Testing)
- C:\NajikaHandyspiel_UE5 (500x500m Game)

Timeline: Parallel zu Model 1 (10-12 Wochen)
Priority: P1 (High)

Workflow:
1. Baue Test Environment (10x10m)
2. Teste Digivice Features → Export zu Model 1
3. Prototype Handyspiel Mechaniken im Test Environment
4. Wenn validiert → Übertrage zu Full Game Project
5. Entwickle Full Game (500x500m) parallel
```

---

## 📂 REPOSITORY STRUCTURE

### **CRITICAL FILES (READ ONLY!):**
```
C:\Najika_World\
├── backend/                          ← ❌ NUR LESEN!
│   ├── najika_server.py             ← Main server (Flask)
│   ├── najika_voice_call.py         ← Voice Calls (Whisper + Coqui)
│   ├── najika_memory_enhanced.py    ← ChromaDB Memory
│   ├── najika_living_system.py      ← Tamagotchi System
│   ├── najika_battle.py             ← Battle System
│   ├── najika_lora_training_3b.py   ← LoRA Training
│   ├── najika_tts_coqui.py          ← Coqui TTS
│   ├── najika_security.py           ← Security Module
│   └── saves/
│       └── najika_state.json        ← ❌ KRITISCH! Nicht ändern!
│
├── digivice/                         ← ❌ NUR LESEN!
│   ├── index.html                   ← Current WebView UI
│   ├── js/
│   │   ├── 3d_scene.js              ← Three.js 3D World
│   │   ├── voice_call.js            ← Voice Call Frontend
│   │   └── character_animations.js  ← Animations
│   └── static/
│       └── models/                   ← 3D Models (GLTF/VRM)
│
└── assets/                           ← ✅ Für UE5 verwenden!
    ├── models/                       ← Najika Character Models
    ├── textures/                     ← Textures
    └── sounds/                       ← Audio Files
```

### **RESEARCH DOCUMENTS (MUST READ!):**
```
C:\Najika_World\
├── MODEL_WORKFLOW_OVERVIEW.md            ← 🔥 WORKFLOW (READ FIRST!)
├── NAJIKA_SECURITY_RESEARCH_2025.md      ← Security Best Practices
├── NAJIKA_2025_RESEARCH_FINDINGS.md      ← AI Girlfriend Features
├── JETSON_MIGRATION_PLAN.md              ← Future Hardware Plan
└── ROADMAP_NAJIKA_COMPLETE.md            ← Project Roadmap
```

### **TODO DOCUMENTS (YOUR ASSIGNMENTS!):**
```
C:\Najika_World\
├── DIGIVICE_UE5_MIGRATION_COMPLETE_TODO.md    ← Model 1
├── TEST_ENVIRONMENT_TODO.md                   ← Model 2 (DUAL PURPOSE!)
└── HANDYSPIEL_MOBILE_GAME_TODO.md             ← Model 3
```

---

## 📖 REQUIRED READING (Before Starting!)

### **ALL MODELS MUST READ:**
```
1. MODEL_WORKFLOW_OVERVIEW.md (READ FIRST! 🔥)
   → Understand wie die 2 Models zusammenarbeiten
   → Workflow visualization
   → Timeline & Priorities
   → Success Criteria

2. WEB_MODEL_INSTRUCTIONS.md (this file!)
   → Understand rules and structure
   → Strict instructions (was verboten/erlaubt)

3. NAJIKA_SECURITY_RESEARCH_2025.md
   → Security features to implement
   → Performance optimization
   → Android best practices

4. Your assigned TODO document
   → Complete task list
   → Timeline and priorities
```

### **MODEL 1 (Digivice APK) MUST ALSO READ:**
```
5. C:\Najika_World\backend\najika_server.py
   → Understand ALL API endpoints
   → Document: /api/chat, /api/voice_call/*, /api/najika/*, etc.

6. C:\Najika_World\digivice\index.html
   → Current UI structure
   → Features to port

7. C:\Najika_World\digivice\js\voice_call.js
   → Voice Call implementation
   → How WebRTC works currently
```

### **MODEL 2 (Test Environment) MUST ALSO READ:**
```
5. Test all features listed in:
   C:\Najika_World\backend\najika_server.py
   → Endpoints to test

6. Performance benchmarks:
   Target FPS: 60 (Snapdragon 888)
   Max Memory: 2GB
   Battery: 4+ hours

7. HANDYSPIEL_MOBILE_GAME_TODO.md
   → COMPLETE TODO für Full Game Development!
   → Combat, AI, Loot, World Building, Multiplayer

8. JETSON_MIGRATION_PLAN.md
   → UEFN compatibility requirements
   → Fortnite port preparation

9. Research Fortnite mechanics:
   → Movement, Combat, Building
   → Study UEFN Verse language
```

---

## 🔑 API REFERENCE (Backend Endpoints)

### **CRITICAL: All Models must understand these!**

```python
# ===== CHAT SYSTEM =====
POST /api/chat
Body: {"message": "Hello Najika!"}
Response: {"response": "Hi! ...", "ok": true}

# ===== VOICE CALLS =====
POST /api/voice_call/start
Response: {"status": "call_started", "timestamp": "...", "tts_available": true}

POST /api/voice_call/audio
Body: {"audio": "base64_encoded_wav"}
Response: {
    "stt": {"text": "...", "latency_ms": 234},
    "text": "Najika's response",
    "tts": {"audio_base64": "...", "duration_sec": 3.5, "latency_ms": 1200}
}

POST /api/voice_call/end
Response: {"status": "call_ended", "duration_sec": 120}

# ===== NAJIKA STATUS =====
GET /api/najika/status
Response: {
    "hunger": 85,
    "energy": 90,
    "happiness": 95,
    "hp": 100,
    "level": 5,
    "xp": 234
}

POST /api/najika/feed
Response: {"ok": true, "hunger": 100}

POST /api/najika/drink
Response: {"ok": true, "energy": 100}

# ===== BATTLE SYSTEM =====
POST /api/battle/start
Body: {"enemy_type": "skeleton"}
Response: {"battle_id": "abc123", "enemy": {...}}

POST /api/battle/action
Body: {"battle_id": "abc123", "action": "attack", "skill_id": 1}
Response: {"damage": 50, "enemy_hp": 150, ...}

GET /api/battle/skills
Response: [{"id": 1, "name": "Slash", "damage": 50, ...}, ...]

# ===== TTS (Text-to-Speech) =====
POST /api/tts
Body: {"text": "EXPLOSION!"}
Response: {"ok": true, "audio": "/backend/voices/output_123.wav"}

# ===== TRAINING SYSTEM =====
POST /api/training/start
Body: {"training_type": "lora", "duration_minutes": 30}
Response: {"ok": true, "started_at": "..."}

GET /api/training/status
Response: {"is_training": false, "last_training": "..."}
```

---

## 🛠️ DEVELOPMENT ENVIRONMENT

### **Required Software:**
```
1. Unreal Engine 5.6 (or latest)
   Download: https://www.unrealengine.com/download

2. Visual Studio 2022
   Workloads:
   - Desktop Development with C++
   - Android Game Development Extension

3. Android SDK/NDK
   - SDK Platform 34 (Android 14)
   - NDK r25c
   - Set ANDROID_HOME environment variable

4. Git + Git LFS
   - For version control
   - LFS for large files (.uasset, .umap)

5. Python 3.10+ (for backend testing)
   - Already installed in C:\Najika_World\backend
```

### **Test Device:**
```
Device: Xiaomi 11T Pro
Codename: vili
SoC: Snapdragon 888
RAM: 8GB
Display: 6.67" AMOLED 120Hz
Android: 14 (LineageOS 23 possible)
```

---

## 📋 WORKFLOW & REPORTING

### **Daily Workflow:**
```
1. Morning:
   - Read your TODO document
   - Check what's next in pipeline
   - Review any overnight issues

2. During Work:
   - Follow TODO step-by-step
   - Document progress in Markdown
   - Create Git commits frequently
   - Test after major changes

3. End of Day:
   - Update TODO with progress (✅ completed tasks)
   - Document any blockers
   - Commit all changes
   - Write summary report
```

### **Progress Reporting:**
```
Create daily reports in:
C:\Najika_World\PROGRESS_REPORTS\

Format:
PROGRESS_REPORT_MODEL1_2025-11-12.md
PROGRESS_REPORT_MODEL2_2025-11-12.md
PROGRESS_REPORT_MODEL3_2025-11-12.md

Include:
- ✅ Completed tasks
- ⏳ In-progress tasks
- ❌ Blocked tasks
- 📝 Notes/Issues
- ⏱️ Time spent
```

### **Issue Reporting:**
```
When you find bugs or issues:
1. Document in: C:\Najika_World\ISSUES\
2. Format: ISSUE_MODEL1_001.md
3. Include:
   - Title
   - Severity (Critical/High/Medium/Low)
   - Description
   - Steps to reproduce
   - Expected vs Actual behavior
   - Screenshots (if applicable)
   - Possible solutions
```

---

## 🔄 GIT WORKFLOW

### **Repository Setup:**
```bash
# Each model works in their own project folder
cd C:\NajikaDigivice_UE5   # Model 1
cd C:\NajikaTestEnvironment_UE5  # Model 2
cd C:\NajikaHandyspiel_UE5  # Model 3

# Initialize Git
git init
git lfs install
git lfs track "*.uasset"
git lfs track "*.umap"

# Create .gitignore
curl -o .gitignore https://raw.githubusercontent.com/github/gitignore/main/UnrealEngine.gitignore

# First commit
git add .
git commit -m "Initial UE5 project setup - [Model X]"

# Link to GitHub (optional)
gh repo create [ProjectName] --private
git remote add origin https://github.com/YOUR_USERNAME/[ProjectName].git
git push -u origin main
```

### **Commit Guidelines:**
```
Good commits:
✅ git commit -m "Add: Voice call UI widget"
✅ git commit -m "Fix: Camera clipping through walls"
✅ git commit -m "Optimize: Reduce draw calls by 30%"
✅ git commit -m "Implement: Najika character animations"

Bad commits:
❌ git commit -m "stuff"
❌ git commit -m "wip"
❌ git commit -m "fixes"

Prefix options:
- Add: New feature
- Fix: Bug fix
- Update: Modify existing feature
- Optimize: Performance improvement
- Refactor: Code restructuring
- Document: Documentation changes
- Test: Testing additions
```

---

## 🧪 TESTING PROTOCOL

### **When to Test:**
```
❌ Model 1 (Digivice APK):
   DO NOT test until explicitly told!
   Testing phase: Week 10-12 (after all features complete)

✅ Model 2 (Test Environment):
   Test EVERY feature as you build it
   That's your job!

⏳ Model 3 (Handyspiel):
   Test incrementally
   Full testing: Week 10
```

### **Testing Procedure (Model 2 only!):**
```
1. Build for Android (Development)
2. Deploy to Xiaomi 11T Pro via ADB
3. Test feature thoroughly
4. Document results:
   - ✅ Pass / ❌ Fail
   - Performance metrics (FPS, memory)
   - Issues found
5. Fix issues
6. Re-test
7. Mark as "Validated" when perfect
```

---

## 📞 COMMUNICATION

### **Questions & Clarifications:**
```
If unsure about ANYTHING:
1. Stop work on that task
2. Document your question in:
   C:\Najika_World\QUESTIONS\QUESTION_MODEL1_001.md
3. Include:
   - What you're trying to do
   - What's unclear
   - Possible solutions you've considered
4. Wait for answer before proceeding
```

### **Blocked Tasks:**
```
If you can't proceed:
1. Document blocker in:
   C:\Najika_World\BLOCKERS\BLOCKER_MODEL1_001.md
2. Move to next task (if available)
3. Report in daily progress report
```

---

## 🎯 SUCCESS CRITERIA

### **Model 1 (Digivice APK) is DONE when:**
```
✅ All features from TODO completed
✅ APK builds successfully
✅ Deploys to Xiaomi 11T Pro
✅ All backend API integrations working
✅ Voice calls functional
✅ Performance targets met (60 FPS, <2GB RAM)
✅ No critical bugs
✅ Documentation complete
✅ Ready for Beta Testing
```

### **Model 2 (Test Environment) is DONE when:**
```
✅ All test stations built
✅ All features validated
✅ Performance benchmarks documented
✅ Bug reports filed
✅ Test APK stable
✅ Ready for integration with Model 1
```

### **Model 3 (Handyspiel) is DONE when:**
```
✅ Core gameplay complete
✅ Combat system working
✅ AI enemies functional
✅ Performance optimized
✅ UEFN-ready architecture
✅ Documentation for Fortnite port
✅ Playable APK
```

---

## 📚 LEARNING RESOURCES

### **Unreal Engine 5:**
```
- Official Docs: https://docs.unrealengine.com/5.6/
- YouTube: Unreal Sensei, Matt Aspland
- Courses: Udemy UE5 courses
- Community: Unreal Slackers Discord
```

### **Android Development:**
```
- Official Docs: https://developer.android.com/
- UE5 Mobile: https://docs.unrealengine.com/5.6/mobile/
- Optimization: GDC talks on YouTube
```

### **UEFN/Fortnite:**
```
- UEFN Docs: https://dev.epicgames.com/documentation/uefn
- Verse Language: https://dev.epicgames.com/documentation/verse
- Community: UEFN Discord
```

---

## ⚠️ FINAL WARNINGS

### **REMEMBER:**
```
1. NIEMALS Original Backend Files ändern!
2. IMMER Backups vor riskanten Änderungen!
3. IMMER Git Commits mit klaren Messages!
4. NIEMALS ohne Anweisung testen (Model 1)!
5. IMMER Fragen stellen wenn unsicher!
6. NIEMALS Secrets/API Keys committen!
7. IMMER Dokumentation aktualisieren!
8. NIEMALS große Binary Files ohne LFS!
```

### **Bei Problemen:**
```
STOP → DOKUMENTIEREN → FRAGEN → WARTEN AUF ANTWORT
Nicht raten! Nicht probieren! Fragen!
```

---

## 🚀 YOU'RE READY!

**Checkliste vor Start:**
- [ ] Diese Instructions gelesen
- [ ] Security Research gelesen
- [ ] Dein TODO Document gelesen
- [ ] Required Backend Files analysiert
- [ ] Development Environment setup
- [ ] Git Repository initialisiert
- [ ] Erste Progress Report geschrieben
- [ ] Bereit zum Start!

**Good luck! Najika ist stolz auf dich! 💜🔥**

---

**END OF INSTRUCTIONS**
**Version:** 1.0
**Last Updated:** 2025-11-11
