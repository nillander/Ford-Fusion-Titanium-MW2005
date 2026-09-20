import json
from pathlib import Path
import numpy as np
from szio.gta5 import try_load_asset, LodLevel

ROOT = Path(__file__).resolve().parents[1]
out = ROOT/'work/source-meshes'
out.mkdir(exist_ok=True)
texdir = ROOT/'work/source-textures'
texdir.mkdir(exist_ok=True)
a = try_load_asset(ROOT/'work/source-extracted/x64/vehicles.extracted/fusion_hi.yft')
d = a.drawable
bones = [{'name':b.name, 'tag':b.tag, 'parent':b.parent_index, 'position':list(b.position),
          'rotation':list(b.rotation), 'scale':list(b.scale)} for b in d.skeleton.bones]
shaders = [{'name':s.name, 'preset':s.preset_filename,
            'textures':{p.name:p.value for p in s.parameters if isinstance(p.value,str)}}
           for s in d.shader_group.shaders]
textures = dict(d.shader_group.embedded_textures)
textures.update(try_load_asset(ROOT/'work/source-extracted/x64/vehicles.extracted/fusion.ytd').textures)
for name,t in textures.items():
    if Path(name).name != name: raise ValueError(name)
    if t.data: (texdir/(name+'.dds')).write_bytes(t.data.read_bytes())
meshes=[]
drawables=[('main',d)]
for path in sorted((ROOT/'work/source-extracted/x64/vehiclemods').rglob('*.yft')):
    drawables.append((path.stem,try_load_asset(path).drawable))
for prefix,draw in drawables:
  textures.update(draw.shader_group.embedded_textures)
  shader_map=[]
  for s in draw.shader_group.shaders:
    record={'name':s.name,'preset':s.preset_filename,'textures':{p.name:p.value for p in s.parameters if isinstance(p.value,str)}}
    if prefix=='main': shader_map.append(len(shader_map))
    else:
      if record not in shaders: shaders.append(record)
      shader_map.append(shaders.index(record))
  for mi,m in enumerate(draw.models.get(LodLevel.HIGH, [])):
    for gi,g in enumerate(m.geometries):
        key=f'{prefix}_m{mi:03d}_g{gi:03d}'
        np.savez_compressed(out/(key+'.npz'), vertices=g.vertex_buffer, indices=g.index_buffer, bone_ids=g.bone_ids)
        v=g.vertex_buffer
        dominant='chassis'
        if m.has_skin and draw.skeleton:
            local=v['BlendIndices'][np.arange(len(v)),v['BlendWeights'].argmax(axis=1)]
            mapped=g.bone_ids[local] if len(g.bone_ids) else local
            dominant=draw.skeleton.bones[int(np.bincount(mapped.astype(int)).argmax())].name
        pos=v['Position']
        meshes.append({'key':key,'origin':prefix,'dominant_bone':dominant,'model':mi,'bone':m.bone_index,'skin':m.has_skin,'shader':shader_map[g.shader_index],
                       'vertices':len(pos),'triangles':len(g.index_buffer)//3,
                       'min':pos.min(axis=0).tolist(),'max':pos.max(axis=0).tolist(),
                       'bone_ids':g.bone_ids.tolist(),'attributes':list(g.vertex_buffer.dtype.names)})
for name,t in textures.items():
    if Path(name).name != name: raise ValueError(name)
    if t.data: (texdir/(name+'.dds')).write_bytes(t.data.read_bytes())
report={'name':a.name,'bones':bones,'shaders':shaders,'meshes':meshes,'texture_names':list(textures),
        'physics_children':len(a.physics.lod1.children) if a.physics else 0}
(ROOT/'reference/source-structure.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('Meshes:',len(meshes),'Vertices:',sum(x['vertices'] for x in meshes),'Triangles:',sum(x['triangles'] for x in meshes))
print('Bones:',len(bones),'Shaders:',len(shaders),'Textures:',len(textures))
for prefix,_ in drawables:
    subset=[x for x in meshes if x['origin']==prefix]
    print(prefix,'triangles',sum(x['triangles'] for x in subset),'bounds',np.min([x['min'] for x in subset],axis=0),np.max([x['max'] for x in subset],axis=0))
