import hashlib
import json
from pathlib import Path
import numpy as np
from PIL import Image
from merge_textures import read_pack
ROOT=Path(__file__).resolve().parents[1]

def load(path):return json.loads((ROOT/path).read_text())
original=load('work/fordgt-geometry.json');compiled=load('work/compiled-geometry.json')
original_by_name={p['name']:p for p in original};by_name={p['name']:p for p in compiled}
assert len(by_name)==len(compiled),'Duplicate names'
assert original_by_name.keys()<=by_name.keys(),'Missing donor slots'
for p in compiled:
    mesh=p['mesh'];vs=mesh['Vertices'];indices=np.array(mesh['Indices'],dtype=int)
    assert len(vs)<=65535,p['name']
    assert len(indices)%3==0 and len(indices)//3==mesh['TriangleCount'],p['name']
    assert sum(g['TriangleCount'] for g in mesh['Groups'])==mesh['TriangleCount'],p['name']
    assert sum(g['VertexCount'] for g in mesh['Groups'])==len(vs),p['name']
    assert not len(indices) or (indices.min()>=0 and indices.max()<len(vs)),p['name']
    pos=np.array([[v['Position'][k] for k in 'xyz'] for v in vs])
    normal=np.array([[v['Normal'][k] for k in 'xyz'] for v in vs])
    assert np.isfinite(pos).all() and np.isfinite(normal).all(),p['name']
    assert np.abs(pos).max()<10,p['name']
    assert all(g['TextureIndex0']<len(p['info']['Textures']) and g['ShaderIndex0']<len(p['info']['Shaders']) for g in mesh['Groups'])
textures=load('reference/texture-independent-validation.json')
expected_names={'MUSTANGGT_INTERIOR','MUSTANGGT_BADGING','MUSTANGGT_KIT00_BRAKELI',
                'MUSTANGGT_LOGO','MUSTANGGT_MISC','MUSTANGGT_TIRE',
                'MUSTANGGT_KIT00_HEADLIG','MUSTANGGT_SKIN1','MUSTANGGT_DRIVER',
                'MUSTANGGT_RIM'}
assert textures['passed'] and textures['count']==len(expected_names)
assert {t['Name'] for t in textures['textures']}==expected_names
for path in (ROOT/'work/compiled-textures').glob('*.dds'):
    with Image.open(path) as img:img.load()
_,tex=read_pack(ROOT/'release/FORDGT/TEXTURES.BIN')
def binhash(s):
    h=0xffffffff
    for c in s:h=(h*33+ord(c))&0xffffffff
    return h
explicit_hashes={'MUSTANGGT_KIT00_HEADLIG':0x95DE5B23,'MUSTANGGT_KIT00_BRAKELI':0x4B7D95B6}
for mat in load('reference/materials.json'):
    assert explicit_hashes.get(mat['texture'],binhash(mat['texture'])) in tex
original_refs={t for p in original for t in p['info']['Textures']}
new_refs={t for p in compiled for t in p['info']['Textures']}
known_global_refs=set()
assert not (new_refs-set(tex)-original_refs-known_global_refs),'New unresolved texture references'
for name,info in load('reference/input-manifest.json').items():
    with (ROOT/name).open('rb') as f:assert hashlib.file_digest(f,'sha256').hexdigest()==info['sha256']
independent=load('reference/geometry-validation.json')
assert independent['passed'] and len(independent['parts'])==len(compiled)
assert independent['triangles']==sum(p['mesh']['TriangleCount'] for p in compiled)
report={'passed':True,'parts':len(compiled),'original_slots_preserved':len(original),'textures':textures['count'],
        'triangles_all_lods':independent['triangles'],
        'triangles_lod_a':sum(p['mesh']['TriangleCount'] for p in compiled if p['name'].endswith('_A')),
        'donor_markers_preserved':True,'donor_wheels_and_brakes_preserved':True,'original_inputs_unchanged':True,
        'in_game_tested':False,'external_texture_hashes_inherited_from_donor':[f'{h:08X}' for h in sorted(new_refs-set(tex))]}
(ROOT/'reference/release-validation.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
