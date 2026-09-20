import bpy
from pathlib import Path
from mathutils import Vector

root=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(root/'blender/compiled-preview.blend'))
colors={'BASE':(1,0,0,1),'INTERIOR':(0,1,0,1),'BODY':(0,0.2,1,1),
        'WINDOW':(0,1,1,1),'HEADLIGHT':(1,1,0,1),'BRAKELIGHT':(1,0,1,1)}
mats={}
for key,color in colors.items():
    mat=bpy.data.materials.new('DIAG_'+key);mat.diffuse_color=color;mat.use_nodes=True
    bs=mat.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=color
    bs.inputs['Emission Color'].default_value=color;bs.inputs['Emission Strength'].default_value=.35
    mats[key]=mat
for o in bpy.data.objects:
    part=o.get('mw_part')
    if not part:continue
    key=next((k for k in ('WINDOW','HEADLIGHT','BRAKELIGHT','INTERIOR','BODY','BASE') if k in part),'BASE')
    o.data.materials.clear();o.data.materials.append(mats[key])
scene=bpy.context.scene;scene.render.engine='BLENDER_EEVEE_NEXT';scene.render.resolution_x=900;scene.render.resolution_y=600;scene.render.resolution_percentage=100
camera=scene.camera
for name,location,scale in [('perspective',(6,5,2.8),6.1),('rear',(-6,-5,2.5),6.1),('side',(0,7,1),5.8)]:
    camera.location=location;camera.rotation_euler=(Vector((0,0,.35))-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.ortho_scale=scale
    scene.render.filepath=str(root/'preview'/f'diagnostic-{name}.png');bpy.ops.render.render(write_still=True)
