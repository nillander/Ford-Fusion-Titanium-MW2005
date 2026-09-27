"""crease-aware geometric normals for skin; report/repair vertices whose stored normal disagrees."""
import sys;sys.path.insert(0,'/home/claude/c12');sys.path.insert(0,'/home/claude/v3/versions/v3-fusion-ajm3899/scripts')
import numpy as np,geo
from partmesh import PartMesh
SKINS=(0xB637F71F,0x9A8AAD9E)
def geo_normals(pm,Fall,ang=40):
    """per (face,corner) crease-aware normal; returns dict vertex->normal (for vertices used by Fall)"""
    P=pm.P; T=P[Fall]; fn=np.cross(T[:,1]-T[:,0],T[:,2]-T[:,0]); ar=np.linalg.norm(fn,axis=1); fu=fn/np.maximum(ar,1e-15)[:,None]
    key=np.round(P*1e4).astype(np.int64); _,wid=np.unique(key,axis=0,return_inverse=True); wid=wid.ravel()
    W=wid[Fall]
    # faces around each welded vertex
    order=np.argsort(W.ravel(),kind='stable'); wsorted=W.ravel()[order]; starts=np.searchsorted(wsorted,np.arange(wid.max()+2))
    cosT=np.cos(np.radians(ang)); out=np.zeros((len(Fall),3,3))
    for t in range(len(Fall)):
        for c in range(3):
            w=W[t,c]; fs=order[starts[w]:starts[w+1]]//3
            m=(fu[fs]@fu[t])>cosT
            s=(fn[fs[m]]).sum(0); out[t,c]=s/max(np.linalg.norm(s),1e-15)
    return out,fu,ar/2
