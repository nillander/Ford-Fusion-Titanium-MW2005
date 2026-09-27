"""Targeted 2012 outer-headlight fit repair, experimental.

Input is the smoothed hl45 dump. Only uncovered gap regions get a bridge;
the existing deep fillers remain hidden behind it. The inner/grille end stays fixed.
"""
import sys
import numpy as np
import geo
from scipy.ndimage import distance_transform_edt, gaussian_filter
from scipy.spatial import cKDTree
from partmesh import PartMesh
from hlgap import masks, RES
from hlfill import SKIN, patch_geom, add


def outer_weight(U, d, side):
    u0, v0, nu, nv = d['grid']
    ii=np.clip(((U[:,0]-u0)/RES).astype(int),0,nu-1)
    jj=np.clip(((U[:,1]-v0)/RES).astype(int),0,nv-1)
    ys,xs=np.nonzero(d['lens'])
    lo=u0+xs.min()*RES; hi=u0+xs.max()*RES
    t=(hi-U[:,0])/(hi-lo) if side=='LEFT' else (U[:,0]-lo)/(hi-lo)
    t=np.clip((t-0.53)/0.39,0,1)
    return t*t*(3-2*t), ii, jj


def advance_lamp(pm,d,side,amount=0.003):
    n,a,b,c0=d['frame']
    P=pm.P
    U=np.c_[(P-c0)@a,(P-c0)@b,(P-c0)@n]
    w,_,_=outer_weight(U,d,side)
    m=(P[:,0]>1.5)&(P[:,2]>0.3)&(np.sign(P[:,1])==np.sign(c0[1]))
    shift=w*amount*m
    pm.P+=shift[:,None]*n


def lift_outer_skin(pm,d,side,maxshift=0.032,maxdist=0.085):
    n,a,b,c0=d['frame']; u0,v0,nu,nv=d['grid']
    ids=np.unique(np.concatenate([g['F'].ravel() for g in pm.groups if pm.tex[g['ti']]==SKIN and len(g['F'])]))
    P=pm.P[ids]
    U=np.c_[(P-c0)@a,(P-c0)@b,(P-c0)@n]
    outer,ii,jj=outer_weight(U,d,side)
    distance=distance_transform_edt(~d['lens'])*RES
    near=distance_transform_edt(~(d['Lh']>-8),return_indices=True)[1]
    lh=gaussian_filter(d['Lh'][near[0],near[1]],4)[jj,ii]
    dist=distance[jj,ii]
    fade=np.clip(1-dist/maxdist,0,1)
    fade=fade*fade*(3-2*fade)
    zone=(dist>0.001)&(dist<maxdist)&(P[:,0]>1.55)&(P[:,2]>0.3)
    zone&=(np.sign(P[:,1])==np.sign(c0[1]))&(pm.N[ids]@n>0.12)
    shift=np.where(zone, np.clip(lh-0.006-U[:,2],0,maxshift)*fade*outer,0)
    pm.P[ids]+=shift[:,None]*n
    # Reuse the existing local fit to remove nearby high-frequency dents, but
    # leave the lamp-facing contour already repaired above in position.
    count=int(np.count_nonzero(shift>1e-6))
    return count,float(shift.max(initial=0))


def bridge(d,k,side,region='outer'):
    u0,v0,nu,nv=d['grid']
    ys,xs=np.nonzero(d['lens'])
    lo,hi=xs.min(),xs.max()
    columns=np.arange(nu)
    outer=(hi-columns)/(hi-lo) if side=='LEFT' else (columns-lo)/(hi-lo)
    masked=dict(d)
    # The grille-side tip already mates with the lamp: do not add a skin there.
    if region=='outer':
        masked['gap']=d['gap'] & (outer[None,:]>0.30)
    elif region=='inner-lower':
        # The isolated black triangle lies below the grille-side white tip.
        # Do not bridge the upper hood edge or the already seated lamp face.
        rows=np.arange(nv)
        masked['gap']=d['gap'] & (outer[None,:]<0.21) & (rows[:,None]>nv*0.49)
    else: raise ValueError(region)
    geom=patch_geom(masked,k,maxdist=0.09)
    if geom is None:return None
    P,N,F=geom
    n,a,b,c0=d['frame'];u0,v0,nu,nv=d['grid']
    U=np.c_[(P-c0)@a,(P-c0)@b,(P-c0)@n]
    ii=np.clip(((U[:,0]-u0)/RES).astype(int),0,nu-1)
    jj=np.clip(((U[:,1]-v0)/RES).astype(int),0,nv-1)
    dl=distance_transform_edt(~d['lens'])*RES
    db=distance_transform_edt(~d['body'])*RES
    valid=d['Lh']>-8
    near=distance_transform_edt(~valid,return_indices=True)[1]
    lh=gaussian_filter(d['Lh'][near[0],near[1]],4)[jj,ii]
    wl=db[jj,ii]/np.maximum(dl[jj,ii]+db[jj,ii],0.001)
    wl=np.clip(wl,0,1)
    # 4 mm behind the lens edge; at body edge form a gently receding lip.
    h=lh-0.023+0.019*wl
    P=P+(h-U[:,2])[:,None]*n
    fn=np.cross(P[F[:,1]]-P[F[:,0]],P[F[:,2]]-P[F[:,0]])
    N=np.zeros_like(P)
    for k1 in range(3):np.add.at(N,F[:,k1],fn)
    N/=np.maximum(np.linalg.norm(N,axis=1,keepdims=True),1e-10)
    return P,N,F


def add_bridge(pm, geoms):
    painted=[g for g in pm.groups if pm.tex[g['ti']]==SKIN]
    ids=np.unique(np.concatenate([g['F'].ravel() for g in painted if len(g['F'])]))
    kd=cKDTree(pm.P[ids])
    shaded=[]
    for P,N,F in geoms:
        _,near=kd.query(P)
        nn=pm.N[ids[near]]
        # Preserve the car's authored paint shading along the join.
        mix=0.90*nn+0.10*N
        mix/=np.maximum(np.linalg.norm(mix,axis=1,keepdims=True),1e-10)
        shaded.append((P,mix,F))
    return add(pm,shaded)


def main(current_path,out_path,test=False):
    Z={p['name']:p for p in geo.load(current_path)}
    D={s:masks(Z,s) for s in ('LEFT','RIGHT')}
    geoms={lod:[x for x in (bridge(D[s],k,s) for s in ('LEFT','RIGHT')) if x is not None]
           for lod,k in (('A',5),('B',7),('C',10),('D',14),('E',14))}
    print('patches', {lod:sum(len(g[0]) for g in gs) for lod,gs in geoms.items()},flush=True)
    records=[]
    for name in sorted(Z):
        if '_BODY_' in name and '_KIT' in name and name.rsplit('_',1)[-1] in 'ABCDE':
            if test and name!='COBALTSS_KIT00_BODY_A':continue
            pm=PartMesh(Z[name])
            lifts={}
            added=add_bridge(pm,geoms[name.rsplit('_',1)[-1]])
            rec,nv=pm.record()
            if nv>65535:raise ValueError((name,nv))
            records.append(rec)
            print(name,'lift',lifts,'added',added,'verts',nv,flush=True)
        elif '_HOOD_' in name and '_KIT' in name and name.rsplit('_',1)[-1] in 'ABCD':
            if test and name!='COBALTSS_KIT00_HOOD_A':continue
            continue
        elif ('HEADLIGHT_' in name or 'HEADLIGHT_GLASS_' in name) and name.rsplit('_',1)[-1] in 'ABCD':
            if test and not name.endswith('_A'):continue
            side='LEFT' if '_LEFT_' in name else 'RIGHT' if '_RIGHT_' in name else None
            if side is None:continue
            pm=PartMesh(Z[name]);advance_lamp(pm,D[side],side)
            rec,nv=pm.record();records.append(rec)
            print(name,'tip advance 3 mm','verts',nv,flush=True)
    with open(out_path,'wb') as f:
        for rec in records:f.write(rec)


if __name__=='__main__':main(sys.argv[1],sys.argv[2],len(sys.argv)>3)
