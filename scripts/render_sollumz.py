"""Render the diagnostic Sollumz import in its native GTA coordinate system."""
import json
from pathlib import Path
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
for obj in list(bpy.data.objects):
    if obj.type in {"LIGHT", "CAMERA"}:
        bpy.data.objects.remove(obj, do_unlink=True)

for obj in bpy.data.objects:
    if obj.type == "MESH" and not obj.hide_render and not obj.name.endswith(".col"):
        for mat in obj.data.materials:
            if mat is None:
                continue
            mat.use_nodes = True
            bs = mat.node_tree.nodes.get("Principled BSDF")
            if bs:
                bs.inputs["Base Color"].default_value = (0.08, 0.18, 0.27, 1.0)
                bs.inputs["Metallic"].default_value = 0.45
                bs.inputs["Roughness"].default_value = 0.28

bpy.ops.mesh.primitive_plane_add(size=200, location=(0, 0, -0.55))
floor = bpy.context.object
floor_mat = bpy.data.materials.new("diagnostic_floor")
floor_mat.diffuse_color = (0.08, 0.09, 0.11, 1)
floor.data.materials.append(floor_mat)

for loc, power, size in [((-3, 4, 7), 1800, 6), ((4, -3, 5), 1600, 5), ((0, 0, 7), 1400, 4)]:
    bpy.ops.object.light_add(type="AREA", location=loc)
    light = bpy.context.object
    light.data.energy = power
    light.data.shape = "DISK"
    light.data.size = size
    light.rotation_euler = (Vector((0, 0, 0.2)) - light.location).to_track_quat("-Z", "Y").to_euler()

bpy.ops.object.camera_add(location=(-5, 6, 3))
camera = bpy.context.object
camera.rotation_euler = (Vector((0, 0, 0.2)) - camera.location).to_track_quat("-Z", "Y").to_euler()
camera.data.type = "ORTHO"
camera.data.ortho_scale = 6.0

scene = bpy.context.scene
scene.camera = camera
scene.render.engine = "BLENDER_EEVEE_NEXT"
scene.render.resolution_x = 1200
scene.render.resolution_y = 800
scene.render.resolution_percentage = 100
scene.world.color = (0.2, 0.2, 0.2)
scene.view_settings.view_transform = "AgX"
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = str(ROOT / "preview/source-sollumz-perspective.png")
bpy.ops.render.render(write_still=True)
print("SOLLUMZ_RENDER_READY")
