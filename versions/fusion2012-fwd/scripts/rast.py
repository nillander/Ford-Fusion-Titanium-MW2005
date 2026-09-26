import ctypes,numpy as np,os
_L=ctypes.CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)),'librast.so'))
def _p(a,t): return a.ctypes.data_as(ctypes.POINTER(t))
def view(az,el):
    a=np.radians(az); e=np.radians(el)
    d=np.array([np.cos(e)*np.cos(a), np.cos(e)*np.sin(a), np.sin(e)])
    up=np.array([0,0,1.]); r=np.cross(up,d); r/=np.linalg.norm(r); u=np.cross(d,r)
    return np.stack([r,u,d]),d
def render(P,F,col,uv=None,texid=None,textures=(),az=35,el=20,W=1200,H=800,scale=None,center=None,
           cull=False,shade=True,bg=(0.55,0.6,0.65),light=(0.4,0.3,0.85),alphatest=False,ortho_d=None):
    """P (nv,3) MW coords; F (n,3); col (n,3) per tri base color; uv (nv,2); texid (n,)"""
    R,d=view(az,el)
    P=np.asarray(P,np.float64); F=np.asarray(F,np.int64)
    cam=P@R.T
    if center is None: center=(cam.min(0)+cam.max(0))/2
    else: center=np.asarray(center)@R.T
    if scale is None:
        ext=cam.max(0)-cam.min(0); scale=0.92*min(W/ext[0],H/ext[1])
    sx=W/2+(cam[:,0]-center[0])*scale; sy=H/2-(cam[:,1]-center[1])*scale; sz=cam[:,2]
    n=np.cross(P[F[:,1]]-P[F[:,0]],P[F[:,2]]-P[F[:,0]]); nl=np.linalg.norm(n,axis=1)+1e-12; n/=nl[:,None]
    keep=np.ones(len(F),bool)
    if cull: keep&=(n@d)>0
    L=np.array(light,float);L/=np.linalg.norm(L)
    c=np.asarray(col,np.float32).copy()
    if shade: c*=(0.35+0.65*np.abs(n@L))[:,None].astype(np.float32)
    idx=np.nonzero(keep)[0]; Fk=F[idx]
    V=np.stack([sx[Fk],sy[Fk],sz[Fk]],-1).astype(np.float32).reshape(-1)
    if uv is None: uv=np.zeros((len(P),2))
    UV=np.asarray(uv,np.float32)[Fk].reshape(-1).copy()
    tid=(np.full(len(F),-1,np.int32) if texid is None else np.asarray(texid,np.int32))[idx].copy()
    C=np.ascontiguousarray(c[idx])
    if textures:
        td=np.concatenate([np.asarray(t,np.float32).reshape(-1,4) for t in textures]).reshape(-1)
        offs=np.cumsum([0]+[t.shape[0]*t.shape[1] for t in textures[:-1]]).astype(np.int64)
        tw=np.array([t.shape[1] for t in textures],np.int32); th=np.array([t.shape[0] for t in textures],np.int32)
    else:
        td=np.zeros(4,np.float32);offs=np.zeros(1,np.int64);tw=np.ones(1,np.int32);th=np.ones(1,np.int32)
    img=np.empty((H,W,3),np.float32); img[:]=bg
    zb=np.full(H*W,-1e30,np.float32); ids=np.full(H*W,-1,np.int32)
    _L.raster(len(idx),_p(V,ctypes.c_float),_p(UV,ctypes.c_float),_p(C,ctypes.c_float),_p(tid,ctypes.c_int),
              _p(td,ctypes.c_float),_p(offs,ctypes.c_int64),_p(tw,ctypes.c_int),_p(th,ctypes.c_int),W,H,
              _p(img,ctypes.c_float),_p(zb,ctypes.c_float),_p(ids,ctypes.c_int),int(alphatest))
    ids=ids.reshape(H,W); ids=np.where(ids>=0,idx[np.maximum(ids,0)],-1)
    return (np.clip(img,0,1)*255).astype(np.uint8),ids
