import geo,render,sys
from PIL import Image
P=geo.load(sys.argv[1]); out=sys.argv[2]; rule=sys.argv[3]
for p in P:
    ng=[]; 
    for gi,g in enumerate(p['groups']):
        o,l=g['offset'],g['length']
        if rule=='start' :
            if o<65536: ng.append(g)
        elif rule=='end':
            cut=min(max(65535-65535%3-o,0),l)
            if cut>0: ng.append(dict(g,length=cut))
        elif rule=='end_multi':  # truncation only when part has >1 group
            if len(p['groups'])==1: ng.append(g)
            else:
                cut=min(max(65535-65535%3-o,0),l)
                if cut>0: ng.append(dict(g,length=cut))
    p['groups']=ng
sel=lambda n:n.endswith('_A')
ims=[Image.fromarray(render.render(P,a,e,sys.argv[4:],W=700,H=500,scale=130,select=sel,cull=True)) for a,e in [(10,8),(160,10),(215,15)]]
o=Image.new('RGB',(2100,500))
for i,im in enumerate(ims): o.paste(im,(700*i,0))
o.save(out)
