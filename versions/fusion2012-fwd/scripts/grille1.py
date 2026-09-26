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
from scipy.ndimage import binary_dilation,gaussian_filter,distance_transform_edt
from skimage.measure import find_contours
from matplotlib.path import Path
SKIN=0xB637F71F; BLACK=0xE67A0B4A
def YE(z): return 0.40+np.clip((np.asarray(z)-0.08)/0.11,0,1)*0.06
ZLO,ZHI,YC=0.0795,0.212,0.95
OFS=0.0015   # patch this far inside the fitted surface
ZHI2=0.30     # around the fog niche (y>0.5) the whole surround is rebuilt, up to above the niche
RES=0.0025
STEP={'A':0.035,'B':0.035,'C':0.05,'D':0.07,'E':0.07}
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
        Q.append((y,0.074))   # lip nose (the shelf at z 0.08 is horizontal: sample just below it)
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
FIT={}
def _resample(C,sp,closed):
    if closed: C=np.r_[C,C[:1]]
    d=np.r_[0,np.cumsum(np.linalg.norm(np.diff(C,axis=0),axis=1))]
    if d[-1]<sp: return C[:1]
    n=max(3,int(round(d[-1]/sp)))
    s=np.linspace(0,d[-1],n+1)[:-1] if closed else np.linspace(0,d[-1],n+1)
    return np.c_[np.interp(s,d,C[:,0]),np.interp(s,d,C[:,1])]
def patch(pm,pods,verbose=False):
    L=pm.name[-1]; st=STEP[L]
    SP,SF=front(pm.P,tris(pm,SKIN))
    sk=lambda Q: xcast(SP,SF,np.asarray(Q,float),'max')
    def pd(Q):
        r=np.stack([xcast(P,F,np.asarray(Q,float),'max') for P,F in pods]); r=np.where(np.isnan(r),-9,r).max(0); return np.where(r<-8,np.nan,r)
    f,fy,fz,med,mx=fitsurf(sk)
    FIT.setdefault(L,f)
    if verbose: print('  fit residual median %.4f max %.4f'%(med,mx))
    fi=np.unique(SF); kd=cKDTree(SP[fi][:,1:])
    y0=0.38; z0=ZLO-4*RES
    ys=np.arange(y0,YC,RES); zs=np.arange(z0,ZHI2+4*RES,RES)
    YY,ZZ=np.meshgrid(ys,zs)
    toyz=lambda c: np.c_[y0+c[:,1]*RES, z0+c[:,0]*RES]
    HSP=0.005 if L=='A' else 0.012 if L in 'BC' else 0.025      # spacing along the niche outline
    OSP=0.010 if L=='A' else 0.02 if L in 'BC' else 0.04        # spacing along the outer outline
    newP=[];newN=[];newF=[]; dropped=0
    for sg in (1,-1):
        Q=np.c_[sg*YY.ravel(),ZZ.ravel()]; xs=sk(Q).reshape(YY.shape); xp=pd(Q).reshape(YY.shape)
        has=~np.isnan(xs); yside=np.array([ys[np.nonzero(r)[0].max()] if r.any() else 0 for r in has])[:,None]
        ztop=np.where(YY>0.5,ZHI2,ZHI)
        region=(YY>=YE(ZZ))&(YY<=yside-0.005)&(ZZ>=ZLO)&(ZZ<=ztop)
        # niche outline: fog-lamp silhouette seen from the front, smoothed, 3 mm outside
        pod=binary_dilation(~np.isnan(xp),iterations=1)
        pods_c=[toyz(c) for c in find_contours(np.pad(gaussian_filter(pod.astype(float),1.2),0),0.5)]
        pods_c=[c for c in pods_c if len(c)>20]
        Hpaths=[Path(np.r_[c,c[:1]]) for c in pods_c]
        # outer outline: region contour, snapped to the exact lines (grille end, bottom, top)
        outs=[]
        for c in find_contours(np.pad(region.astype(float),1),0.5):
            c=toyz(c-1)
            c[:,1]=np.clip(c[:,1],ZLO,None); c[:,1]=np.minimum(c[:,1],np.where(c[:,0]>0.5,ZHI2,ZHI))
            c[:,0]=np.maximum(c[:,0],YE(c[:,1]))
            if len(c)>10: outs.append(c)
        Rpath=Path(np.r_[outs[0],outs[0][:1]]) if len(outs)==1 else None
        def inR(P2):
            if Rpath is not None: return Rpath.contains_points(P2,radius=1e-6)|Rpath.contains_points(P2,radius=-1e-6)
            iy=np.clip(np.round((P2[:,0]-y0)/RES).astype(int),0,len(ys)-1); iz=np.clip(np.round((P2[:,1]-z0)/RES).astype(int),0,len(zs)-1); return region[iz,iy]
        def inH(P2):
            r=np.zeros(len(P2),bool)
            for h in Hpaths: r|=h.contains_points(P2)
            return r
        # points: niche outline (dense), outer outline, interior grid
        Hpts=[_resample(c,HSP,True) for c in pods_c]
        Hpts=[h[inR(h)] for h in Hpts]
        Opts=[_resample(c,OSP,False) for c in outs]
        Opts=[o[~inH(o)] for o in Opts]
        B=np.concatenate(Hpts+Opts)
        gy,gz=np.meshgrid(np.arange(y0,YC,st),np.arange(ZLO,ZHI2+1e-9,st*0.8))
        G=np.c_[gy.ravel(),gz.ravel()]; G=G[inR(G)&~inH(G)]
        if len(B) and len(G):
            dB,_=cKDTree(B).query(G); G=G[dB>0.6*st]
        V=np.r_[B,G]
        _,u=np.unique(np.round(V/0.0015),axis=0,return_index=True); V=V[np.sort(u)]
        T=Delaunay(V).simplices
        c=V[T].mean(1); keep=inR(c)&~inH(c)
        # also drop slivers along the outline (all three points on the same outline)
        T=T[keep]
        used=np.unique(T); remap=-np.ones(len(V),int); remap[used]=np.arange(len(used)); V=V[used]; T=remap[T]
        isH=inH(V) | (cKDTree(np.concatenate(Hpts)).query(V)[0]<1e-6 if sum(len(h) for h in Hpts) else np.zeros(len(V),bool))
        # old skin replaced by the patch (inside the outline, or inside the niche outline in the niche zone)
        g0=[g for g in pm.groups if pm.tex[g['ti']]==SKIN][0]; FF=g0['F']; TP=pm.P[FF]
        cand=np.nonzero((TP[:,:,0].min(1)>1.95)&((np.sign(TP[:,:,1])==sg).all(1)))[0]
        if len(cand):
            Tc=TP[cand]; ok=np.ones(len(cand),bool); okh=np.ones(len(cand),bool)
            for k in range(3):
                q=np.c_[np.abs(Tc[:,k,1]),Tc[:,k,2]]
                a=(q[:,1]>ZLO+0.006)
                ok&=inR(q)&a&(Tc[:,k,0]<f(q[:,0],q[:,1])+0.03)
                okh&=inH(q)&a&(q[:,0]>0.5)
            hid=np.zeros(len(FF),bool); hid[cand[ok|okh]]=True
            g0['F']=FF[~hid]; dropped+=hid.sum()
        o=sum(len(p) for p in newP)
        X3=np.c_[f(V[:,0],V[:,1])-OFS,sg*V[:,0],V[:,1]]
        Nn=np.c_[np.ones(len(V)),-fy(V[:,0],V[:,1])*sg,-fz(V[:,0],V[:,1])]; Nn/=np.linalg.norm(Nn,axis=1,keepdims=True)
        fn=np.cross(X3[T[:,1]]-X3[T[:,0]],X3[T[:,2]]-X3[T[:,0]]); T=np.where((fn[:,0]<0)[:,None],T[:,[0,2,1]],T)
        newP.append(X3); newN.append(Nn); newF.append(T+o)
        # walls: along the niche outline and along the grille end, 3-4 cm back
        E=np.sort(np.r_[T[:,[0,1]],T[:,[1,2]],T[:,[2,0]]],axis=1); ue,cnt=np.unique(E,axis=0,return_counts=True); be=ue[cnt==1]
        onH=cKDTree(np.concatenate(Hpts)).query(V)[0]<1e-6 if sum(len(h) for h in Hpts) else np.zeros(len(V),bool)
        onE=np.abs(V[:,0]-YE(V[:,1]))<0.0015
        for sel,depth in ((onH[be[:,0]]&onH[be[:,1]],0.03),(onE[be[:,0]]&onE[be[:,1]]&(V[be[:,0],1]>ZLO+1e-3)|onE[be[:,0]]&onE[be[:,1]],0.04)):
            bw=be[sel]
            if not len(bw): continue
            vs=np.unique(bw); loc={v:i for i,v in enumerate(vs)}; k=len(vs)
            A=X3[vs]; Bk=A-(depth,0,0); P3=np.r_[A,Bk]; WN=np.zeros((2*k,3)); WT=[]
            cen=V[T].mean(1)
            for a,b in bw:
                ia,ib=loc[a],loc[b]; WT+=[(ia,ib,k+ib),(ia,k+ib,k+ia)]
                t=np.nonzero(((T==a)|(T==b)).sum(1)==2)[0][0]
                d=np.r_[0,sg*((V[a,0]+V[b,0])/2-cen[t,0]),(V[a,1]+V[b,1])/2-cen[t,1]]; d/=np.linalg.norm(d)+1e-12
                for q in (ia,ib,k+ia,k+ib): WN[q]+=d
            WN/=np.maximum(np.linalg.norm(WN,axis=1,keepdims=True),1e-12)
            WT=np.array(WT); fw=np.cross(P3[WT[:,1]]-P3[WT[:,0]],P3[WT[:,2]]-P3[WT[:,0]])
            WT=np.where(((fw*WN[WT[:,0]]).sum(1)<0)[:,None],WT[:,[0,2,1]],WT)
            o=sum(len(p) for p in newP); newP.append(P3); newN.append(WN); newF.append(WT+o)
    P=np.concatenate(newP);N=np.concatenate(newN);F=np.concatenate(newF)
    _,nn=kd.query(P[:,1:]); UV=pm.UV[fi[nn]]; C=pm.C[fi[nn]]
    g=[g for g in pm.groups if pm.tex[g['ti']]==SKIN][0]
    o=pm.add_verts(P,N,UV,C); g['F']=np.r_[g['F'],F+o]
    if verbose: print('  old skin tris replaced',dropped)
    return len(P)
def lipnormals(pm,box=(1.95,-0.06,0.095,0.95),cosmax=0.5):
    """smooth shading of the lower front bumper lip: vertex normals = area-weighted normals of the adjacent
    faces (vertices welded by position) that face the same side (<60 deg from the current normal)"""
    F=tris(pm,SKIN); P=pm.P; N=pm.N
    m=(P[:,0]>box[0])&(P[:,2]>box[1])&(P[:,2]<box[2])&(np.abs(P[:,1])<box[3])
    fm=m[F].any(1); Fs=F[fm]
    key=np.round(P/1e-4).astype(np.int64); _,wid=np.unique(key,axis=0,return_inverse=True); wid=wid.ravel()
    fn=np.cross(P[Fs[:,1]]-P[Fs[:,0]],P[Fs[:,2]]-P[Fs[:,0]])
    fu=fn/np.maximum(np.linalg.norm(fn,axis=1,keepdims=True),1e-15)
    # per welded vertex, the faces around it
    from collections import defaultdict
    adj=defaultdict(list)
    for t,f in enumerate(Fs):
        for v in f: adj[wid[v]].append(t)
    vs=np.nonzero(m)[0]; n=0
    newN=N.copy()
    for v in vs:
        ts=adj.get(wid[v])
        if not ts: continue
        ts=np.array(ts); cur=N[v]/max(np.linalg.norm(N[v]),1e-12)
        ok=(fu[ts]@cur)>cosmax
        if not ok.any(): continue
        s=fn[ts[ok]].sum(0); l=np.linalg.norm(s)
        if l<1e-15: continue
        newN[v]=s/l; n+=1
    pm.N=newN
    return n
def phi(X):
    X=np.asarray(X); y=np.abs(X[:,1]); z=X[:,2]
    return np.maximum.reduce([YE(z)-y+0.004, z-0.225, 0.05-z, 1.95-X[:,0], y-0.97])
def cut_grille(pm):
    n0=pm.ntris()
    for g in pm.groups:
        if pm.tex[g['ti']]!=BLACK or not len(g['F']): continue
        P2,N2,U2,C2,F2=clip_tris(pm.P,pm.N,pm.UV,pm.C,g['F'],phi)
        pm.P=np.r_[pm.P,P2]; pm.N=np.r_[pm.N,N2]; pm.UV=np.r_[pm.UV,U2]; pm.C=np.r_[pm.C,C2]; g['F']=F2
        # black pieces around the fog niche that now stick out of the rebuilt bumper face
        f=FIT.get(pm.name[-1])
        if f is not None:
            C=pm.P[g['F']].mean(1); ay=np.abs(C[:,1])
            rm=(ay>0.5)&(ay<0.95)&(C[:,2]>0.06)&(C[:,2]<0.32)&(C[:,0]>1.95)&(C[:,0]>f(ay,C[:,2])-0.02)
            g['F']=g['F'][~rm]
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
            pm=PartMesh(Z['COBALTSS_%s_BODY_%s'%(k,L)]); n=patch(pm,PD,k=='KIT00'); nl=lipnormals(pm); recs.append(pm); print(pm.name,'patch verts',n,'lip normals',nl)
        gp=PartMesh(Z['COBALTSS_KIT00_RIGHT_SIDE_MIRROR_A' if L=='A' else 'COBALTSS_BASE_'+L])
        print(gp.name,'grille tris net removed',cut_grille(gp)); recs.append(gp)
    with open(out,'wb') as f:
        for pm in recs:
            b,nv=pm.record(); f.write(b); print('%-40s verts %d%s'%(pm.name,nv,' !!VERTS' if nv>65535 else ''))
