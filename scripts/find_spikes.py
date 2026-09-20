import json, math
import heapq
from pathlib import Path

root=Path(__file__).resolve().parents[1]
parts=json.loads((root/'work/compiled-geometry.json').read_text())
largest=[]
for part in parts:
    mesh=part['mesh']
    verts=[(v['Position']['x'],v['Position']['y'],v['Position']['z']) for v in mesh['Vertices']]
    idx=mesh['Indices']
    longest=0.0; longest_tri=None
    for i in range(0,len(idx),3):
        tri=idx[i:i+3]
        if len(tri)<3 or max(tri)>=len(verts):continue
        p=[verts[n] for n in tri]
        edge=max(math.dist(p[a],p[b]) for a,b in ((0,1),(1,2),(2,0)))
        ab=tuple(p[1][j]-p[0][j] for j in range(3)); ac=tuple(p[2][j]-p[0][j] for j in range(3))
        cross=(ab[1]*ac[2]-ab[2]*ac[1],ab[2]*ac[0]-ab[0]*ac[2],ab[0]*ac[1]-ab[1]*ac[0])
        area=.5*math.sqrt(sum(x*x for x in cross))
        largest.append((area,part['name'],tri,p))
        if edge>longest:longest,longest_tri=edge,(tri,p)
    if longest>2.0 or mesh['TriangleCount']<=4:
        print(part['name'],'vertices',len(verts),'tris',mesh['TriangleCount'],'max_edge',round(longest,3),'sample',longest_tri)
print('LARGEST_AREAS')
for area,name,tri,p in sorted(largest,key=lambda x:x[0],reverse=True)[:30]:
    print(round(area,4),name,tri,p)
