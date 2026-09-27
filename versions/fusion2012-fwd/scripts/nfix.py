"""Item 41 (Fusion 2012/2018): normais da lataria discordando da forma (marcas escuras).
Para as faces da pele visíveis de fora (id-buffer de 120 direções) na frente (x>1,3) e na traseira (x<-1,5), cada canto
cuja normal gravada difere da normal geométrica (média das faces vizinhas com menos de ANG° de diferença, pesada pela
área) por mais que DOT recebe a normal geométrica (cópia do vértice só para esse canto, se preciso).
Uso: nfix.py in.dump out.spec PRE TAG"""
import sys;sys.path.insert(0,'/home/claude/c12');sys.path.insert(0,'/home/claude/v3/versions/v3-fusion-ajm3899/scripts')
import numpy as np,geo,pickle,os
from partmesh import PartMesh
from nrm import geo_normals,SKINS
DOT=float(os.environ.get('DOT','0.7')); ANG=float(os.environ.get('ANG','45'))
def fix(pm,faces_idx,Fsel):
    F=pm.groups[0]['F']
    G,fu,ar=geo_normals(pm,F[faces_idx],ANG)
    N=pm.N[F[faces_idx]]; ln=np.linalg.norm(N,axis=2,keepdims=True); Nu=N/np.maximum(ln,1e-9)
    dot=(Nu*G).sum(2); bad=(dot<DOT)&Fsel[:,None]&(ar[:,None]>2e-7)
    t,c=np.nonzero(bad)
    if not len(t): return 0
    vi=F[faces_idx[t],c]; g=G[t,c]
    allF=np.concatenate([gg['F'].ravel() for gg in pm.groups]); uses=np.bincount(allF,minlength=len(pm.P))
    badc=np.bincount(vi,minlength=len(pm.P))
    # in place when every use of the vertex is a bad corner and their targets agree
    acc=np.zeros((len(pm.P),3)); np.add.at(acc,vi,g); an=acc/np.maximum(np.linalg.norm(acc,axis=1,keepdims=True),1e-12)
    agree=np.ones(len(pm.P),bool); np.logical_and.at(agree,vi,(g*an[vi]).sum(1)>0.95)
    inplace=(uses[vi]==badc[vi])&agree[vi]
    v1=np.unique(vi[inplace]); pm.N[v1]=an[v1]*np.linalg.norm(pm.N[v1],axis=1,keepdims=True)
    t2,c2,vi2,g2=t[~inplace],c[~inplace],vi[~inplace],g[~inplace]
    if len(vi2):
        o=pm.add_verts(pm.P[vi2],g2*np.linalg.norm(pm.N[vi2],axis=1,keepdims=True),pm.UV[vi2],pm.C[vi2])
        F[faces_idx[t2],c2]=o+np.arange(len(t2))
    print('   in place',inplace.sum(),'new verts',len(vi2))
    return len(t)
if __name__=='__main__':
    src,out,pre,tag=sys.argv[1:5]
    P=geo.load(src); vis=pickle.load(open('build/vis%s.pkl'%tag,'rb'))
    Z={p['name']:(i,p) for i,p in enumerate(P)}
    pi,p=Z[pre+'_KIT00_BODY_A']; pmA=PartMesh(p)
    m=(vis['part']==pi)&(vis['grp']==0); sv=np.where(vis['seen'][m])[0]
    FA=pmA.groups[0]['F']; C=pmA.P[FA[sv]].mean(1); reg=(C[:,0]>float(os.environ.get('XF','1.3')))|(C[:,0]<float(os.environ.get('XR','-1.5')))
    # visible faces of A, identified by the sorted vertex positions -> apply same to all kits' BODY_A (identical copies there)
    recs=[]
    for k in ('KIT00','KIT01','KIT02','KIT04','KIT05'):
        n='%s_%s_BODY_A'%(pre,k)
        if n not in Z: continue
        pm=PartMesh(Z[n][1]); F=pm.groups[0]['F']
        assert F.shape==FA.shape and np.allclose(pm.P[F],pmA.P[FA]), n
        idx=sv; sel=reg
        c=fix(pm,idx,sel)
        if os.environ.get('PRUNE'): pm.groups[0]['F']=np.delete(pm.groups[0]['F'],np.load(os.environ['PRUNE']),axis=0)
        print(n,'faces matched',len(idx),'corners fixed',c,flush=True); recs.append(pm)
    with open(out,'wb') as f:
        for pm in recs: b,nv=pm.record(); f.write(b)
