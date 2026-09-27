"""Item 29 (parte 2): frestas escuras entre a lataria e o farol (pontas e embaixo do farol).
No plano do farol (depois de trazê-lo para fora), raster de 3 mm da lente e da lataria/capô/peças pretas próximas
(até 3,5 cm abaixo do plano da lente): "fresta" = sem lente nem lataria, até 5 cm da lente, manchas > 0,2 cm².
Cada fresta é fechada com pele pintada (grupo da pintura de KIT00/01/02_BODY_A–E): altura interpolada (RBF) da
lataria em volta, 8 mm para dentro (fica escondida sob a lataria onde as duas se sobrepõem), com normais da própria superfície e UV da pintura mais próxima."""
import sys;sys.path.insert(0,'/home/claude/c12');sys.path.insert(0,'/home/claude/v3/versions/v3-fusion-ajm3899/scripts')
import numpy as np,geo
from partmesh import PartMesh
from hlgap import masks,RES
from scipy.ndimage import binary_dilation,distance_transform_edt
from scipy.interpolate import RBFInterpolator
from scipy.spatial import Delaunay,cKDTree
SKIN=0xB637F71F
def patch_geom(d,K=3):
    n,a,b,c0=d['frame']; u0,v0,nu,nv=d['grid']; gap=d['gap']&~d['lens']&(distance_transform_edt(~d['lens'])*RES<0.025)
    Bh=d['Bh']; ring=binary_dilation(gap,iterations=4)&~gap&~np.isnan(Bh)
    rv,ru=np.nonzero(ring); Q=np.c_[u0+(ru+0.5)*RES,v0+(rv+0.5)*RES]
    if len(Q)<10: return None
    sel=np.random.default_rng(0).choice(len(Q),min(1200,len(Q)),replace=False)
    rbf=RBFInterpolator(Q[sel],Bh[rv,ru][sel],kernel='thin_plate_spline',smoothing=1e-3)
    from skimage.measure import find_contours
    from scipy.ndimage import gaussian_filter
    sp=RES*K
    pts=[]
    for c in find_contours(np.pad(gaussian_filter(gap.astype(float),0.8),1),0.5):
        c=c-1; dd=np.r_[0,np.cumsum(np.linalg.norm(np.diff(c,axis=0),axis=1))]*RES
        if dd[-1]<0.01: continue
        s_=np.linspace(0,dd[-1],max(4,int(dd[-1]/sp)+1)); pts.append(np.c_[u0+(np.interp(s_,dd,c[:,1])+0.5)*RES,v0+(np.interp(s_,dd,c[:,0])+0.5)*RES])
    if not pts: return None
    Bd=np.concatenate(pts)
    gy,gx=np.meshgrid(np.arange(0,gap.shape[0],K),np.arange(0,gap.shape[1],K),indexing='ij')
    from scipy.ndimage import binary_erosion
    inner=binary_erosion(gap,iterations=max(1,K//2)); m=inner[gy,gx]
    Gi=np.c_[u0+(gx[m]+0.5)*RES,v0+(gy[m]+0.5)*RES]
    UV2=np.r_[Bd,Gi]; _,uq=np.unique(np.round(UV2/(sp*0.3)),axis=0,return_index=True); UV2=UV2[np.sort(uq)]
    F=Delaunay(UV2).simplices; cc=UV2[F].mean(1)
    iu=np.clip(((cc[:,0]-u0)/RES).astype(int),0,gap.shape[1]-1); iv=np.clip(((cc[:,1]-v0)/RES).astype(int),0,gap.shape[0]-1)
    F=F[gap[iv,iu]]
    used=np.unique(F); rm=-np.ones(len(UV2),int); rm[used]=np.arange(len(used)); UV2=UV2[used]; F=rm[F]
    h=rbf(UV2)-0.008
    P=c0+UV2[:,:1]*a+UV2[:,1:]*b+h[:,None]*n
    fn=np.cross(P[F[:,1]]-P[F[:,0]],P[F[:,2]]-P[F[:,0]]); F=np.where(((fn@n)<0)[:,None],F[:,[0,2,1]],F)
    fn=np.cross(P[F[:,1]]-P[F[:,0]],P[F[:,2]]-P[F[:,0]]); N=np.zeros_like(P)
    for k in range(3): np.add.at(N,F[:,k],fn)
    N/=np.maximum(np.linalg.norm(N,axis=1,keepdims=True),1e-12)
    return P,N,F
def add(pm,geoms):
    g=[g for g in pm.groups if pm.tex[g['ti']]==SKIN][0]; fi=np.unique(g['F'].ravel()); kd=cKDTree(pm.P[fi]); n=0
    for P,N,F in geoms:
        _,nn=kd.query(P); o=pm.add_verts(P,N,pm.UV[fi[nn]],pm.C[fi[nn]]); g['F']=np.r_[g['F'],F+o]; n+=len(P)
    return n
if __name__=='__main__':
    Z={p['name']:p for p in geo.load(sys.argv[1])}; G={}
    D={side:masks(Z,side) for side in ('LEFT','RIGHT')}
    for L,K in (('A',3),('B',5),('C',8),('D',12),('E',12)):
        G[L]=[g for g in (patch_geom(D[s],K) for s in D) if g]
        print(L,'patch verts',sum(len(g[0]) for g in G[L]))
    recs=[]
    for k in ('KIT00','KIT01','KIT02','KIT04','KIT05'):
        for L in 'ABCDE':
            pm=PartMesh(Z['COBALTSS_%s_BODY_%s'%(k,L)]); add(pm,G[L]); recs.append(pm)
    with open(sys.argv[2],'wb') as f:
        for pm in recs:
            b,nv=pm.record(); f.write(b); print(pm.name,nv,'!!' if nv>65535 else '')
