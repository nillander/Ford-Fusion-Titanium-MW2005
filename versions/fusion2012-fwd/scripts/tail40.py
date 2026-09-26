"""Item 39b (Fusion 2012): lanternas ainda para dentro na lateral — a borda de CIMA.
Medido por fatias em x: na parte lateral (x −2,15 a −1,85) a borda de baixo da lente já está no nível da lataria, mas a
borda de cima fica 3–4,5 cm para dentro (a lente "olha" para cima e a lataria acima forma uma aba saliente). A
lanterna (lente e interior, LODs A–D) recebe um cisalhamento em y pela altura: deslocamento = gap_topo(x)·t, com
t = (z − z_baixo)/(z_cima − z_baixo) da fatia (0 na borda de baixo, 1 na de cima), gap medido 4 mm acima da borda e
menos FL de folga; suavizado em x, rampa na quina de trás (0 em x ≤ XA, cheio a partir de XB).
Uso: tail40.py in.dump out.spec PRE [XA XB FL]"""
import sys;sys.path.insert(0,'/home/claude/c12');sys.path.insert(0,'/home/claude/v3/versions/v3-fusion-ajm3899/scripts')
import numpy as np,geo
from partmesh import PartMesh
from tailtb import tb
from scipy.ndimage import median_filter,gaussian_filter1d
XA=float(sys.argv[4]) if len(sys.argv)>4 else -2.21
XB=float(sys.argv[5]) if len(sys.argv)>5 else -2.16
FL=float(sys.argv[6]) if len(sys.argv)>6 else 0.003
def profile(Z,pre,s,sg):
    xs=np.arange(-2.30,-1.70,0.0125); R=tb(Z,s,sg,xs,pre)
    zb,zt,gt=R[:,1],R[:,2],R[:,6]
    ok=~np.isnan(zt); last=np.where(ok)[0].max(); first=np.where(ok)[0].min()
    for a in (zb,zt):
        a[:first]=a[first]; a[last+1:]=a[last]
        bad=np.isnan(a); a[bad]=np.interp(xs[bad],xs[~bad],a[~bad])
    g=gt.copy(); g[np.isnan(g)|(g<0)]=np.nan
    good=~np.isnan(g); g=np.interp(xs,xs[good],g[good])
    g=median_filter(g,5,mode='nearest'); g=gaussian_filter1d(g,1.5,mode='nearest')
    g=np.clip(g-FL,0,0.05)
    w=np.clip((xs-XA)/(XB-XA),0,1); w=w*w*(3-2*w)
    return xs,zb,zt,g*w
if __name__=='__main__':
    src,out,pre=sys.argv[1:4]; Z={p['name']:p for p in geo.load(src)}; recs=[]
    for s,sg in (('LEFT',1),('RIGHT',-1)):
        xs,zb,zt,g=profile(Z,pre,s,sg); print(s,' '.join('%.3f:%.1f'%(x,v*1e3) for x,v in zip(xs,g) if v>0.0005))
        for L in 'ABCDE':
            for part in ('BRAKELIGHT','BRAKELIGHT_GLASS'):
                n='%s_KIT00_%s_%s_%s'%(pre,s,part,L)
                if n not in Z: continue
                pm=PartMesh(Z[n]); m=sg*pm.P[:,1]>0.2; P=pm.P[m]
                b=np.interp(P[:,0],xs,zb); t=np.interp(P[:,0],xs,zt)
                tt=np.clip((P[:,2]-b)/np.maximum(t-b,0.01),-0.2,1.2)
                pm.P[np.where(m)[0],1]+=sg*np.interp(P[:,0],xs,g)*np.clip(tt,0,None); recs.append(pm)
    with open(out,'wb') as f:
        for pm in recs: b,nv=pm.record(); f.write(b)
