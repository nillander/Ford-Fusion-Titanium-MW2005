from common import *
# exterior visibility of z10 LOD-A body skins (to separate outer skin from the 4 mm backing)
res={}
for nm in ['KIT00_BODY_A','KIT01_BODY_A','KIT02_BODY_A']:
    p=[q for q in Z if q['name']=='MUSTANGGT_'+nm][0]; T=mwsoup.soup([p])
    vis=np.zeros(len(T['F']),bool); col=np.ones((len(T['F']),3),np.float32)
    for az in range(0,360,20):
        for el in (-15,0,15,35,60):
            _,ids=rast.render(T['P'],T['F'],col,az=az,el=el,W=2400,H=1400,shade=False); vis[np.unique(ids[ids>=0])]=True
    for c in [(2.0,0.65,0.4),(2.0,-0.65,0.4),(-2.1,0.6,0.65),(-2.1,-0.6,0.65),(-2.2,0,0.7),(2.1,0.7,0.25),(2.1,-0.7,0.25)]:
        for az,el in [(a,e) for a in range(0,360,30) for e in (-10,10,30)]:
            _,ids=rast.render(T['P'],T['F'],col,az=az,el=el,W=1600,H=1200,center=c,scale=3000,shade=False); vis[np.unique(ids[ids>=0])]=True
    res[nm]=vis; print(nm,vis.sum(),len(vis))
pickle.dump(res,open('zvis.pkl','wb'))
