import json, math
from pathlib import Path

root=Path(__file__).resolve().parents[1]
parts=json.loads((root/'work/compiled-geometry.json').read_text())
for part in parts:
    if part['name']!='MUSTANGGT_BASE_A':continue
    verts=[tuple(v['Position'][k] for k in 'xyz') for v in part['mesh']['Vertices']]
    idx=part['mesh']['Indices'];faces=[tuple(idx[i:i+3]) for i in range(0,len(idx),3)]
    parent=list(range(len(verts)))
    def find(x):
        while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
        return x
    def union(a,b):
        a,b=find(a),find(b)
        if a!=b:parent[b]=a
    for f in faces:union(f[0],f[1]);union(f[0],f[2])
    groups={}
    for fi,f in enumerate(faces):groups.setdefault(find(f[0]),[]).append(fi)
    rows=[]
    for fs in groups.values():
        used=sorted({v for fi in fs for v in faces[fi]});points=[verts[v] for v in used]
        mins=[min(p[j] for p in points) for j in range(3)];maxs=[max(p[j] for p in points) for j in range(3)]
        area=0
        for fi in fs:
            p=[verts[v] for v in faces[fi]];ab=[p[1][j]-p[0][j] for j in range(3)];ac=[p[2][j]-p[0][j] for j in range(3)]
            cr=(ab[1]*ac[2]-ab[2]*ac[1],ab[2]*ac[0]-ab[0]*ac[2],ab[0]*ac[1]-ab[1]*ac[0]);area+=.5*math.sqrt(sum(x*x for x in cr))
        rows.append((len(fs),len(used),round(area,4),tuple(round(maxs[j]-mins[j],3) for j in range(3)),tuple(round(x,3) for x in mins),tuple(round(x,3) for x in maxs),fs[:10]))
    for row in sorted(rows,key=lambda r:(r[0],-r[2])):
        if row[0]<=100 or max(row[3])>2:print(row)
