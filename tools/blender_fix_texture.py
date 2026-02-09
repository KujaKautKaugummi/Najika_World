# ============================================================
# FIX TEXTURE - Findet und verknüpft die Original-Textur
# ============================================================

import bpy
import os

def fix_texture():
    print("\n" + "="*50)
    print("🔧 TEXTURE FIX")
    print("="*50)

    obj = bpy.context.active_object

    if obj is None or obj.type != 'MESH':
        for o in bpy.context.scene.objects:
            if o.type == 'MESH' and len(o.data.vertices) > 10000:
                obj = o
                bpy.context.view_layer.objects.active = obj
                break

    if obj is None:
        print("❌ Kein Mesh!")
        return

    # Zeige alle geladenen Bilder
    print("\n📷 Geladene Bilder:")
    for img in bpy.data.images:
        print(f"   • {img.name}")

    # Zeige alle Materialien
    print("\n🎨 Materialien am Objekt:")
    for mat in obj.data.materials:
        print(f"   • {mat.name}")

    # Suche Textur
    texture = None
    for img in bpy.data.images:
        name_lower = img.name.lower()
        if any(x in name_lower for x in ['texture', 'base', 'color', 'diffuse', 'albedo']):
            texture = img
            print(f"\n✓ Textur gefunden: {img.name}")
            break

    if texture is None:
        # Keine Textur gefunden - vielleicht muss sie neu geladen werden
        print("\n⚠ Keine Textur gefunden!")
        print("   Versuche aus GLB-Ordner zu laden...")

        # Suche im Download-Ordner
        glb_folder = r"C:\Users\0KKK0\Downloads"
        for f in os.listdir(glb_folder):
            if "meshy" in f.lower() and (f.endswith('.png') or f.endswith('.jpg')):
                tex_path = os.path.join(glb_folder, f)
                texture = bpy.data.images.load(tex_path)
                print(f"✓ Textur geladen: {tex_path}")
                break

    if texture is None:
        print("\n❌ Keine Textur gefunden!")
        print("   Exportiere die Textur aus Meshy separat als PNG/JPG")
        return

    # Material mit Textur erstellen
    mat_name = "Najika_Skin_Textured"

    if mat_name in bpy.data.materials:
        mat = bpy.data.materials[mat_name]
        mat.node_tree.nodes.clear()
    else:
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        mat.node_tree.nodes.clear()

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (600, 0)

    # BSDF mit SSS
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (300, 0)
    bsdf.inputs['Subsurface Weight'].default_value = 0.35
    bsdf.inputs['Subsurface Radius'].default_value = (1.0, 0.3, 0.2)
    bsdf.inputs['Roughness'].default_value = 0.4

    # Textur Node
    tex_node = nodes.new('ShaderNodeTexImage')
    tex_node.location = (-200, 0)
    tex_node.image = texture

    # Verbinden
    links.new(tex_node.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    # Zuweisen
    obj.data.materials.clear()
    obj.data.materials.append(mat)

    # Material Preview
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'MATERIAL'

    print("\n✅ TEXTUR VERKNÜPFT!")
    print("   Sollte jetzt farbig sein.")

fix_texture()
