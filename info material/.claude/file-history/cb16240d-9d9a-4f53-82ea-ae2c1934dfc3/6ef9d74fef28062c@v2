# 🔧 BEKANNTE FEHLER - FÜR OPUS ZUM FIXEN
**Stand:** 2025-10-27
**Status:** Basis muss clean sein vor Opus-Übernahme!

---

## 🚨 KRITISCHE FEHLER (SOFORT FIXEN!)

### **1. Skeleton_Mage Model lädt nicht**
**Fehler:**
```
Scene3D: failed to load Skeleton_Mage model
```

**Ursache:**
- Code in `3d_scene.js:755` sucht:
  `/assets/KayKit_Skeletons_1.0_FREE/KayKit_Skeletons_1.0_FREE/characters/gltf/Skeleton_Mage.glb`
- **ABER:** Ordner existiert nicht in `/c/Najika/assets`!

**Assets liegen auf Desktop:**
- `C:\Users\0KKK0\Desktop\modelle\KayKit_Skeletons_1.0_FREE\`

**Lösung:**
```bash
# Option A: Assets kopieren
cp -r "C:/Users/0KKK0/Desktop/modelle/KayKit_Skeletons_1.0_FREE" /c/Najika/assets/

# Option B: Symlink erstellen
cd /c/Najika/assets
ln -s "C:/Users/0KKK0/Desktop/modelle/KayKit_Skeletons_1.0_FREE" .
```

---

### **2. Room Config nicht gefunden**
**Fehler:**
```
ℹ️ No room config found, using defaults
⚠️ Room "Wohnzimmer" not found in config
⚠️ Room "Badezimmer" not found in config
```

**Ursache:**
- `kaykit_loader.js` sucht nach `room_config_detailed.json`
- Datei **fehlt komplett** oder liegt am falschen Ort

**Suche Config:**
```bash
find /c -name "room_config*" 2>/dev/null
```

**Wenn nicht gefunden → Erstellen:**
Location: `/c/Najika/assets/room_config_detailed.json`

**Minimal-Config für Start:**
```json
{
  "Wohnzimmer": {
    "floor": "floor_tile_large.glb",
    "wall": "wall.glb",
    "span": 10,
    "wallHeight": 3,
    "palette": {
      "primary": "#8B4513",
      "secondary": "#D2691E",
      "accent": "#FFD700"
    },
    "props": [
      {
        "model": "torch.glb",
        "position": [4, 1.5, 4],
        "rotation": [0, 0, 0],
        "scale": [1, 1, 1]
      }
    ],
    "spawn": [0, 0, 0]
  },
  "Badezimmer": {
    "floor": "floor_tile_large.glb",
    "wall": "wall.glb",
    "span": 8,
    "wallHeight": 3,
    "palette": {
      "primary": "#4682B4",
      "secondary": "#87CEEB",
      "accent": "#FFFFFF"
    },
    "props": [],
    "spawn": [0, 0, 0]
  },
  "Schlafzimmer": {
    "floor": "floor_tile_large.glb",
    "wall": "wall.glb",
    "span": 10,
    "wallHeight": 3,
    "palette": {
      "primary": "#2F4F4F",
      "secondary": "#696969",
      "accent": "#FFB6C1"
    },
    "props": [],
    "spawn": [0, 0, 0]
  },
  "Küche": {
    "floor": "floor_tile_large.glb",
    "wall": "wall.glb",
    "span": 10,
    "wallHeight": 3,
    "palette": {
      "primary": "#F5DEB3",
      "secondary": "#DEB887",
      "accent": "#CD853F"
    },
    "props": [],
    "spawn": [0, 0, 0]
  },
  "Garten": {
    "floor": "floor_tile_large.glb",
    "wall": "wall.glb",
    "span": 15,
    "wallHeight": 3,
    "palette": {
      "primary": "#228B22",
      "secondary": "#32CD32",
      "accent": "#FFD700"
    },
    "props": [],
    "spawn": [0, 0, 0]
  },
  "Musikraum": {
    "floor": "floor_tile_large.glb",
    "wall": "wall.glb",
    "span": 10,
    "wallHeight": 3,
    "palette": {
      "primary": "#4B0082",
      "secondary": "#8A2BE2",
      "accent": "#FFD700"
    },
    "props": [],
    "spawn": [0, 0, 0]
  },
  "Medizin": {
    "floor": "floor_tile_large.glb",
    "wall": "wall.glb",
    "span": 8,
    "wallHeight": 3,
    "palette": {
      "primary": "#FFFFFF",
      "secondary": "#F0F0F0",
      "accent": "#FF0000"
    },
    "props": [],
    "spawn": [0, 0, 0]
  },
  "Terminal": {
    "floor": "floor_tile_large.glb",
    "wall": "wall.glb",
    "span": 10,
    "wallHeight": 3,
    "palette": {
      "primary": "#000000",
      "secondary": "#1E1E1E",
      "accent": "#00FF00"
    },
    "props": [],
    "spawn": [0, 0, 0]
  },
  "Studieren & Crafting": {
    "floor": "floor_tile_large.glb",
    "wall": "wall.glb",
    "span": 12,
    "wallHeight": 3,
    "palette": {
      "primary": "#8B4513",
      "secondary": "#A0522D",
      "accent": "#FFD700"
    },
    "props": [],
    "spawn": [0, 0, 0]
  },
  "Trainingszimmer": {
    "floor": "floor_tile_large.glb",
    "wall": "wall.glb",
    "span": 15,
    "wallHeight": 3,
    "palette": {
      "primary": "#696969",
      "secondary": "#808080",
      "accent": "#FF4500"
    },
    "props": [],
    "spawn": [0, 0, 0]
  },
  "Kampfarena": {
    "floor": "floor_tile_large.glb",
    "wall": "wall.glb",
    "span": 20,
    "wallHeight": 5,
    "palette": {
      "primary": "#8B0000",
      "secondary": "#B22222",
      "accent": "#FFD700"
    },
    "props": [],
    "spawn": [0, 0, 0]
  },
  "Schwarze Mühle – Keller": {
    "floor": "floor_tile_large.glb",
    "wall": "wall.glb",
    "span": 15,
    "wallHeight": 3,
    "palette": {
      "primary": "#1C1C1C",
      "secondary": "#2F4F4F",
      "accent": "#8B0000"
    },
    "props": [],
    "spawn": [0, 0, 0]
  }
}
```

---

### **3. CSS Selektor-Fehler**
**Fehler:**
```
Regelsatz wegen ungültigem Selektor ignoriert. chat.css:249
Regelsatz wegen ungültigem Selektor ignoriert. code_editor.css:361
```

**Ursache:**
- Ungültige CSS-Selektoren in `chat.css:249` und `code_editor.css:361`

**Lösung:**
1. Öffne `chat.css` Zeile 249
2. Öffne `code_editor.css` Zeile 361
3. Prüfe Selektoren (z.B. `::` statt `:`, fehlende Klammern)
4. Korrigiere oder entferne

---

## ⚠️ WICHTIGE PUNKTE

### **Assets-Struktur muss stimmen:**
```
C:\Najika\
  assets\
    KayKit_Skeletons_1.0_FREE\
      KayKit_Skeletons_1.0_FREE\
        characters\
          gltf\
            Skeleton_Mage.glb  ← MUSS HIER SEIN!
    room_config_detailed.json  ← MUSS HIER SEIN!
    models\
    sounds\
    textures\
```

### **Wo Assets liegen (Desktop):**
```
C:\Users\0KKK0\Desktop\modelle\
  KayKit_Skeletons_1.0_FREE\
  KayKit_DungeonRemastered_1.1_FREE\
  KayKit_Adventurers_1.0_FREE\
```

---

## 📋 FIX-CHECKLIST FÜR OPUS

- [ ] **1. Assets kopieren/linken**
  - KayKit Skeletons → `/c/Najika/assets/`
  - Weitere KayKit Packs nach Bedarf

- [ ] **2. Room Config erstellen**
  - `room_config_detailed.json` → `/c/Najika/assets/`
  - Alle 12 Räume definieren

- [ ] **3. CSS-Fehler fixen**
  - `chat.css:249` prüfen
  - `code_editor.css:361` prüfen

- [ ] **4. Test nach Fixes**
  - Server neu starten
  - Browser refresh
  - Skeleton_Mage sollte laden
  - Räume sollten ohne Warnung laden
  - Keine CSS-Fehler in Console

---

## 🎯 ZIEL: BASIS CLEAN FÜR OPUS

Wenn alle 4 Punkte gefixt → **Basis ist solide** → Opus kann übernehmen!

**Ende Fehler-Liste**
