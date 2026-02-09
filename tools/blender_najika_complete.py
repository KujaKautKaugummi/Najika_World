# ============================================================
# NAJIKA COMPLETE MODEL TOOL - Blender Script v2
# ============================================================
# 1. Importiert GLB Model
# 2. Projiziert Augen/Nase/Lippen vom Referenzbild
# 3. Erstellt Megumin's Halsband (detailliert)
# 4. Optimiert Haut-Shader (SSS)
# 5. Polygon-Reduktion Option
# ============================================================
#
# ANLEITUNG:
# 1. Blender 3.6+ öffnen
# 2. Scripting-Tab
# 3. Dieses Script öffnen
# 4. Run Script (Alt+P)
# ============================================================

import bpy
import bmesh
import os
import math

# ============================================================
# KONFIGURATION
# ============================================================
CONFIG = {
    "model_path": r"C:\Users\0KKK0\Downloads\Meshy_AI__0203174321_texture.glb",
    "face_reference": r"C:\Najika_World\assets\textures\najika_face_reference.png",
    "output_path": r"C:\Najika_World\assets\models\najika\najika_final.glb",

    # Haut-Einstellungen
    "skin_sss_weight": 0.35,
    "skin_sss_radius": (1.0, 0.2, 0.1),
    "skin_roughness": 0.35,

    # Choker-Einstellungen (Megumin Style)
    "choker_color": (0.05, 0.05, 0.05, 1.0),  # Fast Schwarz
    "choker_gem_color": (1.0, 0.8, 0.0, 1.0),  # Gold/Gelb
    "choker_width": 0.025,
    "choker_height_offset": 1.45,  # Hals-Höhe (anpassen!)
}

# ============================================================
# UTILITY FUNKTIONEN
# ============================================================
def find_mesh_object():
    """Findet das Haupt-Mesh-Objekt"""
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH' and len(obj.data.vertices) > 1000:
            return obj
    return None

def get_vertex_z_range(obj):
    """Ermittelt min/max Z-Koordinaten"""
    verts = [obj.matrix_world @ v.co for v in obj.data.vertices]
    z_values = [v.z for v in verts]
    return min(z_values), max(z_values)

# ============================================================
# SCHRITT 1: MODEL IMPORTIEREN
# ============================================================
def import_najika_model():
    """Importiert das Najika GLB Model"""
    print("\n📦 IMPORTIERE MODEL...")

    path = CONFIG["model_path"]
    if not os.path.exists(path):
        print(f"❌ Model nicht gefunden: {path}")
        return None

    # Importiere GLB
    bpy.ops.import_scene.gltf(filepath=path)

    # Finde importiertes Mesh
    obj = find_mesh_object()
    if obj:
        obj.name = "Najika_Body"
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)

        # Stats
        verts = len(obj.data.vertices)
        faces = len(obj.data.polygons)
        z_min, z_max = get_vertex_z_range(obj)

        print(f"✓ Model importiert: {obj.name}")
        print(f"  Vertices: {verts:,}")
        print(f"  Faces: {faces:,}")
        print(f"  Höhe: {z_max - z_min:.2f} units (Z: {z_min:.2f} bis {z_max:.2f})")

        return obj

    print("❌ Kein Mesh gefunden!")
    return None

# ============================================================
# SCHRITT 2: HAUT-SHADER OPTIMIEREN
# ============================================================
def setup_skin_material(obj):
    """Erstellt realistischen Haut-Shader mit SSS"""
    print("\n🎨 ERSTELLE HAUT-SHADER...")

    if obj is None:
        return

    mat_name = "Najika_Skin_Realistic"

    # Material erstellen/holen
    if mat_name in bpy.data.materials:
        mat = bpy.data.materials[mat_name]
        mat.node_tree.nodes.clear()
    else:
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        mat.node_tree.nodes.clear()

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # === NODE SETUP ===

    # Output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (800, 0)

    # Principled BSDF (Haupt-Shader)
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (500, 0)
    bsdf.inputs['Subsurface Weight'].default_value = CONFIG["skin_sss_weight"]
    bsdf.inputs['Subsurface Radius'].default_value = CONFIG["skin_sss_radius"]
    bsdf.inputs['Roughness'].default_value = CONFIG["skin_roughness"]
    bsdf.inputs['Specular IOR Level'].default_value = 0.3

    # Original Texture
    tex_original = nodes.new('ShaderNodeTexImage')
    tex_original.location = (-400, 200)
    tex_original.label = "Original_Skin_Texture"

    # Versuche Original-Textur zu finden
    for img in bpy.data.images:
        if "texture" in img.name.lower() or "base" in img.name.lower():
            tex_original.image = img
            print(f"  → Original Textur gefunden: {img.name}")
            break

    # Face Reference Texture
    tex_face = nodes.new('ShaderNodeTexImage')
    tex_face.location = (-400, -100)
    tex_face.label = "Face_Reference"

    if os.path.exists(CONFIG["face_reference"]):
        img = bpy.data.images.load(CONFIG["face_reference"])
        tex_face.image = img
        print(f"  → Face Reference geladen")
    else:
        print(f"  ⚠ Face Reference nicht gefunden!")
        print(f"    Speichere hier: {CONFIG['face_reference']}")

    # Mix für Face Blending
    mix_face = nodes.new('ShaderNodeMixRGB')
    mix_face.location = (100, 100)
    mix_face.blend_type = 'MIX'
    mix_face.inputs['Fac'].default_value = 0.0
    mix_face.label = "Face_Blend_Control"

    # UV Map Node für Projektion
    uv_map = nodes.new('ShaderNodeUVMap')
    uv_map.location = (-600, 0)
    uv_map.uv_map = "UVMap"

    # Texture Coordinate für Projektion
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-600, -200)

    # === VERBINDUNGEN ===
    links.new(uv_map.outputs['UV'], tex_original.inputs['Vector'])
    links.new(tex_original.outputs['Color'], mix_face.inputs['Color1'])
    links.new(tex_face.outputs['Color'], mix_face.inputs['Color2'])
    links.new(mix_face.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    # Material zuweisen
    obj.data.materials.clear()
    obj.data.materials.append(mat)

    print("✓ Haut-Shader erstellt")
    print("  → Face_Blend_Control: Fac 0→1 für Gesichtsprojektion")

# ============================================================
# SCHRITT 3: MEGUMIN HALSBAND ERSTELLEN
# ============================================================
def create_megumin_choker(body_obj):
    """Erstellt Megumin's charakteristisches Halsband"""
    print("\n💎 ERSTELLE MEGUMIN HALSBAND...")

    if body_obj is None:
        return None

    # Hals-Position ermitteln
    z_min, z_max = get_vertex_z_range(body_obj)
    total_height = z_max - z_min

    # Hals ist ungefähr bei 85-90% der Gesamthöhe
    neck_z = z_min + (total_height * 0.87)

    # Halsradius schätzen (basierend auf Modellgröße)
    neck_radius = total_height * 0.045

    print(f"  Geschätzte Hals-Position: Z={neck_z:.3f}")
    print(f"  Geschätzter Hals-Radius: {neck_radius:.3f}")

    # === HAUPTBAND ===
    bpy.ops.mesh.primitive_torus_add(
        align='WORLD',
        location=(0, 0, neck_z),
        rotation=(math.pi/2, 0, 0),  # Horizontal ausrichten
        major_radius=neck_radius,
        minor_radius=CONFIG["choker_width"] / 2,
        major_segments=64,
        minor_segments=16
    )

    choker_band = bpy.context.active_object
    choker_band.name = "Najika_Choker_Band"

    # Band Material (Schwarz/Dunkel)
    mat_band = bpy.data.materials.new(name="Choker_Band_Material")
    mat_band.use_nodes = True
    bsdf_band = mat_band.node_tree.nodes["Principled BSDF"]
    bsdf_band.inputs['Base Color'].default_value = CONFIG["choker_color"]
    bsdf_band.inputs['Roughness'].default_value = 0.2
    bsdf_band.inputs['Specular IOR Level'].default_value = 0.5
    choker_band.data.materials.append(mat_band)

    # === ZENTRALER EDELSTEIN (Megumin Style) ===
    gem_size = neck_radius * 0.25
    gem_z = neck_z
    gem_y = -(neck_radius + gem_size * 0.3)  # Vorne am Hals

    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=gem_size,
        segments=32,
        ring_count=16,
        location=(0, gem_y, gem_z)
    )

    gem = bpy.context.active_object
    gem.name = "Najika_Choker_Gem"

    # Edelstein leicht abflachen
    gem.scale = (1.0, 0.6, 1.0)
    bpy.ops.object.transform_apply(scale=True)

    # Edelstein Material (Gold/Gelb - Megumin Style)
    mat_gem = bpy.data.materials.new(name="Choker_Gem_Material")
    mat_gem.use_nodes = True
    nodes = mat_gem.node_tree.nodes
    links = mat_gem.node_tree.links

    bsdf_gem = nodes["Principled BSDF"]
    bsdf_gem.inputs['Base Color'].default_value = CONFIG["choker_gem_color"]
    bsdf_gem.inputs['Metallic'].default_value = 0.8
    bsdf_gem.inputs['Roughness'].default_value = 0.1
    bsdf_gem.inputs['Specular IOR Level'].default_value = 1.0

    # Emission für Glühen
    bsdf_gem.inputs['Emission Color'].default_value = (1.0, 0.9, 0.3, 1.0)
    bsdf_gem.inputs['Emission Strength'].default_value = 0.3

    gem.data.materials.append(mat_gem)

    # === SEITLICHE VERZIERUNGEN ===
    for side in [-1, 1]:
        x_pos = side * (neck_radius * 0.7)

        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=gem_size * 0.4,
            segments=16,
            ring_count=8,
            location=(x_pos, gem_y * 0.8, gem_z)
        )

        side_gem = bpy.context.active_object
        side_gem.name = f"Najika_Choker_SideGem_{'L' if side < 0 else 'R'}"
        side_gem.data.materials.append(mat_gem)

    # === ALLES GRUPPIEREN ===
    # Collection erstellen
    if "Najika_Choker" not in bpy.data.collections:
        choker_col = bpy.data.collections.new("Najika_Choker")
        bpy.context.scene.collection.children.link(choker_col)
    else:
        choker_col = bpy.data.collections["Najika_Choker"]

    # Objekte in Collection verschieben
    for obj in bpy.context.scene.objects:
        if "Choker" in obj.name:
            for col in obj.users_collection:
                col.objects.unlink(obj)
            choker_col.objects.link(obj)

    print("✓ Megumin Halsband erstellt")
    print("  → Band: Schwarz mit leichtem Glanz")
    print("  → Edelstein: Gold/Gelb (Megumin-Style)")
    print("  → 2 seitliche Verzierungen")
    print("  ⚠ Position manuell feintunen falls nötig!")

    return choker_band

# ============================================================
# SCHRITT 4: VERTEX GRUPPEN FÜR GESICHT
# ============================================================
def create_face_vertex_groups(obj):
    """Erstellt Vertex-Gruppen für Gesichtsbereiche"""
    print("\n👁 ERSTELLE VERTEX-GRUPPEN...")

    if obj is None:
        return

    groups = ["Face_Eyes", "Face_Nose", "Face_Lips", "Face_All"]

    for group_name in groups:
        if group_name not in obj.vertex_groups:
            obj.vertex_groups.new(name=group_name)

    print("✓ Vertex-Gruppen erstellt:")
    print("  → Face_Eyes: Für Augenbereich")
    print("  → Face_Nose: Für Nasenbereich")
    print("  → Face_Lips: Für Lippenbereich")
    print("  → Face_All: Komplettes Gesicht")
    print("\n  📝 ANLEITUNG:")
    print("  1. Edit Mode (Tab)")
    print("  2. Vertices im Gesicht auswählen")
    print("  3. Object Data Properties > Vertex Groups")
    print("  4. 'Assign' klicken")

# ============================================================
# SCHRITT 5: POLYGON REDUKTION (OPTIONAL)
# ============================================================
def reduce_polygons(obj, ratio=0.5):
    """Reduziert Polygone mit Decimate Modifier"""
    print(f"\n📐 POLYGON-REDUKTION ({ratio*100:.0f}%)...")

    if obj is None:
        return

    original_faces = len(obj.data.polygons)

    # Decimate Modifier
    decimate = obj.modifiers.new(name="Decimate_Reduction", type='DECIMATE')
    decimate.ratio = ratio
    decimate.use_collapse_triangulate = True

    print(f"  Original: {original_faces:,} Faces")
    print(f"  Ziel: ~{int(original_faces * ratio):,} Faces")
    print("  ⚠ Modifier hinzugefügt - Apply manuell wenn zufrieden!")

# ============================================================
# SCHRITT 6: EXPORT
# ============================================================
def export_model(include_choker=True):
    """Exportiert das finale Model als GLB"""
    print("\n💾 EXPORTIERE MODEL...")

    # Wähle relevante Objekte
    bpy.ops.object.select_all(action='DESELECT')

    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            if "Najika" in obj.name:
                obj.select_set(True)
            elif include_choker and "Choker" in obj.name:
                obj.select_set(True)

    output_path = CONFIG["output_path"]
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    bpy.ops.export_scene.gltf(
        filepath=output_path,
        use_selection=True,
        export_format='GLB',
        export_textures=True,
        export_materials='EXPORT'
    )

    print(f"✓ Exportiert: {output_path}")

# ============================================================
# HAUPTPROGRAMM
# ============================================================
def main():
    print("\n" + "="*70)
    print("🎀 NAJIKA COMPLETE MODEL TOOL v2")
    print("="*70)

    # 1. Model importieren
    najika = import_najika_model()

    if najika is None:
        print("\n❌ ABBRUCH: Model konnte nicht geladen werden!")
        return

    # 2. Haut-Shader
    setup_skin_material(najika)

    # 3. Megumin Halsband
    create_megumin_choker(najika)

    # 4. Vertex-Gruppen
    create_face_vertex_groups(najika)

    # 5. Polygon-Reduktion (auskommentiert - manuell aktivieren)
    # reduce_polygons(najika, ratio=0.3)

    # 6. Export (auskommentiert - manuell aktivieren)
    # export_model()

    print("\n" + "="*70)
    print("✅ SETUP ABGESCHLOSSEN!")
    print("="*70)

    print("\n📋 NÄCHSTE SCHRITTE:")
    print("-"*40)
    print("1. FACE REFERENCE speichern:")
    print(f"   {CONFIG['face_reference']}")
    print("")
    print("2. GESICHT PROJIZIEREN:")
    print("   a) Edit Mode → Gesicht auswählen")
    print("   b) UV Editor → Project from View (Numpad 1)")
    print("   c) UVs auf Referenzbild ausrichten")
    print("   d) Material → Face_Blend_Control → Fac erhöhen")
    print("")
    print("3. HALSBAND ANPASSEN:")
    print("   a) Position zum Hals verschieben")
    print("   b) Skalieren falls nötig")
    print("")
    print("4. OPTIONAL:")
    print("   - reduce_polygons() aktivieren")
    print("   - export_model() aktivieren")
    print("-"*40)

# ============================================================
# SCRIPT AUSFÜHREN
# ============================================================
if __name__ == "__main__":
    main()
