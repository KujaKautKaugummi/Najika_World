# ============================================================
# FIX BLACK FACE - Schneller Reset
# ============================================================

import bpy

obj = bpy.context.active_object

if obj and obj.type == 'MESH':
    # Zurück zu Original-Material falls vorhanden
    for mat in bpy.data.materials:
        if "texture" in mat.name.lower() or "material" in mat.name.lower():
            if "Blend" not in mat.name and "Face" not in mat.name:
                obj.data.materials.clear()
                obj.data.materials.append(mat)
                print(f"✓ Original Material wiederhergestellt: {mat.name}")
                break

    # Oder: Blend auf 0 setzen (zeigt nur Original)
    for mat in obj.data.materials:
        if mat.use_nodes:
            for node in mat.node_tree.nodes:
                if "BLEND" in node.label.upper() or "MIX" in node.name.upper():
                    if hasattr(node.inputs.get('Fac'), 'default_value'):
                        node.inputs['Fac'].default_value = 0.0
                        print("✓ Blend auf 0 gesetzt - zeigt Original")

    print("\n💡 Um Face-Blend wieder zu aktivieren:")
    print("   Shader Editor → FACE_BLEND Node → Fac erhöhen (0.3-0.7)")
else:
    print("❌ Wähle erst das Mesh aus!")
