# ============================================================
# NAJIKA EXPORT MIT EINGEBETTETER TEXTUR
# ============================================================
# Textur wird DIREKT in die FBX eingebettet
# ============================================================

import bpy
import os

TEXTURE_PATH = r"C:\Users\0KKK0\Downloads\Meshy_AI__0203173755_texture_fbx\Meshy_AI__0203173755_texture_fbx\Meshy_AI__0203173755_texture.png"
EXPORT_PATH = r"C:\Najika_World\assets\models\najika\najika_embedded_texture.fbx"

def export_with_embedded_texture():
    print("\n" + "="*50)
    print("💾 EXPORT MIT EINGEBETTETER TEXTUR")
    print("="*50)

    obj = None
    armature = None

    # Finde Mesh und Armature
    for o in bpy.context.scene.objects:
        if o.type == 'MESH' and len(o.data.vertices) > 1000:
            obj = o
        elif o.type == 'ARMATURE':
            armature = o

    if obj is None:
        print("❌ Kein Mesh gefunden!")
        return

    print(f"✓ Mesh: {obj.name}")

    # Textur laden falls noch nicht geladen
    img = None
    for image in bpy.data.images:
        if "texture" in image.name.lower() or "meshy" in image.name.lower():
            img = image
            break

    if img is None and os.path.exists(TEXTURE_PATH):
        img = bpy.data.images.load(TEXTURE_PATH)
        print(f"✓ Textur geladen: {img.name}")

    # Material sicherstellen
    if len(obj.data.materials) == 0 or obj.data.materials[0] is None:
        mat = bpy.data.materials.new(name="Najika_Material")
        mat.use_nodes = True
        obj.data.materials.clear()
        obj.data.materials.append(mat)
    else:
        mat = obj.data.materials[0]
        if not mat.use_nodes:
            mat.use_nodes = True

    # Node Tree aufbauen
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Finde oder erstelle BSDF
    bsdf = None
    for node in nodes:
        if node.type == 'BSDF_PRINCIPLED':
            bsdf = node
            break

    if bsdf is None:
        nodes.clear()
        bsdf = nodes.new('ShaderNodeBsdfPrincipled')
        bsdf.location = (300, 0)
        output = nodes.new('ShaderNodeOutputMaterial')
        output.location = (600, 0)
        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    # Textur Node hinzufügen/finden
    tex_node = None
    for node in nodes:
        if node.type == 'TEX_IMAGE':
            tex_node = node
            break

    if tex_node is None:
        tex_node = nodes.new('ShaderNodeTexImage')
        tex_node.location = (-200, 0)

    # Textur zuweisen
    if img:
        tex_node.image = img
        # Verbinden mit Base Color
        links.new(tex_node.outputs['Color'], bsdf.inputs['Base Color'])
        print(f"✓ Textur verbunden: {img.name}")

    # TEXTUR PACKEN (einbetten)
    if img:
        img.pack()
        print("✓ Textur eingepackt (embedded)")

    # Auswahl für Export
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    if armature:
        armature.select_set(True)
    bpy.context.view_layer.objects.active = obj

    # Ordner erstellen
    os.makedirs(os.path.dirname(EXPORT_PATH), exist_ok=True)

    # FBX Export mit eingebetteter Textur
    bpy.ops.export_scene.fbx(
        filepath=EXPORT_PATH,
        use_selection=True,
        path_mode='COPY',           # WICHTIG: Kopiert Texturen
        embed_textures=True,        # WICHTIG: Bettet ein!
        use_mesh_modifiers=True,
        add_leaf_bones=False,
        bake_anim=False,
    )

    print(f"\n✅ EXPORTIERT: {EXPORT_PATH}")
    print("\n📋 Diese FBX hat die Textur EINGEBETTET!")
    print("   Importiere sie in UEFN - sollte mit Textur kommen.")

export_with_embedded_texture()
