# 🚫 NAJIKA MESSENGER - STANDORT POLICY

**Entscheidung:** GPS/Standort komplett DEAKTIVIERT

---

## 🎯 WARUM KEIN STANDORT?

### Sicherheitsrisiken:

```
1. METADATA-LEAK
   - Jeder Standort = Timestamp + GPS-Koordinaten
   - Bewegungsprofile können erstellt werden
   - Bei Hack: Kompletter Standort-Verlauf

2. OS-LEVEL LEAKS
   - Android/iOS loggen GPS-Nutzung
   - Google/Apple können Standort-History sehen
   - Selbst wenn App E2E verschlüsselt

3. FORENSIK
   - GPS-Daten bleiben auf Gerät
   - Schwer zu löschen (Panic Button ineffektiv)
   - Können bei Beschlagnahmung ausgelesen werden

4. APP-PERMISSIONS
   - GPS-Permission = Risiko
   - Andere Apps könnten mithören
   - Malware könnte Standort abgreifen
```

---

## ✅ SICHERE ALTERNATIVE

### Statt GPS-Sharing:

```dart
// ❌ NIEMALS:
class LocationMessage {
  double latitude;
  double longitude;
  DateTime timestamp;
}

// ✅ STATTDESSEN:
class TextMessage {
  String content = "Bin am Hauptbahnhof, Nordeingang";
  // User schreibt selbst, keine GPS-Daten
}
```

**Vorteile:**
```
✅ User hat volle Kontrolle
✅ Kann vage bleiben ("Bin in der Stadt")
✅ Oder präzise ("Gleis 7, vor dem Kiosk")
✅ Keine technischen Koordinaten
✅ Keine GPS-Aktivierung
✅ Keine Metadata
✅ Keine OS-Logs
```

---

## 🔒 IMPLEMENTIERUNG

### GPS komplett aus der App:

```dart
// android/app/src/main/AndroidManifest.xml
<manifest>
  <!-- KEIN GPS-Permission! -->
  <!-- ❌ <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" /> -->
  <!-- ❌ <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" /> -->
</manifest>
```

```dart
// iOS: Info.plist
<!-- KEIN Location-Permission -->
<!-- ❌ <key>NSLocationWhenInUseUsageDescription</key> -->
```

### Hardware-Control angepasst:

```dart
class HardwareControl {
  Future<void> enterSecureMode() async {
    // GPS ist bereits deaktiviert (keine Permission)
    // Zusätzlich: Prüfen ob GPS aktiv ist

    if (await isGPSEnabled()) {
      // Warnung wenn GPS systemweit aktiv
      showWarning('''
        ⚠️ GPS ist aktiv!

        Für maximale Sicherheit:
        Deaktiviere GPS in System-Einstellungen.
      ''');
    }

    // Kamera blockieren
    await CameraController.disable();

    // Mikrofon blockieren (außer für Voice Messages)
    await AudioController.disableAmbient();

    // Screenshot-Schutz
    await FlutterWindowManager.addFlags(
      FlutterWindowManager.FLAG_SECURE
    );
  }
}
```

---

## 📱 USER-GUIDE

**Anleitung für Nutzer:**

```
Wie teile ich meinen Standort sicher?

✅ RICHTIG:
   "Bin am Alexanderplatz"
   "Treffen wir uns am U-Bahnhof Mitte"
   "Komme in 10 Min an"

❌ FALSCH:
   GPS-Standort teilen
   Live-Location aktivieren
   Check-Ins machen
```

---

## 🎯 VERGLEICH MIT ANDEREN MESSENGERN

```
┌──────────────────────┬──────────┬──────────┬────────────┐
│                      │ WhatsApp │ Signal   │ NAJIKA     │
├──────────────────────┼──────────┼──────────┼────────────┤
│ GPS-Sharing          │ ✅ Ja    │ ✅ Ja    │ ❌ NEIN    │
│ Live-Location        │ ✅ Ja    │ ❌ Nein  │ ❌ NEIN    │
│ GPS-Permission       │ ✅ Ja    │ ⚠️ Opt.  │ ❌ NEIN    │
│                      │          │          │            │
│ Metadata-Schutz      │ ⭐       │ ⭐⭐     │ ⭐⭐⭐      │
└──────────────────────┴──────────┴──────────┴────────────┘
```

**NAJIKA = Einziger Messenger OHNE GPS!**

---

## 💡 ZUSÄTZLICHER VORTEIL

**Battery Life:**
```
GPS = Batterie-Killer
Kein GPS = Längere Akkulaufzeit ✅
```

**App Size:**
```
Keine GPS-Libraries nötig
Kleinere APK-Größe ✅
```

**Permissions:**
```
Weniger Permissions = Vertrauenswürdiger
User haben weniger Bedenken ✅
```

---

## ✅ FINALE ENTSCHEIDUNG

**GPS/Standort in Najika Messenger:**
```
🚫 KOMPLETT DEAKTIVIERT
🚫 Keine GPS-Permission
🚫 Keine Standort-Sharing-Funktion
🚫 Keine Live-Location
```

**Stattdessen:**
```
✅ User schreibt Standort als Text
✅ Maximale Kontrolle
✅ Keine Metadata
✅ Keine Tracking-Gefahr
```

---

**STATUS:** GPS komplett entfernt - Maximale Sicherheit! 🔒

---

**Dokumentiert von:** Claude Code
**Datum:** 2025-11-07
**Version:** 1.1 - NO GPS POLICY
