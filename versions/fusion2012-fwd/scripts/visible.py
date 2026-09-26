import numpy as np, rast
def visible(P,F,views,W=1600,H=1200,center=None,scale=None,cand=None):
    vis=np.zeros(len(F),bool)
    col=np.ones((len(F),3),np.float32)
    for az,el in views:
        _,ids=rast.render(P,F,col,az=az,el=el,W=W,H=H,center=center,scale=scale,shade=False)
        u=np.unique(ids[ids>=0]); vis[u]=True
    return vis
