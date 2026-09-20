"""Render geometry read back from the release BIN, using DDS textures read back from its TPK."""
import bpy
import json
import numpy as np
import os
from pathlib import Path
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'work/compiled-geometry.json').read_text())
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
materials={}

def material(shader,texture):
    key=(shader,texture)
    if key in materials:return materials[key]
    mat=bpy.data.materials.new(f'{shader:08X}_{texture:08X}');mat.use_nodes=True
    mat['mw_shader_hash']=f'{shader:08X}';mat['mw_texture_hash']=f'{texture:08X}'
    bs=mat.node_tree.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.42
    path=ROOT/'work/compiled-textures'/f'{texture:08X}.dds'
    if path.exists():
        node=mat.node_tree.nodes.new('ShaderNodeTexImage');node.image=bpy.data.images.load(str(path),check_existing=True)
        mat.node_tree.links.new(node.outputs['Color'],bs.inputs['Base Color'])
    else:bs.inputs['Base Color'].default_value=(.10,.10,.10,1)
    if shader==0xD6D6080A:
        for l in list(bs.inputs['Base Color'].links):mat.node_tree.links.remove(l)
        bs.inputs['Base Color'].default_value=(.025,.045,.07,1)
        bs.inputs['Metallic'].default_value=.65;bs.inputs['Roughness'].default_value=.28
    elif shader==0x54949AFD:bs.inputs['Metallic'].default_value=.9;bs.inputs['Roughness'].default_value=.23
    elif shader==0x471A1DCA:
        for l in list(bs.inputs['Base Color'].links):mat.node_tree.links.remove(l)
        bs.inputs['Base Color'].default_value=(.035,.045,.055,1)
        bs.inputs['Transmission Weight'].default_value=.9;bs.inputs['Roughness'].default_value=.1
    elif shader in (0xA6348EE3,0xD79597D6):
        bs.inputs['Roughness'].default_value=.15;bs.inputs['Metallic'].default_value=.25
    materials[key]=mat;return mat

def add_part(part,translation=(0,0,0),rotate=False,preview_only=False):
    verts=part['mesh']['Vertices'];info=part['info'];offset=0
    for gi,g in enumerate(part['mesh']['Groups']):
        count=g['TriangleCount']*3
        indices=np.array(part['mesh']['Indices'][offset:offset+count],dtype=int).reshape(-1,3);offset+=count
        if not len(indices):continue
        used,inverse=np.unique(indices,return_inverse=True)
        pos=np.array([[verts[i]['Position'][k] for k in 'xyz'] for i in used])
        norm=np.array([[verts[i]['Normal'][k] for k in 'xyz'] for i in used])
        uv=np.array([[verts[i]['UV']['u'],1-verts[i]['UV']['v']] for i in used])
        if rotate:pos[:,:2]*=-1;norm[:,:2]*=-1
        pos+=translation
        mesh=bpy.data.meshes.new(part['name']+f'_{gi}');mesh.from_pydata(pos.tolist(),[],inverse.reshape(-1,3).tolist());mesh.update()
        mesh.polygons.foreach_set('use_smooth',[True]*len(mesh.polygons))
        # Blender 4.5.14 can crash natively when this API receives some
        # compiled MW meshes.  The imported topology remains smooth-shaded;
        # use its calculated normals for the offline preview.
        layer=mesh.uv_layers.new(name='UVMap')
        for loop in mesh.loops:layer.data[loop.index].uv=uv[loop.vertex_index]
        mat=material(info['Shaders'][g['ShaderIndex0']],info['Textures'][g['TextureIndex0']]);mesh.materials.append(mat)
        obj=bpy.data.objects.new(mesh.name,mesh);bpy.context.collection.objects.link(obj)
        obj['mw_part']=part['name'];obj['preview_only']=preview_only
        hidden=not part['name'].endswith('_A') or '_KIT01_' in part['name'] or '_KIT02_' in part['name']
        if not preview_only and ('_TIRE_' in part['name'] or '_BRAKE_' in part['name']):hidden=True
        obj.hide_render=hidden;obj.hide_viewport=hidden

for p in data:
    add_part(p)
tire=next(p for p in data if p['name']=='FORDGT_KIT00_FRONT_TIRE_A')
for x in (1.425,-1.305):
    for y in (.895,-.895):add_part(tire,(x,y,0),y>0,True)

scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=48;scene.cycles.use_denoising=True
try:
    prefs=bpy.context.preferences.addons['cycles'].preferences
    for backend in ('OPTIX','CUDA'):
        try:
            prefs.compute_device_type=backend;prefs.get_devices();break
        except Exception:
            pass
    gpu=[]
    selected=prefs.compute_device_type
    for device in prefs.devices:
        device.use=(device.type==selected)
        if device.use:gpu.append(device.name)
    if gpu:scene.cycles.device='GPU'
except Exception:
    pass
scene.render.resolution_x=1200;scene.render.resolution_y=800;scene.render.resolution_percentage=100
scene.world.color=(.18,.18,.18)
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.345));floor=bpy.context.object;floor.name='STUDIO_floor'
mat=bpy.data.materials.new('STUDIO_floor');mat.diffuse_color=(.10,.12,.15,1);floor.data.materials.append(mat)
for loc,power,size in [((3,4,7),1500,6),((-4,-3,5),1300,5),((0,-1,7),1000,4)]:
    bpy.ops.object.light_add(type='AREA',location=loc);light=bpy.context.object
    light.data.energy=power;light.data.shape='DISK';light.data.size=size
    light.rotation_euler=(Vector((0,0,.3))-light.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add();camera=bpy.context.object;camera.data.type='ORTHO';scene.camera=camera
scene.view_settings.view_transform='AgX'
views=[('perspective',(6,5,2.8),6.1),('rear',(-6,-5,2.5),6.1),('side',(0,7,1),5.8),('front',(7,0,1),3.7)]
if os.environ.get('MW_QUICK_RENDER')=='1':views=views[:1]
for name,location,scale in views:
    camera.location=location;camera.rotation_euler=(Vector((0,0,.35))-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.ortho_scale=scale
    scene.render.filepath=str(ROOT/'preview'/f'compiled-{name}.png');bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/compiled-preview.blend'))
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/fusion-mw.blend'))
print('COMPILED_PREVIEWS_READY')
