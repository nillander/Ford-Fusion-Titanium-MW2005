import sys,os;sys.path.insert(0,'/home/claude/c12');sys.path.insert(0,'/home/claude/v3/versions/v3-fusion-ajm3899/scripts')
import numpy as np,mwsoup,geo,rast,glob
from PIL import Image
TEX={}
def tex(d):
    if d not in TEX: TEX[d]={int(os.path.basename(f)[:8],16):np.asarray(Image.open(f).convert('RGB'),np.float32)/255 for f in glob.glob(d+'/*.dds')}
    return TEX[d]
def gouraud(dump,views,out,sel,W=800,H=500,texdir='tex12',k=2,bg=(1,0,1),skin=(0.33,0.62,0.6)):
    T=tex(texdir); P=geo.load(dump)
    S=mwsoup.soup(P,lambda n:any(n.endswith(s) for s in sel))
    F=S['F'];X=S['P'];N=S['N']/np.maximum(np.linalg.norm(S['N'],axis=1,keepdims=True),1e-9);UV=S['UV']
    # per-face base colour: sample texture at face UV centre (solid-ish parts); skin colour for paint
    base=np.zeros((len(F),3),np.float32)
    for h,im in T.items():
        m=S['tex']==h
        if not m.any(): continue
        uv=UV[F[m]].mean(1); H_,W_=im.shape[:2]
        base[m]=im[np.clip((uv[:,1]*H_).astype(int),0,H_-1),np.clip((uv[:,0]*W_).astype(int),0,W_-1)]
    base[S['tex']==0xB637F71F]=skin
    bs=[]
    for i in range(k):
        for j in range(k-i):
            bs.append([(i,j),(i+1,j),(i,j+1)])
            if i+j<k-1: bs.append([(i+1,j),(i+1,j+1),(i,j+1)])
    A=X[F];NA=N[F];Ps=[];Ns=[];Cs=[]
    for tri in bs:
        w=np.array([[(k-a-b)/k,a/k,b/k] for a,b in tri])
        Ps.append(np.einsum('vw,twc->tvc',w,A)); Ns.append(np.einsum('vw,twc->tvc',w,NA)); Cs.append(base)
    Ps=np.concatenate(Ps).reshape(-1,3);Ns=np.concatenate(Ns);Cs=np.concatenate(Cs);Fs=np.arange(len(Ps)).reshape(-1,3)
    ims=[]
    for az,el,c,s in views:
        R,d=rast.view(az,el); L=d+np.array([0,0,0.6]);L/=np.linalg.norm(L)
        n=Ns.mean(1);n/=np.linalg.norm(n,axis=1)[:,None]+1e-9
        dif=np.clip(n@L,0,1); h=L+d;h/=np.linalg.norm(h); sp=np.clip(n@h,0,1)**40
        cc=Cs*(0.3+0.6*dif)[:,None]+(0.35*sp)[:,None]
        im,_=rast.render(Ps,Fs,np.clip(cc,0,1),az=az,el=el,W=W,H=H,center=c,scale=s,shade=False,cull=True,bg=bg)
        ims.append(Image.fromarray(im))
    cols=min(2,len(ims));o=Image.new('RGB',(W*cols,H*((len(ims)+cols-1)//cols)))
    for i,m in enumerate(ims): o.paste(m,((i%cols)*W,(i//cols)*H))
    o.save(out)
