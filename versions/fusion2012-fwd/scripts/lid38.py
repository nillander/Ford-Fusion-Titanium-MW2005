"""Item 38 (Fusion 2012): tampa do porta-malas entre as lanternas.
1) Lanternas maiores (item 28) passaram a atravessar as paredes do rebaixo da lataria perto das pontas internas:
   triângulos da lataria que ficam na frente da lente (vista de trás) a menos de PK de distância são removidos
   (a lente já cobre essa área).
2) Faixa da tampa entre as lanternas (pele de fora, virada para trás): suavização só em x (Taubin), com vinco,
   bordas da região e vértices perto das lanternas fixos; normais recalculadas pela média das faces.
Uso: lid38.py in.dump out.spec PRE"""
import sys;sys.path.insert(0,'/home/claude/c12');sys.path.insert(0,'/home/claude/v3/versions/v3-fusion-ajm3899/scripts')
import numpy as np,geo,os
from partmesh import PartMesh
from xray import xcast
from scipy.spatial import cKDTree
SKIN=0xB637F71F
PK=float(os.environ.get('PK','0.02')); IT=int(os.environ.get('IT','30')); SM=os.environ.get('SM','1')=='1'
X0,YM,Z0,Z1=-2.0,0.42,0.70,0.86

def lens(Z,pre):
    Ps=[];Fs=[];o=0
    for s in ('LEFT','RIGHT'):
        q=PartMesh(Z[pre+'_KIT00_%s_BRAKELIGHT_GLASS_A'%s]); F=np.concatenate([g['F'] for g in q.groups])
        Ps.append(q.P);Fs.append(F+o);o+=len(q.P)
    return np.concatenate(Ps),np.concatenate(Fs)

def cut(pm,LP,LF):
    n=0
    for g in pm.groups:
        F=g['F']
        if not len(F): continue
        C=pm.P[F].mean(1); m=(C[:,0]<X0)&(C[:,2]>0.6)&(C[:,2]<0.9)&(np.abs(C[:,1])>0.2)&(np.abs(C[:,1])<0.9)
        if not m.any(): continue
        idx=np.where(m)[0]
        # test centroid and the three vertices: all must lie over the lens and be behind/near it
        ok=np.ones(len(idx),bool)
        for pts in [C[idx]]+[pm.P[F[idx,k]] for k in range(3)]:
            lx=xcast(LP,LF,pts[:,1:],'min'); ok&=~np.isnan(lx)&(pts[:,0]>np.nan_to_num(lx,nan=9)-PK)&(pts[:,0]<np.nan_to_num(lx,nan=-9)+0.03)
        # only faces that actually stick out in front of the lens (x smaller = further back)
        lxc=xcast(LP,LF,C[idx][:,1:],'min'); ok&=C[idx,0]<lxc+0.002
        rm=np.zeros(len(F),bool); rm[idx[ok]]=True; g['F']=F[~rm]; n+=rm.sum()
    return n

def smooth(pm,LP):
    P=pm.P; allF=[];own=[]
    for gi,g in enumerate(pm.groups):
        if pm.tex[g['ti']]==SKIN and len(g['F']): allF.append(g['F'])
    F=np.concatenate(allF); T=P[F]; C=T.mean(1)
    fn=np.cross(T[:,1]-T[:,0],T[:,2]-T[:,0]); ar=np.linalg.norm(fn,axis=1); fnu=fn/np.maximum(ar,1e-12)[:,None]
    sel=(C[:,0]<X0)&(np.abs(C[:,1])<YM)&(C[:,2]>Z0)&(C[:,2]<Z1)&(fnu[:,0]<-0.4)
    # weld by position
    key=np.round(P*2e4).astype(np.int64); _,wid,=np.unique(key,axis=0,return_inverse=True)[:2]; wid=wid.ravel()
    W=wid[F]; nw=wid.max()+1
    insel=np.zeros(nw,bool); insel[W[sel].ravel()]=True
    outsel=np.zeros(nw,bool); outsel[W[~sel].ravel()]=True
    fixed=outsel.copy()
    # sharp edges inside selection
    Fs=W[sel]; ns=fnu[sel]; E={}
    for t,(a,b,c) in enumerate(Fs):
        for u,v in ((a,b),(b,c),(c,a)):
            E.setdefault((min(u,v),max(u,v)),[]).append(t)
    for (u,v),ts in E.items():
        if len(ts)==1: fixed[u]=fixed[v]=True
        elif len(ts)==2 and ns[ts[0]]@ns[ts[1]]<np.cos(np.radians(25)): fixed[u]=fixed[v]=True
    # position per welded vertex
    wp=np.zeros((nw,3)); wp[wid]=P
    d,_=cKDTree(LP[:,1:]).query(wp[:,1:]); fixed|=d<0.02
    free=insel&~fixed
    nb=[set() for _ in range(nw)]
    for u,v in E: nb[u].add(v); nb[v].add(u)
    fr=np.where(free)[0]; nbl=[np.array(sorted(nb[i])) for i in fr]
    x=wp[:,0].copy()
    for it in range(IT):
        for lam in (0.5,-0.53):
            avg=np.array([x[l].mean() for l in nbl]); x[fr]=x[fr]+lam*(avg-x[fr])
    dx=x-wp[:,0]; print('  free',len(fr),'max dx %.4f'%np.abs(dx[fr]).max())
    P[:,0]+=dx[wid]
    # normals: area-weighted from selected faces, for free welded verts
    T=P[F[sel]]; fn=np.cross(T[:,1]-T[:,0],T[:,2]-T[:,0])
    acc=np.zeros((nw,3))
    for k in range(3): np.add.at(acc,W[sel][:,k],fn)
    nn=acc/np.maximum(np.linalg.norm(acc,axis=1),1e-12)[:,None]
    vv=np.where(free[wid])[0]
    No=pm.N[vv]; ok=(No*nn[wid[vv]]).sum(1)>0   # keep outward-facing sense
    pm.N[vv[ok]]=nn[wid[vv[ok]]]*np.linalg.norm(No[ok],axis=1)[:,None]
    return len(fr)

if __name__=='__main__':
    src,out,pre=sys.argv[1:4]; Z={p['name']:p for p in geo.load(src)}; LP,LF=lens(Z,pre); recs=[]
    for k in ('KIT00','KIT01','KIT02','KIT04','KIT05'):
        for L in 'ABCDE':
            nme='%s_%s_BODY_%s'%(pre,k,L)
            if nme not in Z: continue
            pm=PartMesh(Z[nme]); c=cut(pm,LP,LF)
            s=smooth(pm,LP) if SM and L in 'AB' else 0
            print(nme,'cut',c,'smoothed',s); recs.append(pm)
    with open(out,'wb') as f:
        for pm in recs: b,nv=pm.record(); f.write(b)
