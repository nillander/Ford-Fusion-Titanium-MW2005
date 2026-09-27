"""visible-from-outside faces via id buffers from many orthographic directions"""
import sys;sys.path.insert(0,'/home/claude/c12');sys.path.insert(0,'/home/claude/v3/versions/v3-fusion-ajm3899/scripts')
import numpy as np,rast
def visible(P,F,naz=24,els=(-10,5,20,40,65),W=900,H=500):
    seen=np.zeros(len(F),bool); col=np.ones((len(F),3),np.float32)
    for el in els:
        for az in np.linspace(0,360,naz,endpoint=False):
            _,ids=rast.render(P,F,col,az=az,el=el,W=W,H=H,cull=True,shade=False)
            u=np.unique(ids[ids>=0]); seen[u]=True
    return seen
