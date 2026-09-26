"""Item 30 (Fusion 2012): faróis de milha redondos (sem a "perninha") e mais à frente.
- A "perninha" era um triângulo solto de 120 cm² do Mondeo a x≈1,87 m (35 cm atrás do para-choque), visível pelo
  furo da lataria, que seguia a silhueta de toda a peça. Removido, junto com os pedacinhos finos (≤8 triângulos)
  que escapam do aro em cima e embaixo.
- A peça do farol de milha (z < 0,35 nas peças KIT00_LEFT/RIGHT_HEADLIGHT_A–D) avança com uma rotação em torno do
  eixo vertical que acompanha a curva do para-choque: +0,8 cm na ponta interna (|y| 0,54) e +2,0 cm na externa
  (|y| 0,78). A base do aro cromado, que descia ~6 mm abaixo da borda inferior da moldura ("calo"), sobe até
  essa borda. A borda da moldura fica ~8–10 mm atrás da lataria (antes 18–38 mm)."""
import sys;sys.path.insert(0,'/home/claude/v3/versions/v3-fusion-ajm3899/scripts');sys.path.insert(0,'/home/claude/c12')
import numpy as np,geo
from partmesh import PartMesh
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
Y1,D1,Y2,D2=0.54,0.008,0.78,0.020
b=(D2-D1)/(Y2-Y1); Y0=0.66; DX0=D1+b*(Y0-Y1); X0=2.15
def fog(pm):
    n_rm=0
    for g in pm.groups:
        F=g['F']; T=pm.P[F]
        zone=(T[:,:,2]<0.35).all(1)
        stray=zone&(T[:,:,0].max(1)<1.95)
        # small loose pieces: connected components (welded) of the fog zone with <=8 triangles in front
        Fz=np.nonzero(zone&~stray)[0]
        key=np.round(pm.P/1e-4).astype(np.int64); _,w=np.unique(key,axis=0,return_inverse=True); w=w.ravel()
        W=w[F[Fz]]; n=w.max()+1
        r=np.r_[W[:,0],W[:,1],W[:,2]]; c=np.r_[W[:,1],W[:,2],W[:,0]]
        _,lab=connected_components(coo_matrix((np.ones(len(r)),(r,c)),shape=(n,n)),directed=False)
        fl=lab[W[:,0]]; u,cnt=np.unique(fl,return_counts=True); small=set(u[cnt<=8])
        piece=np.zeros(len(F),bool)
        for i,t in enumerate(Fz):
            if fl[i] in small and T[t,:,0].mean()>2.14: piece[t]=True
        rm=stray|piece; g['F']=F[~rm]; n_rm+=rm.sum()
    # "calo": the bottom of the chrome ring collar dips ~6 mm below the bezel's lower edge (|y| 0.645-0.69):
    # lift those vertices onto the bezel edge line
    v=np.unique(np.concatenate([g['F'] for g in pm.groups]))
    ay=np.abs(pm.P[v,1]); z=pm.P[v,2]
    zl=np.interp(ay,[0.645,0.69],[0.1526,0.1555])
    k=(ay>=0.645)&(ay<=0.69)&(z<zl)&(pm.P[v,0]>1.95)
    pm.P[v[k],2]=zl[k]; n_lift=k.sum()
    # rigid move of the fog-light vertices
    v=np.unique(np.concatenate([g['F'] for g in pm.groups]))
    v=v[(pm.P[v,2]<0.35)&(pm.P[v,0]>1.95)]
    sg=np.sign(pm.P[v,1].mean()); th=-sg*b; c,s=np.cos(th),np.sin(th); y0=sg*Y0
    x=pm.P[v,0]-X0; y=pm.P[v,1]-y0
    pm.P[v,0]=X0+c*x-s*y+DX0; pm.P[v,1]=y0+s*x+c*y
    nx,ny=pm.N[v,0].copy(),pm.N[v,1].copy(); pm.N[v,0]=c*nx-s*ny; pm.N[v,1]=s*nx+c*ny
    return n_rm,len(v),n_lift
if __name__=='__main__':
    Z={p['name']:p for p in geo.load(sys.argv[1])}; recs=[]
    for L in 'ABCD':
        for s in ('LEFT','RIGHT'):
            pm=PartMesh(Z['COBALTSS_KIT00_%s_HEADLIGHT_%s'%(s,L)]); r,nv,nl=fog(pm); recs.append(pm)
            print(pm.name,'removed tris',r,'moved verts',nv,'lifted',nl)
    with open(sys.argv[2],'wb') as f:
        for pm in recs:
            bb,nv=pm.record(); f.write(bb)
