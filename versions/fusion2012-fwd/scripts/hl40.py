"""Item 37b (Fusion 2012): faróis girados "para dentro" (pedido do teste de 26/09).
No jogo a ponta de trás (junto ao paralama) sobrava para fora e a ponta da frente (junto à grade) ficava para dentro.
Medido: a borda da lente fica ~2,4 cm acima da lataria na ponta de trás e ~1 cm na da frente. O farol (lente e
interior, LODs A–D) gira em torno do eixo vertical da lente (b), passando por um pivô a U0 do centro para o lado da
grade, de ANG graus: a ponta de trás entra, a da frente sai.
Uso: hl40.py in.dump out.spec [ANG U0]"""
import sys;sys.path.insert(0,'/home/claude/c12');sys.path.insert(0,'/home/claude/v3/versions/v3-fusion-ajm3899/scripts')
import numpy as np,geo
from partmesh import PartMesh
from hl29 import frame
ANG=float(sys.argv[3]) if len(sys.argv)>3 else 1.5
U0=float(sys.argv[4]) if len(sys.argv)>4 else 0.12
def rot(axis,ang):
    k=axis/np.linalg.norm(axis); K=np.array([[0,-k[2],k[1]],[k[2],0,-k[0]],[-k[1],k[0],0]])
    return np.eye(3)+np.sin(ang)*K+(1-np.cos(ang))*K@K
if __name__=='__main__':
    Z={p['name']:p for p in geo.load(sys.argv[1])}; recs=[]
    for side,sg in (('LEFT',1),('RIGHT',-1)):
        gl=PartMesh(Z['COBALTSS_KIT00_%s_HEADLIGHT_GLASS_A'%side]); F,n,a,b,c0=frame(gl)
        inner=a if (c0+0.1*a)[1]*sg<(c0-0.1*a)[1]*sg else -a      # direction toward the grille
        p0=c0+U0*inner
        R=rot(b,np.radians(ANG)); outer_pt=c0-0.3*inner
        if ((R@(outer_pt-p0)+p0-outer_pt)@n)>0: R=rot(b,-np.radians(ANG))
        d_out=(R@(outer_pt-p0)+p0-outer_pt)@n; inner_pt=c0+0.3*inner; d_in=(R@(inner_pt-p0)+p0-inner_pt)@n
        print(side,'outer end %.1f mm, inner end %+.1f mm along lens normal'%(d_out*1e3,d_in*1e3))
        for L in 'ABCD':
            for part in ('HEADLIGHT','HEADLIGHT_GLASS'):
                pm=PartMesh(Z['COBALTSS_KIT00_%s_%s_%s'%(side,part,L)]); v=np.unique(np.concatenate([g['F'] for g in pm.groups if len(g['F'])]))
                v=v[(pm.P[v,2]>0.33)&(pm.P[v,0]>1.6)&(sg*pm.P[v,1]>0.3)]
                pm.P[v]=(pm.P[v]-p0)@R.T+p0; pm.N[v]=pm.N[v]@R.T; recs.append(pm)
    with open(sys.argv[2],'wb') as f:
        for pm in recs: bb,nv=pm.record(); f.write(bb)
