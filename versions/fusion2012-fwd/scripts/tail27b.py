"""Item 27 (v2): lanterna da tampa idêntica à parte externa, uma continuação da outra.
Pedido: anel externo em lente vermelha viva, miolo em lente branca uniforme (sem aletas), nas duas partes.
- Peças KIT00_LEFT/RIGHT_BRAKELIGHT_A–D (atlas <CARRO>_KIT00_HEADLIGHT_OFF):
  * faces do interior da tampa que estavam viradas para dentro do carro (normal +x): desviradas (ordem dos vértices e
    normais), para sombrear como as da parte externa (antes ficavam escuras no jogo);
  * anel: vermelho sólido do atlas (0,25; 0,75) = (222,8,8) nas duas partes (tampa e lateral);
  * miolo: branco sólido (0,5625; 0,6875) = (239,235,239) — fundo laranja, moldura prata e área da ré;
  * aletas cromadas e barra horizontal do miolo removidas (peças finas soltas no miolo).
- As lentes (_GLASS) não mudam: a vermelha cobre o anel, a transparente cobre o miolo."""
import sys;sys.path.insert(0,'/home/claude/v3/versions/v3-fusion-ajm3899/scripts');sys.path.insert(0,'/home/claude/c12')
import numpy as np,geo
from partmesh import PartMesh
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
RED=np.array((0.25,0.75)); WHITE=np.array((0.5625,0.6875))
CELLS_RED=[(0.8125,0.6875),(0.714,0.36),(0.729,0.187),(0.714,0.359),(0.713,0.359),(0.713,0.36),(0.714,0.361),(0.73,0.187)]
CELLS_WHITE=[(0.6875,0.5625),(0.688,0.562),(0.896,0.476),(0.897,0.476)]
def near(uv,cells,tol=0.004):
    m=np.zeros(len(uv),bool)
    for c in cells: m|=np.abs(uv-np.array(c)).max(1)<tol
    return m
def edit(pm):
    P=pm.P; stats=dict(flip=0,red=0,white=0,removed=0)
    for g in pm.groups:
        F=g['F']
        if not len(F): continue
        key=np.round(P/1e-4).astype(np.int64);_,w=np.unique(key,axis=0,return_inverse=True);w=w.ravel()
        W=w[F];n=w.max()+1;r=np.r_[W[:,0],W[:,1],W[:,2]];c=np.r_[W[:,1],W[:,2],W[:,0]]
        _,lab=connected_components(coo_matrix((np.ones(len(r)),(r,c)),shape=(n,n)),directed=False);fl=lab[W[:,0]]
        fn=np.cross(P[F[:,1]]-P[F[:,0]],P[F[:,2]]-P[F[:,0]]); A=np.linalg.norm(fn,axis=1)/2
        T=P[F]; C=T.mean(1); ay=np.abs(C[:,1])
        keep=np.ones(len(F),bool); flip=np.zeros(len(F),bool)
        for L in np.unique(fl):
            k=fl==L; Tk=T[k]; ayk=np.abs(Tk[:,:,1])
            lid=(ayk.max()<0.59)&(Tk[:,:,2].min()>0.55)&(Tk[:,:,0].max()<-1.9)
            fx=(fn[k,0]).sum()/max(A[k].sum()*2,1e-12)
            if lid and fx>0.02: flip[k]=True
            # thin loose pieces in the inner area (slats: thin in y; bar: thin in z), fender side
            ext=Tk.reshape(-1,3).max(0)-Tk.reshape(-1,3).min(0)
            inner=(ayk.min()>0.57)&(Tk[:,:,2].min()>0.675)&(Tk[:,:,2].max()<0.77)
            if inner and (ext[1]<0.012 or ext[2]<0.012) and k.sum()<400: keep[k]=False
        g['F']=np.where(flip[:,None],F[:,[0,2,1]],F)[keep]; stats['flip']+=int((flip&keep).sum()); stats['removed']+=int((~keep).sum())
        vf=np.unique(F[flip].ravel()); pm.N[vf]=-pm.N[vf]
    # colours (per vertex, only vertices of the interior part: x < -1.75, z > 0.55, |y| between 0.3 and 0.82)
    used=np.unique(np.concatenate([g['F'] for g in pm.groups if len(g['F'])]))
    sel=used[(P[used,0]<-1.75)&(P[used,2]>0.55)&(np.abs(P[used,1])>0.3)&(np.abs(P[used,1])<0.82)]
    uv=pm.UV[sel]
    r=near(uv,CELLS_RED); wt=near(uv,CELLS_WHITE)
    # remaining black ring cells on the lid side of the far LODs were made red in v1 (0.8125,0.6875) -> covered above
    pm.UV[sel[r]]=RED; pm.UV[sel[wt]]=WHITE; stats['red']=int(r.sum()); stats['white']=int(wt.sum())
    return stats
if __name__=='__main__':
    Z={p['name']:p for p in geo.load(sys.argv[1])}; recs=[]
    pre=sys.argv[3] if len(sys.argv)>3 else 'COBALTSS'
    for L in 'ABCD':
        for s in ('LEFT','RIGHT'):
            pm=PartMesh(Z['%s_KIT00_%s_BRAKELIGHT_%s'%(pre,s,L)]); st=edit(pm); recs.append(pm); print(pm.name,st)
    with open(sys.argv[2],'wb') as f:
        for pm in recs: b,nv=pm.record(); f.write(b)
