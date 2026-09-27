"""Item 37d (Fusion 2012): faróis 8 mm mais para a frente (+x, pedido do usuário) e aro da carcaça aparado: peças da
carcaça (HEADLIGHT, LODs A–D) com centro fora do contorno da lente (no plano da lente, margem MR) são removidas — era
a linha escura/laranja em volta da lente e a cunha escura na ponta junto à grade.
Uso: hltrim.py in.dump out.spec [DX MR]"""
import sys;sys.path.insert(0,'/home/claude/c12');sys.path.insert(0,'/home/claude/v3/versions/v3-fusion-ajm3899/scripts')
import numpy as np,geo
from partmesh import PartMesh
from hl29 import frame
from matplotlib.path import Path
from scipy.spatial import ConvexHull
DX=float(sys.argv[3]) if len(sys.argv)>3 else 0.008; MR=float(sys.argv[4]) if len(sys.argv)>4 else 0.001
Z={p['name']:p for p in geo.load(sys.argv[1])}; recs=[]
for side,sg in (('LEFT',1),('RIGHT',-1)):
    gl=PartMesh(Z['COBALTSS_KIT00_%s_HEADLIGHT_GLASS_A'%side]); Fg,n,a,b,c0=frame(gl)
    V=gl.P[np.unique(Fg)]; G=np.c_[(V-c0)@a,(V-c0)@b]; H=Path(G[ConvexHull(G).vertices])
    for L in 'ABCD':
        for part in ('HEADLIGHT','HEADLIGHT_GLASS'):
            pm=PartMesh(Z['COBALTSS_KIT00_%s_%s_%s'%(side,part,L)])
            if part=='HEADLIGHT':
                rm_t=0
                for g in pm.groups:
                    if not len(g['F']): continue
                    C=pm.P[g['F']].mean(1); Q=np.c_[(C-c0)@a,(C-c0)@b]
                    rm=(C[:,2]>0.35)&(sg*C[:,1]>0.3)&~H.contains_points(Q,radius=MR)&~H.contains_points(Q,radius=-MR)
                    g['F']=g['F'][~rm]; rm_t+=rm.sum()
                print(pm.name,'housing faces trimmed',rm_t)
            v=np.unique(np.concatenate([g['F'] for g in pm.groups if len(g['F'])]))
            v=v[(pm.P[v,2]>0.33)&(pm.P[v,0]>1.6)&(sg*pm.P[v,1]>0.3)]; pm.P[v,0]+=DX; recs.append(pm)
with open(sys.argv[2],'wb') as f:
    for pm in recs: bb,nv=pm.record(); f.write(bb)
