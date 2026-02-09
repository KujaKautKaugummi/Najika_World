# ============================================================
# NAJIKA GLB EXPORT - Für Three.js
# ============================================================

import bpy
import os

EXPORT_PATH = r"C:\Najika_World\assets\models\najika\najika_rigged_final.glb"

def export_glb():
    print("\n💾 GLB EXPORT...")

    # Ordner erstellen
    os.makedirs(os.path.dirname(EXPORT_PATH), exist_ok=True)

    # Alles auswählen
    bpy.ops.object.select_all(action='DESELECT')

    for obj in bpy.context.scene.objects:
        if obj.type in ['ARMATURE', 'MESH']:
            if obj.type == 'MESH' and len(obj.data.vertices) > 1000:
                obj.select_set(True)
                bpy.context.view_layer.objects.active = obj
            elif obj.type == 'ARMATURE':
                obj.select_set(True)

    # Export
    bpy.ops.export_scene.gltf(
        filepath=EXPORT_PATH,
        use_selection=True,
        export_format='GLB',
        export_textures=True,
        export_materials='EXPORT',
        export_skins=True,
        export_animations=False,
    )

    print(f"✅ GLB exportiert: {EXPORT_PATH}")

export_glb()
