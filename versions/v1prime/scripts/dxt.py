import numpy as np
def _565(c):
    c=np.clip(c,0,255).astype(np.int32)
    return ((c[...,0]>>3)<<11)|((c[...,1]>>2)<<5)|(c[...,2]>>3)
def _from565(v):
    r=((v>>11)&31)*255//31; g=((v>>5)&63)*255//63; b=(v&31)*255//31
    return np.stack([r,g,b],-1).astype(np.float32)
def encode_dxt3(rgba):
    H,W,_=rgba.shape; a=rgba.astype(np.float32)
    blocks=a.reshape(H//4,4,W//4,4,4).transpose(0,2,1,3,4).reshape(-1,16,4)
    rgb=blocks[...,:3]; al=blocks[...,3]
    # endpoints along principal extent: use min/max of luminance-projected colors
    mean=rgb.mean(1,keepdims=True); d=rgb-mean
    cov=np.einsum('bki,bkj->bij',d,d)
    axis=np.ones((len(rgb),3),np.float32)
    for _ in range(4): axis=np.einsum('bij,bj->bi',cov,axis); axis/=np.linalg.norm(axis,axis=1,keepdims=True)+1e-9
    proj=np.einsum('bki,bi->bk',d,axis)
    c0=mean[:,0]+axis*proj.max(1,keepdims=True); c1=mean[:,0]+axis*proj.min(1,keepdims=True)
    e0=_565(c0); e1=_565(c1)
    swap=e0<e1; e0,e1=np.where(swap,e1,e0),np.where(swap,e0,e1)
    p0=_from565(e0); p1=_from565(e1)
    pal=np.stack([p0,p1,(2*p0+p1)/3,(p0+2*p1)/3],1)  # b,4,3
    dist=((rgb[:,:,None,:]-pal[:,None,:,:])**2).sum(-1); idx=dist.argmin(-1).astype(np.uint32)
    eq=e0==e1; idx[eq]=0
    code=np.zeros(len(rgb),np.uint32)
    for k in range(16): code|=idx[:,k]<<(2*k)
    a4=np.clip(np.round(al/17),0,15).astype(np.uint64)
    abits=np.zeros(len(rgb),np.uint64)
    for k in range(16): abits|=a4[:,k]<<np.uint64(4*k)
    out=np.zeros((len(rgb),16),np.uint8)
    out[:,0:8]=abits.view(np.uint8).reshape(-1,8)
    out[:,8:10]=e0.astype('<u2').view(np.uint8).reshape(-1,2)
    out[:,10:12]=e1.astype('<u2').view(np.uint8).reshape(-1,2)
    out[:,12:16]=code.astype('<u4').view(np.uint8).reshape(-1,4)
    return out.tobytes()
def write_dds_like(template_path,out_path,rgba):
    hdr=bytearray(open(template_path,'rb').read()[:128])
    import struct
    H,W,_=rgba.shape
    assert hdr[84:88]==b'DXT3'
    struct.pack_into('<I',hdr,12,H); struct.pack_into('<I',hdr,16,W)
    struct.pack_into('<I',hdr,20,H*W)  # linear size DXT3 = W*H bytes
    struct.pack_into('<I',hdr,28,1)    # mip count
    flags=struct.unpack_from('<I',hdr,8)[0]&~0x20000; struct.pack_into('<I',hdr,8,flags)
    open(out_path,'wb').write(bytes(hdr)+encode_dxt3(rgba))

def encode_dxt1(rgba):
    import numpy as np
    full=encode_dxt3(rgba)  # reuse colour block encoding (4-colour mode, c0>c1 enforced)
    b=np.frombuffer(full,np.uint8).reshape(-1,16)[:,8:16]
    # ensure 4-colour mode: when c0==c1 index 0 only -> fine; when c0<c1 encode_dxt3 already swapped
    return b.tobytes()
def write_dds_dxt1(template_path,out_path,rgba):
    import struct
    hdr=bytearray(open(template_path,'rb').read()[:128])
    H,W,_=rgba.shape
    struct.pack_into('<I',hdr,12,H); struct.pack_into('<I',hdr,16,W)
    struct.pack_into('<I',hdr,20,H*W//2); struct.pack_into('<I',hdr,28,1)
    flags=struct.unpack_from('<I',hdr,8)[0]&~0x20000; struct.pack_into('<I',hdr,8,flags)
    hdr[84:88]=b'DXT1'
    open(out_path,'wb').write(bytes(hdr)+encode_dxt1(rgba))
