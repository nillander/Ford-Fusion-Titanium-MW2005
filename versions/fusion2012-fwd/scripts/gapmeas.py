import sys;sys.path.insert(0,'/home/claude/c12');sys.path.insert(0,'/home/claude/v3/versions/v3-fusion-ajm3899/scripts')
import numpy as np,geo
from partmesh import PartMesh
def slice_pts(pm,y):
    F=np.concatenate([g['F'] for g in pm.groups if len(g['F'])]); P=pm.P; out=[]
    for a,b in ((0,1),(1,2),(2,0)):
        A=P[F[:,a]];B=P[F[:,b]]; d=B[:,1]-A[:,1]; t=(y-A[:,1])/np.where(np.abs(d)<1e-12,1e-12,d); m=(t>=0)&(t<=1)
        out.append(A[m]+t[m,None]*(B[m]-A[m]))
    return np.concatenate(out)
for dump in (sys.argv[1:] if __name__=="__main__" else []):
    Z={p['name']:p for p in geo.load(dump)}; body=PartMesh(Z['COBALTSS_KIT00_BODY_A'])
    print(dump)
    for side,sg in (('LEFT',1),('RIGHT',-1)):
        gl=PartMesh(Z['COBALTSS_KIT00_%s_HEADLIGHT_GLASS_A'%side]); row=[]
        for y in np.arange(0.52,0.86,0.03):
            G=slice_pts(gl,sg*y); 
            if len(G)==0: row.append('  --  '); continue
            lo=G[np.argmin(G[:,2])]           # lens bottom point
            B=slice_pts(body,sg*y); B=B[(B[:,2]<lo[2]+0.01)&(B[:,2]>lo[2]-0.08)&(B[:,0]>lo[0]-0.08)]
            if len(B)==0: row.append('  nb  '); continue
            # skin point closest to lens bottom, measured perpendicular-ish: distance
            dd=np.linalg.norm(B[:,[0,2]]-lo[[0,2]],axis=1); j=np.argmin(dd)
            row.append('%5.1f'%(dd[j]*1e3))
        print('  %-5s gap mm (y .52->.85):'%side,' '.join(row))
