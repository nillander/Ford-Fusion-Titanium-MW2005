import numpy as np, geo, sys
def outward(p,g,center=np.array([0,0,0.55])):
    seg=p['idx'][g['offset']:g['offset']+g['length']].astype(int)
    t=seg[:len(seg)//3*3].reshape(-1,3); P=p['v']['p'].astype(float)
    fn=np.cross(P[t[:,1]]-P[t[:,0]],P[t[:,2]]-P[t[:,0]]); c=P[t].mean(1)
    a=np.linalg.norm(fn,axis=1); ok=a>0
    d=((fn[ok]/a[ok,None])*(c[ok]-center)).sum(1)
    return (d>0).mean(), ok.sum()
parts=geo.load(sys.argv[1])
for p in parts:
    if not p['name'].endswith(sys.argv[2] if len(sys.argv)>2 else '_A'): continue
    print(p['name'], ' '.join('g%d:%.2f(%d)'%(i,*outward(p,g)) for i,g in enumerate(p['groups'])))
