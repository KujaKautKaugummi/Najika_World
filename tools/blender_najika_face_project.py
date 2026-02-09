# ============================================================
# NAJIKA FACE PROJECTION TOOL - Blender Script
# ============================================================
# Überträgt Augen, Nase, Lippen vom Referenzbild auf das Modell
#
# ANLEITUNG:
# 1. Blender öffnen
# 2. Scripting-Tab wechseln
# 3. Dieses Script öffnen und ausführen
# ============================================================

import bpy
import os

# ============================================================
# PFADE - ANPASSEN FALLS NÖTIG
# ============================================================
MODEL_PATH = r"C:\Users\0KKK0\Downloads\Meshy_AI__0203174321_texture.glb"
# Referenzbild mit den gewünschten Augen/Nase/Lippen hier einfügen:
REFERENCE_IMAGE = r"C:\Najika_World\assets\textures\najika_face_reference.png"

# ============================================================
# SCHRITT 1: Scene aufräumen
# ============================================================
def clear_scene():
    """Löscht alle Objekte in der Scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    print("✓ Scene aufgeräumt")

# ============================================================
# SCHRITT 2: GLB Model importieren
# ============================================================
def import_model():
    """Importiert das Najika GLB Model"""
    if not os.path.exists(MODEL_PATH):
        print(f"❌ FEHLER: Model nicht gefunden: {MODEL_PATH}")
        return None

    bpy.ops.import_scene.gltf(filepath=MODEL_PATH)

    # Finde das importierte Mesh
    for obj in bpy.context.selected_objects:
        if obj.type == 'MESH':
            print(f"✓ Model importiert: {obj.name}")
            print(f"  Vertices: {len(obj.data.vertices)}")
            print(f"  Faces: {len(obj.data.polygons)}")
            return obj

    return None

# ============================================================
# SCHRITT 3: Gesichts-Vertex-Gruppe erstellen
# ============================================================
def create_face_vertex_group(obj):
    """Erstellt eine Vertex-Gruppe für das Gesicht"""
    if obj is None:
        return

    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    # Neue Vertex-Gruppe für Gesicht
    if "Face_Region" not in obj.vertex_groups:
        vg = obj.vertex_groups.new(name="Face_Region")
        print("✓ Vertex-Gruppe 'Face_Region' erstellt")
        print("  → Wechsle in Edit Mode und wähle das Gesicht aus")
        print("  → Dann: Mesh > Assign to Vertex Group")
    else:
        print("✓ Vertex-Gruppe 'Face_Region' existiert bereits")

# ============================================================
# SCHRITT 4: Material für Texture Projection vorbereiten
# ============================================================
def setup_projection_material(obj):
    """Richtet Material für Texture-Projektion ein"""
    if obj is None:
        return

    mat_name = "Najika_Face_Projected"

    # Prüfe ob Material existiert
    if mat_name in bpy.data.materials:
        mat = bpy.data.materials[mat_name]
    else:
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True

    # Node Tree aufbauen
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Bestehende Nodes entfernen
    for node in nodes:
        nodes.remove(node)

    # === NODES ERSTELLEN ===

    # Output Node
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (600, 0)

    # Principled BSDF für realistische Haut
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (300, 0)
    bsdf.inputs['Subsurface Weight'].default_value = 0.3  # SSS für Haut
    bsdf.inputs['Subsurface Radius'].default_value = (1.0, 0.2, 0.1)  # Rot durchscheinend
    bsdf.inputs['Roughness'].default_value = 0.4

    # Base Color Texture (Original)
    tex_base = nodes.new('ShaderNodeTexImage')
    tex_base.location = (-300, 200)
    tex_base.label = "Original_Texture"

    # Face Reference Texture (zum Projizieren)
    tex_face = nodes.new('ShaderNodeTexImage')
    tex_face.location = (-300, -100)
    tex_face.label = "Face_Reference"

    # Lade Referenzbild falls vorhanden
    if os.path.exists(REFERENCE_IMAGE):
        img = bpy.data.images.load(REFERENCE_IMAGE)
        tex_face.image = img
        print(f"✓ Referenzbild geladen: {REFERENCE_IMAGE}")
    else:
        print(f"⚠ Referenzbild nicht gefunden: {REFERENCE_IMAGE}")
        print("  → Speichere das Referenzbild dort ab!")

    # Mix RGB für Blending
    mix = nodes.new('ShaderNodeMixRGB')
    mix.location = (0, 100)
    mix.blend_type = 'MIX'
    mix.inputs['Fac'].default_value = 0.0  # Startet bei 0 (nur Original)
    mix.label = "Face_Blend"

    # === NODES VERBINDEN ===
    links.new(tex_base.outputs['Color'], mix.inputs['Color1'])
    links.new(tex_face.outputs['Color'], mix.inputs['Color2'])
    links.new(mix.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    # Material zuweisen
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

    print("✓ Projection-Material erstellt")
    print("  → 'Face_Blend' Node: Fac von 0→1 für mehr Reference")

# ============================================================
# SCHRITT 5: UV Projection Setup
# ============================================================
def setup_uv_projection(obj):
    """Bereitet UV-Projektion für das Gesicht vor"""
    if obj is None:
        return

    bpy.context.view_layer.objects.active = obj

    # Prüfe ob UV Map existiert
    if len(obj.data.uv_layers) == 0:
        obj.data.uv_layers.new(name="UVMap")
        print("✓ UV Map erstellt")

    # Zweite UV Map für Projektion
    if "Face_Projection_UV" not in obj.data.uv_layers:
        obj.data.uv_layers.new(name="Face_Projection_UV")
        print("✓ Face_Projection_UV Map erstellt")

    print("\n📋 NÄCHSTE SCHRITTE IN BLENDER:")
    print("="*50)
    print("1. Wechsle in EDIT MODE (Tab)")
    print("2. Wähle die Gesichts-Vertices (Augen, Nase, Mund)")
    print("3. UV Editor öffnen")
    print("4. UV > Project from View (Front)")
    print("5. Referenzbild als Background im UV Editor laden")
    print("6. UVs auf Augen/Nase/Mund ausrichten")
    print("7. Material 'Face_Blend' Fac erhöhen (0→1)")
    print("="*50)

# ============================================================
# SCHRITT 6: Halsband-Basis erstellen
# ============================================================
def create_choker_base(obj):
    """Erstellt eine Basis für Megumin's Halsband"""
    if obj is None:
        return

    # Finde Hals-Position (ungefähr)
    # Bei T-Pose ist der Hals oben in der Mitte

    # Torus als Choker-Basis
    bpy.ops.mesh.primitive_torus_add(
        major_radius=0.08,      # Halsumfang
        minor_radius=0.015,     # Dicke des Bands
        major_segments=48,
        minor_segments=12,
        location=(0, 0, 1.5)    # Ungefähre Hals-Höhe
    )

    choker = bpy.context.active_object
    choker.name = "Najika_Choker_Megumin"

    # Choker Material
    mat = bpy.data.materials.new(name="Choker_Material")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs['Base Color'].default_value = (0.1, 0.1, 0.1, 1)  # Schwarz
    bsdf.inputs['Metallic'].default_value = 0.0
    bsdf.inputs['Roughness'].default_value = 0.3

    choker.data.materials.append(mat)

    print("✓ Choker-Basis erstellt: 'Najika_Choker_Megumin'")
    print("  → Position und Größe manuell anpassen!")
    print("  → Megumin's Choker hat gelbe Verzierung - muss modelliert werden")

# ============================================================
# MAIN - Alles ausführen
# ============================================================
def main():
    print("\n" + "="*60)
    print("🎀 NAJIKA FACE PROJECTION TOOL")
    print("="*60 + "\n")

    # Scene vorbereiten (auskommentiert - manuell aktivieren)
    # clear_scene()

    # Model importieren
    najika = import_model()

    if najika:
        # Face Vertex Group
        create_face_vertex_group(najika)

        # Material Setup
        setup_projection_material(najika)

        # UV Projection
        setup_uv_projection(najika)

        # Choker erstellen
        create_choker_base(najika)

        print("\n" + "="*60)
        print("✅ SETUP ABGESCHLOSSEN!")
        print("="*60)
        print("\n⚠ WICHTIG: Speichere das Referenzbild hier:")
        print(f"   {REFERENCE_IMAGE}")
        print("\nDann folge den Schritten oben für die UV-Projektion.")
    else:
        print("❌ Konnte Model nicht laden!")

# Script ausführen
if __name__ == "__main__":
    main()
