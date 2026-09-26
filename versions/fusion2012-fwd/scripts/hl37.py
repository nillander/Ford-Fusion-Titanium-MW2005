"""Item 37 (Fusion 2012): faróis ainda para dentro da lataria. Como nas lanternas (item 28), o farol (lente e
interior, LODs A–D) é aumentado no plano da lente, a partir do centro da lente, só para o lado da grade (SA) e para
baixo (SB) — a ponta de fora e a borda de cima encostam no paralama/capô e, maiores, atravessavam a lataria;
a profundidade (ao longo da normal da lente) não muda. A borda maior entra sob a lataria em volta e cobre o rebaixo."""
import sys;sys.path.insert(0,'/home/claude/c12');sys.path.insert(0,'/home/claude/v3/versions/v3-fusion-ajm3899/scripts')
import numpy as np,geo
from partmesh import PartMesh
from hl29 import frame
from matplotlib.path import Path
from scipy.spatial import ConvexHull
CUT=True
import os;MR=float(os.environ.get("MR","0.008"))
SA=float(sys.argv[3]) if len(sys.argv)>3 else 1.05; SB=float(sys.argv[4]) if len(sys.argv)>4 else 1.08
OUT=float(sys.argv[5]) if len(sys.argv)>5 else 0.0; SYM=len(sys.argv)>6 and sys.argv[6]=='sym'
if __name__=='__main__':
    Z={p['name']:p for p in geo.load(sys.argv[1])}; recs=[]
    for side,sg in (('LEFT',1),('RIGHT',-1)):
        gl0=PartMesh(Z['COBALTSS_KIT00_%s_HEADLIGHT_GLASS_A'%side]); F,n,a,b,c0=frame(gl0)
        G0=np.c_[(gl0.P[np.unique(F)]-c0)@a,(gl0.P[np.unique(F)]-c0)@b]; hull=G0[ConvexHull(G0).vertices]
        for L in 'ABCD':
            for part in ('HEADLIGHT','HEADLIGHT_GLASS'):
                pm=PartMesh(Z['COBALTSS_KIT00_%s_%s_%s'%(side,part,L)]); v=np.unique(np.concatenate([g['F'] for g in pm.groups if len(g['F'])]))
                v=v[(pm.P[v,2]>0.33)&(pm.P[v,0]>1.6)&(sg*pm.P[v,1]>0.3)]
                Q=pm.P[v]-c0; qa=Q@a; qb=Q@b; qn=Q@n
                # grow only toward the grille (inner end) and downward (bumper side): the outer tip and the top edge
                # touch fender/hood, where a bigger lamp pokes through the body
                inner=np.sign(((c0+0.1*a)[1]**2-(c0-0.1*a)[1]**2))   # +1 if +a points outward
                ia=np.where(qa*inner<0,SA,1.0); up=np.sign((b)[2]); ib=np.where(qb*up<0,SB,1.0)
                if SYM: ia=np.full_like(qa,SA); ib=np.full_like(qb,SB)
                pm.P[v]=c0+np.outer(qa*ia,a)+np.outer(qb*ib,b)+np.outer(qn+OUT,n)
                if CUT and part=='HEADLIGHT':
                    # housing pieces outside the (scaled) lens outline stick through the fender/hood: drop them
                    H=Path(hull*np.array([SA,SB])); rm_tot=0
                    for g in pm.groups:
                        C=pm.P[g['F']].mean(1); Q2=np.c_[(C-c0)@a,(C-c0)@b]
                        rm=(C[:,2]>0.35)&(sg*C[:,1]>0.3)&~H.contains_points(Q2,radius=MR)&~H.contains_points(Q2,radius=-MR)
                        g['F']=g['F'][~rm]; rm_tot+=rm.sum()
                    print(pm.name,'housing tris removed',rm_tot)
                recs.append(pm)
    with open(sys.argv[2],'wb') as f:
        for pm in recs: bb,nv=pm.record(); f.write(bb)
