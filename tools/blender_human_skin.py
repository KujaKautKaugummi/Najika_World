# ============================================================
# NAJIKA HUMAN SKIN - Realistische Haut
# ============================================================
# Macht die Haut menschlicher mit SSS (Subsurface Scattering)
# ============================================================

import bpy

def apply_human_skin():
    """Wendet realistischen Haut-Shader an"""

    print("\n" + "="*50)
    print("🎀 NAJIKA HUMAN SKIN SHADER")
    print("="*50)

    obj = bpy.context.active_object

    if obj is None or obj.type != 'MESH':
        # Versuche Najika zu finden
        for o in bpy.context.scene.objects:
            if o.type == 'MESH' and len(o.data.vertices) > 10000:
                obj = o
                bpy.context.view_layer.objects.active = obj
                break

    if obj is None:
        print("❌ Kein Mesh gefunden!")
        return

    print(f"✓ Mesh: {obj.name}")

    # Material erstellen
    mat_name = "Najika_Human_Skin"

    if mat_name in bpy.data.materials:
        mat = bpy.data.materials[mat_name]
        mat.node_tree.nodes.clear()
    else:
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        mat.node_tree.nodes.clear()

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # === OUTPUT ===
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (800, 0)

    # === PRINCIPLED BSDF (Haupt-Shader) ===
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (500, 0)

    # SSS für menschliche Haut
    bsdf.inputs['Subsurface Weight'].default_value = 0.4
    bsdf.inputs['Subsurface Radius'].default_value = (1.0, 0.35, 0.2)  # Rot/Orange durchscheinen
    bsdf.inputs['Subsurface Scale'].default_value = 0.1

    # Haut-Oberfläche
    bsdf.inputs['Roughness'].default_value = 0.45
    bsdf.inputs['Specular IOR Level'].default_value = 0.4
    bsdf.inputs['Coat Weight'].default_value = 0.1  # Leichter Glanz
    bsdf.inputs['Coat Roughness'].default_value = 0.3

    # === ORIGINAL TEXTUR ===
    tex_color = nodes.new('ShaderNodeTexImage')
    tex_color.location = (-300, 200)
    tex_color.label = "Skin_Color"

    # Suche Original-Textur
    original_tex = None
    for img in bpy.data.images:
        if "texture" in img.name.lower() or "base" in img.name.lower() or "color" in img.name.lower():
            original_tex = img
            tex_color.image = img
            print(f"✓ Textur gefunden: {img.name}")
            break

    if original_tex is None:
        print("⚠ Keine Textur gefunden - verwende Hautfarbe")
        # Fallback: Hautfarbe
        bsdf.inputs['Base Color'].default_value = (0.9, 0.75, 0.65, 1.0)

    # === COLOR CORRECTION für wärmere Haut ===
    hue_sat = nodes.new('ShaderNodeHueSaturation')
    hue_sat.location = (100, 200)
    hue_sat.inputs['Hue'].default_value = 0.5
    hue_sat.inputs['Saturation'].default_value = 1.1  # Etwas mehr Sättigung
    hue_sat.inputs['Value'].default_value = 1.05  # Etwas heller

    # === UV MAP ===
    uv_map = nodes.new('ShaderNodeUVMap')
    uv_map.location = (-500, 200)
    uv_map.uv_map = "UVMap"

    # === VERBINDUNGEN ===
    if original_tex:
        links.new(uv_map.outputs['UV'], tex_color.inputs['Vector'])
        links.new(tex_color.outputs['Color'], hue_sat.inputs['Color'])
        links.new(hue_sat.outputs['Color'], bsdf.inputs['Base Color'])
        links.new(tex_color.outputs['Color'], bsdf.inputs['Subsurface Radius'])

    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    # === MATERIAL ZUWEISEN ===
    obj.data.materials.clear()
    obj.data.materials.append(mat)

    # === VIEWPORT auf Material Preview ===
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'MATERIAL'
                    break

    print("\n✅ HUMAN SKIN SHADER ANGEWENDET!")
    print("="*50)
    print("\n📋 Einstellungen (im Shader Editor anpassbar):")
    print("   • Subsurface Weight: 0.4 (Licht-Durchlass)")
    print("   • Subsurface Radius: Rot/Orange (Blut-Simulation)")
    print("   • Roughness: 0.45 (Haut-Oberfläche)")
    print("   • Coat: 0.1 (Leichter Glanz)")
    print("\n💡 Für Render: Cycles verwenden (Eevee zeigt SSS schlechter)")

# Ausführen
apply_human_skin()
