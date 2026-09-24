import geo,render,sys,numpy as np
from PIL import Image
P=geo.load(sys.argv[1]); out=sys.argv[2]
# color by (part, group, beyond65535)
FIX={('BASE_A',2,False):(1,0.85,0),('BASE_A',4,False):(0,0.5,1),('BASE_A',4,True):(1,0,0),('KIT00_BODY_A',0,False):(0.75,0.75,0.75),('KIT00_BODY_A',0,True):(1,0,1),('BASE_A',3,False):(0,0.8,0),('BASE_A',0,False):(0,1,1),('KIT00_RIGHT_SIDE_MIRROR_A',0,False):(0,0.5,1)}
names={}
for p in P:
    ng=[]
    for gi,g in enumerate(p['groups']):
        o,l=g['offset'],g['length']; cut=min(max(65535-65535%3-o,0),l)
        if cut>0: ng.append(dict(g,length=cut,beyond=False,gi=gi))
        if l-cut>0: ng.append(dict(g,offset=o+cut,length=l-cut,beyond=True,gi=gi))
    p['groups']=ng
keys=[]
def col(p,g):
    gg=p['groups'][g]; k=(p['name'][10:],gg['gi'],gg['beyond'])
    if k not in keys: keys.append(k)
    return FIX.get(k,(0.3,0.3,0.3))
im=render.render(P,0,3,[],W=1800,H=1200,scale=1400,select=lambda n:n.endswith('_A') and 'KIT01' not in n and 'KIT02' not in n,color_by=col,cull=True)
Image.fromarray(im).crop((300,0,1500,700)).save(out)

