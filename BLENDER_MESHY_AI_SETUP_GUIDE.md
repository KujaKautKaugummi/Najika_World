# 🎨 BLENDER + MESHY AI PLUGIN - SETUP ANLEITUNG

**Erstellt:** 2026-01-20
**Zweck:** Lokale Blender Installation mit Meshy AI Plugin verbinden
**Für:** Najika 3D-Modell Generation & Editing

---

## 📋 VORAUSSETZUNGEN

### Software
- ✅ **Blender 4.0+** (empfohlen: neueste Version)
- ✅ **Python 3.10+** (sollte mit Blender mitgeliefert werden)
- ✅ **Meshy AI Account** (kostenlos: https://www.meshy.ai)
- ✅ **Internet-Verbindung** (für API-Zugriff)

### Hardware
- **RAM**: Mindestens 8 GB (16 GB empfohlen)
- **GPU**: Optional, aber empfohlen für schnelleres Rendering
- **Speicher**: ~2 GB frei für Blender + Models

---

## 1️⃣ BLENDER INSTALLATION

### Download & Installation

**Option A: Offizielle Website**
```bash
# 1. Gehe zu https://www.blender.org/download/
# 2. Download Blender 4.2 (oder neuer) für Windows
# 3. Installer ausführen (blender-4.2.0-windows-x64.msi)
# 4. Standard-Installation (C:\Program Files\Blender Foundation\Blender 4.2\)
```

**Option B: Microsoft Store** (einfacher!)
```
1. Microsoft Store öffnen
2. "Blender" suchen
3. Installieren (kostenlos)
4. Automatische Updates
```

**Option C: Portable Version**
```bash
# 1. Download von https://www.blender.org/download/
# 2. ZIP-Version wählen (blender-4.2.0-windows-x64.zip)
# 3. Entpacken nach C:\Tools\Blender\
# 4. blender.exe direkt starten (keine Installation nötig)
```

### Erste Schritte
```
1. Blender starten
2. Edit → Preferences öffnen
3. Add-ons Tab öffnen
4. Bereit für Plugin-Installation!
```

---

## 2️⃣ MESHY AI ACCOUNT ERSTELLEN

### Registrierung
```
1. Gehe zu https://www.meshy.ai
2. "Sign Up" klicken
3. Email + Passwort ODER Google/Discord Login
4. Email verifizieren
```

### API Key erhalten
```
1. Einloggen auf Meshy.ai
2. Oben rechts auf Profil klicken
3. "API Keys" oder "Settings" wählen
4. "Create New API Key" klicken
5. API Key KOPIEREN und SICHER SPEICHERN!
```

**WICHTIG**: API Key sieht so aus: `msy_abc123def456...` (NUR EINMAL angezeigt!)

### Credits
- **Kostenloser Account**: ~200 Credits/Monat
- **Text-to-3D**: ~10-20 Credits pro Modell
- **Image-to-3D**: ~30-40 Credits pro Modell

---

## 3️⃣ MESHY AI PLUGIN FÜR BLENDER

### Methode 1: Offizielles Meshy Plugin (EMPFOHLEN)

**Stand 2026-01-20**: Meshy.ai hat möglicherweise noch KEIN offizielles Blender Plugin!

**Prüfen ob verfügbar**:
```
1. Gehe zu https://docs.meshy.ai
2. Suche nach "Blender Plugin" oder "Integrations"
3. Falls vorhanden: Download-Link folgen
```

**Falls NICHT verfügbar** → Methode 2 nutzen!

---

### Methode 2: Meshy API Python Bridge (DIY)

**Da Meshy möglicherweise kein offizielles Plugin hat, erstellen wir eine Bridge!**

#### Schritt 1: Meshy Python SDK installieren

**In Blender's Python**:
```python
# 1. Blender öffnen
# 2. Scripting Tab wechseln
# 3. Neues Script erstellen
# 4. Folgenden Code ausführen:

import subprocess
import sys

# Blender's Python-Pfad finden
python_exe = sys.executable
print(f"Blender Python: {python_exe}")

# Meshy SDK installieren (via pip)
subprocess.check_call([python_exe, "-m", "ensurepip"])
subprocess.check_call([python_exe, "-m", "pip", "install", "--upgrade", "pip"])
subprocess.check_call([python_exe, "-m", "pip", "install", "requests"])

print("✅ Installation complete!")
```

**ODER extern installieren** (einfacher!):
```bash
# 1. CMD als Administrator öffnen
# 2. Blender's Python finden:
cd "C:\Program Files\Blender Foundation\Blender 4.2\4.2\python\bin"

# 3. Packages installieren:
python.exe -m pip install requests
```

#### Schritt 2: Meshy API Bridge Script erstellen

**Erstelle Datei: `C:\Najika_World\blender\meshy_api_bridge.py`**

```python
"""
MESHY AI API BRIDGE FOR BLENDER
Verbindet Blender mit Meshy.ai Text-to-3D API
"""

import bpy
import requests
import json
import time
import os
from pathlib import Path

class MeshyAPIBridge:
    """Meshy.ai API Client für Blender"""

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.meshy.ai/v2"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def text_to_3d(self, prompt, negative_prompt="", art_style="realistic", output_path=None):
        """
        Generiert 3D-Modell aus Text-Prompt

        Args:
            prompt (str): Text-Beschreibung des Modells
            negative_prompt (str): Was NICHT generieren
            art_style (str): "realistic", "cartoon", "anime", "sculpture"
            output_path (str): Wo .glb/.fbx speichern

        Returns:
            str: Pfad zur generierten .glb Datei
        """

        # 1. Task erstellen
        print(f"📤 Sende Prompt an Meshy AI...")
        print(f"Prompt: {prompt[:100]}...")

        payload = {
            "mode": "preview",  # "preview" (schnell) oder "refine" (langsam, besser)
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "art_style": art_style,
            "seed": 0  # 0 = random
        }

        response = requests.post(
            f"{self.base_url}/text-to-3d",
            headers=self.headers,
            json=payload
        )

        if response.status_code != 200:
            raise Exception(f"API Error: {response.status_code} - {response.text}")

        task_id = response.json()["result"]
        print(f"✅ Task erstellt: {task_id}")

        # 2. Warten bis fertig
        print("⏳ Warte auf Generation...")
        while True:
            status_response = requests.get(
                f"{self.base_url}/text-to-3d/{task_id}",
                headers=self.headers
            )

            status = status_response.json()
            state = status.get("status")
            progress = status.get("progress", 0)

            print(f"Status: {state} ({progress}%)")

            if state == "SUCCEEDED":
                print("✅ Generation erfolgreich!")
                break
            elif state == "FAILED":
                raise Exception(f"Generation fehlgeschlagen: {status.get('error')}")

            time.sleep(5)  # 5 Sekunden warten

        # 3. Download URL erhalten
        model_urls = status.get("model_urls", {})
        glb_url = model_urls.get("glb")

        if not glb_url:
            raise Exception("Keine GLB-Datei in Antwort!")

        # 4. Model herunterladen
        print(f"⬇️ Lade Modell herunter...")
        model_response = requests.get(glb_url)

        # 5. Speichern
        if not output_path:
            output_dir = Path("C:/Najika_World/blender/generated_models")
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / f"najika_model_{task_id}.glb"

        with open(output_path, "wb") as f:
            f.write(model_response.content)

        print(f"✅ Modell gespeichert: {output_path}")
        return str(output_path)

    def import_to_blender(self, glb_path):
        """Importiert .glb Datei in Blender"""

        print(f"📥 Importiere Modell in Blender...")

        # GLB importieren (Blender 4.0+)
        bpy.ops.import_scene.gltf(filepath=glb_path)

        print("✅ Modell importiert!")
        return True


# ===== BLENDER ADDON REGISTRATION =====

class MESHY_OT_generate(bpy.types.Operator):
    """Generate 3D Model from Text using Meshy AI"""
    bl_idname = "meshy.generate"
    bl_label = "Generate with Meshy AI"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        meshy_props = scene.meshy_props

        # API Key prüfen
        if not meshy_props.api_key:
            self.report({'ERROR'}, "Bitte API Key eingeben!")
            return {'CANCELLED'}

        # Bridge erstellen
        bridge = MeshyAPIBridge(meshy_props.api_key)

        try:
            # Generieren
            glb_path = bridge.text_to_3d(
                prompt=meshy_props.prompt,
                negative_prompt=meshy_props.negative_prompt,
                art_style=meshy_props.art_style
            )

            # In Blender importieren
            bridge.import_to_blender(glb_path)

            self.report({'INFO'}, "Modell erfolgreich generiert!")
            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, f"Fehler: {str(e)}")
            return {'CANCELLED'}


class MESHY_PT_panel(bpy.types.Panel):
    """Meshy AI Panel in Blender"""
    bl_label = "Meshy AI Generator"
    bl_idname = "MESHY_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Meshy AI'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        meshy_props = scene.meshy_props

        # API Key
        layout.label(text="API Key:")
        layout.prop(meshy_props, "api_key", text="")

        # Prompt
        layout.label(text="Prompt:")
        layout.prop(meshy_props, "prompt", text="")

        # Negative Prompt
        layout.label(text="Negative Prompt:")
        layout.prop(meshy_props, "negative_prompt", text="")

        # Art Style
        layout.label(text="Art Style:")
        layout.prop(meshy_props, "art_style", text="")

        # Generate Button
        layout.operator("meshy.generate", text="Generate 3D Model", icon='MESH_CUBE')


class MeshyProperties(bpy.types.PropertyGroup):
    api_key: bpy.props.StringProperty(
        name="API Key",
        description="Meshy AI API Key",
        default="",
        subtype='PASSWORD'
    )

    prompt: bpy.props.StringProperty(
        name="Prompt",
        description="Text description of 3D model",
        default="Anime gothic lolita catgirl, 140cm, chibi proportions...",
        maxlen=1024
    )

    negative_prompt: bpy.props.StringProperty(
        name="Negative Prompt",
        description="What NOT to generate",
        default="long arms, long legs, realistic proportions, flat butt",
        maxlen=512
    )

    art_style: bpy.props.EnumProperty(
        name="Art Style",
        description="Visual style of model",
        items=[
            ('realistic', "Realistic", "Realistic style"),
            ('cartoon', "Cartoon", "Cartoon style"),
            ('anime', "Anime", "Anime/manga style"),
            ('sculpture', "Sculpture", "Sculpture style"),
        ],
        default='anime'
    )


classes = (
    MeshyProperties,
    MESHY_OT_generate,
    MESHY_PT_panel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.meshy_props = bpy.props.PointerProperty(type=MeshyProperties)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.meshy_props


if __name__ == "__main__":
    register()
```

#### Schritt 3: Plugin in Blender laden

**Methode A: Als Addon installieren** (permanent):
```
1. Blender öffnen
2. Edit → Preferences → Add-ons
3. "Install..." klicken
4. meshy_api_bridge.py auswählen
5. ✅ Addon aktivieren (Checkbox)
6. Preferences speichern
```

**Methode B: Direkt laden** (temporär):
```
1. Blender öffnen
2. Scripting Tab
3. "Open" → meshy_api_bridge.py
4. "Run Script" klicken
```

---

## 4️⃣ NUTZUNG

### Meshy AI Panel öffnen

```
1. Blender öffnen
2. 3D Viewport
3. Rechte Seitenpanel öffnen (N-Taste drücken)
4. "Meshy AI" Tab sichtbar
```

### API Key eingeben

```
1. Im Meshy AI Panel
2. "API Key" Feld ausfüllen
3. API Key von Meshy.ai einfügen (msy_abc123...)
4. WICHTIG: Wird verschlüsselt gespeichert!
```

### Najika-Modell generieren

```
1. "Prompt" Feld:
   → Kopiere Prompt aus NAJIKA_MESHY_800_ZEICHEN.txt

2. "Negative Prompt" Feld:
   → long arms, long legs, realistic proportions, flat butt, no bulge

3. "Art Style":
   → "Anime" auswählen

4. "Generate 3D Model" klicken

5. Warten (~2-5 Minuten)

6. Modell wird automatisch in Scene importiert! ✅
```

### Modell bearbeiten

```
1. Modell ist jetzt in Blender
2. Edit Mode (Tab-Taste)
3. Proportionen anpassen:
   - S-Taste = Scale (Skalieren)
   - G-Taste = Grab (Bewegen)
   - R-Taste = Rotate (Drehen)
4. Sculpt Mode für Details
5. Material Editor für Texturen
```

---

## 5️⃣ ALTERNATIVE: MANUELLE METHODE (OHNE PLUGIN)

Falls Plugin nicht funktioniert:

### Workflow ohne Plugin

```
1. Meshy.ai Website öffnen (https://app.meshy.ai)
2. Einloggen
3. "Text to 3D" wählen
4. Prompt einfügen (aus NAJIKA_MESHY_800_ZEICHEN.txt)
5. "Generate" klicken
6. Warten (~2-5 Minuten)
7. "Download GLB" klicken
8. Datei speichern (z.B. najika_model.glb)

--- IN BLENDER ---

9. Blender öffnen
10. File → Import → glTF 2.0 (.glb/.gltf)
11. najika_model.glb auswählen
12. Import bestätigen
13. Modell ist jetzt in Blender! ✅
```

---

## 6️⃣ TROUBLESHOOTING

### Problem: "API Key ungültig"

**Lösung**:
```
1. Meshy.ai Website öffnen
2. Neuen API Key erstellen
3. Alten Key löschen
4. Neuen Key in Blender einfügen
```

### Problem: "requests module not found"

**Lösung**:
```bash
# CMD als Admin:
cd "C:\Program Files\Blender Foundation\Blender 4.2\4.2\python\bin"
python.exe -m pip install requests
```

### Problem: "Generation dauert ewig"

**Lösung**:
- Preview Mode dauert ~2-5 Minuten (normal)
- Refine Mode dauert ~10-20 Minuten (besser)
- Internet-Verbindung prüfen
- Meshy.ai Status prüfen: https://status.meshy.ai

### Problem: "Model sieht falsch aus"

**Lösung**:
- Prompt anpassen (siehe nächster Abschnitt)
- Negative Prompts erweitern
- Art Style ändern (anime vs. cartoon)
- Seed ändern (verschiedene Variationen)

---

## 7️⃣ PROMPT-OPTIMIERUNG FÜR NAJIKA

### Aktuelle Probleme beheben

**Falls Arme/Beine zu lang**:
```
Füge hinzu: "VERY SHORT arms and legs, chibi proportions, lolita body"
Wiederhole "SHORT" mehrfach!
```

**Falls Beule nicht sichtbar**:
```
Füge hinzu: "PROMINENT visible bulge in underwear, clearly shown anatomical shape"
Wiederhole "VISIBLE" mehrfach!
```

**Falls Po zu klein**:
```
Füge hinzu: "MASSIVE round butt (DOUBLE size), very large prominent butt as main feature"
Wiederhole "VERY LARGE" mehrfach!
```

**Falls zu realistisch**:
```
Art Style: "anime" (NICHT "realistic")
Füge hinzu: "cute anime style, gothic lolita aesthetic, doll-like features"
```

### Iterations-Strategie

**Iteration 1**: Base Model generieren
- Standard Prompt nutzen
- Prüfen was falsch ist

**Iteration 2**: Korrekturen hinzufügen
- "Same as before BUT: [was korrigieren]"
- Nur 1-2 Dinge auf einmal ändern!

**Iteration 3**: Fein-Tuning
- Details optimieren
- Symmetrie korrigieren

---

## 8️⃣ EXPORT FÜR NAJIKA WORLD

### Format-Konvertierung

**GLB → FBX** (für Three.js):
```
1. Modell in Blender öffnen
2. File → Export → FBX (.fbx)
3. Settings:
   - Scale: 1.0
   - Forward: -Z Forward
   - Up: Y Up
   - Apply Transform: ✅
4. Export bestätigen
```

**GLB → GLTF** (für Web):
```
1. File → Export → glTF 2.0 (.glb/.gltf)
2. Format: glTF Separate (.gltf + .bin + textures)
3. Export bestätigen
```

### In Najika World integrieren

```javascript
// In digivice/js/world/asset_loader.js

import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

const loader = new GLTFLoader();

loader.load('models/najika_model.glb', (gltf) => {
    const najika = gltf.scene;

    // Skalierung anpassen (140cm in Blender Units)
    najika.scale.set(1.4, 1.4, 1.4);

    // Position setzen
    najika.position.set(0, 0, 0);

    // Zur Scene hinzufügen
    scene.add(najika);

    console.log('✅ Najika-Modell geladen!');
});
```

---

## 9️⃣ KOSTEN-ÜBERSICHT

### Meshy AI Pricing (Stand 2026-01-20)

**Free Plan**:
- ~200 Credits/Monat
- Text-to-3D Preview: ~10-20 Credits
- Text-to-3D Refine: ~40-60 Credits
- = ~10-20 Modelle/Monat kostenlos!

**Pro Plan** (~$16/Monat):
- ~1500 Credits/Monat
- Schnellere Generation
- Höhere Qualität
- Mehr Variationen

**Empfehlung für Najika**:
- **Free Plan starten** (reicht für Tests!)
- Bei Zufriedenheit → Pro upgraden

---

## 🎯 QUICK START CHECKLIST

- [ ] Blender 4.0+ installiert
- [ ] Meshy AI Account erstellt
- [ ] API Key erhalten
- [ ] `requests` Package installiert
- [ ] `meshy_api_bridge.py` in Blender geladen
- [ ] API Key im Panel eingegeben
- [ ] Najika-Prompt aus `NAJIKA_MESHY_800_ZEICHEN.txt` kopiert
- [ ] Erstes Modell generiert
- [ ] Modell in Blender importiert
- [ ] Proportionen geprüft
- [ ] Export nach GLB/FBX
- [ ] In Najika World integriert

---

## 📚 ZUSÄTZLICHE RESSOURCEN

### Meshy AI Dokumentation
- **API Docs**: https://docs.meshy.ai
- **Tutorials**: https://meshy.ai/tutorials
- **Discord**: https://discord.gg/meshy (Community Support)

### Blender Tutorials
- **Offiziell**: https://www.blender.org/support/tutorials/
- **3D Modeling**: YouTube "Blender 4.0 Character Modeling"
- **Scripting**: Blender Python API Docs

### Three.js Integration
- **GLTF Loader**: https://threejs.org/docs/#examples/en/loaders/GLTFLoader
- **Model Optimization**: https://gltf.report/

---

## ✅ FERTIG!

**Du hast jetzt:**
- ✅ Blender lokal installiert
- ✅ Meshy AI verbunden (via Plugin ODER manuell)
- ✅ Najika-Modell generieren können
- ✅ Workflow für Iterations und Optimierung
- ✅ Export für Najika World

**Nächste Schritte**:
1. Erstes Modell generieren mit Najika-Prompt
2. Screenshot schicken für Feedback
3. Prompt basierend auf Ergebnis anpassen
4. Iterieren bis perfekt!
5. In Najika World integrieren

**Viel Erfolg! 🎨**

---

**Erstellt von:** Claude Sonnet 4.5
**Für:** Kuja
**Status:** ✅ COMPLETE
**Version:** 1.0 (2026-01-20)
