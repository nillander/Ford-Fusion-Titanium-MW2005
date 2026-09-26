"""Item 27 (v4): lanternas uniformes, tampa e lateral idênticas (lente vermelha por fora, lente branca por dentro).
Base: v2 (`tail27b.py`). Em KIT00_LEFT/RIGHT_BRAKELIGHT_A–D:
- tira a caixa da antiga luz de ré do Mondeo no miolo da tampa (|y| 0,44–0,586, z 0,672–0,75);
- célula preta (0,5625; 0,5625) restante no interior → vermelho (0,25; 0,75);
- fundo atrás de cada lente, nas duas partes: cópia dos triângulos da peça _GLASS 6 mm para dentro (ao longo da
  normal da lente), vermelho sólido atrás da lente vermelha e branco sólido atrás da lente transparente. O interior
  antigo não cobria toda a lente: pelas frestas aparecia o preto da carroceria (manchas pretas/vermelho escuro), e o
  miolo da parte externa ficava vazado."""
import sys;sys.path.insert(0,'/home/claude/v3/versions/v3-fusion-ajm3899/scripts');sys.path.insert(0,'/home/claude/c12')
import numpy as np,geo
from partmesh import PartMesh
from tail27c import comps
RED=np.array((0.25,0.75)); WHITE=np.array((0.5625,0.6875)); BLACK=np.array((0.5625,0.5625))
CLEAR=np.array((0.81,0.56)); DEPTH=0.006
def edit(pm,gl):
    st=dict(box=0,red_bk=0,white_bk=0,black2red=0)
    g=pm.groups[0]; F=g['F']; P=pm.P; fl=comps(P,F); keep=np.ones(len(F),bool)
    for L in np.unique(fl):
        k=fl==L; T=P[F[k]]; ay=np.abs(T[:,:,1])
        if ay.min()>=0.44 and ay.max()<0.586 and T[:,:,2].min()>=0.672 and T[:,:,2].max()<=0.75 and T[:,:,0].max()<-1.9: keep[k]=False
    st['box']=int((~keep).sum()); g['F']=F[keep]
    used=np.unique(g['F'].ravel()); Pn=pm.P
    sel=used[(Pn[used,0]<-1.75)&(Pn[used,2]>0.55)&(np.abs(Pn[used,1])>0.3)&(np.abs(Pn[used,1])<0.82)]
    b=np.abs(pm.UV[sel]-BLACK).max(1)<0.004; pm.UV[sel[b]]=RED; st['black2red']=int(b.sum())
    # backings from the lenses
    Fg=np.concatenate([gg['F'] for gg in gl.groups if len(gg['F'])]); Cg=gl.P[Fg].mean(1)
    zone=(Cg[:,0]<-1.75)&(Cg[:,2]>0.55)&(np.abs(Cg[:,1])>0.3)&(np.abs(Cg[:,1])<0.82)
    uvm=gl.UV[Fg].mean(1); clear=np.abs(uvm-CLEAR).max(1)<0.02
    for name,m,col in (('white_bk',zone&clear,WHITE),('red_bk',zone&~clear,RED)):
        if not m.any(): continue
        Fb=Fg[m]; vs,inv=np.unique(Fb.ravel(),return_inverse=True)
        N=gl.N[vs]/np.maximum(np.linalg.norm(gl.N[vs],axis=1,keepdims=True),1e-12)
        # inward = opposite to the lens normal where it faces out (rear/sides); lens faces point to -x or sideways
        out=np.c_[np.minimum(N[:,0],0)*0+N[:,0],N[:,1],N[:,2]]
        Pb=gl.P[vs]-DEPTH*out
        o=pm.add_verts(Pb,N,np.tile(col,(len(vs),1)),0xFFFFFFFF)
        g['F']=np.r_[g['F'],inv.reshape(-1,3)+o]; st[name]=int(m.sum())
    return st
if __name__=='__main__':
    Z={p['name']:p for p in geo.load(sys.argv[1])}; recs=[]
    for L in 'ABCD':
        for s in ('LEFT','RIGHT'):
            pm=PartMesh(Z['COBALTSS_KIT00_%s_BRAKELIGHT_%s'%(s,L)]); gl=PartMesh(Z['COBALTSS_KIT00_%s_BRAKELIGHT_GLASS_%s'%(s,L)])
            st=edit(pm,gl); recs.append(pm); print(pm.name,st,'verts',len(pm.P))
    with open(sys.argv[2],'wb') as f:
        for pm in recs: b,nv=pm.record(); f.write(b)
