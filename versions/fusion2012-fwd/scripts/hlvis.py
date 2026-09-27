"""Item 42 (Fusion 2012): peças da carcaça do farol (HEADLIGHT) e da moldura preta junto à ponta do farol que aparecem
por fora (não vistas através da lente) são apagadas — eram as lascas pretas/laranja em volta da lente e na ponta junto
à grade. Visibilidade por id-buffer em 120 direções, para cada nível de detalhe (A–D) com as peças do mesmo nível.
Uso: hlvis.py in.dump out.spec"""
import sys;sys.path.insert(0,'/home/claude/c12');sys.path.insert(0,'/home/claude/v3/versions/v3-fusion-ajm3899/scripts')
import numpy as np,geo,mwsoup
from partmesh import PartMesh
from vis import visible
from hl29 import frame
from scipy.ndimage import binary_dilation
from matplotlib.path import Path
P=geo.load(sys.argv[1]); names=[p['name'] for p in P]; recs=[]
for L in 'ABCD':
    def sel(n,L=L):
        if not n.endswith('_'+L) or 'DECAL' in n or 'DRIVER' in n: return False
        if 'KIT0' in n and 'KIT00' not in n: return False
        return not ('STYLE' in n or 'SCOOP' in n or 'SPOILER' in n)
    S=mwsoup.soup(P,sel); seen=visible(S['P'],S['F'])
    for side,sg in (('LEFT',1),('RIGHT',-1)):
        n='COBALTSS_KIT00_%s_HEADLIGHT_%s'%(side,L); pi=names.index(n); pm=PartMesh(P[pi]); tot=0
        gl=PartMesh(P[names.index('COBALTSS_KIT00_%s_HEADLIGHT_GLASS_A'%side)]); Fg,nn,a,b,c0=frame(gl)
        # lens mask in the lens plane (1 mm grid), from the lens triangles
        T2=np.stack([(gl.P[Fg]-c0)@a,(gl.P[Fg]-c0)@b],-1); lo=T2.reshape(-1,2).min(0)-0.02; hi=T2.reshape(-1,2).max(0)+0.02
        gx=np.arange(lo[0],hi[0],0.001); gy=np.arange(lo[1],hi[1],0.001); GX,GY=np.meshgrid(gx,gy); pts=np.c_[GX.ravel(),GY.ravel()]
        mask=np.zeros(len(pts),bool)
        for t in T2:
            bb=(pts[:,0]>=t[:,0].min())&(pts[:,0]<=t[:,0].max())&(pts[:,1]>=t[:,1].min())&(pts[:,1]<=t[:,1].max())
            if bb.any(): mask[np.where(bb)[0][Path(t).contains_points(pts[bb],radius=1e-9)|Path(t[::-1]).contains_points(pts[bb],radius=1e-9)]]=True
        mask=binary_dilation(mask.reshape(GX.shape),iterations=1)
        def inside(Q):
            i=np.clip(((Q[:,1]-lo[1])/0.001).astype(int),0,len(gy)-1); j=np.clip(((Q[:,0]-lo[0])/0.001).astype(int),0,len(gx)-1); return mask[i,j]
        for gi,g in enumerate(pm.groups):
            m=(S['part']==pi)&(S['grp']==gi); sv=seen[m]
            if len(sv)!=len(g['F']): continue
            C=pm.P[g['F']].mean(1); Q=np.c_[(C-c0)@a,(C-c0)@b]; rm=sv&(C[:,2]>0.35)&(sg*C[:,1]>0.3)&~inside(Q)
            g['F']=g['F'][~rm]; tot+=rm.sum()
        print(n,'visible housing faces removed',tot,flush=True); recs.append(pm)
with open(sys.argv[2],'wb') as f:
    for pm in recs: b,nv=pm.record(); f.write(b)
