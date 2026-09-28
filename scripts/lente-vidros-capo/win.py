import numpy as np
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
D=np.load('vidros2018.npz')
Cc=np.array([-0.25,0,0.75])
def tri_info(k):
    P,UV,F,T=[D[k+s] for s in ['_P','_UV','_F','_T']]
    A,B,C=P[F[:,0]],P[F[:,1]],P[F[:,2]]; n=np.cross(B-A,C-A); ar=np.linalg.norm(n,axis=1)/2; n=n/(2*ar[:,None]+1e-15)
    c=(A+B+C)/3; d=c-Cc; d/=np.linalg.norm(d,axis=1)[:,None]; s=(n*d).sum(1)
    return P,F,n,ar,c,s,T
def pieces(F,mask,nv):
    idx=np.nonzero(mask)[0]; f=F[idx]
    # triangles connected if share an edge
    e=np.sort(np.concatenate([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),1); t=np.tile(np.arange(len(f)),3)
    key=e[:,0].astype(np.int64)*100000+e[:,1]; o=np.argsort(key); key=key[o]; t=t[o]
    same=np.nonzero(key[1:]==key[:-1])[0]
    g=coo_matrix((np.ones(len(same)),(t[same],t[same+1])),shape=(len(f),len(f)))
    nc,lab=connected_components(g,directed=False)
    out=np.full(len(F),-1); out[idx]=lab; return out
