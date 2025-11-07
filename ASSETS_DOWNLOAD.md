# 🎨 NAJIKA WORLD - ASSETS DOWNLOAD

**Asset Size:** ~25GB
**Status:** NICHT in GitHub Repository (zu groß!)

---

## 📥 WIE ASSETS INSTALLIEREN?

### **Schritt 1: Assets herunterladen**

**OPTION A: Von KayKit (Offiziell)**
1. Gehe zu https://kaylousberg.itch.io/
2. Lade folgende Packs herunter (alle FREE):
   - KayKit Dungeon Remastered 1.1
   - KayKit Skeletons 1.0
   - KayKit Adventurers 1.0
   - KayKit Furniture Bits 1.0
   - KayKit Restaurant Bits 1.0
   - KayKit Halloween Bits 1.0
   - KayKit Forest Nature Pack 1.0
   - KayKit Platformer Pack 1.0

**OPTION B: Von Kuja's Backup (Privat)**
- Frag Kuja nach Zugriff auf C:\NajikaCore\assets Backup
- Oder Google Drive / Dropbox Link (wenn vorhanden)

---

### **Schritt 2: Assets extrahieren**

**Windows:**
```bash
# Kopiere alle Assets nach:
C:\Najika-World\assets\

# Struktur sollte sein:
C:\Najika-World\assets\
├── KayKit_DungeonRemastered_1.1_FREE\
├── KayKit_Skeletons_1.0_FREE\
├── KayKit_Adventurers_1.0_FREE\
├── KayKit_FurnitureBits_1.0_FREE\
├── ... (weitere Packs)
└── room_config_detailed.json
```

**Linux (Docker/Claude Code):**
```bash
# Kopiere Assets nach:
/home/user/Najika_World/assets/

# Oder mounte Windows-Ordner:
ln -s /mnt/c/Najika-World/assets /home/user/Najika_World/assets
```

---

### **Schritt 3: Verification**

Checke ob Assets korrekt installiert:

```bash
# Windows (PowerShell)
dir C:\Najika-World\assets

# Linux
ls -lh /home/user/Najika_World/assets
```

**Expected Output:**
- 8+ KayKit Ordner
- room_config_detailed.json
- Total Size: ~25GB

---

## 🔧 TROUBLESHOOTING

### Problem: "Skeleton_Mage.glb nicht gefunden"
**Lösung:**
```
Assets müssen in dieser Struktur sein:
assets/
  KayKit_Skeletons_1.0_FREE/
    KayKit_Skeletons_1.0_FREE/
      characters/
        gltf/
          Skeleton_Mage.glb  ← HIER!
```

### Problem: "room_config_detailed.json fehlt"
**Lösung:**
```bash
# Datei wird automatisch generiert beim ersten Start
# Oder manuell erstellen (siehe BEKANNTE_FEHLER_FIXEN.md)
```

---

## 📊 WARUM NICHT IN GITHUB?

**GitHub Limits:**
- Max File Size: 100MB
- Recommended Repo Size: <1GB
- Najika Assets: ~25GB!

**Lösung:**
- Code = GitHub (klein, versioniert)
- Assets = Lokal (groß, statisch)
- Developer lädt Assets einmal separat

---

## 🔗 WEITERE INFOS

- **Asset-Fehler beheben:** Siehe `BEKANNTE_FEHLER_FIXEN.md`
- **KayKit Lizenz:** CC0 (komplett frei verwendbar!)
- **Najika Discord:** [Link falls vorhanden]

---

**Erstellt:** 2025-11-05
**Autor:** Claude Code
**Status:** ✅ AKTUELL
