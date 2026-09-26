"""Item 1 (Fusion 2012): a grade preta inferior não liga os faróis de milha (fotos do 2013).
- A grade termina em |y| = YE(z): 0,40 embaixo (z 0,08) a 0,46 em cima (z 0,19); ponta inclinada como no 2013.
  Os triângulos pretos da grade além disso são recortados (RIGHT_SIDE_MIRROR_A no LOD A, BASE_B–E nos outros).
- O vão entre a ponta da grade e o canto do para-choque é fechado com pele pintada (grupo da pintura de cada
  carroceria KIT00/01/02, LODs A–E): superfície lisa ajustada à lataria em volta da abertura, 3 mm para dentro,
  com um furo no contorno do nicho do farol de milha (fica uma moldura preta de ~5 mm, como no 2013) e uma parede
  de 4 cm na ponta da grade."""
import sys;sys.path.insert(0,'/home/claude/v3/versions/v3-fusion-ajm3899/scripts');sys.path.insert(0,'/home/claude/c12')
import numpy as np,geo
from xray import xcast
from partmesh import PartMesh,clip_tris
from scipy.spatial import cKDTree,Delaunay
from scipy.ndimage import binary_dilation
from skimage.measure import find_contours
from matplotlib.path import Path
SKIN=0xB637F71F; BLACK=0xE67A0B4A
def YE(z): return 0.40+np.clip((np.asarray(z)-0.08)/0.11,0,1)*0.06
ZLO,ZHI,YC=0.0795,0.212,0.95
RES=0.005
STEP={'A':0.03,'B':0.035,'C':0.05,'D':0.07,'E':0.07}
def tris(pm,texh):
    F=[g['F'] for g in pm.groups if pm.tex[g['ti']]==texh and len(g['F'])]
    return np.concatenate(F) if F else np.zeros((0,3),int)
def front(P,F):
    C=P[F].mean(1); m=(C[:,0]>1.85)&(C[:,2]<0.45)&(C[:,2]>-0.05); return P,F[m]
def fitsurf(sk):
    """x = f(|y|,z) fitted to the bumper skin around the opening (both sides)"""
    Q=[]
    for y in np.arange(0.36,0.93,0.01):
        for z in np.r_[np.arange(0.195,0.30,0.01)]:
            if 0.52<y<0.85 and z<0.285: continue
            Q.append((y,z))
        Q.append((y,0.0805))
    Q=np.array(Q); X=[]
    for sg in (1,-1): X.append(sk(np.c_[sg*Q[:,0],Q[:,1]]))
    Q=np.r_[Q,Q]; X=np.r_[X[0],X[1]]; ok=~np.isnan(X); Q=Q[ok]; X=X[ok]
    def A(y,z): y=np.asarray(y);z=np.asarray(z); return np.stack([np.ones_like(y),y,y**2,y**3,y**4,z,z**2,y*z,y**2*z],-1)
    m=np.ones(len(X),bool)
    for it in range(4):
        c,*_=np.linalg.lstsq(A(Q[m,0],Q[m,1]),X[m],rcond=None); r=np.abs(A(Q[:,0],Q[:,1])@c-X); m=r<max(0.004,3*np.median(r))
    f=lambda y,z: A(y,z)@c
    fy=lambda y,z: (A(np.asarray(y)+1e-4,z)@c-A(np.asarray(y)-1e-4,z)@c)/2e-4
    fz=lambda y,z: (A(y,np.asarray(z)+1e-4)@c-A(y,np.asarray(z)-1e-4)@c)/2e-4
    return f,fy,fz,np.median(r[m]),r.max()
def patch(pm,pods,verbose=False):
    L=pm.name[-1]; st=STEP[L]
    SP,SF=front(pm.P,tris(pm,SKIN))
    sk=lambda Q: xcast(SP,SF,np.asarray(Q,float),'max')
    def pd(Q):
        r=np.stack([xcast(P,F,np.asarray(Q,float),'max') for P,F in pods]); r=np.where(np.isnan(r),-9,r).max(0); return np.where(r<-8,np.nan,r)
    f,fy,fz,med,mx=fitsurf(sk)
    if verbose: print('  fit residual median %.4f max %.4f'%(med,mx))
    fi=np.unique(SF); kd=cKDTree(SP[fi][:,1:])
    ys=np.arange(0.38,YC,RES); zs=np.arange(ZLO-2*RES,ZHI+2*RES,RES)
    YY,ZZ=np.meshgrid(ys,zs)
    newP=[];newN=[];newF=[]
    for sg in (1,-1):
        Q=np.c_[sg*YY.ravel(),ZZ.ravel()]; xs=sk(Q).reshape(YY.shape); xp=pd(Q).reshape(YY.shape); fv=f(YY,ZZ)
        # lateral extent of the car at each z (skin seen from the front)
        has=~np.isnan(xs); yside=np.array([ys[np.nonzero(r)[0].max()] if r.any() else 0 for r in has])[:,None]
        region=(YY>=YE(ZZ))&(YY<=yside-0.005)&(ZZ>=ZLO)&(ZZ<=ZHI)
        # skin just behind the patch (0,3-1,3 cm) would be crossed by it: leave those out; skin in front hides the
        # patch, skin far behind (old niche walls) gets covered
        near=has&(xs<fv-0.003)&(xs>=fv-0.013)
        hole=binary_dilation(~np.isnan(xp),iterations=1)|near
        M=region&~hole
        # boundary points (contours) + interior grid
        pts=[]
        for c in find_contours(np.pad(M.astype(float),1),0.5):
            c=c-1; zc=ZLO-2*RES+np.clip(c[:,0],0,len(zs)-1)*RES; yc=0.38+np.clip(c[:,1],0,len(ys)-1)*RES
            yc=np.maximum(yc,YE(zc)); zc=np.clip(zc,ZLO,ZHI); yc=np.minimum(yc,YC)
            seg=np.c_[yc,zc]; d=np.r_[0,np.cumsum(np.linalg.norm(np.diff(seg,axis=0),axis=1))]
            if d[-1]<0.01: continue
            s=np.linspace(0,d[-1],max(4,int(d[-1]/(st*0.6))+1))
            pts.append(np.c_[np.interp(s,d,seg[:,0]),np.interp(s,d,seg[:,1])])
        gy,gz=np.meshgrid(np.arange(0.38,YC+1e-9,st),np.arange(ZLO,ZHI+1e-9,st*0.7))
        G=np.c_[gy.ravel(),gz.ravel()]
        def inside(Pq):
            iy=np.clip(np.round((Pq[:,0]-0.38)/RES).astype(int),0,len(ys)-1); iz=np.clip(np.round((Pq[:,1]-(ZLO-2*RES))/RES).astype(int),0,len(zs)-1)
            return M[iz,iy]
        Mer=M.copy()
        # interior points must be away from the boundary
        from scipy.ndimage import binary_erosion
        Mer=binary_erosion(M,iterations=int(st*0.5/RES))
        iy=np.clip(np.round((G[:,0]-0.38)/RES).astype(int),0,len(ys)-1); iz=np.clip(np.round((G[:,1]-(ZLO-2*RES))/RES).astype(int),0,len(zs)-1)
        G=G[Mer[iz,iy]]
        V=np.r_[np.concatenate(pts),G]
        # merge near-duplicates
        _,u=np.unique(np.round(V/0.002),axis=0,return_index=True); V=V[np.sort(u)]
        T=Delaunay(V).simplices
        c=V[T].mean(1); e=np.r_[(V[T[:,0]]+V[T[:,1]])/2,(V[T[:,1]]+V[T[:,2]])/2,(V[T[:,2]]+V[T[:,0]])/2]
        keep=inside(c)&inside(e[:len(T)]*0.5+c*0.5)&inside(e[len(T):2*len(T)]*0.5+c*0.5)&inside(e[2*len(T):]*0.5+c*0.5)
        T=T[keep]
        used=np.unique(T); remap=-np.ones(len(V),int); remap[used]=np.arange(len(used)); V=V[used]; T=remap[T]
        o=sum(len(p) for p in newP)
        X3=np.c_[f(V[:,0],V[:,1])-0.003,sg*V[:,0],V[:,1]]
        Nn=np.c_[np.ones(len(V)),-fy(V[:,0],V[:,1])*sg,-fz(V[:,0],V[:,1])]; Nn/=np.linalg.norm(Nn,axis=1,keepdims=True)
        # orient faces outward (+x)
        fn=np.cross(X3[T[:,1]]-X3[T[:,0]],X3[T[:,2]]-X3[T[:,0]]); T=np.where((fn[:,0]<0)[:,None],T[:,[0,2,1]],T)
        newP.append(X3); newN.append(Nn); newF.append(T+o)
        # wall along the grille end (points of the patch on the YE line)
        wl=np.nonzero(np.abs(V[:,0]-YE(V[:,1]))<0.002)[0]; wl=wl[np.argsort(V[wl,1])]
        if len(wl)>1:
            o=sum(len(p) for p in newP)
            A=X3[wl]; B=A-(0.04,0,0); nw=np.tile((0,-sg,0.0),(len(wl),1))
            newP.append(np.r_[A,B]); newN.append(np.r_[nw,nw]); k=len(wl); WT=[]
            for i in range(k-1):
                a,b,c2,d=i,i+1,k+i+1,k+i
                t1,t2=(a,b,c2),(a,c2,d)
                WT+=[t1,t2]
            WT=np.array(WT); P3=np.r_[A,B]; fn=np.cross(P3[WT[:,1]]-P3[WT[:,0]],P3[WT[:,2]]-P3[WT[:,0]])
            WT=np.where(((fn@np.array([0,-sg,0.0]))<0)[:,None],WT[:,[0,2,1]],WT); newF.append(WT+o)
    P=np.concatenate(newP);N=np.concatenate(newN);F=np.concatenate(newF)
    _,nn=kd.query(P[:,1:]); UV=pm.UV[fi[nn]]; C=pm.C[fi[nn]]
    g=[g for g in pm.groups if pm.tex[g['ti']]==SKIN][0]
    o=pm.add_verts(P,N,UV,C); g['F']=np.r_[g['F'],F+o]
    return len(P)
def phi(X):
    X=np.asarray(X); y=np.abs(X[:,1]); z=X[:,2]
    return np.maximum.reduce([YE(z)-y+0.004, z-0.225, 0.05-z, 1.95-X[:,0], y-0.97])
def cut_grille(pm):
    n0=pm.ntris()
    for g in pm.groups:
        if pm.tex[g['ti']]!=BLACK or not len(g['F']): continue
        P2,N2,U2,C2,F2=clip_tris(pm.P,pm.N,pm.UV,pm.C,g['F'],phi)
        pm.P=np.r_[pm.P,P2]; pm.N=np.r_[pm.N,N2]; pm.UV=np.r_[pm.UV,U2]; pm.C=np.r_[pm.C,C2]; g['F']=F2
    return n0-pm.ntris()
if __name__=='__main__':
    src,out=sys.argv[1],sys.argv[2]; only=sys.argv[3] if len(sys.argv)>3 else 'ABCDE'
    Z={p['name']:p for p in geo.load(src)}; recs=[]
    def pods(L):
        L2=L if L!='E' else 'D'; r=[]
        for s in ('LEFT','RIGHT'):
            pm=PartMesh(Z['COBALTSS_KIT00_%s_HEADLIGHT_%s'%(s,L2)]); F=np.concatenate([g['F'] for g in pm.groups]); r.append(front(pm.P,F))
        return r
    for L in only:
        PD=pods(L)
        for k in ('KIT00','KIT01','KIT02'):
            pm=PartMesh(Z['COBALTSS_%s_BODY_%s'%(k,L)]); n=patch(pm,PD,k=='KIT00'); recs.append(pm); print(pm.name,'patch verts',n)
        gp=PartMesh(Z['COBALTSS_KIT00_RIGHT_SIDE_MIRROR_A' if L=='A' else 'COBALTSS_BASE_'+L])
        print(gp.name,'grille tris net removed',cut_grille(gp)); recs.append(gp)
    with open(out,'wb') as f:
        for pm in recs:
            b,nv=pm.record(); f.write(b); print('%-40s verts %d%s'%(pm.name,nv,' !!VERTS' if nv>65535 else ''))
