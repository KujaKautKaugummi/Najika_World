# ============================================================
# NAJIKA EXPORT - Alle Settings richtig für UEFN
# ============================================================

import bpy
import os

# Export Pfade
EXPORT_FOLDER = r"C:\Najika_World\assets\models\najika"
FBX_NAME = "najika_rigged_final.fbx"
GLB_NAME = "najika_rigged_final.glb"

def export_najika():
    print("\n" + "="*50)
    print("💾 NAJIKA EXPORT")
    print("="*50)

    # Ordner erstellen falls nicht vorhanden
    os.makedirs(EXPORT_FOLDER, exist_ok=True)

    # Alles auswählen was zu Najika gehört
    bpy.ops.object.select_all(action='DESELECT')

    armature = None
    mesh = None

    for obj in bpy.context.scene.objects:
        if obj.type == 'ARMATURE':
            obj.select_set(True)
            armature = obj
            print(f"✓ Armature: {obj.name}")
        elif obj.type == 'MESH' and len(obj.data.vertices) > 1000:
            obj.select_set(True)
            mesh = obj
            print(f"✓ Mesh: {obj.name}")

    if mesh is None:
        print("❌ Kein Mesh gefunden!")
        return

    # Active Object setzen
    bpy.context.view_layer.objects.active = mesh

    # ==========================================
    # FBX EXPORT (für UEFN)
    # ==========================================
    fbx_path = os.path.join(EXPORT_FOLDER, FBX_NAME)

    bpy.ops.export_scene.fbx(
        filepath=fbx_path,
        use_selection=True,
        apply_scale_options='FBX_SCALE_ALL',
        path_mode='COPY',
        embed_textures=True,
        use_mesh_modifiers=True,
        mesh_smooth_type='FACE',
        use_mesh_edges=False,
        add_leaf_bones=False,
        primary_bone_axis='Y',
        secondary_bone_axis='X',
        use_armature_deform_only=True,
        bake_anim=False,
        bake_anim_use_all_actions=False,
    )

    print(f"\n✅ FBX exportiert: {fbx_path}")

    # ==========================================
    # GLB EXPORT (für Three.js)
    # ==========================================
    glb_path = os.path.join(EXPORT_FOLDER, GLB_NAME)

    bpy.ops.export_scene.gltf(
        filepath=glb_path,
        use_selection=True,
        export_format='GLB',
        export_textures=True,
        export_materials='EXPORT',
        export_skins=True,
        export_animations=False,
        export_apply=True,
    )

    print(f"✅ GLB exportiert: {glb_path}")

    # ==========================================
    # ZUSAMMENFASSUNG
    # ==========================================
    print("\n" + "="*50)
    print("📦 EXPORT FERTIG!")
    print("="*50)
    print(f"\n📁 Ordner: {EXPORT_FOLDER}")
    print(f"\n📄 Dateien:")
    print(f"   • {FBX_NAME} → Für UEFN/Unreal")
    print(f"   • {GLB_NAME} → Für Three.js/Web")
    print("\n🎮 UEFN Import:")
    print("   1. UEFN öffnen")
    print("   2. Content Browser → Import")
    print("   3. FBX auswählen")
    print("   4. Import Settings:")
    print("      • Skeletal Mesh: ✓")
    print("      • Import Textures: ✓")
    print("      • Import Materials: ✓")

export_najika()
