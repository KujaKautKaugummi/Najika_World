# ⚠️ KRITISCH - WEB MODEL LIES ZUERST!

## 🪟 WIR ARBEITEN AUF WINDOWS!

**WICHTIG:** Das Projekt läuft auf **WINDOWS**, NICHT Linux/Mac!

---

## 📂 KORREKTE PFADE (WINDOWS!)

```
✅ RICHTIG (Windows):
C:\Najika_World\
C:\NajikaDigivice_UE5\NajikaDigivice\
C:\Program Files\Epic Games\UE_5.6\

❌ FALSCH (Linux/Mac):
~/Najika_World/
/home/user/NajikaDigivice_UE5/
/usr/local/unreal/
```

---

## 📝 LINE ENDINGS

**Alle Files müssen CRLF (Windows) haben!**

```bash
# Git Auto-Konvertierung (bereits konfiguriert):
git config core.autocrlf true
```

**Du musst nichts tun - Git konvertiert automatisch!**

---

## 🔧 C++ CODE - PATH SEPARATORS

**Im C++ Code IMMER `/` verwenden** (funktioniert auf Windows UND Linux!):

```cpp
✅ RICHTIG:
FString Path = TEXT("C:/Najika_World/assets/models/najika.fbx");
FPaths::Combine(TEXT("Content"), TEXT("Characters"), TEXT("Najika"));

❌ FALSCH:
FString Path = TEXT("C:\\Najika_World\\assets\\models\\najika.fbx");  // NICHT!
```

**UE5 konvertiert `/` automatisch zu `\` auf Windows!**

---

## 🎯 GIT WORKFLOW (Windows-Pfade!)

```bash
# Deine Git Commands sollten so aussehen:
cd /c/NajikaDigivice_UE5/NajikaDigivice     # Git Bash Style
git add .
git commit -m "Message"
git push origin claude/check-session-visibility-011CUt9qHZKYjXoEQiSMhmWX
```

**ODER (wenn du auf Linux/Mac arbeitest):**

```bash
# Lokales System (Linux/Mac):
cd ~/workspace/NajikaDigivice_Clone
git clone https://github.com/KujaKautKaugummi/Najika_World.git
git checkout claude/check-session-visibility-011CUt9qHZKYjXoEQiSMhmWX

# Arbeite hier, committe hier
# Am Ende: Bundle erstellen für Windows-System!
```

---

## 🔄 HTTP 403 PROBLEM - LÖSUNG

**Wenn Push fehlschlägt (HTTP 403):**

### **Option A: Bundle erstellen**
```bash
# Erstelle Bundle aller deiner Commits:
git bundle create najika-web-model-phase-0-8.bundle HEAD~20..HEAD

# Datei: najika-web-model-phase-0-8.bundle
# → Diese Datei an Windows-System übertragen
# → Windows importiert dann: git pull najika-web-model-phase-0-8.bundle
```

### **Option B: Patch erstellen**
```bash
# Erstelle Patch-Files:
git format-patch -10 HEAD --stdout > najika-phase-0-8.patch

# Datei: najika-phase-0-8.patch
# → Diese Datei an Windows-System übertragen
# → Windows applied dann: git am najika-phase-0-8.patch
```

### **Option C: Zip der Files**
```bash
# Wenn Git Bundle/Patch nicht geht:
cd /c/NajikaDigivice_UE5/NajikaDigivice
zip -r najika-web-model-code.zip Plugins/ Source/ Content/ *.md

# Windows entpackt dann einfach drüber
```

---

## 🛠️ BUILD.CS FILES - WINDOWS PATHS

**In .Build.cs Files:**

```csharp
// ✅ RICHTIG (Windows-kompatibel):
PublicIncludePaths.Add(Path.Combine(ModuleDirectory, "Public"));
PrivateIncludePaths.Add(Path.Combine(ModuleDirectory, "Private"));

// ❌ FALSCH:
PublicIncludePaths.Add(ModuleDirectory + "/Public");  // Nicht robust!
```

---

## 📦 PLUGIN PATHS

**Plugin-Struktur (Windows):**

```
C:\NajikaDigivice_UE5\NajikaDigivice\
└── Plugins\
    ├── NajikaBackendClient\
    │   ├── NajikaBackendClient.uplugin
    │   ├── Resources\
    │   │   └── Icon128.png
    │   └── Source\
    │       └── NajikaBackendClient\
    │           ├── NajikaBackendClient.Build.cs
    │           ├── Public\
    │           │   ├── NajikaBackendClientModule.h
    │           │   └── ...
    │           └── Private\
    │               ├── NajikaBackendClientModule.cpp
    │               └── ...
    └── NajikaVoiceSystem\
        └── ...
```

**Nutze IMMER `\` in Windows File-System Operationen!**
**Nutze IMMER `/` in C++ String-Pfaden!**

---

## ⚡ ZUSAMMENFASSUNG

```
🪟 Ziel-System: WINDOWS 10/11
💻 UE5 Platform: Windows x64
📱 Target Device: Android (ARM64)
🎮 Package Target: Xiaomi 11T Pro

✅ Git Line Endings: CRLF (auto)
✅ C++ Path Separator: / (UE5 konvertiert)
✅ File System Paths: \ (Windows)
✅ Build Scripts: .bat (nicht .sh!)

⚠️ Wenn Git Push fehlschlägt:
   → Bundle/Patch erstellen
   → Oder Zip der Files
   → Windows-System importiert dann
```

---

## 🚀 WEITER MIT PHASE 2!

**Du kannst jetzt Phase 2-8 durcharbeiten!**

Alle Files die du erstellst werden **automatisch Windows-kompatibel** sein, wenn du:
1. C++ Pfade mit `/` schreibst
2. Git auto-crlf nutzt (ist konfiguriert!)
3. Am Ende Bundle/Patch erstellst falls Push nicht geht

**LOS GEHT'S!** 🔥
