"""Fusion 2012 — candidato 57 (faróis): lataria lisa em volta de cada farol.
Parametrização radial a partir de um ponto dentro do carro (hl58maps). Superfície alvo H na faixa até R da lente
(fora do capô e da grade): continuação lisa da lataria de fora (min |Laplaciano|²) + rampa biharmônica até a borda
da lente. Os vértices da pintura das carrocerias (todos os kits, LODs A–E) que estão perto da superfície são
PROJETADOS em H (mesma topologia: sem costura), com transição suave na borda da faixa e normais do campo liso.
Uma pele de fundo (grupo da pintura em BASE_A–E) 1,5 mm abaixo de H tapa buracos que existiam na faixa."""
import sys;sys.path.insert(0,'/home/claude/c12');sys.path.insert(0,'/home/claude/v3/versions/v3-fusion-ajm3899/scripts')
import numpy as np,geo,pickle
from partmesh import PartMesh
import hl58maps as M,hl57solve as S
from scipy.ndimage import binary_dilation,binary_erosion,distance_transform_edt,gaussian_filter,map_coordinates
from scipy.spatial import Delaunay
from skimage.measure import find_contours
RES=0.003; SKIN=0xB637F71F
A=dict(BKIN=0,LENSIN=0,LIFT=0.0,LRR=0.045,LOFF=0.002,LSIG=0.012,LTIP=0.15,SIG=0.0,EXH=-1,LENSDOM=False,NDOT=-2.0,R=0.06,RR=0.035,CAP=0.05,RW=0.001,EXCL=2,BLEND=4,WIN_IN=0.03,WIN_OUT=0.04,BACK=0.0015,TEST=False)
for a in sys.argv[3:]:
    k,v=a.split('='); A[k]=type(A[k])(eval(v))
SPACING={'A':(5,2),'B':(6,3),'C':(8,5),'D':(12,8),'E':(12,8)}
def fillnear(X):
    m=np.isnan(X) if X.ndim==2 else np.isnan(X[...,0])
    if not m.any(): return X
    ni=distance_transform_edt(m,return_indices=True)[1]; return X[ni[0],ni[1]]
def sample(G,uv,grid,order=1):
    u0,v0,nu,nv=grid; ci=(uv[:,0]-u0)/RES-0.5; cj=(uv[:,1]-v0)/RES-0.5
    return map_coordinates(G,[cj,ci],order=order,mode='nearest')
def lower_lift(d,band,H):
    """raise the bumper (below the lens) up to the lens lower edge: biharmonic ramp within LRR of the lens"""
    from scipy.sparse import coo_matrix,identity
    from scipy.sparse.linalg import spsolve
    lens=d['lens']; nv,nu=lens.shape
    Lh=d['Lh']; ni=distance_transform_edt(np.isnan(Lh),return_indices=True)[1]; Lf=Lh[ni[0],ni[1]]
    rim=band&binary_dilation(lens,iterations=1)
    lo=np.full(nu,-1); ys,xs=np.nonzero(lens)
    for i in range(nu):
        c=np.nonzero(lens[:,i])[0]
        if len(c): lo[i]=c.min()
    J,I=np.nonzero(rim)
    lower=np.zeros_like(rim); m=(lo[I]>=0)&(J<=lo[I]); lower[J[m],I[m]]=True
    # taper towards both lamp ends (fraction LTIP of the lamp length)
    u=(np.arange(nu)-xs.min())/max(xs.max()-xs.min(),1); tp=np.clip(np.minimum(u,1-u)/A['LTIP'],0,1); tp=tp*tp*(3-2*tp)
    delta=np.clip(Lf-A['LOFF']-H,0,A['LIFT'])*tp[None,:]
    delta=np.where(lower,delta,0.0)
    sg=A['LSIG']/RES; wgt=gaussian_filter(lower.astype(float),sg); dsm=gaussian_filter(delta,sg)/np.maximum(wgt,1e-9)
    dr=np.where(rim,np.where(lower,dsm,0.0),0.0)
    dl=distance_transform_edt(~lens)*RES
    ni2=distance_transform_edt(~rim,return_indices=True)[1]
    near=dr[ni2[0],ni2[1]]
    near=gaussian_filter(near,sg*0.6)
    t=np.clip(1-dl/A['LRR'],0,1); t=t*t*(3-2*t)
    lift=near*t
    lift=np.clip(lift,0,None)
    print('  lift max %.1f mm, lower rim cells %d'%(lift.max()*1e3,lower.sum()))
    return np.where(band,lift,0.0)
def plan(d):
    band,dl,excl=S.band_masks(d,R=A['R'],excl_dil=A['EXCL'],excl_hood=None if A['EXH']<0 else A['EXH'])
    H,Hx,lift=S.ramp4(d,band,Rr=A['RR'],cap=A['CAP'],Rw=A['RW'],with_lens=A['LENSDOM'])
    if A['SIG']>0:
        from scipy.ndimage import median_filter
        Bf=np.where(np.isnan(d['Bh'])|band&np.isnan(d['Bh']),H if True else 0,d['Bh'])
        Bf=np.where(np.isnan(Bf),np.nan,Bf)
        valid=~np.isnan(Bf)&~d['lens']
        B0=np.where(valid,Bf,0.0)
        Bm=median_filter(np.where(valid,Bf,np.nanmedian(Bf)),size=5)
        B0=np.where(valid,Bm,0.0)
        sg=A['SIG']/RES
        num=gaussian_filter(B0,sg); den=gaussian_filter(valid.astype(float),sg)
        Hsm=num/np.maximum(den,1e-6)
        H=np.where(band,Hsm,np.nan)
    if A['LIFT']>0: H=H+lower_lift(d,band,H)
    Hb=np.where(band,H,d['Bh'])
    if A['LENSIN']>0:
        edge=d['lens']&binary_dilation(band,iterations=A['LENSIN'])
        Hb=np.where(edge,np.nan,Hb); Hb=np.where(edge,fillnear(np.where(band,H,np.nan)),Hb)
    Hfull=fillnear(Hb)
    Hs=gaussian_filter(Hfull,1.0)
    # blend weight: 0 outside the band, 1 from BLEND cells inside
    w=np.clip(distance_transform_edt(band|d['lens'])/A['BLEND'],0,1)*band; w=w*w*(3-2*w)
    if A['LENSIN']>0: w=np.where(d['lens']&binary_dilation(band,iterations=A['LENSIN']),1.0,w)
    # paint UV fill for the backing patch
    UV=d['UVr'].copy()
    for k in range(2):
        f=np.where(band,np.nan,UV[...,k]); known=~np.isnan(f)
        fill=S.extrap({'Bh':np.where(known,f,np.nan),'lens':np.zeros_like(band)},~known&binary_dilation(band,iterations=3))
        UV[...,k]=np.where(known,f,fill)
    UV=fillnear(UV)
    return dict(d=d,band=band,H=H,Hs=Hs,w=w,UV=UV,excl=excl)
def field_normals(pl,Q):
    grid=pl['d']['grid']; CC=pl['d']['c']; e=RES; hf=lambda q: sample(pl['Hs'],q,grid)
    P=M.inv(np.c_[Q,hf(Q)],CC)
    Ps=M.inv(np.c_[Q+[e,0],hf(Q+[e,0])],CC)-M.inv(np.c_[Q-[e,0],hf(Q-[e,0])],CC)
    Pt=M.inv(np.c_[Q+[0,e],hf(Q+[0,e])],CC)-M.inv(np.c_[Q-[0,e],hf(Q-[0,e])],CC)
    N=np.cross(Ps,Pt); N/=np.linalg.norm(N,axis=1,keepdims=True)
    return np.where(((N*(P-CC)).sum(1)<0)[:,None],-N,N)
def project(pm,PL):
    ids=np.unique(np.concatenate([g['F'].ravel() for g in pm.groups if pm.tex[g['ti']]==SKIN and len(g['F'])]))
    moved=0
    for side,pl in PL.items():
        d=pl['d']; CC=d['c']; grid=d['grid']; u0,v0,nu,nv=grid
        X=pm.P[ids]; U=M.fwd(X,CC)
        ing=(U[:,0]>u0)&(U[:,0]<u0+nu*RES)&(U[:,1]>v0)&(U[:,1]<v0+nv*RES)&(np.sign(X[:,1])==np.sign(CC[1]))&(X[:,0]>1.4)
        j=np.nonzero(ing)[0]
        w=sample(pl['w'],U[j,:2],grid); h=sample(pl['Hs'],U[j,:2],grid)
        near=(U[j,2]>h-A['WIN_IN'])&(U[j,2]<h+A['WIN_OUT'])&(w>1e-3)
        if A['NDOT']>-1:
            Nf0=field_normals(pl,U[j,:2]); No0=pm.N[ids[j]]/np.maximum(np.linalg.norm(pm.N[ids[j]],axis=1,keepdims=True),1e-9)
            near&=(Nf0*No0).sum(1)>A['NDOT']
        j=j[near]; w=w[near]; h=h[near]
        r=U[j,2]+w*(h-U[j,2])
        vid=ids[j]
        pm.P[vid]=M.inv(np.c_[U[j,:2],r],CC)
        Nf=field_normals(pl,U[j,:2]); No=pm.N[vid]/np.maximum(np.linalg.norm(pm.N[vid],axis=1,keepdims=True),1e-9)
        Nn=(1-w)[:,None]*No+w[:,None]*Nf; pm.N[vid]=Nn/np.maximum(np.linalg.norm(Nn,axis=1,keepdims=True),1e-9)
        moved+=len(vid)
    return moved
def backing(pl,k,kc):
    d=pl['d']; dom=(pl['band']&(distance_transform_edt(pl['band']|d['lens'])>A['BLEND']+1)) if A['BKIN'] else binary_erosion(pl['band'],iterations=A['BLEND']+1); grid=d['grid']; u0,v0,nu,nv=grid; CC=d['c']
    pts=[]
    for c in find_contours(np.pad(dom.astype(float),1),0.5):
        c=c-1; dd=np.r_[0,np.cumsum(np.linalg.norm(np.diff(c,axis=0),axis=1))]
        if dd[-1]<4: continue
        s_=np.linspace(0,dd[-1],max(4,int(dd[-1]/kc)+1))[:-1]
        pts.append(np.c_[u0+(np.interp(s_,dd,c[:,1])+0.5)*RES,v0+(np.interp(s_,dd,c[:,0])+0.5)*RES])
    er=binary_erosion(dom,iterations=max(1,kc))
    gy,gx=np.meshgrid(np.arange(0,nv,k),np.arange(0,nu,k),indexing='ij'); m=er[gy,gx]
    pts.append(np.c_[u0+(gx[m]+0.5)*RES,v0+(gy[m]+0.5)*RES])
    Q=np.concatenate(pts); _,uq=np.unique(np.round(Q/(RES*0.4)),axis=0,return_index=True); Q=Q[np.sort(uq)]
    F=Delaunay(Q).simplices; ok=np.ones(len(F),bool)
    for wt in ((1/3,1/3,1/3),(0.5,0.5,0),(0,0.5,0.5),(0.5,0,0.5)):
        c=wt[0]*Q[F[:,0]]+wt[1]*Q[F[:,1]]+wt[2]*Q[F[:,2]]
        iu=np.clip(((c[:,0]-u0)/RES).astype(int),0,nu-1); iv=np.clip(((c[:,1]-v0)/RES).astype(int),0,nv-1); ok&=dom[iv,iu]
    F=F[ok]; used=np.unique(F); rm=-np.ones(len(Q),int); rm[used]=np.arange(len(used)); Q=Q[used]; F=rm[F]
    h=sample(pl['Hs'],Q,grid)-A['BACK']
    P=M.inv(np.c_[Q,h],CC); N=field_normals(pl,Q)
    fn=np.cross(P[F[:,1]]-P[F[:,0]],P[F[:,2]]-P[F[:,0]]); F=np.where(((fn*(P[F].mean(1)-CC)).sum(1)<0)[:,None],F[:,[0,2,1]],F)
    UV=np.c_[sample(pl['UV'][...,0],Q,grid),sample(pl['UV'][...,1],Q,grid)]
    return P,N,UV,F
def main(src,out):
    Z={p['name']:p for p in geo.load(src)}
    PL={s:plan(M.maps(Z,s)) for s in ('LEFT','RIGHT')}
    pickle.dump(PL,open(out+'.plan.pkl','wb'))
    recs=[]; meta=None
    for k in (('KIT00',) if A['TEST'] else ('KIT00','KIT01','KIT02','KIT04','KIT05')):
        for L in ('A' if A['TEST'] else 'ABCDE'):
            name='COBALTSS_%s_BODY_%s'%(k,L); pm=PartMesh(Z[name])
            g=[g for g in pm.groups if pm.tex[g['ti']]==SKIN][0]
            if meta is None: meta=(pm.sh[g['si']],g['flags'],g['unk1'],int(np.median(pm.C[np.unique(g['F'].ravel())])))
            n=project(pm,PL); b,nv=pm.record(); recs.append(b)
            print('%-26s vertices moved %d  verts %d'%(name,n,nv),flush=True)
    shh,flags,unk1,col=meta
    for L in ('A' if A['TEST'] else 'ABCDE'):
        name='COBALTSS_BASE_%s'%L; pm=PartMesh(Z[name])
        ti=pm.tex_index(SKIN); si=pm.sh_index(shh); F=[]
        for s_,pl in PL.items():
            P,N,UV,Fp=backing(pl,*SPACING[L]); o=pm.add_verts(P,N,UV,col); F.append(Fp+o)
        pm.groups.append(dict(ti=ti,si=si,flags=flags,unk1=unk1,F=np.concatenate(F)))
        b,nv=pm.record(); recs.append(b); print('%-26s + pele de fundo, verts %d'%(name,nv))
        if nv>65535: raise SystemExit('vertex limit')
    open(out,'wb').write(b''.join(recs))
if __name__=='__main__': main(sys.argv[1],sys.argv[2])
