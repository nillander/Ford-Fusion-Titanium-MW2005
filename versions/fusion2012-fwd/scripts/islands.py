import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
def islands(P,F,tol=1e-4,split_by=None):
    key=np.round(P/tol).astype(np.int64)
    _,vid=np.unique(key,axis=0,return_inverse=True); vid=vid.ravel()
    W=vid[F]; nt=len(F); nv=vid.max()+1
    rows=np.repeat(np.arange(nt),3); cols=W.ravel()
    if split_by is not None:
        # separate vertices per group label so different materials don't connect
        cols=cols+nv*np.repeat(np.asarray(split_by),3); nv2=nv*(np.max(split_by)+1)
    else: nv2=nv
    A=coo_matrix((np.ones(3*nt),(rows,cols)),shape=(nt,nv2)).tocsr()
    G=A@A.T
    n,lab=connected_components(G,directed=False)
    return n,lab
