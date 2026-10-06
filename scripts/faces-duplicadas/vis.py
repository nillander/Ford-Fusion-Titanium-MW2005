import numpy as np,ctypes,mwgeo,collections,sys
from scan2 import pairs
lib=ctypes.CDLL('./libidr.so'); fp=ctypes.POINTER(ctypes.c_float); ip=ctypes.POINTER(ctypes.c_int)
def idbuf(Pt,d,W=1600,ext=3.4,sign=1):
    d=d/np.linalg.norm(d); up=np.array([0,0,1.]) if abs(d[2])<0.95 else np.array([1.,0,0])
    r=np.cross(d,up); r/=np.linalg.norm(r); u=np.cross(r,d)
    s=W/(2*ext); X=(Pt@r)*s+W/2; Y=(Pt@u)*s+W/2; Z=-(Pt@d)
    if sign<0: X=W-X
    X=np.ascontiguousarray(X,np.float32);Y=np.ascontiguousarray(Y,np.float32);Z=np.ascontiguousarray(Z,np.float32)
    zb=np.empty(W*W,np.float32); ids=np.empty(W*W,np.int32)
    lib.idbuf(len(Pt),X.ctypes.data_as(fp),Y.ctypes.data_as(fp),Z.ctypes.data_as(fp),W,W,zb.ctypes.data_as(fp),ids.ctypes.data_as(ip))
    return ids
def dirs():
    out=[]
    for el in (2,12,25,40,60,85):
        for az in range(0,360,15):
            a,e=np.radians(az),np.radians(el); out.append(-np.array([np.cos(e)*np.cos(a),np.cos(e)*np.sin(a),np.sin(e)]))
    return out
