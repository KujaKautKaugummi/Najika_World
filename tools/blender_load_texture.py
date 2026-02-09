# ============================================================
# LOAD TEXTURE - Lädt die richtige Textur aus dem FBX-Ordner
# ============================================================

import bpy

TEXTURE_PATH = r"C:\Users\0KKK0\Downloads\Meshy_AI__0203173755_texture_fbx\Meshy_AI__0203173755_texture_fbx\Meshy_AI__0203173755_texture.png"

def load_texture():
    print("\n🎨 LADE TEXTUR...")

    obj = bpy.context.active_object

    if obj is None or obj.type != 'MESH':
        for o in bpy.context.scene.objects:
            if o.type == 'MESH' and len(o.data.vertices) > 1000:
                obj = o
                bpy.context.view_layer.objects.active = obj
                obj.select_set(True)
                break

    if obj is None:
        print("❌ Kein Mesh gefunden!")
        return

    print(f"✓ Mesh: {obj.name}")

    # Textur laden
    img = bpy.data.images.load(TEXTURE_PATH)
    print(f"✓ Textur geladen: {img.name}")

    # Material erstellen
    mat = bpy.data.materials.new(name="Najika_Textured")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (600, 0)

    # BSDF mit SSS für menschliche Haut
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (300, 0)
    bsdf.inputs['Subsurface Weight'].default_value = 0.35
    bsdf.inputs['Subsurface Radius'].default_value = (1.0, 0.3, 0.15)
    bsdf.inputs['Roughness'].default_value = 0.4

    # Textur Node
    tex = nodes.new('ShaderNodeTexImage')
    tex.location = (-100, 0)
    tex.image = img

    # Verbinden
    links.new(tex.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    # Material zuweisen
    obj.data.materials.clear()
    obj.data.materials.append(mat)

    # Material Preview Mode
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'MATERIAL'

    print("✅ FERTIG! Textur angewendet mit Human Skin SSS")

load_texture()
