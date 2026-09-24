import struct, numpy as np
def load(path):
    b=open(path,'rb').read(); o=0
    def rd(fmt):
        nonlocal o; v=struct.unpack_from(fmt,b,o); o+=struct.calcsize(fmt); return v
    n,=rd('<i'); parts=[]
    for _ in range(n):
        l,=rd('<i'); name=b[o:o+l].decode(); o+=l
        h,=rd('<I'); bb=rd('<6f')
        nt,=rd('<i'); tex=list(rd(f'<{nt}I')) if nt else []
        ns,=rd('<i'); sh=list(rd(f'<{ns}I')) if ns else []
        flags,=rd('<i'); ng,=rd('<i'); groups=[]
        for _ in range(ng):
            t=rd('<6B'); fl,vc,tc,off,ln,u1=rd('<6i')
            groups.append(dict(tex=t[:5],shader=t[5],flags=fl,vcount=vc,tris=tc,offset=off,length=ln,unk1=u1))
        nv,=rd('<i')
        vt=np.frombuffer(b,dtype=np.dtype([('p','<3f4'),('n','<3f4'),('c','<i4'),('uv','<2f4')]),count=nv,offset=o); o+=nv*36
        ni,=rd('<i'); idx=np.frombuffer(b,dtype='<u2',count=ni,offset=o); o+=ni*2
        parts.append(dict(name=name,hash=h,bmin=bb[:3],bmax=bb[3:],tex=tex,shaders=sh,flags=flags,groups=groups,v=vt,idx=idx))
    return parts
