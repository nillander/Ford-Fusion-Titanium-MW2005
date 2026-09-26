"""Perspective textured render (game-like) on top of rast: camera at E looking at target."""
import sys;sys.path.insert(0,'/home/claude/c12');sys.path.insert(0,'/home/claude/v3/versions/v3-fusion-ajm3899/scripts')
import numpy as np,geo,mwsoup,rast,glob,os
from PIL import Image
_T={}
def tex(texdir):
    if texdir not in _T: _T[texdir]={int(os.path.basename(f)[:8],16):np.asarray(Image.open(f).convert('RGBA'),np.float32)/255 for f in glob.glob(texdir+'/*.dds')}
    return _T[texdir]
def shot(S,T,E,tgt,fov=40,W=640,H=480,skin=(0.35,0.72,0.68)):
    keys=sorted(T); idx={h:i for i,h in enumerate(keys)}
    tid=np.array([idx.get(int(t),-1) for t in S['tex']]); col=np.ones((len(S['F']),3),np.float32)
    m=np.isin(S['tex'],[0xB637F71F,0x9A8AAD9E]); col[m]=skin; tid[m]=-1
    E=np.array(E,float); f=np.array(tgt,float)-E; f/=np.linalg.norm(f); rr=np.cross(f,[0,0,1.]); rr/=np.linalg.norm(rr); uu=np.cross(rr,f)
    v=S['P']-E; z=v@f; z=np.maximum(z,0.05)
    Pp=np.c_[-z,v@rr/z,v@uu/z]
    s=(W/2)/np.tan(np.radians(fov/2))
    # light from camera-ish, in the transformed space direction does not matter much
    im=rast.render(Pp,S['F'],col,uv=S['UV'],texid=tid,textures=[T[h] for h in keys],az=0,el=0,W=W,H=H,center=(0,0,0),scale=s,alphatest=True,cull=True,bg=(1,0,1),light=(1,0.3,0.6))[0]
    return Image.fromarray(im)
def run(dump,texdir,cams,out,sel=('_A',),W=640,H=480):
    T=tex(texdir); P=geo.load(dump); S=mwsoup.soup(P,lambda n:any(n.endswith(s) for s in sel) and 'DECAL' not in n and ('KIT0' not in n or 'KIT00' in n))
    ims=[shot(S,T,E,t,fov,W,H) for E,t,fov in cams]
    o=Image.new('RGB',(W*len(ims),H))
    for i,m in enumerate(ims): o.paste(m,(i*W,0))
    o.save(out)
if __name__=='__main__':
    cams=[((-3.2,1.35,0.95),(-2.1,0.62,0.76),38),((-3.3,-1.2,0.9),(-2.1,-0.62,0.76),38)]
    run(sys.argv[1],'tex_T12_33',cams,sys.argv[2])
