import sys,numpy as np,pickle
sys.path.insert(0,'/home/claude/c12/lib'); sys.path.insert(0,'/home/claude/v3/versions/v3-fusion-ajm3899/scripts')
import geo,mwsoup,rast
from PIL import Image
def load_tex(extra={}):
    T={}
    import glob,os
    for f in glob.glob('/home/claude/c12/z10tex/*.dds'):
        h=int(os.path.basename(f)[:8],16); T[h]=np.asarray(Image.open(f).convert('RGBA'),np.float32)/255
    for h,f in extra.items(): T[h]=np.asarray(Image.open(f).convert('RGBA'),np.float32)/255
    return T
def render_parts(parts,views,out,tex,W=700,H=420,select=None,skin=(0.55,0.57,0.6)):
    S=mwsoup.soup(parts,select or (lambda n: n.endswith('_A') and not any(k in n for k in ['KIT01','KIT02','STYLE','DECAL'])))
    keys=sorted(tex); idx={h:i for i,h in enumerate(keys)}
    tid=np.array([idx.get(int(t),-1) for t in S['tex']])
    col=np.ones((len(S['F']),3),np.float32)
    col[S['tex']==0x9A8AAD9E]=skin; tid[S['tex']==0x9A8AAD9E]=-1
    glass={0x7B220DDF,0xD195BE56,0xE7E4EF49,0x60F8B13C,0x4CDEBFCA,0x0AB88F5D}
    for g in glass: col[S['tex']==g]=(0.12,0.14,0.17)
    texl=[tex[h] for h in keys]
    ims=[Image.fromarray(rast.render(S['P'],S['F'],col,uv=S['UV'],texid=tid,textures=texl,az=a,el=e,W=W,H=H,center=c,scale=s,alphatest=True)[0]) for a,e,c,s in views]
    cols=2; o=Image.new('RGB',(W*cols,H*((len(ims)+cols-1)//cols)))
    for i,m in enumerate(ims): o.paste(m,((i%cols)*W,(i//cols)*H))
    o.save(out)
VIEWS=[(0,5,(2.2,0,0.35),420),(30,8,(2.0,0.62,0.45),900),(330,8,(2.0,-0.62,0.45),900),(20,3,(2.1,0.7,0.25),1300),(180,8,(-2.2,0,0.6),420),(200,10,(-2.05,0.6,0.7),900),(160,10,(-2.05,-0.6,0.7),900),(35,15,None,None),(215,15,None,None),(90,5,None,None)]
if __name__=='__main__':
    P=geo.load(sys.argv[1])
    tex=load_tex({0x95DE5B23:'/home/claude/c12/tex/atlasA.png',0x4B7D95B6:'/home/claude/c12/tex/atlasB.png'})
    render_parts(P,VIEWS,sys.argv[2],tex)
