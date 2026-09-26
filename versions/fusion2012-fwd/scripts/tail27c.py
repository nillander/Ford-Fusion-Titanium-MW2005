"""Item 27 (v3): acabamento das lanternas depois do teste da v2.
- Miolo da parte da tampa: as peças da antiga luz de ré do Mondeo (caixa de ~7 cm e painéis verticais junto da
  divisão) saem; no lugar, um fundo branco com o formato exato da lente transparente, 12 mm para dentro dela.
- Manchas pretas no anel: tudo o que ainda usava a célula preta (0,5625; 0,5625) no interior das lanternas (contorno
  da parte da tampa, trechos da borda da parte externa, pedacinhos na divisão) passa para o vermelho do anel."""
import sys;sys.path.insert(0,'/home/claude/v3/versions/v3-fusion-ajm3899/scripts');sys.path.insert(0,'/home/claude/c12')
import numpy as np,geo
from partmesh import PartMesh
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
RED=np.array((0.25,0.75)); WHITE=np.array((0.5625,0.6875)); BLACK=np.array((0.5625,0.5625)); CLEAR=np.array((0.81,0.56))
def comps(P,F):
    key=np.round(P/1e-4).astype(np.int64);_,w=np.unique(key,axis=0,return_inverse=True);w=w.ravel()
    W=w[F];n=w.max()+1;r=np.r_[W[:,0],W[:,1],W[:,2]];c=np.r_[W[:,1],W[:,2],W[:,0]]
    _,lab=connected_components(coo_matrix((np.ones(len(r)),(r,c)),shape=(n,n)),directed=False);return lab[W[:,0]]
def edit(pm,gl):
    st=dict(box=0,backing=0,red=0)
    g=pm.groups[0]; F=g['F']; P=pm.P; fl=comps(P,F); keep=np.ones(len(F),bool)
    for L in np.unique(fl):
        k=fl==L; T=P[F[k]]; ay=np.abs(T[:,:,1])
        if ay.min()>=0.44 and ay.max()<0.586 and T[:,:,2].min()>=0.672 and T[:,:,2].max()<=0.75 and T[:,:,0].max()<-1.9:
            keep[k]=False
    st['box']=int((~keep).sum()); g['F']=F[keep]
    # white backing = clear lens of the lid part, 12 mm inside
    Fg=np.concatenate([gg['F'] for gg in gl.groups if len(gg['F'])])
    uvg=gl.UV[Fg].mean(1); Cg=gl.P[Fg].mean(1)
    m=(np.abs(uvg-CLEAR).max(1)<0.02)&(np.abs(gl.P[Fg][:,:,1]).max(1)<0.576)&(Cg[:,2]>0.6)   # lid side only
    if m.any():
        Fb=Fg[m]; vs,inv=np.unique(Fb.ravel(),return_inverse=True)
        Pb=gl.P[vs]+np.array([0.012,0,0]); Nb=gl.N[vs]
        o=pm.add_verts(Pb,Nb,np.tile(WHITE,(len(vs),1)),0xFFFFFFFF)
        g['F']=np.r_[g['F'],inv.reshape(-1,3)+o]; st['backing']=int(m.sum())
    # black -> red inside the lamp
    used=np.unique(np.concatenate([gg['F'] for gg in pm.groups if len(gg['F'])]))
    sel=used[(P[used,0]<-1.75)&(P[used,2]>0.55)&(np.abs(P[used,1])>0.3)&(np.abs(P[used,1])<0.82)] if len(pm.P)==len(P) else used
    Pn=pm.P; sel=used[(Pn[used,0]<-1.75)&(Pn[used,2]>0.55)&(np.abs(Pn[used,1])>0.3)&(np.abs(Pn[used,1])<0.82)]
    b=np.abs(pm.UV[sel]-BLACK).max(1)<0.004; pm.UV[sel[b]]=RED; st['red']=int(b.sum())
    return st
if __name__=='__main__':
    Z={p['name']:p for p in geo.load(sys.argv[1])}; recs=[]
    for L in 'ABCD':
        for s in ('LEFT','RIGHT'):
            pm=PartMesh(Z['COBALTSS_KIT00_%s_BRAKELIGHT_%s'%(s,L)]); gl=PartMesh(Z['COBALTSS_KIT00_%s_BRAKELIGHT_GLASS_%s'%(s,L)])
            st=edit(pm,gl); recs.append(pm); print(pm.name,st)
    with open(sys.argv[2],'wb') as f:
        for pm in recs: b,nv=pm.record(); f.write(b)
