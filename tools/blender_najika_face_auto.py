# ============================================================
# NAJIKA FACE AUTO-PROJECTION - Blender Script
# ============================================================
# Automatisiert alles AUSSER die Gesichts-Auswahl
#
# ANLEITUNG:
# 1. Script ausführen (Alt+P)
# 2. Im Edit Mode: Gesicht auswählen (Augen, Nase, Mund)
# 3. Nochmal Alt+P drücken
# ============================================================

import bpy
import os

REFERENCE_PATH = r"C:\Najika_World\assets\textures\najika_face_reference.png"

def setup_and_project():
    """Hauptfunktion - erkennt automatisch was zu tun ist"""

    obj = bpy.context.active_object

    # Prüfe ob wir ein Mesh haben
    if obj is None or obj.type != 'MESH':
        print("❌ Kein Mesh ausgewählt! Wähle Najika_Body aus.")
        return

    # Prüfe ob wir im Edit Mode sind
    if bpy.context.mode == 'EDIT_MESH':
        # Prüfe ob Vertices ausgewählt sind
        bpy.ops.object.mode_set(mode='OBJECT')
        selected_verts = [v for v in obj.data.vertices if v.select]
        bpy.ops.object.mode_set(mode='EDIT')

        if len(selected_verts) > 50:
            # Genug Vertices ausgewählt - projizieren!
            project_face_uvs()
            setup_material_blend(obj)
            print(f"\n✅ FERTIG! {len(selected_verts)} Vertices projiziert!")
            print("   Schau dir das Ergebnis im 3D View an (Material Preview Mode)")
        else:
            print(f"\n⚠ Nur {len(selected_verts)} Vertices ausgewählt.")
            print("   Wähle mehr aus (Augen, Nase, Mund-Bereich)")
            print("   Dann nochmal Alt+P")
    else:
        # Noch nicht im Edit Mode - Setup machen
        initial_setup(obj)

def initial_setup(obj):
    """Erstes Setup - bereitet alles vor"""
    print("\n" + "="*50)
    print("🎀 NAJIKA FACE AUTO-PROJECTION")
    print("="*50)

    # UV Map erstellen falls nicht vorhanden
    if "Face_UV" not in obj.data.uv_layers:
        obj.data.uv_layers.new(name="Face_UV")
        print("✓ Face_UV Map erstellt")

    # Material vorbereiten
    setup_base_material(obj)

    # In Edit Mode wechseln
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')

    # Frontalansicht
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for region in area.regions:
                if region.type == 'WINDOW':
                    override = {'area': area, 'region': region}
                    bpy.ops.view3d.view_axis(override, type='FRONT')
                    break

    print("\n📋 JETZT:")
    print("   1. Wähle Gesichts-Vertices (Augen, Nase, Mund)")
    print("      → B = Box Select")
    print("      → C = Circle Select")
    print("      → Shift+Klick = Zur Auswahl hinzufügen")
    print("   2. Dann nochmal Alt+P drücken!")
    print("="*50)

def setup_base_material(obj):
    """Erstellt das Blend-Material"""
    mat_name = "Najika_Face_Blend"

    if mat_name in bpy.data.materials:
        mat = bpy.data.materials[mat_name]
    else:
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (600, 0)

    # BSDF mit SSS für Haut
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (300, 0)
    bsdf.inputs['Subsurface Weight'].default_value = 0.3
    bsdf.inputs['Subsurface Radius'].default_value = (1.0, 0.2, 0.1)
    bsdf.inputs['Roughness'].default_value = 0.4

    # Original Textur
    tex_orig = nodes.new('ShaderNodeTexImage')
    tex_orig.location = (-400, 200)
    tex_orig.label = "Original"

    # Suche existierende Textur
    for img in bpy.data.images:
        if "texture" in img.name.lower():
            tex_orig.image = img
            print(f"✓ Original Textur: {img.name}")
            break

    # Referenz Textur
    tex_ref = nodes.new('ShaderNodeTexImage')
    tex_ref.location = (-400, -100)
    tex_ref.label = "Face_Reference"

    if os.path.exists(REFERENCE_PATH):
        img = bpy.data.images.load(REFERENCE_PATH)
        tex_ref.image = img
        print(f"✓ Referenz geladen: {REFERENCE_PATH}")
    else:
        print(f"❌ Referenz nicht gefunden: {REFERENCE_PATH}")
        return

    # UV Maps
    uv_orig = nodes.new('ShaderNodeUVMap')
    uv_orig.location = (-600, 200)
    uv_orig.uv_map = "UVMap"

    uv_face = nodes.new('ShaderNodeUVMap')
    uv_face.location = (-600, -100)
    uv_face.uv_map = "Face_UV"

    # Mix Node
    mix = nodes.new('ShaderNodeMixRGB')
    mix.location = (0, 100)
    mix.blend_type = 'MIX'
    mix.inputs['Fac'].default_value = 0.7  # 70% Referenz
    mix.label = "FACE_BLEND"

    # Verbindungen
    links.new(uv_orig.outputs['UV'], tex_orig.inputs['Vector'])
    links.new(uv_face.outputs['UV'], tex_ref.inputs['Vector'])
    links.new(tex_orig.outputs['Color'], mix.inputs['Color1'])
    links.new(tex_ref.outputs['Color'], mix.inputs['Color2'])
    links.new(mix.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    # Material zuweisen
    if len(obj.data.materials) == 0:
        obj.data.materials.append(mat)
    else:
        obj.data.materials[0] = mat

    print("✓ Material erstellt")

def project_face_uvs():
    """Projiziert UVs für ausgewählte Vertices"""

    # Face_UV aktivieren
    obj = bpy.context.active_object
    if "Face_UV" in obj.data.uv_layers:
        obj.data.uv_layers["Face_UV"].active = True

    # Project from View (Front)
    bpy.ops.uv.project_from_view(
        camera_bounds=False,
        correct_aspect=True,
        scale_to_bounds=True
    )

    print("✓ UVs projiziert (Project from View)")

def setup_material_blend(obj):
    """Aktiviert das Blending im Material"""

    mat_name = "Najika_Face_Blend"
    if mat_name not in bpy.data.materials:
        return

    mat = bpy.data.materials[mat_name]

    # Finde Mix Node und setze Blend
    for node in mat.node_tree.nodes:
        if node.label == "FACE_BLEND":
            node.inputs['Fac'].default_value = 0.7
            print("✓ Face Blend auf 70% gesetzt")
            break

    # Wechsle zu Material Preview
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'MATERIAL'
                    break

# ============================================================
# SCRIPT AUSFÜHREN
# ============================================================
setup_and_project()
