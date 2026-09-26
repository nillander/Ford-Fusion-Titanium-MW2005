import sys;sys.path.insert(0,'/home/claude/c12');sys.path.insert(0,'/home/claude/v3/versions/v3-fusion-ajm3899/scripts')
import numpy as np,geo
from partmesh import PartMesh
from hl29 import frame,samp,allF
def meas(Z,side,pre='COBALTSS',step=0.02):
    gl=PartMesh(Z['%s_KIT00_%s_HEADLIGHT_GLASS_A'%(pre,side)]); F,n,a,b,c0=frame(gl)
    pr=lambda Y: np.c_[(Y-c0)@a,(Y-c0)@b,(Y-c0)@n]
    L=pr(samp(gl.P,F,30))
    bods=[PartMesh(Z[pre+'_KIT00_BODY_A'])]+[PartMesh(Z[pre+'_KIT00_HOOD_A'])] if pre+'_KIT00_HOOD_A' in Z else [PartMesh(Z[pre+'_KIT00_BODY_A'])]
    B=np.concatenate([pr(samp(pm.P,allF(pm)[np.linalg.norm(pm.P[allF(pm)].mean(1)-c0,axis=1)<0.5],4)) for pm in bods]); B=B[np.abs(B[:,2])<0.15]
    rows=[]
    for u in np.arange(L[:,0].min(),L[:,0].max()+1e-9,step):
        l=L[np.abs(L[:,0]-u)<0.006]
        if len(l)<10: continue
        i0,i1=l[:,1].argmin(),l[:,1].argmax(); bmin,bmax=l[i0,1],l[i1,1]
        bb=B[np.abs(B[:,0]-u)<0.006]
        hi=bb[(bb[:,1]>bmax+0.004)&(bb[:,1]<bmax+0.03)]; lo=bb[(bb[:,1]<bmin-0.004)&(bb[:,1]>bmin-0.03)]
        gt=hi[:,2].max()-l[i1,2] if len(hi) else np.nan; gb=lo[:,2].max()-l[i0,2] if len(lo) else np.nan
        rows.append((u,gt,gb))
    return np.array(rows),(n,a,b,c0)
if __name__=='__main__':
    Z={p['name']:p for p in geo.load(sys.argv[1])}
    for s in ('LEFT','RIGHT'):
        R,(n,a,b,c0)=meas(Z,s); print(s,'n',np.round(n,2),'a',np.round(a,2),'b',np.round(b,2),'c0',np.round(c0,3))
        for u,gt,gb in R: print('  u %+.3f  gap(b+) %6.1f  gap(b-) %6.1f mm'%(u,gt*1e3,gb*1e3))
