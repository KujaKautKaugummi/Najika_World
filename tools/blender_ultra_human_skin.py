# ============================================================
# ULTRA HUMAN SKIN - Maximale Realismus für Haut & Haare
# ============================================================

import bpy

TEXTURE_PATH = r"C:\Users\0KKK0\Downloads\Meshy_AI__0203173755_texture_fbx\Meshy_AI__0203173755_texture_fbx\Meshy_AI__0203173755_texture.png"

def create_ultra_human_skin():
    print("\n" + "="*50)
    print("🎀 ULTRA HUMAN SKIN + HAIR")
    print("="*50)

    obj = bpy.context.active_object

    if obj is None or obj.type != 'MESH':
        for o in bpy.context.scene.objects:
            if o.type == 'MESH' and len(o.data.vertices) > 1000:
                obj = o
                bpy.context.view_layer.objects.active = obj
                obj.select_set(True)
                break

    if obj is None:
        print("❌ Kein Mesh!")
        return

    print(f"✓ Mesh: {obj.name}")

    # Textur laden
    img = bpy.data.images.load(TEXTURE_PATH)
    print(f"✓ Textur: {img.name}")

    # ==========================================
    # MATERIAL ERSTELLEN
    # ==========================================
    mat = bpy.data.materials.new(name="Najika_UltraHuman")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # === OUTPUT ===
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (1200, 0)

    # === PRINCIPLED BSDF - ULTRA SKIN ===
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (800, 0)

    # SUBSURFACE SCATTERING (Licht durch Haut)
    bsdf.inputs['Subsurface Weight'].default_value = 0.5  # Mehr SSS!
    bsdf.inputs['Subsurface Radius'].default_value = (1.0, 0.4, 0.25)  # Stärker rot/orange
    bsdf.inputs['Subsurface Scale'].default_value = 0.15

    # HAUT-OBERFLÄCHE
    bsdf.inputs['Roughness'].default_value = 0.35  # Etwas glatter
    bsdf.inputs['Specular IOR Level'].default_value = 0.5  # Mehr Reflexion

    # COAT (Hautglanz/Öl-Schicht)
    bsdf.inputs['Coat Weight'].default_value = 0.15
    bsdf.inputs['Coat Roughness'].default_value = 0.2

    # SHEEN (Feine Härchen auf Haut)
    bsdf.inputs['Sheen Weight'].default_value = 0.05
    bsdf.inputs['Sheen Roughness'].default_value = 0.5

    # === TEXTUR ===
    tex = nodes.new('ShaderNodeTexImage')
    tex.location = (-200, 200)
    tex.image = img

    # === FARB-KORREKTUR (wärmere Hauttöne) ===
    hue_sat = nodes.new('ShaderNodeHueSaturation')
    hue_sat.location = (200, 200)
    hue_sat.inputs['Hue'].default_value = 0.5
    hue_sat.inputs['Saturation'].default_value = 1.15  # Mehr Farbe
    hue_sat.inputs['Value'].default_value = 1.05  # Etwas heller

    # === GAMMA für natürlichere Hauttöne ===
    gamma = nodes.new('ShaderNodeGamma')
    gamma.location = (400, 200)
    gamma.inputs['Gamma'].default_value = 1.1  # Wärmer

    # === RGB CURVES für Hauttöne ===
    curves = nodes.new('ShaderNodeRGBCurve')
    curves.location = (600, 200)
    # Rot leicht anheben für lebendige Haut
    curves.mapping.curves[0].points[1].location = (1.0, 1.05)
    # Grün minimal
    curves.mapping.curves[1].points[1].location = (1.0, 1.0)
    # Blau leicht senken (wärmer)
    curves.mapping.curves[2].points[1].location = (1.0, 0.95)
    curves.mapping.update()

    # === SUBSURFACE COLOR (Blut unter Haut) ===
    sss_color = nodes.new('ShaderNodeRGB')
    sss_color.location = (400, -100)
    sss_color.outputs[0].default_value = (0.8, 0.2, 0.15, 1.0)  # Rötlich

    # === VERBINDUNGEN ===
    links.new(tex.outputs['Color'], hue_sat.inputs['Color'])
    links.new(hue_sat.outputs['Color'], gamma.inputs['Color'])
    links.new(gamma.outputs['Color'], curves.inputs['Color'])
    links.new(curves.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(sss_color.outputs['Color'], bsdf.inputs['Subsurface Radius'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    # === MATERIAL ZUWEISEN ===
    obj.data.materials.clear()
    obj.data.materials.append(mat)

    # === VIEWPORT SETTINGS ===
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'MATERIAL'
                    # Bessere Preview
                    space.shading.use_scene_lights = True
                    space.shading.use_scene_world = False
                    space.shading.studio_light = 'studio.exr'

    print("\n✅ ULTRA HUMAN SKIN ANGEWENDET!")
    print("="*50)
    print("\n📋 Features:")
    print("   • Starkes SSS (Licht durch Haut)")
    print("   • Rötlicher Unterton (Blut)")
    print("   • Coat Layer (Hautglanz)")
    print("   • Sheen (feine Härchen)")
    print("   • Wärmere Farbtöne")
    print("\n💡 TIPP: Für beste Qualität:")
    print("   → Render Engine: Cycles")
    print("   → View: Rendered Mode (Z → 8)")
    print("\n⚠️ HAARE: Mesh-Haare können nicht realistischer")
    print("   werden ohne Particle Hair System!")
    print("   Das muss manuell in Blender gemacht werden.")

create_ultra_human_skin()
