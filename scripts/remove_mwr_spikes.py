import math
import shutil
import struct
from pathlib import Path

root=Path(__file__).resolve().parents[1]
path=root/'work/fusion.mwr'
data=path.read_bytes(); off=0

def take(n):
    global off
    out=data[off:off+n];off+=n;return out

def take_string():
    n=struct.unpack('<i',take(4))[0]
    return struct.pack('<i',n)+take(n)

header=take(12)
_,material_count,mesh_count=struct.unpack('<3i',header)
materials=[take_string() for _ in range(material_count)]
entries=[]
for _ in range(mesh_count):
    name_raw=take_string()
    name=name_raw[4:-1].decode('ascii')
    meta=take(72)
    nv,nf=struct.unpack_from('<2i',meta)
    entries.append({'name':name,'name_raw':name_raw,'meta':meta,'nv':nv,'nf':nf})

vertex_size=24
face_size=36
for e in entries:
    e['vertices']=take(e['nv']*vertex_size)
    e['faces']=[take(face_size) for _ in range(e['nf'])]
if off!=len(data):raise RuntimeError(f'MWR trailing bytes: {len(data)-off}')

removed_total=0
for e in entries:
    if not e['name'].startswith('BASE_'):continue
    vertices=[struct.unpack_from('<3f',e['vertices'],i*vertex_size) for i in range(e['nv'])]
    kept=[];removed=0
    for face in e['faces']:
        values=struct.unpack('<i4h6f',face)
        indices=values[1:4]
        points=[vertices[i] for i in indices]
        ab=tuple(points[1][j]-points[0][j] for j in range(3))
        ac=tuple(points[2][j]-points[0][j] for j in range(3))
        cross=(ab[1]*ac[2]-ab[2]*ac[1],ab[2]*ac[0]-ab[0]*ac[2],ab[0]*ac[1]-ab[1]*ac[0])
        area=.5*math.sqrt(sum(x*x for x in cross))
        # MWR stores position as lateral, vertical, longitudinal.
        vertical=[p[1] for p in points]
        longitudinal=[p[2] for p in points]
        edge=max(math.dist(points[a],points[b]) for a,b in ((0,1),(1,2),(2,0)))
        broad_spike=area>.55 and max(vertical)>.5 and max(vertical)-min(vertical)>.35
        pointed_spike=(edge>.9 and max(vertical)>1.0 and
                       max(longitudinal)>1.8 and min(longitudinal)>0.9)
        spike=broad_spike or pointed_spike
        if spike:removed+=1
        else:kept.append(face)
    if removed:
        e['faces']=kept;e['nf']=len(kept)
        meta=bytearray(e['meta']);struct.pack_into('<i',meta,4,e['nf']);e['meta']=bytes(meta)
        print(e['name'],'removed_spikes',removed)
        removed_total+=removed

if removed_total:
    backup=root/'work/fusion-pre-spike-filter.mwr'
    shutil.copy2(path,backup)
    temp=path.with_suffix('.mwr.tmp')
    with temp.open('wb') as f:
        f.write(header)
        for raw in materials:f.write(raw)
        for e in entries:f.write(e['name_raw']);f.write(e['meta'])
        for e in entries:
            f.write(e['vertices'])
            for face in e['faces']:f.write(face)
    temp.replace(path)
print('MWR_SPIKE_FILTER',removed_total)
