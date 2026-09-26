import sys;sys.path.insert(0,'/home/claude/c12');sys.path.insert(0,'/home/claude/v3/versions/v3-fusion-ajm3899/scripts')
import numpy as np,geo
from partmesh import PartMesh
def tables(Z,pre,s,sg,xs):
    b=PartMesh(Z['%s_KIT00_BODY_A'%pre]); Fb=np.concatenate([g['F'] for g in b.groups if b.tex[g['ti']] in (0xB637F71F,0x9A8AAD9E)])
    Vb=b.P[np.unique(Fb)]; Vb=Vb[(sg*Vb[:,1]>0.5)]
    l=PartMesh(Z['%s_KIT00_%s_BRAKELIGHT_GLASS_A'%(pre,s)]); P=l.P[np.unique(np.concatenate([g['F'] for g in l.groups]))]
    rows=[]
    for x in xs:
        m=np.abs(P[:,0]-x)<0.006
        if m.sum()<3: rows.append((x,np.nan,np.nan,np.nan,np.nan)); continue
        ly=(sg*P[m,1]).max(); z0,z1=P[m,2].min(),P[m,2].max()
        mb=np.abs(Vb[:,0]-x)<0.012
        up=Vb[mb&(Vb[:,2]>z1)&(Vb[:,2]<z1+0.03)]; dn=Vb[mb&(Vb[:,2]<z0)&(Vb[:,2]>z0-0.03)]
        uy=(sg*up[:,1]).max() if len(up) else np.nan; dy=(sg*dn[:,1]).max() if len(dn) else np.nan
        rows.append((x,ly,uy,dy,np.nanmean([uy,dy])-ly))
    return np.array(rows)
if __name__=='__main__':
    Z={p['name']:p for p in geo.load(sys.argv[1])}
    xs=np.arange(-2.25,-1.74,0.025)
    for s,sg in (('LEFT',1),('RIGHT',-1)):
        R=tables(Z,'COBALTSS',s,sg,xs); print(s)
        for r in R: print('  x %.3f lamp %.4f  body_up %.4f body_dn %.4f  gap %6.1f mm'%(r[0],r[1],r[2],r[3],r[4]*1e3))
