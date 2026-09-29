import bpy
import math
import os

OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "models"))
os.makedirs(OUTPUT_DIR, exist_ok=True)

def clear_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def create_material(name, base_color, emission_color, emission_strength=0.0, metallic=0.8, roughness=0.2):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = base_color
        bsdf.inputs["Metallic"].default_value = metallic
        bsdf.inputs["Roughness"].default_value = roughness
        if "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = emission_color
            bsdf.inputs["Emission Strength"].default_value = emission_strength
        elif "Emission" in bsdf.inputs:
            bsdf.inputs["Emission"].default_value = emission_color
    return mat

print("=== Building Cosmic Seed Artifact in Blender ===")
clear_scene()

# 1. Inner Crystalline Core (Icosahedron)
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=1.0, location=(0, 0, 0))
core = bpy.context.active_object
core.name = "SeedCore"
mat_core = create_material("CoreGlow", (1.0, 0.85, 0.3, 1.0), (1.0, 0.7, 0.2, 1.0), emission_strength=5.0, metallic=0.1, roughness=0.1)
core.data.materials.append(mat_core)

# 2. Concentric Gyroscope Rings
rings = []
radii = [1.6, 2.2, 2.8]
rotations = [(0, 0, 0), (math.radians(45), math.radians(45), 0), (math.radians(-45), 0, math.radians(45))]
colors = [(0.2, 0.8, 1.0, 1.0), (0.9, 0.6, 1.0, 1.0), (1.0, 0.8, 0.2, 1.0)]

for idx, (r, rot, col) in enumerate(zip(radii, rotations, colors)):
    bpy.ops.mesh.primitive_torus_add(
        major_radius=r,
        minor_radius=0.07,
        major_segments=48,
        minor_segments=12,
        location=(0, 0, 0),
        rotation=rot
    )
    ring = bpy.context.active_object
    ring.name = f"GyroRing_{idx+1}"
    mat_ring = create_material(f"RingMat_{idx+1}", col, col, emission_strength=2.0, metallic=0.9, roughness=0.15)
    ring.data.materials.append(mat_ring)
    rings.append(ring)

# 3. Outer Stellate Geometric Frame
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=0, radius=3.2, location=(0, 0, 0))
outer_cage = bpy.context.active_object
outer_cage.name = "OuterCage"
# Add wireframe modifier to turn it into an intricate lattice cage
wire_mod = outer_cage.modifiers.new(name="Wireframe", type='WIREFRAME')
wire_mod.thickness = 0.08
wire_mod.use_boundary = True
mat_cage = create_material("CageGold", (1.0, 0.75, 0.2, 1.0), (1.0, 0.5, 0.1, 1.0), emission_strength=1.5, metallic=0.95, roughness=0.1)
outer_cage.data.materials.append(mat_cage)

# Export Seed Artifact to GLB
seed_glb_path = os.path.join(OUTPUT_DIR, "seed_artifact.glb")
bpy.ops.export_scene.gltf(
    filepath=seed_glb_path,
    export_format='GLB',
    use_selection=False,
    export_materials='EXPORT',
    export_extras=True
)
print(f"✓ Exported Cosmic Seed to {seed_glb_path}")

print("\n=== Building Alien Monolith Spire in Blender ===")
clear_scene()

# Create towering alien obelisk
bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=1.0, depth=10.0, location=(0, 0, 5.0))
monolith = bpy.context.active_object
monolith.name = "MonolithSpire"

# Bevel modifier for sharp crystalline sci-fi facets
bevel = monolith.modifiers.new(name="Bevel", type='BEVEL')
bevel.width = 0.15
bevel.segments = 2

mat_mono = create_material("MonolithObsidian", (0.05, 0.05, 0.08, 1.0), (0.0, 0.8, 1.0, 1.0), emission_strength=3.0, metallic=0.9, roughness=0.1)
monolith.data.materials.append(mat_mono)

# Floating energy crown on top
bpy.ops.mesh.primitive_torus_add(major_radius=1.8, minor_radius=0.06, location=(0, 0, 10.5))
crown = bpy.context.active_object
crown.name = "EnergyCrown"
mat_crown = create_material("CrownCyan", (0.1, 0.9, 1.0, 1.0), (0.2, 0.95, 1.0, 1.0), emission_strength=8.0, metallic=0.2, roughness=0.05)
crown.data.materials.append(mat_crown)

# Export Monolith Spire to GLB
mono_glb_path = os.path.join(OUTPUT_DIR, "monolith_spire.glb")
bpy.ops.export_scene.gltf(
    filepath=mono_glb_path,
    export_format='GLB',
    use_selection=False,
    export_materials='EXPORT',
    export_extras=True
)
print(f"✓ Exported Monolith Spire to {mono_glb_path}")

print("\nAll 3D models generated successfully!")
