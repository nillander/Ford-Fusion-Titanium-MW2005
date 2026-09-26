"""Item 28 (Fusion 2012): lanternas traseiras maiores, para encaixarem no nicho da lataria.
Escala de cada lanterna (lentes, interior e fundos, LODs A–D) em coordenadas cilíndricas em volta de um eixo vertical
em (x -1,80; |y| 0,30): ao longo da lanterna (u = ângulo × 0,49 m) SU, na altura SZ, a partir do centro da lente; a
profundidade (raio) de cada ponto não muda. Onde a lataria em volta está mais alta, ela cobre a borda da lanterna
(fica "encaixada"); onde está afundada, a lanterna cobre o afundamento."""
import sys;sys.path.insert(0,'/home/claude/v3/versions/v3-fusion-ajm3899/scripts');sys.path.insert(0,'/home/claude/c12')
import numpy as np,geo
from partmesh import PartMesh
from fit28 import polar,unpolar,R0
SU=float(sys.argv[3]) if len(sys.argv)>3 else 1.05; SZ=float(sys.argv[4]) if len(sys.argv)>4 else 1.10
def center(Z,side,sg):
    g=PartMesh(Z['COBALTSS_KIT00_%s_BRAKELIGHT_GLASS_A'%side]); v=np.unique(np.concatenate([x['F'] for x in g.groups])); v=v[(g.P[v,0]<-1.7)&(g.P[v,2]>0.55)&(sg*g.P[v,1]>0.25)]
    U=polar(g.P[v],sg); return np.array([(U[:,0].min()+U[:,0].max())/2,(U[:,1].min()+U[:,1].max())/2])
if __name__=='__main__':
    Z={p['name']:p for p in geo.load(sys.argv[1])}; recs=[]
    for sg,side in ((1,'LEFT'),(-1,'RIGHT')):
        c=center(Z,side,sg)
        for L in 'ABCD':
            for part in ('BRAKELIGHT','BRAKELIGHT_GLASS'):
                pm=PartMesh(Z['COBALTSS_KIT00_%s_%s_%s'%(side,part,L)]); P=pm.P
                v=np.unique(np.concatenate([g['F'] for g in pm.groups if len(g['F'])])); v=v[(P[v,0]<-1.7)&(P[v,2]>0.55)&(sg*P[v,1]>0.25)]
                U=polar(P[v],sg); Un=U.copy(); Un[:,0]=c[0]+(U[:,0]-c[0])*SU; Un[:,1]=c[1]+(U[:,1]-c[1])*SZ
                pm.P[v]=unpolar(Un,sg)
                dth=(Un[:,0]-U[:,0])/R0*sg; cc,ss=np.cos(dth),np.sin(dth); nx,ny=pm.N[v,0].copy(),pm.N[v,1].copy()
                pm.N[v,0]=cc*nx-ss*ny; pm.N[v,1]=ss*nx+cc*ny
                recs.append(pm)
        print(side,'center u %.3f z %.3f'%tuple(c))
    with open(sys.argv[2],'wb') as f:
        for pm in recs: b,nv=pm.record(); f.write(b)
