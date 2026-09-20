import bpy
import json
import numpy as np
from pathlib import Path
from mathutils import Vector

root=Path(__file__).resolve().parents[1]
data=json.loads((root/'work/nascar-geometry.json').read_text())
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
part=next(p for p in data if p['name']=='SUPRA_KIT00_BODY_A')
verts=part['mesh']['Vertices'];idx=np.array(part['mesh']['Indices'],dtype=int).reshape(-1,3)
used,inverse=np.unique(idx,return_inverse=True)
pos=np.array([[verts[i]['Position'][k] for k in 'xyz'] for i in used])
mesh=bpy.data.meshes.new('nascar_body');mesh.from_pydata(pos.tolist(),[],inverse.reshape(-1,3).tolist());mesh.update()
mesh.polygons.foreach_set('use_smooth',[True]*len(mesh.polygons))
mat=bpy.data.materials.new('nascar_chrome');mat.diffuse_color=(.38,.42,.46,1);mat.metallic=.75;mat.roughness=.24
mesh.materials.append(mat);obj=bpy.data.objects.new('nascar_body',mesh);bpy.context.collection.objects.link(obj)
scene=bpy.context.scene;scene.render.engine='BLENDER_EEVEE_NEXT';scene.render.resolution_x=1100;scene.render.resolution_y=700;scene.world.color=(.05,.06,.08)
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.36));floor=bpy.context.object;floor.data.materials.append(mat)
for loc in ((3,4,7),(-4,-3,5)):
    bpy.ops.object.light_add(type='AREA',location=loc);light=bpy.context.object;light.data.energy=1200;light.data.shape='DISK';light.data.size=5
    light.rotation_euler=(Vector((0,0,.35))-light.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add();cam=bpy.context.object;cam.data.type='ORTHO';scene.camera=cam
for name,location,scale in [('front',(7,0,1),3.7),('perspective',(6,5,2.8),6.1)]:
    cam.location=location;cam.rotation_euler=(Vector((0,0,.35))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale
    scene.render.filepath=str(root/'preview'/f'nascar-{name}.png');bpy.ops.render.render(write_still=True)
