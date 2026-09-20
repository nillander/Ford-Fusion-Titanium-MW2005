"""Create a source scene aligned to the donor wheel centres, with inspectable materials."""
import bpy
import json
import os
import numpy as np
from pathlib import Path
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[1]
default_origins={'main','fusion_exh_2','fusion_rfst','fusion_rollcage'}
selected_origins={name.strip() for name in os.environ.get(
    'FUSION_SOURCE_ORIGINS', ','.join(sorted(default_origins))).split(',') if name.strip()}
origin_label='-'.join(sorted(selected_origins))
src=json.loads((ROOT/'reference/source-structure.json').read_text())
donor=json.loads((ROOT/'work/donor-geometry.json').read_text())
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
for dirname in ('blender','preview','work/processed'):
    (ROOT/dirname).mkdir(exist_ok=True)

# GTA +Y forward/-X left -> MW +X forward/+Y left. Fit axle spacing, preserve donor attributes.
front=src['bones'][43]['position']; rear=src['bones'][48]['position']
sx=(1.425+1.305)/(front[1]-rear[1])
tx=1.425-front[1]*sx
sy=1.0
# The donor wheel centres are at Z=0. The source floor/skirts were aligned to
# the tyre contact patch, which left the body visibly sunk into the road.
body_clearance=0.15
tz=-(front[2]+rear[2])/2+body_clearance
alignment={'longitudinal_scale':sx,'lateral_scale':sy,'vertical_scale':1.0,
           'forward_offset':tx,'vertical_offset':tz,'donor_wheels':[[1.425,.895,0],[-1.305,.895,0]],
           'body_clearance':body_clearance,
           'note':'Wheel centres fitted to donor TireOffsets; source body raised 0.15 m; donor performance files preserved.'}
(ROOT/'reference/alignment.json').write_text(json.dumps(alignment,indent=2))

mats=[]
for i,s in enumerate(src['shaders']):
    mat=bpy.data.materials.new(f'GTA_{i:02d}_{s["preset"]}'); mat.use_nodes=True
    bs=mat.node_tree.nodes.get('Principled BSDF')
    tex=s['textures'].get('diffusesampler','')
    mat['source_shader']=i; mat['source_texture']=tex
    path=ROOT/'work/source-textures'/f'{tex}.dds'
    if path.exists():
        node=mat.node_tree.nodes.new('ShaderNodeTexImage'); node.image=bpy.data.images.load(str(path))
        mat.node_tree.links.new(node.outputs['Color'],bs.inputs['Base Color'])
    else:
        bs.inputs['Base Color'].default_value=(.015,.017,.019,1) if tex=='black' else (.4,.4,.4,1)
    bs.inputs['Roughness'].default_value=.38
    if i==5:
        for l in list(bs.inputs['Base Color'].links): mat.node_tree.links.remove(l)
        bs.inputs['Base Color'].default_value=(.035,.055,.085,1)
        bs.inputs['Metallic'].default_value=.75; bs.inputs['Roughness'].default_value=.2
    if i in (7,8,13,17,19):
        bs.inputs['Metallic'].default_value=.85; bs.inputs['Roughness'].default_value=.18
    if i==16:
        for l in list(bs.inputs['Base Color'].links): mat.node_tree.links.remove(l)
        bs.inputs['Base Color'].default_value=(.03,.04,.055,1)
        bs.inputs['Transmission Weight'].default_value=.92
        bs.inputs['Roughness'].default_value=.08
        bs.inputs['IOR'].default_value=1.45
    mats.append(mat)

for item in src['meshes']:
    # This GTA package distributes the complete stock appearance over the main
    # drawable plus its three vehiclemods drawables. Together they supply the
    # exterior shell, roof, glazing, lighting and exhaust visible in-game.
    if item.get('origin') not in selected_origins:
        continue
    arr=np.load(ROOT/'work/source-meshes'/f'{item["key"]}.npz')
    v=arr['vertices']; p=v['Position'].copy(); n=v['Normal'].copy()
    # Vertices are already in bind/model space; applying bone translations again would disassemble the car.
    p=np.column_stack((p[:,1]*sx+tx,-p[:,0]*sy,p[:,2]+tz))
    n=np.column_stack((n[:,1]/sx,-n[:,0]/sy,n[:,2])); n/=np.maximum(np.linalg.norm(n,axis=1)[:,None],1e-8)
    f=arr['indices'].reshape(-1,3)
    mesh=bpy.data.meshes.new(item['key']); mesh.from_pydata(p.tolist(),[],f.tolist()); mesh.update()
    mesh.polygons.foreach_set('use_smooth',[True]*len(mesh.polygons))
    mesh.normals_split_custom_set_from_vertices(n.tolist())
    uv=mesh.uv_layers.new(name='UVMap')
    for poly in mesh.polygons:
        for li in poly.loop_indices:
            t=v['TexCoord0'][mesh.loops[li].vertex_index]; uv.data[li].uv=(float(t[0]),1-float(t[1]))
    obj=bpy.data.objects.new(item['key'],mesh); bpy.context.collection.objects.link(obj)
    mesh.materials.append(mats[item['shader']]); obj['source_shader']=item['shader']; obj['source_key']=item['key']
    obj['dominant_bone']=item['dominant_bone']

# Donor tire vertices are already in metres; TireOffsets attachment is at the wheel face.
tire=next(p for p in donor if p['name']=='MUSTANGGT_KIT00_FRONT_TIRE_A')
rubber=bpy.data.materials.new('DONOR_tire_preview'); rubber.diffuse_color=(.025,.025,.025,1)
for x in (1.425,-1.305):
    for y in (.895,-.895):
        verts=[[v['Position'][k] for k in ('x','y','z')] for v in tire['mesh']['Vertices']]
        faces=np.array(tire['mesh']['Indices']).reshape(-1,3).tolist()
        mesh=bpy.data.meshes.new('donor_tire'); mesh.from_pydata(verts,[],faces); mesh.materials.append(rubber)
        obj=bpy.data.objects.new('PREVIEW_donor_tire',mesh); bpy.context.collection.objects.link(obj); obj.location=(x,y,0)
        if y>0: obj.rotation_euler.z=3.14159265
        obj['preview_only']=True

scene=bpy.context.scene
scene.render.engine='CYCLES'; scene.cycles.samples=24
try:
    prefs=bpy.context.preferences.addons['cycles'].preferences
    selected=None
    for backend in ('OPTIX','CUDA'):
        try:
            prefs.compute_device_type=backend;prefs.get_devices();selected=backend;break
        except Exception:
            pass
    gpu=[]
    for device in prefs.devices:
        device.use=(device.type==selected)
        if device.use:gpu.append(device.name)
    if gpu:
        scene.cycles.device='GPU'
    (ROOT/'reference/gpu-render.json').write_text(json.dumps({'backend':selected if gpu else 'CPU','devices':gpu},indent=2))
except Exception as exc:
    (ROOT/'reference/gpu-render.json').write_text(json.dumps({'backend':'CPU','devices':[],'error':str(exc)},indent=2))
scene.render.resolution_x=1200; scene.render.resolution_y=800; scene.render.resolution_percentage=100
scene.world.color=(.22,.22,.22)
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.345))
floor=bpy.context.object; floor.name='PREVIEW_floor'; floor['preview_only']=True
mat=bpy.data.materials.new('floor'); mat.diffuse_color=(.11,.13,.16,1); floor.data.materials.append(mat)
for loc,power,size in [((3,4,7),1800,6),((-4,-3,5),1600,5),((0,-1,7),1400,4)]:
    bpy.ops.object.light_add(type='AREA',location=loc); light=bpy.context.object
    light.data.energy=power; light.data.shape='DISK'; light.data.size=size
    light.rotation_euler=(Vector((0,0,.3))-light.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(6,5,3.0)); camera=bpy.context.object
camera.rotation_euler=(Vector((0,0,.35))-camera.location).to_track_quat('-Z','Y').to_euler()
camera.data.type='ORTHO'; camera.data.ortho_scale=6.1; scene.camera=camera
scene.view_settings.view_transform='AgX'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender'/('source-aligned.blend' if selected_origins==default_origins else f'source-aligned-{origin_label}.blend')))
if not os.environ.get('MW_SKIP_RENDER'):
    scene.render.filepath=str(ROOT/'preview'/('source-perspective.png' if selected_origins==default_origins else f'source-{origin_label}-perspective.png')); bpy.ops.render.render(write_still=True)
print('SOURCE_SCENE_READY')
