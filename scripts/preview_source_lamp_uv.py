"""Preview the compiled lamp UVs with the texture read back from the TPK."""
import bpy
import json
import numpy as np
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT/'versions/v2-mustang-shelby/work'
OUT=WORK/'source-lamp-bake'
bpy.ops.wm.open_mainfile(filepath=str(OUT/'source-lamp-bake.blend'))
for obj in bpy.data.objects:
    obj.hide_render=True
parts=json.loads((WORK/'fusion-rear-lenses/geometry.json').read_text())
part=next(p for p in parts if p['name']=='MUSTANGGT_BASE_A')
vertices=part['mesh']['Vertices']
mat=bpy.data.materials.new('Compiled opaque atlas')
mat.use_nodes=True
nodes=mat.node_tree.nodes
nodes.clear()
tex=nodes.new('ShaderNodeTexImage')
tex.image=bpy.data.images.load(str(WORK/'fusion-rear-lenses/verified-textures/4B7D95B6.dds'))
em=nodes.new('ShaderNodeEmission')
out=nodes.new('ShaderNodeOutputMaterial')
mat.node_tree.links.new(tex.outputs['Color'],em.inputs['Color'])
mat.node_tree.links.new(em.outputs[0],out.inputs['Surface'])
new=[]
for group in part['mesh']['Groups']:
    if part['info']['Textures'][group['TextureIndex0']]!=0x4B7D95B6:continue
    indices=np.array(part['mesh']['Indices'][group['Offset']:group['Offset']+group['Length']]).reshape(-1,3)
    used,inv=np.unique(indices,return_inverse=True)
    pos=np.array([[vertices[i]['Position'][k] for k in 'xyz'] for i in used])
    if pos[:,1].mean()<0:continue
    mesh=bpy.data.meshes.new('compiled_lamp')
    mesh.from_pydata(pos.tolist(),[],inv.reshape(-1,3).tolist())
    uv=mesh.uv_layers.new()
    for loop in mesh.loops:
        q=vertices[used[loop.vertex_index]]['UV']
        uv.data[loop.index].uv=(q['u'],1-q['v'])
    mesh.materials.append(mat)
    obj=bpy.data.objects.new(mesh.name,mesh)
    bpy.context.collection.objects.link(obj)
    new.append((obj,'front' if pos[:,0].mean()>0 else 'rear'))
scene=bpy.context.scene
scene.view_settings.view_transform='Standard'
scene.cycles.samples=8
for end in ('front','rear'):
    for obj,which in new:obj.hide_render=which!=end
    scene.camera=bpy.data.objects[end+'_bake_camera']
    scene.render.filepath=str(OUT/(end+'-compiled-uv.png'))
    bpy.ops.render.render(write_still=True)
