import numpy as np
from scipy import ndimage
class Footprint:
    """2D footprint of a lens surface, projected along direction d."""
    def __init__(self,P,F,d=None,cell=0.004,dilate=0.01):
        tri=P[F]
        n=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]); a=np.linalg.norm(n,axis=1)
        if d is None:
            c=tri.mean(1); ref=np.array([0.,0.,0.45])
            sg=np.sign(((c-ref)*n).sum(1)); d=(n*sg[:,None]).sum(0)
        self.d=d/np.linalg.norm(d)
        t=np.cross(self.d,[0,0,1.]); 
        if np.linalg.norm(t)<0.1: t=np.cross(self.d,[1,0,0.])
        self.e1=t/np.linalg.norm(t); self.e2=np.cross(self.d,self.e1)
        q=self.proj(P); self.o=q.min(0)-0.05; self.cell=cell
        self.shape=tuple((np.ceil((q.max(0)+0.05-self.o)/cell)).astype(int)+1)
        depth=np.full(self.shape,-1e9)
        # rasterize triangles by sampling
        for f in F:
            A,B,C=q[f]; sA,sB,sC=(P[f]@self.d)
            lo=np.floor((np.minimum(np.minimum(A,B),C)-self.o)/cell).astype(int); hi=np.ceil((np.maximum(np.maximum(A,B),C)-self.o)/cell).astype(int)
            xs,ys=np.meshgrid(np.arange(lo[0],hi[0]+1),np.arange(lo[1],hi[1]+1),indexing='ij')
            px=self.o[0]+(xs+0.5)*cell; py=self.o[1]+(ys+0.5)*cell
            den=(B[1]-C[1])*(A[0]-C[0])+(C[0]-B[0])*(A[1]-C[1])
            if abs(den)<1e-14: continue
            w0=((B[1]-C[1])*(px-C[0])+(C[0]-B[0])*(py-C[1]))/den
            w1=((C[1]-A[1])*(px-C[0])+(A[0]-C[0])*(py-C[1]))/den
            w2=1-w0-w1; m=(w0>=-0.02)&(w1>=-0.02)&(w2>=-0.02)
            if not m.any(): continue
            z=w0*sA+w1*sB+w2*sC
            xi=xs[m];yi=ys[m];zz=z[m]
            ok=(xi>=0)&(yi>=0)&(xi<self.shape[0])&(yi<self.shape[1])
            np.maximum.at(depth,(xi[ok],yi[ok]),zz[ok])
        self.mask0=depth>-1e8
        self.mask0=ndimage.binary_closing(self.mask0,iterations=2)
        r=max(int(round(dilate/cell)),0)
        self.mask=ndimage.binary_dilation(self.mask0,iterations=r) if r else self.mask0
        # fill depth by nearest
        idx=ndimage.distance_transform_edt(~(depth>-1e8),return_distances=False,return_indices=True)
        self.depth=depth[tuple(idx)]
    def proj(self,X): return np.c_[X@self.e1,X@self.e2]
    def query(self,X):
        q=self.proj(X); ij=np.floor((q-self.o)/self.cell).astype(int)
        ok=(ij[:,0]>=0)&(ij[:,1]>=0)&(ij[:,0]<self.shape[0])&(ij[:,1]<self.shape[1])
        inside=np.zeros(len(X),bool); dz=np.full(len(X),np.nan)
        ii=ij[ok]; inside[ok]=self.mask[ii[:,0],ii[:,1]]
        dz[ok]=X[ok]@self.d-self.depth[ii[:,0],ii[:,1]]
        return inside,dz
def _sdf_grid(self):
    if hasattr(self,'_sd'): return self._sd
    m=self.mask0
    din=ndimage.distance_transform_edt(m)*self.cell; dout=ndimage.distance_transform_edt(~m)*self.cell
    self._sd=np.where(m,-din+0.5*self.cell,dout-0.5*self.cell); return self._sd
def sdf(self,X,dzmin=-0.06,dzmax=0.08,shift=0.0):
    sd=_sdf_grid(self); q=self.proj(X); g=(q-self.o)/self.cell-0.5
    v=ndimage.map_coordinates(sd,[g[:,0],g[:,1]],order=1,mode='nearest')
    ij=np.clip(np.floor((q-self.o)/self.cell).astype(int),0,np.array(self.shape)-1)
    dz=X@self.d-self.depth[ij[:,0],ij[:,1]]
    out=(dz<dzmin)|(dz>dzmax)|(g[:,0]<0)|(g[:,1]<0)|(g[:,0]>self.shape[0]-1)|(g[:,1]>self.shape[1]-1)
    return np.where(out,1.0,v+shift)
Footprint.sdf=sdf
