"""Item 32 (Fusion 2012): borda de baixo do para-choque dianteiro refeita, lisa de um canto ao outro.
O lábio (da ponta em z≈0,079 até a borda de baixo) tinha camadas de pele sobrepostas e cruzadas (sobras do 2018,
do enxerto e da grade do item 1): serrilhado e manchas no sombreado. Em KIT00_BODY_A–E, para |y| ≤ 0,70:
- perfil da lataria em cada fatia de 1 cm em y: reta x = a(y) + b(y)·(z − 0,079) ajustada ao ponto mais à frente
  da pele (raio ao longo de x), com a borda de baixo zb(y); a(y), b(y) e zb(y) suavizados em y (gaussiano de 4 cm);
- a pele antiga do lábio (e camadas escondidas até 3 cm atrás) sai e entra uma superfície regrada lisa nesse perfil,
  com normais da própria superfície e UV da pintura mais próxima; de |y| 0,70 para fora os cantos ficam como estão."""
import sys;sys.path.insert(0,'/home/claude/v3/versions/v3-fusion-ajm3899/scripts');sys.path.insert(0,'/home/claude/c12')
import numpy as np,geo
from partmesh import PartMesh
from xray import xcast
from scipy.ndimage import gaussian_filter1d
from scipy.spatial import cKDTree
SKIN=0xB637F71F; ZT=0.079; YL=0.70; YE=0.705
STEP={'A':(0.01,6),'B':(0.02,4),'C':(0.04,3),'D':(0.08,2),'E':(0.08,2)}
PROFILE={}
def profile(pm):
    F=np.concatenate([g['F'] for g in pm.groups if pm.tex[g['ti']]==SKIN]); C=pm.P[F].mean(1)
    Fr=F[(C[:,0]>1.95)&(C[:,2]<0.1)&(C[:,2]>-0.05)]
    ys=np.arange(-0.74,0.7401,0.01); zs=np.arange(-0.03,ZT+1e-9,0.0025)
    A=[];B=[];ZB=[]
    for y in ys:
        x=xcast(pm.P,Fr,np.c_[np.full(len(zs),y),zs],'max'); ok=~np.isnan(x)
        # contiguous run ending at the top
        idx=np.nonzero(ok)[0]
        if not len(idx): A.append(np.nan);B.append(np.nan);ZB.append(np.nan);continue
        top=idx[-1]; k=top
        while k-1>=0 and ok[k-1]: k-=1
        zz=zs[k:top+1]; xx=x[k:top+1]; m=np.ones(len(zz),bool)
        for it in range(3):
            c=np.polyfit(zz[m]-ZT,xx[m],1); r=np.abs(np.polyval(c,zz-ZT)-xx); m=r<max(0.003,2.5*np.median(r))
        A.append(c[1]);B.append(c[0]);ZB.append(zz[0])
    A,B,ZB=map(np.array,(A,B,ZB))
    for arr in (A,B,ZB):
        bad=np.isnan(arr); arr[bad]=np.interp(ys[bad],ys[~bad],arr[~bad])
    s=4
    return ys,gaussian_filter1d(A,s,mode='nearest'),gaussian_filter1d(B,s,mode='nearest'),gaussian_filter1d(ZB,s,mode='nearest')-0.002
def fix(pm,prof,verbose=False):
    ys,A,Bs,ZB=prof; L=pm.name[-1]; dy,nr=STEP[L]
    a=lambda y: np.interp(y,ys,A); b=lambda y: np.interp(y,ys,Bs); zb=lambda y: np.interp(y,ys,ZB)
    xs=lambda y,z: a(y)+b(y)*(z-ZT)
    g=[g for g in pm.groups if pm.tex[g['ti']]==SKIN][0]; F=g['F']; T=pm.P[F]
    ay=np.abs(T[:,:,1]); zmin=zb(T[:,:,1])-0.004
    inside=(ay.max(1)<YL)&(T[:,:,2].max(1)<=ZT+0.0005)&(T[:,:,2]>=zmin).all(1)&(T[:,:,0].min(1)>1.95)
    near=(T[:,:,0]>xs(T[:,:,1],T[:,:,2])-0.03).all(1)
    rm=inside&near
    fi=np.unique(F[~rm].ravel()); kd=cKDTree(pm.P[fi][:,1:])
    g['F']=F[~rm]
    yv=np.r_[np.arange(-YE,YE,dy),YE]; t=np.linspace(0,1,nr+1)
    Y,Tt=np.meshgrid(yv,t); Zg=ZT+(zb(Y)-ZT)*Tt; Xg=xs(Y,Zg)
    P=np.c_[Xg.ravel(),Y.ravel(),Zg.ravel()]
    # normal of the ruled surface: dP/dy x dP/dz
    e=1e-4; dPy=np.c_[(xs(Y.ravel()+e,Zg.ravel())-xs(Y.ravel()-e,Zg.ravel()))/(2*e),np.ones(P.shape[0]),np.zeros(P.shape[0])]
    dPz=np.c_[b(Y.ravel()),np.zeros(P.shape[0]),np.ones(P.shape[0])]
    N=np.cross(dPy,dPz); N*=np.sign(N[:,0:1]); N/=np.linalg.norm(N,axis=1,keepdims=True)
    nx=len(yv); Fn=[]
    for j in range(nr):
        for i in range(nx-1):
            p=j*nx+i; q=p+1; r_=p+nx; s_=r_+1; Fn+=[(p,q,s_),(p,s_,r_)]
    Fn=np.array(Fn); fn=np.cross(P[Fn[:,1]]-P[Fn[:,0]],P[Fn[:,2]]-P[Fn[:,0]]); Fn=np.where((fn[:,0]<0)[:,None],Fn[:,[0,2,1]],Fn)
    _,nn=kd.query(P[:,1:]); o=pm.add_verts(P,N,pm.UV[fi[nn]],pm.C[fi[nn]])
    g['F']=np.r_[g['F'],Fn+o]
    if verbose: print('  ',pm.name,'old lip tris removed',rm.sum(),'new tris',len(Fn))
    return rm.sum(),len(Fn)
if __name__=='__main__':
    Z={p['name']:p for p in geo.load(sys.argv[1])}; recs=[]
    prof=profile(PartMesh(Z['COBALTSS_KIT00_BODY_A']))
    for L in 'ABCDE':
        pm=PartMesh(Z['COBALTSS_KIT00_BODY_%s'%L]); fix(pm,prof,True); recs.append(pm)
    with open(sys.argv[2],'wb') as f:
        for pm in recs: b,nv=pm.record(); f.write(b); print(pm.name,'verts',nv)
