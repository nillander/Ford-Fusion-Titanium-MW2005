"""2012 lamp graft: Mondeo (GTA 2016 model) lamps + surrounding skin onto the 2018 z10 body."""
from common import *
from scipy.spatial import cKDTree
from lamps2018 import removal_mask, region_of
LS=pickle.load(open('/home/claude/c12/mondeo_lampsel.pkl','rb')); SEL=LS['sel']; KINV=LS['kinv']
FOG=pickle.load(open('/home/claude/c12/fogsel.pkl','rb'))
MVIS=pickle.load(open('/home/claude/c12/mondeo_vis.pkl','rb'))
ZVIS=pickle.load(open('/home/claude/c12/zvis.pkl','rb'))
M=S['M']; MF=S['F']; MSH=S['shader']; MC=M[MF].mean(1)
B=np.array(S['bones']); MBONE=B[S['bone']]
MN=gta2mw_n(S['N'])
uniq=np.zeros(len(MF),bool); _,first=np.unique(KINV,return_index=True); uniq[first]=True
FEAT={'headL':SEL['headL'],'headR':SEL['headR'],'tailL':SEL['tailL'],'tailR':SEL['tailR'],'fogL':FOG['fogL'],'fogR':FOG['fogR']}
for _k in ('tailL','tailR'): FEAT[_k]=FEAT[_k]&(MC[:,2]<0.82)
for _k in ('headL','headR'): FEAT[_k]=FEAT[_k]&(MC[:,2]<0.72)
for _k in ('tailL','tailR','headL','headR'):
    _lens=FEAT[_k]&np.isin(MSH,(15,16)); _t=cKDTree(M[np.unique(MF[_lens])]); _d,_=_t.query(M)
    FEAT[_k]=FEAT[_k]&~((MSH==4)&(_d[MF].max(1)<0.008))
for _k in ('tailL','tailR'):
    _r=FEAT[_k]&(MSH==16); _t=cKDTree(M[np.unique(MF[_r])]); _d,_=_t.query(M)
    FEAT[_k]=FEAT[_k]&~((MSH==15)&(_d[MF].max(1)<0.003))
allfeat=np.zeros(len(MF),bool)
for v in FEAT.values(): allfeat|=v
EXCL_BONES={'interior','steeringwheel','seat_dside_f','seat_pside_f','seat_dside_r','seat_pside_r','hub_lf','hub_rf','hub_lr','hub_rr'}
_pt=cKDTree(M[np.unique(MF[MSH==0])]); _dv,_=_pt.query(M); GUMDUP=(MSH==4)&(_dv[MF].max(1)<0.004)
POOL=uniq&MVIS&~GUMDUP&~allfeat&~np.isin(MBONE,list(EXCL_BONES))&~np.isin(MSH,[1,2,3,5,6,7,8,12,13,15,17,11])
# graft settings: r1 cut radius, r2 patch radius (tangential), with depth window
CFG={'head':dict(r1=0.0,r2=0.035,cut=False,depth=0.12),
     'tail':dict(r1=0.02,r2=0.05,cut=True,depth=0.15),
     'fog':dict(r1=0.012,r2=0.035,cut=True,depth=0.12)}
def part(name): return [q for q in Z if q['name']=='MUSTANGGT_'+name][0]
def sample_tris(P,F,step=0.004):
    """points on triangles (vertices + centroids + subdivisions for big tris)"""
    tri=P[F]; pts=[tri.reshape(-1,3),tri.mean(1)]
    e=np.max(np.linalg.norm(tri-np.roll(tri,1,1),axis=2),1)
    for k in (2,4,8):
        big=e>step*k
        if not big.any(): break
        t=tri[big]; r=np.random.default_rng(0).dirichlet([1,1,1],size=(len(t),k*k))
        pts.append(np.einsum('nkj,njd->nkd',r,t).reshape(-1,3))
    return np.concatenate(pts)
def tangential_dist(X,N,tree,pts,rmax,depth):
    """for points X with normals N: min tangential distance to pts lying within depth behind/around X"""
    out=np.full(len(X),np.inf)
    for i in range(len(X)):
        l=tree.query_ball_point(X[i],np.hypot(rmax,depth))
        if not l: continue
        d=pts[l]-X[i]; h=d@N[i]
        ok=(h<0.02)&(h>-depth)
        if not ok.any(): continue
        t=np.linalg.norm(d[ok]-np.outer(h[ok],N[i]),axis=1)
        out[i]=t.min()
    return out
def z_extra_mask(name,C):
    """2018 lamp-related triangles outside lamp solids that must go (tail internals, bar, fog bezel)"""
    m=np.zeros(len(C),bool)
    if name.startswith(('BASE_','KIT00_RIGHT_SIDE_MIRROR_')):
        m|=(C[:,0]<-1.9)&(C[:,2]>0.58)&(C[:,2]<0.86)&(np.abs(C[:,1])>0.3)
        if name.startswith('BASE_'):
            m|=(C[:,0]<-2.18)&(np.abs(C[:,1])<=0.62)&(C[:,2]>0.68)&(C[:,2]<0.74)   # chrome bar
            m|=(C[:,0]>1.85)&(C[:,2]<0.22)&(np.abs(C[:,1])>0.44)                   # 2018 fog LED bezel
    return m
def z_removed(name):
    """(soup, removal mask) for a z10 part: lamp volumes + extras"""
    p=part(name); T,m=removal_mask(p)
    C=T['P'][T['F']].mean(1)
    if name.startswith('KIT00_INTERIOR'): m[:]=False
    m|=z_extra_mask(name,C)
    return T,m
def kind(k): return k[:-1]
def side(k): return 1 if k[-1]=='L' else -1
def zfeature_points(k,L='A'):
    s=side(k); kd=kind(k); pts=[]
    for nm in ['KIT00_RIGHT_HEADLIGHT_','KIT00_RIGHT_HEADLIGHT_GLASS_','KIT00_RIGHT_BRAKELIGHT_','KIT00_RIGHT_BRAKELIGHT_GLASS_','BASE_','KIT00_RIGHT_SIDE_MIRROR_']:
        T,m=z_removed(nm+L); C=T['P'][T['F']].mean(1)
        reg=region_of(C)
        if kd=='tail': r=(C[:,0]<-1.7)&(C[:,2]>0.45)
        elif kd=='head': r=(C[:,0]>1.55)&(C[:,2]>0.38)
        else: r=(C[:,0]>1.8)&(C[:,2]<0.3)
        mm=m&r&(C[:,1]*s>=0)
        if kd=='fog': continue   # the 2018 fog pocket stays (closed), not part of the graft
        if mm.any(): pts.append(sample_tris(T['P'],T['F'][mm]))
    return np.concatenate(pts) if pts else np.zeros((0,3))
def closest_on(tree_pts,tree,X):
    d,j=tree.query(X); return tree_pts[j],d,j
def rbf_fit(C,D,sigma=0.05,lam=1e-3):
    mu=D.mean(0); K=np.exp(-((C[:,None]-C[None])**2).sum(-1)/(2*sigma**2))
    W=np.linalg.solve(K+lam*np.eye(len(C)),D-mu)
    return lambda X:(np.exp(-((X[:,None]-C[None])**2).sum(-1)/(2*sigma**2))@W)+mu if len(X) else np.zeros((0,3))
# ---- 2018 skin reference (LOD A visible outer skin)
def _skinref():
    p=part('KIT00_BODY_A'); T=mwsoup.soup([p]); vis=ZVIS['KIT00_BODY_A']
    F=T['F'][vis]; tri=T['P'][F]
    rng=np.random.default_rng(1)
    e=np.max(np.linalg.norm(tri-np.roll(tri,1,1),axis=2),1); k=np.clip((e/0.004).astype(int),1,12)
    Ps=[T['P']];Ns=[T['N']];Us=[T['UV']]
    for kk in np.unique(k):
        sel=k==kk; n=kk*kk
        r=rng.dirichlet([1,1,1],size=(sel.sum(),n))
        Ps.append(np.einsum('nkj,njd->nkd',r,tri[sel]).reshape(-1,3))
        Ns.append(np.einsum('nkj,njd->nkd',r,T['N'][F[sel]]).reshape(-1,3))
        Us.append(np.einsum('nkj,njd->nkd',r,T['UV'][F[sel]]).reshape(-1,2))
    vmask=np.zeros(len(T['P']),bool); vmask[np.unique(F)]=True
    P=np.concatenate(Ps);N=np.concatenate(Ns);U=np.concatenate(Us)
    keep=np.r_[vmask,np.ones(len(P)-len(T['P']),bool)]
    P,N,U=P[keep],N[keep],U[keep]; N/=np.linalg.norm(N,axis=1,keepdims=True)+1e-12
    cv=p['v']['c']
    return dict(P=P,N=N,U=U,tree=cKDTree(P),col=int(np.unique(cv,return_counts=True)[0][np.unique(cv,return_counts=True)[1].argmax()]))
SKIN=None
def skin():
    global SKIN
    if SKIN is None: SKIN=_skinref()
    return SKIN
def compute_graft(k):
    cfg=CFG[kind(k)]; s=side(k); SK=skin()
    FM=FEAT[k]
    fpts=[sample_tris(M,MF[FM])]
    zf=zfeature_points(k); fpts.append(zf)
    FP=np.concatenate(fpts)
    _,u=np.unique(np.floor(FP/0.004).astype(np.int64),axis=0,return_index=True); FP=FP[u]; ftree=cKDTree(FP)
    # candidate pool triangles near the feature
    lo=FP.min(0)-cfg['r2']-0.03; hi=FP.max(0)+cfg['r2']+0.03
    cand=POOL&np.all((MC>lo)&(MC<hi),1)&(MC[:,1]*s>=-1e-4 if kind(k)=='tail' else True)
    if kind(k)=='head': cand&=(MBONE!='bonnet')
    cv=np.unique(MF[cand])
    tv=np.full(len(M),np.inf); tv[cv]=tangential_dist(M[cv],MN[cv],ftree,FP,cfg['r2']+0.01,cfg['depth'])
    tri_t=tv[MF].max(1)
    patch=cand&(tri_t<cfg['r2'])
    paint_patch=patch&(MSH==0)
    # ring for warp: paint vertices with t in band
    ringband=(0.004 if kind(k)=='head' else max(cfg['r1'],cfg['r2']-0.025))
    ringtris=cand&(MSH==0)&(tri_t<cfg['r2']+0.02)
    rv=np.unique(MF[ringtris]); rv=rv[(tv[rv]>=ringband)&(tv[rv]<=cfg['r2']+0.02)]
    q,dq,j=closest_on(SK['P'],SK['tree'],M[rv])
    good=dq<0.05
    rv,q,j=rv[good],q[good],j[good]
    D=q+SK['N'][j]*0.0015-M[rv]
    sub=rv if len(rv)<=400 else rv[np.linspace(0,len(rv)-1,400).astype(int)]
    Dsub=D[np.searchsorted(rv,sub)]
    f=rbf_fit(M[sub],Dsub,sigma=0.05,lam=3e-3)
    used=np.unique(MF[patch|FM])
    newP=M.copy(); newP[used]=M[used]+f(M[used])
    newN=MN.copy()
    # snap outer band of the paint patch exactly onto the 2018 skin (+1.5 mm)
    pv=np.unique(MF[paint_patch])
    band0=cfg['r2']-0.015
    w=np.clip((tv[pv]-band0)/0.015,0,1); w=w*w*(3-2*w)
    q2,d2,j2=closest_on(SK['P'],SK['tree'],newP[pv])
    tgt=q2+SK['N'][j2]*0.0015
    ok=d2<0.03
    newP[pv[ok]]=newP[pv[ok]]*(1-w[ok,None])+tgt[ok]*w[ok,None]
    nb=MN[pv]*(1-w[:,None])+SK['N'][j2]*w[:,None]; newN[pv]=nb/np.linalg.norm(nb,axis=1,keepdims=True)
    # uv of paint from the skin (idw of 4 nearest samples)
    dd,jj=SK['tree'].query(newP[pv],k=4); ww=1/np.maximum(dd,1e-4); ww/=ww.sum(1,keepdims=True)
    newUV=np.zeros((len(M),2)); newUV[pv]=(SK['U'][jj]*ww[:,:,None]).sum(1)
    print(k,'feature',FM.sum(),'patch',patch.sum(),'paint',paint_patch.sum(),'ring',len(rv),'mean |D| %.4f max %.4f'%(np.linalg.norm(D,axis=1).mean(),np.linalg.norm(D,axis=1).max()))
    return dict(k=k,FP=FP,ftree=ftree,feature=FM,patch=patch,paint=paint_patch,P=newP,N=newN,UV=newUV,cfg=cfg)
def cut_mask(G,T,vis=None):
    """skin triangles of a 2018 body soup T to remove under graft G (all 3 verts within r1 tangentially)"""
    cfg=G['cfg']
    if not cfg['cut']: return np.zeros(len(T['F']),bool)
    lo=G['FP'].min(0)-0.08; hi=G['FP'].max(0)+0.08
    near=np.all((T['P']>lo)&(T['P']<hi),1)
    t=np.full(len(T['P']),np.inf); idx=np.nonzero(near)[0]
    N=T['N'][idx]; N=N/(np.linalg.norm(N,axis=1,keepdims=True)+1e-12)
    t[idx]=tangential_dist(T['P'][idx],N,G['ftree'],G['FP'],cfg['r1']+0.005,cfg['depth']+0.03)
    return t[T['F']].max(1)<cfg['r1']
# ================= v2: skin-driven grafts =================
LENS_SH=(14,15,16)
def _skinref2():
    p=part('KIT00_BODY_A'); T=mwsoup.soup([p]); vis=ZVIS['KIT00_BODY_A']
    tid=np.nonzero(vis)[0]; F=T['F'][tid]; tri=T['P'][F]
    rng=np.random.default_rng(1)
    e=np.max(np.linalg.norm(tri-np.roll(tri,1,1),axis=2),1); k=np.clip((e/0.004).astype(int),1,12)
    Ps=[];Ns=[];Us=[];Ts=[]
    for kk in np.unique(k):
        sel=np.nonzero(k==kk)[0]; n=kk*kk+1
        r=rng.dirichlet([1,1,1],size=(len(sel),n)); r[:,0]=1/3
        Ps.append(np.einsum('nkj,njd->nkd',r,tri[sel]).reshape(-1,3))
        Ns.append(np.einsum('nkj,njd->nkd',r,T['N'][F[sel]]).reshape(-1,3))
        Us.append(np.einsum('nkj,njd->nkd',r,T['UV'][F[sel]]).reshape(-1,2))
        Ts.append(np.repeat(tid[sel],n))
    P=np.concatenate(Ps);N=np.concatenate(Ns);U=np.concatenate(Us);TI=np.concatenate(Ts)
    N/=np.linalg.norm(N,axis=1,keepdims=True)+1e-12
    return dict(T=T,P=P,N=N,U=U,TI=TI,tree=cKDTree(P))
SK2=None
def skin2():
    global SK2
    if SK2 is None: SK2=_skinref2()
    return SK2
CFG2={'tail':dict(r1=0.018,depth=0.05,band=0.015,hole=0.008,r2=0.06),
      'fog':dict(r1=0.012,depth=0.08,band=0.015,hole=0.008,r2=0.04)}
def cut_feature_points(k):
    s=side(k); kd=kind(k)
    FM=FEAT[k]
    if kd=='tail': FM=FM&np.isin(MSH,LENS_SH)
    pts=[sample_tris(M,MF[FM])]
    if kd=='tail': pts.append(zfeature_points(k))
    FP=np.concatenate(pts)
    _,u=np.unique(np.floor(FP/0.004).astype(np.int64),axis=0,return_index=True); return FP[u]
def centroid_cut(T,FP,ftree,cfg,lo,hi):
    C=T['P'][T['F']].mean(1); Nt=T['N'][T['F']].sum(1); Nt/=np.linalg.norm(Nt,axis=1,keepdims=True)+1e-12
    ti=np.nonzero(np.all((C>lo)&(C<hi),1))[0]
    t=np.full(len(C),np.inf); t[ti]=tangential_dist(C[ti],Nt[ti],ftree,FP,cfg['r1']+0.005,cfg['depth'])
    return t<cfg['r1']
def compute_graft2(k):
    cfg=CFG2[kind(k)]; s=side(k); SK=skin2(); T=SK['T']
    FP=cut_feature_points(k); ftree=cKDTree(FP)
    # 1. cut on LOD-A skin
    lo=FP.min(0)-0.1; hi=FP.max(0)+0.1
    cutA=centroid_cut(T,FP,ftree,cfg,lo,hi)
    if kind(k)=='tail': cutA&=(T['P'][T['F']].mean(1)[:,1]*s>=0)
    # 2. skin sample labels
    lab=cutA[SK['TI']]
    ctree=cKDTree(SK['P'][lab]) if lab.any() else None
    # 3. candidate Mondeo triangles
    FM=FEAT[k]
    box=np.all((MC>lo)&(MC<hi),1)
    if kind(k)=='tail': box&=MC[:,1]*s>=-1e-4
    cand=POOL&box
    cv=np.unique(MF[cand])
    d,j=SK['tree'].query(M[cv])
    tv=np.full(len(M),np.inf)
    tv[cv]=tangential_dist(M[cv],MN[cv],ftree,FP,cfg['r2']+0.005,cfg['depth'])
    dc,_=ctree.query(SK['P'][j])
    cls=np.zeros(len(M),np.int8)  # 0 out, 1 band, 2 in
    inn=(lab[j])|((d>cfg['hole'])&(tv[cv]<cfg['r2']))
    band=(~inn)&(dc<cfg['band'])&(d<=cfg['hole'])
    cls[cv[inn]]=2; cls[cv[band]]=1
    c3=cls[MF]
    patch=cand&(c3.min(1)>=1)&(c3.max(1)==2)
    patch&=~((MSH!=0)&(c3.min(1)<2))    # trims/seams only fully inside
    pv=np.unique(MF[patch]); bv=pv[cls[pv]==1]
    # 4. warp: rbf from band vertices (plus 'in' vertices that lie close to kept skin? none)
    q,dq,jq=M[bv],None,None
    dd,jj=SK['tree'].query(M[bv]); tgt=SK['P'][jj]+SK['N'][jj]*0.0015
    D=tgt-M[bv]
    sub=np.arange(len(bv)) if len(bv)<=500 else np.linspace(0,len(bv)-1,500).astype(int)
    f=rbf_fit(M[bv[sub]],D[sub],sigma=0.04,lam=3e-3)
    used=np.unique(MF[patch|FM])
    newP=M.copy(); newP[used]=M[used]+f(M[used])
    newP[bv]=tgt
    newN=MN.copy(); newN[bv]=SK['N'][jj]
    # normals near the band blend toward skin normals
    ppaint=np.unique(MF[patch&(MSH==0)])
    dd2,jj2=SK['tree'].query(newP[ppaint]); w=np.clip(1-dd2/0.01,0,1)[:,None]*0.5
    nb=MN[ppaint]*(1-w)+SK['N'][jj2]*w; newN[ppaint]=nb/np.linalg.norm(nb,axis=1,keepdims=True); newN[bv]=SK['N'][jj]
    dd3,jj3=SK['tree'].query(newP[ppaint],k=4); ww=1/np.maximum(dd3,1e-4); ww/=ww.sum(1,keepdims=True)
    newUV=np.zeros((len(M),2)); newUV[ppaint]=(SK['U'][jj3]*ww[:,:,None]).sum(1)
    print(k,'cutA',cutA.sum(),'patch',patch.sum(),'band verts',len(bv),'|D| mean %.4f'%np.linalg.norm(D,axis=1).mean())
    return dict(k=k,FP=FP,ftree=ftree,feature=FM,patch=patch,paint=patch&(MSH==0),P=newP,N=newN,UV=newUV,cfg=dict(cfg,cut=True),cutA=cutA,side=s)
def cut_mask2(G,T):
    """cut on any body soup: LOD-A exact; other parts: tangential criterion with same features"""
    cfg=G['cfg']
    lo=G['FP'].min(0)-0.1; hi=G['FP'].max(0)+0.1
    m=centroid_cut(T,G['FP'],G['ftree'],cfg,lo,hi)
    if G['k'].startswith('tail'): m&=(T['P'][T['F']].mean(1)[:,1]*G['side']>=0)
    return m
def compute_graft3(k):
    cfg=CFG2[kind(k)]; s=side(k); SK=skin2(); T=SK['T']
    FM=FEAT[k]; FMc=FM&np.isin(MSH,LENS_SH) if kind(k)=='tail' else FM
    fv=np.unique(MF[FMc]); fp0=sample_tris(M,MF[FMc]); t0=cKDTree(fp0)
    lo=fp0.min(0)-0.12; hi=fp0.max(0)+0.12
    box=np.all((MC>lo)&(MC<hi),1)
    if kind(k)=='tail': box&=MC[:,1]*s>=-1e-4
    cand=POOL&box
    cv=np.unique(MF[cand|FM])
    # 1-2. warp from a paint ring around the feature
    pv=np.unique(MF[cand&(MSH==0)]); d0,_=t0.query(M[pv])
    ring=pv[(d0>0.004)&(d0<cfg['r2'])]
    dd,jj=SK['tree'].query(M[ring]); ok=dd<0.08; ring,jj=ring[ok],jj[ok]
    D=SK['P'][jj]+SK['N'][jj]*0.0015-M[ring]
    sub=np.arange(len(ring)) if len(ring)<=500 else np.linspace(0,len(ring)-1,500).astype(int)
    f=rbf_fit(M[ring[sub]],D[sub],sigma=0.05,lam=3e-3)
    W=M.copy(); W[cv]=M[cv]+f(M[cv])
    # 3. cut features (warped)
    pts=[sample_tris(W,MF[FMc])]
    if kind(k)=='tail': pts.append(zfeature_points(k))
    FP=np.concatenate(pts); _,u=np.unique(np.floor(FP/0.004).astype(np.int64),axis=0,return_index=True); FP=FP[u]; ftree=cKDTree(FP)
    lo2=FP.min(0)-0.1; hi2=FP.max(0)+0.1
    cutA=centroid_cut(T,FP,ftree,cfg,lo2,hi2)
    if kind(k)=='tail': cutA&=(T['P'][T['F']].mean(1)[:,1]*s>=0)
    lab=cutA[SK['TI']]; ctree=cKDTree(SK['P'][lab])
    # 4. classify warped candidate verts
    cvv=np.unique(MF[cand]); d,j=SK['tree'].query(W[cvv])
    tv=np.full(len(M),np.inf); tv[cvv]=tangential_dist(W[cvv],MN[cvv],ftree,FP,cfg['r2']+0.005,cfg['depth'])
    dc,_=ctree.query(SK['P'][j])
    cls=np.zeros(len(M),np.int8)
    inn=(lab[j]&(d<0.02))|((d>cfg['hole'])&(tv[cvv]<cfg['r2']))
    band=(~inn)&(dc<cfg['band'])&(d<=cfg['hole'])
    cls[cvv[inn]]=2; cls[cvv[band]]=1
    c3=cls[MF]
    patch=cand&(c3.min(1)>=1)&(c3.max(1)==2)
    patch&=~((MSH!=0)&(c3.min(1)<2))
    pv2=np.unique(MF[patch]); bv=pv2[cls[pv2]==1]
    dd,jj=SK['tree'].query(W[bv]); W[bv]=SK['P'][jj]+SK['N'][jj]*0.0015
    newN=MN.copy(); newN[bv]=SK['N'][jj]
    pp=np.unique(MF[patch&(MSH==0)])
    dd3,jj3=SK['tree'].query(W[pp],k=4); ww=1/np.maximum(dd3,1e-4); ww/=ww.sum(1,keepdims=True)
    newUV=np.zeros((len(M),2)); newUV[pp]=(SK['U'][jj3]*ww[:,:,None]).sum(1)
    print(k,'ring',len(ring),'|D| %.4f'%np.linalg.norm(D,axis=1).mean(),'cutA',cutA.sum(),'patch',patch.sum(),'band',len(bv))
    return dict(k=k,FP=FP,ftree=ftree,feature=FM,patch=patch,paint=patch&(MSH==0),P=W,N=newN,UV=newUV,cfg=dict(cfg,cut=True),cutA=cutA,side=s)
# ================= v4: rigid lamp + snapped paint flange =================
from footprint import Footprint
CFG4={'head':dict(flange=0.0,hole=True,holer=0.05),'tail':dict(flange=0.022,hole=True,holer=0.06),'fog':dict(flange=0.035,hole=False,holer=0)}
OFF=0.002
def compute_graft4(k):
    cfg=CFG4[kind(k)]; s=side(k); SK=skin2(); T=SK['T']
    FM=FEAT[k]
    lensm=FM&np.isin(MSH,LENS_SH) if kind(k)!='fog' else FM
    lp=sample_tris(M,MF[lensm]); ltree=cKDTree(lp)
    lo=lp.min(0)-0.15; hi=lp.max(0)+0.15
    box=np.all((MC>lo)&(MC<hi),1)
    if kind(k)=='tail': box&=MC[:,1]*s>=-1e-4
    paint=POOL&box&(MSH==0)
    if kind(k)=='head': paint&=MBONE!='bonnet'
    pv=np.unique(MF[paint]); dl,_=ltree.query(M[pv])
    # rigid translation from the paint ring 0.5-3 cm around the lamp
    ring=pv[(dl>0.005)&(dl<0.03)]
    dd,jj=SK['tree'].query(M[ring]); ok=dd<0.06
    Dr=SK['P'][jj[ok]]-M[ring[ok]]
    t=np.median(Dr,axis=0) if ok.sum()>10 else np.zeros(3)
    if kind(k)=='fog':
        yz=cKDTree(SK['P'][:,1:]); rr=pv[(dl>0.006)&(dl<0.025)]
        dd2,j2=yz.query(M[rr][:,1:],k=8)
        cx=np.where(dd2<0.006,SK['P'][j2][:,:,0],-np.inf).max(1)   # front-most skin along x
        ok2=np.isfinite(cx)
        t=np.array([np.median(cx[ok2]-M[rr[ok2],0]),0,0])
    W=M.copy(); W[np.unique(MF[FM|paint])]+=t
    # 2018 holes: removed 2018 features for this lamp
    zf=zfeature_points(k) if cfg['hole'] else np.zeros((0,3))
    ztree=cKDTree(zf) if len(zf) else None
    dsk,jsk=SK['tree'].query(W[pv]); dl,_=ltree.query(W[pv]-0)  # lamp moved with t too
    dl,_=cKDTree(lp+t).query(W[pv])
    dz=ztree.query(W[pv])[0] if ztree is not None else np.full(len(pv),np.inf)
    inflange=dl<cfg['flange']
    inhole=(dsk>0.009)&(dz<cfg['holer'])&(W[pv][:,2]<0.86)
    # hole flange: paint near hole verts but on skin
    holev=pv[inhole]
    nearhole=cKDTree(W[holev]).query(W[pv])[0]<0.02 if len(holev) else np.zeros(len(pv),bool)
    vsel=np.zeros(len(M),bool); vsel[pv[inflange|inhole|nearhole]]=True
    patch=paint&vsel[MF].all(1)
    if kind(k)=='tail': patch&=(W[MF][:,:,0].max(1)<-1.78)
    # vertex placement: snap to skin (+OFF) where skin close, keep near lamp edge
    pp=np.unique(MF[patch]); ii=np.searchsorted(pv,pp)
    d_s=dsk[ii]; d_l=dl[ii]; j_s=jsk[ii]
    w_skin=np.clip((0.013-d_s)/0.004,0,1)          # skin within ~1 cm -> snap
    w_lamp=np.clip((d_l-0.004)/0.008,0,1)           # but keep the lamp edge attached
    w=(w_skin*w_lamp)[:,None]; w=w*w*(3-2*w)
    tgt=SK['P'][j_s]+SK['N'][j_s]*OFF
    W[pp]=W[pp]*(1-w)+tgt*w
    newN=MN.copy(); nb=MN[pp]*(1-w)+SK['N'][j_s]*w; newN[pp]=nb/np.linalg.norm(nb,axis=1,keepdims=True)
    dd3,jj3=SK['tree'].query(W[pp],k=4); ww=1/np.maximum(dd3,1e-4); ww/=ww.sum(1,keepdims=True)
    newUV=np.zeros((len(M),2)); newUV[pp]=(SK['U'][jj3]*ww[:,:,None]).sum(1)
    # cut footprint: lamp lens (moved) plus the flange's inner part
    cutsrc=lensm.copy()
    fp=Footprint(W,MF[cutsrc],d=(np.array([1.0,0.25*s,0.0]) if kind(k)=='fog' else None),dilate=0.0)
    print(k,'t',np.round(t,4),'patch',patch.sum(),'hole verts',len(holev),'dir',np.round(fp.d,2))
    return dict(k=k,feature=FM,patch=patch,paint=patch,P=W,N=newN,UV=newUV,fp=fp,side=s,cfg=cfg,shrink=0.006)
def cut_mask4(G,T):
    """2018 skin triangles covering the new lamp: centroid inside the lens footprint, near the lens depth"""
    C=T['P'][T['F']].mean(1)
    inside,dz=G['fp'].query(C)
    # erode: require the 3 vertices to be inside too
    iv,dv=G['fp'].query(T['P'])
    allin=inside&(iv[T['F']].sum(1)>=2)
    if G['k'].startswith('fog'): allin=inside|(iv[T['F']].sum(1)>=2)
    m=allin&(dz>-0.06)&(dz<(0.14 if G['k'].startswith('fog') else 0.08))
    if G['k'].startswith('tail'): m&=C[:,1]*G['side']>=0
    return m
