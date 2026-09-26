import sys;sys.path.insert(0,'/home/claude/c12');sys.path.insert(0,'/home/claude/v3/versions/v3-fusion-ajm3899/scripts')
import numpy as np,geo
from partmesh import PartMesh
from bulge import samp
def tb(Z,s,sg,xs,pre='COBALTSS',dz=0.004):
    b=PartMesh(Z[pre+'_KIT00_BODY_A']); F=np.concatenate([g['F'] for g in b.groups if b.tex[g['ti']] in (0xB637F71F,0x9A8AAD9E)])
    C=b.P[F].mean(1); F=F[(C[:,0]<-1.6)&(C[:,0]>-2.35)&(sg*C[:,1]>0.4)&(C[:,2]>0.55)]
    S=samp(b.P,F,10)
    l=PartMesh(Z['%s_KIT00_%s_BRAKELIGHT_GLASS_A'%(pre,s)]); L=samp(l.P,np.concatenate([g['F'] for g in l.groups]),10); L=L[sg*L[:,1]>0.3]
    rows=[]
    for x in xs:
        ll=L[np.abs(L[:,0]-x)<0.004]; s_=S[np.abs(S[:,0]-x)<0.004]
        if len(ll)<5: rows.append((x,)+(np.nan,)*6); continue
        it=ll[:,2].argmax(); ib=ll[:,2].argmin(); zt,zb=ll[it,2],ll[ib,2]; yt,yb=sg*ll[it,1],sg*ll[ib,1]
        st=s_[np.abs(s_[:,2]-(zt+dz))<0.0025]; sb=s_[np.abs(s_[:,2]-(zb-dz))<0.0025]
        gt=(sg*st[:,1]).max()-yt if len(st) else np.nan; gb=(sg*sb[:,1]).max()-yb if len(sb) else np.nan
        rows.append((x,zb,zt,yb,yt,gb,gt))
    return np.array(rows)
if __name__=='__main__':
    Z={p['name']:p for p in geo.load(sys.argv[1])}
    for s,sg in (('LEFT',1),('RIGHT',-1)):
        print(s)
        for r in tb(Z,s,sg,np.arange(-2.25,-1.79,0.025)): print('  x %.3f z %.3f..%.3f  y_bot %.3f y_top %.3f  gap bot %5.1f top %5.1f mm'%(r[0],r[1],r[2],r[3],r[4],r[5]*1e3,r[6]*1e3))
