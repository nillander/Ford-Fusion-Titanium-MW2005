import geo,render,sys
from PIL import Image
P=geo.load(sys.argv[1]); out=sys.argv[2]; lod=sys.argv[3] if len(sys.argv)>3 else 'A'
def col(p,g):
    n=p['name']
    if 'HEADLIGHT' in n or 'BRAKELIGHT' in n: return (1,0.9,0) if 'LEFT' in n else (0,0.9,1)
    return (0.75,0.75,0.75)
sel=lambda n:n.endswith('_'+lod) and 'SPOILER' not in n
angs=[(-30,5),(-10,5),(10,5),(30,5),(150,5),(170,5),(190,5),(210,5)]
ims=[Image.fromarray(render.render(P,a,e,[],W=600,H=400,scale=110,select=sel,color_by=col,cull=True)) for a,e in angs]
o=Image.new('RGB',(2400,800))
for i,im in enumerate(ims): o.paste(im,((i%4)*600,(i//4)*400))
o.save(out)
