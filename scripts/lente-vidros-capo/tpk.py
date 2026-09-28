import struct, numpy as np
def chunks(b,o,end,out):
    while o+8<=end:
        t,l=struct.unpack_from('<Ii',b,o)
        out.append((t,o+8,o+8+l))
        if t&0x80000000: chunks(b,o+8,o+8+l,out)
        o+=8+l
def load(path):
    b=open(path,'rb').read(); C=[]; chunks(b,0,len(b),C)
    infos=[c for c in C if c[0]==0x33310004]; datas=[c for c in C if c[0]==0x33320002]
    T={}
    for (t,s,e),(t2,ds,de) in zip(infos,datas):
        p=s
        while p+0x9C<=e:
            name=b[p+12:p+36].split(b'\0')[0].decode('latin1'); h,=struct.unpack_from('<I',b,p+36)
            off,poff,tl=struct.unpack_from('<III',b,p+48); w,hh=struct.unpack_from('<HH',b,p+68)
            fmt,=struct.unpack_from('<I',b,p+0x9C-12)
            T[h]=dict(name=name,off=off,len=tl,w=w,h=hh,fmt=fmt,ds=ds,de=de,b=b)
            p+=0x9C
    # find data base: first 0x80-aligned position within data chunk
    for h,x in T.items():
        x['base']=(x['ds']+0x7F)//0x80*0x80
    return T
def c565(c):
    r=((c>>11)&31)*255//31; g=((c>>5)&63)*255//63; bl=(c&31)*255//31
    return np.stack([r,g,bl],-1).astype(np.float32)
def decode(x):
    b=x['b']; w,h=x['w'],x['h']; fmt=x['fmt']
    bs=8 if fmt==0x31545844 else 16
    n=(w//4)*(h//4); raw=np.frombuffer(b,np.uint8,count=n*bs,offset=x['base']+x['off']).reshape(h//4,w//4,bs)
    col=raw[...,bs-8:]
    c0=col[...,0].astype(np.uint32)|(col[...,1].astype(np.uint32)<<8); c1=col[...,2].astype(np.uint32)|(col[...,3].astype(np.uint32)<<8)
    C0=c565(c0);C1=c565(c1)
    four=(c0>c1)|(bs==16)
    C2=np.where(four[...,None],(2*C0+C1)/3,(C0+C1)/2); C3=np.where(four[...,None],(C0+2*C1)/3,0)
    pal=np.stack([C0,C1,C2,C3],-2) # H W 4 3
    bits=col[...,4:8].astype(np.uint32); bits=bits[...,0]|(bits[...,1]<<8)|(bits[...,2]<<16)|(bits[...,3]<<24)
    idx=np.stack([(bits>>(2*i))&3 for i in range(16)],-1) # H W 16
    rgb=np.take_along_axis(pal[...,None,:,:].repeat(16,2) if False else pal,idx[...,None].repeat(3,-1)[...,:,:] if False else idx[...,None],axis=2) if False else None
    Hh,Ww=idx.shape[:2]
    rgb=pal[np.arange(Hh)[:,None,None],np.arange(Ww)[None,:,None],idx]  # H W 16 3
    if bs==16:
        a=raw[...,:8].astype(np.uint32); ab=np.stack([(a[...,i//2]>>(4*(i%2)))&15 for i in range(16)],-1)*17
    else:
        ab=np.where((~four[...,None])&(idx==3),0,255)
    out=np.concatenate([rgb,ab[...,None].astype(np.float32)],-1).reshape(Hh,Ww,4,4,4).transpose(0,2,1,3,4).reshape(h,w,4)
    return out.astype(np.uint8)
def load2(path):
    b=open(path,'rb').read(); C=[]; chunks(b,0,len(b),C)
    T={}
    for t,s,e in C:
        if t!=0x33310003: continue
        for i in range((e-s)//24):
            h,off,ln,rl,fl,pad=struct.unpack_from('<6I',b,s+24*i)
            assert b[off:off+4]==b'RAWW'
            a,bb=struct.unpack_from('<ii',b,off+8); pitch=a-0x9c
            ip=off+16+pitch
            name=b[ip+12:ip+36].split(b'\0')[0].decode('latin1')
            w,hh=struct.unpack_from('<HH',b,ip+68); fmt,=struct.unpack_from('<I',b,ip+0x9C-12)
            T[h]=dict(name=name,w=w,h=hh,fmt=fmt,base=off+16,off=0,b=b,len=pitch)
    return T
