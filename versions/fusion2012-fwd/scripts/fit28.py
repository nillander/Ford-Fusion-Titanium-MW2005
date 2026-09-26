"""Item 28 (Fusion 2012): lanternas traseiras do tamanho do nicho da lataria.
A lanterna 2012 (Mondeo) é menor que a abertura do 2018: sobra uma faixa escura (paredes do nicho) em volta,
maior no canto inferior interno da tampa e na ponta de cima da lateral. Em vez de escalar a peça inteira (ela
entraria na lataria onde já encaixa), a lanterna é "esticada" até a borda do nicho:
- coordenadas cilíndricas em volta de um eixo vertical em (x -1,80; |y| 0,30): u = ângulo × 0,49 m (ao longo da
  lanterna), z, e r (profundidade);
- raster (2 mm) da lente e da lataria nessas coordenadas; a superfície da lataria em volta é ajustada por um
  polinômio r(u,z); "fresta" = ponto sem lente onde a lataria está >8 mm abaixo dessa superfície, até 7 cm da lente;
- para cada ponto da borda da lente, deslocamento até a borda do nicho (menos 2 mm) e profundidade até 3 mm acima
  da lataria afundada nesse ponto; interpolado para toda a lanterna (RBF thin-plate) e aplicado a todas as peças da
  lanterna (lentes, interior, fundos), LODs A–D."""
import sys;sys.path.insert(0,'/home/claude/v3/versions/v3-fusion-ajm3899/scripts');sys.path.insert(0,'/home/claude/c12')
import numpy as np,geo
from partmesh import PartMesh
from scipy.ndimage import binary_fill_holes,binary_dilation,binary_closing,distance_transform_edt,label
from scipy.interpolate import RBFInterpolator
C0=np.array((-1.80,0.30)); R0=0.49; RES=0.002; MARGIN=0.002; MAXD=0.035; GAPDEPTH=0.008
def polar(X,sg):
    dx=X[:,0]-C0[0]; dy=sg*X[:,1]-C0[1]; th=np.arctan2(dy,dx)
    return np.c_[th*R0,X[:,2],np.hypot(dx,dy)]
def unpolar(U,sg):
    th=U[:,0]/R0; return np.c_[C0[0]+U[:,2]*np.cos(th),sg*(C0[1]+U[:,2]*np.sin(th)),U[:,1]]
def raster(U,F,grid):
    u0,z0,nu,nz=grid; img=np.full((nz,nu),np.nan)
    T=U[F]
    for t in T:
        a=((t[:,0]-u0)/RES);b=((t[:,1]-z0)/RES)
        i0,i1=int(max(np.floor(a.min()),0)),int(min(np.ceil(a.max()),nu-1)); j0,j1=int(max(np.floor(b.min()),0)),int(min(np.ceil(b.max()),nz-1))
        if i1<i0 or j1<j0: continue
        I,J=np.meshgrid(np.arange(i0,i1+1),np.arange(j0,j1+1)); px=I.ravel()+0.5; py=J.ravel()+0.5
        d=(b[1]-b[2])*(a[0]-a[2])+(a[2]-a[1])*(b[0]-b[2])
        if abs(d)<1e-12: continue
        w0=((b[1]-b[2])*(px-a[2])+(a[2]-a[1])*(py-b[2]))/d; w1=((b[2]-b[0])*(px-a[2])+(a[0]-a[2])*(py-b[2]))/d; w2=1-w0-w1
        m=(w0>=-1e-6)&(w1>=-1e-6)&(w2>=-1e-6)
        if not m.any(): continue
        r=w0[m]*t[0,2]+w1[m]*t[1,2]+w2[m]*t[2,2]; jj=J.ravel()[m]; ii=I.ravel()[m]
        cur=img[jj,ii]; img[jj,ii]=np.where(np.isnan(cur),r,np.maximum(cur,r))
    return img
def field(Z,sg,verbose=True):
    side='LEFT' if sg>0 else 'RIGHT'
    g=PartMesh(Z['COBALTSS_KIT00_%s_BRAKELIGHT_GLASS_A'%side]); Fg=np.concatenate([x['F'] for x in g.groups])
    Ug=polar(g.P,sg); zone=(g.P[Fg][:,:,0].mean(1)<-1.7)&(g.P[Fg][:,:,2].mean(1)>0.55); Fg=Fg[zone]
    b=PartMesh(Z['COBALTSS_KIT00_BODY_A']); Fb=np.concatenate([x['F'] for x in b.groups]); Ub=polar(b.P,sg)
    u0,u1=Ug[Fg][:,:,0].min()-0.08,Ug[Fg][:,:,0].max()+0.08; z0,z1=Ug[Fg][:,:,1].min()-0.08,Ug[Fg][:,:,1].max()+0.08
    C=Ub[Fb].mean(1); mb=(C[:,0]>u0)&(C[:,0]<u1)&(C[:,1]>z0)&(C[:,1]<z1)&(C[:,2]>0.3)&(C[:,2]<0.65)&(sg*b.P[Fb][:,:,1].mean(1)>0.2)
    nu,nz=int((u1-u0)/RES)+1,int((z1-z0)/RES)+1; grid=(u0,z0,nu,nz)
    L=raster(Ug,Fg,grid); B=raster(Ub,Fb[mb],grid)
    lens=~np.isnan(L)
    lens=binary_fill_holes(binary_closing(lens,iterations=2))
    UU,ZZ=np.meshgrid(u0+(np.arange(nu)+0.5)*RES,z0+(np.arange(nz)+0.5)*RES)
    dl=distance_transform_edt(~lens)*RES
    ring=(dl>0.03)&(dl<0.10)&~np.isnan(B)
    def A(u,z): u=(u-UU.mean());z=(z-ZZ.mean()); return np.stack([np.ones_like(u),u,z,u*u,u*z,z*z,u**3,u*u*z,u*z*z,z**3],-1)
    m=ring.copy()
    for it in range(4):
        c,*_=np.linalg.lstsq(A(UU[m],ZZ[m]),B[m],rcond=None); res=B-A(UU,ZZ)@c; m=ring&(np.abs(res)<max(0.004,3*np.median(np.abs(res[m]))))
    fit=A(UU,ZZ)@c
    gap=(~lens)&(np.isnan(B)|(B<fit-GAPDEPTH))&(dl<0.07)
    lab,n=label(gap|lens); niche=lab==lab[lens][0] if lens.any() else lens
    niche=binary_fill_holes(binary_closing(niche,iterations=3))
    # rim of the lens: ordered contour; march along the outward normal until leaving the niche
    from skimage.measure import find_contours
    from scipy.ndimage import median_filter,gaussian_filter1d
    cs=find_contours(lens.astype(float),0.5); c=max(cs,key=len)
    d=np.r_[0,np.cumsum(np.linalg.norm(np.diff(c,axis=0),axis=1))]; n=int(d[-1]/1.5); s_=np.linspace(0,d[-1],n,endpoint=False)
    c=np.c_[np.interp(s_,d,c[:,0]),np.interp(s_,d,c[:,1])]          # (row=z, col=u) in pixels
    t=np.roll(c,-3,0)-np.roll(c,3,0); nrm=np.c_[t[:,1],-t[:,0]]; nrm/=np.linalg.norm(nrm,axis=1,keepdims=True)+1e-9
    probe=c+nrm*4
    ins=lens[np.clip(probe[:,0].astype(int),0,nz-1),np.clip(probe[:,1].astype(int),0,nu-1)]
    if ins.mean()>0.5: nrm=-nrm
    dist=np.zeros(len(c))
    for i,(p,q) in enumerate(zip(c,nrm)):
        k=1
        while k<int(MAXD/RES):
            y,x=(p+q*k).astype(int)
            if y<0 or x<0 or y>=nz or x>=nu or not niche[y,x]: break
            k+=1
        dist[i]=(k-1)*RES
    dist=median_filter(dist,size=15,mode='wrap'); dist=gaussian_filter1d(dist,8,mode='wrap')
    dist=np.clip(dist-MARGIN,0,MAXD)
    ri=(np.clip(c[:,0].astype(int),0,nz-1),np.clip(c[:,1].astype(int),0,nu-1))
    P0=np.c_[u0+(c[:,1]+0.5)*RES,z0+(c[:,0]+0.5)*RES]
    D=np.c_[nrm[:,1],nrm[:,0]]*dist[:,None]
    # depth: the moved rim sits 3 mm above the (sunken) skin at its new place
    def filled(img):
        nan=np.isnan(img); _,(jj,ii)=distance_transform_edt(nan,return_indices=True); return img[jj,ii]
    Bs=filled(B); Ls=filled(np.where(lens,L,np.nan))
    moved=np.linalg.norm(D,axis=1)>1e-4
    ti2=np.clip(((P0[:,0]+D[:,0]-u0)/RES).astype(int),0,nu-1); tj2=np.clip(((P0[:,1]+D[:,1]-z0)/RES).astype(int),0,nz-1)
    Dr=np.where(moved,Bs[tj2,ti2]+0.003-Ls[ri],0.0); Dr=gaussian_filter1d(np.minimum(Dr,0.0),8,mode='wrap')
    D3=np.c_[D,Dr]
    sel=np.arange(0,len(P0),max(1,len(P0)//300))
    rbf=RBFInterpolator(P0[sel],D3[sel],kernel='thin_plate_spline',smoothing=1e-3)
    fitf=lambda u,z: A(np.asarray(u),np.asarray(z))@c
    if verbose:
        dd=np.linalg.norm(D,axis=1); print(side,'grid',nu,nz,'lens px',lens.sum(),'gap px',(niche&~lens).sum(),'rim',len(P0),'disp median %.4f p90 %.4f max %.4f'%(np.median(dd),np.percentile(dd,90),dd.max()))
    return rbf,fitf,dict(Dr=Dr,L=L,B=B,lens=lens,niche=niche,fit=fit,grid=grid,P0=P0,D=D)
def apply(pm,sg,rbf,fitf):
    P=pm.P; v=np.unique(np.concatenate([g['F'] for g in pm.groups if len(g['F'])]))
    v=v[(P[v,0]<-1.7)&(P[v,2]>0.55)&(sg*P[v,1]>0.25)]
    U=polar(P[v],sg); D3=rbf(U[:,:2]); D=D3[:,:2]
    Un=U.copy(); Un[:,:2]+=D; Un[:,2]+=np.minimum(D3[:,2],0)
    pm.P[v]=unpolar(Un,sg)
    dth=D[:,0]/R0*sg; c,s=np.cos(dth),np.sin(dth); nx,ny=pm.N[v,0].copy(),pm.N[v,1].copy()
    pm.N[v,0]=c*nx-s*ny; pm.N[v,1]=s*nx+c*ny
    return len(v),np.abs(D).max()
if __name__=='__main__':
    Z={p['name']:p for p in geo.load(sys.argv[1])}; recs=[]
    import pickle; dbg={}
    for sg,side in ((1,'LEFT'),(-1,'RIGHT')):
        rbf,fitf,info=field(Z,sg); dbg[side]=info
        for L in 'ABCD':
            for part in ('BRAKELIGHT','BRAKELIGHT_GLASS'):
                pm=PartMesh(Z['COBALTSS_KIT00_%s_%s_%s'%(side,part,L)]); n,mx=apply(pm,sg,rbf,fitf); recs.append(pm)
                print(' ',pm.name,'verts moved',n,'max disp %.3f'%mx)
    pickle.dump(dbg,open('build/fit28dbg.pkl','wb'))
    with open(sys.argv[2],'wb') as f:
        for pm in recs: b,nv=pm.record(); f.write(b)
