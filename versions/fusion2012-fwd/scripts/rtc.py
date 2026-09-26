import sys;sys.path.insert(0,'/home/claude/c12');sys.path.insert(0,'/home/claude/v3/versions/v3-fusion-ajm3899/scripts')
import numpy as np,geo,mwsoup,rast,glob,os
from PIL import Image
def render(dump,texdir,views,out,sel,W=700,H=380,cull=True,bg=(1,0,1),glass_alpha=None):
    T={int(os.path.basename(f)[:8],16):np.asarray(Image.open(f).convert('RGBA'),np.float32)/255 for f in glob.glob(texdir+'/*.dds')}
    P=geo.load(dump); S=mwsoup.soup(P,lambda n:any(n.endswith(s) for s in sel))
    keys=sorted(T); idx={h:i for i,h in enumerate(keys)}
    tid=np.array([idx.get(int(t),-1) for t in S['tex']]); col=np.ones((len(S['F']),3),np.float32)
    m=S['tex']==0xB637F71F; col[m]=(0.35,0.72,0.68); tid[m]=-1
    ims=[]
    for az,el,c,s in views:
        R,d=rast.view(az,el)
        ims.append(Image.fromarray(rast.render(S['P'],S['F'],col,uv=S['UV'],texid=tid,textures=[T[h] for h in keys],az=az,el=el,W=W,H=H,center=c,scale=s,alphatest=True,cull=cull,bg=bg,light=tuple(d*0.7+np.array([0,0,0.5])))[0]))
    o=Image.new('RGB',(W*len(ims),H))
    for i,m in enumerate(ims): o.paste(m,(i*W,0))
    o.save(out)
