"""Perspective textured render with per-vertex-normal (Gouraud-like) lighting + specular: shows dark marks from bad normals."""
import sys;sys.path.insert(0,'/home/claude/c12');sys.path.insert(0,'/home/claude/v3/versions/v3-fusion-ajm3899/scripts')
import numpy as np,geo,mwsoup,rast,persp
from PIL import Image
SKINS=(0xB637F71F,0x9A8AAD9E)
def default_sel(n):
    if not n.endswith('_A') or 'DECAL' in n or 'DRIVER' in n: return False
    if 'KIT0' in n and 'KIT00' not in n: return False
    if 'STYLE' in n or 'SCOOP' in n or 'SPOILER' in n: return False
    return True
def subdiv(S,k=2):
    F=S['F'];X=S['P'];N=S['N']/np.maximum(np.linalg.norm(S['N'],axis=1,keepdims=True),1e-9);UV=S['UV']
    tris=[]
    for i in range(k):
        for j in range(k-i):
            tris.append([(i,j),(i+1,j),(i,j+1)])
            if i+j<k-1: tris.append([(i+1,j),(i+1,j+1),(i,j+1)])
    Ps=[];Ns=[];Us=[];Ti=[]
    for tri in tris:
        w=np.array([[(k-a-b)/k,a/k,b/k] for a,b in tri])
        Ps.append(np.einsum('vw,twc->tvc',w,X[F]));Ns.append(np.einsum('vw,twc->tvc',w,N[F]));Us.append(np.einsum('vw,twc->tvc',w,UV[F]));Ti.append(S['tex'])
    return np.concatenate(Ps),np.concatenate(Ns),np.concatenate(Us),np.concatenate(Ti)
def shot(Pt,Nt,Ut,Tt,T,E,tgt,fov=34,W=620,H=440,skin=(0.33,0.62,0.6)):
    keys=sorted(T); idx={h:i for i,h in enumerate(keys)}
    tid=np.array([idx.get(int(t),-1) for t in Tt]); sk=np.isin(Tt,SKINS); tid[sk]=-1
    E=np.array(E,float); f=np.array(tgt,float)-E; f/=np.linalg.norm(f); rr=np.cross(f,[0,0,1.]); rr/=np.linalg.norm(rr); uu=np.cross(rr,f)
    # lighting: key light from above-camera side + specular (env-like) using per-sub-tri vertex normals
    L=-f+np.array([0,0,1.2]); L/=np.linalg.norm(L)
    n=Nt.mean(1); n/=np.linalg.norm(n,axis=1)[:,None]+1e-9
    C=Pt.mean(1); v=E-C; v/=np.linalg.norm(v,axis=1)[:,None]
    dif=np.clip(n@L,0,1); hh=L[None]+v; hh/=np.linalg.norm(hh,axis=1)[:,None]; sp=np.clip((n*hh).sum(1),0,1)**30
    lit=(0.25+0.7*dif)[:,None]*np.where(sk[:,None],np.array(skin,np.float32)[None],1.0)+0.4*sp[:,None]
    V=Pt.reshape(-1,3)-E; z=np.maximum(V@f,0.05); Pp=np.c_[-z,V@rr/z,V@uu/z]
    s=(W/2)/np.tan(np.radians(fov/2)); Fs=np.arange(len(Pp)).reshape(-1,3)
    im=rast.render(Pp,Fs,np.clip(lit,0,1).astype(np.float32),uv=Ut.reshape(-1,2),texid=tid,textures=[T[h] for h in keys],az=0,el=0,W=W,H=H,center=(0,0,0),scale=s,alphatest=True,cull=True,bg=(1,0,1),shade=False)[0]
    return Image.fromarray(im)
def run(dump,texdir,cams,out,sel=default_sel,W=620,H=440,cols=3):
    T=persp.tex(texdir); S=mwsoup.soup(geo.load(dump),sel); Pt,Nt,Ut,Tt=subdiv(S)
    ims=[shot(Pt,Nt,Ut,Tt,T,E,t,fov,W,H) for E,t,fov in cams]
    rows=(len(ims)+cols-1)//cols; o=Image.new('RGB',(W*cols,H*rows))
    for i,m in enumerate(ims): o.paste(m,((i%cols)*W,(i//cols)*H))
    o.save(out)
CAMS=[((4.2,2.0,1.1),(1.7,0.3,0.55),34),((4.6,0,1.0),(2.0,0,0.5),34),((4.2,-2.0,1.1),(1.7,-0.3,0.55),34),
      ((-4.2,2.0,1.1),(-1.8,0.3,0.6),34),((-4.6,0,1.0),(-2.1,0,0.55),34),((-4.2,-2.0,1.1),(-1.8,-0.3,0.6),34)]
if __name__=='__main__': run(sys.argv[1],sys.argv[2],CAMS,sys.argv[3])
