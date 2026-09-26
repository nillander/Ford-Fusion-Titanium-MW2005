"""Item 36 (Fusion 2012 e 2018): antena tubarão com a traseira reta.
A ponta de trás da antena (x < −1,095) afinava num "V" (cônica, vista de trás). Os vértices das camadas da antena
(carcaça, camada de fundo e bases; componentes soldados de 15–25 cm de comprimento sobre o teto em |y| < 0,1) com
x < XC são levados para o plano x = XC: a traseira vira uma face plana vertical com o perfil em arco da antena,
lados retos até o teto (90°). O "V" que sobrava embaixo da face (dava para ver o teto) é fechado com um triângulo até o teto. A antena toda recua o mesmo tanto (1,7 cm) para manter a posição da traseira.
Normais dos vértices achatados = (−1, 0, 0). KIT00/01/02/04/05_BODY_A–E."""
import sys;sys.path.insert(0,'/home/claude/v3/versions/v3-fusion-ajm3899/scripts');sys.path.insert(0,'/home/claude/c12')
import numpy as np,geo
from partmesh import PartMesh
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
XC=-1.095; SHIFT=-0.017
def fin_verts(pm):
    X=pm.P; out=set()
    for g in pm.groups:
        F=g['F']
        if not len(F): continue
        C=X[F].mean(1); m=(C[:,2]>1.1)&(np.abs(C[:,1])<0.1)&(C[:,0]<-0.85)&(C[:,0]>-1.2); Fm=F[m]
        if not len(Fm): continue
        key=np.round(X/1e-5).astype(np.int64);_,w=np.unique(key,axis=0,return_inverse=True);w=w.ravel()
        W=w[Fm];n=w.max()+1;r=np.r_[W[:,0],W[:,1],W[:,2]];c=np.r_[W[:,1],W[:,2],W[:,0]]
        _,lab=connected_components(coo_matrix((np.ones(len(r)),(r,c)),shape=(n,n)),directed=False);fl=lab[W[:,0]]
        for L in np.unique(fl):
            T=X[Fm[fl==L]].reshape(-1,3); e=T.max(0)-T.min(0)
            if 0.15<e[0]<0.25 and e[1]<0.12 and T[:,2].min()>1.16: out|=set(Fm[fl==L].ravel().tolist())
    return np.array(sorted(out))
def fix(pm):
    v=fin_verts(pm)
    if not len(v): return 0
    back=pm.P[v,0]<XC; pm.P[v[back],0]=XC; pm.N[v[back]]=(-1,0,0)
    # close the "V" notch at the bottom of the back face with a triangle down to the roof
    bv=v[np.abs(pm.P[v,0]-XC)<1e-6]; B=pm.P[bv]
    L=bv[np.argmin(B[:,1])]; R=bv[np.argmax(B[:,1])]
    c=np.abs(B[:,1])<0.004; A=bv[c][np.argmin(B[c,2])] if c.any() else None
    if A is not None and pm.P[A,2]>max(pm.P[L,2],pm.P[R,2])+0.003:
        P3=pm.P[[L,R,A]].copy(); zr=min(P3[0,2],P3[1,2]); P3[0,2]=P3[1,2]=zr-0.003
        o=pm.add_verts(P3,np.tile((-1.0,0,0),(3,1)),pm.UV[[L,R,A]],pm.C[[L,R,A]])
        g=[g for g in pm.groups if len(g['F']) and np.isin(g['F'],v).any()][0]
        tri=np.array([[o,o+1,o+2]]); fn=np.cross(P3[1]-P3[0],P3[2]-P3[0])
        if fn[0]>0: tri=tri[:,[0,2,1]]
        g['F']=np.r_[g['F'],tri]
        # vertices of the fin sitting on the roof at the back: straight bottom edge
    pm.P[v,0]+=SHIFT
    if 'o' in dir(): pm.P[o:o+3,0]+=SHIFT
    return len(v)
if __name__=='__main__':
    src,out,pre=sys.argv[1:4]; Z={p['name']:p for p in geo.load(src)}; recs=[]
    for k in ('KIT00','KIT01','KIT02','KIT04','KIT05'):
        for L in 'ABCDE':
            n='%s_%s_BODY_%s'%(pre,k,L)
            if n not in Z: continue
            pm=PartMesh(Z[n]); c=fix(pm); recs.append(pm); print(n,c)
    with open(out,'wb') as f:
        for pm in recs: b,nv=pm.record(); f.write(b)
