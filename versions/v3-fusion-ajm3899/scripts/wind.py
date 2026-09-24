import numpy as np, geo, sys
def agree(p,g):
    seg=p['idx'][g['offset']:g['offset']+g['length']].astype(int)
    t=seg[:len(seg)//3*3].reshape(-1,3); P=p['v']['p'].astype(float); N=p['v']['n'].astype(float)
    fn=np.cross(P[t[:,1]]-P[t[:,0]],P[t[:,2]]-P[t[:,0]])
    vn=N[t].sum(1)
    d=(fn*vn).sum(1); ok=np.abs(d)>1e-12
    return (d[ok]>0).mean() if ok.any() else float('nan'), len(t)
if __name__=='__main__':
    parts=geo.load(sys.argv[1]); flt=sys.argv[2] if len(sys.argv)>2 else '_A'
    for p in parts:
        if not p['name'].endswith(flt): continue
        print(p['name'], ' '.join('g%d:%s:%.2f(%d)'%(i,hex(p['shaders'][g['shader']]),*agree(p,g)) for i,g in enumerate(p['groups'])))
