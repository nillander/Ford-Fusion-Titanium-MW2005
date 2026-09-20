import struct, math
from pathlib import Path

data=(Path(__file__).resolve().parents[1]/'work/fusion.mwr').read_bytes();off=0
def take(n):
    global off
    r=data[off:off+n];off+=n;return r
def string():
    n=struct.unpack('<i',take(4))[0];return take(n)[:-1].decode('ascii')
_,nm,np=struct.unpack('<3i',take(12))
for _ in range(nm):string()
meta=[]
for _ in range(np):
    name=string();nv,nf=struct.unpack('<2i',take(8));matrix=take(64);meta.append((name,nv,nf))
for name,nv,nf in meta:
    vb=take(nv*24);faces=[take(36) for _ in range(nf)]
    if name!='BASE_A':continue
    verts=[struct.unpack_from('<3f',vb,i*24) for i in range(nv)]
    out=[]
    for i,face in enumerate(faces):
        ids=struct.unpack('<i4h6f',face)[1:4];p=[verts[j] for j in ids]
        edge=max(math.dist(p[a],p[b]) for a,b in ((0,1),(1,2),(2,0)))
        if edge>.9:out.append((round(edge,3),i,ids,p))
    for row in sorted(out,reverse=True)[:30]:print(row)
