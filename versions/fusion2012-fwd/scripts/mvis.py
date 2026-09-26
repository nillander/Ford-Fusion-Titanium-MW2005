from common import *
from visible import visible
M=S['M'];F=S['F']
views=[(a,e) for a in range(0,360,20) for e in (-15,0,15,35,60)]
vis=np.zeros(len(F),bool)
col=np.ones((len(F),3),np.float32)
for az,el in views:
    _,ids=rast.render(M,F,col,az=az,el=el,W=2400,H=1400,shade=False)
    vis[np.unique(ids[ids>=0])]=True
# close-up views of lamp areas for small parts
for c in [(2.0,0.65,0.4),(2.0,-0.65,0.4),(-2.1,0.6,0.65),(-2.1,-0.6,0.65),(-2.2,0,0.7)]:
    for az,el in [(a,e) for a in range(0,360,30) for e in (-10,10,30)]:
        _,ids=rast.render(M,F,col,az=az,el=el,W=1600,H=1200,center=c,scale=3000,shade=False)
        vis[np.unique(ids[ids>=0])]=True
print('visible',vis.sum(),'of',len(F))
pickle.dump(vis,open('mondeo_vis.pkl','wb'))
