# PHASE 1: UNREAL ENGINE 5 INSTALLATION - WINDOWS
**Model 1 - Digivice APK**
**Datum:** 2025-11-11
**System:** Windows PC
**Ziel:** UE5.6 + Android Development Setup

---

## 🎯 PHASE 1 ÜBERSICHT

### **Was wird installiert:**
```
✅ Epic Games Launcher
✅ Unreal Engine 5.6 (neueste Version)
✅ Visual Studio 2022 Community Edition
✅ Android SDK + NDK
✅ Git + Git LFS
✅ Android Studio (optional, für Debugging)
```

### **Geschätzte Dauer:** 2-4 Stunden
### **Benötigter Speicherplatz:** ~150 GB

---

## 📋 SCHRITT-FÜR-SCHRITT INSTALLATION

### **SCHRITT 1: EPIC GAMES LAUNCHER**

#### 1.1 Download Epic Games Launcher
```
URL: https://www.epicgames.com/store/download
```

1. Öffne den Link im Browser
2. Klicke auf "Download" (Epic Games Launcher für Windows)
3. Führe `EpicInstaller-xxx.msi` aus
4. Folge dem Installationsassistenten
5. **Installationspfad:** `C:\Program Files\Epic Games\Launcher`

#### 1.2 Epic Games Account
1. Öffne Epic Games Launcher
2. Melde dich an (oder erstelle Account)
3. Verifiziere deine E-Mail

---

### **SCHRITT 2: VISUAL STUDIO 2022**

#### 2.1 Download Visual Studio 2022 Community
```
URL: https://visualstudio.microsoft.com/de/downloads/
```

1. Klicke auf "Community Edition" → "Kostenloser Download"
2. Führe `VisualStudioSetup.exe` aus

#### 2.2 Workload-Auswahl (WICHTIG!)
**Im Visual Studio Installer DIESE Workloads auswählen:**

✅ **Desktop-Entwicklung mit C++**
  - MSVC v143 - VS 2022 C++ x64/x86 build tools
  - Windows 10/11 SDK
  - C++ ATL for latest build tools
  - C++ MFC for latest build tools

✅ **Mobile-Entwicklung mit C++** (für Android!)
  - Android Game Development Extension

✅ **Optionale Komponenten:**
  - Git für Windows
  - GitHub Extension für Visual Studio

#### 2.3 Installation starten
1. Klicke auf "Installieren"
2. **Dauer:** 30-60 Minuten
3. **Speicherplatz:** ~20 GB
4. Nach Installation: **Neustart empfohlen**

---

### **SCHRITT 3: ANDROID SDK + NDK**

#### 3.1 Option A: Via Unreal Engine (EMPFOHLEN!)
**UE5 kann Android SDK/NDK automatisch installieren:**
1. Warte bis Schritt 4 (UE5 Installation)
2. UE5 installiert Android SDK/NDK beim ersten Android-Build
3. Pfad: `C:\Users\[Username]\AppData\Local\Android\Sdk`

#### 3.2 Option B: Manuell via Android Studio
```
URL: https://developer.android.com/studio
```

1. Download Android Studio
2. Installiere Android Studio
3. Öffne Android Studio → SDK Manager
4. Installiere:
   - Android SDK Platform 34 (Android 14)
   - Android SDK Build-Tools 34.0.0
   - Android NDK (r25c)
   - Android SDK Command-line Tools

5. **Umgebungsvariable setzen:**
   - Öffne: Systemsteuerung → System → Erweiterte Systemeinstellungen → Umgebungsvariablen
   - Neue Variable: `ANDROID_HOME`
   - Wert: `C:\Users\[Username]\AppData\Local\Android\Sdk`

---

### **SCHRITT 4: UNREAL ENGINE 5.6**

#### 4.1 UE5 Installation starten
1. Öffne **Epic Games Launcher**
2. Navigiere zu: **Unreal Engine** (linke Seite)
3. Klicke auf: **Bibliothek** (oben)
4. Klicke auf: **+ Engine hinzufügen** (rechts oben)
5. Wähle: **Version 5.6** (oder neueste verfügbare Version)

#### 4.2 Komponenten auswählen
**WICHTIG! Folgende Komponenten MÜSSEN ausgewählt werden:**

✅ **Core Components:**
  - Unreal Engine Core Files
  - Starter Content (optional, kann übersprungen werden)

✅ **Target Platforms:**
  - Android
  - Android (ASTC)
  - Android (ETC2)

✅ **Additional Components:**
  - Engine Source (EMPFOHLEN für C++ Development)
  - Editor Symbols for debugging (optional)

❌ **NICHT benötigt:**
  - iOS Support
  - Mac Support
  - Linux Support
  - PlayStation Support
  - Xbox Support
  - Switch Support

#### 4.3 Installation starten
1. **Installationspfad:** `C:\Program Files\Epic Games\UE_5.6`
2. Klicke auf "Installieren"
3. **Dauer:** 1-3 Stunden (abhängig von Internet-Geschwindigkeit)
4. **Speicherplatz:** ~80-100 GB

#### 4.4 Warten auf Installation
- Epic Games Launcher zeigt Fortschritt
- Bei Problemen: Pause → Resume hilft oft
- **Nicht abbrechen!** Installation kann nicht fortgesetzt werden

---

### **SCHRITT 5: GIT + GIT LFS**

#### 5.1 Git für Windows installieren
```
URL: https://git-scm.com/download/win
```

1. Download "Git for Windows"
2. Führe Installer aus
3. **Wichtige Optionen:**
   - Editor: Visual Studio Code (oder deine Wahl)
   - PATH: "Git from command line and also from 3rd-party software"
   - Line ending: "Checkout Windows-style, commit Unix-style"
   - Terminal: "Use Windows' default console window"

4. Installation abschließen

#### 5.2 Git LFS installieren
```
URL: https://git-lfs.com/
```

1. Download Git LFS für Windows
2. Führe Installer aus
3. Nach Installation in CMD/PowerShell:
   ```
   git lfs install
   ```

#### 5.3 Git konfigurieren
Öffne **PowerShell** oder **CMD** und führe aus:
```bash
git config --global user.name "Dein Name"
git config --global user.email "deine@email.com"
```

---

### **SCHRITT 6: VERIFICATION (Alles prüfen!)**

#### 6.1 Visual Studio testen
1. Öffne Visual Studio 2022
2. Create new project → C++ Console App
3. Build & Run
4. ✅ Wenn erfolgreich: C++ Build funktioniert!

#### 6.2 UE5 testen
1. Öffne Epic Games Launcher
2. Starte Unreal Engine 5.6
3. Create New Project:
   - Template: Blank
   - Project Type: C++
   - Target Platform: Mobile
   - Quality Preset: Scalable
   - Project Name: "TestProject"
   - Location: `C:\Temp\TestProject`
4. Create Project
5. ✅ Wenn Editor öffnet: UE5 funktioniert!
6. Schließe Editor und lösche TestProject

#### 6.3 Git testen
Öffne PowerShell und führe aus:
```bash
git --version
git lfs version
```
✅ Beide Commands sollten Versionen ausgeben

#### 6.4 Android SDK testen (falls manuell installiert)
```bash
echo %ANDROID_HOME%
dir "%ANDROID_HOME%"
```
✅ Sollte SDK-Pfad und Dateien anzeigen

---

## 🚀 SCHRITT 7: NAJIKA DIGIVICE PROJEKT ERSTELLEN

### **7.1 Projekt-Ordner vorbereiten**
```bash
# Öffne PowerShell und führe aus:
cd C:\
mkdir NajikaDigivice_UE5
cd NajikaDigivice_UE5
```

### **7.2 UE5-Projekt erstellen**

#### Option A: Via Epic Games Launcher (EMPFOHLEN)
1. Epic Games Launcher öffnen
2. Unreal Engine 5.6 starten
3. **New Project:**
   - Games → Blank
   - Blueprint oder C++: **C++** (WICHTIG!)
   - Target Platform: **Mobile**
   - Quality Preset: **Scalable**
   - Project Name: `NajikaDigivice`
   - Project Location: `C:\NajikaDigivice_UE5`
   - With Starter Content: **No** (wir haben eigene Assets!)

4. **Create Project**
5. Warte auf Projekt-Generierung (5-10 Minuten)
6. Editor öffnet sich automatisch

#### Option B: Via Command Line
```bash
cd "C:\Program Files\Epic Games\UE_5.6\Engine\Binaries\Win64"
UnrealEditor.exe -projectcreate -project="C:\NajikaDigivice_UE5\NajikaDigivice.uproject" -template="TP_Blank" -targetplatform=Mobile
```

### **7.3 Android-Konfiguration**

1. Im UE5 Editor: **Edit** → **Project Settings**

2. **Platforms → Android:**
   ```
   Package Name:      com.najika.digivice
   Minimum SDK:       29 (Android 10)
   Target SDK:        34 (Android 14)
   Orientation:       Landscape (oder Portrait - deine Wahl!)

   Android Package Options:
   ✅ Enable Vulkan Desktop Support
   ✅ Enable Vulkan Mobile Support
   ✅ Support OpenGL ES 3.1
   ✅ Package for ARM64 (modern devices)
   ❌ Package for x86 (nicht benötigt)
   ```

3. **Rendering:**
   ```
   Mobile HDR:                    ✅ Enabled
   Mobile MSAA:                   4x
   Dynamic Lighting:              ✅ Enabled
   Mobile Shaders:                ES 3.1 + Vulkan
   ```

4. **Scalability:**
   ```
   Quality Levels:                Low, Medium, High, Epic
   Default Quality Level:         High (Snapdragon 888!)
   Enable Adaptive Performance:   ✅ Yes
   ```

5. **Klicke:** "Set as Default" → "Apply" → "Save"

---

### **7.4 Git Repository initialisieren**

```bash
# In PowerShell (im Projekt-Ordner):
cd C:\NajikaDigivice_UE5

# Git initialisieren
git init

# Git LFS Setup
git lfs install
git lfs track "*.uasset"
git lfs track "*.umap"
git lfs track "*.ubulk"
git lfs track "*.uexp"
git lfs track "*.fbx"
git lfs track "*.png"
git lfs track "*.jpg"
git lfs track "*.tga"
git lfs track "*.wav"
git lfs track "*.mp3"

# .gitignore herunterladen
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/github/gitignore/main/UnrealEngine.gitignore" -OutFile ".gitignore"

# Erste Commit
git add .
git commit -m "Initial UE5 project setup - NajikaDigivice"
```

### **7.5 (Optional) GitHub Repository erstellen**
```bash
# GitHub CLI (falls installiert):
gh repo create NajikaDigivice_UE5 --private

# Remote hinzufügen:
git remote add origin https://github.com/[USERNAME]/NajikaDigivice_UE5.git
git branch -M main
git push -u origin main
```

---

## ✅ PHASE 1 ABSCHLUSS-CHECKLISTE

### **Software installiert:**
- [ ] Epic Games Launcher installiert
- [ ] Visual Studio 2022 installiert (mit C++ Workload)
- [ ] Unreal Engine 5.6 installiert
- [ ] Android SDK/NDK installiert (oder via UE5)
- [ ] Git + Git LFS installiert

### **Projekt erstellt:**
- [ ] NajikaDigivice UE5-Projekt erstellt
- [ ] Android-Konfiguration abgeschlossen
- [ ] Mobile Rendering konfiguriert
- [ ] Scalability-Einstellungen gesetzt
- [ ] Git Repository initialisiert
- [ ] Erste Commit gemacht

### **Verification:**
- [ ] Visual Studio kann C++ kompilieren
- [ ] UE5 Editor startet ohne Fehler
- [ ] Projekt lädt erfolgreich
- [ ] Git funktioniert (git --version)
- [ ] Git LFS funktioniert (git lfs version)

---

## 🎉 PHASE 1 COMPLETE!

Wenn alle Checkboxen ✅ sind, ist **Phase 1 abgeschlossen!**

**Nächster Schritt:** Phase 2 - Core Systems (Character, World, Camera)

---

## 📝 TROUBLESHOOTING

### **Problem: UE5 Installation schlägt fehl**
**Lösung:**
1. Pause → Resume in Epic Launcher
2. Prüfe Internetverbindung
3. Deaktiviere Antivirus temporär
4. Genug Speicherplatz? (100GB frei!)

### **Problem: Android SDK nicht gefunden**
**Lösung:**
1. Prüfe `ANDROID_HOME` Umgebungsvariable
2. UE5: Edit → Project Settings → Platforms → Android SDK → Auto-detect
3. Oder: Install via Android Studio

### **Problem: Visual Studio kann nicht kompilieren**
**Lösung:**
1. Prüfe ob C++ Workload installiert ist
2. Visual Studio Installer → Modify → Desktop Development with C++
3. Neustart nach Installation

### **Problem: Git LFS funktioniert nicht**
**Lösung:**
```bash
git lfs install --force
git lfs pull
```

### **Problem: UE5 Editor stürzt beim Start ab**
**Lösung:**
1. Prüfe Grafikkarten-Treiber (aktuellste Version!)
2. Prüfe Windows Updates
3. DirectX 12 installiert?
4. Projekt in "Safe Mode" öffnen (rechtsklick .uproject → "Launch in Safe Mode")

---

## 📞 SUPPORT

Bei Problemen:
1. Dokumentiere Problem in: `C:\Najika_World\ISSUES\ISSUE_PHASE1_001.md`
2. Include:
   - Fehlermeldung (Screenshot!)
   - Was du getan hast
   - Was du erwartet hast
   - Was tatsächlich passiert ist

---

**GOOD LUCK! Phase 1 Installation! 🔥**

**Geschätzte Zeit:** 2-4 Stunden
**Nach Abschluss:** Erstelle Progress Report in `C:\Najika_World\PROGRESS_REPORTS\`
