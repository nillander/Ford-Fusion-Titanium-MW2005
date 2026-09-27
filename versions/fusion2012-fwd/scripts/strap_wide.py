"""Cinta de reboque preta (KIT01/KIT05): 30 % mais larga (5 -> 6,5 cm), centrada em y -0,33; suporte junto.
A vermelha (KIT02/KIT04) não muda. Uso: strap_wide.py in.dump out.spec PREFIXO [fator]"""
import sys;sys.path.insert(0,'/home/claude/c12');sys.path.insert(0,'/home/claude/v3/versions/v3-fusion-ajm3899/scripts')
import numpy as np,geo
from partmesh import PartMesh
src,out,pre=sys.argv[1:4]; fac=float(sys.argv[4]) if len(sys.argv)>4 else 1.3
ATLAS={'COBALTSS':0xC195B264,'MUSTANGGT':0x5A006DE9}[pre]; Y=-0.33
Z={p['name']:p for p in geo.load(src)}; recs=[]
for k in ('KIT01','KIT05'):
    for L in 'ABCDE':
        name='%s_%s_BODY_%s'%(pre,k,L); pm=PartMesh(Z[name])
        gs=[g for g in pm.groups if pm.tex[g['ti']]==ATLAS and len(g['F'])<=60]
        assert len(gs)==1,(name,len(gs))
        g=gs[0]; vid=np.unique(g['F'])
        other=np.unique(np.concatenate([x['F'].ravel() for x in pm.groups if x is not g]))
        assert not np.isin(vid,other).any()
        V=pm.P[vid]; assert (np.abs(V[:,1]-Y)<0.04).all() and (V[:,0]>2.3).all()
        pm.P[vid,1]=Y+(V[:,1]-Y)*fac
        b,nv=pm.record(); recs.append(b); print(name,'strap y %.4f..%.4f'%(pm.P[vid,1].min(),pm.P[vid,1].max()),'verts',nv)
open(out,'wb').write(b''.join(recs))
