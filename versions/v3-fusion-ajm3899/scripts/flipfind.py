import numpy as np, geo, sys, json
def tris_of(p,groups=None):
    P=p['v']['p'].astype(np.float64); out=[]
    for gi,g in enumerate(p['groups']):
        if groups is not None and gi not in groups: continue
        seg=p['idx'][g['offset']:g['offset']+g['length']].astype(int).reshape(-1,3)
        out.append((gi,g['offset'],P[seg]))
    return out
def hits(O,D,T,eps=1e-4):
    # O,D: (R,3); T: (M,3,3) -> bool (R,) any hit with t>eps
    v0=T[:,0];e1=T[:,1]-v0;e2=T[:,2]-v0
    res=np.zeros(len(O),bool)
    for s in range(0,len(O),128):
        o=O[s:s+128,None,:]; d=D[s:s+128,None,:]
        p=np.cross(d,e2[None]); det=(e1[None]*p).sum(-1)
        ok=np.abs(det)>1e-12; inv=np.where(ok,1/np.where(ok,det,1),0)
        tv=o-v0[None]; u=(tv*p).sum(-1)*inv
        q=np.cross(tv,e1[None]); v=(d*q).sum(-1)*inv; t=(e2[None]*q).sum(-1)*inv
        h=ok&(u>=0)&(v>=0)&(u+v<=1)&(t>eps)
        res[s:s+128]=h.any(1)
    return res
parts={p['name']:p for p in geo.load(sys.argv[1])}
result={}
for lod in 'ABCDE':
    body=parts['MUSTANGGT_KIT00_BODY_'+lod]; base=parts['MUSTANGGT_BASE_'+lod]
    occ=np.concatenate([t for _,_,t in tris_of(body)]+[t for _,_,t in tris_of(base)])
    for gi,off,T in tris_of(body,[0]):
        n=np.cross(T[:,1]-T[:,0],T[:,2]-T[:,0]); a=np.linalg.norm(n,axis=1); ok=a>1e-12
        n[ok]/=a[ok,None]; c=T.mean(1)
        fwd=hits(c+n*2e-3,n,occ); back=hits(c-n*2e-3,-n,occ)
        flip=np.where(ok&fwd&~back)[0]
        result['MUSTANGGT_KIT00_BODY_'+lod]=[int(off+3*k) for k in flip]
        print(lod,len(T),'flip',len(flip),'enclosed-both',int((fwd&back).sum()),flush=True)
json.dump(result,open(sys.argv[2],'w'))
