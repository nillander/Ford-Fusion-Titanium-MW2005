import sys,pickle,numpy as np
sys.path.insert(0,'/home/claude/c12/lib'); sys.path.insert(0,'/home/claude/v3/versions/v3-fusion-ajm3899/scripts')
import mwsoup,geo,rast
from PIL import Image
A=pickle.load(open('/home/claude/c12/align0.pkl','rb'))
def gta2mw(G,H=None):
    H=A['Hf'] if H is None else H
    M0=np.c_[G[:,1]*A['sx']+A['tx'],-G[:,0],G[:,2]+0.42]
    return (np.c_[M0,np.ones(len(M0))]@H.T)[:,:3]
def gta2mw_n(N,H=None):
    H=A['Hf'] if H is None else H
    L=H[:3,:3]@np.diag([A['sx'],1,1])
    # map gta normal -> mw axes then inverse-transpose
    n0=np.c_[N[:,1],-N[:,0],N[:,2]]
    J=H[:3,:3]@np.diag([A['sx'],1,1])  # jacobian in mw-axis basis (approx: sx applies to x)
    n=n0@np.linalg.inv(J)
    return n/np.maximum(np.linalg.norm(n,axis=1,keepdims=True),1e-12)
S=pickle.load(open('/home/claude/c12/gta/oracle_soup.pkl','rb'))
S['M']=gta2mw(S['P'])
D='/mnt/user-data/uploads/fusion-mw2005/source/fusion-2016-dev/DEV Version/FordFusion/'
FARI=np.asarray(Image.open(D+'fari.PNG').convert('RGBA'),np.float32)/255
RED=np.asarray(Image.open(D+'redglass.png').convert('RGBA'),np.float32)/255
def mcol(S):
    sh=S['shader']; F=S['F']
    col=np.tile([0.75,0.75,0.78],(len(F),1)).astype(np.float32)
    col[sh==4]=[0.12,0.12,0.12]; col[sh==9]=[0.6,0.62,0.66]; col[(sh>=15)&(sh!=16)]=[0.2,0.25,0.3]
    col[(sh==14)|(sh==10)|(sh==16)]=1
    tid=np.full(len(F),-1); tid[(sh==10)|(sh==14)]=0; tid[sh==16]=1
    return col,tid
Z=geo.load('/home/claude/c12/z10.dump')
def zsoup(extra=lambda n:True):
    return mwsoup.soup(Z,lambda n: n.endswith('_A') and not any(k in n for k in ['KIT01','KIT02','STYLE','DECAL','TIRE','BRAKE_A','DRIVER']) and extra(n))
def zcol(ZS):
    th=np.unique(ZS['tex']); rng=np.random.default_rng(1); cmap={t:rng.uniform(0.3,1,3) for t in th}
    col=np.array([cmap[t] for t in ZS['tex']],np.float32); col[ZS['tex']==0x9A8AAD9E]=[0.78,0.78,0.8]; return col
def row(ims,path):
    W=sum(i.width for i in ims);H=max(i.height for i in ims);o=Image.new('RGB',(W,H));x=0
    for i in ims: o.paste(i,(x,0)); x+=i.width
    o.save(path)
