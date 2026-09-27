"""Topology-aware harmonic fairing of the painted 2012 headlight surround."""
import sys
import numpy as np
import geo
from scipy.sparse import coo_matrix,diags
from scipy.sparse.linalg import spsolve
from scipy.ndimage import distance_transform_edt
from partmesh import PartMesh
from hlgap import masks,RES
from hlfill import SKIN


def adjacency(pm):
    faces=np.concatenate([g['F'] for g in pm.groups if pm.tex[g['ti']]==SKIN and len(g['F'])])
    edge=np.concatenate([faces[:,[0,1]],faces[:,[1,2]],faces[:,[2,0]]])
    edge=np.sort(edge,axis=1)
    edge=np.unique(edge,axis=0)
    ij=np.r_[edge,edge[:,::-1]]
    p=pm.P
    dist=np.linalg.norm(p[ij[:,0]]-p[ij[:,1]],axis=1)
    weight=1/np.maximum(dist,0.004)
    A=coo_matrix((weight,(ij[:,0],ij[:,1])),shape=(len(p),len(p))).tocsr()
    return A


def fair(pm,d,side,A,which='upper',profile='original'):
    n,a,b,c0=d['frame'];u0,v0,nu,nv=d['grid']
    P=pm.P;U=np.c_[(P-c0)@a,(P-c0)@b,(P-c0)@n]
    yy,xx=np.nonzero(d['lens'])
    ilim=np.quantile(xx,0.975 if side=='LEFT' else 0.025)
    tip=xx>=ilim if side=='LEFT' else xx<=ilim
    inner_u=u0+np.median(xx[tip])*RES
    outer_u=u0+(xx.min() if side=='LEFT' else xx.max())*RES
    specs={
      'upper':((inner_u+.73*(outer_u-inner_u),-.105),(.165,.095)),
      'lower':((inner_u+.48*(outer_u-inner_u),.105),(.29,.11)),
      'inner':((inner_u,u0*0+v0+np.median(yy[tip])*RES),(.145,.165)),
    }
    if profile=='last-points':
      specs['upper']=((inner_u+.78*(outer_u-inner_u),-.103),(.195,.120))
      specs['inner']=((inner_u,u0*0+v0+np.median(yy[tip])*RES),(.170,.175))
    c,r=specs[which]
    q=((U[:,0]-c[0])/r[0])**2+((U[:,1]-c[1])/r[1])**2
    ij=np.floor((U[:,:2]-[u0,v0])/RES).astype(int)
    inside=(ij[:,0]>=0)&(ij[:,0]<nu)&(ij[:,1]>=0)&(ij[:,1]<nv)
    ij[:,0]=np.clip(ij[:,0],0,nu-1);ij[:,1]=np.clip(ij[:,1],0,nv-1)
    dist=distance_transform_edt(~d['lens'])[ij[:,1],ij[:,0]]*RES
    select=(q<1)&inside&(dist>0.004)&(P[:,0]>1.55)&(P[:,2]>0.3)
    select&=(np.sign(P[:,1])==np.sign(c0[1]))&(pm.N@n>0.12)&(U[:,2]>-0.10)
    v=np.flatnonzero(select)
    if len(v)<10:return 0,0.0
    L=diags(np.asarray(A.sum(axis=1)).ravel())-A
    rhs=-(L[v]@U[:,2]-L[v][:,v]@U[v,2])
    sub=L[v][:,v]
    reg=0.01*np.median(sub.diagonal())
    try:target=spsolve(sub+diags(np.full(len(v),reg)),rhs+reg*U[v,2])
    except Exception as e:print('solver failed',e);return 0,0.0
    limit={'upper':0.030,'lower':0.020,'inner':0.025 if profile=='last-points' else 0.018}[which]
    change=np.clip((target-U[v,2])*0.75,-limit,limit)
    pm.P[v]+=change[:,None]*n
    # Smooth custom normals separately after the geometry test.
    return int(np.count_nonzero(np.abs(change)>1e-6)),float(np.max(np.abs(change),initial=0))


def main(src,out,test=False,profile='original'):
    Z={p['name']:p for p in geo.load(src)}
    D={s:masks(Z,s) for s in ('LEFT','RIGHT')}
    recs=[]
    for name in sorted(Z):
        if not ('_KIT' in name and '_BODY_' in name and name.rsplit('_',1)[-1] in 'ABCDE'):continue
        if test and name!='COBALTSS_KIT00_BODY_A':continue
        pm=PartMesh(Z[name]);A=adjacency(pm)
        changes={s:{region:fair(pm,d,s,A,region,profile) for region in ('upper','lower','inner')}
                 for s,d in D.items()}
        if not any(x[0] for side in changes.values() for x in side.values()):continue
        record,nv=pm.record();recs.append(record)
        print(name,changes,nv,flush=True)
    with open(out,'wb') as f:
        for r in recs:f.write(r)

if __name__=='__main__':main(sys.argv[1],sys.argv[2],False,sys.argv[3] if len(sys.argv)>3 else 'original')
