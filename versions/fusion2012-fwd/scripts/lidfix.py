"""Item 7: remove the 2018 chrome-bar lip on the trunk lid (between the tail lights).
The 2018 upper lid ends in a lip sloping out/down to z~0.73 (the bar sat under it). The 2012 lid goes
straight down from the crease (z~0.776) to the plate recess. Vertices of the lip (outside the crease plane)
are pulled onto that plane, keeping the skin thickness; lateral blend near the tail lights."""
import numpy as np
from xray import xcast
SKIN=0x9A8AAD9E
Z0,Z1=0.7255,0.7775     # lip band
ZC=0.779                # just above the crease: reference x of the upper lid
SLOPE=0.07              # 2012 face leans inward going down (Mondeo)
Y0,Y1=0.34,0.385        # full effect |y|<Y0, fades to 0 at Y1
def skin_tris(pm):
    F=[g['F'] for g in pm.groups if pm.tex[g['ti']]==SKIN and len(g['F'])]
    return np.concatenate(F) if F else np.zeros((0,3),int)
def facing(P,F,vs,pn):
    """+1 if the triangles around each vertex face along pn (outer skin), -1 if against (inner layer)"""
    m=np.zeros(len(P),bool); m[vs]=True
    adj=F[m[F].any(1)]
    fn=np.cross(P[adj[:,1]]-P[adj[:,0]],P[adj[:,2]]-P[adj[:,0]])
    fn/=np.maximum(np.linalg.norm(fn,axis=1,keepdims=True),1e-15)
    d=(fn@pn)
    acc=np.zeros(len(P))
    for k in range(3): np.add.at(acc,adj[:,k],d)
    s=np.sign(acc[vs]); s[s==0]=1
    return s
def lidfix(pm,verbose=False):
    F=skin_tris(pm)
    if not len(F): return 0
    P=pm.P; C=P[F].mean(1)
    rr=(C[:,0]<-2.1)&(C[:,2]>0.68)&(C[:,2]<0.83)&(np.abs(C[:,1])<0.45)
    Fr=F[rr]
    if not len(Fr): return 0
    vids=np.unique(Fr.ravel())
    V=P[vids]
    cand=(V[:,2]>Z0)&(V[:,2]<Z1)&(np.abs(V[:,1])<Y1)&(V[:,0]<-2.2)
    if not cand.any(): return 0
    vc=vids[cand]; Vc=P[vc]
    xc=xcast(P,Fr,np.c_[Vc[:,1],np.full(len(Vc),ZC)])
    xo=xcast(P,Fr,Vc[:,1:])
    ok=np.isfinite(xc)&np.isfinite(xo)
    tgt=xc+(ZC-Vc[:,2])*SLOPE
    out=Vc[:,0]<tgt-0.0015                 # outside the 2012 plane -> part of the lip
    sel=ok&out
    w=np.clip((Y1-np.abs(Vc[:,1]))/(Y1-Y0),0,1)
    newx=tgt+np.maximum(Vc[:,0]-xo,0)       # keep offset to the outer skin (inner layer stays inside)
    newx=np.maximum(newx,Vc[:,0])           # only ever move inward
    x2=Vc[:,0]+w*(newx-Vc[:,0])
    moved=vc[sel]; P[moved,0]=x2[sel]
    # normals of moved vertices from adjacent skin triangles
    mset=np.zeros(len(P),bool); mset[moved]=True
    adj=F[mset[F].any(1)]
    fn=np.cross(P[adj[:,1]]-P[adj[:,0]],P[adj[:,2]]-P[adj[:,0]])
    acc=np.zeros_like(P); 
    for k in range(3): np.add.at(acc,adj[:,k],fn)
    # the 2012 face is one plane: outer layer normal = plane normal, inner layer = opposite
    pn=np.array([-1.0,0.0,SLOPE]); pn/=np.linalg.norm(pn)
    sgn=facing(P,F,moved,pn)
    wm=w[sel][:,None]
    nn=pm.N[moved]*(1-wm)+wm*(sgn[:,None]*pn)
    pm.N[moved]=nn/np.maximum(np.linalg.norm(nn,axis=1,keepdims=True),1e-12)
    # smooth, uniform shading: every outward skin vertex lying on the new plane gets the plane normal
    V2=P[vids]; b2=(V2[:,2]>0.712)&(V2[:,2]<0.7765)&(np.abs(V2[:,1])<Y1)&(V2[:,0]<-2.2)
    vb=vids[b2]; Vb=P[vb]
    xcb=xcast(P,Fr,np.c_[Vb[:,1],np.full(len(Vb),ZC)])
    on=np.isfinite(xcb)&(np.abs(Vb[:,0]-(xcb+(ZC-Vb[:,2])*SLOPE))<0.003)&(facing(P,F,vb,pn)>0)
    wb=np.clip((Y1-np.abs(Vb[:,1]))/(Y1-Y0),0,1)[on][:,None]
    nb=pm.N[vb[on]]*(1-wb)+wb*pn
    pm.N[vb[on]]=nb/np.maximum(np.linalg.norm(nb,axis=1,keepdims=True),1e-12)
    if verbose: print(pm.name,'plane normals',int(on.sum()))
    # lower-lid top rows (just under the old shelf): normals from their own non-horizontal faces (no shelf bleed)
    b3=(V2[:,2]>0.705)&(V2[:,2]<0.7285)&(np.abs(V2[:,1])<Y1)&(V2[:,0]<-2.2)
    v3=vids[b3]; V3=P[v3]
    xc3=xcast(P,Fr,np.c_[V3[:,1],np.full(len(V3),ZC)])
    near=np.isfinite(xc3)&(V3[:,0]<xc3+(ZC-V3[:,2])*SLOPE+0.012)
    v3=v3[near]
    if len(v3):
        m=np.zeros(len(P),bool); m[v3]=True
        adj=F[m[F].any(1)]
        fn=np.cross(P[adj[:,1]]-P[adj[:,0]],P[adj[:,2]]-P[adj[:,0]])
        un=fn/np.maximum(np.linalg.norm(fn,axis=1,keepdims=True),1e-15)
        keepf=np.abs(un[:,2])<0.8
        adj,fn=adj[keepf],fn[keepf]
        fn=fn*np.sign(fn@pn)[:,None]          # orient outward
        acc=np.zeros_like(P)
        for k in range(3): np.add.at(acc,adj[:,k],fn)
        a=acc[v3]; l=np.linalg.norm(a,axis=1)
        ok=(l>1e-12)&(facing(P,F,v3,pn)>0)
        pm.N[v3[ok]]=a[ok]/l[ok,None]
        if verbose: print(pm.name,'lower-lid top normals',int(ok.sum()))
    if verbose: print(pm.name,'lip verts moved',len(moved),'max dx %.3f'%(np.abs(x2[sel]-Vc[sel,0]).max() if sel.any() else 0))
    return len(moved)
STRIPS=((0.738,0.782,0.003),(0.7262,0.7320,0.004))   # (z0,z1,offset behind the plane)
YS=0.345
def backing(pm,g):
    """paint strips just behind the new lid plane: covers the crease crack (z~0.77) and the shelf seam (z~0.728)"""
    F=g['F']; P=pm.P; C=P[F].mean(1)
    rr=(C[:,0]<-2.1)&(C[:,2]>0.68)&(C[:,2]<0.83)&(np.abs(C[:,1])<0.45)
    Fr=F[rr]
    ys=np.linspace(-YS,YS,int(round(2*YS/0.01))+1)
    xc=xcast(P,Fr,np.c_[ys,np.full(len(ys),ZC)])
    if not np.isfinite(xc).all():
        ok=np.isfinite(xc); xc=np.interp(ys,ys[ok],xc[ok])
    pn=np.array([-1.0,0.0,SLOPE]); pn/=np.linalg.norm(pn)
    vids=np.unique(Fr.ravel()); tree=None
    from scipy.spatial import cKDTree
    tree=cKDTree(P[vids])
    Ps=[];Is=[];o=0
    for z0,z1,off in STRIPS:
        zz=np.linspace(z0,z1,max(3,int(round((z1-z0)/0.011))+1))
        Y,ZZ=np.meshgrid(ys,zz)
        X=(np.interp(Y,ys,xc)+(ZC-ZZ)*SLOPE)+off
        Q=np.c_[X.ravel(),Y.ravel(),ZZ.ravel()]
        ny=len(ys); I=[]
        for i in range(len(zz)-1):
            for j in range(ny-1):
                a=i*ny+j; b=a+1; c=a+ny; d=c+1
                I+=[(a,c,b),(b,c,d)]
        I=np.array(I)
        # outward facing (towards -x): fix winding so geometric normal ~ pn
        t=Q[I]; n=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0])
        if (n@pn).mean()<0: I=I[:,[0,2,1]]
        Ps.append(Q); Is.append(I+o); o+=len(Q)
    Q=np.concatenate(Ps); I=np.concatenate(Is)
    _,nn=tree.query(Q); src=vids[nn]
    base=pm.add_verts(Q,np.tile(pn,(len(Q),1)),pm.UV[src],pm.C[src])
    g['F']=np.r_[g['F'],I+base]
    return len(I)
def apply(pm,verbose=False):
    n=lidfix(pm,verbose)
    if not n: return 0
    for g in pm.groups:
        if pm.tex[g['ti']]==SKIN and len(g['F']):
            k=backing(pm,g)
            if verbose: print('   backing tris',k)
            break
    return n
