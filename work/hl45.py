"""Experimental local surface relaxation around the 2012 headlights.

Run against the installed 43 geometry dump. Only existing painted vertices
are moved; no new skirt or artificial ring is introduced.
"""
import sys
import numpy as np
import geo
from scipy.spatial import cKDTree
from scipy.ndimage import distance_transform_edt
from partmesh import PartMesh
from hlgap import masks, RES
from hlfill import SKIN


def smooth_part(pm, d, radius=0.075, strength=0.8, maxshift=0.014):
    n, a, b, c0 = d['frame']
    u0, v0, nu, nv = d['grid']
    ids = np.unique(np.concatenate([g['F'].ravel() for g in pm.groups
                                    if pm.tex[g['ti']] == SKIN and len(g['F'])]))
    P = pm.P[ids]
    U = np.c_[(P-c0)@a, (P-c0)@b, (P-c0)@n]
    ij = np.floor((U[:, :2]-[u0, v0])/RES).astype(int)
    inside = (ij[:, 0]>=0)&(ij[:, 0]<nu)&(ij[:, 1]>=0)&(ij[:, 1]<nv)
    ij[:, 0] = np.clip(ij[:, 0], 0, nu-1)
    ij[:, 1] = np.clip(ij[:, 1], 0, nv-1)
    distmap = distance_transform_edt(~d['lens'])*RES
    dist = distmap[ij[:, 1], ij[:, 0]]
    side = np.sign(c0[1])
    eligible = inside & (P[:, 0]>1.55)&(side*P[:, 1]>0.3)&(P[:, 2]>0.32)
    eligible &= (U[:, 2]>-0.10)&(pm.N[ids]@n>0.2)
    target = eligible & (dist>0.002)&(dist<0.11)
    src = np.flatnonzero(eligible)
    tree = cKDTree(U[src, :2])
    changes = np.zeros(len(ids))
    for i in np.flatnonzero(target):
        near = src[tree.query_ball_point(U[i, :2], radius)]
        if len(near)<16: continue
        dv = U[near, :2]-U[i, :2]
        dh = U[near, 2]-U[i, 2]
        same = (np.abs(dh)<0.055)&(pm.N[ids[near]]@pm.N[ids[i]]>0.55)
        near=near[same]; dv=dv[same]; dh=dh[same]
        if len(near)<12: continue
        r2 = np.sum(dv*dv, axis=1)
        w = np.exp(-r2/(2*0.035**2))
        # The quadratic surface retains the intended convex fender and hood shape.
        x,y = dv.T
        A = np.c_[np.ones(len(dv)),x,y,x*x,x*y,y*y]
        coef = np.linalg.lstsq(A*w[:, None], U[near, 2]*w, rcond=1e-9)[0]
        inner = np.clip((dist[i]-0.002)/0.012,0,1)
        outer = np.clip((0.11-dist[i])/0.05,0,1)
        fade = (inner*inner*(3-2*inner))*(outer*outer*(3-2*outer))
        changes[i] = np.clip((coef[0]-U[i,2])*strength*fade,-maxshift,maxshift)
    pm.P[ids] += changes[:, None]*n
    # Keep shading aligned with the new surface. Face-normal correction is
    # blended, because the original asset uses custom normals at trim lines.
    moved = np.abs(changes)>1e-6
    if moved.any():
        N = np.zeros_like(pm.N)
        for g in pm.groups:
            if pm.tex[g['ti']] != SKIN: continue
            F = g['F']
            fn = np.cross(pm.P[F[:, 1]]-pm.P[F[:, 0]],pm.P[F[:, 2]]-pm.P[F[:, 0]])
            for k in range(3): np.add.at(N,F[:, k],fn)
        orig=pm.N[ids[moved]]
        surf=N[ids[moved]]
        norm=np.linalg.norm(surf,axis=1)
        good=norm>1e-9
        surf[good]/=norm[good,None]
        blend=0.3*surf+0.7*orig
        pm.N[ids[moved]]=blend/np.maximum(np.linalg.norm(blend,axis=1,keepdims=True),1e-9)
    return int(moved.sum()), np.round(np.percentile(changes[moved]*1000,[0,25,50,75,100]),2) if moved.any() else []


def main(src_path,out_path,all_lods=False):
    Z={p['name']:p for p in geo.load(src_path)}
    D={side:masks(Z,side) for side in ('LEFT','RIGHT')}
    records=[]
    for name in sorted(Z):
        if not (('_BODY_' in name and '_KIT' in name) or ('_HOOD_' in name and '_KIT' in name)):
            continue
        if not all_lods and name not in ('COBALTSS_KIT00_BODY_A','COBALTSS_KIT00_HOOD_A'):
            continue
        if all_lods and name.rsplit('_',1)[-1] not in 'ABCDE': continue
        pm=PartMesh(Z[name])
        if not any(pm.tex[g['ti']]==SKIN for g in pm.groups):continue
        moved={side:smooth_part(pm,d) for side,d in D.items()}
        if not any(x[0] for x in moved.values()):continue
        rec,nv=pm.record()
        if nv>65535:raise ValueError((name,nv))
        records.append(rec)
        print(name,moved,'vertices',nv,flush=True)
    with open(out_path,'wb') as f:
        for rec in records:f.write(rec)

if __name__=='__main__':main(sys.argv[1],sys.argv[2],len(sys.argv)>3)
