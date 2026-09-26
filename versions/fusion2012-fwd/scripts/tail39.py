"""Item 39 (Fusion 2012): ponta de fora das lanternas (na lateral/para-lama traseiro) ainda afundada sob a lataria.
Medido por fatias em x: na parte lateral (x −2,15 a −1,80) a lente ficava 1,3–3 cm para dentro da borda da lataria
em volta (a borda de cima e a de baixo do buraco da lanterna). A lanterna inteira (lente e interior, LODs A–D) é
deslocada para fora em y, fatia a fatia, pelo quanto falta até a borda (menos FL), suavizado ao longo de x e com
rampa na quina de trás (0 em x ≤ XA, cheio a partir de XB) — a parte de trás, que já está certa, não se move.
Uso: tail39.py in.dump out.spec PRE [XA XB FL]"""
import sys;sys.path.insert(0,'/home/claude/c12');sys.path.insert(0,'/home/claude/v3/versions/v3-fusion-ajm3899/scripts')
import numpy as np,geo
from partmesh import PartMesh
from slice39 import tables
XA=float(sys.argv[4]) if len(sys.argv)>4 else -2.20
XB=float(sys.argv[5]) if len(sys.argv)>5 else -2.14
FL=float(sys.argv[6]) if len(sys.argv)>6 else 0.001
def profile(Z,pre,s,sg):
    xs=np.arange(-2.25,-1.70,0.0125); R=tables(Z,pre,s,sg,xs)
    g=np.clip(np.nan_to_num(R[:,4],nan=0)-FL,0,None)
    ok=~np.isnan(R[:,1]); g[~ok]=0
    # fill the far end (lamp tip) with the last valid value, then smooth
    last=np.where(ok)[0].max(); g[last+1:]=g[last]
    k=np.exp(-0.5*((np.arange(-4,5)*0.0125)/0.02)**2); k/=k.sum(); gs=np.convolve(np.pad(g,4,mode='edge'),k,'valid')
    w=np.clip((xs-XA)/(XB-XA),0,1); w=w*w*(3-2*w)
    return xs,gs*w
if __name__=='__main__':
    src,out,pre=sys.argv[1:4]; Z={p['name']:p for p in geo.load(src)}; recs=[]
    for s,sg in (('LEFT',1),('RIGHT',-1)):
        xs,d=profile(Z,pre,s,sg); print(s,' '.join('%.3f:%.1f'%(x,v*1e3) for x,v in zip(xs,d) if v>0))
        for L in 'ABCDE':
            for part in ('BRAKELIGHT','BRAKELIGHT_GLASS'):
                n='%s_KIT00_%s_%s_%s'%(pre,s,part,L)
                if n not in Z: continue
                pm=PartMesh(Z[n]); m=sg*pm.P[:,1]>0.2
                pm.P[m,1]+=sg*np.interp(pm.P[m,0],xs,d); recs.append(pm)
    with open(out,'wb') as f:
        for pm in recs: b,nv=pm.record(); f.write(b)
