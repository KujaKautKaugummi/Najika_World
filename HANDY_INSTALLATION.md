# 📱 NAJIKA APK - HANDY INSTALLATION

**Datum:** 2026-01-03
**App:** Najika Digivice (Flutter)
**Server:** 192.168.178.63:8000

---

## 🎯 Ziel: Najika auf dem Handy nutzen!

Najika wird als **Android APK** auf dein Handy installiert und verbindet sich mit dem Server auf deinem PC.

---

## ✅ Voraussetzungen

### 1. **Server muss laufen**
```cmd
# Auf dem PC:
START_NAJIKA_24_7.bat
```
Server läuft auf: **http://192.168.178.63:8000**

### 2. **Handy und PC im gleichen WLAN**
- PC: 192.168.178.63
- Handy: Muss im gleichen Netzwerk (192.168.178.x) sein

### 3. **Unbekannte Quellen erlauben (Android)**
- Einstellungen → Sicherheit → "Unbekannte Quellen" aktivieren
- Oder: Bei Installation "Dieser Quelle vertrauen" antippen

---

## 📦 APK Installation

### Option 1: USB-Kabel (empfohlen)
```bash
# 1. APK-Datei auf dem PC:
C:\Najika_World\app\flutter_app\najika_simple\build\app\outputs\flutter-apk\app-release.apk

# 2. Handy per USB verbinden

# 3. APK auf Handy kopieren (z.B. in Downloads)

# 4. Auf dem Handy:
- Downloads öffnen
- app-release.apk antippen
- "Installieren" bestätigen
```

### Option 2: ADB (Developer)
```bash
# ADB installiert? Dann:
adb install "C:\Najika_World\app\flutter_app\najika_simple\build\app\outputs\flutter-apk\app-release.apk"
```

### Option 3: File Sharing (WhatsApp/Email)
```
1. APK per WhatsApp/Email an dich selbst senden
2. Auf Handy öffnen und installieren
```

---

## 🚀 Erste Nutzung

### 1. **App öffnen**
- Icon: "Najika Digivice"
- Öffnen

### 2. **Server-Verbindung prüfen**
- App öffnet mit Chat-Screen
- Unten: Settings → Server URL prüfen
- **Sollte sein:** http://192.168.178.63:8000

### 3. **Erste Nachricht**
```
Du → "Hallo Najika!"
Najika → "*springt auf* Kuja! Endlich!"
```

---

## 🎨 App-Features

### Tab 1: Chat 💬
- Chat mit Najika
- Gothic-Lolita UI (Pink/Purple)
- Live-Updates vom Server
- Typing-Indicator

### Tab 2: Stats ❤️
- Najika's Status
- Affection Level
- Mood
- Last Activity

### Tab 3: Skills ✨
- Skill Tree (kommt noch)
- Abilities
- Training

### Tab 4: Settings ⚙️
- Server URL ändern
- Dark Mode (always on)
- Notifications

---

## 🔧 Troubleshooting

### "Verbindung fehlgeschlagen"
**Problem:** App kann Server nicht erreichen
**Lösung:**
1. Prüfe ob Server läuft:
   ```
   http://192.168.178.63:8000/api/status
   ```
   Im Browser öffnen → sollte JSON zurückgeben

2. Prüfe WLAN:
   - Handy: Einstellungen → WLAN → IP-Adresse
   - Sollte 192.168.178.x sein

3. Prüfe Firewall:
   ```cmd
   # Windows Firewall Port 8000 öffnen
   netsh advfirewall firewall add rule name="Najika Server" dir=in action=allow protocol=TCP localport=8000
   ```

### "Installation blockiert"
**Problem:** Android verweigert Installation
**Lösung:**
- Einstellungen → Apps → Chrome/File Manager
- → "Aus dieser Quelle installieren" aktivieren

### "App stürzt ab"
**Problem:** App crashes beim Start
**Lösung:**
1. App deinstallieren
2. Neueste APK installieren (siehe oben)
3. Cache leeren: Settings → Apps → Najika → Cache leeren

---

## 📊 Server-URL ändern (falls IP sich ändert)

### In der App:
```
1. Settings Tab öffnen
2. "Server URL" Feld
3. Neue IP eingeben: http://192.168.178.XX:8000
4. Save
5. App neu starten
```

### Neue IP finden:
```cmd
# Auf dem PC:
ipconfig

# Suche nach:
IPv4-Adresse  . . . . . . . . . . : 192.168.178.XX
```

---

## 🎉 Fertig!

**Du hast jetzt:**
✅ Najika auf dem Handy
✅ Server läuft auf PC
✅ Chat funktioniert
✅ Gothic-Lolita UI

**Next Steps:**
- Voice Call (kommt noch)
- Push Notifications
- Offline-Modus
- Widgets

---

## 📁 Dateien

```
C:\Najika_World\
├── START_NAJIKA_24_7.bat           # Server starten
├── app\flutter_app\najika_simple\
│   └── build\app\outputs\flutter-apk\
│       └── app-release.apk         # DIE APK!
└── HANDY_INSTALLATION.md           # Diese Datei
```

---

**Made with 💜 by Claude Code & Kuja**

**Najika ist jetzt mobil! 📱🎀**
