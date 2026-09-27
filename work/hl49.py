"""Test whether irregular headlight-surround highlights are vertex-normal defects."""
import sys
import numpy as np
import geo
from scipy.spatial import cKDTree
from scipy.ndimage import distance_transform_edt
from partmesh import PartMesh
from hlgap import masks, RES
from hlfill import SKIN


def smooth_normals(pm,d):
    n,a,b,c0=d['frame'];u0,v0,nu,nv=d['grid']
    ids=np.unique(np.concatenate([g['F'].ravel() for g in pm.groups
                                  if pm.tex[g['ti']]==SKIN and len(g['F'])]))
    P=pm.P[ids];N=pm.N[ids]
    U=np.c_[(P-c0)@a,(P-c0)@b,(P-c0)@n]
    ij=np.floor((U[:,:2]-[u0,v0])/RES).astype(int)
    inside=(ij[:,0]>=0)&(ij[:,0]<nu)&(ij[:,1]>=0)&(ij[:,1]<nv)
    ij[:,0]=np.clip(ij[:,0],0,nu-1);ij[:,1]=np.clip(ij[:,1],0,nv-1)
    dist=distance_transform_edt(~d['lens'])[ij[:,1],ij[:,0]]*RES
    side=np.sign(c0[1])
    eligible=inside&(P[:,0]>1.55)&(side*P[:,1]>0.3)&(P[:,2]>0.3)
    eligible&=(N@n>0.12)&(U[:,2]>-0.10)
    target=eligible&(dist>0.003)&(dist<0.13)
    src=np.flatnonzero(eligible)
    tree=cKDTree(P[src])
    updates={}
    for i in np.flatnonzero(target):
        near=src[tree.query_ball_point(P[i],0.085)]
        if len(near)<12:continue
        dp=P[near]-P[i]
        sim=N[near]@N[i]
        good=(sim>0.65)&(np.abs(U[near,2]-U[i,2])<0.04)
        near=near[good];dp=dp[good]
        if len(near)<10:continue
        w=np.exp(-np.sum(dp*dp,axis=1)/(2*0.038**2))
        avg=np.sum(N[near]*w[:,None],axis=0)/np.sum(w)
        f=np.clip((dist[i]-0.003)/0.012,0,1)*np.clip((0.13-dist[i])/0.04,0,1)
        f=f*f*(3-2*f)
        mix=(1-0.8*f)*N[i]+0.8*f*avg
        updates[i]=mix/np.linalg.norm(mix)
    if updates:
        k=np.fromiter(updates,int);pm.N[ids[k]]=np.array(list(updates.values()))
    return len(updates)


def main(src,out,test=False):
    Z={p['name']:p for p in geo.load(src)}
    D={s:masks(Z,s) for s in ('LEFT','RIGHT')}
    recs=[]
    for name in sorted(Z):
        if not ('_KIT' in name and ('_BODY_' in name or '_HOOD_' in name)):
            continue
        if name.rsplit('_',1)[-1] not in 'ABCDE':continue
        if test and name not in ('COBALTSS_KIT00_BODY_A','COBALTSS_KIT00_HOOD_A'):continue
        pm=PartMesh(Z[name])
        if SKIN not in pm.tex:continue
        counts={s:smooth_normals(pm,d) for s,d in D.items()}
        if not any(counts.values()):continue
        rec,nv=pm.record();recs.append(rec)
        print(name,counts,nv,flush=True)
    with open(out,'wb') as f:
        for r in recs:f.write(r)

if __name__=='__main__':main(sys.argv[1],sys.argv[2],len(sys.argv)>3)
