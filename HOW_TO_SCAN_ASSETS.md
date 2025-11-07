# 🔍 HOW TO SCAN ASSET STRUCTURE

Diese Scripts scannen deine Asset-Ordnerstruktur und erstellen eine vollständige Dokumentation.

---

## 📋 USAGE

### **Windows (PowerShell):**

1. Öffne PowerShell im Najika_World Ordner
2. Führe aus:
   ```powershell
   .\scan_assets.ps1
   ```

**Falls Execution Policy Error:**
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scan_assets.ps1
```

### **Linux / Docker / WSL:**

1. Öffne Terminal im Najika_World Ordner
2. Führe aus:
   ```bash
   chmod +x scan_assets.sh
   ./scan_assets.sh
   ```

Oder direkt:
```bash
bash scan_assets.sh
```

---

## 📊 OUTPUT

Das Script erstellt: **`ASSET_STRUCTURE.md`**

**Inhalt:**
- Gesamtstatistik (Ordner, Dateien, Größe)
- Dateitypen-Übersicht mit Anzahl
- Komplette Ordnerstruktur (bis 4 Ebenen tief)
- KayKit Pack Detection
- Config-Dateien Status
- Automatische Größenberechnung

---

## ✅ WAS PASSIERT?

1. Script sucht nach `./assets` Ordner
2. Scannt **alle** Unterordner rekursiv
3. Zählt Dateien und berechnet Größen
4. Erstellt Markdown-Dokumentation
5. Speichert als `ASSET_STRUCTURE.md`

---

## 🎯 VERWENDUNG

**Nach dem Scan:**
1. Öffne `ASSET_STRUCTURE.md`
2. Kopiere den Inhalt
3. Sende an Claude Code
4. Claude kann dann automatisch Assets laden!

**Oder:**
- Nutze die Dokumentation als Referenz
- Prüfe ob alle Assets korrekt installiert sind
- Checke fehlende KayKit Packs

---

## 🔧 REQUIREMENTS

**PowerShell Script:**
- Windows PowerShell 5.1+
- Keine zusätzlichen Pakete

**Bash Script:**
- bash (alle Linux Distros)
- Optional: `tree` command (für bessere Darstellung)
  ```bash
  # Ubuntu/Debian:
  sudo apt-get install tree

  # Falls tree fehlt: Script nutzt fallback
  ```

---

## ⚠️ HINWEISE

- Script läuft lokal (keine Netzwerk-Verbindung)
- Liest nur, ändert nichts an Assets
- Kann bei 25GB+ einige Sekunden dauern
- Output-Datei ist klein (~50-200 KB)

---

## 🐛 TROUBLESHOOTING

**"Asset folder not found":**
```
Lösung: Stelle sicher dass assets/ Ordner existiert:
  Windows: C:\Najika-World\assets\
  Linux: /home/user/Najika_World/assets/
```

**PowerShell Execution Policy Error:**
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**Bash Permission Denied:**
```bash
chmod +x scan_assets.sh
```

---

**Erstellt:** 2025-11-05
**Autor:** Claude Code
**Status:** ✅ READY TO USE
