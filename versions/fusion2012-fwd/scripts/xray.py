import numpy as np
def xcast(P,F,Q,mode='min'):
    """Q (n,2) yz points; returns x of min (outermost at rear) hit through triangles (P,F) along x; nan if none"""
    T=P[F]; out=np.full(len(Q),np.nan)
    y=T[:,:,1]; z=T[:,:,2]
    ymin,ymax,zmin,zmax=y.min(1),y.max(1),z.min(1),z.max(1)
    cs=0.01; bins={}
    for i in range(len(T)):
        for a in range(int(np.floor(ymin[i]/cs)),int(np.floor(ymax[i]/cs))+1):
            for b in range(int(np.floor(zmin[i]/cs)),int(np.floor(zmax[i]/cs))+1):
                bins.setdefault((a,b),[]).append(i)
    for k,(qy,qz) in enumerate(Q):
        l=bins.get((int(np.floor(qy/cs)),int(np.floor(qz/cs))))
        if not l: continue
        t=T[l]; a=t[:,0,1:];b=t[:,1,1:];c=t[:,2,1:]
        v0=b-a;v1=c-a;v2=np.array([qy,qz])-a
        den=v0[:,0]*v1[:,1]-v1[:,0]*v0[:,1]; ok=np.abs(den)>1e-14
        u=np.where(ok,(v2[:,0]*v1[:,1]-v1[:,0]*v2[:,1])/np.where(ok,den,1),-1)
        v=np.where(ok,(v0[:,0]*v2[:,1]-v2[:,0]*v0[:,1])/np.where(ok,den,1),-1)
        inside=ok&(u>=-1e-9)&(v>=-1e-9)&(u+v<=1+1e-9)
        if not inside.any(): continue
        xs=(t[:,0,0]+u*(t[:,1,0]-t[:,0,0])+v*(t[:,2,0]-t[:,0,0]))[inside]
        out[k]=xs.min() if mode=='min' else xs.max()
    return out
