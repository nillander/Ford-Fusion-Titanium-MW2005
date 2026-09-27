"""Radial (star-shaped) parametrisation of the front corner around each headlight.
(s,t) = R0*(azimuth, elevation) seen from a centre inside the car, h = radius. Grid RES=3 mm (at R0)."""
import sys;sys.path.insert(0,'/home/claude/c12');sys.path.insert(0,'/home/claude/v3/versions/v3-fusion-ajm3899/scripts')
import numpy as np,geo
from partmesh import PartMesh
from bulge import allF
from scipy.ndimage import binary_closing,binary_fill_holes
from hl57maps import attr_raster,skinF
RES=0.003; SKIN=0xB637F71F; R0=0.7
def centre(side): return np.array([1.50,0.28 if side=='LEFT' else -0.28,0.38])
def fwd(X,c):
    V=X-c; r=np.linalg.norm(V,axis=1); th=np.arctan2(V[:,1],V[:,0]); ph=np.arcsin(np.clip(V[:,2]/np.maximum(r,1e-9),-1,1))
    return np.c_[R0*th,R0*ph,r]
def inv(S,c):
    th=S[:,0]/R0; ph=S[:,1]/R0; r=S[:,2]
    return c+r[:,None]*np.c_[np.cos(ph)*np.cos(th),np.cos(ph)*np.sin(th),np.sin(ph)]
def raster(U,F,grid,A=None):
    """max-radius raster (+ optional attributes); drops triangles that straddle the azimuth seam"""
    T=U[F]; ok=(np.ptp(T[:,:,0],1)<0.3)&(np.ptp(T[:,:,1],1)<0.3)
    F=F[ok]
    if A is None:
        import fit28; fit28.RES=RES; return fit28.raster(U,F,grid)
    return attr_raster(U,F,A,grid)
def maps(Z,side,pre='COBALTSS',M=0.10):
    c=centre(side); pr=lambda X: fwd(X,c)
    gl=PartMesh(Z[f'{pre}_KIT00_{side}_HEADLIGHT_GLASS_A']); FL=allF(gl); L=pr(gl.P)
    u0,u1=L[:,0].min()-M,L[:,0].max()+M; v0,v1=L[:,1].min()-M,L[:,1].max()+M
    nu,nv=int((u1-u0)/RES)+1,int((v1-v0)/RES)+1; grid=(u0,v0,nu,nv)
    def near(pm,F):
        U=pr(pm.P[F].mean(1)); X=pm.P[F].mean(1)
        return F[(U[:,0]>u0-0.02)&(U[:,0]<u1+0.02)&(U[:,1]>v0-0.02)&(U[:,1]<v1+0.02)&(U[:,2]>0.15)&(np.sign(X[:,1]-c[1]*0)==np.sign(c[1]))]
    out=dict(c=c,grid=grid)
    out['Lh']=raster(L,FL,grid)
    hd=PartMesh(Z[f'{pre}_KIT00_{side}_HEADLIGHT_A']); out['Hh']=raster(pr(hd.P),near(hd,allF(hd)),grid)
    body=PartMesh(Z[f'{pre}_KIT00_BODY_A']); Fs=near(body,skinF(body))
    Ub=pr(body.P)
    fn=np.cross(body.P[Fs[:,1]]-body.P[Fs[:,0]],body.P[Fs[:,2]]-body.P[Fs[:,0]])
    outward=((body.P[Fs].mean(1)-c)*fn).sum(1)>0
    Ff=Fs[outward]
    out['Bh']=raster(Ub,Ff,grid); out['UVr']=raster(Ub,Ff,grid,body.UV)
    hood=PartMesh(Z[f'{pre}_KIT00_HOOD_A']); out['Dh']=raster(pr(hood.P),near(hood,allF(hood)),grid)
    MISC={'COBALTSS':0xE67A7FA5,'MUSTANGGT':0x5A00E244}[pre]
    pm=PartMesh(Z[f'{pre}_KIT00_RIGHT_SIDE_MIRROR_A']); o1=raster(pr(pm.P),near(pm,allF(pm)),grid)
    pm=PartMesh(Z[f'{pre}_BASE_A']); o2=raster(pr(pm.P),near(pm,skinF(pm,MISC)),grid)
    out['Oh']=np.fmax(o1,o2)
    out['lens']=binary_fill_holes(binary_closing(~np.isnan(out['Lh']),iterations=2))
    return out
if __name__=='__main__':
    import pickle
    Z={p['name']:p for p in geo.load(sys.argv[1])}
    pickle.dump({s:maps(Z,s) for s in ('LEFT','RIGHT')},open(sys.argv[2],'wb'))
