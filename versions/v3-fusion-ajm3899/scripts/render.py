import numpy as np, geo, sys, os
from PIL import Image
_texcache={}
def tex(h, dirs):
    if h in _texcache: return _texcache[h]
    im=None
    for d in dirs:
        p=os.path.join(d,'%08X.dds'%h)
        if os.path.exists(p):
            try: im=np.asarray(Image.open(p).convert('RGBA')).astype(np.float32)/255
            except Exception as e: print('tex fail',p,e)
            break
    _texcache[h]=im; return im
def view_matrix(az,el):
    a=np.radians(az); e=np.radians(el)
    # camera looks toward origin from direction d
    d=np.array([np.cos(e)*np.cos(a), np.cos(e)*np.sin(a), np.sin(e)])
    up=np.array([0,0,1.]); r=np.cross(up,d); r/=np.linalg.norm(r); u=np.cross(d,r)
    return np.stack([r,u,d]), d
def render(parts, az, el, texdirs, W=900, H=600, scale=170, select=None, color_by=None, light=None, cull=False, smooth=False):
    R,d=view_matrix(az,el)
    img=np.ones((H,W,3),np.float32)*np.array([0.55,0.6,0.65]); zb=np.full((H,W),-1e9,np.float32)
    L=np.array([0.4,0.3,0.85]); L/=np.linalg.norm(L)
    for pi,p in enumerate(parts):
        if select and not select(p['name']): continue
        v=p['v']; P=v['p'].astype(np.float64); UV=v['uv']
        cam=P@R.T
        sx=W/2+cam[:,0]*scale; sy=H/2-cam[:,1]*scale+40; sz=cam[:,2]
        for gi,g in enumerate(p['groups']):
            seg=p['idx'][g['offset']:g['offset']+g['length']].astype(np.int64)
            if len(seg)<3: continue
            tris=seg[:len(seg)//3*3].reshape(-1,3)
            ti=g['tex'][0]; th=p['tex'][ti] if ti<len(p['tex']) else None
            T=tex(th,texdirs) if th is not None else None
            base=np.array(color_by(p,gi)) if color_by else None
            for a,b,c in tris:
                x0,x1,x2=sx[a],sx[b],sx[c]; y0,y1,y2=sy[a],sy[b],sy[c]
                area=(x1-x0)*(y2-y0)-(x2-x0)*(y1-y0)
                if abs(area)<1e-9: continue
                minx=max(int(min(x0,x1,x2)),0); maxx=min(int(max(x0,x1,x2))+1,W-1)
                miny=max(int(min(y0,y1,y2)),0); maxy=min(int(max(y0,y1,y2))+1,H-1)
                if minx>maxx or miny>maxy: continue
                n=np.cross(P[b]-P[a],P[c]-P[a]); nn=np.linalg.norm(n)
                if nn==0: continue
                n/=nn
                if cull and n@d<0: continue
                shade=0.35+0.65*abs(n@L)
                xs,ys=np.meshgrid(np.arange(minx,maxx+1)+0.5,np.arange(miny,maxy+1)+0.5)
                w0=((x1-xs)*(y2-ys)-(x2-xs)*(y1-ys))/area
                w1=((x2-xs)*(y0-ys)-(x0-xs)*(y2-ys))/area
                w2=1-w0-w1
                m=(w0>=0)&(w1>=0)&(w2>=0)
                if not m.any(): continue
                z=w0*sz[a]+w1*sz[b]+w2*sz[c]
                sub=zb[miny:maxy+1,minx:maxx+1]
                m&=z>sub
                if not m.any(): continue
                sub[m]=z[m]
                if base is not None: col=np.broadcast_to(base,(m.sum(),3))
                elif T is not None:
                    u=w0*UV[a,0]+w1*UV[b,0]+w2*UV[c,0]; vv=w0*UV[a,1]+w1*UV[b,1]+w2*UV[c,1]
                    th_,tw_=T.shape[:2]
                    tx=(np.mod(u[m],1)*tw_).astype(int)%tw_; ty=(np.mod(vv[m],1)*th_).astype(int)%th_
                    col=T[ty,tx,:3]
                else: col=np.broadcast_to(np.array([0.8,0.8,0.8]),(m.sum(),3))
                if smooth:
                    N=p['v']['n']
                    nn_=(w0[m,None]*N[a]+w1[m,None]*N[b]+w2[m,None]*N[c]); nn_/=np.linalg.norm(nn_,axis=1,keepdims=True)+1e-9
                    ncam=nn_@R.T
                    refl=0.5+0.5*np.sin(ncam[:,1]*9)  # banded env to expose normal noise
                    sh=(0.3+0.4*np.abs(nn_@L)+0.3*refl)[:,None]
                    img[miny:maxy+1,minx:maxx+1][m]=col*sh
                else:
                    img[miny:maxy+1,minx:maxx+1][m]=col*shade
    return (np.clip(img,0,1)*255).astype(np.uint8)
VIEWS={'front':(0,8),'rear':(180,8),'side':(90,5),'persp':(35,20),'rear34':(215,20),'top':(90,80)}
if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser(); ap.add_argument('dump'); ap.add_argument('out'); ap.add_argument('--tex',nargs='*',default=[])
    ap.add_argument('--views',default='persp,rear34'); ap.add_argument('--lod',default='A'); ap.add_argument('--only',default=None); ap.add_argument('--exclude',default=None); ap.add_argument('--cull',action='store_true')
    a=ap.parse_args()
    parts=geo.load(a.dump)
    def sel(n):
        if a.only and not any(s in n for s in a.only.split(',')): return False
        if a.exclude and any(s in n for s in a.exclude.split(',')): return False
        return n.endswith('_'+a.lod) or (a.lod=='A' and False)
    ims=[Image.fromarray(render(parts,*VIEWS[v],a.tex,select=sel,cull=a.cull)) for v in a.views.split(',')]
    W=sum(i.width for i in ims); out=Image.new('RGB',(W,ims[0].height)); x=0
    for i in ims: out.paste(i,(x,0)); x+=i.width
    out.save(a.out); print('saved',a.out)
