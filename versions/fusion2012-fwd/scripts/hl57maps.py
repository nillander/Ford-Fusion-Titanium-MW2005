import sys;sys.path.insert(0,'/home/claude/c12');sys.path.insert(0,'/home/claude/v3/versions/v3-fusion-ajm3899/scripts')
import numpy as np,geo,rast
from partmesh import PartMesh
from bulge import samp,allF
from hl29 import frame
from scipy.ndimage import binary_closing,binary_fill_holes
RES=0.003; SKIN=0xB637F71F
def zraster(U,F,grid):
    """max-height raster through the C rasterizer: orthographic view along +n"""
    u0,v0,nu,nv=grid
    if len(F)==0: return np.full((nv,nu),np.nan),np.full((nv,nu),-1)
    # rast.render uses view(az,el); build our own coords: pass P already in screen space via az=0,el=90? simpler: numpy loop
    import fit28; fit28.RES=RES
    return fit28.raster(U,F,grid)
def attr_raster(U,F,A,grid):
    u0,v0,nu,nv=grid; h=np.full((nv,nu),-9.0); out=np.full((nv,nu,A.shape[1]),np.nan)
    T=U[F]; TA=A[F]
    for t,ta in zip(T,TA):
        a=(t[:,0]-u0)/RES; b=(t[:,1]-v0)/RES
        i0,i1=int(max(np.floor(a.min()),0)),int(min(np.ceil(a.max()),nu-1)); j0,j1=int(max(np.floor(b.min()),0)),int(min(np.ceil(b.max()),nv-1))
        if i1<i0 or j1<j0: continue
        I,J=np.meshgrid(np.arange(i0,i1+1),np.arange(j0,j1+1)); px=I.ravel()+0.5; py=J.ravel()+0.5
        d=(b[1]-b[2])*(a[0]-a[2])+(a[2]-a[1])*(b[0]-b[2])
        if abs(d)<1e-12: continue
        w0=((b[1]-b[2])*(px-a[2])+(a[2]-a[1])*(py-b[2]))/d; w1=((b[2]-b[0])*(px-a[2])+(a[0]-a[2])*(py-b[2]))/d; w2=1-w0-w1
        m=(w0>=-1e-6)&(w1>=-1e-6)&(w2>=-1e-6)
        if not m.any(): continue
        z=w0[m]*t[0,2]+w1[m]*t[1,2]+w2[m]*t[2,2]; jj=J.ravel()[m]; ii=I.ravel()[m]
        up=z>h[jj,ii]; jj,ii,z=jj[up],ii[up],z[up]
        W=np.c_[w0[m][up],w1[m][up],w2[m][up]]
        h[jj,ii]=z; out[jj,ii]=W@ta
    return out
def skinF(pm,tex=SKIN):
    F=[g['F'] for g in pm.groups if pm.tex[g['ti']]==tex and len(g['F'])]
    return np.concatenate(F) if F else np.zeros((0,3),int)
def maps(Z,side,pre='COBALTSS',R=0.10):
    gl=PartMesh(Z[f'{pre}_KIT00_{side}_HEADLIGHT_GLASS_A']); F,n,a,b,c0=frame(gl)
    pr=lambda Y: np.c_[(Y-c0)@a,(Y-c0)@b,(Y-c0)@n]
    L=pr(gl.P); FL=allF(gl)
    u0,u1=L[:,0].min()-R,L[:,0].max()+R; v0,v1=L[:,1].min()-R,L[:,1].max()+R
    nu,nv=int((u1-u0)/RES)+1,int((v1-v0)/RES)+1; grid=(u0,v0,nu,nv)
    def near(pm,F):
        C=pm.P[F].mean(1); U=pr(C); return F[(np.abs(U[:,0]-(u0+u1)/2)<(u1-u0)/2+0.02)&(np.abs(U[:,1]-(v0+v1)/2)<(v1-v0)/2+0.02)&(U[:,2]>-0.2)]
    out=dict(frame=(n,a,b,c0),grid=grid)
    out['Lh']=zraster(L,FL,grid)
    hd=PartMesh(Z[f'{pre}_KIT00_{side}_HEADLIGHT_A']); out['Hh']=zraster(pr(hd.P),near(hd,allF(hd)),grid)
    body=PartMesh(Z[f'{pre}_KIT00_BODY_A']); Fs=near(body,skinF(body))
    # front-facing skin only
    fn=np.cross(body.P[Fs[:,1]]-body.P[Fs[:,0]],body.P[Fs[:,2]]-body.P[Fs[:,0]]); Fs_front=Fs[fn@n>0]
    out['Bh']=zraster(pr(body.P),Fs_front,grid); out['Ball']=zraster(pr(body.P),Fs,grid)
    hood=PartMesh(Z[f'{pre}_KIT00_HOOD_A']); out['Dh']=zraster(pr(hood.P),near(hood,allF(hood)),grid)
    oth=[]
    MISC={'COBALTSS':0xE67A7FA5,'MUSTANGGT':0x5A00E244}[pre]
    pm=PartMesh(Z[f'{pre}_KIT00_RIGHT_SIDE_MIRROR_A']); oth.append(zraster(pr(pm.P),near(pm,allF(pm)),grid))
    pm=PartMesh(Z[f'{pre}_BASE_A']); oth.append(zraster(pr(pm.P),near(pm,skinF(pm,MISC)),grid))
    out['Oh']=np.fmax(*oth)
    # paint UV of the visible skin (for the new patch)
    Ub=pr(body.P); out['UVr']=attr_raster(Ub,Fs_front,body.UV,grid)
    lens=binary_fill_holes(binary_closing(~np.isnan(out['Lh']),iterations=2)); out['lens']=lens
    return out
if __name__=='__main__':
    import pickle
    Z={p['name']:p for p in geo.load(sys.argv[1])}
    D={s:maps(Z,s) for s in ('LEFT','RIGHT')}
    pickle.dump(D,open(sys.argv[2],'wb'))
