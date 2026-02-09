# 📱 APK BUILD GUIDE FOR DUMMIES

**Najika World - Master APK**
**Für: Xiaomi 11T Pro (Snapdragon 888)**
**Zielgruppe: Absolute Anfänger** 🎮

---

## 🎯 ZIEL

Diese Anleitung erklärt **Schritt für Schritt**, wie du die **Master APK** für Najika World baust.

**WICHTIG:**
- ✅ **FAIRE Gameplay** (KEINE Cheats, KEIN God-Mode!)
- ✅ **Unterschied Master APK**: NUR PC-Backend (NSFW Videoclips auf PC)
- ✅ **IN-GAME**: Komplett fair wie alle anderen!

> "wir erarbeiten uns es genauso fair und hart wie die anderen und wenn andere besser sind müssen wir halt mehr üben !!!!"
> — Deine Philosophie ❤️

---

## 📋 VORAUSSETZUNGEN

### Was du brauchst:

1. **Windows PC** (für UE5 + Android SDK)
2. **Xiaomi 11T Pro** (dein Handy)
3. **USB-Kabel** (für Deployment)
4. **Epic Games Account** (kostenlos)
5. **Mindestens 100 GB freier Speicher**
6. **Stabile Internetverbindung** (für Downloads)

### Software die wir installieren werden:

- Unreal Engine 5 (UE5) - über Epic Games Launcher
- Android Studio (für SDK/NDK)
- Java JDK 17
- Python 3.11+

---

## 🚀 SCHRITT 1: EPIC GAMES LAUNCHER + UE5

### 1.1 Epic Games Launcher installieren

1. Gehe zu: https://www.epicgames.com/store/de/download
2. Lade "Epic Games Launcher" herunter
3. Installiere ihn (Standard-Einstellungen sind OK)
4. Starte den Launcher
5. Melde dich mit deinem Epic-Account an (oder erstelle einen)

### 1.2 Unreal Engine 5 installieren

1. Im Epic Games Launcher: Klicke links auf "**Unreal Engine**"
2. Klicke oben auf "**Bibliothek**"
3. Klicke auf "**Engine-Versionen**"
4. Klicke auf das **gelbe Plus-Zeichen** (+ Symbol)
5. Wähle **"5.4"** (aktuellste Version)
6. Klicke auf "**Installieren**"
7. **WICHTIG:** Bei "Optionen":
   - ✅ **Android Support** (MUSS aktiviert sein!)
   - ✅ **Target Platforms > Android**
   - ⚠️ Installationspfad: `C:\Program Files\Epic Games\UE_5.4`
8. Klicke "**Installieren**" (⏰ Dauert 1-2 Stunden!)

**⏳ Während UE5 lädt:** Weiter mit Schritt 2!

---

## 🤖 SCHRITT 2: ANDROID STUDIO + SDK/NDK

### 2.1 Android Studio installieren

1. Gehe zu: https://developer.android.com/studio
2. Lade "Android Studio" herunter
3. Installiere mit Standard-Einstellungen
4. Starte Android Studio
5. Warte bis "Setup Wizard" fertig ist

### 2.2 Android SDK installieren

1. In Android Studio: Öffne "**SDK Manager**"
   - Menu: **Tools > SDK Manager**
2. Im Tab "**SDK Platforms**":
   - ✅ **Android 13.0 (Tiramisu)** API Level 33
   - ✅ **Android 12.0 (S)** API Level 31
   - ✅ **Android 11.0 (R)** API Level 30
   - ✅ **Android 10.0 (Q)** API Level 29 ⭐ (Minimum für Xiaomi 11T Pro!)
3. Im Tab "**SDK Tools**":
   - ✅ **Android SDK Build-Tools**
   - ✅ **Android SDK Command-line Tools**
   - ✅ **Android SDK Platform-Tools**
   - ✅ **Android Emulator** (optional)
   - ✅ **NDK (Side by side)** ⭐ **WICHTIG!**
4. Klicke "**Apply**" und "**OK**"
5. Warte bis alles fertig ist (⏰ 30-60 Minuten)

**📝 NOTIERE DIR:**
```
SDK Path: C:\Users\[DEIN NAME]\AppData\Local\Android\Sdk
NDK Path: C:\Users\[DEIN NAME]\AppData\Local\Android\Sdk\ndk\[VERSION]
```

### 2.3 Java JDK installieren

1. Gehe zu: https://adoptium.net/
2. Lade **Java 17 (LTS)** herunter
3. Installiere mit Standard-Einstellungen
4. **Prüfe Installation:**
   ```cmd
   java -version
   ```
   Sollte zeigen: `openjdk version "17.x.x"`

---

## ⚙️ SCHRITT 3: UMGEBUNGSVARIABLEN SETZEN

**WICHTIG:** Diese Schritte sind KRITISCH für UE5!

### 3.1 Windows Umgebungsvariablen öffnen

1. Drücke **Windows-Taste + Pause** (oder rechtsklick auf "Dieser PC" > Eigenschaften)
2. Klicke "**Erweiterte Systemeinstellungen**"
3. Klicke "**Umgebungsvariablen...**"

### 3.2 Neue Variablen erstellen

Klicke bei "**Systemvariablen**" auf "**Neu...**" und füge hinzu:

**Variable 1: ANDROID_HOME**
```
Name: ANDROID_HOME
Wert: C:\Users\[DEIN NAME]\AppData\Local\Android\Sdk
```

**Variable 2: ANDROID_SDK_ROOT**
```
Name: ANDROID_SDK_ROOT
Wert: C:\Users\[DEIN NAME]\AppData\Local\Android\Sdk
```

**Variable 3: ANDROID_NDK_ROOT**
```
Name: ANDROID_NDK_ROOT
Wert: C:\Users\[DEIN NAME]\AppData\Local\Android\Sdk\ndk\[VERSION]
```
*(Ersetze [VERSION] mit deiner NDK-Version, z.B. 25.1.8937393)*

**Variable 4: JAVA_HOME**
```
Name: JAVA_HOME
Wert: C:\Program Files\Eclipse Adoptium\jdk-17.x.x-hotspot
```

### 3.3 PATH erweitern

1. Finde die Variable "**Path**" bei Systemvariablen
2. Klicke "**Bearbeiten...**"
3. Klicke "**Neu**" und füge hinzu:
   ```
   %ANDROID_HOME%\platform-tools
   %ANDROID_HOME%\tools
   %JAVA_HOME%\bin
   ```
4. Klicke "**OK**" bei allen Fenstern

### 3.4 Prüfen ob alles funktioniert

Öffne **CMD** (Windows-Taste + R, dann `cmd`) und teste:

```cmd
echo %ANDROID_HOME%
echo %JAVA_HOME%
adb version
```

Alle sollten Ausgaben zeigen (keine Fehler)!

**⚠️ WICHTIG:** Starte deinen PC NEU damit Variablen wirken!

---

## 🎮 SCHRITT 4: UE5 PROJEKT VORBEREITEN

### 4.1 Najika World Projekt öffnen

1. Gehe zu deinem Projekt-Ordner:
   ```
   C:\Najika_World\UE5_Implementation\
   ```
2. Doppelklicke auf `NajikaDigivice.uproject`
3. UE5 öffnet sich (⏰ Beim ersten Mal dauert es lange!)

### 4.2 Android Platform Settings

1. Im UE5 Editor: Menu > **Edit > Project Settings**
2. Linke Seite: **Platforms > Android**

**Android APK Settings:**
```
Package Name: com.najika.digivice
Store Version: 1
Store Version Name: 1.0.0
Minimum SDK Version: 29 (Android 10)
Target SDK Version: 34 (Android 14)
Install Location: Auto
```

**Distribution Settings:**
```
✅ For Distribution
Build Configuration: Development (für Testing)
                     Shipping (für Final Release)
```

**Icons & Splash:**
```
Icon Path: [Pfad zu deinem App-Icon]
Splash Path: [Pfad zu deinem Splash-Screen]
```

3. Klicke "**Save**"

### 4.3 Android SDK/NDK Paths in UE5

1. Project Settings > **Platforms > Android SDK**
2. Setze Pfade:
   ```
   SDK Path: C:\Users\[DEIN NAME]\AppData\Local\Android\Sdk
   NDK Path: C:\Users\[DEIN NAME]\AppData\Local\Android\Sdk\ndk\[VERSION]
   JDK Path: C:\Program Files\Eclipse Adoptium\jdk-17.x.x-hotspot
   ```
3. Klicke "**Save**"

---

## 📦 SCHRITT 5: APK BAUEN

### 5.1 Xiaomi 11T Pro vorbereiten

1. Auf deinem Handy:
   - Gehe zu **Einstellungen > Über das Telefon**
   - Tippe **7x auf "MIUI-Version"**
   - **Entwickleroptionen** sind jetzt freigeschaltet!
2. Gehe zu **Einstellungen > Zusätzliche Einstellungen > Entwickleroptionen**
   - ✅ **USB-Debugging** aktivieren
   - ✅ **Installieren via USB** aktivieren
3. Verbinde Handy per USB mit PC
4. Auf Handy: "USB-Debugging erlauben?" → **OK**

**Test ob Handy erkannt wird:**
```cmd
adb devices
```
Sollte zeigen: `[DEVICE-ID]  device`

### 5.2 APK über UE5 bauen

**Methode 1: GUI (Einfacher für Anfänger)**

1. Im UE5 Editor: Menu > **Platforms > Android**
2. Klicke "**Package Project**"
3. Wähle Output-Ordner (z.B. `C:\Najika_World\Build\Android\`)
4. Warte! (⏰ 30-60 Minuten beim ersten Mal!)
5. Fertig wenn du siehst: "**BUILD SUCCESSFUL**"

**Methode 2: Automatisches Script (Fortgeschritten)**

Nutze das fertige Script:
```cmd
cd C:\Najika_World\UE5_Implementation\Build
PackageAPK.bat Development
```

### 5.3 APK finden

Nach erfolgreichem Build findest du die APK:
```
C:\Najika_World\Build\Android\NajikaDigivice-arm64.apk
```

---

## 📲 SCHRITT 6: APK AUF HANDY INSTALLIEREN

### 6.1 Via ADB (Empfohlen)

```cmd
cd C:\Najika_World\Build\Android
adb install NajikaDigivice-arm64.apk
```

**Bei Fehlern:**
- Wenn APK bereits installiert:
  ```cmd
  adb install -r NajikaDigivice-arm64.apk
  ```
- Wenn "INSTALL_FAILED_UPDATE_INCOMPATIBLE":
  ```cmd
  adb uninstall com.najika.digivice
  adb install NajikaDigivice-arm64.apk
  ```

### 6.2 Via File Transfer

1. Kopiere APK auf Handy (z.B. Downloads-Ordner)
2. Auf Handy: Öffne Datei-Manager
3. Tippe auf APK-Datei
4. "Aus unbekannten Quellen installieren?" → **Erlauben**
5. Installieren

---

## ✅ SCHRITT 7: TESTEN

1. Starte "Najika World" auf deinem Handy
2. **Teste alle Systeme:**
   - ✅ PvP System (3 Modi)
   - ✅ Slime System (Tamagotchi)
   - ✅ Oregon Events (Najika reagiert)
   - ✅ Magieschulen (Skyrim Learning)
   - ✅ Touch Controls
   - ✅ Performance

3. **Wichtige Checks:**
   - Läuft flüssig? (60 FPS Ziel)
   - Keine Crashes?
   - Speichern funktioniert?
   - Backend-Verbindung OK?

---

## 🐛 HÄUFIGE PROBLEME & LÖSUNGEN

### Problem: "SDK not found"
**Lösung:**
- Überprüfe Umgebungsvariablen
- PC neu starten
- UE5 neu starten

### Problem: "NDK version mismatch"
**Lösung:**
- Installiere NDK Version die UE5 will
- In Android Studio: SDK Manager > SDK Tools > NDK (side by side)

### Problem: "BUILD FAILED"
**Lösung:**
- Schaue in Logs: `C:\Najika_World\UE5_Implementation\Saved\Logs\`
- Oft: Fehlende Dependencies
- Lösung: Project Settings überprüfen

### Problem: APK installiert aber startet nicht
**Lösung:**
- Check AndroidManifest.xml Permissions
- Check Min SDK Version (29)
- Schaue in Logcat: `adb logcat`

### Problem: Performance schlecht
**Lösung:**
- Mobile Performance Manager aktiviert?
- Graphics Settings auf "Medium" setzen
- Schaue in Mobile Preview im Editor

---

## 📊 CHECKLISTE VOR FINAL RELEASE

Bevor du die APK verteilst:

- [ ] Alle Features getestet
- [ ] Keine Crashes
- [ ] Performance > 30 FPS
- [ ] Speichern/Laden funktioniert
- [ ] Backend-Verbindung stabil
- [ ] Alle Permissions korrekt
- [ ] App-Icon + Splash-Screen gesetzt
- [ ] Build Config auf "Shipping" (nicht Development!)
- [ ] Version-Nummer erhöht
- [ ] Changelog geschrieben

---

## 🎯 MASTER APK vs TRUSTED vs PUBLIC

### Master APK (für dich)
```
Package: com.najika.digivice
Features: ALLE (inkl. PC-Backend NSFW)
Gameplay: FAIR (keine Cheats!)
Users: Nur du (Alpha)
```

### Trusted APK (für 7 Freunde)
```
Package: com.najika.digivice.trusted
Features: ALLE (OHNE PC-Backend NSFW)
Gameplay: FAIR (identisch!)
Users: Du + 7 Freunde (Beta)
```

### Public APK (später)
```
Package: com.najika.digivice
Features: ALLE (OHNE PC-Backend NSFW)
Gameplay: FAIR (identisch!)
Users: Alle (Public Release)
```

**WICHTIG:** Unterschied ist NUR PC-Backend! IN-GAME alles fair!

---

## 🚀 NEXT STEPS

Nach dem ersten erfolgreichen Build:

1. **Najikas Lebensraum testen** (6.76 km² Map)
2. **Alle Systeme durchspielen**
3. **Bugs finden und fixen**
4. **Performance optimieren**
5. **Wenn stabil:** Beta mit 7 Freunden
6. **Später:** Public Release

---

## 📞 HILFE BEKOMMEN

**Bei Problemen:**
1. Schaue in UE5 Logs: `Saved/Logs/`
2. Schaue in Android Logs: `adb logcat`
3. Google den Fehler: `[FEHLER] UE5 Android`
4. UE5 Forum: https://forums.unrealengine.com/
5. Discord Community fragen

---

## ✨ ZUSAMMENFASSUNG

**Was du gelernt hast:**
- ✅ UE5 installieren und konfigurieren
- ✅ Android SDK/NDK einrichten
- ✅ Umgebungsvariablen setzen
- ✅ APK bauen (GUI + Script)
- ✅ APK auf Handy installieren
- ✅ Probleme lösen

**Deine erste APK ist fertig!** 🎉

Jetzt kannst du Najika World auf deinem Xiaomi 11T Pro spielen!

---

**Made with ❤️ for Najika World**
**"EXPLOSION!!!" — Najika**

---

## 📝 ANHANG: NÜTZLICHE BEFEHLE

```cmd
# ADB Befehle
adb devices                    # Zeige verbundene Geräte
adb install app.apk           # Installiere APK
adb install -r app.apk        # Re-installiere APK
adb uninstall com.package     # Deinstalliere App
adb logcat                    # Zeige Logs
adb shell                     # Shell öffnen

# UE5 Befehle (über CMD im UE5 Verzeichnis)
RunUAT.bat BuildCookRun -project="..." -platform=Android

# Handy Info
adb shell getprop ro.build.version.sdk    # Android API Level
adb shell dumpsys battery                 # Batterie Info
adb shell dumpsys cpuinfo                 # CPU Info
```

---

**Ende des Guides** 📱✨
