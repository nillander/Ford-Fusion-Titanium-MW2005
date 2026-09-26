import sys,pickle,numpy as np
sys.path.insert(0,'/home/claude/c12/lib'); import rast
from PIL import Image
S=pickle.load(open('oracle_soup.pkl','rb'))
D='/mnt/user-data/uploads/fusion-mw2005/source/fusion-2016-dev/DEV Version/FordFusion/'
fari=np.asarray(Image.open(D+'fari.PNG').convert('RGBA'),np.float32)/255
red=np.asarray(Image.open(D+'redglass.png').convert('RGBA'),np.float32)/255
P=np.c_[S['P'][:,1],-S['P'][:,0],S['P'][:,2]]
sh=S['shader']; F=S['F']
col=np.tile([0.75,0.75,0.78],(len(F),1)).astype(np.float32)
col[sh==4]=[0.12,0.12,0.12]; col[sh==9]=[0.6,0.62,0.66]; col[(sh>=15)&(sh!=16)]=[0.2,0.25,0.3]
col[sh==14]=[1,1,1]; col[sh==10]=[1,1,1]; col[sh==16]=[1,1,1]
tid=np.full(len(F),-1); tid[(sh==10)|(sh==14)]=0; tid[sh==16]=1
views=[(float(a),float(b)) for a,b in [x.split(':') for x in sys.argv[2].split(',')]]
ims=[]
sel=np.ones(len(F),bool)
if len(sys.argv)>3: exec(sys.argv[3])
for az,el in views:
    im,_=rast.render(P,F[sel],col[sel],uv=S['UV'],texid=tid[sel],textures=[fari,red],az=az,el=el,W=900,H=600,cull=False)
    ims.append(Image.fromarray(im))
out=Image.new('RGB',(900*len(ims),600))
for i,m in enumerate(ims): out.paste(m,(900*i,0))
out.save(sys.argv[1])
