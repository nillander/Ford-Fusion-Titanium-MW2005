import geo,render,sys,numpy as np
from PIL import Image
P=geo.load(sys.argv[1]); out=sys.argv[2]
# split each group into drawable (<65535 end) and beyond parts by creating synthetic groups
for p in P:
    ng=[]
    for gi,g in enumerate(p['groups']):
        o,l=g['offset'],g['length']
        cut=min(max(65535-65535%3-o,0),l)
        if cut>0: ng.append(dict(g,length=cut,beyond=False,gi=gi))
        if l-cut>0: ng.append(dict(g,offset=o+cut,length=l-cut,beyond=True,gi=gi))
    p['groups']=ng
cols=[(0.8,0.8,0.8),(0.2,0.7,1),(0.2,0.9,0.2),(1,0.8,0),(0.7,0.3,1),(0,1,1)]
def col(p,g):
    gg=p['groups'][g]
    if gg['beyond']: return (1,0,0)
    if 'BASE' in p['name']: return cols[gg['gi']%6]
    return (0.85,0.85,0.85)
sel=lambda n:n.endswith('_A')
views=[(0,5,600),(25,10,300),(180,5,300)]
ims=[Image.fromarray(render.render(P,a,e,[],W=900,H=600,scale=s,select=sel,color_by=col,cull=True)) for a,e,s in views]
o=Image.new('RGB',(2700,600))
for i,im in enumerate(ims): o.paste(im,(900*i,0))
o.save(out)
