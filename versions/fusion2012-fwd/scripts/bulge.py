"""Faróis e lanternas "para dentro da carroceria" (itens 29 e 28): a lente fica 2–7 cm abaixo do nível da lataria em
volta; a borda encosta na abertura, mas o meio afunda. Correção sem abrir frestas nem entrar no capô:
- plano da lâmpada: normal média da lente (n) e eixos (a, b) no plano; alturas ao longo de n;
- superfície da lataria "contínua" por cima da abertura: thin-plate (RBF) ajustada à camada mais externa da
  lataria/capô num anel de 1,5–7 cm em volta da lente;
- deslocamento ao longo de n = max(0, superfície − 3 mm − lente), multiplicado por uma rampa de 0 na borda da lente a 1
  a 3 cm para dentro; aplicado a todas as peças da lâmpada (lente, interior, fundos) pela posição (a,b) de cada vértice.
  A borda fica onde está (sem frestas), o meio sobe até o nível da lataria."""
import sys;sys.path.insert(0,'/home/claude/v3/versions/v3-fusion-ajm3899/scripts');sys.path.insert(0,'/home/claude/c12')
import numpy as np,geo
from partmesh import PartMesh
from scipy.ndimage import binary_dilation,binary_fill_holes,binary_closing,distance_transform_edt,gaussian_filter
from scipy.interpolate import RBFInterpolator,RegularGridInterpolator
RES=0.004
def samp(X,F,k=6,seed=0):
    rng=np.random.default_rng(seed);r=rng.random((len(F)*k,2));r=np.where(r.sum(1,keepdims=True)>1,1-r,r);t=np.repeat(np.arange(len(F)),k)
    return X[F[t,0]]+r[:,:1]*(X[F[t,1]]-X[F[t,0]])+r[:,1:]*(X[F[t,2]]-X[F[t,0]])
def allF(pm): return np.concatenate([g['F'] for g in pm.groups if len(g['F'])])
def field(lens_pm,lens_sel,body_pms,RAMP=0.03,CLEAR=0.003,verbose=''):
    X=lens_pm.P; F=allF(lens_pm); F=F[lens_sel(X[F].mean(1))]
    fn=np.cross(X[F[:,1]]-X[F[:,0]],X[F[:,2]]-X[F[:,0]]); n=fn.sum(0); n/=np.linalg.norm(n)
    # outward: away from the car centre (x ~ 0, y ~ 0)
    c0=X[np.unique(F)].mean(0)
    if np.dot(n,c0*np.array([1,1,0]))<0: n=-n
    a=np.cross(n,[0,0,1.]); a/=np.linalg.norm(a); b=np.cross(n,a)
    proj=lambda Y: np.c_[(Y-c0)@a,(Y-c0)@b,(Y-c0)@n]
    G=proj(samp(X,F,20))
    u0,u1=G[:,0].min()-0.1,G[:,0].max()+0.1; v0,v1=G[:,1].min()-0.1,G[:,1].max()+0.1
    nu,nv=int((u1-u0)/RES)+1,int((v1-v0)/RES)+1
    iu=((G[:,0]-u0)/RES).astype(int); iv=((G[:,1]-v0)/RES).astype(int)
    Lh=np.full((nv,nu),-9.0); np.maximum.at(Lh,(iv,iu),G[:,2])
    M=Lh>-8; M=binary_fill_holes(binary_closing(M,iterations=2))
    Lh=np.where(Lh>-8,Lh,np.nan)
    # fill lens height holes by nearest
    _,(jj,ii)=distance_transform_edt(np.isnan(Lh),return_indices=True); Lf=Lh[jj,ii]
    D=distance_transform_edt(~M)*RES; Din=distance_transform_edt(M)*RES
    pts=[]
    for pm in body_pms:
        Y=pm.P; FF=allF(pm); C=Y[FF].mean(1); m=np.linalg.norm(C-c0,axis=1)<0.5
        pts.append(proj(samp(Y,FF[m],4)))
    B=np.concatenate(pts); bu=((B[:,0]-u0)/RES).astype(int); bv=((B[:,1]-v0)/RES).astype(int)
    ok=(bu>=0)&(bu<nu)&(bv>=0)&(bv<nv); B=B[ok]; bu=bu[ok]; bv=bv[ok]; d=D[bv,bu]
    ring=(d>0.015)&(d<0.07)&(np.abs(B[:,2])<0.15)
    Bh=np.full((nv,nu),-9.0); np.maximum.at(Bh,(bv[ring],bu[ring]),B[ring,2])
    rv,ru=np.nonzero(Bh>-8); Q=np.c_[u0+(ru+0.5)*RES,v0+(rv+0.5)*RES]; H=Bh[rv,ru]
    sel=np.random.default_rng(1).choice(len(Q),min(1500,len(Q)),replace=False)
    rbf=RBFInterpolator(Q[sel],H[sel],kernel='thin_plate_spline',smoothing=5e-3)
    UU,VV=np.meshgrid(u0+(np.arange(nu)+0.5)*RES,v0+(np.arange(nv)+0.5)*RES)
    S=np.full((nv,nu),np.nan); S[M]=rbf(np.c_[UU[M],VV[M]])
    off=np.where(M,np.clip(S-CLEAR-Lf,0,None)*np.clip(Din/RAMP,0,1),0.0)
    off=gaussian_filter(off,1.5)*M
    if verbose:
        h=(Lf-S)[M]; print(verbose,'lens vs surface median %+.4f p10 %+.4f | offset max %.4f median(in) %.4f'%(np.nanmedian(h),np.nanpercentile(h,10),off.max(),np.median(off[M])))
    it=RegularGridInterpolator((v0+(np.arange(nv)+0.5)*RES,u0+(np.arange(nu)+0.5)*RES),off,bounds_error=False,fill_value=0.0)
    return dict(proj=proj,n=n,it=it,info=dict(M=M,off=off,S=S,L=Lf,grid=(u0,v0,nu,nv)))
def apply(pm,fld,sel):
    P=pm.P; v=np.unique(allF(pm)); v=v[sel(P[v])]
    Q=fld['proj'](P[v]); o=fld['it'](np.c_[Q[:,1],Q[:,0]])
    pm.P[v]+=o[:,None]*fld['n']
    return len(v),o.max()
